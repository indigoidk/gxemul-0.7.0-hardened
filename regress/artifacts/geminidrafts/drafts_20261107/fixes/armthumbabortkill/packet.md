# GXemul hardened fork -- DRAFT A FIX for one filed issue, `armthumbabortkill` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 2d25df65).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `armthumbabortkill`, state `open`, severity `HIGH`)

**title:** cpu_arm.c: FIVE Thumb sites halt the emulator AFTER the abort is already delivered and T cleared -- the halt PREVENTS THE GUEST'S ABORT HANDLER FROM RUNNING

**state_note (head):**

[2026-11-02, records] #562 as landed (4f908ad5) shifts cpu_arm.c by +50, not +42: the five filed sites are :1277, :1607, :1650, :1679, :1703 at 987cb596.  ||  2026-10-07 pre-brief READING (Opus 5.5, read-only, nothing run; brief not written -- the seat's response was classifier-stopped at the witness-design step): (1) the row's own reopen condition (an MMU-on ARM vehicle) is NOT met by arm_msrmode_probe.py; owner asked whether to reopen anyway.  (2) on ARM a failing DEVICE read raises no exception (memory_rw.c's exception arms are MIPS/M88K only), so a bare delete of running=0 with `return 0` would re-run the Thumb instruction forever with an unlatched fatal() -- argues for a conditional decline; unreachable on testarm (all seven devices return 1).  (3) candidate siblings, UNVERIFIED: the PC-relative site passes CACHE_INSTRUCTION -> Prefetch Abort where Thumb LDR(3) is a Data Abort (ddi0100i.txt:23050-23051); Thumb pc bit 0 may make the saved abort return address 1 low; testarm's default SA1110 is ARMv4 with no Thumb (seat's recollection, unchecked) -- ANSWERED 2026-10-09 (Fable 5.1's regress review of #562, finding 2, regress/artifacts/armmsrmodekill/regress_20261009/fable5_regress562.md): src/include/arm_cpu_types.h has NO Thumb capability field and cpu_dyntrans.c selects arm_cpu_interpret_thumb_SLOW on ARM_FLAG_T alone, as the armmmuvehicle record already says from agy's research -- T alone selects the Thumb interpreter on any ARM CPU here.  Cite sites by grep anchor: #562 shifts cpu_arm.c by +42.  ||  filed 2026-09-17 from the grok seat's site-by-site triage of cpu_arm.c (the cpusexitsweep research row).  **FIVE SITES, ONE DEFECT: 1227, 1557, 1600, 1629, 1653.**  *** IT IS A FUNCTIONAL DEFECT, NOT MERELY A HALT, WHICH IS WHY IT IS HIGH AND IS NOT PART OF THE CENSUS: on an MMU fault the abort is ALREADY DELIVERED and T is ALREADY CLEARED, so the `cpu->running = 0' that follows PREVENTS THE GUEST'S OWN ABORT HANDLER FROM EVER RUNNING.  A guest that would have recovered instead stops. ***  DISPOSITION: option-set member 1 DELETE -- match the ARM load/store path.  **KEEP the `return 0'; do NOT fall through to `pc += 2'.**  IN-TREE PRECEDENT: #312 said of the ARM-mode analogue that 'halting was never right'.  SELECTOR: a guest-supplied instruction or address in arm_cpu_interpret_thumb_SLOW, which is the PRODUCTION Thumb path -- cpu_dyntrans.c calls it whenever ARM_FLAG_T is set and ignores its return value -- so these are reachable by any Thumb guest taking a memory fault.  NOT YET WITNESSED: no probe has been built.  This is a READING by a file-reading seat, and the round that takes it owes the rung-3 ATTEMPT the 2026-08-27 lifecycle ruling requires.  *** WITNESS DISPOSITION: DOCUMENTED-ONLY, WITH THE ATTEMPT RECORDED.  DO NOT BUILD `regress/arm_thumbabort_probe.py` FROM THE SPEC, AND DO NOT BUILD A PATCHED COPY IN THIS CAMPAIGN. ***  The lifecycle ask is satisfied in the form it was written for: a seat WAS asked to try a rung-3 probe, DID specify one, and then condemned its own spec against the tree.  So `none` here means 'tried; the vehicle costs a new MMU-on ARM harness that this row does not outrank', NOT 'did not think to' -- which are different states and must not render the same. THIRTEEN HOLES, derived against source rather than restated.  **The two that end the question:** *** HOLE 3 -- THE `t ifetch` ROW (site 1227) IS VACUOUS BY CONSTRUCTION AND THE SPEC'S OWN SCORE IS THEREFORE A WRONG RECORD. ***  `X(bx)` sets T before `qui [... 4776 more characters not shown]

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- delete cpu->running = 0 but keep return 0 at the 5 Thumb sites

## The code at the cited lines

### `src/cpus/cpu_dyntrans.c` around the row's cited line 177 (HEAD 2d25df65, lines 132-222)

```c
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

End with one line: `FIXDRAFT_ARMTHUMBABORTKILL: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
