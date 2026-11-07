# GXemul hardened fork -- DRAFT A FIX for one filed issue, `osiopdmainval` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 8d9df658).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `osiopdmainval`, state `open`, severity `MED`)

**title:** devices/dev_osiop.c:write_byte -- SCRIPTS DMA writes guest RAM through the host page without invalidating translated code -- WRONG-RESULT (stale code runs after a DMA load)

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T40 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A7-37).  Source URLs: https://github.com/ajfa/mvme187-sysv88-gxemul/commit/4a01173afc4beafabbd61ca385bd158d07d4a415.  Our site at de8c7547: src/devices/dev_osiop.c:261-277.  Portable fix: yes -- port ajfa mvme187 4a01173 patch 04 (invalidate on DMA write).  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- port ajfa mvme187 4a01173 patch 04

## The code at the cited lines

### `src/devices/dev_osiop.c` around the row's cited line 261 (HEAD 8d9df658, lines 141-381)

```c
  141|  *
  142|  *  The SIP bit in ISTAT is basically a "summary" of whether there is
  143|  *  a non-masked SCSI interrupt. Similarly for DIP, for DMA.
  144|  *
  145|  *  However, the SIP and DIP bits are set even if interrupts are
  146|  *  masked away using DIEN and SIEN. (At least that is how I understood
  147|  *  things from reading OpenBSD's osiop.c osiop_poll().) 
  148|  */
  149| static int osiop_update_sip_and_dip(struct osiop_data *d)
  150| {
  151| 	int assert = 0;
  152| 
  153| 	/*  First, let's assume no interrupt assertions.  */
  154| 	d->reg[OSIOP_ISTAT] &= ~(OSIOP_ISTAT_SIP | OSIOP_ISTAT_DIP);
  155| 
  156| 	/*  Any enabled SCSI interrupts?  */
  157| 	if (d->reg[OSIOP_SSTAT0])
  158| 		d->reg[OSIOP_ISTAT] |= OSIOP_ISTAT_SIP;
  159| 	if (d->reg[OSIOP_SSTAT0] & d->reg[OSIOP_SIEN])
  160| 		assert = 1;
  161| 
  162| 	/*  Or enabled DMA interrupts?  */
  163| 	if (d->reg[OSIOP_DSTAT] & ~OSIOP_DIEN_RES)
  164| 		d->reg[OSIOP_ISTAT] |= OSIOP_ISTAT_DIP;
  165| 	if (d->reg[OSIOP_DSTAT] & d->reg[OSIOP_DIEN] & ~OSIOP_DIEN_RES)
  166| 		assert = 1;
  167| 
  168| 	return assert;
  169| }
  170| 
  171| 
  172| /*
  173|  *  osiop_reassert_interrupts():
  174|  *
  175|  *  Recalculate interrupt assertions; if either of the SIP or DIP bits
  176|  *  in the ISTAT register is set, then we should cause an interrupt.
  177|  *
  178|  *  (The d->asserted stuff is to make sure we don't call INTERRUPT_DEASSERT
  179|  *  etc. too often when not necessary. Just an optimization.)
  180|  */
  181| static void osiop_reassert_interrupts(struct osiop_data *d)
  182| {
  183| 	int assert = 0;
  184| 
  185| 	if (osiop_update_sip_and_dip(d))
  186| 		assert = 1;
  187| 
  188| 	if (assert && !d->asserted)
  189| 		INTERRUPT_ASSERT(d->irq);
  190| 	if (!assert && d->asserted)
  191| 		INTERRUPT_DEASSERT(d->irq);
  192| 
  193| 	d->asserted = assert;
  194| }
  195| 
  196| 
  197| /*
  198|  *  #118: A guest can point the SCSI SCRIPTS engine at unmapped physical RAM;
  199|  *  memory_paddr_to_hostaddr() then returns NULL. Warn once (the author's
  200|  *  loud-but-continue style) and stop THIS controller's script engine, instead of
  201|  *  dereferencing NULL (a host crash) or fabricating a transfer. The emulator
  202|  *  keeps running; only this script halts. (Codex+agy course-correction consensus.)
  203|  */
  204| static void osiop_hostpage_fault(struct osiop_data *d)
  205| {
  206| 	if (!d->hostpage_fault_warned) {
  207| 		fatal("[ osiop: SCSI SCRIPTS referenced unmapped physical page "
  208| 		    "0x%08x; stopping script (would have been a host NULL deref) ]\n",
  209| 		    (int) d->last_phys_page);
  210| 		d->hostpage_fault_warned = 1;
  211| 	}
  212| 	d->scripts_running = 0;
  213| }
  214| 
  215| 
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
  307| 		}
  308| 		d->scripts_running = 0;
  309| 		return 0;
  310| 	}
  311| 
  312| 	instr = read_word(d, cpu, dsp);
  313| 
  314| 	dsp += sizeof(instr);
  315| 	*dspp = dsp;
  316| 
  317| 	return instr;
  318| }
  319| 
  320| 
  321| /*
  322|  *  osiop_execute_scripts_instr():
  323|  *
  324|  *  Interprets a single SCRIPTS machine code instruction. Returns 1 if
  325|  *  execution should continue, or 0 if there was an interrupt.
  326|  *
  327|  *  See "Symbios SYM53C710 SCSI I/O Processor Technical Manual, version 3.1"
  328|  *  chapter 5 for details about the instruction set.
  329|  */
  330| int osiop_execute_scripts_instr(struct cpu *cpu, struct osiop_data *d)
  331| {
  332| 	uint32_t *dsap = (uint32_t*) &d->reg[OSIOP_DSA];
  333| 	uint32_t *dnadp = (uint32_t*) &d->reg[OSIOP_DNAD];
  334| 	uint32_t *dbcp = (uint32_t*) &d->reg[OSIOP_DBC];
  335| 	uint32_t *dspsp = (uint32_t*) &d->reg[OSIOP_DSPS];
  336| 	uint32_t *dspp = (uint32_t*) &d->reg[OSIOP_DSP];
  337| 	uint32_t *tempp = (uint32_t*) &d->reg[OSIOP_TEMP];
  338| 
  339| 	uint32_t dspOrig = *dspp;
  340| 	uint32_t instr1 = osiop_get_next_scripts_word(cpu, d);
  341| 	uint32_t instr2 = osiop_get_next_scripts_word(cpu, d);
  342| 	uint32_t dbc, target_addr = 0;
  343| 	uint8_t dcmd;
  344| 	int32_t reladdr;
  345| 	int opcode, phase, relative_addressing, table_indirect_addressing;
  346| 	int select_with_atn, scsi_ids_to_select = -1, scsi_id_to_select;
  347| 	int test_carry, compare_data, compare_phase;
  348| 	int jump_if_true, wait_for_valid_phase;
  349| 	int comparison = 0, interrupt_instead_of_branch = 0;
  350| 	
  351| 	/*
  352| 	 *  According to the 53C710 manual, chapter 5 (introduction): the first
  353| 	 *  32-bit word is always loaded into DCMD and DBC, the second into
  354| 	 *  DSPS, the third (only used by memory move instructions) is loaded
  355| 	 *  into the TEMP register.
  356| 	 */
  357| 
  358| 	if (!d->scripts_running) {	/* #118: host-page fault during SCRIPTS fetch above */
  359| 		*dspp = dspOrig;	/* leave DSP at the faulting instr; don't fake progress */
  360| 		return 0;
  361| 	}
  362| 
  363| 	dcmd = d->reg[OSIOP_DCMD] = instr1 >> 24;
  364| 	dbc = *dbcp = instr1 & 0x00ffffff;
  365| 	*dspsp = instr2;
  366| 
  367| 	reladdr = (instr2 << 8);
  368| 	reladdr >>= 8;
  369| 
  370| 	opcode = (dcmd >> 3) & 7;
  371| 	phase = dcmd & 7;
  372| 
  373| 	if (osiop_debug)
  374| 		debug("{ SCRIPTS @ 0x%08x:  0x%08x 0x%08x",
  375| 		    (int) dspOrig, (int) instr1, (int) instr2);
  376| 
  377| 	switch (dcmd & 0xc0) {
  378| 
  379| 	case 0x00:
  380| 		{
  381| 			int ofs1 = instr1 & 0x00ffffff;
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

## YOUR PREVIOUS DRAFT SAID `STILL PRESENT: UNSETTLED` -- here is what it said was missing

```text
STILL PRESENT: UNSETTLED -- line 275 writes directly to `d->last_host_page`, but the function to invalidate the translated code cache (e.g. cpu_invalidate_translation) is missing from the provided text, and `struct cpu` is not defined here.
```

## What you said was missing, from HEAD

(no definition of a name you used was found in HEAD's src/ -- the name may not exist)


## Added by the coordinator: the definitions your description pointed at

Your previous reply described what was missing without naming it; these are the definitions HEAD has for it.  If the
model carries NO field that distinguishes the architecture version you need, say so as UNSETTLED -- do not invent one.

### `src/include/cpu.h` lines 396-406 (the translation-cache hooks every struct cpu carries)

```c
  396| 			    uint64_t *return_paddr, int flags);
  397| 	void		(*update_translation_table)(struct cpu *,
  398| 			    uint64_t vaddr_page, unsigned char *host_page,
  399| 			    int writeflag, uint64_t paddr_page);
  400| 	void		(*invalidate_translation_caches)(struct cpu *,
  401| 			    uint64_t paddr, int flags);
  402| 	void		(*invalidate_code_translation)(struct cpu *,
  403| 			    uint64_t paddr, int flags);
  404| 	void		(*useremul_syscall)(struct cpu *cpu, uint32_t code);
  405| 	int		(*instruction_has_delayslot)(struct cpu *cpu,
  406| 			    unsigned char *ib);
```

### `src/include/cpu.h` lines 520-528 (their flag values)

```c
  520| 
  521| 
  522| #define	JUST_MARK_AS_NON_WRITABLE	1
  523| #define	INVALIDATE_ALL			2
  524| #define	INVALIDATE_PADDR		4
  525| #define	INVALIDATE_VADDR		8
  526| #define	INVALIDATE_VADDR_UPPER4		16	/*  useful for PPC emulation  */
  527| 
  528| 
```

Now draft the fix, or -- if it still cannot be written from what is shown -- say `STILL PRESENT: UNSETTLED` and name the
exact definition or function still missing.  A name that appears in no section of this packet does not exist in HEAD; do
not use it.  Do not return an empty edit list, and do not return edits that change only comments.
