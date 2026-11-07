# GXemul hardened fork -- DRAFT A FIX for one filed issue, `mipseidicu0` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 8d9df658).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `mipseidicu0`, state `open`, severity `MED`)

**title:** src/cpus/cpu_mips_instr.c:2719-2726 -- the Release-2 EI/DI handler X(ei_or_di) writes Status.IE with no cop0_availability_check, so user mode gets no Coprocessor Unusable exception -- WRONG-RESULT (user mode, Release-2 CPUs)

**state_note (head):**



**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- add cop0_availability_check before setting or clearing Status.IE

## The code at the cited lines

### `src/cpus/cpu_mips_instr.c` around the row's cited line 2719 (HEAD 8d9df658, lines 2599-2839)

```c
 2599| 	    / sizeof(struct mips_instr_call);
 2600| 	cpu->pc &= ~((MIPS_IC_ENTRIES_PER_PAGE-1)<< MIPS_INSTR_ALIGNMENT_SHIFT);
 2601| 	cpu->pc += (low_pc << MIPS_INSTR_ALIGNMENT_SHIFT);
 2602| 	mips_cpu_exception(cpu, EXCEPTION_SYS, 0, 0, 0, 0, 0, 0);
 2603| }
 2604| X(break)
 2605| {
 2606| 	int low_pc = ((size_t)ic - (size_t)cpu->cd.mips.cur_ic_page)
 2607| 	    / sizeof(struct mips_instr_call);
 2608| 	cpu->pc &= ~((MIPS_IC_ENTRIES_PER_PAGE-1)<< MIPS_INSTR_ALIGNMENT_SHIFT);
 2609| 	cpu->pc += (low_pc << MIPS_INSTR_ALIGNMENT_SHIFT);
 2610| 	mips_cpu_exception(cpu, EXCEPTION_BP, 0, 0, 0, 0, 0, 0);
 2611| }
 2612| X(reboot)
 2613| {
 2614| 	if (!cop0_availability_check(cpu, ic))
 2615| 		return;
 2616| 
 2617| 	cpu->running = false;
 2618| 	cpu->cd.mips.next_ic = &nothing_call;
 2619| }
 2620| 
 2621| 
 2622| /*
 2623|  *  promemul:  PROM software emulation.
 2624|  */
 2625| X(promemul)
 2626| {
 2627| 	/*  Synchronize the PC and call the correct emulation layer:  */
 2628| 	MODE_int_t old_pc;
 2629| 	int res, low_pc = ((size_t)ic - (size_t)cpu->cd.mips.cur_ic_page)
 2630| 	    / sizeof(struct mips_instr_call);
 2631| 	cpu->pc &= ~((MIPS_IC_ENTRIES_PER_PAGE-1)<< MIPS_INSTR_ALIGNMENT_SHIFT);
 2632| 	cpu->pc += (low_pc << MIPS_INSTR_ALIGNMENT_SHIFT);
 2633| 	old_pc = cpu->pc;
 2634| 
 2635| 	switch (cpu->machine->machine_type) {
 2636| 	case MACHINE_PMAX:
 2637| 		res = decstation_prom_emul(cpu);
 2638| 		break;
 2639| 	case MACHINE_PS2:
 2640| 		res = playstation2_sifbios_emul(cpu);
 2641| 		break;
 2642| 	case MACHINE_ARC:
 2643| 	case MACHINE_SGI:
 2644| 		res = arcbios_emul(cpu);
 2645| 		break;
 2646| 	case MACHINE_EVBMIPS:
 2647| 		res = yamon_emul(cpu);
 2648| 		break;
 2649| 	default:fatal("TODO: Unimplemented machine type for PROM magic trap\n");
 2650| 		exit(1);
 2651| 	}
 2652| 
 2653| 	if (res) {
 2654| 		/*  Return from the PROM call:  */
 2655| 		cpu->pc = (MODE_int_t)cpu->cd.mips.gpr[MIPS_GPR_RA];
 2656| 		cpu->delay_slot = NOT_DELAYED;
 2657| 
 2658| 		if (cpu->machine->show_trace_tree)
 2659| 			cpu_functioncall_trace_return(cpu);
 2660| 	} else {
 2661| 		/*  The PROM call blocks.  */
 2662| 		cpu->n_translated_instrs += 10;
 2663| 		cpu->pc = old_pc;
 2664| 	}
 2665| 
 2666| 	quick_pc_to_pointers(cpu);
 2667| }
 2668| 
 2669| 
 2670| /*
 2671|  *  tlbw: TLB write indexed and random
 2672|  *
 2673|  *  arg[0] = 1 for random, 0 for indexed
 2674|  *  arg[2] = relative addr of this instruction within the page
 2675|  */
 2676| X(tlbw)
 2677| {
 2678| 	if (!cop0_availability_check(cpu, ic))
 2679| 		return;
 2680| 
 2681| 	cpu->pc &= ~((MIPS_IC_ENTRIES_PER_PAGE-1)<<MIPS_INSTR_ALIGNMENT_SHIFT);
 2682| 	cpu->pc |= ic->arg[2];
 2683| 	coproc_tlbwri(cpu, ic->arg[0]);
 2684| }
 2685| 
 2686| 
 2687| /*
 2688|  *  tlbp: TLB probe
 2689|  *  tlbr: TLB read
 2690|  *
 2691|  *  arg[2] = relative addr of this instruction within the page
 2692|  */
 2693| X(tlbp)
 2694| {
 2695| 	if (!cop0_availability_check(cpu, ic))
 2696| 		return;
 2697| 
 2698| 	cpu->pc &= ~((MIPS_IC_ENTRIES_PER_PAGE-1)<<MIPS_INSTR_ALIGNMENT_SHIFT);
 2699| 	cpu->pc |= ic->arg[2];
 2700| 	coproc_tlbpr(cpu, 0);
 2701| }
 2702| X(tlbr)
 2703| {
 2704| 	if (!cop0_availability_check(cpu, ic))
 2705| 		return;
 2706| 
 2707| 	cpu->pc &= ~((MIPS_IC_ENTRIES_PER_PAGE-1)<<MIPS_INSTR_ALIGNMENT_SHIFT);
 2708| 	cpu->pc |= ic->arg[2];
 2709| 	coproc_tlbpr(cpu, 1);
 2710| }
 2711| 
 2712| 
 2713| /*
 2714|  *  ei_or_di:  MIPS32/64 rev 2, Enable or disable interrupts
 2715|  *
 2716|  *  arg[0] = ptr to rt
 2717|  *  arg[1] = non-zero to enable interrupts
 2718|  */
 2719| X(ei_or_di)
 2720| {
 2721| 	reg(ic->arg[0]) = cpu->cd.mips.coproc[0]->reg[COP0_STATUS];
 2722| 	if (ic->arg[1])
 2723| 		cpu->cd.mips.coproc[0]->reg[COP0_STATUS] |= STATUS_IE;
 2724| 	else
 2725| 		cpu->cd.mips.coproc[0]->reg[COP0_STATUS] &= ~STATUS_IE;
 2726| }
 2727| 
 2728| 
 2729| /*
 2730|  *  rfe: Return from exception handler (R2000/R3000)
 2731|  */
 2732| X(rfe)
 2733| {
 2734| 	if (!cop0_availability_check(cpu, ic))
 2735| 		return;
 2736| 
 2737| 	/*  Just rotate the interrupt/user bits:  */
 2738| 	/*  #230: (panel: Codex/Fable/agy/Ollama) R3000 RFE pops the KU/IE
 2739| 	    stack bits [3:0]<-[5:2] but leaves [5:4] (KUo/IEo) UNCHANGED; the
 2740| 	    old ~0x3f wrongly cleared [5:4], losing the outer privilege/interrupt
 2741| 	    level across nested exceptions.  */
 2742| 	cpu->cd.mips.coproc[0]->reg[COP0_STATUS] =
 2743| 	    (cpu->cd.mips.coproc[0]->reg[COP0_STATUS] & ~0x0f) |
 2744| 	    ((cpu->cd.mips.coproc[0]->reg[COP0_STATUS] & 0x3c) >> 2);
 2745| 
 2746| 	/*
 2747| 	 *  Note: no pc to pointers conversion is necessary here. Usually the
 2748| 	 *  rfe instruction resides in the delay slot of a jr k0/k1, and
 2749| 	 *  it is up to that instruction to do the pointer conversion.
 2750| 	 */
 2751| }
 2752| 
 2753| 
 2754| /*
 2755|  *  eret: Return from exception handler (non-R3000 style)
 2756|  */
 2757| X(eret)
 2758| {
 2759| 	if (!cop0_availability_check(cpu, ic))
 2760| 		return;
 2761| 
 2762| 	if (cpu->cd.mips.coproc[0]->reg[COP0_STATUS] & STATUS_ERL) {
 2763| 		cpu->pc = cpu->cd.mips.coproc[0]->reg[COP0_ERROREPC];
 2764| 		cpu->cd.mips.coproc[0]->reg[COP0_STATUS] &= ~STATUS_ERL;
 2765| 	} else {
 2766| 		cpu->pc = cpu->cd.mips.coproc[0]->reg[COP0_EPC];
 2767| 		cpu->delay_slot = 0;             
 2768| 		cpu->cd.mips.coproc[0]->reg[COP0_STATUS] &= ~STATUS_EXL;
 2769| 	}
 2770| 
 2771| 	quick_pc_to_pointers(cpu);
 2772| 
 2773| 	cpu->cd.mips.rmw = 0;   /*  the "LL bit"  */
 2774| }
 2775| 
 2776| 
 2777| /*
 2778|  *  deret: Return from debug (EJTAG) handler
 2779|  */
 2780| X(deret)
 2781| {
 2782| 	if (!cop0_availability_check(cpu, ic))
 2783| 		return;
 2784| 
 2785| 	/*
 2786| 	 *  According to the MIPS64 manual, deret loads PC from the DEPC cop0
 2787| 	 *  register, and jumps there immediately. No delay slot.
 2788| 	 *
 2789| 	 *  TODO: This instruction is only available if the processor is in
 2790| 	 *  debug mode. (What does that mean?)
 2791| 	 *
 2792| 	 *  TODO: This instruction is undefined in a delay slot.
 2793| 	 */
 2794| 
 2795| 	cpu->pc = cpu->cd.mips.coproc[0]->reg[COP0_DEPC];
 2796| 	cpu->delay_slot = 0;
 2797| 	cpu->cd.mips.coproc[0]->reg[COP0_STATUS] &= ~STATUS_EXL;
 2798| 	quick_pc_to_pointers(cpu);
 2799| }
 2800| 
 2801| 
 2802| /*
 2803|  *  idle:  Called from the implementation of wait, or netbsd_pmax_idle.
 2804|  */
 2805| X(idle)
 2806| {
 2807| 	/*
 2808| 	 *  If there is an interrupt, then just return. Otherwise
 2809| 	 *  re-run the wait instruction (after a delay).
 2810| 	 */
 2811| 	uint32_t status = cpu->cd.mips.coproc[0]->reg[COP0_STATUS];
 2812| 	uint32_t cause = cpu->cd.mips.coproc[0]->reg[COP0_CAUSE];
 2813| 
 2814| 	if (cpu->cd.mips.cpu_type.exc_model != EXC3K) {
 2815| 		if (status & (STATUS_EXL | STATUS_ERL))
 2816| 			status &= ~STATUS_IE;
 2817| 	}
 2818| 
 2819| 	/*  Ugly R5900 special case:  (TODO: move this?)  */
 2820| 	if (cpu->cd.mips.cpu_type.rev == MIPS_R5900 &&
 2821| 	    !(status & R5900_STATUS_EIE))
 2822| 		status &= ~STATUS_IE;
 2823| 	if (status & STATUS_IE && (status & cause & STATUS_IM_MASK))
 2824| 		return;
 2825| 
 2826| 	// Sync pc:
 2827| 	int low_pc = ((size_t)ic - (size_t)cpu->cd.mips.cur_ic_page)
 2828| 	    / sizeof(struct mips_instr_call);
 2829| 	cpu->pc &= ~((MIPS_IC_ENTRIES_PER_PAGE-1)
 2830| 	    << MIPS_INSTR_ALIGNMENT_SHIFT);
 2831| 	cpu->pc += (low_pc << MIPS_INSTR_ALIGNMENT_SHIFT);
 2832| 
 2833| 	cpu->cd.mips.next_ic = ic;
 2834| 	cpu->is_halted = true;
 2835| 
 2836| 	cpu->wants_to_idle = true;
 2837| 	cpu->n_translated_instrs += N_DYNTRANS_IDLE_BREAK;
 2838| 	cpu->cd.mips.next_ic = &nothing_call;
 2839| }
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

End with one line: `FIXDRAFT_MIPSEIDICU0: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
