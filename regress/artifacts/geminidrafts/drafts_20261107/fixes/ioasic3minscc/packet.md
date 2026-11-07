# GXemul hardened fork -- DRAFT A FIX for one filed issue, `ioasic3minscc` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD d2a6f233).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `ioasic3minscc`, state `open`, severity `MED`)

**title:** devices/dev_dec_ioasic.c -- 3MIN SCC transmit/receive DMA is under `#if 0` -- WRONG-RESULT (Ultrix 4.5 serial console waits forever)

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T67 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: medium; report rows: A2-47).  Source URLs: https://github.com/rpajarola/gxemul/commit/7aeae85458685ce7628f0ca5b6bcf9ebe611f393.  Our site at de8c7547: src/devices/dev_dec_ioasic.c:180-258.  Portable fix: yes -- port rpajarola 7aeae85.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- port rpajarola 7aeae85 is available

## The code at the cited lines

### `src/devices/dev_dec_ioasic.c` around the row's cited line 180 (HEAD d2a6f233, lines 135-225)

```c
  135| 			(uint64_t)(writeflag == MEM_WRITE ? idata : odata));
  136| 		break;
  137| 
  138| 	case IOASIC_ISDN_X_NEXTPTR:
  139| 		if (writeflag == MEM_WRITE)
  140| 			d->isdn_x_nextptr = idata;
  141| 		else
  142| 			odata = d->isdn_x_nextptr;
  143| 
  144| 		debug("[ dec_ioasic: %s ISDN_X_NEXTPTR, data=0x%08" PRIx64 " ]\n",
  145| 			writeflag == MEM_WRITE ? "write to" : "read from",
  146| 			(uint64_t)(writeflag == MEM_WRITE ? idata : odata));
  147| 		break;
  148| 
  149| 	case IOASIC_ISDN_R_DMAPTR:
  150| 		if (writeflag == MEM_WRITE)
  151| 			d->isdn_r_dmaptr = idata;
  152| 		else
  153| 			odata = d->isdn_r_dmaptr;
  154| 
  155| 		debug("[ dec_ioasic: %s ISDN_R_DMAPTR, data=0x%08" PRIx64 " ]\n",
  156| 			writeflag == MEM_WRITE ? "write to" : "read from",
  157| 			(uint64_t)(writeflag == MEM_WRITE ? idata : odata));
  158| 		break;
  159| 
  160| 	case IOASIC_ISDN_R_NEXTPTR:
  161| 		if (writeflag == MEM_WRITE)
  162| 			d->isdn_r_nextptr = idata;
  163| 		else
  164| 			odata = d->isdn_r_nextptr;
  165| 
  166| 		debug("[ dec_ioasic: %s ISDN_R_NEXTPTR, data=0x%08" PRIx64 " ]\n",
  167| 			writeflag == MEM_WRITE ? "write to" : "read from",
  168| 			(uint64_t)(writeflag == MEM_WRITE ? idata : odata));
  169| 		break;
  170| 
  171| 	case IOASIC_CSR:
  172| 		if (writeflag == MEM_WRITE)
  173| 			d->csr = idata;
  174| 		else
  175| 			odata = d->csr;
  176| 
  177| 		debug("[ dec_ioasic: %s CSR, data=0x%08" PRIx64 " ]\n",
  178| 			writeflag == MEM_WRITE ? "write to" : "read from",
  179| 			(uint64_t)(writeflag == MEM_WRITE ? idata : odata));
  180| #if 0
  181| 		if (writeflag == MEM_WRITE) {
  182| 			csr = d->reg[(IOASIC_CSR - IOASIC_SLOT_1_START) / 0x10];
  183| 
  184| 			d->reg[(IOASIC_INTR - IOASIC_SLOT_1_START) / 0x10] &=
  185| 			    ~IOASIC_INTR_T2_PAGE_END;
  186| 
  187| 			if (csr & IOASIC_CSR_DMAEN_T2) {
  188| 				/*  Transmit data:  */
  189| 				curptr = (d->reg[(IOASIC_SCC_T2_DMAPTR -
  190| 				    IOASIC_SLOT_1_START) / 0x10] >> 3)
  191| 				    | ((d->reg[(IOASIC_SCC_T2_DMAPTR -
  192| 				    IOASIC_SLOT_1_START) / 0x10] & 0x1f) << 29);
  193| 				dma_len = 0x1000 - (curptr & 0xffc);
  194| 
  195| 				if ((curptr & 0xfff) == 0)
  196| 					break;
  197| 
  198| 				if (d->dma_func[3] != NULL) {
  199| 					d->dma_func[3](cpu,
  200| 					    d->dma_func_extra[3], curptr,
  201| 					    dma_len, 1);
  202| 				} else
  203| 					fatal("[ dec_ioasic: DMA tx: data @ "
  204| 					    "%08x, len %i bytes, but no "
  205| 					    "handler? ]\n", (int)curptr,
  206| 					    dma_len);
  207| 
  208| 				/*  and signal the end of page:  */
  209| 				d->reg[(IOASIC_INTR - IOASIC_SLOT_1_START) /
  210| 				    0x10] |= IOASIC_INTR_T2_PAGE_END;
  211| 
  212| 				d->reg[(IOASIC_CSR - IOASIC_SLOT_1_START) /
  213| 				    0x10] &= ~IOASIC_CSR_DMAEN_T2;
  214| 				curptr |= 0xfff;
  215| 				curptr ++;
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

End with one line: `FIXDRAFT_IOASIC3MINSCC: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.

## YOUR PREVIOUS DRAFT FAILED -- correct it

An earlier draft for this row was applied to the code above and checked.  It failed like this:

```text
APPLY FAILED: FAIL /mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/gweb/jobs_20261106_kits/fix_ioasic3minscc//reply.txt: 0 json blocks
```

The previous edits:

```json
(no edit block was returned)
```


Return a CORRECTED draft in the same form.  If an `old` string occurred more than once, lengthen it with a distinctive
neighbouring line; if it occurred zero times, copy it exactly from the code shown; use only names that appear in this
packet.  If the fix cannot be written from what is shown, say `STILL PRESENT: UNSETTLED` and name what is missing.
