# GXemul hardened fork -- DRAFT A FIX for one filed issue, `osiopdmainval` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD d2a6f233).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `osiopdmainval`, state `open`, severity `MED`)

**title:** devices/dev_osiop.c:write_byte -- SCRIPTS DMA writes guest RAM through the host page without invalidating translated code -- WRONG-RESULT (stale code runs after a DMA load)

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T40 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A7-37).  Source URLs: https://github.com/ajfa/mvme187-sysv88-gxemul/commit/4a01173afc4beafabbd61ca385bd158d07d4a415.  Our site at de8c7547: src/devices/dev_osiop.c:261-277.  Portable fix: yes -- port ajfa mvme187 4a01173 patch 04 (invalidate on DMA write).  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- port ajfa mvme187 4a01173 patch 04

## The code at the cited lines

### `src/devices/dev_osiop.c` around the row's cited line 261 (HEAD d2a6f233, lines 216-306)

```c
  216| /*  Helper: returns a word in host order, from emulated physical RAM.  */
  217| static uint32_t read_word(struct osiop_data *d, struct cpu *cpu, uint32_t addr)
  218| {
  219| 	uint32_t word;
  220| 
  221| 	if (d->last_host_page == NULL ||
  222| 	    d->last_phys_page != (addr & 0xfffff000)) {
  223| 		d->last_phys_page = addr & 0xfffff000;
  224| 		d->last_host_page =
  225| 		    memory_paddr_to_hostaddr(cpu->mem, d->last_phys_page, 0);
  226| 	}
  227| 
  228| 	if (d->last_host_page == NULL) {	/* #118 */
  229| 		osiop_hostpage_fault(d);
  230| 		return 0;
  231| 	}
  232| 
  233| 	word = *((uint32_t *) (d->last_host_page + (addr & 0xffc)));
  234| 
  235| 	if (cpu->byte_order == EMUL_LITTLE_ENDIAN)
  236| 		word = LE32_TO_HOST(word);
  237| 	else
  238| 		word = BE32_TO_HOST(word);
  239| 
  240| 	return word;
  241| }
  242| 
  243| 
  244| /*  Helper: reads/writes single bytes from emulated physical RAM.  */
  245| static uint8_t read_byte(struct osiop_data *d, struct cpu *cpu, uint32_t addr)
  246| {
  247| 	if (d->last_host_page == NULL ||
  248| 	    d->last_phys_page != (addr & 0xfffff000)) {
  249| 		d->last_phys_page = addr & 0xfffff000;
  250| 		d->last_host_page =
  251| 		    memory_paddr_to_hostaddr(cpu->mem, d->last_phys_page, 0);
  252| 	}
  253| 
  254| 	if (d->last_host_page == NULL) {	/* #118 */
  255| 		osiop_hostpage_fault(d);
  256| 		return 0;
  257| 	}
  258| 
  259| 	return d->last_host_page[addr & 0xfff];
  260| }
  261| static void write_byte(struct osiop_data *d, struct cpu *cpu, uint32_t addr, uint8_t byte)
  262| {
  263| 	if (d->last_host_page == NULL ||
  264| 	    d->last_phys_page != (addr & 0xfffff000)) {
  265| 		d->last_phys_page = addr & 0xfffff000;
  266| 		d->last_host_page =
  267| 		    memory_paddr_to_hostaddr(cpu->mem, d->last_phys_page, 1);
  268| 	}
  269| 
  270| 	if (d->last_host_page == NULL) {	/* #118 */
  271| 		osiop_hostpage_fault(d);
  272| 		return;
  273| 	}
  274| 
  275| 	d->last_host_page[addr & 0xfff] = byte;
  276| }
  277| 
  278| 
  279| /*
  280|  *  osiop_get_next_scripts_word():
  281|  *
  282|  *  Reads a 32-bit word at physical memory location DSP, and returns it
  283|  *  in host order. DSP is then advanced to point to the next instruction word.
  284|  *
  285|  *  (NOTE/TODO: This could be optimized to read from a host page directly,
  286|  *  but then care must be taken when the instruction pointer (DSP) goes
  287|  *  over a page boundary to the next page. At least the page lookup
  288|  *  could be "cached"...)
  289|  */
  290| uint32_t osiop_get_next_scripts_word(struct cpu *cpu, struct osiop_data *d)
  291| {
  292| 	uint32_t *dspp = (uint32_t*) &d->reg[OSIOP_DSP];
  293| 	uint32_t dsp = *dspp;
  294| 	uint32_t instr;
  295| 
  296| 	if (dsp & 3) {
  297| 		/*  Guest-reachable via an ordinary (unaligned) DSP register
  298| 		    write, and recoverable: warn once and stop this script
  299| 		    engine (the #118 pattern) instead of exit(1). The caller
  300| 		    checks scripts_running right after the fetch and leaves
  301| 		    DSP at the faulting instruction.  */
  302| 		static int warned = 0;
  303| 		if (!warned) {
  304| 			fatal("[ osiop: unaligned DSP 0x%08x; "
  305| 			    "stopping script ]\n", dsp);
  306| 			warned = 1;
```

## The data structures those files define (every field that exists)

### `src/devices/dev_osiop.c` -- `struct osiop_data {` (HEAD lines 75-99)

```c
   75| struct osiop_data {
   76| 	struct interrupt	irq;
   77| 	int			asserted;
   78| 	
   79| 	int			scripts_running;
   80| 
   81| 	/*  Current transfer:  */
   82| 	int			selected_id;
   83| 	struct scsi_transfer	*xferp;
   84| 	size_t			data_offset;
   85| 
   86| 	/*  Cached emulated physical RAM page lookup:  */
   87| 	uint32_t		last_phys_page;
   88| 	uint8_t			*last_host_page;
   89| 	int			hostpage_fault_warned;	/* #118: warn once */
   90| 
   91| 	/*  ALU:  */
   92| 	int			carry;
   93| 	
   94| 	/*
   95| 	 *  Most of these are byte-addressed, but some are not. (Note: For
   96| 	 *  convenience, 32-bit words are stored in host byte order!)
   97| 	 */
   98| 	uint8_t			reg[OSIOP_NREGS];
   99| };
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

End with one line: `FIXDRAFT_OSIOPDMAINVAL: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
