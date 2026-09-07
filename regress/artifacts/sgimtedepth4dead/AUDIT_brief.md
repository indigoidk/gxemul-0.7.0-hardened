# AUDIT (read-only) — `do_mte_transfer()` in `dev_sgi_re.c`, whole function

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

**Check the premises, not just the derivations.** Where I state something as fact, ask whether it is
true. A seat that re-derives a premise from something this brief did NOT give it is worth more than
one that agrees. **A recent panel had seven of nine seats confirm a premise stated wrongly.**

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.** There are three pristine-2021-upstream copies of
GXemul under the project root. They are NOT this fork.

**SCOPE YOUR READING TO `GXEMUL-SEC/src/` AND `GXEMUL-SEC/regress/*.py`.** Do not read
`GXEMUL-SEC/regress/artifacts/` or `GXEMUL-SEC/tools/pipeline/ledger.json`.

**Where this brief states an ARITHMETIC claim — a value range, a set of reachable encodings —
ENUMERATE it rather than reasoning about it.** Walk the values.

**VERDICT LINE FIRST**, so your answer survives truncation.

---

## Why this function, now

`do_mte_transfer()` models the SGI CRIME memory-transfer engine. It has just been implicated in a
defect chain that nobody had connected, so the function deserves reading as a whole rather than at
the one site.

**The established chain, verified — treat it as context, and correct it if it is wrong:**

    src_mode = (src_tlb << 10) + (((mode & MTE_MODE_DEPTH_MASK) >> MTE_DEPTH_SHIFT) << 8);
    dst_mode = (dst_tlb << 10) + (((mode & MTE_MODE_DEPTH_MASK) >> MTE_DEPTH_SHIFT) << 8);
    if (depth == 4) {                     /* depth = 8 << field, so 8/16/32/64 -- never 4 */
            src_mode |= DE_MODE_TYPE_RGBA;
            dst_mode |= DE_MODE_TYPE_RGBA;
    }

The constructed modes carry no colour bits, so the colour type is `0x00` (CI). The only thing that
would make them RGBA is that condition, which cannot be true. So the transfer always runs CI — and
CI's pixel-write arm assigns only `buf[0]` while the transfer length is `bufdepth` bytes, which is
2 or 4 at the documented `MTE_DEPTH_16` / `MTE_DEPTH_32`.

## The questions

**Q1 — is that chain right?** In particular: is the colour type really `0x00` for every reachable
mode, and does any other path set colour bits on these two locals before use?

**Q2 — read the WHOLE function and say what else is wrong.** It is roughly 200 lines and does
address arithmetic, stride handling, a fill path with a `zerobuf`, and a per-pixel loop. I have
looked at three things in it and found two defects, which is a poor ratio to stop on. **Specifically
worth checking:**

* the `zerobuf` fill path — its length arithmetic against `sizeof(zerobuf)`;
* the stride and step handling, including negative or zero steps;
* whether `src0`/`src1`/`dst0`/`dst1` bounds are checked before use, and against what;
* anything that reads a field the guest supplies without constraining it.

**Q3 — what does the function do that its comments claim it does not, or vice versa?** Two defects
in a neighbouring handler tonight were each an assignment contradicting a comment directly above it,
and this file has a `TODO... probably not correct!` habit. **A comment asserting a property the code
does not have is a defect in this project's terms, not a style issue.**

**Q4 — if `if (depth == 4)` were corrected, what would change?** I believe correcting it alone would
switch the path to RGBA, which fills four bytes — masking the byte-leak at depth 32 while leaving
depth 16 (two bytes, four filled) and every other caller untouched. **Is that right?** It decides
whether the two defects can share a round or must be sequenced.

## What I am not asking

Do not write a fix, a test, or a program. I want the function read and what is wrong in it named.

**If, while verifying a claim, you found something ELSE — say so.** Several of tonight's best
findings arrived that way, including the chain above, which came out of a brief about a different
defect entirely.
