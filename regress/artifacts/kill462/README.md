# `#462` kill-table artifacts — READ THIS BEFORE CITING `table462.results`

Preserved evidence for round `#462`. The files here are **evidence and are not
edited**; this note corrects the record beside them rather than rewriting them,
which is the same discipline the oracle-correction rule imposes on a re-pinned
row.

## The `SCORE=` lines are sound. The `RED:` lines are NOT.

`table462.results` was produced by a driver whose reddened-row extractor used an
**unanchored `grep FAIL`**. Row `nodata stale`'s own DESCRIPTION contains the
string `FAILED-COMMAND`, so that row gets annotated `RED:` even when it passed —
including in the clean `base` section, which scored 58/58 and by construction has
no red row at all.

Measured 2026-08-25, with denominators, which is what makes it checkable:

    sections: 15      RED-annotated lines: 63
    of those 63 -- end in "ok" (phantom): 14      end in "FAIL" (genuine): 49

## *** THE PHANTOM IS IN 14 OF 15 SECTIONS, AND THE EXCEPTION IS THE POINT ***

`Mb1` is the one section where `nodata stale`'s line ends in `FAIL` — there the
row **genuinely failed**. Every other section's `nodata stale` line is a pass
mislabelled as a failure.

**So the blunt repair destroys a true positive.** A reader who concludes "ignore
all `nodata stale` lines" discards the single genuine kill of that row in the
whole table. The row is not untrustworthy; the *annotation* is, and only where
the row passed.

This is the project's own recorded class in a new shape: *when two checks
disagree, find out which one is broken — do not keep the one that agrees with
what you expected.* Here the contaminated extractor and the true result agree on
`Mb1` and disagree everywhere else, and the disagreement is the signal.

## What to trust

* **Trustworthy:** the `SCORE=GDROM_DEF_RESULT=n/58` lines — the probe's own
  result line, not the driver's post-hoc grep.
* **Trustworthy:** the diff hunks under each `=== Mn ===` header.
* **Contaminated:** the `RED:` lines, in the one direction described above.

## Correct extraction

    grep "^    RED:" table462.results | grep "FAIL$"

Anchoring on the trailing `FAIL` keeps `Mb1`'s genuine `nodata stale` kill and
drops the fourteen phantoms. Verified against the section-by-section counts above.

## Why this is recorded rather than fixed

This is the project's documented *"a pattern that matched nothing reports zero for
everything"* class in its mirror form: a pattern that matched too much reports a
failure that never happened. The carrier already records the incident. What it did
not record is that **the preserved artifact still carries the bad annotations**, so
a future reader re-derives the wrong answer from evidence that looks
authoritative. That gap is what this file closes.

The scores themselves survived because they were written into the round's records
at the time — the "transcription outlived the evidence" shape the names-its-log
rule exists to prevent, reached from the opposite direction.
