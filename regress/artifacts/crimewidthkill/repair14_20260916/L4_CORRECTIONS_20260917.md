# `#529` REPAIR 14 -- L4 RECORDS CORRECTIONS FROM THE OWED PASS 2 (grok, 2026-09-17)

**`PRETABLE.out` IS NOT EDITED AND MUST NOT BE.**  Its mtime (03:16, before the table logs) is the
ORDER PROOF that it preceded table 1 -- the same discriminator the oracle-correction rule uses.
Editing it to fix a wrong prediction would destroy the one property that makes it evidence.
Corrections therefore land HERE, dated, beside it.

## THE RULING THAT PRODUCED THESE -- Q2, and it rejected BOTH readings I offered

I asked whether "killed on their named rows" means AT LEAST ONE or ALL.  grok rejected both and
named a third thing:

> **SPLIT KILL FROM CHANNEL.**  *"'At least one' lets an over-broad prediction pass the channel
> check.  Naming all 204 rows would then 'pass'.  That is the check-that-cannot-fail, and it is the
> reading that lets you close.  Do not take it."*
>
> **`check_pred.py` ALREADY IMPLEMENTS THE THIRD THING** -- exact set equality, verdict
> `CHECK_PRED12_PASS_WITH_PREDICTION_MISSES`.  **A prediction miss is L4 of PRETABLE (a WRONG
> RECORD), not L2.  L4 is fixed IN THE RECORD, not by adding rows.**

That is the ruling.  The tool was already right; the carrier's wording was the ambiguous part.

## CORRECTION 1 -- `G_lane_ctl`'s CHANNEL line predicted FOUR rows.  The true set is ONE.

    PRETABLE.out predicted : {acc ctl0c, acc ctl4r, p acc ctl0c, p acc ctl4r}
    MEASURED (check_pred)  : {p acc ctl4r}                      203/204, sole carrier

**The prediction was over-broad.  It is corrected here, not re-read as satisfied.**  Q1 is
separately ruled: sole-carrier at 203/204 is **NOT a floor breach** -- acceptable.

## CORRECTION 2 -- MY OWN REASONING WAS OVERSTATED, and grok corrected it while upholding my grade

I graded `M1_gotolatch` (which ran with NO prediction) a PRETABLE completeness defect rather than a
floor breach.  **That grade is upheld.**  But I justified it by writing *"whatever it scored would
have matched"*, and that is **FALSE**:

> `check_pred.py` puts `M1_gotolatch` in `MUST_STAY_KILLED`.  **A 204/204 would have printed
> `REGRESSION` and `CHECK_PRED12_FAIL`.**  So the leg was NOT unfalsifiable.

**The cannot-fail part is the SET, not the KILL** -- "194/204 with any ten names" and "203/204 with
one" both read as *still killed*.  That is a real but much narrower defect than I claimed.
*A correction is not safer than the thing it corrects; this one is a correction OF a correction.*

## CORRECTION 3 -- A FALSE CONTRACT CLAIM, VERIFIED IN THE SOURCE BEFORE BEING RECORDED HERE

The contract treats the `default:` arm as **host-log only**.  **That is false for `acc ctl0c`**, and
`src/devices/dev_sgi_ip32.c` says so plainly:

    :280   } else if (len == 4) {          <-- the WIDTH ARM, and it runs BEFORE the switch
    :290       odata = d->reg[relative_addr / 8];
    :353   case CRIME_CONTROL:  /* 0x008 */
    :396   default:                        <-- +0x0c has NO case label, so it lands here

`0x0c / 8 == 0x08 / 8 == 1`, so **a 4-byte read at +0x0c takes CONTROL's LOW half out of the width
arm and only THEN reaches `default:` for a debug print.**  A decline skips the width arm and answers
**0**.  That is **GUEST-VISIBLE, not host-log**.

## THE UNASKED FINDING, and it is the one that matters most for the next table

> **`ctl0c` NEVER REDS UNDER ANY OF THE FIFTEEN LEGS** -- including `G_clr_ctl4r`, the
> equivalent-cell decline the pair was added to make observable.

That mutant is `relative_addr == CRIME_CONTROL` (`0x08`); `+0x0c` is a **different switch label**
(`default:`).  Same storage (`relative_addr / 8`), different switch.  **So the DISCRIMINATING half
of the pair has no measured kill in this table.**

Accept-row failability: *a row is not discharged by EXISTING.*  **Do not add a row -- the rows
exist.**  Either run a decline that actually hits `0x0c`, or **stop claiming `ctl0c` as
`G_lane_ctl`'s channel.**

## A LATENT APPARATUS HAZARD, recorded because it did NOT fire

`check_pred.py` still slices `ln[:15]`.  This probe's names look <= 14 (`p acc istat lw`,
`rst alive once`).  **`#530`'s padded-column bug is the same family.**  It did not fire here; that
is not proof the slice is safe.

## DOES THIS PASS CLOSE THE CHAIN?

**No.**  grok's verdict: *"Repair 14's accept-side floor-zero holds on the measured set.
`G_lane_ctl` 203/204 is not a floor breach.  Do not close on 'at least one named row reddened'.
`M1_gotolatch` is a PRETABLE completeness defect, not a floor breach, and it does not void the zero
for the denominator you stated.  This pass does not close `#529`: the decline-suppression face
stays open, as PRETABLE said before the run."*
