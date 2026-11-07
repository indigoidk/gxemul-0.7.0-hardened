# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `ppclswizero` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `ppclswizero`, state `open`)

**title:** cpus/cpu_ppc_instr.c:X(lswi) -- the unfilled low-order bytes of the last register keep stale data (zero-filled only in MODE_POWER), and the byte assembly uses signed-overflow shifts -- WRONG-RESULT (+ host UB)

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T22 (class WRONG-RESULT; reach U, user mode; effort: small; report rows: A4-17, A(b-1) class 1 (lswi shifts)).  Source URLs: https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/3cdc32f0d3ab8f4d33f09a13a02b4c5cb80b3221, https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/e88c21b997c83d816aea2f4806ed05a5723e5492.  Our site at de8c7547: src/cpus/cpu_ppc_instr.c:3056-3059.  Portable fix: yes -- port rs6000 3cdc32f, rs6000 e88c21b.  Filing check (TRIAGE.md): only `mrwstore2` mentions lswi, for partial completion.  witness: none -- research finding, not yet reproduced here.

**The drafter's own reading:** STILL PRESENT: YES -- cpus/cpu_ppc_instr.c:3069-3072

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/cpus/cpu_ppc_instr.c b/src/cpus/cpu_ppc_instr.c
index 508e9181..9554c68a 100644
--- a/src/cpus/cpu_ppc_instr.c
+++ b/src/cpus/cpu_ppc_instr.c
@@ -3066,10 +3066,10 @@ X(lswi)
 			return;
 		}
 
-		if (cpu->cd.ppc.mode == MODE_POWER && sub == 0)
+		if (sub == 0)
 			cpu->cd.ppc.gpr[rt] = 0;
-		cpu->cd.ppc.gpr[rt] &= ~(0xff << (24-8*sub));
-		cpu->cd.ppc.gpr[rt] |= (d << (24-8*sub));
+		cpu->cd.ppc.gpr[rt] &= ~(0xffU << (24-8*sub));
+		cpu->cd.ppc.gpr[rt] |= ((uint32_t)d << (24-8*sub));
 		sub ++;
 		if (sub == 4) {
 			rt = (rt + 1) & 31;
```

## Every edited function, after the fix

### `src/cpus/cpu_ppc_instr.c` -- post-edit lines 3049-3081 (`+` marks a line the diff added or the point of a deletion)

```c
 3049|  X(lswi)
 3050|  {
 3051|  	MODE_uint_t addr = reg(ic->arg[1]);
 3052|  	int rt = ic->arg[0], nb = ic->arg[2];
 3053|  	int sub = 0;
 3054|  
 3055|  	int low_pc = ((size_t)ic - (size_t)cpu->cd.ppc.cur_ic_page)
 3056|  	    / sizeof(struct ppc_instr_call);
 3057|  	cpu->pc &= ~((PPC_IC_ENTRIES_PER_PAGE-1)
 3058|  	    << PPC_INSTR_ALIGNMENT_SHIFT);
 3059|  	cpu->pc += (low_pc << PPC_INSTR_ALIGNMENT_SHIFT);
 3060|  
 3061|  	while (nb > 0) {
 3062|  		unsigned char d;
 3063|  		if (cpu->memory_rw(cpu, cpu->mem, addr, &d, 1,
 3064|  		    MEM_READ, CACHE_DATA) != MEMORY_ACCESS_OK) {
 3065|  			/*  exception  */
 3066|  			return;
 3067|  		}
 3068|  
 3069|+ 		if (sub == 0)
 3070|  			cpu->cd.ppc.gpr[rt] = 0;
 3071|+ 		cpu->cd.ppc.gpr[rt] &= ~(0xffU << (24-8*sub));
 3072|+ 		cpu->cd.ppc.gpr[rt] |= ((uint32_t)d << (24-8*sub));
 3073|  		sub ++;
 3074|  		if (sub == 4) {
 3075|  			rt = (rt + 1) & 31;
 3076|  			sub = 0;
 3077|  		}
 3078|  		addr ++;
 3079|  		nb --;
 3080|  	}
 3081|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_PPCLSWIZERO: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_PPCLSWIZERO: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
