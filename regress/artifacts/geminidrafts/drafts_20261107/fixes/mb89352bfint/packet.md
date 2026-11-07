# GXemul hardened fork -- DRAFT A FIX for one filed issue, `mb89352bfint` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 2d25df65).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `mb89352bfint`, state `open`, severity `MED`)

**title:** devices/dev_mb89352.c -- the BUS FREE interrupt (PCTL_BFINT_ENAB) is a TODO -- WRONG-RESULT

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T90 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A1-27, C U9(a)).  Source URLs: https://github.com/retroprom/gxemul/commit/a1cafe7c.  Our site at de8c7547: src/devices/dev_mb89352.c:107.  Portable fix: yes -- port upstream a1cafe7c.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- port upstream a1cafe7c.

## The code at the cited lines

### `src/devices/dev_mb89352.c` around the row's cited line 107 (HEAD 2d25df65, lines 62-152)

```c
   62| 
   63| static char *regname[16] = {
   64| 	"BDID", "SCTL", "SCMD", "TMOD", "INTS", "PSNS", "SSTS", "SERR",
   65| 	"PCTL", "MBC",  "DREG", "TEMP", "TCH",  "TCM",  "TCL",  "EXBF"
   66| };
   67| 
   68| 
   69| #define PH_BUS_FREE		4
   70| 
   71| 
   72| struct mb89352_data {
   73| 	int			subsys;
   74| 
   75| 	struct interrupt	irq;
   76| 	bool			irq_asserted;
   77| 
   78| 	uint8_t			reg[MB89352_NREGS];
   79| 	
   80| 	int			target;		// target SCSI ID, e.g. 6
   81| 	int			phase;
   82| 
   83| 	struct scsi_transfer	*xferp;
   84| 	size_t			transfer_count;
   85| 	size_t			transfer_bufpos;
   86| };
   87| 
   88| 
   89| void reg_debug(struct cpu* cpu, struct mb89352_data *d, int writeflag, int regnr, int data)
   90| {
   91| 	if (!ENOUGH_VERBOSITY(d->subsys, VERBOSITY_DEBUG))
   92| 		return;
   93| 
   94| 	if (writeflag == MEM_WRITE)
   95| 		debugmsg_cpu(cpu, d->subsys, "",
   96| 		    VERBOSITY_DEBUG, "WRITE to %s: 0x%02x", regname[regnr], data);
   97| 	else
   98| 		debugmsg_cpu(cpu, d->subsys, "",
   99| 		    VERBOSITY_DEBUG, "read from %s", regname[regnr]);
  100| }			    
  101| 
  102| 
  103| static void reassert_interrupts(struct mb89352_data *d)
  104| {
  105| 	bool assert = d->reg[INTS] != 0;
  106| 
  107| 	// TODO: BUS FREE interrupt enable: PCTL_BFINT_ENAB
  108| 
  109| 	if (!(d->reg[SCTL] & SCTL_INTR_ENAB))
  110| 		assert = false;
  111| 	if (d->reg[SCTL] & SCTL_DISABLE)
  112| 		assert = false;
  113| 
  114| 	if (assert && !d->irq_asserted)
  115| 		INTERRUPT_ASSERT(d->irq);
  116| 	else if (!assert && d->irq_asserted)
  117| 		INTERRUPT_DEASSERT(d->irq);
  118| 
  119| 	d->irq_asserted = assert;
  120| }
  121| 
  122| 
  123| static void reset_controller(struct mb89352_data *d)
  124| {
  125| 	memset(d->reg, 0, sizeof(d->reg));
  126| 
  127| 	d->reg[BDID] = 7;
  128| 	d->reg[SCTL] = SCTL_DISABLE;
  129| }
  130| 
  131| 
  132| DEVICE_TICK(mb89352)
  133| {
  134| 	struct mb89352_data *d = (struct mb89352_data *) extra;
  135| 	reassert_interrupts(d);
  136| }
  137| 
  138| 
  139| int mb89352_dreg_read(struct cpu* cpu, struct mb89352_data *d, int writeflag)
  140| {
  141| 	int odata;
  142| 
  143| 	if (d->xferp == NULL) {
  144| 		debugmsg_cpu(cpu, d->subsys, "", VERBOSITY_ERROR,
  145| 	    	    "DREG: no ongoing transfer to read from?");
  146| 	    	cpu->running = 0;
  147| 	    	return 0;
  148| 	}
  149| 	
  150| 	uint8_t *p = d->xferp->data_in;
  151| 	size_t len = d->xferp->data_in_len;
  152| 	
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

End with one line: `FIXDRAFT_MB89352BFINT: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
