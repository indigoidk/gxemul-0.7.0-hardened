# GXemul hardened fork -- DRAFT A FIX for one filed issue, `ioasicintrclr` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 8d9df658).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `ioasicintrclr`, state `open`, severity `MED`)

**title:** devices/dev_dec_ioasic.c IOASIC_INTR write -- the write clears every bit set in the value, including the devices' read-only lines -- WRONG-RESULT

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T65 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: one-line; report rows: A2-25).  Source URLs: https://github.com/rpajarola/gxemul/commit/e108b546b2e6217ad30bb688b4cbb029755ce230.  Our site at de8c7547: src/devices/dev_dec_ioasic.c:261-265.  Portable fix: yes -- port rpajarola e108b54.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- port rpajarola e108b54

## The code at the cited lines

### `src/devices/dev_dec_ioasic.c` around the row's cited line 261 (HEAD 8d9df658, lines 141-381)

```c
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
  307| 		else
  308| 			odata = d->isdn_r_data;
  309| 
  310| 		debug("[ dec_ioasic: %s ISDN_R_DATA, data=0x%08" PRIx64 " ]\n",
  311| 			writeflag == MEM_WRITE ? "write to" : "read from",
  312| 			(uint64_t)(writeflag == MEM_WRITE ? idata : odata));
  313| 		break;
  314| 
  315| 	case IOASIC_LANCE_DECODE:
  316| 		if (writeflag == MEM_WRITE)
  317| 			d->lance_decode = idata;
  318| 		else
  319| 			odata = d->lance_decode;
  320| 
  321| 		debug("[ dec_ioasic: %s LANCE_DECODE, data=0x%08" PRIx64 " ]\n",
  322| 			writeflag == MEM_WRITE ? "write to" : "read from",
  323| 			(uint64_t)(writeflag == MEM_WRITE ? idata : odata));
  324| 		break;
  325| 
  326| 	case IOASIC_SCSI_DECODE:
  327| 		if (writeflag == MEM_WRITE)
  328| 			d->scsi_decode = idata;
  329| 		else
  330| 			odata = d->scsi_decode;
  331| 
  332| 		debug("[ dec_ioasic: %s SCSI_DECODE, data=0x%08" PRIx64 " ]\n",
  333| 			writeflag == MEM_WRITE ? "write to" : "read from",
  334| 			(uint64_t)(writeflag == MEM_WRITE ? idata : odata));
  335| 		break;
  336| 
  337| 	case IOASIC_SCC0_DECODE:
  338| 		if (writeflag == MEM_WRITE)
  339| 			d->scc0_decode = idata;
  340| 		else
  341| 			odata = d->scc0_decode;
  342| 
  343| 		debug("[ dec_ioasic: %s SCC0_DECODE, data=0x%08" PRIx64 " ]\n",
  344| 			writeflag == MEM_WRITE ? "write to" : "read from",
  345| 			(uint64_t)(writeflag == MEM_WRITE ? idata : odata));
  346| 		break;
  347| 
  348| 	case IOASIC_SCC1_DECODE:
  349| 		if (writeflag == MEM_WRITE)
  350| 			d->scc1_decode = idata;
  351| 		else
  352| 			odata = d->scc1_decode;
  353| 
  354| 		debug("[ dec_ioasic: %s SCC1_DECODE, data=0x%08" PRIx64 " ]\n",
  355| 			writeflag == MEM_WRITE ? "write to" : "read from",
  356| 			(uint64_t)(writeflag == MEM_WRITE ? idata : odata));
  357| 		break;
  358| 
  359| 	case IOASIC_FLOPPY_DECODE:
  360| 		if (writeflag == MEM_WRITE)
  361| 			d->floppy_decode = idata;
  362| 		else
  363| 			odata = d->floppy_decode;
  364| 
  365| 		debug("[ dec_ioasic: %s FLOPPY_DECODE, data=0x%08" PRIx64 " ]\n",
  366| 			writeflag == MEM_WRITE ? "write to" : "read from",
  367| 			(uint64_t)(writeflag == MEM_WRITE ? idata : odata));
  368| 		break;
  369| 
  370| 	case IOASIC_SCSI_SCR:
  371| 		if (writeflag == MEM_WRITE)
  372| 			d->scsi_scr = idata;
  373| 		else
  374| 			odata = d->scsi_scr;
  375| 
  376| 		debug("[ dec_ioasic: %s SCSI_SCR, data=0x%08" PRIx64 " ]\n",
  377| 			writeflag == MEM_WRITE ? "write to" : "read from",
  378| 			(uint64_t)(writeflag == MEM_WRITE ? idata : odata));
  379| 		break;
  380| 
  381| 	case IOASIC_SCSI_SDR0:
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

End with one line: `FIXDRAFT_IOASICINTRCLR: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.

## YOUR PREVIOUS DRAFT SAID `STILL PRESENT: UNSETTLED` -- here is what it said was missing

```text
STILL PRESENT: UNSETTLED -- 264| 			d->intr &= ~idata; (need the definition of the IOASIC_INTR writable/read-only bitmask)
The defect is visible at line 264 where all bits set in `idata` are cleared from `d->intr`. However, the provided code snippet does not include the definitions of which interrupt bits are software-clearable versus read-only hardware lines (e.g., a mask like `IOASIC_INTR_CLEARABLE_MASK`). Without seeing the header file or definitions for these bits, I cannot draft the correct bitwise mask to apply.
```

## What you said was missing, from HEAD

### `src/include/thirdparty/tc_ioasicreg.h` lines 105-121 (where HEAD defines `IOASIC_INTR`)

```c
  105| #define IOASIC_ISDN_X_NEXTPTR		IOASIC_SLOT_1_START+0x090
  106| #define IOASIC_ISDN_R_DMAPTR		IOASIC_SLOT_1_START+0x0a0
  107| #define IOASIC_ISDN_R_NEXTPTR		IOASIC_SLOT_1_START+0x0b0
  108| #define IOASIC_BUFF0			IOASIC_SLOT_1_START+0x0c0
  109| #define IOASIC_BUFF1			IOASIC_SLOT_1_START+0x0d0
  110| #define IOASIC_BUFF2			IOASIC_SLOT_1_START+0x0e0
  111| #define IOASIC_BUFF3			IOASIC_SLOT_1_START+0x0f0
  112| #define IOASIC_CSR			IOASIC_SLOT_1_START+0x100
  113| #define IOASIC_INTR			IOASIC_SLOT_1_START+0x110
  114| #define IOASIC_IMSK			IOASIC_SLOT_1_START+0x120
  115| #define IOASIC_CURADDR			IOASIC_SLOT_1_START+0x130
  116| #define IOASIC_ISDN_X_DATA		IOASIC_SLOT_1_START+0x140
  117| #define IOASIC_ISDN_R_DATA		IOASIC_SLOT_1_START+0x150
  118| #define IOASIC_LANCE_DECODE		IOASIC_SLOT_1_START+0x160
  119| #define IOASIC_SCSI_DECODE		IOASIC_SLOT_1_START+0x170
  120| #define IOASIC_SCC0_DECODE		IOASIC_SLOT_1_START+0x180
  121| #define IOASIC_SCC1_DECODE		IOASIC_SLOT_1_START+0x190
```


Now draft the fix, or -- if it still cannot be written from what is shown -- say `STILL PRESENT: UNSETTLED` and name the
exact definition or function still missing.  A name that appears in no section of this packet does not exist in HEAD; do
not use it.  Do not return an empty edit list, and do not return edits that change only comments.
