# GXemul hardened fork -- DRAFT A FIX for one filed issue, `mipscountidle` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD d2a6f233).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `mipscountidle`, state `open`, severity `MED`)

**title:** cpus/cpu_dyntrans.c idle path -- WAIT/STANDBY batches subtract N_DYNTRANS_IDLE_BREAK, so Count does not advance while the guest idles -- WRONG-RESULT

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T46 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A3-31).  Source URLs: https://github.com/jroark/GXemul/commit/45b34df624c82b883d341e818b40b438b4f4af77.  Our site at de8c7547: src/cpus/cpu_dyntrans.c:376-377.  Portable fix: yes -- port jroark 45b34df.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- port jroark 45b34df

## The code at the cited lines

### `src/cpus/cpu_dyntrans.c` around the row's cited line 376 (HEAD d2a6f233, lines 331-421)

```c
  331| 		for (;;) {
  332| 			struct DYNTRANS_IC *ic;
  333| 
  334| 			S; I; S; I; S; I; S; I; S; I; S; I;
  335| 			S; I; S; I; S; I; S; I; S; I; S; I;
  336| 			S; I; S; I; S; I; S; I; S; I; S; I;
  337| 			S; I; S; I; S; I; S; I; S; I; S; I;
  338| 
  339| 			cpu->n_translated_instrs += 24;
  340| 			if (cpu->n_translated_instrs >= N_SAFE_DYNTRANS_LIMIT)
  341| 				break;
  342| 		}
  343| 	} else {
  344| 		/*
  345| 		 *  Execute multiple instructions:
  346| 		 *
  347| 		 *  (This is the core dyntrans loop.)
  348| 		 */
  349| 		n_instrs = 0;
  350| 
  351| 		for (;;) {
  352| 			struct DYNTRANS_IC *ic;
  353| 
  354| 			I; I; I; I; I;   I; I; I; I; I;
  355| 			I; I; I; I; I;   I; I; I; I; I;
  356| 			I; I; I; I; I;   I; I; I; I; I;
  357| 			I; I; I; I; I;   I; I; I; I; I;
  358| 			I; I; I; I; I;   I; I; I; I; I;
  359| 
  360| 			I; I; I; I; I;   I; I; I; I; I;
  361| 
  362| 			I; I; I; I; I;   I; I; I; I; I;
  363| 			I; I; I; I; I;   I; I; I; I; I;
  364| 			I; I; I; I; I;   I; I; I; I; I;
  365| 			I; I; I; I; I;   I; I; I; I; I;
  366| 			I; I; I; I; I;   I; I; I; I; I;
  367| 
  368| 			I; I; I; I; I;   I; I; I; I; I;
  369| 
  370| 			cpu->n_translated_instrs += 120;
  371| 			if (cpu->n_translated_instrs >= N_SAFE_DYNTRANS_LIMIT)
  372| 				break;
  373| 		}
  374| 	}
  375| 
  376| 	if (cpu->wants_to_idle) {
  377| 		cpu->n_translated_instrs -= N_DYNTRANS_IDLE_BREAK;
  378| 
  379| 		// TODO: More arch specific interrupt checks
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

End with one line: `FIXDRAFT_MIPSCOUNTIDLE: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
