# OPUS SEAT -- pcc2widthkills, pass 2 (b78bb0f) and pass 3 (the repair)

## PASS 2 -- the shipped 60-row detector at b78bb0f: SIX CLEAN SWEEPS

Baseline named before mutant 1: b78bb0f, dev_pcc2.c md5 4c0cfc6d8e6cb099ebe7e92420e6b71e,
proven three ways (cmp vs SEC at clone time; == `git show b78bb0f:`; == the frozen restore
copy).  Scratch clone of build/ under /tmp; no project tree written.  11 probe runs, all
sentinel-complete.

  BASE 60/60 | M1 60/60 SWEEP | M2 60/60 SWEEP | M3 49/60 | M4 60/60 EQUIVALENT
  M5 59/60   | M6 60/60 SWEEP | M7 60/60 SWEEP | M8 60/60 SWEEP | M9 60/60 SWEEP
  M10 60/60 (disclosed)

Smallest escaping edit: ONE CHARACTER (PCC2_W_SCCTX_LEN -> ...SCCRX..., T->R at index 10).
Non-equivalence proved: collide 2->1 declines (M1); MASK readback 0x0->0xbb (M2).

ROOT CAUSE: the product comment's census mixed UNITS -- "five even-offset BLOCKS" plus
"seven odd ones" = twelve, which reads as all twelve blocks but is five blocks plus seven
LABELS.  IPL (0x3e) and MASK (0x3f) were in neither list, so the probe built from it had
zero rows at either, and `latch two' pinned 1 of 66 possible latch collisions.

## PASS 3 -- the repair (78 rows) owes its own pass 2, and I am the only builder

Instrument FROZEN (d9239db6..., 78 rows); product BASE2 6fdb3880...; both verified
identical to the live worktree during the run.

  BASE2 78/78 | M1 77/78 RED latch all | M2 75/78 RED latch all, op mask dcl, rb mask
  M6 / M7 / M8 / M9 -- see RESULTS3.md

## THE ONE OBLIGATION STILL OPEN, found by READING not by a table

The repair's own PRETABLE says a four-arm (PSCALEADJ/SCCICR/SCCRX/SCSIICR)
announce-then-land escape is "the sentence owed".  Measured against the shipped probe:
the CATCHES list GREW 19 -> 24 lines; the DOES-NOT-CATCH list is BYTE-IDENTICAL to
b78bb0f; the owed sentence is nowhere in the file.  Under the round's own reading of
clause (e), an escape is "outside the contract" only if the CONTRACT says so.

## PASS 3 COMPLETE (78-row repaired detector, frozen instrument)

  BASE2 78/78 | M1 77 | M2 75 | M6 77 | M7 71 | M8 75 | M9 75
  ALL SIX pass-2 clean sweeps are killed.  Every red row predicted by name at 13:41.
  Restore verified against the b78bb0f blob; sentinel cleared.

  Cross-validated against the round's independent rig on three overlapping cells:
  M2 = their M_DELETE_MASK (75/78, same 3 rows); M7 = their M_KILL_IPL (71/78, same 7);
  M8 = their M_LENGT2_SCCTX (75/78, same 3).  Different clone, driver and binary.

## THE OPEN FINDING WAS RESOLVED WITH ROWS, NOT A SENTENCE (probe 78 -> 82)

Added: rb sccicr / rb sccrx / rb scsiicr (the `rb mask' pattern I proposed) and
`op pscale noig'.  The new comment credits the ruling: "The measuring seat asked whether
a disclosure can discharge a floor clause; it cannot, or every breach becomes a sentence."

AND IT IMPROVED ON MY RECOMMENDATION.  I said PSCALEADJ needed only a DOES-NOT-CATCH
sentence because its body stores nothing.  Wrong in a useful direction: its body PRINTS
"ignored (value ...)", so the message IS a channel, and `op pscale noig' asserts it at
ZERO.  All four arms got a real channel; no sentence is owed.

## STILL RUNNING -- because the 82-row repair is itself new floor-bound material

  pass 3b  M_FALL x4 vs the 78-row detector  -- was the disclosed gap really an escape?
  pass 3c  M_FALL x4 + BASE3 vs the 82 rows  -- do the new rows actually kill it?

## PASS 3b -- the disclosed gap was REAL (78-row detector)

  M_FALL_SCCICR / SCCRX / SCSIICR / PSCALEADJ:  78/78 EACH -- four TOTAL clean sweeps.
  All four predicted 78/78 at 13:51, before any cell ran.
  So the 78-row detector was BELOW THE FLOOR at four arms, and the PRETABLE's
  "sentence owed" would have shipped four clause-(d) breaches with a paragraph
  explaining them.

## PASS 3c -- do the four NEW rows actually close it?  (82-row repair)

  BASE3            82/82
  M_FALL_SCCICR    81/82  RED `rb sccicr' ALONE   got 0x18, want 0x1f  (= 0xb8 & 0x1f)
  ...three arms pending

  AND THIS RUN IS LOAD-BEARING, not confirmatory: the round has NO M_FALL cell in any
  of its own artifacts.  Its nine measured shapes all make the arm STOP ANNOUNCING, so
  none of them exercises the path these four rows were added for.  The rows were
  written from reasoning; this is the first measurement of them.
