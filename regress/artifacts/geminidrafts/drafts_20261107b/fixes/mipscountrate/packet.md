# GXemul hardened fork -- REVISE ONE FIX DRAFT after a review, `mipscountrate` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork
removes crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  You drafted a fix for the
issue below; it compiles at HEAD 8d9df658.  A separate review then reported problems with it.  You cannot read files; work
from this text.  This is a DRAFTING task: FIX ONLY, as exact edits -- no tests, probes or reproduction steps.

## The issue (ledger row `mipscountrate`, state `open`)

**title:** cpus/cpu_dyntrans.c Count update -- Count advances once per instruction instead of once per two cycles, with no per-machine divisor -- WRONG-RESULT (timebase ratio)

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T45 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: medium; report rows: A3-29, A3-30).  Source URLs: https://github.com/jroark/GXemul/commit/dabf5ce42e300c0f0c46c3a032b1ae414a54bf48, https://github.com/jroark/GXemul/commit/b0411219afea8ffef07405b6cb817e5e6bfb750e.  Our site at de8c7547: src/cpus/cpu_dyntrans.c:425-426.  Portable fix: yes -- port jroark dabf5ce, jroark b041121 (BE-300 rate is jroark's value).  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

## Every function your previous draft changed, as it reads AT HEAD (your new edits apply to THIS text)

### `src/cpus/cpu_dyntrans.c` -- AT HEAD, lines 177-466 (`*` marks a line your previous draft changed)

```c
  177|  int DYNTRANS_RUN_INSTR_DEF(struct cpu *cpu)
  178|  {
  179|  	MODE_uint_t cached_pc;
  180|  	int low_pc, n_instrs;
  181|  
     | [... lines 182-314 not shown ...]
  315|  					cpu->pc -= len;
  316|  				}
  317|  #endif
  318|  			}
  319|  		}
  320|  
  321|  		if (cpu->machine->statistics.enabled)
  322|  			S;
  323|  
  324|  		/*  Execute just one instruction:  */
  325|  		I;
  326|  
  327|  		n_instrs = 1;
  328|  	} else if (cpu->machine->statistics.enabled) {
  329|  		/*  Gather statistics while executing multiple instructions:  */
  330|  		n_instrs = 0;
  331|  		for (;;) {
  332|  			struct DYNTRANS_IC *ic;
  333|  
  334|  			S; I; S; I; S; I; S; I; S; I; S; I;
  335|  			S; I; S; I; S; I; S; I; S; I; S; I;
  336|  			S; I; S; I; S; I; S; I; S; I; S; I;
  337|  			S; I; S; I; S; I; S; I; S; I; S; I;
  338|  
  339|  			cpu->n_translated_instrs += 24;
  340|  			if (cpu->n_translated_instrs >= N_SAFE_DYNTRANS_LIMIT)
  341|  				break;
  342|  		}
  343|  	} else {
  344|  		/*
  345|  		 *  Execute multiple instructions:
  346|  		 *
  347|  		 *  (This is the core dyntrans loop.)
  348|  		 */
  349|  		n_instrs = 0;
  350|  
  351|  		for (;;) {
  352|  			struct DYNTRANS_IC *ic;
  353|  
  354|  			I; I; I; I; I;   I; I; I; I; I;
  355|  			I; I; I; I; I;   I; I; I; I; I;
  356|  			I; I; I; I; I;   I; I; I; I; I;
  357|  			I; I; I; I; I;   I; I; I; I; I;
  358|  			I; I; I; I; I;   I; I; I; I; I;
  359|  
  360|  			I; I; I; I; I;   I; I; I; I; I;
  361|  
  362|  			I; I; I; I; I;   I; I; I; I; I;
  363|  			I; I; I; I; I;   I; I; I; I; I;
  364|  			I; I; I; I; I;   I; I; I; I; I;
  365|  			I; I; I; I; I;   I; I; I; I; I;
  366|  			I; I; I; I; I;   I; I; I; I; I;
  367|  
  368|  			I; I; I; I; I;   I; I; I; I; I;
  369|  
  370|  			cpu->n_translated_instrs += 120;
  371|  			if (cpu->n_translated_instrs >= N_SAFE_DYNTRANS_LIMIT)
  372|  				break;
  373|  		}
  374|  	}
  375|  
  376|  	if (cpu->wants_to_idle) {
  377|  		cpu->n_translated_instrs -= N_DYNTRANS_IDLE_BREAK;
  378|  
  379|  		// TODO: More arch specific interrupt checks
  380|  		if (false
  381|  #ifdef DYNTRANS_M88K
  382|  		    || (cpu->cd.m88k.irq_asserted && !(cpu->cd.m88k.cr[M88K_CR_PSR] & M88K_PSR_IND))
  383|  #endif
  384|  		    ) {
  385|  			debugmsg_cpu(cpu, SUBSYS_CPU, "idle", VERBOSITY_DEBUG, "not idling; exception");
  386|  			cpu->wants_to_idle = false;
  387|  		}
  388|  
  389|  		cpu->has_been_idling = true;
  390|  	}
  391|  
  392|  	n_instrs += cpu->n_translated_instrs;
  393|  
  394|  	/*  Synchronize the program counter:  */
  395|  	low_pc = ((size_t)cpu->cd.DYNTRANS_ARCH.next_ic - (size_t)
  396|  	    cpu->cd.DYNTRANS_ARCH.cur_ic_page) / sizeof(struct DYNTRANS_IC);
  397|  	if (low_pc >= 0 && low_pc < DYNTRANS_IC_ENTRIES_PER_PAGE) {
  398|  		cpu->pc &= ~((DYNTRANS_IC_ENTRIES_PER_PAGE-1) <<
  399|  		    DYNTRANS_INSTR_ALIGNMENT_SHIFT);
  400|  		cpu->pc += (low_pc << DYNTRANS_INSTR_ALIGNMENT_SHIFT);
  401|  	} else if (low_pc == DYNTRANS_IC_ENTRIES_PER_PAGE) {
  402|  		/*  Switch to next page:  */
  403|  		cpu->pc &= ~((DYNTRANS_IC_ENTRIES_PER_PAGE-1) <<
  404|  		    DYNTRANS_INSTR_ALIGNMENT_SHIFT);
  405|  		cpu->pc += (DYNTRANS_IC_ENTRIES_PER_PAGE <<
  406|  		    DYNTRANS_INSTR_ALIGNMENT_SHIFT);
  407|  	} else if (low_pc == DYNTRANS_IC_ENTRIES_PER_PAGE + 1) {
  408|  		/*  Switch to next page and skip an instruction which was
  409|  		    already executed (in a delay slot):  */
  410|  		cpu->pc &= ~((DYNTRANS_IC_ENTRIES_PER_PAGE-1) <<
  411|  		    DYNTRANS_INSTR_ALIGNMENT_SHIFT);
  412|  		cpu->pc += ((DYNTRANS_IC_ENTRIES_PER_PAGE + 1) <<
  413|  		    DYNTRANS_INSTR_ALIGNMENT_SHIFT);
  414|  	}
  415|  
  416|  #ifdef DYNTRANS_MIPS
  417|  	/*  Update the count register (on everything except EXC3K):  */
  418|  	if (cpu->cd.mips.cpu_type.exc_model != EXC3K) {
  419|  		uint32_t old;
  420|  		int32_t diff1, diff2;
  421|  		cpu->cd.mips.coproc[0]->reg[COP0_COUNT] -= cpu->cd.mips.count_register_read_count;
  422|  		cpu->cd.mips.count_register_read_count = 0;
  423|  		old = cpu->cd.mips.coproc[0]->reg[COP0_COUNT];
  424|  		diff1 = cpu->cd.mips.coproc[0]->reg[COP0_COMPARE] - old;
  425|* 		cpu->cd.mips.coproc[0]->reg[COP0_COUNT] =
  426|* 		    (int32_t) (old + n_instrs);
  427|* 		diff2 = cpu->cd.mips.coproc[0]->reg[COP0_COMPARE] -
  428|  		    cpu->cd.mips.coproc[0]->reg[COP0_COUNT];
  429|  
  430|  		if (cpu->cd.mips.compare_register_set) {
  431|  #if 1
  432|  /*  Not yet.  TODO  */
  433|  			if (cpu->machine->emulated_hz > 0) {
  434|  				if (cpu->cd.mips.compare_interrupts_pending > 0)
  435|  					INTERRUPT_ASSERT(
  436|  					    cpu->cd.mips.irq_compare);
  437|  			} else
  438|  #endif
  439|  			{
  440|  				if (diff1 > 0 && diff2 <= 0)
  441|  					INTERRUPT_ASSERT(
  442|  					    cpu->cd.mips.irq_compare);
  443|  			}
  444|  		}
  445|  	}
  446|  #endif
  447|  #ifdef DYNTRANS_PPC
  448|  	/*  Update the Decrementer and Time base registers:  */
  449|  	{
  450|  		uint32_t old = cpu->cd.ppc.spr[SPR_DEC];
  451|  		cpu->cd.ppc.spr[SPR_DEC] = (uint32_t) (old - n_instrs);
  452|  		if ((old >> 31) == 0 && (cpu->cd.ppc.spr[SPR_DEC] >> 31) == 1
  453|  		    && !(cpu->cd.ppc.cpu_type.flags & PPC_NO_DEC))
  454|  			cpu->cd.ppc.dec_intr_pending = 1;
  455|  		old = cpu->cd.ppc.spr[SPR_TBL];
  456|  		cpu->cd.ppc.spr[SPR_TBL] = (uint32_t) (old + n_instrs);
  457|  		if ((old >> 31) == 1 && (cpu->cd.ppc.spr[SPR_TBL] >> 31) == 0)
  458|  			cpu->cd.ppc.spr[SPR_TBU] ++;
  459|  	}
  460|  #endif
  461|  
  462|  	cpu->ninstrs += n_instrs;
  463|  
  464|  	/*  Return the nr of instructions executed:  */
  465|  	return n_instrs;
  466|  }
```



## Your previous draft's edits

```json
[
  {
    "file": "src/cpus/cpu_dyntrans.c",
    "old": "\t\tcpu->cd.mips.coproc[0]->reg[COP0_COUNT] =\n\t\t    (int32_t) (old + n_instrs);",
    "new": "\t\t/* #NNN: Count advances once per two cycles */\n\t\tcpu->cd.mips.coproc[0]->reg[COP0_COUNT] =\n\t\t    (int32_t) (old + (n_instrs / 2));",
    "why": "Advances count once per two cycles instead of once per instruction."
  }
]
```

## The review of that draft (it can be WRONG -- judge each point against the code above)

```text
FIXREVIEW_MIPSCOUNTRATE: DEFECT, 1 FINDINGS
1. The diff targets the correct site named in the issue, but it introduces a severe flaw: because `n_instrs` is an integer, dividing it by 2 evaluates to 0 whenever `n_instrs == 1` (such as in the single-stepping block at lines 324-327). This permanently stalls the Count register during single-instruction execution.
2. CONTROL FLOW: No control flow keywords (return, goto, break) are added. The common tail is always reached and executed.
3. RETURN VALUE: The return value of the function is unaffected, as the local variable `n_instrs` is not modified by the change (it still accurately returns the number of instructions executed).
4. What ELSE does the diff change: Nothing. Only the value assigned to `COP0_COUNT` is affected.
5. House idioms: The new comment correctly utilizes the required `/* #NNN: ... */` tag format and lines remain within 79 columns.
src/cpus/cpu_dyntrans.c:427: DEFECT: Integer division by 2 truncates odd increments (especially 1), stalling the counter. Fix: Track fractional cycle progress in the `cpu` struct across calls, rather than dividing the local variable.
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

End with two lines: `REVISION_MIPSCOUNTRATE: <a> ACCEPTED, <r> REJECTED` and `FIXDRAFT_MIPSCOUNTRATE: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
