# GXemul hardened fork -- DRAFT A FIX for one filed issue, `fbfiqsilent` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at lines the coordinator LOCATED from names the row uses (the row cites none) (HEAD 8d9df658).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `fbfiqsilent`, state `open`, severity `med`)

**title:** dev_footbridge.c answers FIQEnable reads with a silent constant 0 while its IRQ twin kills the host -- the whole FIQ column is softer than the IRQ column [corrected 2026-11-02: since #539 (78360718, 2026-09-19) the IRQ twin returns d->irq_enable with no exit (dev_footbridge.c:600-607 at 987cb596); the FIQ read still answers 0 (:649-652)]

**state_note (head):**

*** codex ASSESS 2026-09-08.  THE ASYMMETRY IS REAL, AND BOTH SIDES ARE ACCEPT. ***

**IRQ_ENABLE_SET read (`+0x188`):**

    odata = d->irq_enable;
    fatal("[ WARNING: footbridge read from ENABLE SET? ]");
    exit(1);

*** IT COMPUTES THE CORRECT VALUE AND THEN ENDS THE HOST. ***  That is member 4 ACCEPT in its purest
form -- delete the kill, keep the value -- and it is the SAME SHAPE this project already found at
`+0x188`'s neighbour, where the datasheet showed a documented read-only register whose answer the
model produced and discarded.

**FIQ_ENABLE_SET (`+0x288`)** returns a silent constant zero.  *"Zero is correct when disabled, but
not for every configured state"* -- so the silent half is a fidelity gap, not a non-defect.

**Both warrant member 4, in SEPARATE rounds.**

*** AND IT REFUTED MY BRIEF'S PREMISE, WHICH IS THE FINDING THAT TRAVELS FURTHEST. ***  I told it
that footbridge being ARM meant FAULT might be available.  **The ARM device-failure arm does not
exist**; `memory_rw.c` has `#ifdef MEM_MIPS` and `#ifdef MEM_M88K` and nothing else.  See the
generalised note now carried on the three `dev_lca.c` rows.

**This row is NOT blocked on a manual**, which is why it was chosen: `_scratchpad/dc21285.txt` is
present, and the same datasheet has already changed one footbridge disposition in this project.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- member 4 shape (delete the kill/silent return, keep the value) for FIQ_ENABLE_SET

## The code at the cited lines

### `src/devices/dev_footbridge.c` around line 598 -- LOCATED BY THE COORDINATOR from the name `IRQ_ENABLE_SET` the row uses (the row cites no line; check this is the defect's site) (HEAD 8d9df658, lines 478-718)

```c
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
  610| 			    always right; the exit(1) that followed it is gone.  */
  611| 			odata = d->irq_enable;
  612| 		}
  613| 		break;
  614| 
  615| 	case IRQ_ENABLE_CLEAR:
  616| 		if (writeflag == MEM_WRITE) {
  617| 			d->irq_enable &= ~idata;
  618| 			if (d->irq_status & d->irq_enable)
  619| 				INTERRUPT_ASSERT(d->irq);
  620| 			else
  621| 				INTERRUPT_DEASSERT(d->irq);
  622| 		} else if (!d->warned_irq_clear_r) {
  623| 			/*  #545: IRQEnableClear is write-only (7.3.33) and Table
  624| 			    7-10 names no register at 18Ch for reads, so the read
  625| 			    is declined with 0 -- the IRQEnable value that used to
  626| 			    be computed here is 188h's answer, not 18Ch's.  */
  627| 			d->warned_irq_clear_r = 1;
  628| 			fatal("[ WARNING: footbridge read from "
  629| 			    "ENABLE CLEAR? (once) ]\n");
  630| 		}
  631| 		break;
  632| 
  633| 	case FIQ_STATUS:
  634| 		if (writeflag == MEM_READ)
  635| 			odata = d->fiq_status & d->fiq_enable;
  636| 		else if (!d->warned_fiq_status_w) {
  637| 			/*  #545: read-only (7.3.29); declined, announced once.  */
  638| 			d->warned_fiq_status_w = 1;
  639| 			fatal("[ WARNING: footbridge write to fiq status? "
  640| 			    "(once) ]\n");
  641| 		}
  642| 		break;
  643| 
  644| 	case FIQ_RAW_STATUS:
  645| 		if (writeflag == MEM_READ)
  646| 			odata = d->fiq_status;
  647| 		else if (!d->warned_fiq_raw_w) {
  648| 			/*  #545: read-only (7.3.30); declined, announced once.  */
  649| 			d->warned_fiq_raw_w = 1;
  650| 			fatal("[ footbridge write to fiq_raw_status (once) ]\n");
  651| 		}
  652| 		break;
  653| 
  654| 	case FIQ_ENABLE_SET:
  655| 		if (writeflag == MEM_WRITE)
  656| 			d->fiq_enable |= idata;
  657| 		break;
  658| 
  659| 	case FIQ_ENABLE_CLEAR:
  660| 		if (writeflag == MEM_WRITE)
  661| 			d->fiq_enable &= ~idata;
  662| 		break;
  663| 
  664| 	case TIMER_1_LOAD:
  665| 		if (writeflag == MEM_READ)
  666| 			odata = d->timer_load[timer_nr];
  667| 		else {
  668| 			d->timer_load[timer_nr] = idata & TIMER_MAX_VAL;
  669| 			reload_timer_value(cpu, d, timer_nr);
  670| 			/*  debug("[ footbridge: timer %i (1-based), "
  671| 			    "value %i ]\n", timer_nr + 1,
  672| 			    (int)d->timer_value[timer_nr]);  */
  673| 			INTERRUPT_DEASSERT(d->timer_irq[timer_nr]);
  674| 		}
  675| 		break;
  676| 
  677| 	case TIMER_1_VALUE:
  678| 		if (writeflag == MEM_READ)
  679| 			odata = d->timer_value[timer_nr];
  680| 		else
  681| 			d->timer_value[timer_nr] = idata & TIMER_MAX_VAL;
  682| 		break;
  683| 
  684| 	case TIMER_1_CONTROL:
  685| 		if (writeflag == MEM_READ)
  686| 			odata = d->timer_control[timer_nr];
  687| 		else {
  688| 			d->timer_control[timer_nr] = idata;
  689| 			/*  #432: both prescaler bits set is TIMER_EXTERNAL
  690| 			    (0x0C, dc21285reg.h:364) -- a LEGAL named encoding,
  691| 			    and it used to reach fatal()+exit(1) right here, so a
  692| 			    guest selecting the external clock source KILLED THE
  693| 			    HOST.  Arguably likelier than the zero load, since it
  694| 			    is a documented mode rather than a malformed value.
  695| 			    The rate an external clock would actually give is
  696| 			    UNKNOWN and is NOT invented: footbridge_effective_cycles()
  697| 			    now gives the encoding a defined, survivable meaning
  698| 			    (the unprescaled period), and the real semantics are
  699| 			    filed for a round that has a datasheet.  */
  700| 			if (idata & TIMER_ENABLE) {
  701| 				reload_timer_value(cpu, d, timer_nr);
  702| 			} else {
  703| 				d->pending_timer_interrupts[timer_nr] = 0;
  704| 			}
  705| 			INTERRUPT_DEASSERT(d->timer_irq[timer_nr]);
  706| 		}
  707| 		break;
  708| 
  709| 	case TIMER_1_CLEAR:
  710| 		/*  #474: a READ must not perform the clear.  This case carried no
  711| 		    writeflag test at all, while TIMER_1_CONTROL immediately above it
  712| 		    does -- so a guest READ reloaded the counter, decremented the
  713| 		    pending count and DEASSERTED the interrupt.  A guest that merely
  714| 		    read the register silently acknowledged a pending timer interrupt;
  715| 		    the guest-visible consequence is a LOST interrupt, not a bad value.
  716| 
  717| 		    FOUR addresses, not one: the fold above normalises 0x30C/0x32C/
  718| 		    0x34C/0x36C onto this single case.
```

### `src/devices/dev_footbridge.c` around line 654 -- LOCATED BY THE COORDINATOR from the name `FIQ_ENABLE_SET` the row uses (the row cites no line; check this is the defect's site) (HEAD 8d9df658, lines 534-774)

```c
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
  610| 			    always right; the exit(1) that followed it is gone.  */
  611| 			odata = d->irq_enable;
  612| 		}
  613| 		break;
  614| 
  615| 	case IRQ_ENABLE_CLEAR:
  616| 		if (writeflag == MEM_WRITE) {
  617| 			d->irq_enable &= ~idata;
  618| 			if (d->irq_status & d->irq_enable)
  619| 				INTERRUPT_ASSERT(d->irq);
  620| 			else
  621| 				INTERRUPT_DEASSERT(d->irq);
  622| 		} else if (!d->warned_irq_clear_r) {
  623| 			/*  #545: IRQEnableClear is write-only (7.3.33) and Table
  624| 			    7-10 names no register at 18Ch for reads, so the read
  625| 			    is declined with 0 -- the IRQEnable value that used to
  626| 			    be computed here is 188h's answer, not 18Ch's.  */
  627| 			d->warned_irq_clear_r = 1;
  628| 			fatal("[ WARNING: footbridge read from "
  629| 			    "ENABLE CLEAR? (once) ]\n");
  630| 		}
  631| 		break;
  632| 
  633| 	case FIQ_STATUS:
  634| 		if (writeflag == MEM_READ)
  635| 			odata = d->fiq_status & d->fiq_enable;
  636| 		else if (!d->warned_fiq_status_w) {
  637| 			/*  #545: read-only (7.3.29); declined, announced once.  */
  638| 			d->warned_fiq_status_w = 1;
  639| 			fatal("[ WARNING: footbridge write to fiq status? "
  640| 			    "(once) ]\n");
  641| 		}
  642| 		break;
  643| 
  644| 	case FIQ_RAW_STATUS:
  645| 		if (writeflag == MEM_READ)
  646| 			odata = d->fiq_status;
  647| 		else if (!d->warned_fiq_raw_w) {
  648| 			/*  #545: read-only (7.3.30); declined, announced once.  */
  649| 			d->warned_fiq_raw_w = 1;
  650| 			fatal("[ footbridge write to fiq_raw_status (once) ]\n");
  651| 		}
  652| 		break;
  653| 
  654| 	case FIQ_ENABLE_SET:
  655| 		if (writeflag == MEM_WRITE)
  656| 			d->fiq_enable |= idata;
  657| 		break;
  658| 
  659| 	case FIQ_ENABLE_CLEAR:
  660| 		if (writeflag == MEM_WRITE)
  661| 			d->fiq_enable &= ~idata;
  662| 		break;
  663| 
  664| 	case TIMER_1_LOAD:
  665| 		if (writeflag == MEM_READ)
  666| 			odata = d->timer_load[timer_nr];
  667| 		else {
  668| 			d->timer_load[timer_nr] = idata & TIMER_MAX_VAL;
  669| 			reload_timer_value(cpu, d, timer_nr);
  670| 			/*  debug("[ footbridge: timer %i (1-based), "
  671| 			    "value %i ]\n", timer_nr + 1,
  672| 			    (int)d->timer_value[timer_nr]);  */
  673| 			INTERRUPT_DEASSERT(d->timer_irq[timer_nr]);
  674| 		}
  675| 		break;
  676| 
  677| 	case TIMER_1_VALUE:
  678| 		if (writeflag == MEM_READ)
  679| 			odata = d->timer_value[timer_nr];
  680| 		else
  681| 			d->timer_value[timer_nr] = idata & TIMER_MAX_VAL;
  682| 		break;
  683| 
  684| 	case TIMER_1_CONTROL:
  685| 		if (writeflag == MEM_READ)
  686| 			odata = d->timer_control[timer_nr];
  687| 		else {
  688| 			d->timer_control[timer_nr] = idata;
  689| 			/*  #432: both prescaler bits set is TIMER_EXTERNAL
  690| 			    (0x0C, dc21285reg.h:364) -- a LEGAL named encoding,
  691| 			    and it used to reach fatal()+exit(1) right here, so a
  692| 			    guest selecting the external clock source KILLED THE
  693| 			    HOST.  Arguably likelier than the zero load, since it
  694| 			    is a documented mode rather than a malformed value.
  695| 			    The rate an external clock would actually give is
  696| 			    UNKNOWN and is NOT invented: footbridge_effective_cycles()
  697| 			    now gives the encoding a defined, survivable meaning
  698| 			    (the unprescaled period), and the real semantics are
  699| 			    filed for a round that has a datasheet.  */
  700| 			if (idata & TIMER_ENABLE) {
  701| 				reload_timer_value(cpu, d, timer_nr);
  702| 			} else {
  703| 				d->pending_timer_interrupts[timer_nr] = 0;
  704| 			}
  705| 			INTERRUPT_DEASSERT(d->timer_irq[timer_nr]);
  706| 		}
  707| 		break;
  708| 
  709| 	case TIMER_1_CLEAR:
  710| 		/*  #474: a READ must not perform the clear.  This case carried no
  711| 		    writeflag test at all, while TIMER_1_CONTROL immediately above it
  712| 		    does -- so a guest READ reloaded the counter, decremented the
  713| 		    pending count and DEASSERTED the interrupt.  A guest that merely
  714| 		    read the register silently acknowledged a pending timer interrupt;
  715| 		    the guest-visible consequence is a LOST interrupt, not a bad value.
  716| 
  717| 		    FOUR addresses, not one: the fold above normalises 0x30C/0x32C/
  718| 		    0x34C/0x36C onto this single case.
  719| 
  720| 		    GUARD THE BODY, KEEP THE break.  An early return here would skip
  721| 		    the function's common tail, which writes odata back on a read, and
  722| 		    would hand a guest an untouched buffer -- a defect this code does
  723| 		    not currently have.  */
  724| 		if (writeflag == MEM_WRITE) {
  725| 			if (d->timer_control[timer_nr] & TIMER_MODE_PERIODIC) {
  726| 				reload_timer_value(cpu, d, timer_nr);
  727| 			}
  728| 
  729| 			if (d->pending_timer_interrupts[timer_nr] > 0) {
  730| 				d->pending_timer_interrupts[timer_nr] --;
  731| 			}
  732| 
  733| 			INTERRUPT_DEASSERT(d->timer_irq[timer_nr]);
  734| 		}
  735| 		break;
  736| 
  737| 	case SDRAM_BA_MASK:
  738| 		if (writeflag == MEM_READ) {
  739| 			/*  #585: an R/W register (DC21285 7.3.9; 7.3.10 for
  740| 			    104h), so this read is legal -- it used to end the
  741| 			    emulator with exit(1).  The write arms keep nothing
  742| 			    (hardware would read back W & 0x8ffc0000 here,
  743| 			    W & 0x0ffc0000 at 104h; keeping writes is filed),
  744| 			    so the read is declined: odata stays 0 and the
  745| 			    common tail below returns it -- keep the break.
  746| 			    0 is also both registers' normal reset value;
  747| 			    00FC0000h is only the mask's blank-ROM-programming
  748| 			    default.  Announced once per register.  */
  749| 			if (!d->warned_sdram_mask_r) {
  750| 				d->warned_sdram_mask_r = 1;
  751| 				fatal("[ footbridge: read of sdram_ba_mask "
  752| 				    "declined, reads 0 (written values are "
  753| 				    "not kept) (once) ]\n");
  754| 			}
  755| 		} else {
  756| 			switch (idata) {
  757| 			case SDRAM_MASK_256KB:
  758| 			case SDRAM_MASK_512KB:
  759| 			case SDRAM_MASK_1MB:
  760| 			case SDRAM_MASK_2MB:
  761| 			case SDRAM_MASK_4MB:
  762| 			case SDRAM_MASK_8MB:
  763| 			case SDRAM_MASK_16MB:
  764| 			case SDRAM_MASK_32MB:
  765| 			case SDRAM_MASK_64MB:
  766| 			case SDRAM_MASK_128MB:
  767| 			case SDRAM_MASK_256MB:
  768| 				break;
  769| 			default:
  770| 				fatal("[ footbridge write to sdram_ba_mask "
  771| 				    "%#llx ]\n", (long long)idata);
  772| 				break;
  773| 			}
  774| 		}
```

### `src/cpus/memory_rw.c` around line 614 -- LOCATED BY THE COORDINATOR from the name `MEM_M88K` the row uses (the row cites no line; check this is the defect's site) (HEAD 8d9df658, lines 494-734)

```c
  494| 				paddr -= mem->devices[i].baseaddr;
  495| 				if (paddr + len > mem->devices[i].length) {
  496| 					/*  Note the truncation per the
  497| 					    warn-loudly ethos, but only at
  498| 					    debug verbosity (-v) and at most
  499| 					    8 times (single-threaded), since
  500| 					    probing at the end of a device's
  501| 					    mapped range is common and benign
  502| 					    (cf. the unwarned zero-fill in
  503| 					    #95/#119 above).  */
  504| 					static int n_trunc_msgs = 0;
  505| 					if (ENOUGH_VERBOSITY(SUBSYS_MEMORY,
  506| 					    VERBOSITY_DEBUG) &&
  507| 					    n_trunc_msgs < 8) {
  508| 						n_trunc_msgs ++;
  509| 						debugmsg_cpu(cpu,
  510| 						    SUBSYS_MEMORY,
  511| 						    mem->devices[i].name,
  512| 						    VERBOSITY_DEBUG,
  513| 						    "%s truncated at end of"
  514| 						    " device: offset 0x%llx,"
  515| 						    " len %i -> %i",
  516| 						    writeflag == MEM_WRITE ?
  517| 						    "write" : "read",
  518| 						    (long long) paddr,
  519| 						    (int) len,
  520| 						    (int) (mem->devices[i].
  521| 						    length - paddr));
  522| 					}
  523| 					len = mem->devices[i].length - paddr;
  524| 				}
  525| 
  526| 				if (cpu->update_translation_table != NULL &&
  527| 				    !(ok & MEMORY_NOT_FULL_PAGE) &&
  528| 				    mem->devices[i].flags & DM_DYNTRANS_OK) {
  529| 					int wf = writeflag == MEM_WRITE? 1 : 0;
  530| 					unsigned char *host_addr;
  531| 
  532| 					if (!(mem->devices[i].flags &
  533| 					    DM_DYNTRANS_WRITE_OK))
  534| 						wf = 0;
  535| 
  536| 					if (writeflag && wf) {
  537| 						if (paddr < mem->devices[i].
  538| 						    dyntrans_write_low)
  539| 							mem->devices[i].
  540| 							dyntrans_write_low =
  541| 							    paddr &~offset_mask;
  542| 						if (paddr >= mem->devices[i].
  543| 						    dyntrans_write_high)
  544| 							mem->devices[i].
  545| 						 	dyntrans_write_high =
  546| 							    paddr | offset_mask;
  547| 					}
  548| 
  549| 					if (mem->devices[i].flags &
  550| 					    DM_EMULATED_RAM) {
  551| 						/*  MEM_WRITE to force the page
  552| 						    to be allocated, if it
  553| 						    wasn't already  */
  554| 						uint64_t *pp = (uint64_t *)mem->
  555| 						    devices[i].dyntrans_data;
  556| 						uint64_t p = orig_paddr - *pp;
  557| 						host_addr =
  558| 						    memory_paddr_to_hostaddr(
  559| 						    mem, p & ~offset_mask,
  560| 						    MEM_WRITE);
  561| 					} else if ((paddr | offset_mask) <
  562| 					    mem->devices[i].length) {
  563| 						host_addr = mem->devices[i].
  564| 						    dyntrans_data +
  565| 						    (paddr & ~offset_mask);
  566| 					} else {
  567| 						/*  #155: (Codex/Fable)
  568| 						    don't install dyntrans
  569| 						    fast-path access to a
  570| 						    device page that is not
  571| 						    fully backed; keep it on
  572| 						    the bounded slow path.  */
  573| 						host_addr = NULL;
  574| 					}
  575| 
  576| 					if (host_addr != NULL)
  577| 						cpu->update_translation_table(
  578| 						    cpu, vaddr & ~offset_mask,
  579| 						    host_addr, wf,
  580| 						    orig_paddr & ~offset_mask);
  581| 				}
  582| 
  583| 				res = 0;
  584| 				if (!no_exceptions || (mem->devices[i].flags &
  585| 				    DM_READS_HAVE_NO_SIDE_EFFECTS)) {
  586| 					bool running_before_device_access = cpu->running;
  587| 					res = mem->devices[i].f(cpu, mem, paddr,
  588| 					    data, len, writeflag,
  589| 					    mem->devices[i].extra);
  590| 
  591| 					if (running_before_device_access && !cpu->running)
  592| 						return MEMORY_ACCESS_FAILED;
  593| 				}
  594| 
  595| 				if (res == 0)
  596| 					res = -1;
  597| 
  598| 				/*
  599| 				 *  If accessing the memory mapped device
  600| 				 *  failed, then return with an exception.
  601| 				 *  (Architecture specific.)
  602| 				 */
  603| 				if (res <= 0 && !no_exceptions) {
  604| 					debug("[ %s device '%s' addr %08lx "
  605| 					    "failed ]\n", writeflag?
  606| 					    "writing to" : "reading from",
  607| 					    mem->devices[i].name, (long)paddr);
  608| #ifdef MEM_MIPS
  609| 					mips_cpu_exception(cpu,
  610| 					    cache == CACHE_INSTRUCTION?
  611| 					    EXCEPTION_IBE : EXCEPTION_DBE,
  612| 					    0, vaddr, 0, 0, 0, 0);
  613| #endif
  614| #ifdef MEM_M88K
  615| 					/*  #570: record the bus error in the faulting side's
  616| 					    CMMU first: PFSR = BERROR << 16 (the field
  617| 					    OpenBSD/mvme88k's trap.c extracts) and PFAR =
  618| 					    orig_paddr, the PHYSICAL address saved before paddr
  619| 					    was made device-relative.  cmmu[0] is the instruction
  620| 					    CMMU, cmmu[1] the data CMMU (memory_m88k.c's index);
  621| 					    the other CMMU is not written.  For a CPU without a
  622| 					    CMMU, this arm makes no register write; the exception
  623| 					    call is unchanged.  `null route` scores data-access
  624| 					    delivery; instruction-access delivery is unscored
  625| 					    (`null surv` scores survival only).  NO_EXCEPTIONS
  626| 					    callers (e.g. the debugger's dump) never get here:
  627| 					    the test above keeps them out.  */
  628| 					{
  629| 						struct m8820x_cmmu *cmmu =
  630| 						    cpu->cd.m88k.cmmu[cache ==
  631| 						    CACHE_INSTRUCTION ? 0 : 1];
  632| 						if (cmmu != NULL) {
  633| 							cmmu->reg[CMMU_PFSR] =
  634| 							    CMMU_PFSR_BERROR << 16;
  635| 							cmmu->reg[CMMU_PFAR] =
  636| 							    (uint32_t) orig_paddr;
  637| 						}
  638| 					}
  639| 					m88k_exception(cpu, cache == CACHE_INSTRUCTION
  640| 					    ? M88K_EXCEPTION_INSTRUCTION_ACCESS
  641| 					    : M88K_EXCEPTION_DATA_ACCESS, 0);
  642| #endif
  643| 					return MEMORY_ACCESS_FAILED;
  644| 				}
  645| 				goto do_return_ok;
  646| 			}
  647| 
  648| 			if (paddr < mem->devices[i].baseaddr)
  649| 				end = i - 1;
  650| 			if (paddr >= mem->devices[i].endaddr)
  651| 				start = i + 1;
  652| 			i = (start + end) >> 1;
  653| 		} while (start <= end);
  654| 	}
  655| 
  656| 
  657| #ifdef MEM_MIPS
  658| 	/*
  659| 	 *  Data and instruction cache emulation:
  660| 	 */
  661| 
  662| 	switch (cpu->cd.mips.cpu_type.mmu_model) {
  663| 	case MMU3K:
  664| 		/*  if not uncached addess  (TODO: generalize this)  */
  665| 		if (!(misc_flags & PHYSICAL) && cache != CACHE_NONE &&
  666| 		    !((vaddr & 0xffffffffULL) >= 0xa0000000ULL &&
  667| 		      (vaddr & 0xffffffffULL) <= 0xbfffffffULL)) {
  668| 			if (memory_cache_R3000(cpu, cache, paddr,
  669| 			    writeflag, len, data))
  670| 				goto do_return_ok;
  671| 		}
  672| 		break;
  673| 	default:
  674| 		/*  R4000 etc  */
  675| 		/*  TODO  */
  676| 		;
  677| 	}
  678| #endif	/*  MEM_MIPS  */
  679| 
  680| 
  681| 	/*  Outside of physical RAM?  */
  682| 	if (paddr >= mem->physical_max) {
  683| #ifdef MEM_MIPS
  684| 		if ((paddr & 0xffffc00000ULL) == 0x1fc00000) {
  685| 			/*  Ok, this is PROM stuff  */
  686| 		} else if ((paddr & 0xfffff00000ULL) == 0x1ff00000) {
  687| 			/*  Sprite reads from this area of memory...  */
  688| 			/*  TODO: is this still correct?  */
  689| 			if (writeflag == MEM_READ)
  690| 				memset(data, 0, len);
  691| 			goto do_return_ok;
  692| 		} else
  693| #endif /* MIPS */
  694| 		{
  695| 			if (paddr >= mem->physical_max && !no_exceptions)
  696| 				if (memory_warn_about_unimplemented_addr
  697| 				    (cpu, mem, writeflag, paddr, len))
  698| 					return MEMORY_ACCESS_FAILED;
  699| 
  700| 			if (writeflag == MEM_READ) {
  701| 				/*  Return all zeroes? (Or 0xff? TODO)  */
  702| 				memset(data, 0, len);
  703| 
  704| #if 0
  705| /*
  706|  *  NOTE: This code prevents a PROM image from a real 5000/200 from booting.
  707|  *  I think I introduced it because it was how some guest OS (NetBSD?) detected
  708|  *  the amount of RAM on some machine.
  709|  *
  710|  *  TODO: Figure out if it is not needed anymore, and remove it completely.
  711|  */
  712| #ifdef MEM_MIPS
  713| 				/*
  714| 				 *  For real data/instruction accesses, cause
  715| 				 *  an exceptions on an illegal read:
  716| 				 */
  717| 				if (cache != CACHE_NONE && !no_exceptions &&
  718| 				    paddr >= mem->physical_max &&
  719| 				    paddr < mem->physical_max+1048576) {
  720| 					mips_cpu_exception(cpu,
  721| 					    EXCEPTION_DBE, 0, vaddr, 0,
  722| 					    0, 0, 0);
  723| 				}
  724| #endif  /*  MEM_MIPS  */
  725| #endif
  726| 			}
  727| 
  728| 			/*  Hm? Shouldn't there be a DBE exception for
  729| 			    invalid writes as well?  TODO  */
  730| 
  731| 			goto do_return_ok;
  732| 		}
  733| 	}
  734| 
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

End with one line: `FIXDRAFT_FBFIQSILENT: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
