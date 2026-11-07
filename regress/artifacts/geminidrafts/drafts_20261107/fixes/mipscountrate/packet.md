# GXemul hardened fork -- DRAFT A FIX for one filed issue, `mipscountrate` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD d2a6f233).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `mipscountrate`, state `open`, severity `MED`)

**title:** cpus/cpu_dyntrans.c Count update -- Count advances once per instruction instead of once per two cycles, with no per-machine divisor -- WRONG-RESULT (timebase ratio)

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T45 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: medium; report rows: A3-29, A3-30).  Source URLs: https://github.com/jroark/GXemul/commit/dabf5ce42e300c0f0c46c3a032b1ae414a54bf48, https://github.com/jroark/GXemul/commit/b0411219afea8ffef07405b6cb817e5e6bfb750e.  Our site at de8c7547: src/cpus/cpu_dyntrans.c:425-426.  Portable fix: yes -- port jroark dabf5ce, jroark b041121 (BE-300 rate is jroark's value).  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- port jroark dabf5ce and b041121

## The code at the cited lines

### `src/cpus/cpu_dyntrans.c` around the row's cited line 425 (HEAD d2a6f233, lines 380-470)

```c
  380| 		if (false
  381| #ifdef DYNTRANS_M88K
  382| 		    || (cpu->cd.m88k.irq_asserted && !(cpu->cd.m88k.cr[M88K_CR_PSR] & M88K_PSR_IND))
  383| #endif
  384| 		    ) {
  385| 			debugmsg_cpu(cpu, SUBSYS_CPU, "idle", VERBOSITY_DEBUG, "not idling; exception");
  386| 			cpu->wants_to_idle = false;
  387| 		}
  388| 
  389| 		cpu->has_been_idling = true;
  390| 	}
  391| 
  392| 	n_instrs += cpu->n_translated_instrs;
  393| 
  394| 	/*  Synchronize the program counter:  */
  395| 	low_pc = ((size_t)cpu->cd.DYNTRANS_ARCH.next_ic - (size_t)
  396| 	    cpu->cd.DYNTRANS_ARCH.cur_ic_page) / sizeof(struct DYNTRANS_IC);
  397| 	if (low_pc >= 0 && low_pc < DYNTRANS_IC_ENTRIES_PER_PAGE) {
  398| 		cpu->pc &= ~((DYNTRANS_IC_ENTRIES_PER_PAGE-1) <<
  399| 		    DYNTRANS_INSTR_ALIGNMENT_SHIFT);
  400| 		cpu->pc += (low_pc << DYNTRANS_INSTR_ALIGNMENT_SHIFT);
  401| 	} else if (low_pc == DYNTRANS_IC_ENTRIES_PER_PAGE) {
  402| 		/*  Switch to next page:  */
  403| 		cpu->pc &= ~((DYNTRANS_IC_ENTRIES_PER_PAGE-1) <<
  404| 		    DYNTRANS_INSTR_ALIGNMENT_SHIFT);
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

End with one line: `FIXDRAFT_MIPSCOUNTRATE: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
