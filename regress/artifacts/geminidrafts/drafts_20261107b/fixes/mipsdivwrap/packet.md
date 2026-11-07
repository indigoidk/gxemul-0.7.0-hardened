# GXemul hardened fork -- REVISE ONE FIX DRAFT after a review, `mipsdivwrap` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork
removes crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  You drafted a fix for the
issue below; it compiles at HEAD 8d9df658.  A separate review then reported problems with it.  You cannot read files; work
from this text.  This is a DRAFTING task: FIX ONLY, as exact edits -- no tests, probes or reproduction steps.

## The issue (ledger row `mipsdivwrap`, state `open`)

**title:** cpus/cpu_mips_instr.c:X(div)/X(ddiv) -- INT_MIN / -1 returns LO=0 (and ddiv HI = dividend) where the manuals give the wrapped quotient with HI=0 -- WRONG-RESULT

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T21 (class WRONG-RESULT; reach U, user mode; effort: one-line each; report rows: A6-5, A issues (CHERI PR#1)).  Source URLs: https://github.com/CTSRD-CHERI/gxemul/commit/1236c18954d858650dcc6267ede063fad1e6df6b, https://github.com/CTSRD-CHERI/gxemul/pull/1.  Our site at de8c7547: src/cpus/cpu_mips_instr.c:1839-1840, :1863-1867.  Portable fix: yes -- port CHERI 1236c18 / CHERI PR#1 (result value only; the host-trap guard is already present).  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

## Every function your previous draft changed, as it reads AT HEAD (your new edits apply to THIS text)

### `src/cpus/cpu_mips_instr.c` -- AT HEAD, lines 1833-1845 (`*` marks a line your previous draft changed)

```c
 1833|  X(div)
 1834|  {
 1835|  	int32_t a = reg(ic->arg[0]), b = reg(ic->arg[1]);
 1836|  	int32_t res, rem;
 1837|  	if (b == 0)
 1838|  		res = 0, rem = a;
 1839|  	else if (a == (int32_t)0x80000000U && b == -1)
 1840|* 		res = 0, rem = 0;
 1841|* 	else
 1842|  		res = a / b, rem = a - b*res;
 1843|  	cpu->cd.mips.lo = (int32_t)res;
 1844|  	cpu->cd.mips.hi = (int32_t)rem;
 1845|  }
```

### `src/cpus/cpu_mips_instr.c` -- AT HEAD, lines 1857-1870 (`*` marks a line your previous draft changed)

```c
 1857|  X(ddiv)
 1858|  {
 1859|  	int64_t a = reg(ic->arg[0]), b = reg(ic->arg[1]);
 1860|  	int64_t res, rem;
 1861|  	if (b == 0)
 1862|  		res = 0;
 1863|  	else if (a == (int64_t)0x8000000000000000ULL && b == -1)
 1864|* 		res = 0;
 1865|* 	else
 1866|  		res = a / b;
 1867|  	rem = a - b*res;
 1868|  	cpu->cd.mips.lo = res;
 1869|  	cpu->cd.mips.hi = rem;
 1870|  }
```



## Your previous draft's edits

```json
[
  {
    "file": "src/cpus/cpu_mips_instr.c",
    "old": "\telse if (a == (int32_t)0x80000000U && b == -1)\n\t\tres = 0, rem = 0;",
    "new": "\telse if (a == (int32_t)0x80000000U && b == -1)\n\t\tres = a, rem = 0;",
    "why": "/* #mipsdivwrap: return wrapped quotient INT_MIN instead of 0 for div */"
  },
  {
    "file": "src/cpus/cpu_mips_instr.c",
    "old": "\telse if (a == (int64_t)0x8000000000000000ULL && b == -1)\n\t\tres = 0;",
    "new": "\telse if (a == (int64_t)0x8000000000000000ULL && b == -1)\n\t\tres = a;",
    "why": "/* #mipsdivwrap: return wrapped quotient INT_MIN for ddiv (rem naturally evaluates to 0) */"
  }
]
```

## The review of that draft (it can be WRONG -- judge each point against the code above)

```text
FIXREVIEW_MIPSDIVWRAP: DEFECT, 3 FINDINGS
1. The diff successfully addresses the wrong-result defect described in the issue for both `X(div)` and `X(ddiv)`, accurately setting the quotient to `INT_MIN` instead of `0`.
2. CONTROL FLOW: No added `return`, `goto`, `break`, or early exit skips the common tail. The code safely falls through to write the updated `res` and `rem` variables into the CPU state.
3. RETURN VALUE: No path returns something different (both functions are `void`). The implied result is correctly written directly to the guest-visible `cpu->cd.mips.lo` and `hi` registers.
4. The fix introduces a new crash-on-malformed-input defect (Undefined Behavior) in `X(ddiv)`. Because it only sets `res = a` on line 1865 and does not skip the common tail calculation, line 1869 unconditionally evaluates `rem = a - b*res`. When `b = -1` and `res = INT64_MIN`, `b*res` triggers signed integer overflow. This will crash UBSan/hardened builds. `X(div)` safely avoids this by calculating `rem` inside the branches.
5. The new comments violate house idioms; they use `#CHERI PR#1:` instead of the required numeric `/* #NNN: ... */` tag format.
src/cpus/cpu_mips_instr.c:1869, DEFECT, rem = (b == -1) ? 0 : a - b * res;
src/cpus/cpu_mips_instr.c:1841, STYLE, /* #1: INT_MIN / -1 wrapped quotient is INT_MIN, rem 0 */
src/cpus/cpu_mips_instr.c:1866, STYLE, /* #1: INT_MIN / -1 wrapped quotient is INT_MIN, rem 0 */
FIXREVIEW_MIPSDIVWRAP: DEFECT, 3 FINDINGS
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

End with two lines: `REVISION_MIPSDIVWRAP: <a> ACCEPTED, <r> REJECTED` and `FIXDRAFT_MIPSDIVWRAP: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
