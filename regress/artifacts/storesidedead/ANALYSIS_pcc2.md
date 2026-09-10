# ONE FILE: which rows in `regress/pcc2_width_probe.py` would pass if their action never ran?

**Answer in prose. Do not propose a code change, do not write a test, do not construct any input
sequence.** Per-row assessment only; I will do the repairs.

## §B0 — READ EXACTLY ONE FILE

    regress/pcc2_width_probe.py

**Nothing else.** Not the device, not the other probes, not `CHANGELOG.md`, not
`tools/pipeline/ledger.json`, not `OUTSTANDING_BUGS.md`, not `_scratchpad/`.

*Two previous firings of this question died without a verdict — one scoped as `regress/*.py`
(2.4 MB), one scoped to six files (325 KB). **The scope was the defect both times, not the
question.** This file holds 25 of the 90 candidate rows in the tree, which is the largest single
share, so it is worth answering alone and answering completely.*

## §C — THE MEMBERSHIP TEST IS SETTLED.  It is yours, from an earlier firing.

> *"A row belongs in this census if its own oracle can pass when the tested action is OMITTED; it
> is already paired only if another check ON THAT SAME ACCESS requires positive evidence AFTER the
> action."*

Also yours, and taken as given — do not re-derive any of it:

* *"a label such as `survives` or `unchanged` does not decide membership"* — judge the ORACLE;
* *"paired means another assertion consumes observations from the SAME emulator session; a
  requested print without an assertion does not qualify"*;
* **the fourth guise**: *"exactly one message across two or more accesses" — the FIRST access can
  supply the one message even if a LATER access never runs.* This one matters most here, because
  a count row LOOKS positive and is still satisfied by a skipped action. **So when you judge
  pairing, check the ORDER: the positive evidence must be retired AFTER the action under test.**

## §D — THE QUESTIONS

**Q1. The per-row table.** Every `row(...)` in the file: its label, what its oracle actually
tests, and VACUOUS-ALONE or ALREADY-PAIRED. Where a loop emits several labelled rows from one
call site, name the rows it produces rather than the call site.

**Q2. For each vacuous-alone row, what positive post-action observable is available at that
site?** In words. If none exists, say so — that changes the disposition from *repair* to
*disclose*, which is a real answer and I would rather have it than a strained suggestion.

**Q3. Which ones actually MATTER?** Rank them. I would rather repair three rows that guard
something real than twenty that guard nothing, and you are better placed than I am to tell which
is which after reading the whole file.

**Q4. Is any row vacuous in a way a MUTANT would expose but a reading would not?** That decides
whether this becomes a measured round or a records round, and it is the one thing I cannot settle
by reading.
