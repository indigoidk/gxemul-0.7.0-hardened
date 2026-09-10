# A census question: regression rows whose oracle passes when the tested action never happened

**Answer in prose. Do not propose a code change, do not write a test, and do not construct any input
sequence.** I want the census and the per-row assessment; I will decide the repairs.

## Read only these files

    regress/*.py     -- the probe files only
    regress/lib.sh   -- only if a probe's helper is defined there

Do not read `CHANGELOG.md`, `tools/pipeline/ledger.json`, `OUTSTANDING_BUGS.md`, or anything under
`_scratchpad/`.

## Please do not simply ratify

**Before you count anything, say what you think makes a row a member of this class** — and check
that your pattern tests that property rather than a correlate of it. This project has been bitten
three times in one day by censuses that keyed on a NAME (a variable's spelling, a row's label, a
line's leading characters) when the defining property was something else. **Report the per-file
breakdown, not just a total**, because a disagreement between two counting methods is the only cheap
signal that one of them is measuring the wrong thing.

**VERDICT LINE FIRST.**

## The class, stated concretely from a case I hit today

A row asserted "the alias write was REFUSED" by checking that a particular diagnostic string was
ABSENT from the session output. It scored GREEN on a build where the host had already died before
that write ever executed. **An absence-of-evidence oracle cannot distinguish "the action ran and
correctly produced nothing" from "the action never ran at all."**

The repair was to bind the row to a POSITIVE observable retired AFTER the action — something that
can only appear if the action executed — so that "never ran" renders differently from "ran and was
refused".

The same shape appears in at least three guises, and I suspect there are more:

* **absence-of-message**: the row wants a string NOT to appear;
* **no-effect**: the row wants some state to be UNCHANGED after a store;
* **survival**: the row wants the process to still be alive, or to have exited 0.

All three are satisfied by the action never happening.

## The questions

**Q1. Define the class precisely, then census it.** Which rows across `regress/*.py` have an oracle
that a *skipped action* would satisfy? Give the per-file breakdown and name the rows.

**Q2. Split the census into VACUOUS-ALONE and ALREADY-PAIRED.** Some of these rows will sit beside a
second row on the same access that supplies a positive observable — a value read back, a counter, a
later checkpoint. Those need nothing. **This split is the whole answer; a single total would be
misleading in both directions.**

**Q3. For each vacuous-alone row, what positive observable is AVAILABLE at that site?** Describe it
in words — a value the device returns, a message a neighbouring path prints, a subsequent access
that could only run if the first completed. If no such observable exists at some site, say so; that
is a real answer and it changes the disposition from "repair" to "disclose".

**Q4. Is there a probe in this tree that handles this WELL?** Name it and describe its idiom
precisely. An in-tree precedent is worth far more than a general principle, and if one exists the
repair everywhere else is to copy it.

**Q5. Rank the findings by how much a repair would buy.** I would rather fix three rows that guard
something real than twenty that guard nothing. Say which sites you think matter and why.
