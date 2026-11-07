# GXemul hardened fork -- DRAFT A FIX for one filed issue, `ppcintentrymsr` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD d2a6f233).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `ppcintentrymsr`, state `open`, severity `MED`)

**title:** cpus/cpu_ppc.c:ppc_exception -- interrupt entry clears only EE, RI and PR; IR, DR, FP, SE, BE, FE0, FE1 and POW stay set and LE is not taken from ILE -- WRONG-RESULT (handlers run translated with FP/trace state of the interrupted context)

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T19 (class WRONG-RESULT; reach U, user mode; effort: small; report rows: A4-18).  Source URLs: https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/9bcc860c665aadb9b4ff852667fa5f490f90bf09, https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/0b8e81afd3fc59a0ec237224f94282098f2a0c27, https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/7cb33c85d3d21be36240f586f9b8e4c3c86364ef.  Our site at de8c7547: src/cpus/cpu_ppc.c:335.  Portable fix: yes -- port rs6000 9bcc860, rs6000 0b8e81a, rs6000 7cb33c8 together with the IR/DR flush row.  Filing check (TRIAGE.md): 0 hits for ILE / interrupt-entry MSR.  Port together with the MSR IR/DR flush, which `ppcbatstale` carries in its governing text (TRIAGE.md T96).  witness: none -- research finding, not yet reproduced here.  | 2026-11-05 (#582 qhslowifetch): the fix's `#QQQ` names this row.  #582's arm (d) raises a machine check through ppc_exception(cpu, PPC_EXCEPTION_MC), the constant new in #582, and ppc_exception() leaves MSR[ME] set (src/cpus/cpu_ppc.c:335 clears EE, RI and PR only), where the architecture clears it on a machine check (Book III v2.01 Figure 28 and PEM Table 6-8, as the ruling cites them) -- so a second failing fetch takes a second machine check instead of checkstopping.  The ruling (regress/artifacts/qhslowifetch/adj_20261104/FINAL_FABLE.md F2) filed 'ppc_exception()'s MSR modelling as a whole: per-interrupt clearing of IR, DR, FE0, FE1, FP, SE, BE and ME'; ME on a machine check is that filing's new member here.  No pmppc fetch reaches arm (d) (`ppcifetchdeclineprod`).

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- Port commits and clear ME along with IR/DR flush

## The code at the cited lines

### `src/cpus/cpu_ppc.c` around the row's cited line 335 (HEAD d2a6f233, lines 290-380)

```c
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
  373| 		debug("  <%s>\n", symbol != NULL? symbol : " no symbol ");
  374| 
  375| 		debug("cpu%i: lr  = 0x", x);
  376| 		if (bits32)
  377| 			debug("%08" PRIx32, (uint32_t)cpu->cd.ppc.spr[SPR_LR]);
  378| 		else
  379| 			debug("%016" PRIx64, (uint64_t)cpu->cd.ppc.spr[SPR_LR]);
  380| 		debug("  cr  = 0x%08" PRIx32, (uint32_t)cpu->cd.ppc.cr);
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

End with one line: `FIXDRAFT_PPCINTENTRYMSR: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.

## YOUR PREVIOUS DRAFT FAILED -- correct it

An earlier draft for this row was applied to the code above and checked.  It failed like this:

```text
APPLY FAILED: FAIL /mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/gweb/jobs_20261106_kits/fix_ppcintentrymsr//reply.txt: 0 json blocks
```

The previous edits:

```json
(no edit block was returned)
```


Return a CORRECTED draft in the same form.  If an `old` string occurred more than once, lengthen it with a distinctive
neighbouring line; if it occurred zero times, copy it exactly from the code shown; use only names that appear in this
packet.  If the fix cannot be written from what is shown, say `STILL PRESENT: UNSETTLED` and name what is missing.
