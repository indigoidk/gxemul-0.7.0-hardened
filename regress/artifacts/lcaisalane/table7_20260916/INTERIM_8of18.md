# Table 7 -- INTERIM.  *** NOT A VERDICT. ***
# Opened at 8 of 18 legs; UPDATED at 10 of 18 (see the UPDATE section at the end).
# The filename says 8of18 and is left alone deliberately -- the checkpoint cites it by name,
# and renaming a cited artifact is how a citation goes dead.

Written 2026-09-17 ~04:05 while the run is still in flight, so that the two prediction misses are
resolved while the evidence is fresh rather than reconstructed in three hours.  **The closing
condition is NOT evaluated here** -- this project has three recorded instances of a tally written
before the thing it counts had finished, and every one of them was wrong.

Each score names its log.  All eight carry the completion sentinel `LCAISALANE_DONE`.

    leg        predicted   measured   log                     reds  sentinel  witness
    base        352/352     352/352   logs/probe_base.raw        0   DONE      PASS
    cdxZL3      351/352     351/352   logs/probe_cdxZL3.raw      1   DONE      FAIL
    RD2z        320/352     320/352   logs/probe_RD2z.raw       32   DONE      FAIL
    RD2post     286/352     286/352   logs/probe_RD2post.raw    66   DONE      FAIL
    WWtail      336/352     336/352   logs/probe_WWtail.raw     16   DONE      FAIL
    WWall       267/352     267/352   logs/probe_WWall.raw      85   DONE      FAIL
    Wpure       251/352     255/352   logs/probe_Wpure.raw      97   DONE      FAIL   <-- MISS +4
    RWall       320/352     324/352   logs/probe_RWall.raw      28   DONE      FAIL   <-- MISS +4

## THE TWO MISSES ARE THE **DERIVED** COMPONENT, NOT A CARRIED ONE -- which is the benign branch
## the PRETABLE named in advance, and it was CHECKED rather than inferred from the arithmetic.

`PRETABLE.out` pre-committed the reading: *"a miss there is a PREDICTION error and is reported as
one; a miss on a CARRIED component means the merge changed an existing row's behaviour, which would
be a far more serious finding about repair 6."*

Three legs predicted `kbcmd(derived) = 4`.  Reading the four `kbcmd <w> post` rows directly:

    WWall   kbcmd b/w/l/q post   got 0x1  want 0x0   RED    -- the derived 4 DID fire
    Wpure   kbcmd b/w/l/q post   got 0x0  want 0x0   green  -- SATISFIED, not absent
    RWall   kbcmd b/w/l/q post   got 0x0  want 0x0   green  -- SATISFIED, not absent
    base    kbcmd b/w/l/q post   got 0x0  want 0x0   green

`got == want == 0x0` matters: the rows are present and legitimately green, so this is not a row that
silently stopped being tested (the padded-column / mis-cut class).  With kbcmd = 0 the component sums
are EXACT in both missing legs:

    Wpure   legacy 32 + pit 64 + kbcmd 0 + z1 1 = 97   -> 255/352   (predicted kbcmd 4 -> 251)
    RWall   legacy 18 + pit 10 + kbcmd 0 + z1 0 = 28   -> 324/352   (predicted kbcmd 4 -> 320)

**So EVERY CARRIED COMPONENT IS EXACTLY RIGHT in all eight legs, and only the fresh derivation was
wrong, in the direction the PRETABLE flagged as least trustworthy.**  The derivation's error is
specific and worth naming for the closing pass: `post` reds only where the mutant actually queues a
SECOND reply (WWall duplicates the store); in `Wpure` and `RWall` no second command byte is ever
delivered, so the queue is empty after one pop and `post` reads its correct 0x0.

`cdxZL3` = 351/352 with its single red being exactly `stub3 z1` -- the enumeration's own check on
itself, and it passes.  A 352/352 there would have meant repair 6's row is vacuous.

## AN APPARATUS CORRECTION, recorded because the next reader will reach for the same grep

`grep -cE 'FAIL *$'` reports **one more** than the true red count on every leg that has any, and 0 on
the leg that has none -- a constant +1 that reads like a real discrepancy.  The extra match is the
SUMMARY line `LCAISALANE_WITNESS=FAIL`, not a row.  Exclude `^LCAISALANE_` and every leg agrees with
its own `RESULT=` arithmetic exactly (column `reds` above).

*This is the carrier's pattern-matched-something-it-should-not class.  It was caught by the
denominator habit -- cross-checking the count against `RESULT` instead of citing it alone -- and if it
had been cited as the score it would have been wrong by one in eight places at once.*

---

# UPDATE -- 10 of 18, 2026-09-17 04:24.  Still NOT a verdict; eight legs outstanding.

    leg        predicted   measured   log                     reds  sentinel
    dNZtail     344/352     344/352   logs/probe_dNZtail.raw     8   DONE      EXACT
    noff        279/352     279/352   logs/probe_noff.raw       73   DONE      EXACT

## *** `noff` IS A TABLE-VALIDITY GATE AND IT PASSES -- CHECKED BY ROW NAME, NOT BY COUNT. ***

`PRETABLE.out` pre-committed: *"`noff` green would mean the 150 new rows are vacuous and NOTHING
else in this table may be believed."*  It also predicted the exact red set: *"the 73 pit rows it
already reds, AND NOTHING ELSE (it touches no lca code)."*

Measured -- and verified the way the kbcmd miss taught, by NAME rather than by arithmetic, because
a count can agree for the wrong reason:

    73 red rows total (summary lines excluded)
      19  pitT      18  pit2      18  pit1      18  pit0      = 73
       0  stub* / kbcmd* / kbcq* / lane* / isa*

**So the 150 new pit rows are LIVE -- they red under a mutant that disables them -- and no lca row
moved under a mutant that touches no lca code.**  Both halves of the prediction hold.

Running tally against PRETABLE, 10 legs: **EIGHT EXACT, TWO MISS (+4 each)**, both misses fully
attributed to the DERIVED kbcmd component and no carried component disturbed (see above).

**NOW IN FLIGHT: `W23` and `Wdrop` -- two of the THREE legs `PRETABLE.out` marks
`*** LOW CONFIDENCE ***`** and calls "the point of this table", because their components were
UNMEASURED and predicted rather than carried.  A miss there is a PREDICTION error and is reported
as one; the interesting outcome is what they actually red.

---

# UPDATE -- 12 of 18, 2026-09-17 04:54.  Still NOT a verdict; six legs outstanding.

**BOTH LOW-CONFIDENCE LEGS LANDED, AND BOTH MISS.  Every miss is the UNMEASURED component; every
CARRIED component is exact.**  That is the benign branch `PRETABLE.out` named in advance:
*"a miss there is a PREDICTION error and is reported as one; a miss on a CARRIED component means the
merge changed an existing row's behaviour, which would be a far more serious finding about repair 6."*

    leg        predicted    measured   log                    reds
    W23        ~343/352     351/352    logs/probe_W23.raw        1   MISS  -8   (LOW CONFIDENCE)
    Wdrop      ~231/352     262/352    logs/probe_Wdrop.raw     90   MISS -31   (LOW CONFIDENCE)

## Wdrop, decomposed by ROW NAME rather than by arithmetic

    component                  predicted   measured
    pit  (pitT/2/1/0, 8 each)      64          32     <-- the UNMEASURED one.  EXACTLY HALF.
    kbcmd                           8           8     exact
    legacy + the stub3 z1 row      49 + 1      50     exact
                                  ------      ----
                                   122          90

**The ENTIRE 31-row miss is the write-parity pit component coming in at exactly half.**  The
prediction assumed all 64 write-parity rows would red; 32 did, 8 per counter across four counters.
*Exactly half is a signal rather than noise -- it is consistent with the write-parity rows reddening
on one parity and not both -- but this record does NOT claim that mechanism, which is unmeasured.*

**AND THE kbcmd COMPONENT FIRED CORRECTLY HERE (8 predicted, 8 measured), which matters for the
earlier finding:** on `Wpure` and `RWall` the same derived component contributed ZERO against a
predicted 4.  So kbcmd is not simply wrong everywhere -- it is right where a second reply is actually
queued and zero where none is, exactly as the 10-of-18 note derived.  The derivation's error is
narrow and its shape is now measured twice in each direction.

*A caveat on the source rather than on the measurement: PRETABLE.out line 205's columns are ambiguous
for this leg, because the long `UNMEASURED -- predicted 64' text overflows the kbcmd column and pushes
`8' into visual alignment with z1.  Read against the measurement and against WWall's unambiguous row,
the 8 is kbcmd.  Stated here because resolving a column by what was measured is mildly circular and a
future reader should know the ambiguity existed rather than inherit my reading of it.*

## W23: NOT AN ESCAPE, BUT A SOLE CARRIER -- worth naming before the closing pass

Its single red is `stub3 w2` (`(2,3) STORE 0x5a.. SP(0x63)`), a len-2 store at lane 3, which is
exactly the cell W23 mutates.  The leg clears the closing condition -- 351/352, not 352/352 -- **by
one row**.  That row is the SOLE CARRIER for this mutant, so if it were ever removed or measured
vacuous, W23 becomes a total escape and the pass would not close.

STILL IN FLIGHT: `RWtail` and `WXR`.  Four legs after those.

---

# THE `Wdrop` PIT MISS IS RESOLVED, AND IT IS A **QUALITY RESULT**, NOT A COVERAGE GAP.
# Settled 2026-09-17 05:0x from logs already on disk -- no run, no machine.

The 10-of-18 note recorded pit at 32 measured against 64 predicted -- *exactly half* -- and
deliberately did NOT claim a mechanism.  The mechanism is now measured, and it goes the good way.

**THE PIT ROWS SPLIT BY DIRECTION, AND `Wdrop` IS A WRITE-ONLY MUTANT.**  Row names carry the
discriminator: `ps*` rows are STORES, `pl*` rows are LOADS.

    mutant   pit reds   store (ps)   load (pl)   other
    Wdrop        32         32            0         0     <- write-drop: ONLY stores red
    noff         73         32           32         9     <- feature off: BOTH directions red

    and Wdrop's red set is a strict SUBSET of noff's (comm: no row red in Wdrop but not in noff).

**Zero leakage in either direction.**  A write-drop mutant reds every store row and not one load row.
That is precisely the property a detector should have, and it is stronger than the prediction assumed.

**SO PRETABLE's 64 WAS THE FEATURE-OFF FIGURE APPLIED TO A DIRECTIONAL MUTANT.**  It is a prediction
error of exactly the kind the block flagged as its least trustworthy number -- *the write-parity rows*
was the label, and 64 is the count of write AND read parity rows together.  **The rows are not
vacuous; the prediction was direction-blind.**

RECONCILIATION OF THE TWO noff FIGURES, because the 10-of-18 note said 73 and this says 64 and both
are right: 73 is every pit red, 64 is ps+pl, and the remaining **9** are 4 `live1' LIVENESS+DEVSIG
controls (one per counter, which legitimately fail when the feature is off) plus 5 read-parity
`pw r1'/`pw t6'/`pw t3' rows.  73 = 32 + 32 + 9, and NONE of the 9 red under `Wdrop'.
*Recorded because two different true counts of "the same thing" is exactly how a frozen number gets
written, and the next reader should see the decomposition rather than have to re-derive which is which.*

**FOR THE CLOSING PASS:** this is evidence FOR repair 6's row set, and it is the kind that a score
alone cannot give -- 262/352 looks like a miss and is actually a detector behaving better than its
own prediction.

---

# *** CORRECTION TO THE SECTION ABOVE.  MY RESOLUTION OF THE `Wdrop` MISS WAS WRONG IN ITS STATED
# REASON, AND A CORRECTION IS NOT SAFER THAN THE THING IT CORRECTS. ***  2026-09-17 05:3x.

**What I wrote, and what is wrong with it.**  The section above says:

> *"SO PRETABLE's 64 WAS THE FEATURE-OFF FIGURE APPLIED TO A DIRECTIONAL MUTANT"*

**That is FALSE, and one measurement refutes it: `noff` -- the feature-off leg -- reds 32 store rows,
not 64.**  I checked `Wdrop` against `noff`, found 32 and 32, and stopped at a story that fit two
points.  `WWall` and `Wpure` each red **64** store rows, which no reading of "feature off" explains.

I also wrote that *32 is the write-side pit count*.  Also false: **there are 64 store rows.**

## THE ACTUAL MECHANISM, read off the rows' own text rather than inferred

The pit store rows come in **BYTE PAIRS**, because the 8253 latch is LSB-then-MSB behind a flip-flop:

    pit1 ps5a w4   want 0x5a   "STORE 0x5a: ONE lca write leaves it in the LSB (an EXTRA access -> 0x12)"
    pit1 ps5a w4B  want 0x12   "...and the MSB holds the flat 0x12 (an EXTRA access -> 0x5a)"

Under `Wdrop` the pair reads:

    w4    got 0x12  want 0x5a   FAIL   <- the write never landed, so the LSB holds the flat value
    w4B   got 0x12  want 0x12   ok     <- the dropped write was never going to reach the MSB

**So the two counts are two different MUTANT SIGNATURES, not two populations:**

    32 store reds  =  a DROPPED write   (only the LSB row moves)     Wdrop, WXR, noff
    64 store reds  =  an EXTRA write    (the flip-flop parity shifts, BOTH rows move)   WWall, Wpure

and the rows' own notes predict exactly that -- they say what an EXTRA access does to each member.

**PRETABLE PREDICTED 64 FOR `Wdrop`: THE DUPLICATE SIGNATURE FOR A DROP MUTANT.**  That is the
prediction error, now stated precisely instead of by analogy.

## WHAT SURVIVES FROM THE EARLIER SECTION, AND IT IS THE PART THAT MATTERED

* `Wdrop` reds **zero** load rows -- the direction split is real and is unaffected by this correction.
* `Wdrop`'s red set is still a strict subset of `noff`'s.
* **The rows are still not vacuous, and the conclusion is now STRONGER than the one it replaces:** the
  byte-pair rows DISCRIMINATE A DROPPED WRITE FROM A DUPLICATED ONE.  A detector that tells those two
  apart by which member of a pair moves is doing more than "reds when something is wrong".

## A TAXONOMY SLIP OF MINE, RECORDED BECAUSE IT NEARLY PRODUCED A SECOND FALSE FINDING

Classifying pit rows I used only `ps`/`pl` and read `RWtail` as **0 pit reds against a predicted 4** --
an exact total with a wrong composition, which I was about to file.  **It was my grep.**  There is a
third prefix, `pw`, which I had already seen in noff's "other 9" bucket and failed to carry forward.
`RWtail` is legacy 2 (`tailr`) + pit 4 (`pitT pw`) = 6: EXACT in total AND composition.

The complete taxonomy, derived from the base log so nobody re-guesses it:

    64 ps   (store)     64 pl   (load)     10 pw     8 live     4 alive     = 150 pit rows

*Both errors here were mine, both were caught by continuing to measure rather than stopping at a
satisfying story, and the second was caught only because the first made me re-check the classification.*
