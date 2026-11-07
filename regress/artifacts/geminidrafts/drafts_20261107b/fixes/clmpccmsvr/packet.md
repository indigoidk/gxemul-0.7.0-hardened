# GXemul hardened fork -- DRAFT A FIX for one filed issue, `clmpccmsvr` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 8d9df658).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `clmpccmsvr`, state `open`, severity `MED`)

**title:** devices/dev_clmpcc.c -- MSVR does not report CD/DSR/CTS, and the IACK context (STK/CAR) and EOI restore are not modelled -- WRONG-RESULT (SVR4 /dev/console does not open)

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T86 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A7-43).  Source URLs: https://github.com/ajfa/mvme187-sysv88-gxemul/commit/4a01173afc4beafabbd61ca385bd158d07d4a415.  Our site at de8c7547: src/devices/dev_clmpcc.c:175-177, :224-234.  Portable fix: yes -- port ajfa mvme187 4a01173 patches 05/06.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- Portable fix available upstream.

## The code at the cited lines

### `src/devices/dev_clmpcc.c` around the row's cited line 175 (HEAD 8d9df658, lines 55-295)

```c
   55| 
   56| 
   57| #define debug fatal
   58| 
   59| #define	CLMPCC_LEN		0x200
   60| #define	DEV_CLMPCC_TICK_SHIFT	16
   61| 
   62| struct clmpcc_data {
   63| 	unsigned char	reg[CLMPCC_LEN];
   64| 
   65| 	int		console_handle;
   66| 
   67| 	/*  Interrupt pins on the PCC2 controller:  */
   68| 	struct interrupt irq_scc_rxe;
   69| 	struct interrupt irq_scc_m;
   70| 	struct interrupt irq_scc_tx;
   71| 	struct interrupt irq_scc_rx;
   72| };
   73| 
   74| 
   75| static void reassert_interrupts(struct clmpcc_data *d)
   76| {
   77| 	int rxintr = 0;
   78| 
   79| 	if (console_charavail(d->console_handle))
   80| 		rxintr = 1;
   81| 
   82| 	if (rxintr)
   83| 		INTERRUPT_ASSERT(d->irq_scc_rx);
   84| 	else
   85| 		INTERRUPT_DEASSERT(d->irq_scc_rx);
   86| 
   87| 	/*  TODO: Hack/experiment for now...  */
   88| 	if ((d->reg[CLMPCC_REG_IER] & 3) != 0)
   89| 		INTERRUPT_ASSERT(d->irq_scc_tx);
   90| 	else
   91| 		INTERRUPT_DEASSERT(d->irq_scc_tx);
   92| }
   93| 
   94| 
   95| DEVICE_TICK(clmpcc)
   96| {
   97| 	struct clmpcc_data *d = (struct clmpcc_data *) extra;
   98| 	reassert_interrupts(d);
   99| }
  100| 
  101| 
  102| DEVICE_ACCESS(clmpcc)
  103| {
  104| 	struct clmpcc_data *d = (struct clmpcc_data *) extra;
  105| 	uint64_t idata = 0, odata = 0;
  106| 
  107| 	if (writeflag == MEM_WRITE) {
  108| 		idata = memory_readmax64(cpu, data, len);
  109| 		d->reg[relative_addr] = idata;
  110| 	}
  111| 
  112| 	if (writeflag == MEM_READ)
  113| 		odata = d->reg[relative_addr];
  114| 
  115| 	switch (relative_addr) {
  116| 
  117| 	case 0:	/*  Used by OpenBSD/mvme88k when probing...  */
  118| 		break;
  119| 
  120| 	case CLMPCC_REG_TPR:	/*  Timer Period Register  */
  121| 		break;
  122| 
  123| 	case CLMPCC_REG_CAR:	/*  Channel Access Register  */
  124| 		/*  debug("[ clmpcc: selecting channel %i ]\n",
  125| 		    (int) idata);  */
  126| 		break;
  127| 
  128| 	case CLMPCC_REG_CCR:	/*  Channel Command Register:  */
  129| 		odata = 0;
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
  221| 		odata = 0x0f;
  222| 		break;
  223| 
  224| 	case CLMPCC_REG_TEOIR:	/*  Tx End of Interrupt Register  */
  225| 		/*  TODO: Do something more realistic?  */
  226| 		INTERRUPT_DEASSERT(d->irq_scc_tx);
  227| 		break;
  228| 
  229| 	case CLMPCC_REG_REOIR:	/*  Rx End of Interrupt Register  */
  230| 		/*  TODO: Do something more realistic?  */
  231| 		INTERRUPT_DEASSERT(d->irq_scc_rx);
  232| 		break;
  233| 
  234| 	case CLMPCC_REG_TDR:
  235| 		if (writeflag == MEM_WRITE) {
  236| 			if (d->reg[CLMPCC_REG_CAR] == 0)
  237| 				console_putchar(d->console_handle, idata);
  238| 			else
  239| 				fatal("[ clmpcc: TODO: transmit "
  240| 				    "to channel, CAR!=0 ]\n");
  241| 		} else {
  242| 			odata = console_readchar(d->console_handle);
  243| 		}
  244| 		break;
  245| 
  246| 	default:if (writeflag == MEM_READ)
  247| 			fatal("[ clmpcc: unimplemented READ from offset 0x%x ]"
  248| 			    "\n", (int)relative_addr);
  249| 		else
  250| 			fatal("[ clmpcc: unimplemented WRITE to offset 0x%x: "
  251| 			    "0x%x ]\n", (int)relative_addr, (int)idata);
  252| 		exit(1);
  253| 	}
  254| 
  255| 	if (writeflag == MEM_READ)
  256| 		memory_writemax64(cpu, data, len, odata);
  257| 
  258| 	return 1;
  259| }
  260| 
  261| 
  262| DEVINIT(clmpcc)
  263| {
  264| 	struct clmpcc_data *d;
  265| 	char tmpstr[100];
  266| 
  267| 	CHECK_ALLOCATION(d = (struct clmpcc_data *) malloc(sizeof(struct clmpcc_data)));
  268| 	memset(d, 0, sizeof(struct clmpcc_data));
  269| 
  270| 	d->console_handle =
  271| 	    console_start_slave(devinit->machine, devinit->name2 != NULL?
  272| 	    devinit->name2 : devinit->name, devinit->in_use);
  273| 
  274| 	/*
  275| 	 *  Connect to the PCC2's interrupt pins:
  276| 	 *
  277| 	 *  The supplied interrupt_path is something like
  278| 	 *  "machine[0].cpu[0].pcc2".
  279| 	 *
  280| 	 *  We want to use "machine[0].cpu[0].pcc2.x", where x is
  281| 	 *  0xc, 0xd, 0xe, and 0xf (PCC2V_SCC_xxx).
  282| 	 */
  283| 	snprintf(tmpstr, sizeof(tmpstr), "%s.%i",
  284| 	    devinit->interrupt_path, PCC2V_SCC_RXE);
  285| 	INTERRUPT_CONNECT(tmpstr, d->irq_scc_rxe);
  286| 	snprintf(tmpstr, sizeof(tmpstr), "%s.%i",
  287| 	    devinit->interrupt_path, PCC2V_SCC_M);
  288| 	INTERRUPT_CONNECT(tmpstr, d->irq_scc_m);
  289| 	snprintf(tmpstr, sizeof(tmpstr), "%s.%i",
  290| 	    devinit->interrupt_path, PCC2V_SCC_TX);
  291| 	INTERRUPT_CONNECT(tmpstr, d->irq_scc_tx);
  292| 	snprintf(tmpstr, sizeof(tmpstr), "%s.%i",
  293| 	    devinit->interrupt_path, PCC2V_SCC_RX);
  294| 	INTERRUPT_CONNECT(tmpstr, d->irq_scc_rx);
  295| 
```

## The data structures those files define (every field that exists)

### `src/devices/dev_clmpcc.c` -- `struct clmpcc_data {` (HEAD lines 62-72)

```c
   62| struct clmpcc_data {
   63| 	unsigned char	reg[CLMPCC_LEN];
   64| 
   65| 	int		console_handle;
   66| 
   67| 	/*  Interrupt pins on the PCC2 controller:  */
   68| 	struct interrupt irq_scc_rxe;
   69| 	struct interrupt irq_scc_m;
   70| 	struct interrupt irq_scc_tx;
   71| 	struct interrupt irq_scc_rx;
   72| };
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

End with one line: `FIXDRAFT_CLMPCCMSVR: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.

## YOUR PREVIOUS DRAFT SAID `STILL PRESENT: UNSETTLED` -- here is what it said was missing

```text
STILL PRESENT: UNSETTLED -- src/devices/dev_clmpcc.c:175
The code shown confirms the defect: `CLMPCC_REG_MSVR_RTS` and `DTR` simply `break;` without modifying `odata` (leaving it 0), thereby not reporting CD/DSR/CTS (lines 175-177). Likewise, the IACK and EOI logic at `CLMPCC_REG_TEOIR` / `REOIR` is explicitly a stub (`/* TODO: Do something more realistic? */`, lines 224-232). 
However, the fix cannot be drafted from the provided text. The bit positions and active levels for CD/DSR/CTS in the MSVR register are not defined in the code or the prompt, nor are the specific behaviors required for STK/CAR and EOI restore. Settling this requires reading the upstream patch (`ajfa mvme187 4a01173`) or a CD2401 / CLMPCC hardware datasheet.
FIXDRAFT_CLMPCCMSVR: UNSETTLED PRESENT, 0 EDITS
```

## What you said was missing, from HEAD

### `src/include/thirdparty/clmpccreg.h` lines 91-107 (where HEAD defines `CLMPCC_REG_MSVR_RTS`)

```c
   91| #define CLMPCC_REG_TBPR     0xc3    /* Transmit Baud Rate Period Register */
   92| #define CLMPCC_REG_TCOR     0xc0    /* Transmit Clock Options Register */
   93| 
   94| /* Channel Command and Status Registers */
   95| #define CLMPCC_REG_CCR      0x13    /* Channel Command Register */
   96| #define CLMPCC_REG_STCR     0x12    /* Special Transmit Command Register */
   97| #define CLMPCC_REG_CSR      0x1a    /* Channel Status Register */
   98| #define CLMPCC_REG_MSVR     0xde    /* Modem Signal Value Register */
   99| #define CLMPCC_REG_MSVR_RTS 0xde    /* Modem Signal Value Register (RTS) */
  100| #define CLMPCC_REG_MSVR_DTR 0xdf    /* Modem Signal Value Register (DTR) */
  101| 
  102| /* Interrupt Registers */
  103| #define CLMPCC_REG_LIVR     0x09    /* Local Interrupt Vector Register */
  104| #define CLMPCC_REG_IER      0x11    /* Interrupt Enable Register */
  105| #define CLMPCC_REG_LICR     0x26    /* Local Interrupting Channel Register */
  106| #define CLMPCC_REG_STK      0xe2    /* Stack Register */
  107| 
```

### `src/include/thirdparty/clmpccreg.h` lines 116-132 (where HEAD defines `CLMPCC_REG_TEOIR`)

```c
  116| #define CLMPCC_REG_REOIR    0x84    /* Receive End of Interrupt Register */
  117| 
  118| /* Transmit Interrupt Registers */
  119| #define CLMPCC_REG_TPILR    0xe0    /* Transmit Priority Interrupt Level Reg */
  120| #define CLMPCC_REG_TIR      0xec    /* Transmit Interrupt Register */
  121| #define CLMPCC_REG_TISR     0x8a    /* Transmit Interrupt Status Register */
  122| #define CLMPCC_REG_TFTC     0x80    /* Transmit FIFO Transfer Count */
  123| #define CLMPCC_REG_TDR      0xf8    /* Transmit Data Register */
  124| #define CLMPCC_REG_TEOIR    0x85    /* Transmit End of Interrupt Register */
  125| 
  126| /* Modem Interrupt Registers */
  127| #define CLMPCC_REG_MPILR    0xe3    /* Modem Priority Interrupt Level Reg */
  128| #define CLMPCC_REG_MIR      0xef    /* Modem Interrupt Register */
  129| #define CLMPCC_REG_MISR     0x8b    /* Modem (/Timer) Interrupt Status Reg */
  130| #define CLMPCC_REG_MEOIR    0x86    /* Modem End of Interrupt Register */
  131| 
  132| /* DMA Registers */
```


Now draft the fix, or -- if it still cannot be written from what is shown -- say `STILL PRESENT: UNSETTLED` and name the
exact definition or function still missing.  A name that appears in no section of this packet does not exist in HEAD; do
not use it.  Do not return an empty edit list, and do not return edits that change only comments.
