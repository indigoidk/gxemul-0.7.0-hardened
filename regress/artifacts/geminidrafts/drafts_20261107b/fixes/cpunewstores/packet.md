# GXemul hardened fork -- DRAFT A FIX for one filed issue, `cpunewstores` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 2d25df65).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `cpunewstores`, state `open`, severity `LOW`)

**title:** cpus/cpu_mips.c:mips_cpu_new, cpu_arm.c:arm_cpu_new, cpu_alpha.c:alpha_cpu_new -- guest-memory stores are issued before the CPU is in machine->cpus[]; the ARM one plants the OpenFirmware SWI word 0xef8c64be at RAM top-8 (its address field has no reader; the word routes to `ofemulnodata`'s exit) -- HYGIENE (latent; prerequisite for the SMP row)

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T147 (class HYGIENE; reach C, configuration, debugger, host environment or a non-default build; effort: small; report rows: A1-36, A1-40, A1-54, A1-60, B P2, B rec.5, C U2).  Source URLs: https://github.com/retroprom/gxemul/commit/d2462ba6, https://github.com/retroprom/gxemul/commit/77708717, https://github.com/skrll/gxemul/commit/a4e2335, https://github.com/NetBSD/pkgsrc/blob/trunk/emulators/gxemul/patches/patch-src_cpus_cpu__arm.c, https://github.com/Randrianasulu/GXemul/commit/9bfc91e.  Our site at de8c7547: src/cpus/cpu_mips.c:294-304; src/cpus/cpu_arm.c:181-188; src/cpus/cpu_alpha.c:99-103; src/core/emul.c:492-503.  Portable fix: yes -- port upstream d2462ba6, upstream 77708717 (= skrll a4e2335, pkgsrc patch-src_cpus_cpu__arm.c), r6577(k).  Filing check (TRIAGE.md): `#555` settled only the MIPS word's survival, OB:1895.  Reach C, not build-only (regress/artifacts/research_20261022/adj_20261022/ADJ_RULINGS.md B).  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- Portable fix available upstream.

## The code at the cited lines

### `src/cpus/cpu_mips.c` around the row's cited line 294 (HEAD 2d25df65, lines 249-339)

```c
  249| 		memset(&templ, 0, sizeof(templ));
  250| 		templ.line = 1 << (STATUS_IM_SHIFT + i);
  251| 		templ.name = name;
  252| 		templ.extra = cpu;
  253| 		templ.interrupt_assert = mips_cpu_interrupt_assert;
  254| 		templ.interrupt_deassert = mips_cpu_interrupt_deassert;
  255| 		interrupt_handler_register(&templ);
  256| 
  257| 		if (i == 7)
  258| 			INTERRUPT_CONNECT(name, cpu->cd.mips.irq_compare);
  259| 	}
  260| 
  261| 	/*  System coprocessor (0), and FPU (1):  */
  262| 	cpu->cd.mips.coproc[0] = mips_coproc_new(cpu, 0);
  263| 	cpu->cd.mips.coproc[1] = mips_coproc_new(cpu, 1);
  264| 
  265| 	switch (cpu->cd.mips.cpu_type.mmu_model) {
  266| 	case MMU3K:
  267| 		cpu->vaddr_mask = 0x00000000ffffffffULL;
  268| 		cpu->translate_v2p = translate_v2p_mmu3k;
  269| 		break;
  270| 	case MMU8K:
  271| 		cpu->translate_v2p = translate_v2p_mmu8k;
  272| 		break;
  273| 	case MMU10K:
  274| 		cpu->vaddr_mask = ENTRYHI_R_MASK | ENTRYHI_VPN2_MASK_R10K | 0x1fff;
  275| 		cpu->translate_v2p = translate_v2p_mmu10k;
  276| 		break;
  277| 	default:
  278| 		if (cpu->is_32bit)
  279| 			cpu->vaddr_mask = 0x00000000ffffffffULL;
  280| 		else
  281| 			cpu->vaddr_mask = ENTRYHI_R_MASK | ENTRYHI_VPN2_MASK | 0x1fff;
  282| 
  283| 		if (cpu->cd.mips.cpu_type.rev == MIPS_R4100)
  284| 			cpu->translate_v2p = translate_v2p_mmu4100;
  285| 		else
  286| 			cpu->translate_v2p = translate_v2p_generic;
  287| 	}
  288| 
  289| 	// TODO: Consider moving to src/machine/machine_test.c?
  290| 	// This is only here to make the floating point tests work out-of-the-box.
  291| 	if (!cpu->is_32bit)
  292| 		cpu->cd.mips.coproc[0]->reg[COP0_STATUS] |= STATUS_FR;
  293| 
  294| 	if (cpu->machine->prom_emulation) {
  295| 		/*
  296| 		 *  Default behaviour of jumping to 0xbfc00000 should be
  297| 		 *  a reboot, unless machine-specific initialization code
  298| 		 *  overrides this.
  299| 		 *
  300| 		 *  Note: Specifically big-endian machines should override
  301| 		 *  this, since the default MIPS CPU is little-endian!
  302| 		 */
  303| 		store_32bit_word(cpu, 0xffffffff9fc00000ULL, 0x00c0de0d);
  304| 	}
  305| 
  306| 	/*  Add all register names to the settings:  */
  307| 	CPU_SETTINGS_ADD_REGISTER64("pc", cpu->pc);
  308| 	CPU_SETTINGS_ADD_REGISTER64("hi", cpu->cd.mips.hi);
  309| 	CPU_SETTINGS_ADD_REGISTER64("lo", cpu->cd.mips.lo);
  310| 	for (i=0; i<N_MIPS_GPRS; i++)
  311| 		CPU_SETTINGS_ADD_REGISTER64(regnames[i], cpu->cd.mips.gpr[i]);
  312| 	/*  TODO: Write via special handler function!  */
  313| 	for (i=0; i<N_MIPS_COPROC_REGS; i++)
  314| 		CPU_SETTINGS_ADD_REGISTER64(cop0_names[i],
  315| 		    cpu->cd.mips.coproc[0]->reg[i]);
  316| 
  317| 	return 1;
  318| }
  319| 
  320| 
  321| /*
  322|  *  mips_cpu_dumpinfo():
  323|  *
  324|  *  Debug dump of MIPS-specific CPU data for specific CPU.
  325|  */
  326| void mips_cpu_dumpinfo(struct cpu *cpu, bool verbose)
  327| {
  328| 	struct mips_cpu_type_def *ct = &cpu->cd.mips.cpu_type;
  329| 	int secondary_cache_size = 0;
  330| 	if (cpu->cd.mips.cache_secondary)
  331| 		secondary_cache_size = 1 << cpu->cd.mips.cache_secondary;
  332| 
  333| 	if (!verbose) {
  334| 		debugmsg(SUBSYS_MACHINE, "cpu", VERBOSITY_INFO,
  335| 		    "%s (%i-bit, I+D = %i+%i KB, L2 = %i KB)",
  336| 		    cpu->name,
  337| 		    cpu->is_32bit? 32 : 64,
  338| 		    (int)(cpu->cd.mips.cache_size[CACHE_INSTRUCTION] / 1024),
  339| 		    (int)(cpu->cd.mips.cache_size[CACHE_DATA] / 1024),
```

### `src/cpus/cpu_arm.c` around the row's cited line 181 (HEAD 2d25df65, lines 136-226)

```c
  136| 		cpu->cd.arm.cpsr |= ARM_MODE_SVC32;
  137| 		cpu->cd.arm.control |= ARM_CONTROL_R;
  138| 	}
  139| 
  140| 	/*  #291: the cache-size fields are 3 bits wide and encode the size as
  141| 	    log2(bytes) - 9, but 32 of the entries in arm_cpu_types.h leave
  142| 	    dcache_shift at 0 (ARM1136JSR1, which the rpi machine selects, is
  143| 	    one). Those computed 0 - 9 = -9 and shifted it left, which is
  144| 	    undefined behaviour -- UBSan reports it on upstream 0.7.0 too, so
  145| 	    this is inherited, not introduced here.
  146| 
  147| 	    It is not merely undefined, it is WRONG: -9 does not stay inside
  148| 	    its 3-bit field. ARM1136JSR1 yielded 0xffdea0ea where 0x0b02a0ea
  149| 	    is correct, smearing 0xf4dc0000 across the CLASS and HARVARD
  150| 	    fields as well.
  151| 
  152| 	    Casting to unsigned would silence the sanitizer and leave the
  153| 	    register just as corrupt (measured: byte-identical 0xffdea0ea), so
  154| 	    it is not the fix. An unspecified size encodes as 0, and each
  155| 	    field is masked to its own width. CPUs that do specify both sizes
  156| 	    are unaffected -- ARM920T, SA110 and 80321_400 all produce exactly
  157| 	    the value they produced before.  */
  158| 	uint32_t dsize = cpu->cd.arm.cpu_type.dcache_shift >= 9 ?
  159| 	    (uint32_t) (cpu->cd.arm.cpu_type.dcache_shift - 9) : 0;
  160| 	uint32_t isize = cpu->cd.arm.cpu_type.icache_shift >= 9 ?
  161| 	    (uint32_t) (cpu->cd.arm.cpu_type.icache_shift - 9) : 0;
  162| 
  163| 	/*  TODO: Some of these values (iway and dway) aren't used yet:  */
  164| 	cpu->cd.arm.cachetype =
  165| 	      (5 << ARM_CACHETYPE_CLASS_SHIFT)
  166| 	    | (1 << ARM_CACHETYPE_HARVARD_SHIFT)
  167| 	    | ((dsize << ARM_CACHETYPE_DSIZE_SHIFT) & ARM_CACHETYPE_DSIZE)
  168| 	    | (5 << ARM_CACHETYPE_DASSOC_SHIFT)		/*  32-way  */
  169| 	    | (2 << ARM_CACHETYPE_DLINE_SHIFT)		/*  8 words/line  */
  170| 	    | ((isize << ARM_CACHETYPE_ISIZE_SHIFT) & ARM_CACHETYPE_ISIZE)
  171| 	    | (5 << ARM_CACHETYPE_IASSOC_SHIFT)		/*  32-way  */
  172| 	    | (2 << ARM_CACHETYPE_ILINE_SHIFT);		/*  8 words/line  */
  173| 
  174| 	/*  Coprocessor 15 = the system control coprocessor.  */
  175| 	cpu->cd.arm.coproc[15] = arm_coproc_15;
  176| 
  177| 	/*  Coprocessor 14 for XScale:  */
  178| 	if (cpu->cd.arm.cpu_type.flags & ARM_XSCALE)
  179| 		cpu->cd.arm.coproc[14] = arm_coproc_xscale_14;
  180| 
  181| 	/*
  182| 	 *  NOTE/TODO: Ugly hack for OpenFirmware emulation:
  183| 	 */
  184| 	if (cpu->machine->prom_emulation) {
  185| 		cpu->cd.arm.of_emul_addr = cpu->machine->physical_ram_in_mb
  186| 		    * 1048576 - 8;
  187| 		store_32bit_word(cpu, cpu->cd.arm.of_emul_addr, 0xef8c64be);
  188| 	}
  189| 
  190| 	cpu->cd.arm.flags = cpu->cd.arm.cpsr >> 28;
  191| 
  192| 	CPU_SETTINGS_ADD_REGISTER64("pc", cpu->pc);
  193| 	for (i=0; i<N_ARM_REGS - 1; i++)
  194| 		CPU_SETTINGS_ADD_REGISTER32(arm_regname[i], cpu->cd.arm.r[i]);
  195| 
  196| 	CPU_SETTINGS_ADD_REGISTER32("cpsr", cpu->cd.arm.cpsr);
  197| 
  198| 	/*  Register the CPU's "IRQ" and "FIQ" interrupts:  */
  199| 	{
  200| 		struct interrupt templ;
  201| 		char name[50];
  202| 		snprintf(name, sizeof(name), "%s.irq", cpu->path);
  203| 
  204|                 memset(&templ, 0, sizeof(templ));
  205|                 templ.line = 0;
  206|                 templ.name = name;
  207|                 templ.extra = cpu;
  208|                 templ.interrupt_assert = arm_irq_interrupt_assert;
  209|                 templ.interrupt_deassert = arm_irq_interrupt_deassert;
  210|                 interrupt_handler_register(&templ);
  211| 
  212| 		/*  FIQ: TODO  */
  213|         }
  214| 
  215| 	return 1;
  216| }
  217| 
  218| 
  219| /*
  220|  *  arm_setup_initial_translation_table():
  221|  *
  222|  *  When booting kernels (such as OpenBSD or NetBSD) directly, it is assumed
  223|  *  that the MMU is already enabled by the boot-loader. This function tries
  224|  *  to emulate that.
  225|  */
  226| void arm_setup_initial_translation_table(struct cpu *cpu, uint32_t ttb_addr)
```

### `src/cpus/cpu_alpha.c` around the row's cited line 99 (HEAD 2d25df65, lines 54-144)

```c
   54| 
   55| /*  Alpha symbolic register names:  */
   56| static const char *alpha_regname[N_ALPHA_REGS] = ALPHA_REG_NAMES; 
   57| 
   58| void alpha_irq_interrupt_assert(struct interrupt *interrupt);
   59| void alpha_irq_interrupt_deassert(struct interrupt *interrupt);
   60| 
   61| 
   62| /*
   63|  *  alpha_cpu_new():
   64|  *
   65|  *  Create a new Alpha CPU object by filling the CPU struct.
   66|  *  Return 1 on success, 0 if cpu_type_name isn't a valid Alpha processor.
   67|  */
   68| int alpha_cpu_new(struct cpu *cpu, struct memory *mem,
   69| 	struct machine *machine, int cpu_id, char *cpu_type_name)
   70| {
   71| 	int i = 0;
   72| 	struct alpha_cpu_type_def cpu_type_defs[] = ALPHA_CPU_TYPE_DEFS;
   73| 
   74| 	/*  Scan the cpu_type_defs list for this cpu type:  */
   75| 	while (cpu_type_defs[i].name != NULL) {
   76| 		if (strcasecmp(cpu_type_defs[i].name, cpu_type_name) == 0) {
   77| 			break;
   78| 		}
   79| 		i++;
   80| 	}
   81| 	if (cpu_type_defs[i].name == NULL)
   82| 		return 0;
   83| 
   84| 	cpu->is_32bit = 0;
   85| 	cpu->byte_order = EMUL_LITTLE_ENDIAN;
   86| 
   87| 	cpu->memory_rw = alpha_memory_rw;
   88| 	cpu->run_instr = alpha_run_instr;
   89| 	cpu->translate_v2p = alpha_translate_v2p;
   90| 	cpu->update_translation_table = alpha_update_translation_table;
   91| 	cpu->invalidate_translation_caches =
   92| 	    alpha_invalidate_translation_caches;
   93| 	cpu->invalidate_code_translation = alpha_invalidate_code_translation;
   94| 
   95| 	cpu->cd.alpha.cpu_type = cpu_type_defs[i];
   96| 
   97| 	cpu->cd.alpha.r[ALPHA_SP] = 0xfffffc000000ff00ULL;
   98| 
   99| 	/*  Set up dummy kentry pointers to something which crashes
  100| 	    the machine:  */
  101| 	store_32bit_word(cpu, 0x10010, 0x3fffffc);
  102| 	for (i=0; i<N_ALPHA_KENTRY; i++)
  103| 		cpu->cd.alpha.kentry[i] = 0x10010;
  104| 
  105| 	/*  Bogus initial context (will be overwritten on first
  106| 	    context switch):  */
  107| 	cpu->cd.alpha.ctx = 0x10100;
  108| 
  109| 	CPU_SETTINGS_ADD_REGISTER64("pc", cpu->pc);
  110| 	for (i=0; i<N_ALPHA_REGS; i++)
  111| 		CPU_SETTINGS_ADD_REGISTER64(alpha_regname[i],
  112| 		    cpu->cd.alpha.r[i]);
  113| 
  114| 	/*  Register the CPU interrupt pin:  */
  115| 	{
  116| 		struct interrupt templ;
  117| 
  118| 		memset(&templ, 0, sizeof(templ));
  119| 		templ.line = 0;
  120| 		templ.name = cpu->path;
  121| 		templ.extra = cpu;
  122| 		templ.interrupt_assert = alpha_irq_interrupt_assert; 
  123| 		templ.interrupt_deassert = alpha_irq_interrupt_deassert; 
  124| 		interrupt_handler_register(&templ);
  125| 	}
  126| 
  127| 	return 1;
  128| }
  129| 
  130| 
  131| /*
  132|  *  alpha_cpu_dumpinfo():
  133|  */
  134| void alpha_cpu_dumpinfo(struct cpu *cpu, bool verbose)
  135| {
  136| 	debugmsg(SUBSYS_MACHINE, "cpu", VERBOSITY_INFO, "%s", cpu->name);
  137| }
  138| 
  139| 
  140| /*
  141|  *  alpha_cpu_list_available_types():
  142|  *
  143|  *  Print a list of available Alpha CPU types.
  144|  */
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

End with one line: `FIXDRAFT_CPUNEWSTORES: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
