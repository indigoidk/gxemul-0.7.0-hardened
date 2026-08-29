# CHANNEL-CHECK PREDICTION on `accept sil` — written BEFORE the measuring seat's result

**Written 2026-08-29 ~05:40, main loop, from READING ONLY.  The measuring seat has
`M_growA` built (`/tmp/gxr2m_bins/M_growA`, 05:03) and has not yet scored it.**

The order is the point.  This project's oracle-correction rule turns on a mechanical
discriminator — *a number written before the run that produces it cannot be told from a number
fitted to the answer*.  So this is written first and scored later, and if it is wrong that is
recorded here rather than quietly dropped.

## THE CLAIM THIS TESTS

The round's own record says **`accept sil` has never been scored by ANY mutant.**  The
pre-table CHANNEL check says a row whose named channel cannot vary under its named mutant is
VACUOUS BY CONSTRUCTION, *and that this is knowable at writing time, before any table runs.*
So: is `accept sil` vacuous, or merely unscored so far?

## THE ROWS, AS SHIPPED

```python
t, alive, how = session(store16(GDROM_CNTLO, 0x98, A) + store16(GDROM_CNTHI, 0x01, A)
                        + packet(cmd(0x30, 0x20, 0x0001), A))
row("acceptA",    "%d" % len(HUH.findall(t)),      "1", "the LEGAL format still enters the arm")
row("accept sil", "%d" % len(FMT_DECL.findall(t)), "0", "and it is not declined")
```

The session sends data format **0x20 — the LEGAL one**.  The product guard is
`} else if (d->cmd[1] != 0x20) {`.

## PREDICTION 1 — `accept sil` IS NOT VACUOUS.  M_growA should REDDEN it.

`M_growA` is `!= 0x20` -> `!= 0x21`.  Under it a legal 0x20 satisfies the guard, enters the
decline arm, and — in a FRESH session with the latch clear — **emits the decline once**.  So
`FMT_DECL` goes 0 -> 1 against a want of 0.

**PREDICTED: `accept sil` RED under M_growA.**  If it comes back GREEN my reading is wrong and
the row is worse than unscored.

## PREDICTION 2 — and this is the one worth measuring: it is NOT INDEPENDENTLY killed

Under that same mutant the arm `break`s before `sector_nr`, so the legal path never completes
and `HUH` goes 1 -> 0.  **PREDICTED: `acceptA` RED under M_growA too.**

If both fall to the same mutant and to no other, then **no enumerated mutant DISTINGUISHES
them**, and the row-demand rule is explicit that rows are owed per enumerated mutant, never per
refusing state — *"two states no enumerated mutant distinguishes collapse into one row."*  On
that reading `accept sil` is surplus.

## THE COUNTER-ARGUMENT, stated now so it is not invented afterwards

The two rows read **different channels**: `acceptA` asserts the legal path COMPLETES; `accept
sil` asserts NO DECLINE IS EMITTED.  A future edit could break the second without the first —
adding a diagnostic on the legal path that does not alter control flow leaves `HUH` at 1 and
`FMT_DECL` at 1.  No mutant in the current table has that shape, which is exactly why the
question is *"should such a mutant be enumerated?"* rather than *"is the row dead?"*

**I am NOT proposing to add one.**  A filter may reject or repair a row; it may never demand a
new one — that is the stop condition that keeps the CHANNEL check from growing row count
without bound.

## HOW TO SCORE THIS

When `probe_M_growA.log` lands, read the `acceptA` and `accept sil` rows:

| outcome | what it means |
|---|---|
| both RED | Prediction 1 and 2 both hold.  `accept sil` is killed but not independently — a KEEP/COLLAPSE judgement, not a floor breach |
| `accept sil` GREEN, `acceptA` RED | Prediction 1 is WRONG.  The row is vacuous under its own named mutant — clause-(d)-adjacent, and it is the sole carrier of the no-decline claim |
| both GREEN | the mutant is mis-built or the target is dead — a RESULT, not noise; do not re-aim it until which of the three explanations applies has been measured |

*Nothing here licenses an edit.  It is a reading, recorded in the order that makes it
falsifiable.*

---

# SCORED, 2026-08-29 — against `probe_M_growA.log` (13/20, 7 failing rows)

**BOTH PREDICTIONS CORRECT, and the measured values match the derived ones exactly.**

| row | got | want | predicted | outcome |
|---|---|---|---|---|
| `acceptA` | 0 | 1 | RED | **RED — P2 correct** |
| `accept sil` | 1 | 0 | RED | **RED — P1 correct** |

The mechanism is the one derived from reading, not a coincidence of colour: `M_growA` widens
`!= 0x20` to `!= 0x21`, so the accept session's LEGAL 0x20 now satisfies the guard, enters the
decline arm, and `break`s. `HUH` therefore disappears (0 against a want of 1) and a decline is
emitted (1 against a want of 0). Both halves moved for the predicted reason.

## WHAT THIS SETTLES

**`accept sil` IS NOT VACUOUS.** The round's note that it *"has never been scored by ANY
mutant"* is now false: `M_growA` scores it, and reddens it. The CHANNEL check's claim — that a
row's channel-under-its-mutant is knowable at WRITING time, before any table runs — held here.

**AND IT IS NOT INDEPENDENTLY KILLED.** `acceptA` falls to the same mutant, and no mutant in
the table distinguishes them. Under the row-demand rule (*rows are owed per enumerated mutant,
never per refusing state*) that makes `accept sil` a candidate for collapse.

**NO ROW IS PROPOSED AND NONE IS REMOVED.** The two read genuinely different channels —
`acceptA` asserts the legal path COMPLETES, `accept sil` asserts NO DECLINE IS EMITTED — and a
future edit adding a diagnostic on the legal path without altering control flow would break the
second and not the first. That is a KEEP/COLLAPSE judgement for the round to make, not a floor
breach. **A filter may reject or repair a row; it may never demand a new one** — so the
"enumerate a mutant that distinguishes them" move is deliberately not made.

*Recorded because the prediction was written BEFORE the run, and a prediction nobody scores is
just prose. Five other rows also fell to `M_growA` — `fmt says`, `fmt x2`, `latch cond`,
`both sites`, `crossbit` — which was not predicted and is not claimed as one.*

---

# *** MY CONCLUSION WAS REFUTED BY THE COMPLETED TABLE.  The two PREDICTIONS held; the
# INFERENCE I drew from them did not.  2026-08-29, after `Md_hoistannounce` landed. ***

I wrote, above: *"no mutant in the table distinguishes them ... that makes `accept sil` a
candidate for collapse."*  **False.**  `Md_hoistannounce` distinguishes them exactly:

    MUTANT              acceptA    accept sil
    M_growA             RED        RED
    Md_hoistannounce    green      RED        <-- an enumerated mutant SEPARATES them
    (all ten others)    green      green

**So `accept sil` IS independently killed, and the KEEP/COLLAPSE question is settled: KEEP.**
Hoisting the announce out of the latch leaves the legal path completing — `acceptA` stays green
— while emitting a decline the legal session should never see, which is precisely the channel
`accept sil` reads and `acceptA` cannot.

## WHY I GOT IT WRONG, WHICH IS THE PART WORTH KEEPING

**I generalised about the WHOLE TABLE from ONE mutant.**  When I wrote it, `M_growA` was the
only mutant that had touched either row; `Md_hoistannounce` had not yet been scored.  Saying
*"no mutant in the table distinguishes them"* was a claim about mutants that had not run.

That is this project's frozen-number class in its inference form: **not a number written before
its run, but a UNIVERSAL written before its population was complete.**  The score-claim rule
says a number names the artifact that produced it; the same discipline applies to a quantifier —
*"no mutant distinguishes them"* needed to name the table it was quantifying over, and the
honest form at the time was **"no mutant SCORED SO FAR distinguishes them, and four are
pending."**

**The restraint I argued for was still right, and for a better reason than I gave.**  I declined
to propose a mutant that would separate the two rows, on the ground that a filter may reject or
repair a row but never demand a new one.  The table then produced such a mutant anyway — from
the round's own clause-(d) enumeration, not from a filter reaching for one.  *The bound held and
the coverage arrived through the licensed channel, which is exactly how it is supposed to work.*
