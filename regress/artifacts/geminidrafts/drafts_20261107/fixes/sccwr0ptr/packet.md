# GXemul hardened fork -- DRAFT A FIX for one filed issue, `sccwr0ptr` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 2d25df65).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `sccwr0ptr`, state `open`, severity `MED`)

**title:** devices/dev_scc.c:DEVICE_ACCESS(scc) -- the WR0 register pointer is the whole byte & 15 and WR0 commands are not decoded -- WRONG-RESULT

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T68 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A2-29).  Source URLs: https://github.com/rpajarola/gxemul/commit/2dfd6ec32be07d7dd38a707f66742de3e2023ed3.  Our site at de8c7547: src/devices/dev_scc.c:402-405.  Portable fix: yes -- port rpajarola 2dfd6ec.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- port rpajarola 2dfd6ec

## The code at the cited lines

### `src/devices/dev_scc.c` around the row's cited line 402 (HEAD 2d25df65, lines 357-447)

```c
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
```

## WHAT TO RETURN

1. One line: `STILL PRESENT: YES|NO|UNSETTLED -- <the line of code shown that shows it>`.  The cited line numbers may have
   moved since the row was written; judge from the code shown.  If NO, say what already fixed it and STOP (no edits).
2. If YES: EXACTLY ONE fenced ```json block -- a list of edits, the smallest fix that removes the defect without changing any
   other behaviour: [{"file": "src/...", "old": "<exact text from the code above, without the line-number prefix; it must occur
   EXACTLY ONCE in that file>", "new": "<replacement>", "why": "<one line>"}].  Use JSON escapes (\t, \n).  Tabs stay tabs;
   lines within 79 columns; tag a new comment `/* #NNN: ... */`.  Prefer the file's existing idioms (a decline, a once-per-
   device announce, a clamp) over new machinery.
3. After the block: what the fix deliberately does NOT change, and anything you could not settle from the code shown.

End with one line: `FIXDRAFT_SCCWR0PTR: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
