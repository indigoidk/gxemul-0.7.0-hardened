# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `mipsdivwrap` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `mipsdivwrap`, state `open`)

**title:** cpus/cpu_mips_instr.c:X(div)/X(ddiv) -- INT_MIN / -1 returns LO=0 (and ddiv HI = dividend) where the manuals give the wrapped quotient with HI=0 -- WRONG-RESULT

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T21 (class WRONG-RESULT; reach U, user mode; effort: one-line each; report rows: A6-5, A issues (CHERI PR#1)).  Source URLs: https://github.com/CTSRD-CHERI/gxemul/commit/1236c18954d858650dcc6267ede063fad1e6df6b, https://github.com/CTSRD-CHERI/gxemul/pull/1.  Our site at de8c7547: src/cpus/cpu_mips_instr.c:1839-1840, :1863-1867.  Portable fix: yes -- port CHERI 1236c18 / CHERI PR#1 (result value only; the host-trap guard is already present).  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**The drafter's own reading:** STILL PRESENT: YES -- src/cpus/cpu_mips_instr.c:1840

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/cpus/cpu_mips_instr.c b/src/cpus/cpu_mips_instr.c
index 0df67fd9..ba91d225 100644
--- a/src/cpus/cpu_mips_instr.c
+++ b/src/cpus/cpu_mips_instr.c
@@ -1837,7 +1837,7 @@ X(div)
 	if (b == 0)
 		res = 0, rem = a;
 	else if (a == (int32_t)0x80000000U && b == -1)
-		res = 0, rem = 0;
+		res = a, rem = 0;
 	else
 		res = a / b, rem = a - b*res;
 	cpu->cd.mips.lo = (int32_t)res;
@@ -1859,12 +1859,11 @@ X(ddiv)
 	int64_t a = reg(ic->arg[0]), b = reg(ic->arg[1]);
 	int64_t res, rem;
 	if (b == 0)
-		res = 0;
+		res = 0, rem = a;
 	else if (a == (int64_t)0x8000000000000000ULL && b == -1)
-		res = 0;
+		res = a, rem = 0;
 	else
-		res = a / b;
-	rem = a - b*res;
+		res = a / b, rem = a - b*res;
 	cpu->cd.mips.lo = res;
 	cpu->cd.mips.hi = rem;
 }
```

## Every edited function, after the fix

### `src/cpus/cpu_mips_instr.c` -- post-edit lines 1833-1845 (`+` marks a line the diff added or the point of a deletion)

```c
 1833|  X(div)
 1834|  {
 1835|  	int32_t a = reg(ic->arg[0]), b = reg(ic->arg[1]);
 1836|  	int32_t res, rem;
 1837|  	if (b == 0)
 1838|  		res = 0, rem = a;
 1839|  	else if (a == (int32_t)0x80000000U && b == -1)
 1840|+ 		res = a, rem = 0;
 1841|  	else
 1842|  		res = a / b, rem = a - b*res;
 1843|  	cpu->cd.mips.lo = (int32_t)res;
 1844|  	cpu->cd.mips.hi = (int32_t)rem;
 1845|  }
```

### `src/cpus/cpu_mips_instr.c` -- post-edit lines 1857-1869 (`+` marks a line the diff added or the point of a deletion)

```c
 1857|  X(ddiv)
 1858|  {
 1859|  	int64_t a = reg(ic->arg[0]), b = reg(ic->arg[1]);
 1860|  	int64_t res, rem;
 1861|  	if (b == 0)
 1862|+ 		res = 0, rem = a;
 1863|  	else if (a == (int64_t)0x8000000000000000ULL && b == -1)
 1864|+ 		res = a, rem = 0;
 1865|  	else
 1866|+ 		res = a / b, rem = a - b*res;
 1867|  	cpu->cd.mips.lo = res;
 1868|  	cpu->cd.mips.hi = rem;
 1869|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_MIPSDIVWRAP: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_MIPSDIVWRAP: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
