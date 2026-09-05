# PASS 3 -- the repair made in response to my pass 2 owes its own pass 2

INSTRUMENT FROZEN for all runs: probe.frozen.py md5 d9239db620ae675f9462a11fb0924478
(78 rows).  PRODUCT: dev_pcc2.base2.c md5 6fdb3880b35858b337fbe8e9a0eff0b8, which was
byte-identical to the live worktree when the run started.  A comparison run owes ONE
instrument -- python reads the whole file at startup, so an edit between runs would put
a different instrument on either side of the diff.

| # | edit | 60-row (pass 2) | 78-row (repaired) |
|---|---|---|---|
| BASE2 | none | 60/60 | **78/78** |
| M1 | latch bit alias SCCTX->SCCRX (1 char) | 60/60 SWEEP | (pending) |
| M2 | MASK `len != 1`->`len > 2` | 60/60 SWEEP | (pending) |
| M6 | MASK announce-then-fall-through | 60/60 SWEEP | (pending) |
| M7 | verbatim exit(1) at IPL | 60/60 SWEEP | (pending) |
| M8 | guard deleted at SCCTX | 60/60 SWEEP | (pending) |
| M9 | guard deleted at MASK | 60/60 SWEEP | (pending) |

BASE2 = 78/78 discharges the first half of the floor: the detector is green on the fix.

## FINDING FROM READING, INDEPENDENT OF THE TABLE: THE OWED SENTENCE WAS NOT WRITTEN

The repair's own PRETABLE (SECTION 2) says, of PSCALEADJ/SCCICR/SCCRX/SCSIICR:

  "A guard edit that lands the write AND still announces (the M_FALL_MASK shape) at one
   of those four would escape; THAT IS THE SENTENCE OWED"

Measured against the shipped probe:

  CATCHES list        b78bb0f 19 lines -> repaired 24 lines   (GREW)
  DOES NOT CATCH      byte-IDENTICAL to b78bb0f               (UNCHANGED)
  the owed sentence   appears NOWHERE in pcc2_width_probe.py

So the repair strengthened its POSITIVE claims and did not record the NEGATIVE one its
own artifact named.  This matters under the round's OWN reading of clause (e): a
disclosed escape is "outside the contract" only if the CONTRACT says so.  The
disclosure lives in a kill-table artifact; the contract is what ships beside the rows
and is what a future reader consults.  A contract that grew its CATCHES list while its
DOES-NOT-CATCH list stood still reads as MORE complete than before, not less.

Disposition: L3 (undischarged obligation -- the round's own artifact names it as owed)
or L4 (wrong record).  Cost: one sentence.  Independent of how the floor question below
is resolved.

## LATCH-AXIS ROBUSTNESS OF THE REPAIR (reasoned, not measured -- stated as such)

`latch all' counts DECL occurrences == 12 across twelve one-write-per-block sessions.
Single-edit attacks on the latch and where they land:

  drop `d->warned |= bit'  -> every block floods, but `latch all' writes each block
                             ONCE so it still counts 12.  CAUGHT BY `latch same' (2 != 1).
  invert the latch test    -> nothing ever announces; `latch all' 0.  CAUGHT.
  alias two enum members   -> 11.  CAUGHT (measured: M1).
  change the message text  -> DECL stops matching; count drops.  CAUGHT.
  duplicate a decline call -> latch still prints once; 12.  Benign (no behaviour change).

So `latch all' + `latch same' cover the latch axis between them: cardinality catches
collisions, same-site-twice catches floods.  Neither alone does.

A read-side guard regression scoped to an ODD arm (e.g. `len != 1' restored for BOTH
directions at SCCICR) has no row -- but it is nearly harmless: the memcpy above the
switch has already served the data, so the only effect is a spurious announce whose
text says "write" about a read.  Recorded as benign, not filed.
M1: latch all 11/12 FAIL -- sole killer as predicted

MEASURED, pass 3 (78-row repaired detector, frozen instrument):
  BASE2  78/78
  M1     77/78  RED: latch all            <- prediction was "latch all SOLE killer": EXACT

## HOW PASS 3 RELATES TO THE ROUND'S OWN REPAIR TABLE

killtable2_20260903/part1 ran NINE mutants against the 78-row detector, all killed,
zero sweeps: M_DELETE 72, M_DELETE_MASK 75, M_DELETE_TXICR 74, M_KILL_IPL 71,
M_KILL_MASK 73, M_LENGT2_SCCERR 76, M_LENGT2_SCCTX 75, M_LENGT2_TXCTL 73,
M_LENGT2_TXICR 74, BASE 78/78.

Its own PRETABLE SECTION 4 predicts THIRTEEN.  Four are not in part1:

    M_ALIAS_SCCTX    the latch-bit alias      <- my M1: MEASURED 77/78, RED `latch all'
    M_LENGT2_MASK    `len > 2' at MASK        <- my M2
    M_FALL_MASK      announce-then-land       <- my M6
    M_IDATA_GENCTL   operand swap to a value  <- (their own find; rows shipped)

So pass 3 is not a duplicate: it lands on three of the four cells the round's table has
not yet reached, using a FROZEN copy of the same instrument.  Pass 3b then measures the
one shape the PRETABLE explicitly says would escape, which is in nobody's mutant list.

## STANDING SUMMARY (pass 3 in flight)

  BASE2  78/78                       the repaired detector is green on the fix
  M1     77/78  RED: latch all       the ONE-CHARACTER latch alias is now caught
  M2     RED: latch all (+ op mask dcl / rb mask expected)

## WHAT I WILL RECOMMEND REGARDLESS OF THE REMAINING CELLS

1. The ORIGINAL diff at b78bb0f, with its 60-row detector, was below the vacuity floor:
   six measured clean sweeps, smallest ONE CHARACTER, all inside clause (d)'s
   diff-closed enumeration.  DO NOT CLOSE was the right pass-2 verdict.

2. The REPAIR is strong and was built with the mandatory pre-table block that table 1
   skipped.  It fixes the census (five -> SIX guest-reachable), rows IPL and MASK, adds
   per-arm readbacks, and adds `latch all' -- which measurably kills the mutant that
   swept the 60-row detector.

3. ONE OBLIGATION REMAINS UNDISCHARGED, found by reading and independent of any cell:
   the PRETABLE says a four-arm announce-then-land escape is "the sentence owed", the
   CATCHES list GREW (19 -> 24 lines) and the DOES-NOT-CATCH list is byte-identical to
   b78bb0f.  The owed sentence appears nowhere in the probe.  Cost: one sentence.

4. HOUSEKEEPING: build/ and build-asan/ still hold b78bb0f while SEC and est/ carry the
   repair (self-consistent, so no stale-binary trap today, but the no-VPATH rule wants
   the propagation); and the ledger row still reads "Detector 60 rows ... seven mutants
   zero sweeps ... Owes pass 2".

## WHY M6 + PASS 3b TOGETHER MAKE THE ARGUMENT, rather than either alone

From the round's own part1 reds:
  M_KILL_IPL      latch all, latch all lv, hrd ipl, hrd ipl lv, hwr ipl, hwr ipl lv, hwr ipl dcl
  M_DELETE_MASK   latch all, op mask dcl, rb mask
  M_LENGT2_SCCTX  rb scctx, rb scctx dcl, latch all

Every one of those shapes makes the arm STOP ANNOUNCING, so the `dcl' row and
`latch all' both move -- two independent channels.  The ANNOUNCE-THEN-LAND shape is
different: the announce SURVIVES, so `dcl' stays 1 and `latch all' stays 12, and the
READBACK is the only channel left.

  M6 (my run)   = M_FALL_MASK at an arm that HAS a readback  -> expect RED on `rb mask' ALONE
  PASS 3b       = the same shape at the four arms WITHOUT one -> expect 78/78

If both land as predicted, the pair is the proof: the shape is detectable ONLY by a
readback, and four of the twelve arms have none.  That is a statement about the
detector's structure, not about one lucky mutant.
  M2   75/78  RED: latch all, op mask dcl, rb mask   <- all three predicted killers

## THE DECISIVE OBSERVATION, measured mid-M6

Under M6 (announce-then-land at MASK) the cardinality row reads:

    latch all        12           12    ... ok
    latch all lv     exit0        exit0 ... ok

`latch all' is GREEN.  It must be: the decline helper is still CALLED, so the bit is
still set and the message still printed; only the `break' is gone, so the write ALSO
lands.  Cardinality counts ANNOUNCES, and the announce is intact.

So for the announce-then-land shape the ONLY available channel is a READBACK of the
register.  MASK has one (`rb mask').  PSCALEADJ, SCCICR, SCCRX and SCSIICR do not --
which is exactly what the repair's PRETABLE discloses and what pass 3b measures.

This is clause (f)'s lesson in a new costume: a suite that asserts the ANNOUNCE
(distinctness/cardinality) is invariant under an edit that leaves the announce alone.

  M6   77/78  RED: rb mask ALONE   <- prediction EXACT.  latch all 12 (green),
                                      op mask dcl 1 (green).  The READBACK is the only
                                      channel that sees announce-then-land.

## THE STRUCTURAL RESULT, now measured rather than argued

  shape                         latch all   <arm> dcl   readback
  guard deleted / len>2 / kill   MOVES       MOVES       moves
  ANNOUNCE-THEN-LAND             12 (green)  1 (green)   THE ONLY CHANNEL

Twelve blocks; readbacks exist at GENCTL, VECBASE, TxCTL, TxICR, SCCTX, MASK (and
SCCERR is value-identical by design, disclosed).  PSCALEADJ, SCCICR, SCCRX, SCSIICR
have NONE -- so the announce-then-land shape at those four has no channel at all.
Pass 3b measures exactly that.

## INDEPENDENT-RIG CROSS-VALIDATION

  round's rig  /tmp/gxpcc2b     their driver, their clone   BASE 78/78
  my rig       /tmp/gxopus_pcc2 my driver, my clone         BASE2 78/78

and the overlapping cell agrees channel-for-channel:

  their M_DELETE_MASK  75/78  latch all, op mask dcl, rb mask
  my    M2             75/78  latch all, op mask dcl, rb mask

Two independently built binaries, two drivers, two clones, one detector, same answer.
That is the control neither table has on its own.
  M7   71/78  RED: latch all, latch all lv, hrd ipl, hrd ipl lv, hwr ipl, hwr ipl lv,
                    hwr ipl dcl   -- IDENTICAL to the round's own M_KILL_IPL (71/78,
                    same seven rows), from a different rig and a different driver.
                    `hrd ipl' shows exit1 and `hrd ipl lv' shows died: the guest-
                    reachable host kill the 60-row detector could not see.
  M8   75/78  RED: rb scctx, rb scctx dcl, latch all   -- three predicted killers; also
                    identical to the round's own M_LENGT2_SCCTX (75/78, same three rows),
                    from a different rig.  Guard DELETED at SCCTX vs their `len > 2':
                    different edits, same observable, same channels.
  M9   75/78  RED: latch all, op mask dcl, rb mask  -- same three channels as M2 (both
                    make MASK's halfword LAND) and as the round's own M_DELETE_MASK.

## PASS 3 COMPLETE -- ALL SIX PASS-2 SWEEPS ARE KILLED BY THE REPAIR

  BASE2 78/78 | M1 77 | M2 75 | M6 77 | M7 71 | M8 75 | M9 75
  Restore verified against the b78bb0f blob; PART 1 OK; SENTINEL CLEARED.

Every one of the six edits that scored 60/60 against the shipped detector now reds, and
every red row was predicted by name before the run (PREDICTIONS3.txt, 13:41).

## PASS 3b -- THE DISCLOSED GAP WAS REAL

  M_FALL_SCCICR  vs the 78-row detector:  78/78  TOTAL CLEAN SWEEP
  (predicted 78/78 at 13:51, before the cell ran)

Guard kept, announce kept, `break' removed.  `op sccicr dcl' stays 1 and `latch all'
stays 12 BY CONSTRUCTION, and 0xb8 & 0x1f = 0x18 lands in SCCICR -- an INTERRUPT
CONTROL register -- followed by reassert_interrupts().  Every one of the 78 rows green.

So the PRETABLE's own sentence ("a guard edit that lands the write AND still announces
at one of those four would escape") was a CORRECT prediction of a real clause-(d)
breach, not a pessimistic disclaimer.  Disclosing it would have shipped it.

That settles the disposition question empirically in favour of the reading the round
adopted: a floor clause cannot be discharged by a sentence.  The four rows added in the
78 -> 82 step were NECESSARY, and pass 3c now checks that they actually kill this.

## PASS 3b COMPLETE -- FOUR TOTAL CLEAN SWEEPS, ALL FOUR PREDICTED

  M_FALL_SCCICR     78/78
  M_FALL_SCCRX      78/78
  M_FALL_SCSIICR    78/78
  M_FALL_PSCALEADJ  78/78
  RESTORE PART 1 OK; SENTINEL CLEARED.

Four one-edit mutants, each removing a single `break;', each leaving a 78-row
gate-enforced detector completely green.  Predicted 78/78 apiece at 13:51, before any
cell ran.

The three storing arms land the neighbour lane in an INTERRUPT CONTROL register and
call reassert_interrupts(); PSCALEADJ reaches a print it should never reach.

CONCLUSION: the 78-row detector was BELOW THE VACUITY FLOOR at four arms, by the round's
own disclosure, and the disclosure could not discharge it.  The 78 -> 82 repair was
mandatory.  Pass 3c now measures whether those four rows actually close it.
