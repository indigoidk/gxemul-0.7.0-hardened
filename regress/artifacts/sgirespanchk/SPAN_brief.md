# AUDIT (read-only) — write SPANS in `dev_sgi_re.c`: does a bounded index guarantee a bounded access?

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

**Check the premises, not just the derivations.** Where I state something as fact, ask whether it is
true. A seat that re-derives a premise from something this brief did NOT give it is worth more than
one that agrees.

**A recent brief of mine stated a premise that was simply false — an index variable's type — and I
built four paragraphs of consequences on it before a seat read the declaration. Please read the
declarations.**

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.** There are three pristine-2021-upstream copies of
GXemul under the project root. They are NOT this fork; line numbers there differ by hundreds.

**SCOPE YOUR READING TO `GXEMUL-SEC/src/`.** Do not read `GXEMUL-SEC/regress/artifacts/` or
`GXEMUL-SEC/tools/pipeline/ledger.json`.

**Where this brief states an ARITHMETIC claim — an index range, a width, a bound — ENUMERATE it
rather than reasoning about it.** Walk the values.

**VERDICT LINE FIRST**, so your answer survives truncation.

---

## The distinction this brief is about

An index bound answers *where does an access start*. It does not answer *where does it finish*. An
array access of width `w` at index `i` into an array of `n` elements is in range only if
`i + w <= n`, and a guard of the form `if (i >= n) return;` establishes only the first half.

I am told — and I have not verified it — that several accesses in this file are multi-byte, with the
width chosen from a register-derived value rather than being a constant.

## The questions

**Q1 — enumerate the multi-byte accesses.** For each array in this file (`re_tlb_a`, `re_tlb_b`,
`re_tlb_c`, `re_tex`, `re_linear_a`, `re_linear_b`, and any others — that list is what I noticed, not
a census), give: the declared type and element count, every site that reads or writes it, whether the
access is single-element or spans several, and where the span width comes from.

**Q2 — for each multi-element access, is the END of the span bounded?** State the guard that bounds
it, or say plainly that none exists. Where the guard bounds only the start, say what the largest
reachable end offset is and whether it exceeds the array.

**Q3 — where the width or offset derives from a register, what values can it take?** I am interested
in the declared type and the writing path, not in whether a driver would choose such a value.

**Q4 — does any access depend on the CALLER for alignment or size?** If a function is safe only
because its callers happen to pass aligned or bounded arguments, name the function, name the property
it relies on, and name the callers you checked. **An unchecked assumption that happens to hold is a
different thing from a checked one, and I want the difference stated.**

## What I am not asking

Do not write a fix, a test, or a program. Do not describe how a guest would reach any of these — I
want the code read and the spans characterised, nothing more.

**If, while verifying a claim, you found something ELSE — say so.**
