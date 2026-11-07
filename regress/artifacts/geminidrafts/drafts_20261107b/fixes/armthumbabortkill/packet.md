# GXemul hardened fork -- DRAFT A FIX for one filed issue, `armthumbabortkill` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 8d9df658).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `armthumbabortkill`, state `open`, severity `HIGH`)

**title:** cpu_arm.c: FIVE Thumb sites halt the emulator AFTER the abort is already delivered and T cleared -- the halt PREVENTS THE GUEST'S ABORT HANDLER FROM RUNNING

**state_note (head):**

[2026-11-02, records] #562 as landed (4f908ad5) shifts cpu_arm.c by +50, not +42: the five filed sites are :1277, :1607, :1650, :1679, :1703 at 987cb596.  ||  2026-10-07 pre-brief READING (Opus 5.5, read-only, nothing run; brief not written -- the seat's response was classifier-stopped at the witness-design step): (1) the row's own reopen condition (an MMU-on ARM vehicle) is NOT met by arm_msrmode_probe.py; owner asked whether to reopen anyway.  (2) on ARM a failing DEVICE read raises no exception (memory_rw.c's exception arms are MIPS/M88K only), so a bare delete of running=0 with `return 0` would re-run the Thumb instruction forever with an unlatched fatal() -- argues for a conditional decline; unreachable on testarm (all seven devices return 1).  (3) candidate siblings, UNVERIFIED: the PC-relative site passes CACHE_INSTRUCTION -> Prefetch Abort where Thumb LDR(3) is a Data Abort (ddi0100i.txt:23050-23051); Thumb pc bit 0 may make the saved abort return address 1 low; testarm's default SA1110 is ARMv4 with no Thumb (seat's recollection, unchecked) -- ANSWERED 2026-10-09 (Fable 5.1's regress review of #562, finding 2, regress/artifacts/armmsrmodekill/regress_20261009/fable5_regress562.md): src/include/arm_cpu_types.h has NO Thumb capability field and cpu_dyntrans.c selects arm_cpu_interpret_thumb_SLOW on ARM_FLAG_T alone, as the armmmuvehicle record already says from agy's research -- T alone selects the Thumb interpreter on any ARM CPU here.  Cite sites by grep anchor: #562 shifts cpu_arm.c by +42.  ||  filed 2026-09-17 from the grok seat's site-by-site triage of cpu_arm.c (the cpusexitsweep research row).  **FIVE SITES, ONE DEFECT: 1227, 1557, 1600, 1629, 1653.**  *** IT IS A FUNCTIONAL DEFECT, NOT MERELY A HALT, WHICH IS WHY IT IS HIGH AND IS NOT PART OF THE CENSUS: on an MMU fault the abort is ALREADY DELIVERED and T is ALREADY CLEARED, so the `cpu->running = 0' that follows PREVENTS THE GUEST'S OWN ABORT HANDLER FROM EVER RUNNING.  A guest that would have recovered instead stops. ***  DISPOSITION: option-set member 1 DELETE -- match the ARM load/store path.  **KEEP the `return 0'; do NOT fall through to `pc += 2'.**  IN-TREE PRECEDENT: #312 said of the ARM-mode analogue that 'halting was never right'.  SELECTOR: a guest-supplied instruction or address in arm_cpu_interpret_thumb_SLOW, which is the PRODUCTION Thumb path -- cpu_dyntrans.c calls it whenever ARM_FLAG_T is set and ignores its return value -- so these are reachable by any Thumb guest taking a memory fault.  NOT YET WITNESSED: no probe has been built.  This is a READING by a file-reading seat, and the round that takes it owes the rung-3 ATTEMPT the 2026-08-27 lifecycle ruling requires.  *** WITNESS DISPOSITION: DOCUMENTED-ONLY, WITH THE ATTEMPT RECORDED.  DO NOT BUILD `regress/arm_thumbabort_probe.py` FROM THE SPEC, AND DO NOT BUILD A PATCHED COPY IN THIS CAMPAIGN. ***  The lifecycle ask is satisfied in the form it was written for: a seat WAS asked to try a rung-3 probe, DID specify one, and then condemned its own spec against the tree.  So `none` here means 'tried; the vehicle costs a new MMU-on ARM harness that this row does not outrank', NOT 'did not think to' -- which are different states and must not render the same. THIRTEEN HOLES, derived against source rather than restated.  **The two that end the question:** *** HOLE 3 -- THE `t ifetch` ROW (site 1227) IS VACUOUS BY CONSTRUCTION AND THE SPEC'S OWN SCORE IS THEREFORE A WRONG RECORD. ***  `X(bx)` sets T before `qui [... 4776 more characters not shown]

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- delete cpu->running = 0 but keep return 0 at the 5 Thumb sites

## The code at the cited lines

### `src/cpus/cpu_dyntrans.c` around the row's cited line 177 (HEAD 8d9df658, lines 57-297)

```c
   57| 	/*  low_pc must be within the page!  */
   58| 	if (low_pc < 0 || low_pc > DYNTRANS_IC_ENTRIES_PER_PAGE)
   59| 		return;
   60| 
   61| 	buf[0] = '\0';
   62| 
   63| 	while ((ch = cpu->machine->statistics.fields[i]) != '\0') {
   64| 		if (i != 0)
   65| 			strlcat(buf, " ", sizeof(buf));
   66| 
   67| 		switch (ch) {
   68| 		case 'i':
   69| 			snprintf(buf + strlen(buf), sizeof(buf),
   70| 			    "%p", (void *)ic->f);
   71| 			break;
   72| 		case 'p':
   73| 			/*  Physical program counter address:  */
   74| 			cpu->cd.DYNTRANS_ARCH.cur_physpage = (struct DYNTRANS_TC_PHYSPAGE *)
   75| 			    cpu->cd.DYNTRANS_ARCH.cur_ic_page;
   76| 			a = cpu->cd.DYNTRANS_ARCH.cur_physpage->physaddr;
   77| 			a &= ~((DYNTRANS_IC_ENTRIES_PER_PAGE-1) <<
   78| 			    DYNTRANS_INSTR_ALIGNMENT_SHIFT);
   79| 			a += low_pc << DYNTRANS_INSTR_ALIGNMENT_SHIFT;
   80| 			if (cpu->is_32bit)
   81| 				snprintf(buf + strlen(buf), sizeof(buf),
   82| 				    "0x%08" PRIx32, (uint32_t)a);
   83| 			else
   84| 				snprintf(buf + strlen(buf), sizeof(buf),
   85| 				    "0x%016" PRIx64, (uint64_t)a);
   86| 			break;
   87| 		case 'v':
   88| 			/*  Virtual program counter address:  */
   89| 			a = cpu->pc;
   90| 			a &= ~((DYNTRANS_IC_ENTRIES_PER_PAGE-1) <<
   91| 			    DYNTRANS_INSTR_ALIGNMENT_SHIFT);
   92| 			a += low_pc << DYNTRANS_INSTR_ALIGNMENT_SHIFT;
   93| 			if (cpu->is_32bit)
   94| 				snprintf(buf + strlen(buf), sizeof(buf),
   95| 				    "0x%08" PRIx32, (uint32_t)a);
   96| 			else
   97| 				snprintf(buf + strlen(buf), sizeof(buf),
   98| 				    "0x%016" PRIx64, (uint64_t)a);
   99| 			break;
  100| 		}
  101| 		i++;
  102| 	}
  103| 
  104| 	fprintf(cpu->machine->statistics.file, "%s\n", buf);
  105| }
  106| 
  107| 
  108| #define S		gather_statistics(cpu)
  109| 
  110| 
  111| #if 1
  112| 
  113| /*  The normal instruction execution core:  */
  114| #define I	ic = cpu->cd.DYNTRANS_ARCH.next_ic ++; ic->f(cpu, ic);
  115| 
  116| #else
  117| 
  118| /*  For heavy debugging:  */
  119| #define I	ic = cpu->cd.DYNTRANS_ARCH.next_ic ++;	\
  120| 		{	\
  121| 			int low_pc = ((size_t)cpu->cd.DYNTRANS_ARCH.next_ic - \
  122| 			    (size_t)cpu->cd.DYNTRANS_ARCH.cur_ic_page) / \
  123| 			    sizeof(struct DYNTRANS_IC);			\
  124| 			printf("cur_ic_page=%p ic=%p (low_pc=0x%x)\n",	\
  125| 			    cpu->cd.DYNTRANS_ARCH.cur_ic_page,		\
  126| 			    ic, low_pc << DYNTRANS_INSTR_ALIGNMENT_SHIFT); \
  127| 		} \
  128| 		ic->f(cpu, ic);
  129| 
  130| #endif
  131| 
  132| /*  static long long nr_of_I_calls = 0;  */
  133| 
  134| /*  Temporary hack for finding NULL bugs:  */
  135| /*  #define I	ic = cpu->cd.DYNTRANS_ARCH.next_ic ++; 			\
  136| 		nr_of_I_calls ++;					\
  137| 		if (ic->f == NULL) {					\
  138| 			int low_pc = ((size_t)cpu->cd.DYNTRANS_ARCH.next_ic - \
  139| 			    (size_t)cpu->cd.DYNTRANS_ARCH.cur_ic_page) / \
  140| 			    sizeof(struct DYNTRANS_IC);			\
  141| 			cpu->pc &= ~((DYNTRANS_IC_ENTRIES_PER_PAGE-1) << \
  142| 			    DYNTRANS_INSTR_ALIGNMENT_SHIFT);		\
  143| 			cpu->pc += (low_pc << DYNTRANS_INSTR_ALIGNMENT_SHIFT);\
  144| 			printf("Crash at %016" PRIx64"\n", cpu->pc);	\
  145| 			printf("nr of I calls: %lli\n", nr_of_I_calls);	\
  146| 			printf("Next ic = %p\n", cpu->cd.		\
  147| 				DYNTRANS_ARCH.next_ic);			\
  148| 			printf("cur ic page = %p\n", cpu->cd.		\
  149| 				DYNTRANS_ARCH.cur_ic_page);		\
  150| 			cpu->running = 0;				\
  151| 			return 0;					\
  152| 		}							\
  153| 		ic->f(cpu, ic);  */
  154| 
  155| /*  Temporary hack for MIPS, to hunt for 32-bit/64-bit sign-extension bugs:  */
  156| /*  #define I		{ int k; for (k=1; k<=31; k++)	\
  157| 	cpu->cd.mips.gpr[k] = (int32_t)cpu->cd.mips.gpr[k];\
  158| 	if (cpu->cd.mips.gpr[0] != 0) {			\
  159| 		fatal("NOOOOOO\n"); exit(1);		\
  160| 	}						\
  161| 	ic = cpu->cd.DYNTRANS_ARCH.next_ic ++; ic->f(cpu, ic); }
  162| */
  163| #endif	/*  STATIC STUFF  */
  164| 
  165| 
  166| 
  167| #ifdef	DYNTRANS_RUN_INSTR_DEF
  168| /*
  169|  *  XXX_run_instr():
  170|  *
  171|  *  Execute one or more instructions on a specific CPU, using dyntrans.
  172|  *  (For dualmode archs, this function is included twice.)
  173|  *
  174|  *  Return value is the number of instructions executed during this call,
  175|  *  0 if no instructions were executed.
  176|  */
  177| int DYNTRANS_RUN_INSTR_DEF(struct cpu *cpu)
  178| {
  179| 	MODE_uint_t cached_pc;
  180| 	int low_pc, n_instrs;
  181| 
  182| 	/*  Ugly... fix this some day.  */
  183| #ifdef DYNTRANS_DUALMODE_32
  184| #ifdef MODE32
  185| 	DYNTRANS_PC_TO_POINTERS32(cpu);
  186| #else
  187| 	DYNTRANS_PC_TO_POINTERS(cpu);
  188| #endif
  189| #else
  190| 	DYNTRANS_PC_TO_POINTERS(cpu);
  191| #endif
  192| 
  193| 	cpu->wants_to_idle = false;
  194| 
  195| 	/*
  196| 	 *  Interrupt assertion?  (This is _below_ the initial PC to pointer
  197| 	 *  conversion; if the conversion caused an exception of some kind
  198| 	 *  then interrupts are probably disabled, and the exception will get
  199| 	 *  priority over device interrupts.)
  200| 	 *
  201| 	 *  TODO: Turn this into a family-specific function somewhere...
  202|  	 */
  203| 
  204| 	/*  Note: Do not cause interrupts while single-stepping. It is
  205| 	    so horribly annoying.  */
  206| 	if (!single_step) {
  207| #ifdef DYNTRANS_ARM
  208| 		if (cpu->cd.arm.irq_asserted && !(cpu->cd.arm.cpsr & ARM_FLAG_I))
  209| 			arm_exception(cpu, ARM_EXCEPTION_IRQ);
  210| #endif
  211| #ifdef DYNTRANS_M88K
  212| 		if (cpu->cd.m88k.irq_asserted &&
  213| 		    !(cpu->cd.m88k.cr[M88K_CR_PSR] & M88K_PSR_IND))
  214| 			m88k_exception(cpu, M88K_EXCEPTION_INTERRUPT, 0);
  215| #endif
  216| #ifdef DYNTRANS_MIPS
  217| 		int enabled, mask;
  218| 		int status = cpu->cd.mips.coproc[0]->reg[COP0_STATUS];
  219| 		if (cpu->cd.mips.cpu_type.exc_model == EXC3K) {
  220| 			/*  R3000:  */
  221| 			enabled = status & MIPS_SR_INT_IE;
  222| 		} else {
  223| 			/*  R4000 and others:  */
  224| 			enabled = (status & STATUS_IE)
  225| 			    && !(status & STATUS_EXL) && !(status & STATUS_ERL);
  226| 			/*  Special case for R5900/C790/TX79:  */
  227| 			if (cpu->cd.mips.cpu_type.rev == MIPS_R5900 &&
  228| 			    !(status & R5900_STATUS_EIE))
  229| 				enabled = 0;
  230| 		}
  231| 		mask = status & cpu->cd.mips.coproc[0]->reg[COP0_CAUSE]
  232| 		    & STATUS_IM_MASK;
  233| 
  234| 		if (enabled && mask)
  235| 			mips_cpu_exception(cpu, EXCEPTION_INT, 0, 0, 0, 0, 0,0);
  236| #endif
  237| #ifdef DYNTRANS_PPC
  238| 		if (cpu->cd.ppc.dec_intr_pending && cpu->cd.ppc.msr & PPC_MSR_EE) {
  239| 			if (!(cpu->cd.ppc.cpu_type.flags & PPC_NO_DEC))
  240| 				ppc_exception(cpu, PPC_EXCEPTION_DEC);
  241| 			cpu->cd.ppc.dec_intr_pending = 0;
  242| 		}
  243| 		if (cpu->cd.ppc.irq_asserted && cpu->cd.ppc.msr & PPC_MSR_EE)
  244| 			ppc_exception(cpu, PPC_EXCEPTION_EI);
  245| #endif
  246| #ifdef DYNTRANS_SH
  247| 		if (cpu->cd.sh.int_to_assert > 0 && !(cpu->cd.sh.sr & SH_SR_BL)
  248| 		    && ((cpu->cd.sh.sr & SH_SR_IMASK) >> SH_SR_IMASK_SHIFT)
  249| 		    < cpu->cd.sh.int_level)
  250| 			sh_exception(cpu, 0, cpu->cd.sh.int_to_assert, 0);
  251| #endif
  252| 	}
  253| 
  254| #ifdef DYNTRANS_ARM
  255| 	if (cpu->cd.arm.cpsr & ARM_FLAG_T) {
  256| 		// fatal("THUMB execution not implemented.\n");
  257| 		// cpu->running = false;
  258| 		// return 0;
  259| 		
  260| 		arm_cpu_interpret_thumb_SLOW(cpu);
  261| 		return 1;
  262| 	}
  263| #endif
  264| 
  265| 	cached_pc = cpu->pc;
  266| 
  267| 	cpu->n_translated_instrs = 0;
  268| 
  269| 	cpu->cd.DYNTRANS_ARCH.cur_physpage = (struct DYNTRANS_TC_PHYSPAGE *)
  270| 	    cpu->cd.DYNTRANS_ARCH.cur_ic_page;
  271| 
  272| 	if (single_step || cpu->machine->instruction_trace
  273| 	    || cpu->machine->register_dump) {
  274| 		/*
  275| 		 *  Single-step:
  276| 		 */
  277| 		struct DYNTRANS_IC *ic = cpu->cd.DYNTRANS_ARCH.next_ic;
  278| 		if (cpu->machine->register_dump) {
  279| 			debug("\n");
  280| 			cpu_register_dump(cpu->machine, cpu, 1, 0x1);
  281| 		}
  282| 		if (single_step || cpu->machine->instruction_trace) {
  283| 			/*  TODO/Note: This must be large enough to hold
  284| 			    any instruction for any ISA:  */
  285| 			unsigned char instr[1 <<
  286| 			    DYNTRANS_INSTR_ALIGNMENT_SHIFT];
  287| 			if (!cpu->memory_rw(cpu, cpu->mem, cached_pc, &instr[0],
  288| 			    sizeof(instr), MEM_READ, CACHE_INSTRUCTION)) {
  289| 				fatal("XXX_run_instr(): could not read "
  290| 				    "the instruction\n");
  291| 			} else {
  292| #ifdef DYNTRANS_DELAYSLOT
  293| 				int len =
  294| #endif
  295| 				    cpu_disassemble_instr(
  296| 				    cpu->machine, cpu, instr, 1, cpu->pc);
  297| #ifdef DYNTRANS_DELAYSLOT
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

End with one line: `FIXDRAFT_ARMTHUMBABORTKILL: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
