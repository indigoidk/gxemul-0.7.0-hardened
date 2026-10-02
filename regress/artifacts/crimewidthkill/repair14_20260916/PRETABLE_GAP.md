# A PRETABLE COMPLETENESS GAP: one of fifteen legs has NO PREDICTION.  Found 2026-09-17, table 12.

    driver legs (kill529r14.sh LIST):  15
    legs with a prediction in PRETABLE.out: 14
    legs WITHOUT:                           1   -- **M1_gotolatch**

`grep -ci gotolatch PRETABLE.out` returns **0**.  The leg ran, scored **194/204** (ten reds), and there
is nothing in the pre-run block to check that number against.

## WHY THIS MATTERS RATHER THAN BEING TIDY-UP

The PRE-TABLE block is mandatory for any round shipping or extending a kill-table-backed detector, and
its stated content includes *per row, the mutant it kills and the observable that differs*.  A leg with
no predicted score and no named rows produces a number that cannot be wrong -- **whatever it scored, it
would have "matched"**.  That is this project's check-that-cannot-fail shape arriving through the
prediction side rather than the assertion side.

**An UNPREDICTED leg and a PREDICTED-AND-MATCHED leg must not read the same in the record**, which is
the same rule that makes an unrun check and an inapplicable one render differently.

## THE MITIGATION, stated so the finding is not inflated

`M1_gotolatch` is **well killed** -- 194/204, ten reds across ten distinct rows (`sh08b run`,
`sb08 msg`, `mid nodflt`, `istat sh/sb/lh`, `imask sh/sb/lh`, `gate run`).  **There is no escape here
and no floor question.**  What is missing is the falsifiable claim, not the coverage.

And the mutant is a serious one, which is why the omission is worth naming.  From
`mutants14.frozen.py:31-35`:

> *"The `goto` MOVED INSIDE the latch block: one line, up one line.  The FIRST refusal in a session
> declines correctly; EVERY LATER ONE falls through into the register switch, and SILENTLY, because the
> latch it just set suppresses the announce."*

That is the decline-suppression face in its GENERAL form -- the same family as `M3_timelatch` and
`M5_revlatch`, which PRETABLE does disclose by name.  So the block predicted two specific instances of
the family and left the general one unlisted.

## FOR THE CLOSING PASS

Not a floor breach; a PRETABLE completeness defect.  The closing condition at `PRETABLE.out:138-140`
says the pass closes when *"all six mutants above are killed on their named rows"* -- **M1 is not among
them and has no named rows**, so the condition is silent about a leg the table nevertheless ran.

---

## AN APPARATUS ERROR OF MINE, RECORDED BECAUSE IT NEARLY DOUBLED THE FINDING

My first extraction of the driver's leg list used `tr -d '\\n'` to strip line continuations.  **That
deletes backslashes AND every literal `n`**, so it reported `G_lane_ctl` as `G_lae_ctl` and
`M4_timeplain` as `M4_timeplai` -- both then showed as "NO PREDICTION" because the mangled names match
nothing.  I nearly filed three gaps where there is one.

The backslash class again, in my own one-liner.  Re-derived with python's `str.replace` on the
continuation character and a split, which is immune in both directions -- and the corrected count is
**exactly one**.
