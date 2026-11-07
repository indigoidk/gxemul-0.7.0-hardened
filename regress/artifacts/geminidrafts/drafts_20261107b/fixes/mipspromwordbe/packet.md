# GXemul hardened fork -- REVISE ONE FIX DRAFT after a review, `mipspromwordbe` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork
removes crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  You drafted a fix for the
issue below; it compiles at HEAD 8d9df658.  A separate review then reported problems with it.  You cannot read files; work
from this text.  This is a DRAFTING task: FIX ONLY, as exact edits -- no tests, probes or reproduction steps.

## The issue (ledger row `mipspromwordbe`, state `open`)

**title:** src/cpus/cpu_mips.c:300-303 + src/cpus/cpu_mips_instr.c:4339-4342 -- mips_cpu_new stores the default PROM word 0x00c0de0d while the CPU is still little-endian, so a big-endian machine that keeps it fetches a JAL rather than break 0x30378 -- WRONG-RESULT (reboot path on big-endian machines that keep the word, e.g. baremips)

**state_note (head):** 

## Every function your previous draft changed, as it reads AT HEAD (your new edits apply to THIS text)

### `src/cpus/cpu_mips.c` -- AT HEAD, lines 91-318 (`*` marks a line your previous draft changed)

```c
   91|  {
   92|  	int i, found, j, tags_size, n_cache_lines, size_per_cache_line;
   93|  	struct mips_cpu_type_def cpu_type_defs[] = MIPS_CPU_TYPE_DEFS;
   94|  	int x, linesize;
   95|  
   96|  	/*  Scan the cpu_type_defs list for this cpu type:  */
   97|  	i = 0;
   98|  	found = -1;
   99|  	while (i >= 0 && cpu_type_defs[i].name != NULL) {
  100|  		if (strcasecmp(cpu_type_defs[i].name, cpu_type_name) == 0) {
  101|  			found = i;
  102|  			break;
  103|  		}
  104|  		i++;
  105|  	}
  106|  
  107|  	if (found == -1)
  108|  		return 0;
  109|  
  110|  	cpu->memory_rw                = mips_memory_rw;
  111|  	cpu->cd.mips.cpu_type         = cpu_type_defs[found];
  112|  	cpu->name                     = strdup(cpu->cd.mips.cpu_type.name);
  113|  	cpu->byte_order               = EMUL_LITTLE_ENDIAN;
  114|  	cpu->cd.mips.gpr[MIPS_GPR_SP] = INITIAL_STACK_POINTER;
  115|  
  116|  	if (cpu->cd.mips.cpu_type.isa_level <= 2 ||
  117|  	    cpu->cd.mips.cpu_type.isa_level == 32)
  118|  		cpu->is_32bit = 1;
  119|  
  120|  	if (cpu->is_32bit) {
  121|  		cpu->run_instr = mips32_run_instr;
  122|  		cpu->update_translation_table = mips32_update_translation_table;
  123|  		cpu->invalidate_translation_caches =
  124|  		    mips32_invalidate_translation_caches;
  125|  		cpu->invalidate_code_translation =
  126|  		    mips32_invalidate_code_translation;
  127|  	} else {
  128|  		cpu->run_instr = mips_run_instr;
  129|  		cpu->update_translation_table = mips_update_translation_table;
  130|  		cpu->invalidate_translation_caches =
  131|  		    mips_invalidate_translation_caches;
  132|  		cpu->invalidate_code_translation =
  133|  		    mips_invalidate_code_translation;
  134|  	}
  135|  
  136|  	cpu->instruction_has_delayslot = mips_cpu_instruction_has_delayslot;
  137|  
  138|  	/*
  139|  	 *  CACHES:
  140|  	 *
  141|  	 *  1) Use DEFAULT_PCACHE_SIZE and DEFAULT_PCACHE_LINESIZE etc.
  142|  	 *  2) If there are specific values defined for this type of cpu,
  143|  	 *     in its cpu_type substruct, then let's use those.
  144|  	 *  3) Values in the emul struct override both of the above.
  145|  	 *
  146|  	 *  Once we've decided which values to use, they are stored in
  147|  	 *  the emul struct so they can be used from src/machine.c etc.
  148|  	 */
  149|  
  150|  	x = DEFAULT_PCACHE_SIZE;
  151|  	if (cpu->cd.mips.cpu_type.pdcache)
  152|  		x = cpu->cd.mips.cpu_type.pdcache;
  153|  	if (cpu->cd.mips.cache_pdcache == 0)
  154|  		cpu->cd.mips.cache_pdcache = x;
  155|  
  156|  	x = DEFAULT_PCACHE_SIZE;
  157|  	if (cpu->cd.mips.cpu_type.picache)
  158|  		x = cpu->cd.mips.cpu_type.picache;
  159|  	if (cpu->cd.mips.cache_picache == 0)
  160|  		cpu->cd.mips.cache_picache = x;
  161|  
  162|  	if (cpu->cd.mips.cache_secondary == 0)
  163|  		cpu->cd.mips.cache_secondary = cpu->cd.mips.cpu_type.scache;
  164|  
  165|  	linesize = DEFAULT_PCACHE_LINESIZE;
  166|  	if (cpu->cd.mips.cpu_type.pdlinesize)
  167|  		linesize = cpu->cd.mips.cpu_type.pdlinesize;
  168|  	if (cpu->cd.mips.cache_pdcache_linesize == 0)
  169|  		cpu->cd.mips.cache_pdcache_linesize = linesize;
  170|  
  171|  	linesize = DEFAULT_PCACHE_LINESIZE;
  172|  	if (cpu->cd.mips.cpu_type.pilinesize)
  173|  		linesize = cpu->cd.mips.cpu_type.pilinesize;
  174|  	if (cpu->cd.mips.cache_picache_linesize == 0)
  175|  		cpu->cd.mips.cache_picache_linesize = linesize;
  176|  
  177|  	linesize = 0;
  178|  	if (cpu->cd.mips.cpu_type.slinesize)
  179|  		linesize = cpu->cd.mips.cpu_type.slinesize;
  180|  	if (cpu->cd.mips.cache_secondary_linesize == 0)
  181|  		cpu->cd.mips.cache_secondary_linesize = linesize;
  182|  
  183|  
  184|  	/*
  185|  	 *  Primary Data and Instruction caches:
  186|  	 */
  187|  	for (i=CACHE_DATA; i<=CACHE_INSTRUCTION; i++) {
  188|  		switch (i) {
  189|  		case CACHE_DATA:
  190|  			x = 1 << cpu->cd.mips.cache_pdcache;
  191|  			linesize = 1 << cpu->cd.mips.cache_pdcache_linesize;
  192|  			break;
  193|  		case CACHE_INSTRUCTION:
  194|  			x = 1 << cpu->cd.mips.cache_picache;
  195|  			linesize = 1 << cpu->cd.mips.cache_picache_linesize;
  196|  			break;
  197|  		}
  198|  
  199|  		/*  Primary cache size and linesize:  */
  200|  		cpu->cd.mips.cache_size[i] = x;
  201|  		cpu->cd.mips.cache_linesize[i] = linesize;
  202|  
  203|  		switch (cpu->cd.mips.cpu_type.rev) {
  204|  		case MIPS_R2000:
  205|  		case MIPS_R3000:
  206|  			size_per_cache_line = sizeof(struct r3000_cache_line);
  207|  			break;
  208|  		default:
  209|  			size_per_cache_line = 32;	/*  TODO  */
  210|  		}
  211|  
  212|  		cpu->cd.mips.cache_mask[i] = cpu->cd.mips.cache_size[i] - 1;
  213|  
  214|  		CHECK_ALLOCATION(cpu->cd.mips.cache[i] = (unsigned char *)
  215|  		    malloc(cpu->cd.mips.cache_size[i]));
  216|  
  217|  		n_cache_lines = cpu->cd.mips.cache_size[i] /
  218|  		    cpu->cd.mips.cache_linesize[i];
  219|  		tags_size = n_cache_lines * size_per_cache_line;
  220|  
  221|  		CHECK_ALLOCATION(cpu->cd.mips.cache_tags[i] =
  222|  		    malloc(tags_size));
  223|  
  224|  		/*  Initialize the cache tags:  */
  225|  		switch (cpu->cd.mips.cpu_type.rev) {
  226|  		case MIPS_R2000:
  227|  		case MIPS_R3000:
  228|  			for (j=0; j<n_cache_lines; j++) {
  229|  				struct r3000_cache_line *rp;
  230|  				rp = (struct r3000_cache_line *)
  231|  				    cpu->cd.mips.cache_tags[i];
  232|  				rp[j].tag_paddr = 0;
  233|  				rp[j].tag_valid = 0;
  234|  			}
  235|  			break;
  236|  		default:
  237|  			;
  238|  		}
  239|  
  240|  		/*  Set cache_last_paddr to something "impossible":  */
  241|  		cpu->cd.mips.cache_last_paddr[i] = IMPOSSIBLE_PADDR;
  242|  	}
  243|  
  244|  	/*  Register the CPU's interrupts:  */
  245|  	for (i=2; i<8; i++) {
  246|  		struct interrupt templ;
  247|  		char name[50];
  248|  		snprintf(name, sizeof(name), "%s.%i", cpu->path, i);
  249|  		memset(&templ, 0, sizeof(templ));
  250|  		templ.line = 1 << (STATUS_IM_SHIFT + i);
  251|  		templ.name = name;
  252|  		templ.extra = cpu;
  253|  		templ.interrupt_assert = mips_cpu_interrupt_assert;
  254|  		templ.interrupt_deassert = mips_cpu_interrupt_deassert;
  255|  		interrupt_handler_register(&templ);
  256|  
  257|  		if (i == 7)
  258|  			INTERRUPT_CONNECT(name, cpu->cd.mips.irq_compare);
  259|  	}
  260|  
  261|  	/*  System coprocessor (0), and FPU (1):  */
  262|  	cpu->cd.mips.coproc[0] = mips_coproc_new(cpu, 0);
  263|  	cpu->cd.mips.coproc[1] = mips_coproc_new(cpu, 1);
  264|  
  265|  	switch (cpu->cd.mips.cpu_type.mmu_model) {
  266|  	case MMU3K:
  267|  		cpu->vaddr_mask = 0x00000000ffffffffULL;
  268|  		cpu->translate_v2p = translate_v2p_mmu3k;
  269|  		break;
  270|  	case MMU8K:
  271|  		cpu->translate_v2p = translate_v2p_mmu8k;
  272|  		break;
  273|  	case MMU10K:
  274|  		cpu->vaddr_mask = ENTRYHI_R_MASK | ENTRYHI_VPN2_MASK_R10K | 0x1fff;
  275|  		cpu->translate_v2p = translate_v2p_mmu10k;
  276|  		break;
  277|  	default:
  278|  		if (cpu->is_32bit)
  279|  			cpu->vaddr_mask = 0x00000000ffffffffULL;
  280|  		else
  281|  			cpu->vaddr_mask = ENTRYHI_R_MASK | ENTRYHI_VPN2_MASK | 0x1fff;
  282|  
  283|  		if (cpu->cd.mips.cpu_type.rev == MIPS_R4100)
  284|  			cpu->translate_v2p = translate_v2p_mmu4100;
  285|  		else
  286|  			cpu->translate_v2p = translate_v2p_generic;
  287|  	}
  288|  
  289|  	// TODO: Consider moving to src/machine/machine_test.c?
  290|  	// This is only here to make the floating point tests work out-of-the-box.
  291|  	if (!cpu->is_32bit)
  292|  		cpu->cd.mips.coproc[0]->reg[COP0_STATUS] |= STATUS_FR;
  293|  
  294|  	if (cpu->machine->prom_emulation) {
  295|  		/*
  296|  		 *  Default behaviour of jumping to 0xbfc00000 should be
  297|  		 *  a reboot, unless machine-specific initialization code
  298|  		 *  overrides this.
  299|  		 *
  300|* 		 *  Note: Specifically big-endian machines should override
  301|* 		 *  this, since the default MIPS CPU is little-endian!
  302|* 		 */
  303|  		store_32bit_word(cpu, 0xffffffff9fc00000ULL, 0x00c0de0d);
  304|  	}
  305|  
  306|  	/*  Add all register names to the settings:  */
  307|  	CPU_SETTINGS_ADD_REGISTER64("pc", cpu->pc);
  308|  	CPU_SETTINGS_ADD_REGISTER64("hi", cpu->cd.mips.hi);
  309|  	CPU_SETTINGS_ADD_REGISTER64("lo", cpu->cd.mips.lo);
  310|  	for (i=0; i<N_MIPS_GPRS; i++)
  311|  		CPU_SETTINGS_ADD_REGISTER64(regnames[i], cpu->cd.mips.gpr[i]);
  312|  	/*  TODO: Write via special handler function!  */
  313|  	for (i=0; i<N_MIPS_COPROC_REGS; i++)
  314|  		CPU_SETTINGS_ADD_REGISTER64(cop0_names[i],
  315|  		    cpu->cd.mips.coproc[0]->reg[i]);
  316|  
  317|  	return 1;
  318|  }
```

### `src/cpus/cpu_mips_instr.c` -- AT HEAD, lines 4270-5805 (`*` marks a line your previous draft changed)

```c
 4270|  X(to_be_translated)
 4271|  {
 4272|  	uint64_t addr, low_pc;
 4273|  	uint32_t iword, imm;
 4274|  	unsigned char *page;
 4275|  	unsigned char ib[4];
 4276|  	int main_opcode, rt, rs, rd, sa, s6, x64 = 0, s10;
 4277|  	int in_crosspage_delayslot = 0;
 4278|  	void (*samepage_function)(struct cpu *, struct mips_instr_call *);
 4279|  	int store, signedness, size;
 4280|  
 4281|  	/*  Figure out the (virtual) address of the instruction:  */
 4282|  	low_pc = ((size_t)ic - (size_t)cpu->cd.mips.cur_ic_page)
 4283|  	    / sizeof(struct mips_instr_call);
 4284|  
 4285|  	/*  Special case for branch with delayslot on the next page:  */
 4286|  	if (cpu->delay_slot == TO_BE_DELAYED && low_pc == 0) {
 4287|  		/*  fatal("[ delay-slot translation across page "
 4288|  		    "boundary ]\n");  */
 4289|  		in_crosspage_delayslot = 1;
 4290|  	}
 4291|  
 4292|  	addr = cpu->pc & ~((MIPS_IC_ENTRIES_PER_PAGE-1)
 4293|  	    << MIPS_INSTR_ALIGNMENT_SHIFT);
 4294|  	addr += (low_pc << MIPS_INSTR_ALIGNMENT_SHIFT);
 4295|  	cpu->pc = (MODE_int_t)addr;
 4296|  	addr &= ~((1 << MIPS_INSTR_ALIGNMENT_SHIFT) - 1);
 4297|  
 4298|  	/*  Read the instruction word from memory:  */
 4299|  #ifdef MODE32
 4300|  	page = cpu->cd.mips.host_load[(uint32_t)addr >> 12];
 4301|  #else
 4302|  	{
 4303|  		const uint32_t mask1 = (1 << DYNTRANS_L1N) - 1;
 4304|  		const uint32_t mask2 = (1 << DYNTRANS_L2N) - 1;
 4305|  		const uint32_t mask3 = (1 << DYNTRANS_L3N) - 1;
 4306|  		uint32_t x1 = (addr >> (64-DYNTRANS_L1N)) & mask1;
 4307|  		uint32_t x2 = (addr >> (64-DYNTRANS_L1N-DYNTRANS_L2N)) & mask2;
 4308|  		uint32_t x3 = (addr >> (64-DYNTRANS_L1N-DYNTRANS_L2N-
 4309|  		    DYNTRANS_L3N)) & mask3;
 4310|  		struct DYNTRANS_L2_64_TABLE *l2 = cpu->cd.mips.l1_64[x1];
 4311|  		struct DYNTRANS_L3_64_TABLE *l3 = l2->l3[x2];
 4312|  		page = l3->host_load[x3];
 4313|  	}
 4314|  #endif
 4315|  
 4316|  	if (page != NULL) {
 4317|  		/*  fatal("TRANSLATION HIT!\n");  */
 4318|  		memcpy(ib, page + (addr & 0xffc), sizeof(ib));
 4319|  	} else {
 4320|  		/*  fatal("TRANSLATION MISS!\n");  */
 4321|  		if (!cpu->memory_rw(cpu, cpu->mem, addr, ib,
 4322|  		    sizeof(ib), MEM_READ, CACHE_INSTRUCTION)) {
 4323|  			/*  #234: A guest-reachable instruction-fetch bus/TLB
 4324|  			    error has already installed the MIPS exception and
 4325|  			    redirected the PC to the vector (via
 4326|  			    mips_cpu_exception -> pc_to_pointers; the exception
 4327|  			    is also logged by #210). Return so the CPU takes it,
 4328|  			    instead of "goto bad" which sets cpu->running = 0
 4329|  			    and halts the host emulator.  */
 4330|  			return;
 4331|  		}
 4332|  	}
 4333|  
 4334|  	{
 4335|  		uint32_t *p = (uint32_t *) ib;
 4336|  		iword = *p;
 4337|  	}
 4338|  
 4339|  	if (cpu->byte_order == EMUL_LITTLE_ENDIAN)
 4340|  		iword = LE32_TO_HOST(iword);
 4341|* 	else
 4342|* 		iword = BE32_TO_HOST(iword);
 4343|* 
 4344|  
 4345|  #define DYNTRANS_TO_BE_TRANSLATED_HEAD
 4346|  #include "cpu_dyntrans.c"
 4347|  #undef  DYNTRANS_TO_BE_TRANSLATED_HEAD
 4348|  
 4349|  
 4350|  	/*
 4351|  	 *  Translate the instruction:
 4352|   	 *
 4353|  	 *  NOTE: _NEVER_ allow writes to the zero register; all instructions
 4354|  	 *  that use the zero register as their destination should be treated
 4355|  	 *  as NOPs, except those that access memory (they should use the
 4356|  	 *  scratch register instead).
 4357|  	 */
 4358|  
 4359|  	main_opcode = iword >> 26;
 4360|  	rs = (iword >> 21) & 31;
 4361|  	rt = (iword >> 16) & 31;
 4362|  	rd = (iword >> 11) & 31;
 4363|  	sa = (iword >>  6) & 31;
 4364|  	imm = (int16_t)iword;
 4365|  	s6 = iword & 63;
 4366|  	s10 = (rs << 5) | sa;
 4367|  
 4368|  	switch (main_opcode) {
 4369|  
 4370|  	case HI6_SPECIAL:
 4371|  		switch (s6) {
 4372|  
 4373|  		case SPECIAL_SLL:
 4374|  		case SPECIAL_SLLV:
 4375|  		case SPECIAL_SRL:
 4376|  		case SPECIAL_SRLV:
 4377|  		case SPECIAL_SRA:
 4378|  		case SPECIAL_SRAV:
 4379|  		case SPECIAL_DSRL:
 4380|  		case SPECIAL_DSRLV:
 4381|  		case SPECIAL_DSRL32:
 4382|  		case SPECIAL_DSLL:
 4383|  		case SPECIAL_DSLLV:
 4384|  		case SPECIAL_DSLL32:
 4385|  		case SPECIAL_DSRA:
 4386|  		case SPECIAL_DSRAV:
 4387|  		case SPECIAL_DSRA32:
 4388|  			switch (s6) {
 4389|  			case SPECIAL_SLL:  ic->f = instr(sll); break;
 4390|  			case SPECIAL_SLLV: ic->f = instr(sllv); sa = -1; break;
 4391|  			case SPECIAL_SRL:  ic->f = instr(srl); break;
 4392|  			case SPECIAL_SRLV: ic->f = instr(srlv); sa = -1; break;
 4393|  			case SPECIAL_SRA:  ic->f = instr(sra); break;
 4394|  			case SPECIAL_SRAV: ic->f = instr(srav); sa = -1; break;
 4395|  			case SPECIAL_DSRL: ic->f = instr(dsrl); x64=1; break;
 4396|  			case SPECIAL_DSRLV:ic->f = instr(dsrlv);
 4397|  					   x64 = 1; sa = -1; break;
 4398|  			case SPECIAL_DSRL32:ic->f= instr(dsrl); x64=1;
 4399|  					   sa += 32; break;
 4400|  			case SPECIAL_DSLL: ic->f = instr(dsll); x64=1; break;
 4401|  			case SPECIAL_DSLLV:ic->f = instr(dsllv);
 4402|  					   x64 = 1; sa = -1; break;
 4403|  			case SPECIAL_DSLL32:ic->f= instr(dsll); x64=1;
     | [... lines 4404-5775 not shown ...]
 5776|  		ic->f = instr(cache);
 5777|  		break;
 5778|  
 5779|  	default:goto bad;
 5780|  	}
 5781|  
 5782|  
 5783|  #ifdef MODE32
 5784|  	if (x64) {
 5785|  		static int has_warned = 0;
 5786|  		if (!has_warned && !cpu->translation_readahead) {
 5787|  			fatal("[ WARNING/NOTE: attempt to execute a 64-bit"
 5788|  			    " instruction on an emulated 32-bit processor; "
 5789|  			    "pc=0x%08" PRIx32" ]\n", (uint32_t)cpu->pc);
 5790|  			has_warned = 1;
 5791|  		}
 5792|  		if (cpu->translation_readahead)
 5793|  			goto bad;
 5794|  		else
 5795|  			ic->f = instr(reserved);
 5796|  	}
 5797|  #else
 5798|  	(void)x64; // avoid compiler warning
 5799|  #endif
 5800|  
 5801|  
 5802|  #define	DYNTRANS_TO_BE_TRANSLATED_TAIL
 5803|  #include "cpu_dyntrans.c" 
 5804|  #undef	DYNTRANS_TO_BE_TRANSLATED_TAIL
 5805|  }
```



## Your previous draft's edits

```json
[
  {
    "file": "src/cpus/cpu_mips.c",
    "old": "\t\t *  Note: Specifically big-endian machines should override\n\t\t *  this, since the default MIPS CPU is little-endian!\n\t\t */\n\t\tstore_32bit_word(cpu, 0xffffffff9fc00000ULL, 0x00c0de0d);",
    "new": "\t\t *  Note: The instruction translator detects the byte-swapped\n\t\t *  word for big-endian machines that do not override this.\n\t\t */\n\t\tstore_32bit_word(cpu, 0xffffffff9fc00000ULL, 0x00c0de0d);",
    "why": "Update the comment to reflect that big-endian machines no longer need to manually override the little-endian PROM word"
  },
  {
    "file": "src/cpus/cpu_mips_instr.c",
    "old": "\tif (cpu->byte_order == EMUL_LITTLE_ENDIAN)\n\t\tiword = LE32_TO_HOST(iword);\n\telse\n\t\tiword = BE32_TO_HOST(iword);",
    "new": "\tif (cpu->byte_order == EMUL_LITTLE_ENDIAN)\n\t\tiword = LE32_TO_HOST(iword);\n\telse {\n\t\tiword = BE32_TO_HOST(iword);\n\t\t/*  Fix for big-endian machines keeping the little-endian PROM word:  */\n\t\tif (iword == 0x0ddec000 && addr == 0xffffffff9fc00000ULL)\n\t\t\tiword = 0x00c0de0d;\n\t}",
    "why": "Intercept the byte-swapped PROM word (decoded as JAL) on big-endian machines and correct it back to the BREAK instruction"
  }
]
```

## The review of that draft (it can be WRONG -- judge each point against the code above)

```text
FIXREVIEW_MIPSPROMWORDBE: DEFECT, 2 FINDINGS
1. Does the diff remove the defect the issue describes, at every site the issue names? Name any site it misses.
It modifies the named sites. However, it checks `addr == 0xffffffff9fc00000ULL` (kseg0), which misses fetches from the standard MIPS boot vector at `0xffffffffbfc00000ULL` (kseg1).
2. CONTROL FLOW: does any added `return`, `goto`, `break` or early exit skip code the function would otherwise run?
No control flow statements are added.
3. RETURN VALUE: does any path now return something different?
No return values or return paths are changed.
4. What ELSE does the diff change -- state left set or cleared, a value the guest can now see, a message on a path that did not print one -- beyond removing the defect?
It mutates the local `iword` value prior to instruction translation, which directly changes the instruction the guest executes if it hits this specific address and byte sequence.
5. House idioms (low severity):
The new comment in `src/cpus/cpu_mips_instr.c` exceeds the 79-column limit (with two tabs of indentation, it spans 90 columns) and lacks the required `/* #NNN: ... */` issue tag format.
src/cpus/cpu_mips_instr.c:4344: DEFECT: condition misses kseg1 fetches. Fix: `if (iword == 0x0ddec000 && (addr == 0xffffffff9fc00000ULL || addr == 0xffffffffbfc00000ULL))`
src/cpus/cpu_mips_instr.c:4343: STYLE: comment exceeds 79 cols and lacks tag. Fix: `/* #mipspromwordbe: fix BE keeping LE PROM word */`
```

## WHAT TO RETURN

1. For EACH review finding, one line: `ACCEPT` or `REJECT`, and why, citing the code shown.  A suggestion that uses a
   function, macro or field that appears nowhere in this packet does not exist in HEAD: reject it or replace it with an
   idiom the packet shows.
2. One line: `STILL PRESENT: YES|NO|UNSETTLED -- <the line of code that shows it>`.
3. If YES: EXACTLY ONE fenced ```json block -- the COMPLETE corrected edit list (not a delta), applying to the HEAD text
   above: [{"file": "src/...", "old": "<exact HEAD text, occurring EXACTLY ONCE in that file>", "new": "<replacement>",
   "why": "<one line>"}].  JSON escapes (\t, \n); tabs stay tabs; lines within 79 columns; a new comment carries
   `/* #NNN: ... */`.  Never an empty list and never comment-only edits for a defect in behaviour.  If every finding is
   rejected, return the previous edits unchanged.
4. After the block: what the fix deliberately does not change.

End with two lines: `REVISION_MIPSPROMWORDBE: <a> ACCEPTED, <r> REJECTED` and `FIXDRAFT_MIPSPROMWORDBE: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
