# `#519` -- MY OWN PREMISES S4 AND S6 WERE WRONG ABOUT THE MUTANTS, AND THE CORRECTION MAKES THE ROUND WORSE, NOT BETTER

**Source:** `codex_corner_20260910.txt` (GPT-6 Astra at max, 7,447 bytes, ZERO cyber flags, 13m18s).
Written up here the moment it landed, before any row is designed on the old reading.

## WHAT I HAD WRONG

The closure brief asserted, as settled premise S4, that `M13_widthdecline` and `M14_lineardecline` are
**ACCEPT-SIDE** breaches -- mutants that make the helper *decline writes it should accept* -- and that they
escape because every existing decline row already satisfies the added condition.

**That is backwards.** From the actual mutator
(`killtable_20260910/mut519b.py`, read rather than remembered):

> *"The actual mutator replaces unconditional `ok = 0` **inside the unsupported default** with a
> conditional decline. Those mutants wrongly **PERMIT unsupported writes**."*

So the mutants do not over-decline. They **under-decline**: at any cell where the added condition is
false, the unsupported colour type is let through and the store below executes.

## WHY THE CORRECTED READING IS THE MORE ALARMING ONE

The `#519` fix DELETED the `random()` fill. So a mutant that permits the store no longer writes
host-PRNG bytes -- **it writes whatever is in `buf`, which at that point is UNINITIALISED STACK**:

> *"Their permitted stores consume uninitialized `buf`; the random fills were deleted."*

That is the same class of defect the round exists to close (unasked-for bytes into guest memory) arriving
by a new route, and it is arguably worse than what shipped: `random()` at least produced values with no
relationship to host memory contents. **`buf` is `uint8_t buf[8]` in the enclosing function**, so its
contents are whatever the previous call left there. It also ties this round to `sgirebufuninit`, which is
already a separate filed row -- the two are now the same store.

## WHAT SURVIVES, AND WHAT DOES NOT

* **The field arithmetic SURVIVES, confirmed independently.** Type mask `0x00f0`, depth mask `0x0300`,
  TLB mask `0x1c00` do not overlap; `0x00f0` really is `type=0xf0` (YCRCB) with `bufdepth=1` and
  `linear=false`.
* **The corner ROW still works**, because a cell where neither added condition holds is exactly where an
  under-declining mutant lets the store through -- but it now reds for a DIFFERENT REASON than my brief
  said, and a row comment written from the old reading would have been a wrong record on arrival.
* **What does NOT survive is my claim that `0x00f0` is "the most realistic guest input".** codex:
  *"That establishes documented field encodings and helper reachability -- not that this particular
  combination is the most realistic driver input."* Correct: I inferred realism from documentedness.
* **AND ONE CORNER IS NOT ENOUGH.** Its verdict: *"One corner closes the three named predicates, not the
  complete store-guard class."* It prescribes **TLB_A/B/C x {CI8, RGB32, RGBA32, ABGR32, YCRCB8-first,
  YCRCB8-repeat} = 18 new readback cells in three sessions**, which is a real cost to weigh against my
  one-row plan.

## THE LESSON, and it is the one the premise-audit rule exists for

**I wrote the mutants' direction into the brief as a SETTLED PREMISE without re-reading the mutator.**
Had the brief merely asserted it, six packet-fed seats would have confirmed it -- that is the measured
behaviour of this panel. It was caught because the brief said, in its own question 1, *"re-derive S3 and
S6 from the source, not from this brief"*, and because the seat could open `mut519b.py`.

*A premise stated as a question costs one clause and converts a ratification into a test. This is the
third time in this project that clause has paid, and the first time it caught a claim about the round's
own instruments rather than about the code under test.*
