# GXemul hardened fork -- DRAFT A FIX for one filed issue, `scc3minlines` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 8d9df658).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `scc3minlines`, state `open`, severity `MED`)

**title:** devices/dev_scc.c -- 3MIN line mapping: every channel goes to lk201_tx_data, so keyboard commands reach the console and mouse input is dropped -- WRONG-RESULT

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T72 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A2-33).  Source URLs: https://github.com/rpajarola/gxemul/commit/5d3e9ee0884c1a0e2eed6e1ec77ce9ba85d9f0de.  Our site at de8c7547: src/devices/dev_scc.c:445, :128-134.  Portable fix: yes -- port rpajarola 5d3e9ee.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- port rpajarola 5d3e9ee

## The code at the cited lines

### `src/devices/dev_scc.c` around the row's cited line 445 (HEAD 8d9df658, lines 325-525)

```c
  325| 
  326| 	if (writeflag == MEM_WRITE)
  327| 		idata = memory_readmax64(cpu, data, len);
  328| 
  329| 	/*  relative_addr /= d->addrmul;  */
  330| 		/*  See SGI comment below instead.  */
  331| 	/*
  332| 	 *  SGI writes command to 0x0f, and data to 0x1f.
  333| 	 *  (TODO: This works for port nr 0, how about port nr 1?)
  334| 	 */
  335| 	if ((relative_addr & 0x0f) == 0xf) {
  336| 		if (relative_addr == 0x0f)
  337| 			relative_addr = 1;
  338| 		else
  339| 			relative_addr = 5;
  340| 	}
  341| 
  342| 	port = relative_addr / 8;
  343| 	relative_addr &= 7;
  344| 	if (port >= N_SCC_PORTS) {
  345| 		/*  #101 (refined, Codex+agy course-correction): a guest can address
  346| 		    beyond the real SCC ports within the 0x1000 window. The earlier
  347| 		    "% N_SCC_PORTS" was host-safe but ALIASED out-of-range offsets onto a
  348| 		    valid port (wrong hardware). Ignore the access instead -- loud once,
  349| 		    no aliasing, still no OOB into scc_register_r[].  */
  350| 		static int scc_oob_warned = 0;
  351| 		if (!scc_oob_warned) {
  352| 			fatal("[ scc: out-of-range port %i (beyond %i) ignored; "
  353| 			    "not aliased ]\n", port, N_SCC_PORTS);
  354| 			scc_oob_warned = 1;
  355| 		}
  356| 		if (writeflag == MEM_READ)
  357| 			memory_writemax64(cpu, data, len, 0);
  358| 		return 1;
  359| 	}
  360| 
  361| 	dev_scc_tick(cpu, extra);
  362| 
  363| 	/*
  364| 	 *  Ultrix writes words such as 0x1200 to relative address 0,
  365| 	 *  instead of writing the byte 0x12 directly to address 1.
  366| 	 */
  367| 	if ((relative_addr == 0 || relative_addr == 4) && (idata & 0xff) == 0) {
  368| 		ultrix_mode = 1;
  369| 		relative_addr ++;
  370| 		idata >>= 8;
  371| 	}
  372| 
  373| 	switch (relative_addr) {
  374| 	case 1:		/*  command  */
  375| 		if (writeflag==MEM_READ) {
  376| 			odata = d->scc_register_r[port * N_SCC_REGS +
  377| 			    d->register_selected[port]];
  378| 
  379| 			if (d->register_selected[port] == SCC_RR3) {
  380| 				if (port == SCC_CHANNEL_B)
  381| 					fatal("WARNING! scc channel B has "
  382| 					    "no RR3\n");
  383| 
  384| 				d->scc_register_r[port * N_SCC_REGS +
  385| 				    SCC_RR3] = 0;
  386| 
  387| 				INTERRUPT_DEASSERT(d->irq);
  388| 			}
  389| 
  390| #ifdef SCC_DEBUG
  391| 			fatal("[ scc: port %i, register %i, read value "
  392| 			    "0x%02x ]\n", port, d->register_selected[port],
  393| 			    (int)odata);
  394| #endif
  395| 			d->register_select_in_progress[port] = 0;
  396| 			d->register_selected[port] = 0;
  397| 			/*  debug("[ scc: (port %i) read from 0x%08lx ]\n",
  398| 			    port, (long)relative_addr);  */
  399| 		} else {
  400| 			/*  If no register is selected, then select one.
  401| 			    Otherwise, write to the selected register.  */
  402| 			if (d->register_select_in_progress[port] == 0) {
  403| 				d->register_select_in_progress[port] = 1;
  404| 				d->register_selected[port] = idata;
  405| 				d->register_selected[port] &= (N_SCC_REGS-1);
  406| 			} else {
  407| 				d->scc_register_w[port * N_SCC_REGS +
  408| 				    d->register_selected[port]] = idata;
  409| #ifdef SCC_DEBUG
  410| 				fatal("[ scc: port %i, register %i, write "
  411| 				    "value 0x%02x ]\n", port,
  412| 				    d->register_selected[port], idata);
  413| #endif
  414| 
  415| 				d->scc_register_r[port * N_SCC_REGS +
  416| 				    SCC_RR12] = d->scc_register_w[port *
  417| 				    N_SCC_REGS + SCC_WR12];
  418| 				d->scc_register_r[port * N_SCC_REGS +
  419| 				    SCC_RR13] = d->scc_register_w[port *
  420| 				    N_SCC_REGS + SCC_WR13];
  421| 
  422| 				d->register_select_in_progress[port] = 0;
  423| 				d->register_selected[port] = 0;
  424| 			}
  425| 		}
  426| 		break;
  427| 	case 5:		/*  data  */
  428| 		if (writeflag==MEM_READ) {
  429| 			if (rx_avail(d, port))
  430| 				odata = rx_nextchar(d, port);
  431| 
  432| 			/*  TODO:  perhaps only clear the RX part of RR3?  */
  433| 			d->scc_register_r[N_SCC_REGS + SCC_RR3] = 0;
  434| 
  435| 			INTERRUPT_DEASSERT(d->irq);
  436| 
  437| //			debug("[ scc: (port %i) read from 0x%08lx: 0x%02x ]\n",
  438| //			    port, (long)relative_addr, (int)odata);
  439| 		} else {
  440| 			/*  debug("[ scc: (port %i) write to  0x%08lx: "
  441| 			    "0x%08x ]\n", port, (long)relative_addr,
  442| 			    (int)idata);  */
  443| 
  444| 			/*  Send the character:  */
  445| 			lk201_tx_data(&d->lk201, d->scc_nr * 2 + port, idata);
  446| 
  447| 			/*  Loopback:  */
  448| 			if (d->scc_register_w[port * N_SCC_REGS + SCC_WR14]
  449| 			    & SCC_WR14_LOCAL_LOOPB)
  450| 				dev_scc_add_to_rx_queue(d, idata, d->scc_nr
  451| 				    * 2 + port);
  452| 
  453| 			/*  TX interrupt:  */
  454| 			if (d->scc_register_w[port * N_SCC_REGS + SCC_WR9] &
  455| 			    SCC_WR9_MASTER_IE &&
  456| 			    d->scc_register_w[port * N_SCC_REGS + SCC_WR1] &
  457| 			    SCC_WR1_TX_IE) {
  458| 				if (port == SCC_CHANNEL_A)
  459| 					d->scc_register_r[N_SCC_REGS + SCC_RR3]
  460| 					    |= SCC_RR3_TX_IP_A;
  461| 				else
  462| 					d->scc_register_r[N_SCC_REGS + SCC_RR3]
  463| 					    |= SCC_RR3_TX_IP_B;
  464| 			}
  465| 
  466| 			dev_scc_tick(cpu, extra);
  467| 		}
  468| 		break;
  469| 	default:
  470| 		if (writeflag==MEM_READ) {
  471| 			debug("[ scc: (port %i) read from 0x%08lx ]\n",
  472| 			    port, (long)relative_addr);
  473| 		} else {
  474| 			debug("[ scc: (port %i) write to  0x%08lx: 0x%08x ]\n",
  475| 			    port, (long)relative_addr, (int)idata);
  476| 		}
  477| 	}
  478| 
  479| 	if (ultrix_mode && writeflag == MEM_READ) {
  480| 		odata <<= 8;
  481| 	}
  482| 
  483| 	if (writeflag == MEM_READ)
  484| 		memory_writemax64(cpu, data, len, odata);
  485| 
  486| 	return 1;
  487| }
  488| 
  489| 
  490| /*
  491|  *  dev_scc_init():
  492|  *
  493|  *	use_fb = non-zero when using graphical console + keyboard
  494|  *	scc_nr = 0 or 1
  495|  *	addmul = 1 in most cases, 8 on SGI?
  496|  */
  497| void *dev_scc_init(struct machine *machine, struct memory *mem,
  498| 	uint64_t baseaddr, char* irq_path, int use_fb, int scc_nr, int addrmul)
  499| {
  500| 	struct scc_data *d;
  501| 
  502| 	CHECK_ALLOCATION(d = (struct scc_data *) malloc(sizeof(struct scc_data)));
  503| 	memset(d, 0, sizeof(struct scc_data));
  504| 
  505| 	INTERRUPT_CONNECT(irq_path, d->irq);
  506| 	d->scc_nr  = scc_nr;
  507| 	d->use_fb  = use_fb;
  508| 	d->addrmul = addrmul;
  509| 	d->console_handle = console_start_slave(machine, "SCC", 1);
  510| 
  511| 	d->scc_register_r[SCC_RR0] |= SCC_RR0_TX_UNDERRUN;
  512| 
  513| 	lk201_init(&d->lk201, use_fb,
  514| 	    dev_scc_space_available_in_queue,
  515| 	    dev_scc_add_to_rx_queue,
  516| 	    d->console_handle, d);
  517| 
  518| 	memory_device_register(mem, "scc", baseaddr, DEV_SCC_LENGTH,
  519| 	    dev_scc_access, d, DM_DEFAULT, NULL);
  520| 	machine_add_tickfunction(machine, dev_scc_tick, d, SCC_TICK_SHIFT);
  521| 
  522| 	return (void *) d;
  523| }
  524| 
  525| 
```

## The data structures those files define (every field that exists)

### `src/devices/dev_scc.c` -- `struct scc_data {` (HEAD lines 77-97)

```c
   77| struct scc_data {
   78| 	struct interrupt	irq;
   79| 
   80| 	int		use_fb;
   81| 	int		console_handle;
   82| 
   83| 	int		scc_nr;
   84| 	int		addrmul;
   85| 
   86| 	int		register_select_in_progress[N_SCC_PORTS];
   87| 	int		register_selected[N_SCC_PORTS];
   88| 
   89| 	unsigned char	scc_register_r[N_SCC_PORTS * N_SCC_REGS];
   90| 	unsigned char	scc_register_w[N_SCC_PORTS * N_SCC_REGS];
   91| 
   92| 	unsigned char	rx_queue_char[N_SCC_PORTS * MAX_QUEUE_LEN];
   93| 	int		cur_rx_queue_pos_write[N_SCC_PORTS];
   94| 	int		cur_rx_queue_pos_read[N_SCC_PORTS];
   95| 
   96| 	struct lk201_data lk201;
   97| };
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

End with one line: `FIXDRAFT_SCC3MINLINES: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.

## YOUR PREVIOUS DRAFT SAID `STILL PRESENT: UNSETTLED` -- here is what it said was missing

```text
STILL PRESENT: UNSETTLED -- src/devices/dev_scc.c:445 requires routing mouse input but the required output functions and port mappings are undeclared in this packet.
The defect cannot be fixed using only the functions and fields declared in the provided code snippet. The issue states that mouse input is dropped because all channels go to `lk201_tx_data`, but there is no function visible in this packet to handle mouse data transmission, nor is it clear which specific `port` and `scc_nr` corresponds to the mouse.
FIXDRAFT_SCC3MINLINES: UNSETTLED PRESENT, 0 EDITS
```

## What you said was missing, from HEAD

### `src/devices/lk201.c` lines 265-281 (where HEAD defines `lk201_tx_data`)

```c
  265| 
  266| 	int dx, dy, mouse_buttons, mouse_fb_nr;
  267| 	console_getmouse(&dx, &dy, &mouse_buttons, &mouse_fb_nr);
  268| 
  269| 	lk201_send_mouse_update_sequence(d, dx, dy, mouse_buttons, mouse_fb_nr);
  270| }
  271| 
  272| 
  273| void lk201_tx_data(struct lk201_data *d, int port, int idata)
  274| {
  275| 	switch (port) {
  276| 	case DCKBD_PORT:		/*  port 0  */
  277| 		if (!d->use_fb) {
  278| 			/*  Simply print the character to stdout:  */
  279| 			console_putchar(d->console_handle, idata);
  280| 		} else {
  281| 			debug("[ lk201: writing data to KBD: 0x%02x ]\n", idata);
```

### `src/include/devices.h` lines 525-541 (where HEAD defines `lk201_tx_data`)

```c
  525|         unsigned char           keyb_buf[8];
  526|         int                     keyb_buf_pos;
  527|                         
  528|         int                     mouse_mode;
  529|         int                     mouse_revision;         /*  0..15  */  
  530|         int                     mouse_buttons;
  531| };
  532| void lk201_tick(struct machine *, struct lk201_data *); 
  533| void lk201_tx_data(struct lk201_data *, int port, int idata);
  534| void lk201_init(struct lk201_data *d, int use_fb,
  535| 	int (*space_available_in_queue)(void *,int),
  536| 	void (*add_to_rx_queue)(void *,int,int),
  537| 	int console_handle, void *);
  538| 
  539| 
  540| #endif	/*  DEVICES_H  */
  541| 
```


Now draft the fix, or -- if it still cannot be written from what is shown -- say `STILL PRESENT: UNSETTLED` and name the
exact definition or function still missing.  A name that appears in no section of this packet does not exist in HEAD; do
not use it.  Do not return an empty edit list, and do not return edits that change only comments.
