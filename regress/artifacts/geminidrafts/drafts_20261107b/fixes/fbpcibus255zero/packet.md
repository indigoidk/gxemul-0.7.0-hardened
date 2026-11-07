# GXemul hardened fork -- DRAFT A FIX for one filed issue, `fbpcibus255zero` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at lines the coordinator LOCATED from names the row uses (the row cites none) (HEAD 8d9df658).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `fbpcibus255zero`, state `open`, severity `MED`)

**title:** A PCI-config read decoding to bus 255 returns 0, not the no-device answer

**state_note (head):**

GOVERNING TEXT (from the dispositions file, cut at 400 characters): CONFIRMED-NEW MED `fbpcibus255zero` "A PCI-config read decoding to bus 255 returns 0, not the no-device answer".** `dev_footbridge.c:486-491`: after `bus_pci_setaddr`, bus 255 prints and `return 1` BEFORE `bus_pci_data_access()` (`:498-499`) and before the read writeback (`:501-502`); `memory_rw.c:491-492` has pre-zeroed the buffer, so the guest reads 0. Everywhere else an absent device...

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- PCI empty bus reads should return 0xFFFFFFFF instead of leaving the pre-zeroed 0

## The code at the cited lines

### `src/devices/dev_footbridge.c` around line 489 -- LOCATED BY THE COORDINATOR from the name `bus_pci_setaddr` the row uses (the row cites no line; check this is the defect's site) (HEAD 8d9df658, lines 369-609)

```c
  369| 
  370| 	for (i=0; i<N_FOOTBRIDGE_TIMERS; i++) {
  371| 		if (d->timer_control[i] & TIMER_ENABLE) {
  372| 			if (d->pending_timer_interrupts[i] > 0) {
  373| 				/*  #432: the same never-zero span, WITHOUT the
  374| 				    prescaler -- this is a 24-bit counter, and the
  375| 				    prescaler slows the rate rather than widening
  376| 				    it.  */
  377| 				d->timer_value[i] = random() %
  378| 				    footbridge_effective_cycles(d->timer_load[i],
  379| 				    d->timer_control[i], 0);
  380| 				INTERRUPT_ASSERT(d->timer_irq[i]);
  381| 			}
  382| 		}
  383| 	}
  384| }
  385| 
  386| 
  387| /*
  388|  *  footbridge_interrupt_assert():
  389|  */
  390| void footbridge_interrupt_assert(struct interrupt *interrupt)
  391| {
  392| 	struct footbridge_data *d = (struct footbridge_data *) interrupt->extra;
  393| 	d->irq_status |= interrupt->line;
  394| 
  395| 	// Patch from NetBSD:
  396| 	// "fix hang interrupt issue. Always assert the irq's even if we have
  397| 	//  already asserted the global irq for the device. prevents hangs with
  398| 	//  cats."
  399| 	if ((d->irq_status & d->irq_enable) /* && !d->irq_asserted */) {
  400| 		d->irq_asserted = 1;
  401| 		INTERRUPT_ASSERT(d->irq);
  402| 	}
  403| }
  404| 
  405| 
  406| /*
  407|  *  footbridge_interrupt_deassert():
  408|  */
  409| void footbridge_interrupt_deassert(struct interrupt *interrupt)
  410| {
  411| 	struct footbridge_data *d = (struct footbridge_data *) interrupt->extra;
  412| 	d->irq_status &= ~interrupt->line;
  413| 
  414| 	if (!(d->irq_status & d->irq_enable) && d->irq_asserted) {
  415| 		d->irq_asserted = 0;
  416| 		INTERRUPT_DEASSERT(d->irq);
  417| 	}
  418| }
  419| 
  420| 
  421| /*
  422|  *  Reading the byte at 0x79000000 is a quicker way to figure out which ISA
  423|  *  interrupt has occurred (and acknowledging it at the same time), than
  424|  *  dealing with the legacy 0x20/0xa0 ISA ports.
  425|  */
  426| DEVICE_ACCESS(footbridge_isa)
  427| {
  428| 	/*  struct footbridge_data *d = extra;  */
  429| 	uint64_t idata = 0, odata = 0;
  430| 	int x;
  431| 
  432| 	if (writeflag == MEM_WRITE) {
  433| 		idata = memory_readmax64(cpu, data, len);
  434| 		fatal("[ footbridge_isa: WARNING/TODO: write! idata = 0x%016" PRIx64" ]\n", idata);
  435| 	}
  436| 
  437| 	x = cpu->machine->isa_pic_data.last_int;
  438| 	if (x < 8)
  439| 		odata = cpu->machine->isa_pic_data.pic1->irq_base + x;
  440| 	else
  441| 		odata = cpu->machine->isa_pic_data.pic2->irq_base + x - 8;
  442| 
  443| 	if (writeflag == MEM_READ)
  444| 		memory_writemax64(cpu, data, len, odata);
  445| 
  446| 	return 1;
  447| }
  448| 
  449| 
  450| /*
  451|  *  Reset pin at ISA port 0x338, at least in the NetWinder:
  452|  *
  453|  *  TODO: NOT WORKING YET!
  454|  */
  455| DEVICE_ACCESS(footbridge_reset)
  456| {
  457| 	uint64_t idata = 0;
  458| 
  459| 	if (writeflag == MEM_WRITE) {
  460| 		idata = memory_readmax64(cpu, data, len);
  461| 		if (idata & 0x40) {
  462| 			debug("[ footbridge_reset: GP16: Halting. ]\n");
  463| 			/*  #220: (Codex/Fable) cpu->running=0 already halts cleanly;
  464| 			    the col-0 exit(1) was a debug hack that kills the host.  */
  465| 			cpu->running = 0;
  466| 		}
  467| 	}
  468| 
  469| 	return 1;
  470| }
  471| 
  472| 
  473| /*
  474|  *  The Footbridge PCI configuration space is implemented as a direct memory
  475|  *  space (i.e. not one port for addr and one port for data). This function
  476|  *  translates that into bus_pci calls.
  477|  */
  478| DEVICE_ACCESS(footbridge_pci)
  479| {
  480| 	struct footbridge_data *d = (struct footbridge_data *) extra;
  481| 	uint64_t idata = 0, odata = 0;
  482| 	int bus, dev, func, reg;
  483| 
  484| 	if (writeflag == MEM_WRITE)
  485| 		idata = memory_readmax64(cpu, data, len|MEM_PCI_LITTLE_ENDIAN);
  486| 
  487| 	/*  Decompose the (direct) address into its components:  */
  488| 	bus_pci_decompose_1(relative_addr, &bus, &dev, &func, &reg);
  489| 	bus_pci_setaddr(cpu, d->pcibus, bus, dev, func, reg);
  490| 
  491| 	if (bus == 255) {
  492| 		fatal("[ footbridge DEBUG ERROR: bus 255 unlikely,"
  493| 		    " pc (might not be updated) = 0x%08x ]\n", (int)cpu->pc);
  494| 		/*  #220: (Codex/Fable) don't exit() the host on a guest PCI
  495| 		    access to the (unlikely) bus 255; treat it as handled.  */
  496| 		return 1;
  497| 	}
  498| 
  499| 	debug("[ footbridge pci: %s bus %i, device %i, function %i, register "
  500| 	    "%i ]\n", writeflag == MEM_READ? "read from" : "write to", bus,
  501| 	    dev, func, reg);
  502| 
  503| 	bus_pci_data_access(cpu, d->pcibus, writeflag == MEM_READ?
  504| 	    &odata : &idata, len, writeflag);
  505| 
  506| 	if (writeflag == MEM_READ)
  507| 		memory_writemax64(cpu, data, len|MEM_PCI_LITTLE_ENDIAN, odata);
  508| 
  509| 	return 1;
  510| }
  511| 
  512| 
  513| DEVICE_ACCESS(footbridge)
  514| {
  515| 	struct footbridge_data *d = (struct footbridge_data *) extra;
  516| 	uint64_t idata = 0, odata = 0;
  517| 	int timer_nr = 0;
  518| 
  519| 	if (writeflag == MEM_WRITE)
  520| 		idata = memory_readmax64(cpu, data, len);
  521| 
  522| 	if (relative_addr >= TIMER_1_LOAD && relative_addr <= TIMER_4_CLEAR) {
  523| 		timer_nr = (relative_addr >> 5) & (N_FOOTBRIDGE_TIMERS - 1);
  524| 		relative_addr &= ~0x060;
  525| 	}
  526| 
  527| 	switch (relative_addr) {
  528| 
  529| 	case VENDOR_ID:
  530| 		odata = 0x1011;  /*  DC21285_VENDOR_ID  */
  531| 		break;
  532| 
  533| 	case DEVICE_ID:
  534| 		odata = 0x1065;  /*  DC21285_DEVICE_ID  */
  535| 		break;
  536| 
  537| 	case 0x04:
  538| 	case 0x0c:
  539| 	case 0x10:
  540| 	case 0x14:
  541| 	case 0x18:
  542| 		/*  TODO. Written to by Linux.  */
  543| 		break;
  544| 
  545| 	case REVISION:
  546| 		odata = 3;  /*  footbridge revision number  */
  547| 		break;
  548| 
  549| 	case PCI_ADDRESS_EXTENSION:
  550| 		/*  TODO: Written to by Linux.  */
  551| 		if (writeflag == MEM_WRITE && idata != 0)
  552| 			fatal("[ footbridge: TODO: write to PCI_ADDRESS_"
  553| 			    "EXTENSION: 0x%llx ]\n", (long long)idata);
  554| 		break;
  555| 
  556| 	case SA_CONTROL:
  557| 		/*  Read by Linux:  */
  558| 		odata = PCI_CENTRAL_FUNCTION;
  559| 		break;
  560| 
  561| 	case UART_DATA:
  562| 		if (writeflag == MEM_WRITE)
  563| 			console_putchar(d->console_handle, idata);
  564| 		break;
  565| 
  566| 	case UART_RX_STAT:
  567| 		/*  TODO  */
  568| 		odata = 0;
  569| 		break;
  570| 
  571| 	case UART_FLAGS:
  572| 		odata = UART_TX_EMPTY;
  573| 		break;
  574| 
  575| 	case IRQ_STATUS:
  576| 		if (writeflag == MEM_READ)
  577| 			odata = d->irq_status & d->irq_enable;
  578| 		else if (!d->warned_irq_status_w) {
  579| 			/*  #545: read-only register (7.3.29); the write is
  580| 			    declined -- no register changes, only this site's
  581| 			    warn-once latch is set -- and announced once.  */
  582| 			d->warned_irq_status_w = 1;
  583| 			fatal("[ WARNING: footbridge write to irq status? "
  584| 			    "(once) ]\n");
  585| 		}
  586| 		break;
  587| 
  588| 	case IRQ_RAW_STATUS:
  589| 		if (writeflag == MEM_READ)
  590| 			odata = d->irq_status;
  591| 		else if (!d->warned_irq_raw_w) {
  592| 			/*  #545: read-only (7.3.30); declined, announced once.  */
  593| 			d->warned_irq_raw_w = 1;
  594| 			fatal("[ footbridge write to irq_raw_status (once) ]\n");
  595| 		}
  596| 		break;
  597| 
  598| 	case IRQ_ENABLE_SET:
  599| 		if (writeflag == MEM_WRITE) {
  600| 			d->irq_enable |= idata;
  601| 			if (d->irq_status & d->irq_enable)
  602| 				INTERRUPT_ASSERT(d->irq);
  603| 			else
  604| 				INTERRUPT_DEASSERT(d->irq);
  605| 		} else {
  606| 			/*  #539: a read of 188h is documented -- IRQEnable is
  607| 			    "read-only ... can only be changed by writing to
  608| 			    the EnableSet and EnableClear registers", reset 0
  609| 			    (DC21285 Table 7-10, 7.3.31).  The value below was
```

## The data structures those files define (every field that exists)

### `src/devices/dev_footbridge.c` -- `struct footbridge_data {` (HEAD lines 60-100)

```c
   60| struct footbridge_data {
   61| 	struct interrupt irq;
   62| 
   63| 	struct pci_data *pcibus;
   64| 
   65| 	int		console_handle;
   66| 
   67| 	uint32_t	timer_load[N_FOOTBRIDGE_TIMERS];
   68| 	uint32_t	timer_value[N_FOOTBRIDGE_TIMERS];
   69| 	uint32_t	timer_control[N_FOOTBRIDGE_TIMERS];
   70| 
   71| 	struct interrupt timer_irq[N_FOOTBRIDGE_TIMERS];
   72| 	struct timer	*timer[N_FOOTBRIDGE_TIMERS];
   73| 	int		pending_timer_interrupts[N_FOOTBRIDGE_TIMERS];
   74| 	/*  #442: the per-timer bound on the counter above, one emulated second of
   75| 	    that timer's delivered rate, recomputed by reload_timer_value().  */
   76| 	int		pending_bound[N_FOOTBRIDGE_TIMERS];
   77| 
   78| 	int		irq_asserted;
   79| 
   80| 	uint32_t	irq_status;
   81| 	uint32_t	irq_enable;
   82| 
   83| 	uint32_t	fiq_status;
   84| 	uint32_t	fiq_enable;
   85| 
   86| 	/*  #545: one warn-once latch per undefined-direction access that used
   87| 	    to end the process (DC21285 7.3.29-7.3.33: "The Status and RawStatus
   88| 	    are read-only, and EnableClear and Soft are write-only").  Zeroed by
   89| 	    DEVINIT's memset and by the offline differentials' calloc.  */
   90| 	int		warned_irq_status_w;
   91| 	int		warned_irq_raw_w;
   92| 	int		warned_irq_clear_r;
   93| 	int		warned_fiq_status_w;
   94| 	int		warned_fiq_raw_w;
   95| 	/*  #585: one warn-once latch per SDRAM register READ that used to end
   96| 	    the process (7.3.9, 7.3.10: both registers are R/W).  Zeroed by
   97| 	    the same memset and calloc as the five above.  */
   98| 	int		warned_sdram_mask_r;
   99| 	int		warned_sdram_offset_r;
  100| };
```

RULES FOR THE EDITS: change ONLY text that appears in this packet; use ONLY fields, functions and macros that appear in it
(a draft that calls an undeclared function or a field that does not exist does not compile); make each `old` long enough to
occur exactly once in its file -- include a distinctive neighbouring line when a statement repeats.

## WHAT TO RETURN

1. One line: `STILL PRESENT: YES|NO|UNSETTLED -- <the line of code shown that shows it>`.  The cited line numbers may have
   moved since the row was written; judge from the code shown.  If NO, say what already fixed it and STOP (no edits).
2. If YES: EXACTLY ONE fenced ```json block -- a list of edits, the smallest fix that removes the defect without changing any
   other behaviour: [{"file": "src/...", "old": "<exact text from the code above, without the line-number prefix; it must occur
   EXACTLY ONCE in that file>", "new": "<replacement>", "why": "<one line>"}].  Use JSON escapes (\t, \n).  Tabs stay tabs;
   lines within 79 columns; tag a new comment `/* #NNN: ... */`.  Prefer the file's existing idioms (a decline, a once-per-
   device announce, a clamp) over new machinery.
3. After the block: what the fix deliberately does NOT change, and anything you could not settle from the code shown.

End with one line: `FIXDRAFT_FBPCIBUS255ZERO: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
