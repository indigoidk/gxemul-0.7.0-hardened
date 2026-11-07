# GXemul hardened fork -- DRAFT A FIX for one filed issue, `ppcdecwrite` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD d2a6f233).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `ppcdecwrite`, state `open`, severity `MED`)

**title:** cpus/cpu_ppc_instr.c:X(mtspr) DEC -- a software DEC write that flips bit 0 from 0 to 1 does not signal the decrementer exception -- WRONG-RESULT

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T42 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A4-24).  Source URLs: https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/241f5e273caf75599ebb8ebc554e1e9faaacf508.  Our site at de8c7547: src/cpus/cpu_ppc_instr.c:2807-2810; src/cpus/cpu_dyntrans.c:450-454.  Portable fix: yes -- port rs6000 241f5e2.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- Port available from rs6000 241f5e2

## The code at the cited lines

### `src/cpus/cpu_ppc_instr.c` around the row's cited line 2807 (HEAD d2a6f233, lines 2762-2852)

```c
 2762| 	if (ba | !bb)	/*  #575: CR[BA] | ~CR[BB] (Book I); this was NOR  */
 2763| 		cpu->cd.ppc.cr |= (1 << (31-bt));
 2764| }
 2765| X(crnor) {
 2766| 	uint32_t iword = ic->arg[0]; int bt = (iword >> 21) & 31;
 2767| 	int ba = (iword >> 16) & 31, bb = (iword >> 11) & 31;
 2768| 	ba = (cpu->cd.ppc.cr >> (31-ba)) & 1;
 2769| 	bb = (cpu->cd.ppc.cr >> (31-bb)) & 1;
 2770| 	cpu->cd.ppc.cr &= ~(1 << (31-bt));
 2771| 	if (!(ba | bb))
 2772| 		cpu->cd.ppc.cr |= (1 << (31-bt));
 2773| }
 2774| X(crxor) {
 2775| 	uint32_t iword = ic->arg[0]; int bt = (iword >> 21) & 31;
 2776| 	int ba = (iword >> 16) & 31, bb = (iword >> 11) & 31;
 2777| 	ba = (cpu->cd.ppc.cr >> (31-ba)) & 1;
 2778| 	bb = (cpu->cd.ppc.cr >> (31-bb)) & 1;
 2779| 	cpu->cd.ppc.cr &= ~(1 << (31-bt));
 2780| 	if (ba ^ bb)
 2781| 		cpu->cd.ppc.cr |= (1 << (31-bt));
 2782| }
 2783| 
 2784| 
 2785| /*
 2786|  *  mfspr: Move from SPR
 2787|  *
 2788|  *  arg[0] = pointer to destination register
 2789|  *  arg[1] = pointer to source SPR
 2790|  */
 2791| X(mfspr) {
 2792| 	/*  TODO: Check permission  */
 2793| 	reg(ic->arg[0]) = reg(ic->arg[1]);
 2794| }
 2795| X(mfspr_pmc1) {
 2796| 	/*
 2797| 	 *  TODO: This is a temporary hack to make NetBSD/ppc detect
 2798| 	 *  a CPU of the correct (emulated) speed.
 2799| 	 */
 2800| 	reg(ic->arg[0]) = cpu->machine->emulated_hz / 10;
 2801| }
 2802| X(mftb) {
 2803| 	/*  NOTE/TODO: This increments the time base (slowly) if it
 2804| 	    is being polled.  */
 2805| 	if (++cpu->cd.ppc.spr[SPR_TBL] == 0)
 2806| 		cpu->cd.ppc.spr[SPR_TBU] ++;
 2807| 	reg(ic->arg[0]) = cpu->cd.ppc.spr[SPR_TBL];
 2808| }
 2809| X(mftbu) {
 2810| 	reg(ic->arg[0]) = cpu->cd.ppc.spr[SPR_TBU];
 2811| }
 2812| 
 2813| 
 2814| /*
 2815|  *  mtspr: Move to SPR.
 2816|  *
 2817|  *  arg[0] = pointer to source register
 2818|  *  arg[1] = pointer to the SPR
 2819|  */
 2820| X(mtspr) {
 2821| 	/*  TODO: Check permission  */
 2822| 	reg(ic->arg[1]) = reg(ic->arg[0]);
 2823| }
 2824| X(mtspr_sprg2) {
 2825| 	if (cpu->cd.ppc.bits == 32) {
 2826| 		// Ignore for now. FreeBSD/powerpc seems to write 0xffffffe0
 2827| 		// here, and read it back. If it is non-zero, it assumes a 64-bit
 2828| 		// cpu.
 2829| 	} else {
 2830| 		reg(ic->arg[1]) = reg(ic->arg[0]);
 2831| 	}
 2832| }
 2833| X(mtlr) {
 2834| 	cpu->cd.ppc.spr[SPR_LR] = reg(ic->arg[0]);
 2835| }
 2836| X(mtctr) {
 2837| 	cpu->cd.ppc.spr[SPR_CTR] = reg(ic->arg[0]);
 2838| }
 2839| 
 2840| 
 2841| /*
 2842|  *  rfi[d]:  Return from Interrupt
 2843|  */
 2844| X(rfi)
 2845| {
 2846| 	uint64_t tmp;
 2847| 
 2848| 	reg_access_msr(cpu, &tmp, 0, 0);
 2849| 	tmp &= ~0xffff;
 2850| 	tmp |= (cpu->cd.ppc.spr[SPR_SRR1] & 0xffff);
 2851| 	reg_access_msr(cpu, &tmp, 1, 0);
 2852| 
```

### `src/cpus/cpu_dyntrans.c` around the row's cited line 450 (HEAD d2a6f233, lines 405-495)

```c
  405| 		cpu->pc += (DYNTRANS_IC_ENTRIES_PER_PAGE <<
  406| 		    DYNTRANS_INSTR_ALIGNMENT_SHIFT);
  407| 	} else if (low_pc == DYNTRANS_IC_ENTRIES_PER_PAGE + 1) {
  408| 		/*  Switch to next page and skip an instruction which was
  409| 		    already executed (in a delay slot):  */
  410| 		cpu->pc &= ~((DYNTRANS_IC_ENTRIES_PER_PAGE-1) <<
  411| 		    DYNTRANS_INSTR_ALIGNMENT_SHIFT);
  412| 		cpu->pc += ((DYNTRANS_IC_ENTRIES_PER_PAGE + 1) <<
  413| 		    DYNTRANS_INSTR_ALIGNMENT_SHIFT);
  414| 	}
  415| 
  416| #ifdef DYNTRANS_MIPS
  417| 	/*  Update the count register (on everything except EXC3K):  */
  418| 	if (cpu->cd.mips.cpu_type.exc_model != EXC3K) {
  419| 		uint32_t old;
  420| 		int32_t diff1, diff2;
  421| 		cpu->cd.mips.coproc[0]->reg[COP0_COUNT] -= cpu->cd.mips.count_register_read_count;
  422| 		cpu->cd.mips.count_register_read_count = 0;
  423| 		old = cpu->cd.mips.coproc[0]->reg[COP0_COUNT];
  424| 		diff1 = cpu->cd.mips.coproc[0]->reg[COP0_COMPARE] - old;
  425| 		cpu->cd.mips.coproc[0]->reg[COP0_COUNT] =
  426| 		    (int32_t) (old + n_instrs);
  427| 		diff2 = cpu->cd.mips.coproc[0]->reg[COP0_COMPARE] -
  428| 		    cpu->cd.mips.coproc[0]->reg[COP0_COUNT];
  429| 
  430| 		if (cpu->cd.mips.compare_register_set) {
  431| #if 1
  432| /*  Not yet.  TODO  */
  433| 			if (cpu->machine->emulated_hz > 0) {
  434| 				if (cpu->cd.mips.compare_interrupts_pending > 0)
  435| 					INTERRUPT_ASSERT(
  436| 					    cpu->cd.mips.irq_compare);
  437| 			} else
  438| #endif
  439| 			{
  440| 				if (diff1 > 0 && diff2 <= 0)
  441| 					INTERRUPT_ASSERT(
  442| 					    cpu->cd.mips.irq_compare);
  443| 			}
  444| 		}
  445| 	}
  446| #endif
  447| #ifdef DYNTRANS_PPC
  448| 	/*  Update the Decrementer and Time base registers:  */
  449| 	{
  450| 		uint32_t old = cpu->cd.ppc.spr[SPR_DEC];
  451| 		cpu->cd.ppc.spr[SPR_DEC] = (uint32_t) (old - n_instrs);
  452| 		if ((old >> 31) == 0 && (cpu->cd.ppc.spr[SPR_DEC] >> 31) == 1
  453| 		    && !(cpu->cd.ppc.cpu_type.flags & PPC_NO_DEC))
  454| 			cpu->cd.ppc.dec_intr_pending = 1;
  455| 		old = cpu->cd.ppc.spr[SPR_TBL];
  456| 		cpu->cd.ppc.spr[SPR_TBL] = (uint32_t) (old + n_instrs);
  457| 		if ((old >> 31) == 1 && (cpu->cd.ppc.spr[SPR_TBL] >> 31) == 0)
  458| 			cpu->cd.ppc.spr[SPR_TBU] ++;
  459| 	}
  460| #endif
  461| 
  462| 	cpu->ninstrs += n_instrs;
  463| 
  464| 	/*  Return the nr of instructions executed:  */
  465| 	return n_instrs;
  466| }
  467| #endif	/*  DYNTRANS_RUN_INSTR  */
  468| 
  469| 
  470| 
  471| #ifdef DYNTRANS_FUNCTION_TRACE_DEF
  472| /*
  473|  *  XXX_cpu_functioncall_trace():
  474|  *
  475|  *  Without this function, the main trace tree function prints something
  476|  *  like    <f()>  or  <0x1234()>   on a function call. It is up to this
  477|  *  function to print the arguments passed.
  478|  */
  479| void DYNTRANS_FUNCTION_TRACE_DEF(struct cpu *cpu, int n_args)
  480| {
  481| 	int show_symbolic_function_name = 1;
  482|         char strbuf[55];
  483| 	char *symbol;
  484| 	uint64_t ot;
  485| 	int x, print_dots = 1, n_args_to_print =
  486| #if defined(DYNTRANS_ALPHA)
  487| 	    6
  488| #else
  489| #if defined(DYNTRANS_SH) || defined(DYNTRANS_M88K) || defined(DYNTRANS_RISCV) || defined(DYNTRANS_I960)
  490| 	    8	/*  For 32-bit and 64-bit SuperH, M88K, i960, and RISC-V  */
  491| #else
  492| 	    4	/*  Default value for most archs  */
  493| #endif
  494| #endif
  495| 	    ;
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

End with one line: `FIXDRAFT_PPCDECWRITE: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
