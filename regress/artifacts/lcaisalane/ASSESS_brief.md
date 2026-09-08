# lcaisalane -- three claimed defects in eleven lines of `DEVICE_ACCESS(lca_isa)`

## 0. SCOPE

Read `GXEMUL-SEC/src/devices/dev_lca.c` -- the `lca_isa` access function and whatever else in that
file it depends on. Please avoid `regress/artifacts/` and `tools/pipeline/ledger.json`.

Tree: `GXEMUL-SEC/src/`. Ignore the pristine 2021 `src/` at the project root.

*** NO MUTANT, NO EVASION, NO GUEST SEQUENCE IS WANTED. *** This is a source review of code that
exists. (You refused two briefs of mine tonight that asked for an edit defeating a detector, and for
a guest sequence reaching a defect. Nothing here does either.)

## 1. THE FILED CLAIM -- a claim, not a premise

> *"`dev_lca.c` `DEVICE_ACCESS(lca_isa)`: THREE defects in eleven lines -- an off-by-one guard,
> [and two others]."*

**I have not verified any of it**, and the row's own summary is truncated in my notes, so I am
deliberately NOT telling you what the other two are supposed to be. **Find what is there.**

**Please do not simply ratify** -- and equally, do not manufacture three findings because the claim
says three. If there are two, or five, or none, say that.

## 2. QUESTIONS -- VERDICT LINE FIRST

**Q1. Read the function and enumerate what is actually wrong**, if anything. For each: quote the
line, say what it does, and say what it should do.

**Q2. For each finding, which option-set member is the right disposition?**
**1 DELETE · 2 DECLINE (silent) · 3 DECLINE + LATCHED ANNOUNCE · 4 ACCEPT · 5 FAULT · 6 BACKED
ACCEPT · 7 IMPLEMENT.**
*** CAUTION: member 5 FAULT is NOT universally available. *** It works where `memory_rw` dispatches
a CPU exception on a failed device access -- MIPS and M88K. **This is an Alpha machine**, and this
project has established there is no Alpha equivalent and no MM-fault dispatch at all
(`ALPHA_KENTRY_MM` has definitions and no consumers). If FAULT is your recommendation, say that it
obliges building delivery first.

**Q3. GREP THE FORK FOR THE IDIOM** before reasoning from first principles. How do the sibling
handlers in this same file, and comparable ISA-bridge handlers elsewhere, treat the same situation?
A sibling that already does the right thing is worth more than an argument.

**Q4. Is this ONE round or several?** The project's rule: a round takes ONE site; a second joins only
if it is the same semantic class, covered by ONE fix design and ONE oracle, with no new oracle.
**More findings create more candidate rounds, never bigger rounds.**

**Q5. Severity for each, argued rather than asserted** -- and note that `dev_lca.c` already has
three rows held for adjudication (`lcabadval`, `lcaconfbus1kill`, `lcairqstubkill`). If any finding
here is really one of those wearing a different hat, say so; I would rather withdraw a duplicate
than file it.

**Q6. What observable would distinguish fixed from unfixed?** Name the channel. If the honest answer
is that nothing in-tree exercises this path, say so -- that caps the severity and makes it a
documented-only candidate.
