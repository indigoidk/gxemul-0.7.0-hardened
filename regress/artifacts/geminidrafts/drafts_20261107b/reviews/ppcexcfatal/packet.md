# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `ppcexcfatal` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `ppcexcfatal`, state `open`)

**title:** cpus/cpu_ppc.c:ppc_exception + memory_ppc.c:ppc_translate_v2p -- one `fatal()` line per exception (decrementer, syscall) and per translation fault unless -q -- HYGIENE (guest-drivable host log flood)

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T140 (class HYGIENE; reach U, user mode; effort: one-line; report rows: A1-10, C U21).  Source URLs: https://github.com/retroprom/gxemul/commit/6d2d8bf0, https://sourceforge.net/p/gxemul/code2/HEAD/log/.  Our site at de8c7547: src/cpus/cpu_ppc.c:329-331; src/cpus/memory_ppc.c:302-305.  Portable fix: yes -- port upstream 6d2d8bf0 (SVN r6532) at INFO level.  Filing check (TRIAGE.md): `mrwstore2` says "SIBLING FILED" for memory_ppc.c:302-305 but no row or OB entry carries it; `floodclass` censuses device files.  Not a duplicate (regress/artifacts/research_20261022/adj_20261022/ADJ_RULINGS.md A).  This row is the carrier `mrwstore2`'s 'SIBLING FILED' claim about memory_ppc.c:302-305 never had (TRIAGE.md R5).  witness: none -- research finding, not yet reproduced here.

**The drafter's own reading:** STILL PRESENT: YES -- cpu_ppc.c:329 and memory_ppc.c:302 still contain the `fatal()` calls at HEAD.

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/cpus/cpu_ppc.c b/src/cpus/cpu_ppc.c
index e9bbadaa..f6a6390f 100644
--- a/src/cpus/cpu_ppc.c
+++ b/src/cpus/cpu_ppc.c
@@ -326,9 +326,7 @@ void ppc_exception(struct cpu *cpu, int exception_nr)
 	else
 		cpu->cd.ppc.spr[SPR_SRR1] = (cpu->cd.ppc.msr & 0x87c0ffff);
 
-	if (!quiet_mode)
-		fatal("[ PPC Exception 0x%x; pc=0x%" PRIx64" ]\n",
-		    exception_nr, cpu->pc);
+	/* #NNN: removed fatal() to prevent guest-drivable host log flood */
 
 	/*  Disable External Interrupts, Recoverable Interrupt Mode,
 	    and go to Supervisor mode  */
diff --git a/src/cpus/memory_ppc.c b/src/cpus/memory_ppc.c
index a5bd8e99..0be28b80 100644
--- a/src/cpus/memory_ppc.c
+++ b/src/cpus/memory_ppc.c
@@ -299,10 +299,7 @@ int ppc_translate_v2p(struct cpu *cpu, uint64_t vaddr,
 	if (flags & FLAG_NOEXCEPTIONS)
 		return 0;
 
-	if (!quiet_mode)
-		fatal("[ memory_ppc: exception! vaddr=0x%" PRIx64" pc=0x%" PRIx64
-		    " instr=%i user=%i wf=%i ]\n", (uint64_t) vaddr,
-		    (uint64_t) cpu->pc, instr, user, writeflag);
+	/* #NNN: removed fatal() to prevent guest-drivable host log flood */
 
 	if (cpu->cd.ppc.cpu_type.flags & PPC_603) {
 		cpu->cd.ppc.spr[instr? SPR_IMISS : SPR_DMISS] = vaddr;
```

## Every edited function, after the fix

### `src/cpus/cpu_ppc.c` -- post-edit lines 318-343 (`+` marks a line the diff added or the point of a deletion)

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
  329|+ 	/* #NNN: removed fatal() to prevent guest-drivable host log flood */
  330|  
  331|  	/*  Disable External Interrupts, Recoverable Interrupt Mode,
  332|  	    and go to Supervisor mode  */
  333|  	cpu->cd.ppc.msr &= ~(PPC_MSR_EE | PPC_MSR_RI | PPC_MSR_PR);
  334|  
  335|  	cpu->pc = exception_nr * 0x100;
  336|  	if (cpu->cd.ppc.msr & PPC_MSR_IP)
  337|  		cpu->pc += 0xfff00000ULL;
  338|  
  339|  	if (cpu->is_32bit)
  340|  		ppc32_pc_to_pointers(cpu);
  341|  	else
  342|  		ppc_pc_to_pointers(cpu);
  343|  }
```

### `src/cpus/memory_ppc.c` -- post-edit lines 247-324 (`+` marks a line the diff added or the point of a deletion)

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
  302|+ 	/* #NNN: removed fatal() to prevent guest-drivable host log flood */
  303|  
  304|  	if (cpu->cd.ppc.cpu_type.flags & PPC_603) {
  305|  		cpu->cd.ppc.spr[instr? SPR_IMISS : SPR_DMISS] = vaddr;
  306|  
  307|  		msr |= PPC_MSR_TGPR;
  308|  		reg_access_msr(cpu, &msr, 1, 0);
  309|  
  310|  		ppc_exception(cpu, instr? 0x10 : (writeflag? 0x12 : 0x11));
  311|  	} else {
  312|  		if (!instr) {
  313|  			cpu->cd.ppc.spr[SPR_DAR] = vaddr;
  314|  			cpu->cd.ppc.spr[SPR_DSISR] = match?
  315|  			    DSISR_PROTECT : DSISR_NOTFOUND;
  316|  			if (writeflag)
  317|  				cpu->cd.ppc.spr[SPR_DSISR] |= DSISR_STORE;
  318|  		}
  319|  		ppc_exception(cpu, instr?
  320|  		    PPC_EXCEPTION_ISI : PPC_EXCEPTION_DSI);
  321|  	}
  322|  
  323|  	return 0;
  324|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_PPCEXCFATAL: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_PPCEXCFATAL: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
