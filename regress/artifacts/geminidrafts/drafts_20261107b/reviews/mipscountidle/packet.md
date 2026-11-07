# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `mipscountidle` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `mipscountidle`, state `open`)

**title:** cpus/cpu_dyntrans.c idle path -- WAIT/STANDBY batches subtract N_DYNTRANS_IDLE_BREAK, so Count does not advance while the guest idles -- WRONG-RESULT

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T46 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A3-31).  Source URLs: https://github.com/jroark/GXemul/commit/45b34df624c82b883d341e818b40b438b4f4af77.  Our site at de8c7547: src/cpus/cpu_dyntrans.c:376-377.  Portable fix: yes -- port jroark 45b34df.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**The drafter's own reading:** STILL PRESENT: YES -- `cpu->n_translated_instrs -= N_DYNTRANS_IDLE_BREAK;` at line 377.

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/cpus/cpu_dyntrans.c b/src/cpus/cpu_dyntrans.c
index 05a941db..1e0ca2b4 100644
--- a/src/cpus/cpu_dyntrans.c
+++ b/src/cpus/cpu_dyntrans.c
@@ -374,7 +374,7 @@ int DYNTRANS_RUN_INSTR_DEF(struct cpu *cpu)
 	}
 
 	if (cpu->wants_to_idle) {
-		cpu->n_translated_instrs -= N_DYNTRANS_IDLE_BREAK;
+		/* #mipscountidle: do not subtract N_DYNTRANS_IDLE_BREAK so time advances */
 
 		// TODO: More arch specific interrupt checks
 		if (false
```

## Every edited function, after the fix

### `src/cpus/cpu_dyntrans.c` -- post-edit lines 177-466 (`+` marks a line the diff added or the point of a deletion)

```c
  177|  int DYNTRANS_RUN_INSTR_DEF(struct cpu *cpu)
  178|  {
  179|  	MODE_uint_t cached_pc;
  180|  	int low_pc, n_instrs;
  181|  
     | [... lines 182-266 not shown ...]
  267|  	cpu->n_translated_instrs = 0;
  268|  
  269|  	cpu->cd.DYNTRANS_ARCH.cur_physpage = (struct DYNTRANS_TC_PHYSPAGE *)
  270|  	    cpu->cd.DYNTRANS_ARCH.cur_ic_page;
  271|  
  272|  	if (single_step || cpu->machine->instruction_trace
  273|  	    || cpu->machine->register_dump) {
  274|  		/*
  275|  		 *  Single-step:
  276|  		 */
  277|  		struct DYNTRANS_IC *ic = cpu->cd.DYNTRANS_ARCH.next_ic;
  278|  		if (cpu->machine->register_dump) {
  279|  			debug("\n");
  280|  			cpu_register_dump(cpu->machine, cpu, 1, 0x1);
  281|  		}
  282|  		if (single_step || cpu->machine->instruction_trace) {
  283|  			/*  TODO/Note: This must be large enough to hold
  284|  			    any instruction for any ISA:  */
  285|  			unsigned char instr[1 <<
  286|  			    DYNTRANS_INSTR_ALIGNMENT_SHIFT];
  287|  			if (!cpu->memory_rw(cpu, cpu->mem, cached_pc, &instr[0],
  288|  			    sizeof(instr), MEM_READ, CACHE_INSTRUCTION)) {
  289|  				fatal("XXX_run_instr(): could not read "
  290|  				    "the instruction\n");
  291|  			} else {
  292|  #ifdef DYNTRANS_DELAYSLOT
  293|  				int len =
  294|  #endif
  295|  				    cpu_disassemble_instr(
  296|  				    cpu->machine, cpu, instr, 1, cpu->pc);
  297|  #ifdef DYNTRANS_DELAYSLOT
  298|  				/*  Show the instruction in the delay slot,
  299|  				    if any:  */
  300|  				if (cpu->instruction_has_delayslot == NULL)
  301|  					fatal("WARNING: ihd func not yet"
  302|  					    " implemented?\n");
  303|  				else if (cpu->instruction_has_delayslot(cpu,
  304|  				    instr)) {
  305|  					int saved_delayslot = cpu->delay_slot;
  306|  					cpu->memory_rw(cpu, cpu->mem, cached_pc
  307|  					    + len, &instr[0],
  308|  					    sizeof(instr), MEM_READ,
  309|  					    CACHE_INSTRUCTION);
  310|  					cpu->delay_slot = DELAYED;
  311|  					cpu->pc += len;
  312|  					cpu_disassemble_instr(cpu->machine,
  313|  					    cpu, instr, 1, cpu->pc);
  314|  					cpu->delay_slot = saved_delayslot;
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
  377|+ 		/* #mipscountidle: do not subtract N_DYNTRANS_IDLE_BREAK so time advances */
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
  425|  		cpu->cd.mips.coproc[0]->reg[COP0_COUNT] =
  426|  		    (int32_t) (old + n_instrs);
  427|  		diff2 = cpu->cd.mips.coproc[0]->reg[COP0_COMPARE] -
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

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_MIPSCOUNTIDLE: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_MIPSCOUNTIDLE: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
