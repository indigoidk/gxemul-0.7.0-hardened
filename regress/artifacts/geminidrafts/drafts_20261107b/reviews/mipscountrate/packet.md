# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `mipscountrate` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `mipscountrate`, state `open`)

**title:** cpus/cpu_dyntrans.c Count update -- Count advances once per instruction instead of once per two cycles, with no per-machine divisor -- WRONG-RESULT (timebase ratio)

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T45 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: medium; report rows: A3-29, A3-30).  Source URLs: https://github.com/jroark/GXemul/commit/dabf5ce42e300c0f0c46c3a032b1ae414a54bf48, https://github.com/jroark/GXemul/commit/b0411219afea8ffef07405b6cb817e5e6bfb750e.  Our site at de8c7547: src/cpus/cpu_dyntrans.c:425-426.  Portable fix: yes -- port jroark dabf5ce, jroark b041121 (BE-300 rate is jroark's value).  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**The drafter's own reading:** STILL PRESENT: YES -- src/cpus/cpu_dyntrans.c:425

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/cpus/cpu_dyntrans.c b/src/cpus/cpu_dyntrans.c
index 05a941db..2e77836e 100644
--- a/src/cpus/cpu_dyntrans.c
+++ b/src/cpus/cpu_dyntrans.c
@@ -422,8 +422,9 @@ int DYNTRANS_RUN_INSTR_DEF(struct cpu *cpu)
 		cpu->cd.mips.count_register_read_count = 0;
 		old = cpu->cd.mips.coproc[0]->reg[COP0_COUNT];
 		diff1 = cpu->cd.mips.coproc[0]->reg[COP0_COMPARE] - old;
+		/* #NNN: Count advances once per two cycles */
 		cpu->cd.mips.coproc[0]->reg[COP0_COUNT] =
-		    (int32_t) (old + n_instrs);
+		    (int32_t) (old + (cpu->ninstrs + n_instrs) / 2 - cpu->ninstrs / 2);
 		diff2 = cpu->cd.mips.coproc[0]->reg[COP0_COMPARE] -
 		    cpu->cd.mips.coproc[0]->reg[COP0_COUNT];
```

## Every edited function, after the fix

### `src/cpus/cpu_dyntrans.c` -- post-edit lines 177-467 (`+` marks a line the diff added or the point of a deletion)

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
  425|+ 		/* #NNN: Count advances once per two cycles */
  426|  		cpu->cd.mips.coproc[0]->reg[COP0_COUNT] =
  427|+ 		    (int32_t) (old + (cpu->ninstrs + n_instrs) / 2 - cpu->ninstrs / 2);
  428|  		diff2 = cpu->cd.mips.coproc[0]->reg[COP0_COMPARE] -
  429|  		    cpu->cd.mips.coproc[0]->reg[COP0_COUNT];
  430|  
  431|  		if (cpu->cd.mips.compare_register_set) {
  432|  #if 1
  433|  /*  Not yet.  TODO  */
  434|  			if (cpu->machine->emulated_hz > 0) {
  435|  				if (cpu->cd.mips.compare_interrupts_pending > 0)
  436|  					INTERRUPT_ASSERT(
  437|  					    cpu->cd.mips.irq_compare);
  438|  			} else
  439|  #endif
  440|  			{
  441|  				if (diff1 > 0 && diff2 <= 0)
  442|  					INTERRUPT_ASSERT(
  443|  					    cpu->cd.mips.irq_compare);
  444|  			}
  445|  		}
  446|  	}
  447|  #endif
  448|  #ifdef DYNTRANS_PPC
  449|  	/*  Update the Decrementer and Time base registers:  */
  450|  	{
  451|  		uint32_t old = cpu->cd.ppc.spr[SPR_DEC];
  452|  		cpu->cd.ppc.spr[SPR_DEC] = (uint32_t) (old - n_instrs);
  453|  		if ((old >> 31) == 0 && (cpu->cd.ppc.spr[SPR_DEC] >> 31) == 1
  454|  		    && !(cpu->cd.ppc.cpu_type.flags & PPC_NO_DEC))
  455|  			cpu->cd.ppc.dec_intr_pending = 1;
  456|  		old = cpu->cd.ppc.spr[SPR_TBL];
  457|  		cpu->cd.ppc.spr[SPR_TBL] = (uint32_t) (old + n_instrs);
  458|  		if ((old >> 31) == 1 && (cpu->cd.ppc.spr[SPR_TBL] >> 31) == 0)
  459|  			cpu->cd.ppc.spr[SPR_TBU] ++;
  460|  	}
  461|  #endif
  462|  
  463|  	cpu->ninstrs += n_instrs;
  464|  
  465|  	/*  Return the nr of instructions executed:  */
  466|  	return n_instrs;
  467|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_MIPSCOUNTRATE: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_MIPSCOUNTRATE: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
