# armbfiwidth -- apply `#510`'s repair to the third site, and check that it is the right one

## 0. READING SCOPE

`GXEMUL-SEC/src/cpus/cpu_arm_instr.c` -- the `ubfx`, `sbfx` and `bfi` handlers and their decoder
arms. Please avoid `regress/artifacts/` and `tools/pipeline/ledger.json`.

Tree: `GXEMUL-SEC/src/`. Ignore the pristine 2021 `src/` at the project root -- it will disagree by
hundreds of lines.

**This is a C-semantics and code-consistency review.** Nothing here needs a guest sequence.

## 1. THE SITUATION

`#510` repaired an undefined shift in TWO handlers and left a third. The repaired form is:

    uint32_t mask = (width == 32) ? 0xffffffffU : ((1U << width) - 1);

`X(bfi)`, about fifty lines below the second repair, still reads:

    uint32_t mask = (1 << width) - 1;

with `int width = msb - lsb + 1;` and `msb`, `lsb` each decoded independently as 0..31.

## 2. SETTLED PREMISES -- re-derived by enumeration, not asserted

Over all **1024** encodable `(msb, lsb)` pairs:

    width < 0     465   UNDEFINED  (negative shift count)
    width == 0     31   DEFINED    -- 1 << 0 is 1; mask becomes 0
    width 1..30   525   DEFINED
    width == 31     2   UNDEFINED  (1 is `int`; 2^31 not representable -- signed overflow)
    width == 32     1   UNDEFINED  (count >= width of the promoted type)
    ------------------
    UNDEFINED     468

The 496 pairs with `msb < lsb` (architecturally invalid field ordering) OVERLAP this set by 465 --
they are not disjoint populations. **You corrected an earlier version of this row that said 499;
check the 468 too.**

## 3. QUESTIONS -- VERDICT LINE FIRST

**Please do not simply ratify.** You have refuted premises of mine on four briefs tonight. **Check
the premises, not just the derivations.**

**Q1. Quote all three sites** as they stand, and confirm the two repaired ones use the form above
and the third does not.

**Q2. Does `#510`'s form actually cover `X(bfi)`'s domain?** This is the load-bearing question.
That form special-cases `width == 32` -- but `bfi`'s width can be **negative** and can be **31**,
and I do not believe `ubfx`/`sbfx` can produce either. **If their decoders constrain width to
1..32, then `#510`'s repair is correct THERE and insufficient HERE**, and transferring it verbatim
would leave 467 of the 468 undefined pairs undefined. Derive each handler's width domain from its
own decoder arm and say whether the three domains differ.

**Q3. What SHOULD `bfi` do for `width <= 0`?** The architecture presumably leaves `msb < lsb`
UNPREDICTABLE. **If you cannot establish that from a manual present in this tree, say so** --
`_scratchpad/` holds sixteen PDFs and BFI/BFC are in none of them, as you established on the
`armbfcdecode` brief. An honest "the architecture is not locally citable, so pick a defined
behaviour and document it as a choice" is the answer I want if that is the case; this project has
shipped model-sourced page citations before and is trying not to again.

**Q4. Give the smallest repair that makes every one of the 1024 pairs defined**, in the style of the
two repaired siblings so it reads as one family. State what it does for each of the four domains
above, and whether it changes behaviour for any pair that is currently DEFINED -- **that last part
matters more than the fix**, because a repair that alters the 525 well-defined widths is a
behavioural change wearing a UB-fix's clothes.

**Q5. What ORACLE distinguishes fixed from unfixed?** Not a guest sequence -- name the observable.
Note that undefined behaviour may compile to something that *looks* right on this host, so a row
asserting a particular wrong value is pinning the compiler, not the code. Is a UBSan build the only
honest detector here? If so, say it -- `build-asan/` exists and is currently clean and freshly
built.

**Q6. Is `armbfcdecode` entangled with this?** That row says the same handler dispatches BFC (source
field 15) as BFI. **You ruled last pass that they are two rounds.** Does anything in the repair you
propose here make that separation harder or easier?
