# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `mipscountread` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `mipscountread`, state `open`)

**title:** cpus/cpu_mips_coproc.c:coproc_register_read COP0_COUNT -- an MFC0 Count read bumps Count, and a bump that reaches Compare raises IP7 only at the batch end -- WRONG-RESULT (Linux cevt-r4k probe)

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T44 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A3-28).  Source URLs: https://github.com/jroark/GXemul/commit/dc55abccde355926cfbe9f64a5c04867186b2f0b, https://github.com/jroark/GXemul/commit/445d32d1fe895c000ff4a51c589225e31c82054c.  Our site at de8c7547: src/cpus/cpu_mips_coproc.c:590-595; src/cpus/cpu_dyntrans.c:420-441.  Portable fix: yes -- port jroark dc55abc, jroark 445d32d.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**The drafter's own reading:** STILL PRESENT: YES -- `if (cp->coproc_nr==0 && reg_nr==COP0_COUNT) {`

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/cpus/cpu_dyntrans.c b/src/cpus/cpu_dyntrans.c
index 05a941db..5a13ce4c 100644
--- a/src/cpus/cpu_dyntrans.c
+++ b/src/cpus/cpu_dyntrans.c
@@ -418,8 +418,6 @@ int DYNTRANS_RUN_INSTR_DEF(struct cpu *cpu)
 	if (cpu->cd.mips.cpu_type.exc_model != EXC3K) {
 		uint32_t old;
 		int32_t diff1, diff2;
-		cpu->cd.mips.coproc[0]->reg[COP0_COUNT] -= cpu->cd.mips.count_register_read_count;
-		cpu->cd.mips.count_register_read_count = 0;
 		old = cpu->cd.mips.coproc[0]->reg[COP0_COUNT];
 		diff1 = cpu->cd.mips.coproc[0]->reg[COP0_COMPARE] - old;
 		cpu->cd.mips.coproc[0]->reg[COP0_COUNT] =
diff --git a/src/cpus/cpu_mips_coproc.c b/src/cpus/cpu_mips_coproc.c
index f6af6955..f714973e 100644
--- a/src/cpus/cpu_mips_coproc.c
+++ b/src/cpus/cpu_mips_coproc.c
@@ -588,9 +588,6 @@ void coproc_register_read(struct cpu *cpu,
 	if (cp->coproc_nr==0 && reg_nr==COP0_WIRED)	unimpl = 0;
 	if (cp->coproc_nr==0 && reg_nr==COP0_BADVADDR)	unimpl = 0;
 	if (cp->coproc_nr==0 && reg_nr==COP0_COUNT) {
-		/*  TODO: Increase count in a more meaningful way!  */
-		cp->reg[COP0_COUNT] = (int32_t) (cp->reg[COP0_COUNT] + 1);
-		cpu->cd.mips.count_register_read_count ++;
 		unimpl = 0;
 	}
 	if (cp->coproc_nr==0 && reg_nr==COP0_ENTRYHI)	unimpl = 0;
```

## Every edited function, after the fix

### `src/cpus/cpu_dyntrans.c` -- post-edit lines 177-464 (`+` marks a line the diff added or the point of a deletion)

```c
  177|  int DYNTRANS_RUN_INSTR_DEF(struct cpu *cpu)
  178|  {
  179|  	MODE_uint_t cached_pc;
  180|  	int low_pc, n_instrs;
  181|  
     | [... lines 182-310 not shown ...]
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
  421|+ 		old = cpu->cd.mips.coproc[0]->reg[COP0_COUNT];
  422|  		diff1 = cpu->cd.mips.coproc[0]->reg[COP0_COMPARE] - old;
  423|  		cpu->cd.mips.coproc[0]->reg[COP0_COUNT] =
  424|  		    (int32_t) (old + n_instrs);
  425|  		diff2 = cpu->cd.mips.coproc[0]->reg[COP0_COMPARE] -
  426|  		    cpu->cd.mips.coproc[0]->reg[COP0_COUNT];
  427|  
  428|  		if (cpu->cd.mips.compare_register_set) {
  429|  #if 1
  430|  /*  Not yet.  TODO  */
  431|  			if (cpu->machine->emulated_hz > 0) {
  432|  				if (cpu->cd.mips.compare_interrupts_pending > 0)
  433|  					INTERRUPT_ASSERT(
  434|  					    cpu->cd.mips.irq_compare);
  435|  			} else
  436|  #endif
  437|  			{
  438|  				if (diff1 > 0 && diff2 <= 0)
  439|  					INTERRUPT_ASSERT(
  440|  					    cpu->cd.mips.irq_compare);
  441|  			}
  442|  		}
  443|  	}
  444|  #endif
  445|  #ifdef DYNTRANS_PPC
  446|  	/*  Update the Decrementer and Time base registers:  */
  447|  	{
  448|  		uint32_t old = cpu->cd.ppc.spr[SPR_DEC];
  449|  		cpu->cd.ppc.spr[SPR_DEC] = (uint32_t) (old - n_instrs);
  450|  		if ((old >> 31) == 0 && (cpu->cd.ppc.spr[SPR_DEC] >> 31) == 1
  451|  		    && !(cpu->cd.ppc.cpu_type.flags & PPC_NO_DEC))
  452|  			cpu->cd.ppc.dec_intr_pending = 1;
  453|  		old = cpu->cd.ppc.spr[SPR_TBL];
  454|  		cpu->cd.ppc.spr[SPR_TBL] = (uint32_t) (old + n_instrs);
  455|  		if ((old >> 31) == 1 && (cpu->cd.ppc.spr[SPR_TBL] >> 31) == 0)
  456|  			cpu->cd.ppc.spr[SPR_TBU] ++;
  457|  	}
  458|  #endif
  459|  
  460|  	cpu->ninstrs += n_instrs;
  461|  
  462|  	/*  Return the nr of instructions executed:  */
  463|  	return n_instrs;
  464|  }
```

### `src/cpus/cpu_mips_coproc.c` -- post-edit lines 579-645 (`+` marks a line the diff added or the point of a deletion)

```c
  579|  {
  580|  	int unimpl = 1;
  581|  
  582|  	if (cp->coproc_nr==0 && reg_nr==COP0_INDEX)	unimpl = 0;
  583|  	if (cp->coproc_nr==0 && reg_nr==COP0_RANDOM)	unimpl = 0;
  584|  	if (cp->coproc_nr==0 && reg_nr==COP0_ENTRYLO0)	unimpl = 0;
  585|  	if (cp->coproc_nr==0 && reg_nr==COP0_ENTRYLO1)	unimpl = 0;
  586|  	if (cp->coproc_nr==0 && reg_nr==COP0_CONTEXT)	unimpl = 0;
  587|  	if (cp->coproc_nr==0 && reg_nr==COP0_PAGEMASK)	unimpl = 0;
  588|  	if (cp->coproc_nr==0 && reg_nr==COP0_WIRED)	unimpl = 0;
  589|  	if (cp->coproc_nr==0 && reg_nr==COP0_BADVADDR)	unimpl = 0;
  590|  	if (cp->coproc_nr==0 && reg_nr==COP0_COUNT) {
  591|+ 		unimpl = 0;
  592|  	}
  593|  	if (cp->coproc_nr==0 && reg_nr==COP0_ENTRYHI)	unimpl = 0;
  594|  	if (cp->coproc_nr==0 && reg_nr==COP0_COMPARE)	unimpl = 0;
  595|  	if (cp->coproc_nr==0 && reg_nr==COP0_STATUS)	unimpl = 0;
  596|  	if (cp->coproc_nr==0 && reg_nr==COP0_CAUSE)	unimpl = 0;
  597|  	if (cp->coproc_nr==0 && reg_nr==COP0_EPC)	unimpl = 0;
  598|  	if (cp->coproc_nr==0 && reg_nr==COP0_PRID)	unimpl = 0;
  599|  	if (cp->coproc_nr==0 && reg_nr==COP0_CONFIG) {
  600|  		if (select > 0) {
  601|  			switch (select) {
  602|  			case 1:	*ptr = cpu->cd.mips.cop0_config_select1;
  603|  				break;
  604|  			default:fatal("coproc_register_read(): unimplemented"
  605|  				    " config register select %i\n", select);
  606|  				/*  #213: (Codex/Fable) guest-reachable via mfc0 Config2..7;
  607|  				    return a defined 0 instead of exit()ing the host.  */
  608|  				*ptr = 0;
  609|  				break;
  610|  			}
  611|  			return;
  612|  		}
  613|  		unimpl = 0;
  614|  	}
  615|  	if (cp->coproc_nr==0 && reg_nr==COP0_LLADDR)	unimpl = 0;
  616|  	if (cp->coproc_nr==0 && reg_nr==COP0_WATCHLO)	unimpl = 0;
  617|  	if (cp->coproc_nr==0 && reg_nr==COP0_WATCHHI)	unimpl = 0;
  618|  	if (cp->coproc_nr==0 && reg_nr==COP0_XCONTEXT)	unimpl = 0;
  619|  	if (cp->coproc_nr==0 && reg_nr==COP0_ERRCTL)	unimpl = 0;
  620|  	if (cp->coproc_nr==0 && reg_nr==COP0_CACHEERR)	unimpl = 0;
  621|  	if (cp->coproc_nr==0 && reg_nr==COP0_TAGDATA_LO)	unimpl = 0;
  622|  	if (cp->coproc_nr==0 && reg_nr==COP0_TAGDATA_HI)	unimpl = 0;
  623|  	if (cp->coproc_nr==0 && reg_nr==COP0_ERROREPC)	unimpl = 0;
  624|  	if (cp->coproc_nr==0 && reg_nr==COP0_RESERV22) {
  625|  		/*  Used by Linux on Linksys WRT54G  */
  626|  		unimpl = 0;
  627|  	}
  628|  	if (cp->coproc_nr==0 && reg_nr==COP0_DEBUG)	unimpl = 0;
  629|  	if (cp->coproc_nr==0 && reg_nr==COP0_PERFCNT)	unimpl = 0;
  630|  	if (cp->coproc_nr==0 && reg_nr==COP0_DESAVE)	unimpl = 0;
  631|  
  632|  	if (cp->coproc_nr==1)	unimpl = 0;
  633|  
  634|  	if (unimpl) {
  635|  		fatal("cpu%i: warning: read from unimplemented coproc%i"
  636|  		    " register %i (%s)\n", cpu->cpu_id, cp->coproc_nr, reg_nr,
  637|  		    cp->coproc_nr==0? cop0_names[reg_nr] : "?");
  638|  
  639|  		mips_cpu_exception(cpu, EXCEPTION_CPU, 0, 0,
  640|  		    cp->coproc_nr, 0, 0, 0);
  641|  		return;
  642|  	}
  643|  
  644|  	*ptr = cp->reg[reg_nr];
  645|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_MIPSCOUNTREAD: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_MIPSCOUNTREAD: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
