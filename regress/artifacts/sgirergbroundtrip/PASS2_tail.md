
---

## The questions

**Q1 — THE PREMISE AUDIT.** Every claim in §C is stated as settled. **Which of them is wrong?** The
one I most want challenged is S2: the scanout warrant. It rests on a 32-bit path in `dev_sgi_gbe.c`
whose `color_mode` is a **GBE** register (`CRMFB_MODE_TYP_*`), while the arm I edited switches on a
**DE** register (`DE_MODE_TYPE_*`). Those are different registers. **Does the argument actually
close, or does it need a guest to have programmed both consistently — and if so, is that an
assumption I have smuggled in?**

**Q2 — WHAT IS THE SMALLEST EDIT THAT BREAKS THIS AND STILL PASSES?** Name the row you expect to stay
green. I am specifically after the clause-(d) family: predicates the fix depends on, weakened to the
least-restrictive form that still reads like the corrected code. **Table 2 already covers the WIDTH
axis in both directions** (`M6_cond`, `M7_cond8`) — so tell me which *other* axis is unpinned. The
guarded body reads `buf[0..2]`, `bufdepth`, `color_mode`, `tileptr` and `ofs`; the guard reads
`mode & DE_MODE_TYPE_MASK`.

**Q3 — THE ASK-AGAIN.** The table is clean. **Give me one more mutant.** This is capped at a single
ask per detector per round, and anything found is disposed of individually under L1–L4 — a floor
breach among the findings is still L2 and still repaired in-round, because the cap counts ASKS and
never FINDINGS.

**Q4 — IS THE DETECTOR'S CONTRACT HONEST?** It claims to catch edits that move RGB channel bytes, at
transfer widths 4 and 8, in both the GET and PUT directions. **What does it NOT catch that a reader
would assume it does?** Clause (e) says a detector that names its limits is falsifiable and one
claiming completeness is not — so I would rather add a disclosure than discover a gap.

**Q5 — THE ROW SET.** Eight rows: three controls (`live`, `devsig`, `copy lin_a`), and five on the
defect (`rgb chan`, `rgb not corrupt`, `rgb alive`, `rgb samemode`, `rgb depth64`). **Is any of them
vacuous — able to stay green under the mutant it exists to catch?** For each, its channel is the
destination word read back through a guest load, except `rgb alive` (process survival) and `devsig`
(a device register value RAM would not produce).

**Q6 — THE GATE BLOCK.** It greps row names with **two** spaces, because the probe pads with `%-16s`
plus one explicit space and the longest name is 15 characters — one character of margin. **Is there a
failure mode in that block I have not defended against?** The two known ones are a name matching two
rows (one-space form) and a name ≥ 16 characters making the pattern unsatisfiable so the check goes
silently green.

## What I am not asking

Do not run anything and do not rewrite the fix. This is a review of a diff that is already measured.

**If, while verifying a claim, you found something ELSE — say so.**
