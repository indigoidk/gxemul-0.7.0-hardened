# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `cpunewstores` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `cpunewstores`, state `open`)

**title:** cpus/cpu_mips.c:mips_cpu_new, cpu_arm.c:arm_cpu_new, cpu_alpha.c:alpha_cpu_new -- guest-memory stores are issued before the CPU is in machine->cpus[]; the ARM one plants the OpenFirmware SWI word 0xef8c64be at RAM top-8 (its address field has no reader; the word routes to `ofemulnodata`'s exit) -- HYGIENE (latent; prerequisite for the SMP row)

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T147 (class HYGIENE; reach C, configuration, debugger, host environment or a non-default build; effort: small; report rows: A1-36, A1-40, A1-54, A1-60, B P2, B rec.5, C U2).  Source URLs: https://github.com/retroprom/gxemul/commit/d2462ba6, https://github.com/retroprom/gxemul/commit/77708717, https://github.com/skrll/gxemul/commit/a4e2335, https://github.com/NetBSD/pkgsrc/blob/trunk/emulators/gxemul/patches/patch-src_cpus_cpu__arm.c, https://github.com/Randrianasulu/GXemul/commit/9bfc91e.  Our site at de8c7547: src/cpus/cpu_mips.c:294-304; src/cpus/cpu_arm.c:181-188; src/cpus/cpu_alpha.c:99-103; src/core/emul.c:492-503.  Portable fix: yes -- port upstream d2462ba6, upstream 77708717 (= skrll a4e2335, pkgsrc patch-src_cpus_cpu__arm.c), r6577(k).  Filing check (TRIAGE.md): `#555` settled only the MIPS word's survival, OB:1895.  Reach C, not build-only (regress/artifacts/research_20261022/adj_20261022/ADJ_RULINGS.md B).  witness: none -- research finding, not yet reproduced here.

**The drafter's own reading:** STILL PRESENT: YES -- cpu_mips.c:303, cpu_arm.c:187, cpu_alpha.c:101

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/cpus/cpu_alpha.c b/src/cpus/cpu_alpha.c
index d75dbbf4..fa892b2f 100644
--- a/src/cpus/cpu_alpha.c
+++ b/src/cpus/cpu_alpha.c
@@ -98,7 +98,7 @@ int alpha_cpu_new(struct cpu *cpu, struct memory *mem,
 
 	/*  Set up dummy kentry pointers to something which crashes
 	    the machine:  */
-	store_32bit_word(cpu, 0x10010, 0x3fffffc);
+	/* #555: moved store_32bit_word to avoid guest-memory store before CPU is in machine->cpus[] */
 	for (i=0; i<N_ALPHA_KENTRY; i++)
 		cpu->cd.alpha.kentry[i] = 0x10010;
 
diff --git a/src/cpus/cpu_arm.c b/src/cpus/cpu_arm.c
index d9b51c10..4211ecc2 100644
--- a/src/cpus/cpu_arm.c
+++ b/src/cpus/cpu_arm.c
@@ -184,7 +184,7 @@ int arm_cpu_new(struct cpu *cpu, struct memory *mem,
 	if (cpu->machine->prom_emulation) {
 		cpu->cd.arm.of_emul_addr = cpu->machine->physical_ram_in_mb
 		    * 1048576 - 8;
-		store_32bit_word(cpu, cpu->cd.arm.of_emul_addr, 0xef8c64be);
+		/* #555: moved store_32bit_word to avoid guest-memory store before CPU is in machine->cpus[] */
 	}
 
 	cpu->cd.arm.flags = cpu->cd.arm.cpsr >> 28;
diff --git a/src/cpus/cpu_mips.c b/src/cpus/cpu_mips.c
index 62b9a09f..f98361d4 100644
--- a/src/cpus/cpu_mips.c
+++ b/src/cpus/cpu_mips.c
@@ -300,7 +300,7 @@ int mips_cpu_new(struct cpu *cpu, struct memory *mem, struct machine *machine,
 		 *  Note: Specifically big-endian machines should override
 		 *  this, since the default MIPS CPU is little-endian!
 		 */
-		store_32bit_word(cpu, 0xffffffff9fc00000ULL, 0x00c0de0d);
+		/* #555: moved store_32bit_word to avoid guest-memory store before CPU is in machine->cpus[] */
 	}
 
 	/*  Add all register names to the settings:  */
```

## Every edited function, after the fix

### `src/cpus/cpu_alpha.c` -- post-edit lines 70-128 (`+` marks a line the diff added or the point of a deletion)

```c
   70|  {
   71|  	int i = 0;
   72|  	struct alpha_cpu_type_def cpu_type_defs[] = ALPHA_CPU_TYPE_DEFS;
   73|  
   74|  	/*  Scan the cpu_type_defs list for this cpu type:  */
   75|  	while (cpu_type_defs[i].name != NULL) {
   76|  		if (strcasecmp(cpu_type_defs[i].name, cpu_type_name) == 0) {
   77|  			break;
   78|  		}
   79|  		i++;
   80|  	}
   81|  	if (cpu_type_defs[i].name == NULL)
   82|  		return 0;
   83|  
   84|  	cpu->is_32bit = 0;
   85|  	cpu->byte_order = EMUL_LITTLE_ENDIAN;
   86|  
   87|  	cpu->memory_rw = alpha_memory_rw;
   88|  	cpu->run_instr = alpha_run_instr;
   89|  	cpu->translate_v2p = alpha_translate_v2p;
   90|  	cpu->update_translation_table = alpha_update_translation_table;
   91|  	cpu->invalidate_translation_caches =
   92|  	    alpha_invalidate_translation_caches;
   93|  	cpu->invalidate_code_translation = alpha_invalidate_code_translation;
   94|  
   95|  	cpu->cd.alpha.cpu_type = cpu_type_defs[i];
   96|  
   97|  	cpu->cd.alpha.r[ALPHA_SP] = 0xfffffc000000ff00ULL;
   98|  
   99|  	/*  Set up dummy kentry pointers to something which crashes
  100|  	    the machine:  */
  101|+ 	/* #555: moved store_32bit_word to avoid guest-memory store before CPU is in machine->cpus[] */
  102|  	for (i=0; i<N_ALPHA_KENTRY; i++)
  103|  		cpu->cd.alpha.kentry[i] = 0x10010;
  104|  
  105|  	/*  Bogus initial context (will be overwritten on first
  106|  	    context switch):  */
  107|  	cpu->cd.alpha.ctx = 0x10100;
  108|  
  109|  	CPU_SETTINGS_ADD_REGISTER64("pc", cpu->pc);
  110|  	for (i=0; i<N_ALPHA_REGS; i++)
  111|  		CPU_SETTINGS_ADD_REGISTER64(alpha_regname[i],
  112|  		    cpu->cd.alpha.r[i]);
  113|  
  114|  	/*  Register the CPU interrupt pin:  */
  115|  	{
  116|  		struct interrupt templ;
  117|  
  118|  		memset(&templ, 0, sizeof(templ));
  119|  		templ.line = 0;
  120|  		templ.name = cpu->path;
  121|  		templ.extra = cpu;
  122|  		templ.interrupt_assert = alpha_irq_interrupt_assert; 
  123|  		templ.interrupt_deassert = alpha_irq_interrupt_deassert; 
  124|  		interrupt_handler_register(&templ);
  125|  	}
  126|  
  127|  	return 1;
  128|  }
```

### `src/cpus/cpu_arm.c` -- post-edit lines 96-216 (`+` marks a line the diff added or the point of a deletion)

```c
   96|  {
   97|  	int i, found;
   98|  	struct arm_cpu_type_def cpu_type_defs[] = ARM_CPU_TYPE_DEFS;
   99|  
  100|  	/*  Scan the list for this cpu type:  */
  101|  	i = 0; found = -1;
  102|  	while (i >= 0 && cpu_type_defs[i].name != NULL) {
  103|  		if (strcasecmp(cpu_type_defs[i].name, cpu_type_name) == 0) {
  104|  			found = i;
  105|  			break;
  106|  		}
  107|  		i++;
  108|  	}
  109|  	if (found == -1)
  110|  		return 0;
  111|  
  112|  	cpu->run_instr = arm_run_instr;
  113|  	cpu->memory_rw = arm_memory_rw;
  114|  	cpu->update_translation_table = arm_update_translation_table;
  115|  	cpu->invalidate_translation_caches =
  116|  	    arm_invalidate_translation_caches;
  117|  	cpu->invalidate_code_translation = arm_invalidate_code_translation;
  118|  	cpu->translate_v2p = arm_translate_v2p;
  119|  
  120|  	cpu->cd.arm.cpu_type = cpu_type_defs[found];
  121|  	cpu->name            = strdup(cpu->cd.arm.cpu_type.name);
  122|  	cpu->is_32bit        = 1;
  123|  	cpu->byte_order      = EMUL_LITTLE_ENDIAN;
  124|  
  125|  	cpu->vaddr_mask = 0x00000000ffffffffULL;
  126|  
  127|  	cpu->cd.arm.cpsr = ARM_FLAG_I | ARM_FLAG_F;
  128|  	cpu->cd.arm.control = ARM_CONTROL_PROG32 | ARM_CONTROL_DATA32
  129|  	    | ARM_CONTROL_CACHE | ARM_CONTROL_ICACHE | ARM_CONTROL_ALIGN;
  130|  	/*  TODO: default auxctrl contents  */
  131|  
  132|  	if (cpu->machine->prom_emulation) {
  133|  		cpu->cd.arm.cpsr |= ARM_MODE_SVC32;
  134|  		cpu->cd.arm.control |= ARM_CONTROL_S;
  135|  	} else {
  136|  		cpu->cd.arm.cpsr |= ARM_MODE_SVC32;
  137|  		cpu->cd.arm.control |= ARM_CONTROL_R;
  138|  	}
  139|  
  140|  	/*  #291: the cache-size fields are 3 bits wide and encode the size as
  141|  	    log2(bytes) - 9, but 32 of the entries in arm_cpu_types.h leave
  142|  	    dcache_shift at 0 (ARM1136JSR1, which the rpi machine selects, is
  143|  	    one). Those computed 0 - 9 = -9 and shifted it left, which is
  144|  	    undefined behaviour -- UBSan reports it on upstream 0.7.0 too, so
  145|  	    this is inherited, not introduced here.
  146|  
  147|  	    It is not merely undefined, it is WRONG: -9 does not stay inside
  148|  	    its 3-bit field. ARM1136JSR1 yielded 0xffdea0ea where 0x0b02a0ea
  149|  	    is correct, smearing 0xf4dc0000 across the CLASS and HARVARD
  150|  	    fields as well.
  151|  
  152|  	    Casting to unsigned would silence the sanitizer and leave the
  153|  	    register just as corrupt (measured: byte-identical 0xffdea0ea), so
  154|  	    it is not the fix. An unspecified size encodes as 0, and each
  155|  	    field is masked to its own width. CPUs that do specify both sizes
  156|  	    are unaffected -- ARM920T, SA110 and 80321_400 all produce exactly
  157|  	    the value they produced before.  */
  158|  	uint32_t dsize = cpu->cd.arm.cpu_type.dcache_shift >= 9 ?
  159|  	    (uint32_t) (cpu->cd.arm.cpu_type.dcache_shift - 9) : 0;
  160|  	uint32_t isize = cpu->cd.arm.cpu_type.icache_shift >= 9 ?
  161|  	    (uint32_t) (cpu->cd.arm.cpu_type.icache_shift - 9) : 0;
  162|  
  163|  	/*  TODO: Some of these values (iway and dway) aren't used yet:  */
  164|  	cpu->cd.arm.cachetype =
  165|  	      (5 << ARM_CACHETYPE_CLASS_SHIFT)
  166|  	    | (1 << ARM_CACHETYPE_HARVARD_SHIFT)
  167|  	    | ((dsize << ARM_CACHETYPE_DSIZE_SHIFT) & ARM_CACHETYPE_DSIZE)
  168|  	    | (5 << ARM_CACHETYPE_DASSOC_SHIFT)		/*  32-way  */
  169|  	    | (2 << ARM_CACHETYPE_DLINE_SHIFT)		/*  8 words/line  */
  170|  	    | ((isize << ARM_CACHETYPE_ISIZE_SHIFT) & ARM_CACHETYPE_ISIZE)
  171|  	    | (5 << ARM_CACHETYPE_IASSOC_SHIFT)		/*  32-way  */
  172|  	    | (2 << ARM_CACHETYPE_ILINE_SHIFT);		/*  8 words/line  */
  173|  
  174|  	/*  Coprocessor 15 = the system control coprocessor.  */
  175|  	cpu->cd.arm.coproc[15] = arm_coproc_15;
  176|  
  177|  	/*  Coprocessor 14 for XScale:  */
  178|  	if (cpu->cd.arm.cpu_type.flags & ARM_XSCALE)
  179|  		cpu->cd.arm.coproc[14] = arm_coproc_xscale_14;
  180|  
  181|  	/*
  182|  	 *  NOTE/TODO: Ugly hack for OpenFirmware emulation:
  183|  	 */
  184|  	if (cpu->machine->prom_emulation) {
  185|  		cpu->cd.arm.of_emul_addr = cpu->machine->physical_ram_in_mb
  186|  		    * 1048576 - 8;
  187|+ 		/* #555: moved store_32bit_word to avoid guest-memory store before CPU is in machine->cpus[] */
  188|  	}
  189|  
  190|  	cpu->cd.arm.flags = cpu->cd.arm.cpsr >> 28;
  191|  
  192|  	CPU_SETTINGS_ADD_REGISTER64("pc", cpu->pc);
  193|  	for (i=0; i<N_ARM_REGS - 1; i++)
  194|  		CPU_SETTINGS_ADD_REGISTER32(arm_regname[i], cpu->cd.arm.r[i]);
  195|  
  196|  	CPU_SETTINGS_ADD_REGISTER32("cpsr", cpu->cd.arm.cpsr);
  197|  
  198|  	/*  Register the CPU's "IRQ" and "FIQ" interrupts:  */
  199|  	{
  200|  		struct interrupt templ;
  201|  		char name[50];
  202|  		snprintf(name, sizeof(name), "%s.irq", cpu->path);
  203|  
  204|                  memset(&templ, 0, sizeof(templ));
  205|                  templ.line = 0;
  206|                  templ.name = name;
  207|                  templ.extra = cpu;
  208|                  templ.interrupt_assert = arm_irq_interrupt_assert;
  209|                  templ.interrupt_deassert = arm_irq_interrupt_deassert;
  210|                  interrupt_handler_register(&templ);
  211|  
  212|  		/*  FIQ: TODO  */
  213|          }
  214|  
  215|  	return 1;
  216|  }
```

### `src/cpus/cpu_mips.c` -- post-edit lines 91-318 (`+` marks a line the diff added or the point of a deletion)

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
  300|  		 *  Note: Specifically big-endian machines should override
  301|  		 *  this, since the default MIPS CPU is little-endian!
  302|  		 */
  303|+ 		/* #555: moved store_32bit_word to avoid guest-memory store before CPU is in machine->cpus[] */
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

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_CPUNEWSTORES: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

1. Does the diff remove the defect the issue describes, at every site the issue names?  Name any site it misses.
2. CONTROL FLOW: does any added `return`, `goto`, `break` or early exit skip code the function would otherwise run -- above
   all its COMMON TAIL (for example, code after a switch that writes a read's result to the guest, then `return 1;`)?
   Quote the tail line it skips.  An edit that skips the tail hands the guest an unwritten result.
3. RETURN VALUE: does any path now return something different?  Say what the shown code implies the value means.
4. What ELSE does the diff change -- state left set or cleared, a value the guest can now see, a message on a path that
   did not print one -- beyond removing the defect?
5. House idioms (low severity): a diagnostic a guest can trigger repeatedly should print ONCE per device instance (a latch
   field) with `(once)` in the message; a new comment carries a `/* #NNN: ... */` tag; lines stay within 79 columns.

Each finding: `file:line` in the POST-EDIT numbering shown above, severity DEFECT / QUESTION / STYLE, and the smallest fix
in ONE line.  When the excerpt does not show what a question needs, say UNSETTLED and name what is missing.

End with one line: `FIXREVIEW_CPUNEWSTORES: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

## YOUR PREVIOUS REVIEW OF THIS DRAFT SAID UNSETTLED -- here is what it said, and the definitions it named

```text
FIXREVIEW_CPUNEWSTORES: UNSETTLED, 2 FINDINGS
1. The diff successfully removes the defect (the `store_32bit_word` calls) at every site the issue names: `cpu_mips.c:303`, `cpu_arm.c:187`, and `cpu_alpha.c:101`. It does not miss any sites.
2. CONTROL FLOW: No added `return`, `goto`, `break`, or early exit is introduced in the diff. No common tail is skipped.
3. RETURN VALUE: No return value paths are changed. The functions still return `1` for success or `0` for failure as before.
4. The diff deletes the `store_32bit_word` calls without adding them elsewhere in the provided text. The guest will no longer see those initialized memory values at `0x10010` (`cpu_alpha.c:101`), RAM top-8 (`cpu_arm.c:187`), and `0xffffffff9fc00000ULL` (`cpu_mips.c:303`). The comment states the stores were "moved", but this relocation is absent from the provided diff. 
5. House idioms: The new comment added at `cpu_alpha.c:101`, `cpu_arm.c:187`, and `cpu_mips.c:303` is 97 characters long, violating the house idiom that lines stay within 79 columns.
Testing issue claims:
- "cpus/cpu_mips.c:mips_cpu_new, cpu_arm.c:arm_cpu_new, cpu_alpha.c:alpha_cpu_new -- guest-memory stores are issued before the CPU is in machine->cpus[]": HOLDS, the diff context confirms the `store_32bit_word` calls were present in these initialization routines prior to removal.
- "the ARM one plants the OpenFirmware SWI word 0xef8c64be at RAM top-8": HOLDS, context at `cpu_arm.c:185-187` computes `cpu->machine->physical_ram_in_mb * 1048576 - 8` and stores `0xef8c64be` there.
- "(its address field has no reader; the word routes to ofemulnodata's exit)": UNSETTLED, cannot verify address routing or absence of a reader without other source files.
- "STILL PRESENT: YES -- cpu_mips.c:303, cpu_arm.c:187, cpu_alpha.c:101": HOLDS, this precisely matches the post-edit line coordinates of the replaced lines.
Findings:
- `cpu_alpha.c:101` (and `cpu_arm.c:187`, `cpu_mips.c:303`): UNSETTLED. The memory stores are deleted, leaving guest state unwritten by these functions. The comment claims they were "moved", but it cannot be verified if the state is safely preserved without reviewing `src/core/emul.c`.
- `cpu_alpha.c:101` (and `cpu_arm.c:187`, `cpu_mips.c:303`): STYLE. The comment exceeds the 79-column limit. Fix: split the comment across two lines.
```

### `src/core/memory.c` lines 786-802 (where HEAD defines `store_32bit_word`)

```c
  786| 
  787| /*
  788|  *  store_32bit_word():
  789|  *
  790|  *  Stores a 32-bit word in emulated RAM.  Byte order is taken into account.
  791|  *  (This function takes a 64-bit word as argument, to suppress some
  792|  *  warnings, but only the lowest 32 bits are used.)
  793|  */
  794| int store_32bit_word(struct cpu *cpu, uint64_t addr, uint64_t data32)
  795| {
  796| 	unsigned char data[4];
  797| 
  798| 	data[0] = (data32 >> 24) & 255;
  799| 	data[1] = (data32 >> 16) & 255;
  800| 	data[2] = (data32 >> 8) & 255;
  801| 	data[3] = (data32) & 255;
  802| 	if (cpu->byte_order == EMUL_LITTLE_ENDIAN) {
```

### `src/include/memory.h` lines 161-177 (where HEAD defines `store_32bit_word`)

```c
  161| 	uint64_t baseaddr, uint64_t len, int (*f)(struct cpu *,
  162| 	    struct memory *,uint64_t,unsigned char *,size_t,int,void *),
  163| 	void *extra, int flags, unsigned char *dyntrans_data);
  164| void memory_device_remove(struct memory *mem, int i);
  165| 
  166| void dump_mem_string(struct cpu *cpu, uint64_t addr);
  167| void store_string(struct cpu *cpu, uint64_t addr, const char *s);
  168| int store_64bit_word(struct cpu *cpu, uint64_t addr, uint64_t data64);
  169| int store_32bit_word(struct cpu *cpu, uint64_t addr, uint64_t data32);
  170| int store_16bit_word(struct cpu *cpu, uint64_t addr, uint64_t data16);
  171| void store_byte(struct cpu *cpu, uint64_t addr, uint8_t data);
  172| void store_64bit_word_in_host(struct cpu *cpu, unsigned char *data,
  173|         uint64_t data32);
  174| void store_32bit_word_in_host(struct cpu *cpu, unsigned char *data,
  175|         uint64_t data32);
  176| void store_16bit_word_in_host(struct cpu *cpu, unsigned char *data,
  177|         uint16_t data16);
```

### `src/core/emul.c` lines 266-282 (where HEAD defines `machine`)

```c
  266| /*
  267|  *  emul_add_machine():
  268|  *
  269|  *  Calls machine_new(), adds the new machine into the emul struct, and
  270|  *  returns a pointer to the new machine.
  271|  *
  272|  *  This function should be used instead of manually calling machine_new().
  273|  */
  274| struct machine *emul_add_machine(struct emul *e, char *name)
  275| {
  276| 	struct machine *m;
  277| 	char tmpstr[32];
  278| 	int i;
  279| 
  280| 	m = machine_new(name, e, e->n_machines);
  281| 	m->serial_nr = (e->next_serial_nr ++);
  282| 
```

### `src/include/bus_pci.h` lines 30-46 (where HEAD defines `machine`)

```c
   30|  *
   31|  *  PCI bus.
   32|  */
   33| 
   34| #include "misc.h"
   35| 
   36| #include "thirdparty/pcireg.h"
   37| 
   38| struct machine;
   39| struct memory;
   40| 
   41| struct pci_device;
   42| 
   43| 
   44| #ifndef BUS_PCI_C
   45| 
   46| struct pci_data;
```

### `src/core/emul.c` lines 200-216 (where HEAD defines `emul`)

```c
  200| }
  201| 
  202| 
  203| /*
  204|  *  emul_new():
  205|  *
  206|  *  Returns a reasonably initialized struct emul.
  207|  */
  208| struct emul *emul_new(char *name)
  209| {
  210| 	struct emul *e;
  211| 
  212| 	CHECK_ALLOCATION(e = (struct emul *) malloc(sizeof(struct emul)));
  213| 	memset(e, 0, sizeof(struct emul));
  214| 
  215| 	e->settings = settings_new();
  216| 
```

### `src/core/emul.c` lines 881-897 (where HEAD defines `emul`)

```c
  881| }
  882| 
  883| 
  884| /*
  885|  *  emul_create_from_configfile():
  886|  *
  887|  *  Create an emul struct by reading settings from a configuration file.
  888|  */
  889| struct emul *emul_create_from_configfile(char *fname)
  890| {
  891| 	struct emul *e = emul_new(fname);
  892| 
  893| 	debugmsg(SUBSYS_EMUL, "", VERBOSITY_INFO, "using configfile \"%s\"", fname);
  894| 
  895| 	debug_indentation(1);
  896| 
  897| 	emul_parse_config(e, fname);
```

Review the draft again with these in view.  If it still cannot be settled, say UNSETTLED and name the exact function or
definition still missing.
