# GXemul hardened fork -- DRAFT A FIX for one filed issue, `clmpccmsvr` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 2d25df65).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `clmpccmsvr`, state `open`, severity `MED`)

**title:** devices/dev_clmpcc.c -- MSVR does not report CD/DSR/CTS, and the IACK context (STK/CAR) and EOI restore are not modelled -- WRONG-RESULT (SVR4 /dev/console does not open)

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T86 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A7-43).  Source URLs: https://github.com/ajfa/mvme187-sysv88-gxemul/commit/4a01173afc4beafabbd61ca385bd158d07d4a415.  Our site at de8c7547: src/devices/dev_clmpcc.c:175-177, :224-234.  Portable fix: yes -- port ajfa mvme187 4a01173 patches 05/06.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- Portable fix available upstream.

## The code at the cited lines

### `src/devices/dev_clmpcc.c` around the row's cited line 175 (HEAD 2d25df65, lines 130-220)

```c
  130| 		break;
  131| 
  132| 	case CLMPCC_REG_CMR:	/*  Channel Mode Register  */
  133| 	case CLMPCC_REG_COR1:	/*  Channel Option Register #1  */
  134| 	case CLMPCC_REG_COR2:	/*  Channel Option Register #2  */
  135| 	case CLMPCC_REG_COR3:	/*  Channel Option Register #3  */
  136| 	case CLMPCC_REG_COR4:	/*  Channel Option Register #4  */
  137| 	case CLMPCC_REG_COR5:	/*  Channel Option Register #5  */
  138| 	case CLMPCC_REG_COR6:	/*  Channel Option Register #6  */
  139| 	case CLMPCC_REG_COR7:	/*  Channel Option Register #7  */
  140| 	case CLMPCC_REG_SCHR1:	/*  Special Character Register #1  */
  141| 	case CLMPCC_REG_SCHR2:	/*  Special Character Register #2  */
  142| 	case CLMPCC_REG_SCHR3:	/*  Special Character Register #3  */
  143| 	case CLMPCC_REG_SCHR4:	/*  Special Character Register #4  */
  144| 	case CLMPCC_REG_SCRl:	/*  Special Character Range (low)  */
  145| 	case CLMPCC_REG_SCRh:	/*  Special Character Range (high)  */
  146| 	case CLMPCC_REG_LNXT:	/*  LNext Character  */
  147| 		break;
  148| 
  149| 	case CLMPCC_REG_STCR:	/*  Special Transmit Command Register  */
  150| 		if (writeflag == MEM_WRITE) {
  151| 			if (idata == 0x0b) {
  152| 				if (d->reg[CLMPCC_REG_CAR] == 0)
  153| 					console_putchar(d->console_handle,
  154| 					    d->reg[CLMPCC_REG_SCHR3]);
  155| 				else
  156| 					fatal("[ clmpcc: TODO: transmit "
  157| 					    "to channel, CAR!=0 ]\n");
  158| 
  159| 				/*  Command done:  */
  160| 				d->reg[CLMPCC_REG_STCR] = 0x00;
  161| 			} else {
  162| 				fatal("clmpcc: unimplemented STCR byte "
  163| 				    "0x%02x\n", (int) idata);
  164| 				exit(1);
  165| 			}
  166| 		}
  167| 		break;
  168| 
  169| 	case CLMPCC_REG_RBPR:	/*  Receive Baud Rate Period Register  */
  170| 	case CLMPCC_REG_TBPR:	/*  Transmit Baud Rate Period Register  */
  171| 	case CLMPCC_REG_RCOR:	/*  Receive Clock Options Register  */
  172| 	case CLMPCC_REG_TCOR:	/*  Transmit Clock Options Register  */
  173| 		break;
  174| 
  175| 	case CLMPCC_REG_MSVR_RTS:/* Modem Signal Value Register, RTS  */
  176| 	case CLMPCC_REG_MSVR_DTR:/* Modem Signal Value Register, DTR  */
  177| 		break;
  178| 
  179| 	case CLMPCC_REG_RTPRl:	/*  Receive Timeout Period Register (low)  */
  180| 	case CLMPCC_REG_RTPRh:	/*  Receive Timeout Period Register (high)  */
  181| 		break;
  182| 
  183| 	case CLMPCC_REG_IER:	/*  Interrupt Enable Register  */
  184| 	case CLMPCC_REG_LIVR:	/*  Local Interrupt Vector Register  */
  185| 	case CLMPCC_REG_RPILR:	/*  Rx Priority Interrupt Level Register  */
  186| 	case CLMPCC_REG_TPILR:	/*  Tx Priority Interrupt Level Register  */
  187| 	case CLMPCC_REG_MPILR:	/*  Modem Priority Interrupt Level Register  */
  188| 		reassert_interrupts(d);
  189| 		break;
  190| 
  191| 	case CLMPCC_REG_RISRl:	/*  Receive Interrupt Status Reg (low)  */
  192| 		odata = 0x00;
  193| 		break;
  194| 
  195| 	case CLMPCC_REG_TIR:	/*  Transmit Interrupt Register  */
  196| 		odata = 0x40;	/*  see openbsd's cl_txintr  */
  197| 		break;
  198| 
  199| 	case CLMPCC_REG_RIR:	/*  Rx Interrupt Register  */
  200| 		odata = 0x00;
  201| 		if (console_charavail(d->console_handle))
  202| 			odata = 0xc0;
  203| 		break;
  204| 
  205| 	case CLMPCC_REG_LICR:	/*  Local Interrupt Status Register  */
  206| 		odata = 0;	/*  channel nr << 2  */
  207| 		break;
  208| 
  209| 	case CLMPCC_REG_RFOC:	/*  Rx FIFO Output Count  */
  210| 		odata = 0;
  211| 		if (console_charavail(d->console_handle))
  212| 			odata = 1;
  213| 		break;
  214| 
  215| 	case CLMPCC_REG_TFTC:	/*  Tx FIFO Transfer Count  */
  216| 		/*
  217| 		 *  0x1f is low enough to allow OpenBSD/mvme88k's ramdisk
  218| 		 *  kernel to run (bsd.rd), but not the default kernel (bsd).
  219| 		 *  Lowering it to 0x0f seems to work.
  220| 		 */
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

End with one line: `FIXDRAFT_CLMPCCMSVR: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
