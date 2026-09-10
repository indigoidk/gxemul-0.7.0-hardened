# Which of these rows would still pass if the action they test never happened?

**Answer in prose. Do not propose a code change, do not write a test, and do not construct any input
sequence.** I want the per-row assessment; I will do the repairs.

## §B0 — READ ONLY THESE SIX FILES.  The list is derived, not guessed.

    regress/pcc2_width_probe.py        (25 candidate rows)
    regress/pcc2_default_probe.py      ( 9)
    regress/sgi_de_width_probe.py      ( 7)
    regress/asic_badaddr_probe.py      ( 6)
    regress/gdrom_default_probe.py     ( 6)
    regress/arm_flags_probe.py         ( 3)

Derived by matching the `want` ARGUMENT — not the row name — against absence/zero/no-change values
across `regress/*.py`: **90 such rows in 19 files, of which these six hold 56.** The other thirteen
files hold 1–5 each and are out of scope for this pass.

**Do NOT read `CHANGELOG.md`, `tools/pipeline/ledger.json`, `OUTSTANDING_BUGS.md`, or anything under
`_scratchpad/`.** A previous firing of this question was scoped as `regress/*.py` — which is not a
bound — and died at 2.4 MB without producing its table. If you find yourself needing a fact that
lives only outside these six files, say so and stop.

## §C — THE MEMBERSHIP TEST IS ALREADY SETTLED.  It is yours, from the previous firing.

> *"A row belongs in this census if its own oracle can pass when the tested action is OMITTED; it is
> already paired only if another check ON THAT SAME ACCESS requires positive evidence AFTER the
> action."*

You also established, and I am taking as given: *"a label such as `survives` or `unchanged` does not
decide membership"*, and *"paired means another assertion consumes observations from the SAME
emulator session — a requested print without an assertion does not qualify."*

**Do not re-derive these. Spend the budget on the per-row table.**

## §C2 — A FOURTH GUISE YOU NAMED, which I want applied throughout

> *"exactly one message across two or more accesses" — the FIRST access can supply the one message
> even if a LATER access never runs.*

This one is subtle because the row looks POSITIVE: it asserts a message is *present*, and is still
satisfied by a skipped action, because the evidence was produced before the skip. **It defeats the
obvious repair for the whole class** — "pair the negative oracle with a positive one" — since a
positive oracle sited BEFORE the action under test is worth nothing.

**So when you judge pairing, check the ORDER: the positive evidence must be retired AFTER the action,
not merely present in the same session.**

## §D — THE QUESTIONS

**Q1. The per-row table.** For each of the six files: which rows are VACUOUS-ALONE, which are
ALREADY-PAIRED, and for the paired ones, what supplies the positive post-action evidence. Name rows
as they are labelled in the source.

**Q2. Two leads of yours I could not verify — please settle them.** You reported (a) *"the CMMU probe
prints a row labelled VALUE, but its return path grades only survival"* and (b) *"some ARM flag rows
reduce the untouched output sentinel to a single bit that matches the expected answer."* I could not
identify the CMMU probe from your description and it is not in the six above — **name the file** if
it is one of them, or say it is elsewhere and I will scope a separate pass. For (b),
`arm_flags_probe.py` is included; please point at the specific rows.

**Q3. For each vacuous-alone row, what positive post-action observable is AVAILABLE at that site?**
Describe it in words. If none exists, say so — that changes the disposition from *repair* to
*disclose*, which is a real answer.

**Q4. Rank by what a repair would BUY.** I would rather fix three rows that guard something real than
twenty that guard nothing. Which sites actually matter, and why?

**Q5. Is any of these rows vacuous in a way that a MUTANT would expose but a reading would not?**
That is the question I cannot answer from the source, and it decides whether this becomes a
measured round or a records round.
