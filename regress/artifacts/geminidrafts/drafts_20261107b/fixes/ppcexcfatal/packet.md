# GXemul hardened fork -- REVISE ONE FIX DRAFT after a review, `ppcexcfatal` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork
removes crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  You drafted a fix for the
issue below; it compiles at HEAD 8d9df658.  A separate review then reported problems with it.  You cannot read files; work
from this text.  This is a DRAFTING task: FIX ONLY, as exact edits -- no tests, probes or reproduction steps.

## The issue (ledger row `ppcexcfatal`, state `open`)

**title:** cpus/cpu_ppc.c:ppc_exception + memory_ppc.c:ppc_translate_v2p -- one `fatal()` line per exception (decrementer, syscall) and per translation fault unless -q -- HYGIENE (guest-drivable host log flood)

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T140 (class HYGIENE; reach U, user mode; effort: one-line; report rows: A1-10, C U21).  Source URLs: https://github.com/retroprom/gxemul/commit/6d2d8bf0, https://sourceforge.net/p/gxemul/code2/HEAD/log/.  Our site at de8c7547: src/cpus/cpu_ppc.c:329-331; src/cpus/memory_ppc.c:302-305.  Portable fix: yes -- port upstream 6d2d8bf0 (SVN r6532) at INFO level.  Filing check (TRIAGE.md): `mrwstore2` says "SIBLING FILED" for memory_ppc.c:302-305 but no row or OB entry carries it; `floodclass` censuses device files.  Not a duplicate (regress/artifacts/research_20261022/adj_20261022/ADJ_RULINGS.md A).  This row is the carrier `mrwstore2`'s 'SIBLING FILED' claim about memory_ppc.c:302-305 never had (TRIAGE.md R5).  witness: none -- research finding, not yet reproduced here.

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
  326|  	else
  327|  		cpu->cd.ppc.spr[SPR_SRR1] = (cpu->cd.ppc.msr & 0x87c0ffff);
  328|  
  329|* 	if (!quiet_mode)
  330|* 		fatal("[ PPC Exception 0x%x; pc=0x%" PRIx64" ]\n",
  331|* 		    exception_nr, cpu->pc);
  332|* 
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
  302|* 	if (!quiet_mode)
  303|* 		fatal("[ memory_ppc: exception! vaddr=0x%" PRIx64" pc=0x%" PRIx64
  304|* 		    " instr=%i user=%i wf=%i ]\n", (uint64_t) vaddr,
  305|* 		    (uint64_t) cpu->pc, instr, user, writeflag);
  306|* 
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
  321|  		}
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
    "old": "\tif (!quiet_mode)\n\t\tfatal(\"[ PPC Exception 0x%x; pc=0x%\" PRIx64\" ]\\n\",\n\t\t    exception_nr, cpu->pc);\n",
    "new": "\t/* #NNN: removed fatal() to prevent guest-drivable host log flood */\n",
    "why": "Removing fatal() mitigates log flood without affecting exception state."
  },
  {
    "file": "src/cpus/memory_ppc.c",
    "old": "\tif (!quiet_mode)\n\t\tfatal(\"[ memory_ppc: exception! vaddr=0x%\" PRIx64\" pc=0x%\" PRIx64\n\t\t    \" instr=%i user=%i wf=%i ]\\n\", (uint64_t) vaddr,\n\t\t    (uint64_t) cpu->pc, instr, user, writeflag);\n",
    "new": "\t/* #NNN: removed fatal() to prevent guest-drivable host log flood */\n",
    "why": "Removing fatal() mitigates log flood without affecting memory fault state."
  }
]
```

## The review of that draft (it can be WRONG -- judge each point against the code above)

```text
FIXREVIEW_PPCEXCFATAL: DEFECT, 2 FINDINGS
1. Does the diff remove the defect the issue describes, at every site the issue names? Name any site it misses.
The diff visits both sites named in the issue (`cpu_ppc.c:ppc_exception` and `memory_ppc.c:ppc_translate_v2p`) and stops the `fatal()` log flood. However, the issue explicitly requires to "port upstream 6d2d8bf0 (SVN r6532) at INFO level". The diff fails this requirement by deleting the messages entirely instead of downgrading them to an info-level logging macro. 
2. CONTROL FLOW: does any added return, goto, break or early exit skip code the function would otherwise run?
No. The diff solely removes code and adds comments. It does not introduce any early exits, `return`, `goto`, or `break` statements. No common tail is skipped.
3. RETURN VALUE: does any path now return something different?
No. Return values and paths are unchanged.
4. What ELSE does the diff change?
By completely removing the `fatal()` calls rather than porting them to INFO level, the fix completely blinds the host to these exceptions and translation faults, dropping diagnostic state that should have been preserved at a lower visibility level.
5. House idioms:
The new comments correctly implement the `/* #NNN: ... */` tag, and the modified lines remain within the 79-column limit.
**Findings:**
* `cpu_ppc.c:329` DEFECT: The fix deletes the log instead of downgrading it; replace `/* #NNN: ... */` with an INFO-level log macro (e.g., `info(...)`) preserving the original message.
* `memory_ppc.c:302` DEFECT: The fix deletes the log instead of downgrading it; replace `/* #NNN: ... */` with an INFO-level log macro (e.g., `info(...)`) preserving the original message.
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

End with two lines: `REVISION_PPCEXCFATAL: <a> ACCEPTED, <r> REJECTED` and `FIXDRAFT_PPCEXCFATAL: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
