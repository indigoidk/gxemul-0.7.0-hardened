# GXemul hardened fork -- DRAFT A FIX for one filed issue, `mipscountread` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD d2a6f233).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `mipscountread`, state `open`, severity `MED`)

**title:** cpus/cpu_mips_coproc.c:coproc_register_read COP0_COUNT -- an MFC0 Count read bumps Count, and a bump that reaches Compare raises IP7 only at the batch end -- WRONG-RESULT (Linux cevt-r4k probe)

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T44 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A3-28).  Source URLs: https://github.com/jroark/GXemul/commit/dc55abccde355926cfbe9f64a5c04867186b2f0b, https://github.com/jroark/GXemul/commit/445d32d1fe895c000ff4a51c589225e31c82054c.  Our site at de8c7547: src/cpus/cpu_mips_coproc.c:590-595; src/cpus/cpu_dyntrans.c:420-441.  Portable fix: yes -- port jroark dc55abc, jroark 445d32d.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- port jroark dc55abc and 445d32d

## The code at the cited lines

### `src/cpus/cpu_mips_coproc.c` around the row's cited line 590 (HEAD d2a6f233, lines 545-635)

```c
  545| 			} else if (cpu->is_32bit) {
  546| 				/*  MIPS32 etc.:  */
  547| 				oldvaddr = cp->tlbs[i].hi & ENTRYHI_VPN2_MASK;
  548| 				oldvaddr = (int32_t)oldvaddr;
  549| 			} else {
  550| 				/*  Assume MMU4K  */
  551| 				oldvaddr = cp->tlbs[i].hi &
  552| 				    (ENTRYHI_R_MASK | ENTRYHI_VPN2_MASK);
  553| 			}
  554| 
  555| 			mask |= 0x1fff;
  556| 			oldvaddr &= ~mask;
  557| 
  558| 			// printf("pagesize = %016llx mask = %016llx\n", pagesize, mask);
  559| 			
  560| 			if (cp->tlbs[i].lo0 & ENTRYLO_V)
  561| 				for (uint64_t ofs = 0; ofs < pagesize; ofs += 0x1000)
  562| 					cpu->invalidate_translation_caches(cpu, oldvaddr + ofs, INVALIDATE_VADDR);
  563| 			
  564| 			if (cp->tlbs[i].lo1 & ENTRYLO_V)
  565| 				for (uint64_t ofs = 0; ofs < pagesize; ofs += 0x1000)
  566| 					cpu->invalidate_translation_caches(cpu, oldvaddr + ofs + pagesize, INVALIDATE_VADDR);
  567| 		}
  568| 	}
  569| }
  570| 
  571| 
  572| /*
  573|  *  coproc_register_read();
  574|  *
  575|  *  Read a value from a MIPS coprocessor register.
  576|  */
  577| void coproc_register_read(struct cpu *cpu,
  578| 	struct mips_coproc *cp, int reg_nr, uint64_t *ptr, int select)
  579| {
  580| 	int unimpl = 1;
  581| 
  582| 	if (cp->coproc_nr==0 && reg_nr==COP0_INDEX)	unimpl = 0;
  583| 	if (cp->coproc_nr==0 && reg_nr==COP0_RANDOM)	unimpl = 0;
  584| 	if (cp->coproc_nr==0 && reg_nr==COP0_ENTRYLO0)	unimpl = 0;
  585| 	if (cp->coproc_nr==0 && reg_nr==COP0_ENTRYLO1)	unimpl = 0;
  586| 	if (cp->coproc_nr==0 && reg_nr==COP0_CONTEXT)	unimpl = 0;
  587| 	if (cp->coproc_nr==0 && reg_nr==COP0_PAGEMASK)	unimpl = 0;
  588| 	if (cp->coproc_nr==0 && reg_nr==COP0_WIRED)	unimpl = 0;
  589| 	if (cp->coproc_nr==0 && reg_nr==COP0_BADVADDR)	unimpl = 0;
  590| 	if (cp->coproc_nr==0 && reg_nr==COP0_COUNT) {
  591| 		/*  TODO: Increase count in a more meaningful way!  */
  592| 		cp->reg[COP0_COUNT] = (int32_t) (cp->reg[COP0_COUNT] + 1);
  593| 		cpu->cd.mips.count_register_read_count ++;
  594| 		unimpl = 0;
  595| 	}
  596| 	if (cp->coproc_nr==0 && reg_nr==COP0_ENTRYHI)	unimpl = 0;
  597| 	if (cp->coproc_nr==0 && reg_nr==COP0_COMPARE)	unimpl = 0;
  598| 	if (cp->coproc_nr==0 && reg_nr==COP0_STATUS)	unimpl = 0;
  599| 	if (cp->coproc_nr==0 && reg_nr==COP0_CAUSE)	unimpl = 0;
  600| 	if (cp->coproc_nr==0 && reg_nr==COP0_EPC)	unimpl = 0;
  601| 	if (cp->coproc_nr==0 && reg_nr==COP0_PRID)	unimpl = 0;
  602| 	if (cp->coproc_nr==0 && reg_nr==COP0_CONFIG) {
  603| 		if (select > 0) {
  604| 			switch (select) {
  605| 			case 1:	*ptr = cpu->cd.mips.cop0_config_select1;
  606| 				break;
  607| 			default:fatal("coproc_register_read(): unimplemented"
  608| 				    " config register select %i\n", select);
  609| 				/*  #213: (Codex/Fable) guest-reachable via mfc0 Config2..7;
  610| 				    return a defined 0 instead of exit()ing the host.  */
  611| 				*ptr = 0;
  612| 				break;
  613| 			}
  614| 			return;
  615| 		}
  616| 		unimpl = 0;
  617| 	}
  618| 	if (cp->coproc_nr==0 && reg_nr==COP0_LLADDR)	unimpl = 0;
  619| 	if (cp->coproc_nr==0 && reg_nr==COP0_WATCHLO)	unimpl = 0;
  620| 	if (cp->coproc_nr==0 && reg_nr==COP0_WATCHHI)	unimpl = 0;
  621| 	if (cp->coproc_nr==0 && reg_nr==COP0_XCONTEXT)	unimpl = 0;
  622| 	if (cp->coproc_nr==0 && reg_nr==COP0_ERRCTL)	unimpl = 0;
  623| 	if (cp->coproc_nr==0 && reg_nr==COP0_CACHEERR)	unimpl = 0;
  624| 	if (cp->coproc_nr==0 && reg_nr==COP0_TAGDATA_LO)	unimpl = 0;
  625| 	if (cp->coproc_nr==0 && reg_nr==COP0_TAGDATA_HI)	unimpl = 0;
  626| 	if (cp->coproc_nr==0 && reg_nr==COP0_ERROREPC)	unimpl = 0;
  627| 	if (cp->coproc_nr==0 && reg_nr==COP0_RESERV22) {
  628| 		/*  Used by Linux on Linksys WRT54G  */
  629| 		unimpl = 0;
  630| 	}
  631| 	if (cp->coproc_nr==0 && reg_nr==COP0_DEBUG)	unimpl = 0;
  632| 	if (cp->coproc_nr==0 && reg_nr==COP0_PERFCNT)	unimpl = 0;
  633| 	if (cp->coproc_nr==0 && reg_nr==COP0_DESAVE)	unimpl = 0;
  634| 
  635| 	if (cp->coproc_nr==1)	unimpl = 0;
```

### `src/cpus/cpu_dyntrans.c` around the row's cited line 420 (HEAD d2a6f233, lines 375-465)

```c
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

End with one line: `FIXDRAFT_MIPSCOUNTREAD: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
