# GXemul hardened fork -- DRAFT A FIX for one filed issue, `ioasicesar` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD d2a6f233).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `ioasicesar`, state `open`, severity `MED`)

**title:** devices/dev_dec_ioasic.c -- station-address ROM reads return a synthetic pattern -- WRONG-RESULT

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T66 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A2-27).  Source URLs: https://github.com/rpajarola/gxemul/commit/e108b546b2e6217ad30bb688b4cbb029755ce230.  Our site at de8c7547: src/devices/dev_dec_ioasic.c:415.  Portable fix: yes -- port rpajarola e108b54.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- port rpajarola e108b54 is available

## The code at the cited lines

### `src/devices/dev_dec_ioasic.c` around the row's cited line 415 (HEAD d2a6f233, lines 370-460)

```c
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
  382| 		if (writeflag == MEM_WRITE)
  383| 			d->scsi_sdr0 = idata;
  384| 		else
  385| 			odata = d->scsi_sdr0;
  386| 
  387| 		debug("[ dec_ioasic: %s SCSI_SDR0, data=0x%08" PRIx64 " ]\n",
  388| 			writeflag == MEM_WRITE ? "write to" : "read from",
  389| 			(uint64_t)(writeflag == MEM_WRITE ? idata : odata));
  390| 		break;
  391| 
  392| 	case IOASIC_SCSI_SDR1:
  393| 		if (writeflag == MEM_WRITE)
  394| 			d->scsi_sdr1 = idata;
  395| 		else
  396| 			odata = d->scsi_sdr1;
  397| 
  398| 		debug("[ dec_ioasic: %s SCSI_SDR1, data=0x%08" PRIx64 " ]\n",
  399| 			writeflag == MEM_WRITE ? "write to" : "read from",
  400| 			(uint64_t)(writeflag == MEM_WRITE ? idata : odata));
  401| 		break;
  402| 
  403| 
  404| 	case IOASIC_SYS_ETHER_ADDRESS(0) + 0x00:
  405| 	case IOASIC_SYS_ETHER_ADDRESS(0) + 0x04:
  406| 	case IOASIC_SYS_ETHER_ADDRESS(0) + 0x08:
  407| 	case IOASIC_SYS_ETHER_ADDRESS(0) + 0x0c:
  408| 	case IOASIC_SYS_ETHER_ADDRESS(0) + 0x10:
  409| 	case IOASIC_SYS_ETHER_ADDRESS(0) + 0x14:
  410| 		/*  Station's ethernet address:  */
  411| 		if (writeflag == MEM_WRITE) {
  412| 			fatal("[ dec_ioasic: attempt to write to the station's"
  413| 			    " ethernet address. ignored for now. ]\n");
  414| 		} else {
  415| 			odata = ((relative_addr - IOASIC_SYS_ETHER_ADDRESS(0)) / 4 + 1) * 0x10;
  416| 		}
  417| 		break;
  418| 
  419| 	/*  The DECstation 5000/125's PROM uses these for cache testing. TODO.  */
  420| 	case 0x0f004:
  421| 	case 0x1f008:
  422| 	case 0x2f00c:
  423| 	case 0x3f010:
  424| 	case 0x4f014:
  425| 	case 0x5f018:
  426| 	case 0x6f01c:
  427| 	case 0x7f020:
  428| 	case 0x8f024:
  429| 	case 0x9f028:
  430| 	case 0xaf02c:
  431| 	case 0xbf030:
  432| 		break;
  433| 
  434| 	default:
  435| 		if (writeflag == MEM_WRITE)
  436| 			fatal("[ dec_ioasic: unimplemented write to address "
  437| 			    "0x%llx, data=0x%08llx ]\n",
  438| 			    (long long)relative_addr, (long long)idata);
  439| 		else
  440| 			fatal("[ dec_ioasic: unimplemented read from address "
  441| 			    "0x%llx ]\n", (long long)relative_addr);
  442| 		// exit(1);
  443| 	}
  444| 
  445| 	if (writeflag == MEM_READ)
  446| 		memory_writemax64(cpu, data, len, odata);
  447| 
  448| 	return 1;
  449| }
  450| 
  451| 
  452| /*
  453|  *  dev_dec_ioasic_init():
  454|  *
  455|  *  For DECstation "type 4", the rackmount_flag selects which model type
  456|  *  the IOASIC should identify itself as (5000 for zero, 5900 if rackmount_flag
  457|  *  is non-zero). It is probably not meaningful on other machines than
  458|  *  type 4.
  459|  */
  460| struct dec_ioasic_data *dev_dec_ioasic_init(struct cpu *cpu,
```

## The data structures those files define (every field that exists)

### `src/include/devices.h` -- `struct dec_ioasic_data` (HEAD lines 82-110)

```c
   82| struct dec_ioasic_data {
   83| 	uint32_t	scsi_dmaptr;		/*  0x000  */
   84| 	uint32_t	scsi_nextptr;		/*  0x010  */
   85| 	uint32_t	lance_dmaptr;		/*  0x020  */
   86| 	uint32_t	floppy_dmaptr;		/*  0x070  */
   87| 	uint32_t	isdn_x_dmaptr;		/*  0x080  */
   88| 	uint32_t	isdn_x_nextptr;		/*  0x090  */
   89| 	uint32_t	isdn_r_dmaptr;		/*  0x0a0  */
   90| 	uint32_t	isdn_r_nextptr;		/*  0x0b0  */
   91| 	uint32_t	csr;			/*  0x100  */
   92| 	uint32_t	intr;			/*  0x110  */
   93| 	uint32_t	imsk;			/*  0x120  */
   94| 	uint32_t	isdn_x_data;		/*  0x140  */
   95| 	uint32_t	isdn_r_data;		/*  0x150  */
   96| 	uint32_t	lance_decode;		/*  0x160  */
   97| 	uint32_t	scsi_decode;		/*  0x170  */
   98| 	uint32_t	scc0_decode;		/*  0x180  */
   99| 	uint32_t	scc1_decode;		/*  0x190  */
  100| 	uint32_t	floppy_decode;		/*  0x1a0  */
  101| 	uint32_t	scsi_scr;		/*  0x1b0  */
  102| 	uint32_t	scsi_sdr0;		/*  0x1c0  */
  103| 	uint32_t	scsi_sdr1;		/*  0x1d0  */
  104| 
  105| 	int		(*dma_func[MAX_IOASIC_DMA_FUNCTIONS])(struct cpu *, void *, uint64_t addr, size_t dma_len, int tx);
  106| 	void		*dma_func_extra[MAX_IOASIC_DMA_FUNCTIONS];
  107| 	int		rackmount_flag;
  108| 	struct interrupt *irq;
  109| 	int		int_asserted;
  110| };
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

End with one line: `FIXDRAFT_IOASICESAR: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.

## YOUR PREVIOUS DRAFT FAILED -- correct it

An earlier draft for this row was applied to the code above and checked.  It failed like this:

```text
APPLY FAILED: FAIL /mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/gweb/jobs_20261106_kits/fix_ioasicesar//reply.txt: 0 json blocks
```

The previous edits:

```json
(no edit block was returned)
```


Return a CORRECTED draft in the same form.  If an `old` string occurred more than once, lengthen it with a distinctive
neighbouring line; if it occurred zero times, copy it exactly from the code shown; use only names that appear in this
packet.  If the fix cannot be written from what is shown, say `STILL PRESENT: UNSETTLED` and name what is missing.
