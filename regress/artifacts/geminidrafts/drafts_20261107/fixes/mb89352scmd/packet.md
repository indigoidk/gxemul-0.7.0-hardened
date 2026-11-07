# GXemul hardened fork -- DRAFT A FIX for one filed issue, `mb89352scmd` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 2d25df65).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `mb89352scmd`, state `open`, severity `MED`)

**title:** devices/dev_mb89352.c SCMD decode -- the command is matched on the whole byte instead of bits 7:5 (no RST_ATN/SET_ATN) and transfers are accepted only with PROG_XFR -- WRONG-RESULT (variants reach the halting default arm)

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T89 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A1-24, A1-27, C U9(b)).  Source URLs: https://github.com/retroprom/gxemul/commit/a1cafe7c, https://github.com/retroprom/gxemul/commit/922fc86b, https://sourceforge.net/p/gxemul/code2/HEAD/log/.  Our site at de8c7547: src/devices/dev_mb89352.c:364, :409-410, :527-535.  Portable fix: yes -- port the decode part of upstream a1cafe7c + upstream 922fc86b (SVN r6544/r6546/r6550).  Filing check (TRIAGE.md): `qhmbunimplstops` covers only the resulting halt.  Not a duplicate of `qhmbunimplstops` (regress/artifacts/research_20261022/adj_20261022/ADJ_RULINGS.md A: it exceeds the row it resembles).  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- portable fix is fully identified from upstream commits

## The code at the cited lines

### `src/devices/dev_mb89352.c` around the row's cited line 364 (HEAD 2d25df65, lines 319-409)

```c
  319| 	if (writeflag == MEM_WRITE)
  320| 		idata = memory_readmax64(cpu, data, len);
  321| 	else
  322| 		odata = d->reg[regnr];
  323| 
  324| 	reg_debug(cpu, d, writeflag, regnr, idata);
  325| 
  326| 	switch (regnr) {
  327| 
  328| 	case BDID:
  329| 		if (writeflag == MEM_WRITE) {
  330| 			d->reg[BDID] = idata;
  331| 			if (idata != 7)
  332| 				debugmsg_cpu(cpu, d->subsys, "",
  333| 				    VERBOSITY_INFO, "unimplemented BDID value: 0x%x",
  334| 			    	    (int) idata);
  335| 		} else {
  336| 			odata = (1 << d->reg[BDID]);
  337| 		}
  338| 		break;
  339| 
  340| 	case SCTL:
  341| 		if (writeflag == MEM_WRITE) {
  342| 			d->reg[SCTL] = idata;
  343| 
  344| 			if (idata & SCTL_DIAG)
  345| 				debugmsg_cpu(cpu, d->subsys, "",
  346| 				    VERBOSITY_ERROR,
  347| 			    	    "Diagnostics mode NOT IMPLEMENTED");
  348| 
  349| 			if (idata & SCTL_CTRLRST) {
  350| 				debugmsg(d->subsys, "", VERBOSITY_INFO, "resetting controller");
  351| 				reset_controller(d);
  352| 			}
  353| 		}
  354| 		break;
  355| 
  356| 	case SCMD:
  357| 		if (writeflag == MEM_WRITE) {
  358| 			d->reg[SCMD] = idata;
  359| 			
  360| 			// RST = Reset ?
  361| 			if (idata & SCMD_RST)
  362| 				idata = SCMD_BUS_REL;
  363| 			
  364| 			switch (idata) {
  365| 
  366| 			case SCMD_BUS_REL:	// 0x00
  367| 				d->reg[SSTS] &= ~(SSTS_TARGET | SSTS_INITIATOR | SSTS_XFR);
  368| 				d->phase = PH_BUS_FREE;
  369| 				// TODO: BUS FREE interrupt enable: PCTL_BFINT_ENAB?
  370| 				break;
  371| 
  372| 			case SCMD_SELECT:
  373| 				// Select target in the temp register.
  374| 				{
  375| 					int target = 0;
  376| 					while (target < 8) {
  377| 						int m = 1 << target;
  378| 						if (d->reg[TEMP] & ~(1 << 7) & m)
  379| 							break;
  380| 						target ++;
  381| 					}
  382| 
  383| 					if (target < 8)
  384| 						debugmsg_cpu(cpu, d->subsys, "",
  385| 						    VERBOSITY_DEBUG,
  386| 					    	    "selecting target %i", target);
  387| 					else
  388| 						debugmsg_cpu(cpu, d->subsys, "",
  389| 						    VERBOSITY_WARNING,
  390| 					    	    "SCMD_SELECT with no target?");
  391| 
  392| 					d->target = target;
  393| 					d->reg[INTS] |= INTS_CMD_DONE;
  394| 					d->reg[PSNS] &= ~7;
  395| 					d->phase = PH_CMD;
  396| 					d->reg[PSNS] |= PSNS_REQ;
  397| 
  398| 					if (d->xferp != NULL)
  399| 						scsi_transfer_free(d->xferp);
  400| 
  401| 					d->xferp = scsi_transfer_alloc();
  402| 					d->transfer_bufpos = 0;
  403| 
  404| 					d->reg[SSTS] &= ~SSTS_TARGET;
  405| 					d->reg[SSTS] |= SSTS_BUSY;
  406| 				}
  407| 				break;
  408| 
  409| 			case SCMD_XFR | SCMD_PROG_XFR:
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

End with one line: `FIXDRAFT_MB89352SCMD: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
