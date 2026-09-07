# AUDIT (read-only) — index-guard asymmetry in `dev_sgi_re.c`: which bounds check only one side?

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

**Check the premises, not just the derivations.** Where I state something as fact, ask whether it is
true. A seat that re-derives a premise from something this brief did NOT give it is worth more than
one that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.** There are three pristine-2021-upstream copies of
GXemul under the project root. They are NOT this fork.

**SCOPE YOUR READING TO `GXEMUL-SEC/src/` AND `GXEMUL-SEC/regress/*.py`.** Do not read
`GXEMUL-SEC/regress/artifacts/` or `GXEMUL-SEC/tools/pipeline/ledger.json`.

**Where this brief states an ARITHMETIC claim — an index range, a bound — ENUMERATE it rather than
reasoning about it.** Walk the values.

**VERDICT LINE FIRST**, so your answer survives truncation.

---

## The pattern to look for

`dev_sgi_re.c` indexes several fixed-size arrays with values derived from device registers. One
known site checks only the upper bound:

    case 4: tile_nr = x >> 12;
            if (tile_nr >= 32)      /* upper bound only */
                    return;
            ... d->re_linear_a[tile_nr] ...

`tile_nr` is `int` and `x` is a signed coordinate, so a negative `x` yields a negative `tile_nr`,
which passes a `>= 32` test. **That one is already known and is not the question.**

## The question

**Q1 — which OTHER array indexes in this file are bounded on one side only?** Enumerate them.
For each, give: the array and its declared size, the expression that produces the index, the guard
if any, and whether the index's type and provenance permit a value below zero or above the bound.

The arrays worth checking include `re_tlb_a`, `re_tlb_b`, `re_tlb_c`, `re_tex`, `re_linear_a`,
`re_linear_b`, `de_reg`, `mte_reg`, and any local array indexed by a register-derived value. **Do
not limit yourself to that list** — it is what I noticed, not a census.

**Q2 — for each index, is the arithmetic itself safe?** Several are shifts or divisions of a
coordinate. A right shift of a negative signed value, a division that rounds toward zero, and a
mask that assumes non-negative input all behave differently from the obvious reading. **Say where
the expression, rather than the guard, is what admits an out-of-range value.**

**Q3 — where a guard exists, does it constrain the value actually used?** A guard on one variable
followed by indexing with a different expression is a common shape. Point out any case where the
checked quantity and the indexing quantity differ.

**Q4 — which of these are guest-influenced at all?** Some indexes derive from registers the guest
writes; others from internal state. I am interested in the difference, since it separates a
robustness defect from a correctness one.

## What I am not asking

Do not write a fix, a test, or a program. Do not describe how a guest would reach any of these — I
want the code read and the asymmetries named, nothing more.

**If, while verifying a claim, you found something ELSE — say so.**
