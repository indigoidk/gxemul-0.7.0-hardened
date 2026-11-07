# GXemul hardened fork -- DRAFT A FIX for one filed issue, `sccintpend` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD d2a6f233).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `sccintpend`, state `open`, severity `MED`)

**title:** devices/dev_scc.c -- RR3 and data reads clear all interrupt-pending bits, one WR1 governs both channels, special-condition-only mode interrupts per character, WR9 is stored per channel -- WRONG-RESULT

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T69 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: medium; report rows: A2-30).  Source URLs: https://github.com/rpajarola/gxemul/commit/2dfd6ec32be07d7dd38a707f66742de3e2023ed3, https://github.com/rpajarola/gxemul/commit/7aeae85458685ce7628f0ca5b6bcf9ebe611f393, https://github.com/rpajarola/gxemul/commit/a99af56307177bf32c0e789360fb36212b47225f.  Our site at de8c7547: src/devices/dev_scc.c:379-388, :432-435, :215-216, :201, :454.  Portable fix: yes -- port rpajarola 2dfd6ec, rpajarola 7aeae85, rpajarola a99af56.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- port rpajarola 2dfd6ec, 7aeae85, a99af56

## The code at the cited lines

### `src/devices/dev_scc.c` around the row's cited line 379 (HEAD d2a6f233, lines 334-424)

```c
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

End with one line: `FIXDRAFT_SCCINTPEND: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
