# GXemul hardened fork -- DRAFT A FIX for one filed issue, `ioasicintrclr` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 2d25df65).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `ioasicintrclr`, state `open`, severity `MED`)

**title:** devices/dev_dec_ioasic.c IOASIC_INTR write -- the write clears every bit set in the value, including the devices' read-only lines -- WRONG-RESULT

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T65 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: one-line; report rows: A2-25).  Source URLs: https://github.com/rpajarola/gxemul/commit/e108b546b2e6217ad30bb688b4cbb029755ce230.  Our site at de8c7547: src/devices/dev_dec_ioasic.c:261-265.  Portable fix: yes -- port rpajarola e108b54.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- port rpajarola e108b54

## The code at the cited lines

### `src/devices/dev_dec_ioasic.c` around the row's cited line 261 (HEAD 2d25df65, lines 216-306)

```c
  216| 
  217| 				d->reg[(IOASIC_SCC_T2_DMAPTR -
  218| 				    IOASIC_SLOT_1_START) / 0x10] = ((curptr <<
  219| 				    3) & ~0x1f) | ((curptr >> 29) & 0x1f);
  220| 			}
  221| 
  222| 			if (csr & IOASIC_CSR_DMAEN_R2) {
  223| 				/*  Receive data:  */
  224| 				curptr = (d->reg[(IOASIC_SCC_R2_DMAPTR -
  225| 				    IOASIC_SLOT_1_START) / 0x10] >> 3)
  226| 				    | ((d->reg[(IOASIC_SCC_R2_DMAPTR -
  227| 				    IOASIC_SLOT_1_START) / 0x10] & 0x1f) << 29);
  228| 				dma_len = 0x1000 - (curptr & 0xffc);
  229| 
  230| 				dma_res = 0;
  231| 				if (d->dma_func[3] != NULL) {
  232| 					dma_res = d->dma_func[3](cpu,
  233| 					    d->dma_func_extra[3], curptr,
  234| 					    dma_len, 0);
  235| 				} else
  236| 					fatal("[ dec_ioasic: DMA tx: data @ "
  237| 					    "%08x, len %i bytes, but no "
  238| 					    "handler? ]\n", (int)curptr,
  239| 					    dma_len);
  240| 
  241| 				/*  and signal the end of page:  */
  242| 				if (dma_res > 0) {
  243| 					if ((curptr & 0x800) != ((curptr +
  244| 					    dma_res) & 0x800))
  245| 						d->reg[(IOASIC_INTR -
  246| 						    IOASIC_SLOT_1_START) / 0x10]
  247| 						    |= IOASIC_INTR_R2_HALF_PAGE;
  248| 					curptr += dma_res;
  249| /*					d->reg[(IOASIC_CSR - IOASIC_SLOT_1_START
  250| 					   ) / 0x10] &= ~IOASIC_CSR_DMAEN_R2; */
  251| 					d->reg[(IOASIC_SCC_R2_DMAPTR -
  252| 					    IOASIC_SLOT_1_START) / 0x10] =
  253| 					    ((curptr << 3) & ~0x1f) | ((curptr
  254| 					    >> 29) & 0x1f);
  255| 				}
  256| 			}
  257| 		}
  258| #endif
  259| 		break;
  260| 
  261| 	case IOASIC_INTR:
  262| 		if (writeflag == MEM_WRITE) {
  263| 			/*  Clear bits on write?  */
  264| 			d->intr &= ~idata;
  265| 			dec_ioasic_reassert(d);
  266| 		} else {
  267| 			odata = d->intr;
  268| 
  269| 			/*  Note/TODO: How about other models than KN03?  */
  270| 			//if (!d->rackmount_flag)
  271| 			//	odata |= KN03_INTR_PROD_JUMPER;
  272| 		}
  273| 
  274| 		debug("[ dec_ioasic: %s INTR, data=0x%08" PRIx64 " ]\n",
  275| 			writeflag == MEM_WRITE ? "write to" : "read from",
  276| 			(uint64_t)(writeflag == MEM_WRITE ? idata : odata));
  277| 
  278| 		break;
  279| 
  280| 	case IOASIC_IMSK:
  281| 		if (writeflag == MEM_WRITE) {
  282| 			d->imsk = idata;
  283| 			dec_ioasic_reassert(d);
  284| 		} else {
  285| 			odata = d->imsk;
  286| 		}
  287| 
  288| 		debug("[ dec_ioasic: %s IMSK, data=0x%08" PRIx64 " ]\n",
  289| 			writeflag == MEM_WRITE ? "write to" : "read from",
  290| 			(uint64_t)(writeflag == MEM_WRITE ? idata : odata));
  291| 		break;
  292| 
  293| 	case IOASIC_ISDN_X_DATA:
  294| 		if (writeflag == MEM_WRITE)
  295| 			d->isdn_x_data = idata;
  296| 		else
  297| 			odata = d->isdn_x_data;
  298| 
  299| 		debug("[ dec_ioasic: %s ISDN_X_DATA, data=0x%08" PRIx64 " ]\n",
  300| 			writeflag == MEM_WRITE ? "write to" : "read from",
  301| 			(uint64_t)(writeflag == MEM_WRITE ? idata : odata));
  302| 		break;
  303| 
  304| 	case IOASIC_ISDN_R_DATA:
  305| 		if (writeflag == MEM_WRITE)
  306| 			d->isdn_r_data = idata;
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

End with one line: `FIXDRAFT_IOASICINTRCLR: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
