# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `ppcbatppkill` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `ppcbatppkill`, state `open`)

**title:** PPC: a BAT hit with PP=00, or a store through a read-only BAT, reaches fatal()+exit(1) instead of a DSI/ISI

**state_note (head):** [2026-10-22] RE-FOUND by the external-fixes adjudication as N5 (regress/artifacts/research_20261022/adj_20261022/ADJ_RULINGS.md C; Grok 4.7, adj_20261022/grok_adj.txt): memory_ppc.c:69-73 (the BAT block returns 0 for PP=none, or for a write to a read-only BAT) and the caller's exit at :273-276 are this row's defect, so no second row is filed -- the seat searched for the message text 'TODO: BAT exception', which this row does not quote.  `qhslowifetch`'s fix (return into an ISI already raised) is not this row's fix (regress/artifacts/research_20261022/adj_20261022/ADJ_RULINGS.md B, T6).  ||  GOVERNING TEXT (from the dispositions file, cut at 400 characters): `ppcbatppkill` HIGH -- PPC: a BAT hit with PP=00, or a store through a read-only BAT, reaches `fatal()` + `exit(1)` (memory_ppc.c `ppc_bat_block` -> `:273-276`) instead of a DSI/ISI (ppc_pem32_rev2_2001.txt:13503-13519). Also precedes the FLAG_NOEXCEPTIONS test, so a debugger `dump` of such a block ends the process

**The drafter's own reading:** STILL PRESENT: YES -- src/cpus/memory_ppc.c:274

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/cpus/memory_ppc.c b/src/cpus/memory_ppc.c
index a5bd8e99..f527115c 100644
--- a/src/cpus/memory_ppc.c
+++ b/src/cpus/memory_ppc.c
@@ -271,8 +271,8 @@ int ppc_translate_v2p(struct cpu *cpu, uint64_t vaddr,
 		if (res > 0)
 			return res;
 		if (res == 0) {
-			fatal("[ TODO: BAT exception ]\n");
-			exit(1);
+			match = 1;
+			goto do_exception;
 		}
 	}
 
@@ -289,6 +289,7 @@ int ppc_translate_v2p(struct cpu *cpu, uint64_t vaddr,
 	}
 
 
+do_exception:
 	/*
 	 *  No match? Then cause an exception.
 	 *
```

## Every edited function, after the fix

### `src/cpus/memory_ppc.c` -- post-edit lines 247-328 (`+` marks a line the diff added or the point of a deletion)

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
  274|+ 			match = 1;
  275|+ 			goto do_exception;
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
  292|+ do_exception:
  293|  	/*
  294|  	 *  No match? Then cause an exception.
  295|  	 *
  296|  	 *  PPC603: cause a software TLB reload exception.
  297|  	 *  All others: cause a DSI or ISI.
  298|  	 */
  299|  
  300|  	if (flags & FLAG_NOEXCEPTIONS)
  301|  		return 0;
  302|  
  303|  	if (!quiet_mode)
  304|  		fatal("[ memory_ppc: exception! vaddr=0x%" PRIx64" pc=0x%" PRIx64
  305|  		    " instr=%i user=%i wf=%i ]\n", (uint64_t) vaddr,
  306|  		    (uint64_t) cpu->pc, instr, user, writeflag);
  307|  
  308|  	if (cpu->cd.ppc.cpu_type.flags & PPC_603) {
  309|  		cpu->cd.ppc.spr[instr? SPR_IMISS : SPR_DMISS] = vaddr;
  310|  
  311|  		msr |= PPC_MSR_TGPR;
  312|  		reg_access_msr(cpu, &msr, 1, 0);
  313|  
  314|  		ppc_exception(cpu, instr? 0x10 : (writeflag? 0x12 : 0x11));
  315|  	} else {
  316|  		if (!instr) {
  317|  			cpu->cd.ppc.spr[SPR_DAR] = vaddr;
  318|  			cpu->cd.ppc.spr[SPR_DSISR] = match?
  319|  			    DSISR_PROTECT : DSISR_NOTFOUND;
  320|  			if (writeflag)
  321|  				cpu->cd.ppc.spr[SPR_DSISR] |= DSISR_STORE;
  322|  		}
  323|  		ppc_exception(cpu, instr?
  324|  		    PPC_EXCEPTION_ISI : PPC_EXCEPTION_DSI);
  325|  	}
  326|  
  327|  	return 0;
  328|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_PPCBATPPKILL: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_PPCBATPPKILL: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
