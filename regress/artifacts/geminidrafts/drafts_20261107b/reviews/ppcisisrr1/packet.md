# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `ppcisisrr1` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `ppcisisrr1`, state `open`)

**title:** cpus/cpu_ppc.c:ppc_exception + memory_ppc.c:ppc_translate_v2p -- an ISI sets no SRR1 reason bit (not-found, protection, no-execute) -- WRONG-RESULT

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T25 (class WRONG-RESULT; reach U, user mode; effort: small; report rows: A4-19).  Source URLs: https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/8b0737a40738a47c4dd5e360c482caa5756b2c54, https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/7cb33c85d3d21be36240f586f9b8e4c3c86364ef.  Our site at de8c7547: src/cpus/cpu_ppc.c:327; src/cpus/memory_ppc.c:315-323.  Portable fix: partial, or an idea only -- port with correction: rs6000 8b0737a, rs6000 7cb33c8 (its no-execute/guarded bit is wrong).  Filing check (TRIAGE.md): 0 hits.  Do not port rs6000's no-execute/guarded ISI bit (regress/artifacts/research_20261022/adj_20261022/ADJ_RULINGS.md F).  witness: none -- research finding, not yet reproduced here.

**The drafter's own reading:** STILL PRESENT: YES -- cpu_ppc.c:328 (the draft reads potentially stale SRR1 state)

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/cpus/memory_ppc.c b/src/cpus/memory_ppc.c
index a5bd8e99..4a4011a7 100644
--- a/src/cpus/memory_ppc.c
+++ b/src/cpus/memory_ppc.c
@@ -321,6 +321,11 @@ int ppc_translate_v2p(struct cpu *cpu, uint64_t vaddr,
 		}
 		ppc_exception(cpu, instr?
 		    PPC_EXCEPTION_ISI : PPC_EXCEPTION_DSI);
+		if (instr) {
+			/* #ppcisisrr1: ISI uses DSISR layout. */
+			cpu->cd.ppc.spr[SPR_SRR1] |= match?
+			    DSISR_PROTECT : DSISR_NOTFOUND;
+		}
 	}
 
 	return 0;
```

## Every edited function, after the fix

### `src/cpus/memory_ppc.c` -- post-edit lines 247-332 (`+` marks a line the diff added or the point of a deletion)

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
  321|  		}
  322|  		ppc_exception(cpu, instr?
  323|  		    PPC_EXCEPTION_ISI : PPC_EXCEPTION_DSI);
  324|+ 		if (instr) {
  325|+ 			/* #ppcisisrr1: ISI uses DSISR layout. */
  326|+ 			cpu->cd.ppc.spr[SPR_SRR1] |= match?
  327|+ 			    DSISR_PROTECT : DSISR_NOTFOUND;
  328|+ 		}
  329|  	}
  330|  
  331|  	return 0;
  332|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_PPCISISRR1: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_PPCISISRR1: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
