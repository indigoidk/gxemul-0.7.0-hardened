# GXemul hardened fork -- REVISE ONE FIX DRAFT after a review, `ppcisisrr1` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork
removes crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  You drafted a fix for the
issue below; it compiles at HEAD 8d9df658.  A separate review then reported problems with it.  You cannot read files; work
from this text.  This is a DRAFTING task: FIX ONLY, as exact edits -- no tests, probes or reproduction steps.

## The issue (ledger row `ppcisisrr1`, state `open`)

**title:** cpus/cpu_ppc.c:ppc_exception + memory_ppc.c:ppc_translate_v2p -- an ISI sets no SRR1 reason bit (not-found, protection, no-execute) -- WRONG-RESULT

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T25 (class WRONG-RESULT; reach U, user mode; effort: small; report rows: A4-19).  Source URLs: https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/8b0737a40738a47c4dd5e360c482caa5756b2c54, https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/7cb33c85d3d21be36240f586f9b8e4c3c86364ef.  Our site at de8c7547: src/cpus/cpu_ppc.c:327; src/cpus/memory_ppc.c:315-323.  Portable fix: partial, or an idea only -- port with correction: rs6000 8b0737a, rs6000 7cb33c8 (its no-execute/guarded bit is wrong).  Filing check (TRIAGE.md): 0 hits.  Do not port rs6000's no-execute/guarded ISI bit (regress/artifacts/research_20261022/adj_20261022/ADJ_RULINGS.md F).  witness: none -- research finding, not yet reproduced here.

## Every function your previous draft changed, as it reads AT HEAD (your new edits apply to THIS text)

### `src/cpus/cpu_ppc.c` -- AT HEAD, lines 318-345 (`*` marks a line your previous draft changed)

```c
  318|  void ppc_exception(struct cpu *cpu, int exception_nr)
  319|  {
  320|  	/*  Save PC and MSR:  */
  321|  	cpu->cd.ppc.spr[SPR_SRR0] = cpu->pc;
  322|  
  323|  	if (exception_nr >= 0x10 && exception_nr <= 0x13)
  324|  		cpu->cd.ppc.spr[SPR_SRR1] = (cpu->cd.ppc.msr & 0xffff)
  325|  		    | (cpu->cd.ppc.cr & 0xf0000000);
  326|* 	else
  327|* 		cpu->cd.ppc.spr[SPR_SRR1] = (cpu->cd.ppc.msr & 0x87c0ffff);
  328|* 
  329|  	if (!quiet_mode)
  330|  		fatal("[ PPC Exception 0x%x; pc=0x%" PRIx64" ]\n",
  331|  		    exception_nr, cpu->pc);
  332|  
  333|  	/*  Disable External Interrupts, Recoverable Interrupt Mode,
  334|  	    and go to Supervisor mode  */
  335|  	cpu->cd.ppc.msr &= ~(PPC_MSR_EE | PPC_MSR_RI | PPC_MSR_PR);
  336|  
  337|  	cpu->pc = exception_nr * 0x100;
  338|  	if (cpu->cd.ppc.msr & PPC_MSR_IP)
  339|  		cpu->pc += 0xfff00000ULL;
  340|  
  341|  	if (cpu->is_32bit)
  342|  		ppc32_pc_to_pointers(cpu);
  343|  	else
  344|  		ppc_pc_to_pointers(cpu);
  345|  }
```

### `src/cpus/memory_ppc.c` -- AT HEAD, lines 247-327 (`*` marks a line your previous draft changed)

```c
  247|  {
  248|  	int instr = flags & FLAG_INSTR, res = 0, match, user;
  249|  	int writeflag = flags & FLAG_WRITEFLAG? 1 : 0;
  250|  	uint64_t msr;
  251|  
  252|  	reg_access_msr(cpu, &msr, 0, 0);
  253|  	user = msr & PPC_MSR_PR? 1 : 0;
  254|  
  255|  	if (cpu->cd.ppc.bits == 32)
  256|  		vaddr &= 0xffffffff;
  257|  
  258|  	if ((instr && !(msr & PPC_MSR_IR)) || (!instr && !(msr & PPC_MSR_DR))) {
  259|  		*return_paddr = vaddr;
  260|  		return 2;
  261|  	}
  262|  
  263|  	if (cpu->cd.ppc.cpu_type.flags & PPC_601) {
  264|  		fatal("ppc_translate_v2p(): TODO: 601\n");
  265|  		exit(1);
  266|  	}
  267|  
  268|  	/*  Try the BATs first:  */
  269|  	if (cpu->cd.ppc.bits == 32) {
  270|  		res = ppc_bat(cpu, vaddr, return_paddr, flags, user);
  271|  		if (res > 0)
  272|  			return res;
  273|  		if (res == 0) {
  274|  			fatal("[ TODO: BAT exception ]\n");
  275|  			exit(1);
  276|  		}
  277|  	}
  278|  
  279|  	/*  Virtual to physical translation:  */
  280|  	if (cpu->cd.ppc.bits == 32) {
  281|  		match = ppc_vtp32(cpu, vaddr, return_paddr, &res, msr,
  282|  		    writeflag, instr);
  283|  		if (match && res > 0)
  284|  			return res;
  285|  	} else {
  286|  		/*  htaborg = sdr1 & 0xfffffffffffc0000ULL;  */
  287|  		fatal("TODO: ppc 64-bit translation\n");
  288|  		exit(1);
  289|  	}
  290|  
  291|  
  292|  	/*
  293|  	 *  No match? Then cause an exception.
  294|  	 *
  295|  	 *  PPC603: cause a software TLB reload exception.
  296|  	 *  All others: cause a DSI or ISI.
  297|  	 */
  298|  
  299|  	if (flags & FLAG_NOEXCEPTIONS)
  300|  		return 0;
  301|  
  302|  	if (!quiet_mode)
  303|  		fatal("[ memory_ppc: exception! vaddr=0x%" PRIx64" pc=0x%" PRIx64
  304|  		    " instr=%i user=%i wf=%i ]\n", (uint64_t) vaddr,
  305|  		    (uint64_t) cpu->pc, instr, user, writeflag);
  306|  
  307|  	if (cpu->cd.ppc.cpu_type.flags & PPC_603) {
  308|  		cpu->cd.ppc.spr[instr? SPR_IMISS : SPR_DMISS] = vaddr;
  309|  
  310|  		msr |= PPC_MSR_TGPR;
  311|  		reg_access_msr(cpu, &msr, 1, 0);
  312|  
  313|  		ppc_exception(cpu, instr? 0x10 : (writeflag? 0x12 : 0x11));
  314|  	} else {
  315|  		if (!instr) {
  316|  			cpu->cd.ppc.spr[SPR_DAR] = vaddr;
  317|  			cpu->cd.ppc.spr[SPR_DSISR] = match?
  318|  			    DSISR_PROTECT : DSISR_NOTFOUND;
  319|  			if (writeflag)
  320|  				cpu->cd.ppc.spr[SPR_DSISR] |= DSISR_STORE;
  321|* 		}
  322|  		ppc_exception(cpu, instr?
  323|  		    PPC_EXCEPTION_ISI : PPC_EXCEPTION_DSI);
  324|  	}
  325|  
  326|  	return 0;
  327|  }
```



## Your previous draft's edits

```json
[
  {
    "file": "src/cpus/cpu_ppc.c",
    "old": "\telse\n\t\tcpu->cd.ppc.spr[SPR_SRR1] = (cpu->cd.ppc.msr & 0x87c0ffff);",
    "new": "\telse {\n\t\tuint32_t reason = (exception_nr == PPC_EXCEPTION_ISI) ?\n\t\t    (cpu->cd.ppc.spr[SPR_SRR1] & ~0x87c0ffff) : 0;\n\t\tcpu->cd.ppc.spr[SPR_SRR1] = (cpu->cd.ppc.msr & 0x87c0ffff) | reason;\n\t}",
    "why": "/* #ppcisisrr1: Preserve upper-half reason bits in SRR1 for ISI exceptions. */"
  },
  {
    "file": "src/cpus/memory_ppc.c",
    "old": "\t\tif (!instr) {\n\t\t\tcpu->cd.ppc.spr[SPR_DAR] = vaddr;\n\t\t\tcpu->cd.ppc.spr[SPR_DSISR] = match?\n\t\t\t    DSISR_PROTECT : DSISR_NOTFOUND;\n\t\t\tif (writeflag)\n\t\t\t\tcpu->cd.ppc.spr[SPR_DSISR] |= DSISR_STORE;\n\t\t}\n\t\tppc_exception(cpu, instr?\n\t\t    PPC_EXCEPTION_ISI : PPC_EXCEPTION_DSI);",
    "new": "\t\tif (!instr) {\n\t\t\tcpu->cd.ppc.spr[SPR_DAR] = vaddr;\n\t\t\tcpu->cd.ppc.spr[SPR_DSISR] = match?\n\t\t\t    DSISR_PROTECT : DSISR_NOTFOUND;\n\t\t\tif (writeflag)\n\t\t\t\tcpu->cd.ppc.spr[SPR_DSISR] |= DSISR_STORE;\n\t\t} else {\n\t\t\t/* #ppcisisrr1: ISI uses the same bit layout as DSISR for not-found and protect. */\n\t\t\tcpu->cd.ppc.spr[SPR_SRR1] = match?\n\t\t\t    DSISR_PROTECT : DSISR_NOTFOUND;\n\t\t}\n\t\tppc_exception(cpu, instr?\n\t\t    PPC_EXCEPTION_ISI : PPC_EXCEPTION_DSI);",
    "why": "Set the appropriate bits (not-found or protection) in SRR1 when raising an ISI exception."
  }
]
```

## The review of that draft (it can be WRONG -- judge each point against the code above)

```text
FIXREVIEW_PPCISISRR1: DEFECT, 2 FINDINGS
1. **Defect removal**: Yes, the diff sets the reason bits (via `DSISR_PROTECT` and `DSISR_NOTFOUND`) in `memory_ppc.c` and merges them into SRR1 in `cpu_ppc.c` for `PPC_EXCEPTION_ISI`. (Whether the DSISR constants physically map into `~0x87c0ffff` correctly is UNSETTLED; requires the header defining them).
2. **Control Flow**: No added returns, gotos, breaks, or early exits skip any code.
3. **Return Value**: No paths return anything different.
4. **State changed**: By reading `cpu->cd.ppc.spr[SPR_SRR1]` in `cpu_ppc.c:328`, the fix introduces a state leak. If *any* other site in the codebase triggers `PPC_EXCEPTION_ISI` without manually seeding `SPR_SRR1` first, whatever stale data the guest left in those SRR1 bits will be preserved and exposed back to the guest.
5. **House idioms**: The new comment in `memory_ppc.c:322` exceeds 79 columns. 
* `src/cpus/cpu_ppc.c:328`, DEFECT, reads potentially uninitialized/stale guest state; fix: pass the reason code as an argument to `ppc_exception` instead of side-channeling it through the guest's SPR_SRR1 register.
* `src/cpus/memory_ppc.c:322`, STYLE, comment exceeds 79 columns; fix: break into two lines.
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

End with two lines: `REVISION_PPCISISRR1: <a> ACCEPTED, <r> REJECTED` and `FIXDRAFT_PPCISISRR1: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
