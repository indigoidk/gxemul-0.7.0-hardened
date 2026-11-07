# GXemul hardened fork -- DRAFT A FIX for one filed issue, `ppcisisrr1` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD d2a6f233).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `ppcisisrr1`, state `open`, severity `MED`)

**title:** cpus/cpu_ppc.c:ppc_exception + memory_ppc.c:ppc_translate_v2p -- an ISI sets no SRR1 reason bit (not-found, protection, no-execute) -- WRONG-RESULT

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T25 (class WRONG-RESULT; reach U, user mode; effort: small; report rows: A4-19).  Source URLs: https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/8b0737a40738a47c4dd5e360c482caa5756b2c54, https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/7cb33c85d3d21be36240f586f9b8e4c3c86364ef.  Our site at de8c7547: src/cpus/cpu_ppc.c:327; src/cpus/memory_ppc.c:315-323.  Portable fix: partial, or an idea only -- port with correction: rs6000 8b0737a, rs6000 7cb33c8 (its no-execute/guarded bit is wrong).  Filing check (TRIAGE.md): 0 hits.  Do not port rs6000's no-execute/guarded ISI bit (regress/artifacts/research_20261022/adj_20261022/ADJ_RULINGS.md F).  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- Port partial fixes excluding no-execute/guarded ISI bit

## The code at the cited lines

### `src/cpus/cpu_ppc.c` around the row's cited line 327 (HEAD d2a6f233, lines 282-372)

```c
  282| 				uint64_t t = cpu->cd.ppc.gpr[i];
  283| 				cpu->cd.ppc.gpr[i] = cpu->cd.ppc.tgpr[i];
  284| 				cpu->cd.ppc.tgpr[i] = t;
  285| 			}
  286| 		}
  287| 
  288| 		if (cpu->cd.ppc.msr & PPC_MSR_IP) {
  289| 			fatal("\n[ Reboot hack for NetBSD/prep. TODO: "
  290| 			    "fix this. ]\n");
  291| 			cpu->running = 0;
  292| 		}
  293| 	}
  294| 
  295| 	/*  TODO: Is the little-endian bit writable?  */
  296| 
  297| 	cpu->cd.ppc.msr &= ~PPC_MSR_LE;
  298| 	if (cpu->byte_order != EMUL_BIG_ENDIAN)
  299| 		cpu->cd.ppc.msr |= PPC_MSR_LE;
  300| 
  301| 	if (!writeflag)
  302| 		*valuep = cpu->cd.ppc.msr;
  303| 
  304| 	if (check_for_interrupts && cpu->cd.ppc.msr & PPC_MSR_EE) {
  305| 		if (cpu->cd.ppc.dec_intr_pending &&
  306| 		    !(cpu->cd.ppc.cpu_type.flags & PPC_NO_DEC)) {
  307| 			ppc_exception(cpu, PPC_EXCEPTION_DEC);
  308| 			cpu->cd.ppc.dec_intr_pending = 0;
  309| 		} else if (cpu->cd.ppc.irq_asserted)
  310| 			ppc_exception(cpu, PPC_EXCEPTION_EI);
  311| 	}
  312| }
  313| 
  314| 
  315| /*
  316|  *  ppc_exception():
  317|  */
  318| void ppc_exception(struct cpu *cpu, int exception_nr)
  319| {
  320| 	/*  Save PC and MSR:  */
  321| 	cpu->cd.ppc.spr[SPR_SRR0] = cpu->pc;
  322| 
  323| 	if (exception_nr >= 0x10 && exception_nr <= 0x13)
  324| 		cpu->cd.ppc.spr[SPR_SRR1] = (cpu->cd.ppc.msr & 0xffff)
  325| 		    | (cpu->cd.ppc.cr & 0xf0000000);
  326| 	else
  327| 		cpu->cd.ppc.spr[SPR_SRR1] = (cpu->cd.ppc.msr & 0x87c0ffff);
  328| 
  329| 	if (!quiet_mode)
  330| 		fatal("[ PPC Exception 0x%x; pc=0x%" PRIx64" ]\n",
  331| 		    exception_nr, cpu->pc);
  332| 
  333| 	/*  Disable External Interrupts, Recoverable Interrupt Mode,
  334| 	    and go to Supervisor mode  */
  335| 	cpu->cd.ppc.msr &= ~(PPC_MSR_EE | PPC_MSR_RI | PPC_MSR_PR);
  336| 
  337| 	cpu->pc = exception_nr * 0x100;
  338| 	if (cpu->cd.ppc.msr & PPC_MSR_IP)
  339| 		cpu->pc += 0xfff00000ULL;
  340| 
  341| 	if (cpu->is_32bit)
  342| 		ppc32_pc_to_pointers(cpu);
  343| 	else
  344| 		ppc_pc_to_pointers(cpu);
  345| }
  346| 
  347| 
  348| /*
  349|  *  ppc_cpu_register_dump():
  350|  *
  351|  *  Dump cpu registers in a relatively readable format.
  352|  *
  353|  *  gprs: set to non-zero to dump GPRs and some special-purpose registers.
  354|  *  coprocs: if bit i is set, then we should dump registers from coproc i.
  355|  */
  356| void ppc_cpu_register_dump(struct cpu *cpu, int gprs, int coprocs)
  357| {
  358| 	char *symbol;
  359| 	uint64_t offset, tmp;
  360| 	int i, x = cpu->cpu_id;
  361| 	int bits32 = cpu->cd.ppc.bits == 32;
  362| 
  363| 	if (gprs) {
  364| 		/*  Special registers (pc, ...) first:  */
  365| 		symbol = get_symbol_name(&cpu->machine->symbol_context,
  366| 		    cpu->pc, &offset);
  367| 
  368| 		debug("cpu%i: pc  = 0x", x);
  369| 		if (bits32)
  370| 			debug("%08" PRIx32, (uint32_t)cpu->pc);
  371| 		else
  372| 			debug("%016" PRIx64, (uint64_t)cpu->pc);
```

### `src/cpus/memory_ppc.c` around the row's cited line 315 (HEAD d2a6f233, lines 270-329)

```c
  270| 		res = ppc_bat(cpu, vaddr, return_paddr, flags, user);
  271| 		if (res > 0)
  272| 			return res;
  273| 		if (res == 0) {
  274| 			fatal("[ TODO: BAT exception ]\n");
  275| 			exit(1);
  276| 		}
  277| 	}
  278| 
  279| 	/*  Virtual to physical translation:  */
  280| 	if (cpu->cd.ppc.bits == 32) {
  281| 		match = ppc_vtp32(cpu, vaddr, return_paddr, &res, msr,
  282| 		    writeflag, instr);
  283| 		if (match && res > 0)
  284| 			return res;
  285| 	} else {
  286| 		/*  htaborg = sdr1 & 0xfffffffffffc0000ULL;  */
  287| 		fatal("TODO: ppc 64-bit translation\n");
  288| 		exit(1);
  289| 	}
  290| 
  291| 
  292| 	/*
  293| 	 *  No match? Then cause an exception.
  294| 	 *
  295| 	 *  PPC603: cause a software TLB reload exception.
  296| 	 *  All others: cause a DSI or ISI.
  297| 	 */
  298| 
  299| 	if (flags & FLAG_NOEXCEPTIONS)
  300| 		return 0;
  301| 
  302| 	if (!quiet_mode)
  303| 		fatal("[ memory_ppc: exception! vaddr=0x%" PRIx64" pc=0x%" PRIx64
  304| 		    " instr=%i user=%i wf=%i ]\n", (uint64_t) vaddr,
  305| 		    (uint64_t) cpu->pc, instr, user, writeflag);
  306| 
  307| 	if (cpu->cd.ppc.cpu_type.flags & PPC_603) {
  308| 		cpu->cd.ppc.spr[instr? SPR_IMISS : SPR_DMISS] = vaddr;
  309| 
  310| 		msr |= PPC_MSR_TGPR;
  311| 		reg_access_msr(cpu, &msr, 1, 0);
  312| 
  313| 		ppc_exception(cpu, instr? 0x10 : (writeflag? 0x12 : 0x11));
  314| 	} else {
  315| 		if (!instr) {
  316| 			cpu->cd.ppc.spr[SPR_DAR] = vaddr;
  317| 			cpu->cd.ppc.spr[SPR_DSISR] = match?
  318| 			    DSISR_PROTECT : DSISR_NOTFOUND;
  319| 			if (writeflag)
  320| 				cpu->cd.ppc.spr[SPR_DSISR] |= DSISR_STORE;
  321| 		}
  322| 		ppc_exception(cpu, instr?
  323| 		    PPC_EXCEPTION_ISI : PPC_EXCEPTION_DSI);
  324| 	}
  325| 
  326| 	return 0;
  327| }
  328| 
  329| 
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

End with one line: `FIXDRAFT_PPCISISRR1: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
