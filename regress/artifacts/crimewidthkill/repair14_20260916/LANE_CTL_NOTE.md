# `G_lane_ctl` -- the leg that tests repair 14's CONTROL pair.  MEASURED 2026-09-17 08:2x, table 12.

    PRETABLE predicted:  reds acc ctl4r, acc ctl0c, p acc ctl4r, p acc ctl0c   ->  200/204
    MEASURED:            reds p acc ctl4r ONLY                                 ->  203/204

**THE MUTANT IS KILLED.  203/204 is not 204/204, so this is a PREDICTION MISS, not an escape.**

## WHICH ROW MOVED, AND WHY THE OTHER THREE DID NOT

    row            base        G_lane_ctl
    acc ctl4r      0x0         0x0        green -- CLEAR twin unaffected
    acc ctl0c      0x100       0x100      green -- CLEAR twin unaffected
    p acc ctl4r    0x0         0x100      *** RED -- the sole carrier ***
    p acc ctl0c    0x100       0x100      green

The mutant's effect is confined to the **POST (latch-SET) session** and within it to the **HIGH-lane
read**.  The CLEAR twin does not move at all, so the whole latch-CLEAR half contributes nothing here.

**THAT IS COHERENT RATHER THAN DISAPPOINTING, and the two rows have DIFFERENT jobs:**
* `ctl4r` reads `+0x08`, whose correct answer is 0.  Alone it is vacuous against a DECLINE, because a
  decline also answers 0 -- which is what its own note says.  Under a LANE edit it goes to 0x100, i.e.
  NON-ZERO, so it fires on its own.
* `ctl0c` reads `+0x0c`, whose correct answer is 0x100.  Its job is to catch a DECLINE at that offset
  (which would answer 0).  A lane SWAP leaves 0x100 there, so it correctly does not move.

So the pair is not four rows redundantly watching one edit; it is two rows watching two different
edits, and this leg exercises one of them.  **PRETABLE's four-red prediction was wrong about which
rows this mutant moves.**

## *** SOLE CARRIER -- NAME IT IN THE CLOSING PASS ***

`p acc ctl4r` is the **only** row in a 204-row instrument that reds under `G_lane_ctl`.  If that row
were ever removed or measured vacuous, this mutant becomes a TOTAL ESCAPE at 204/204.  That is the
same shape table 7 recorded for `W23`/`stub3 w2`, and it is the kind of fact a score alone hides:
203/204 looks comfortable and is one row from nothing.

*Recorded while the table was still running, so the observation is not reconstructed afterwards.*

---

## *** A QUESTION THE CLOSING CONDITION DOES NOT SETTLE, AND THIS LEG MADE IT LIVE. ***

`PRETABLE.out:138-140` states the closing condition, written before the run so it could not be fitted
afterwards:

> *"this pass closes the ACCEPT-side class only.  It closes when **all six mutants above are killed on
> their named rows**, the three controls do not move, and the base reports 204/204."*

**`G_lane_ctl` names FOUR rows and moved ONE of them.**  The row that moved (`p acc ctl4r`) IS one of
the four named, so this is not the "red row outside its prediction" case that `:142` says must be
re-run alone.  But the condition's wording admits two readings:

    (a) killed on AT LEAST ONE of its named rows   -> G_lane_ctl PASSES
    (b) killed on ALL of its named rows            -> G_lane_ctl FAILS the condition

**I am not choosing between them here, deliberately.**  Picking the reading that lets my own repair
close is exactly the shape the order discriminator exists to prevent, and the author of a repair is
the worst-placed person to resolve an ambiguity in its own pass criterion.  **It goes to the closing
pass as a named question.**

*The honest note either way: the mutant IS killed, base IS 204/204, and the row that fired is the row
the pair was added for.  What is unsettled is whether a four-row prediction that yields one red counts
as the condition being met, or as the condition being met by luck.*
