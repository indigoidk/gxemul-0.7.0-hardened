# PASS 3c -- announce-then-land vs the 82-row repair

Frozen instrument probe82.frozen.py md5 cd22f95109e978c93f718dfd334042b9 (82 rows),
identical to the live worktree probe when the run started.  Product BASE3 md5
6fdb3880b35858b337fbe8e9a0eff0b8, likewise identical.  HEAD still b78bb0f (uncommitted),
so this measures exactly what is staged to ship.

Predictions recorded at 14:10, BEFORE any cell (PREDICTIONS3C.txt):
  BASE3 82/82; each M_FALL 81/82 with exactly ONE row moving --
  `rb <arm>' for SCCICR/SCCRX/SCSIICR, `op pscale noig' for PSCALEADJ.

  BASE3             82/82   <- MEASURED, matches

## WHY PASS 3c IS LOAD-BEARING RATHER THAN CONFIRMATORY

Checked at 14:32: the round's own artifacts contain NO M_FALL cell.
  killtable2_20260903/ holds PRETABLE.out and part1 only.
  part1's nine mutants are M_DELETE, M_DELETE_MASK, M_DELETE_TXICR, M_KILL_IPL,
  M_KILL_MASK, M_LENGT2_SCCERR, M_LENGT2_SCCTX, M_LENGT2_TXCTL, M_LENGT2_TXICR.
  `find -iname "*FALL*"' returns nothing.

So the four rows added in the 78 -> 82 step (rb sccicr, rb sccrx, rb scsiicr,
op pscale noig) were written from REASONING -- the PRETABLE's prediction plus this
seat's finding -- and NOTHING has measured that they kill the shape they were added
for.  Pass 3c is that measurement, and it is the last floor question outstanding
before the commit.

The three shapes the round DID measure (delete / len>2 / kill) all make the arm STOP
ANNOUNCING, so they move the `dcl' row and `latch all' as well.  None of them exercises
the announce-then-land path these four rows exist to catch.  A row added for a shape
that no mutant in the table produces is exactly the vacuity the floor's clause (b)/(d)
machinery exists to detect -- which is why it has to be run, not asserted.

  M_FALL_SCCICR     MEASURED: rb sccicr got 0x18, want 0x1f -> FAIL, and it is the
                    SOLE red.  latch all 12 (green), op sccicr dcl 1 (green),
                    rb sccrx / rb scsiicr / op pscale noig all green.
                    0x18 = 0xb8 & 0x1f -- the neighbour's lane in an interrupt-control
                    register, exactly the value predicted at 14:10.

  The kill is PRECISE: only the mutated arm's own row moves.  That is the correct
  signature -- the shape leaves every other channel untouched by construction, so a
  one-row kill is the strongest result available, not a weak one.
  M_FALL_SCCRX      81/82  RED rb sccrx ALONE  (0xb8 & 0xdf = 0x98)

## VALUE-LEVEL CONFIRMATION, not just red/green

Each verified row caught the EXACT byte predicted at 14:10 from the arm's own mask,
which is stronger than a colour change -- it shows the row observes the real defect
rather than merely differing:

    rb sccicr   got 0x18   = 0xb8 & 0x1f   (SCCICR's mask)
    rb sccrx    got 0x98   = 0xb8 & 0xdf   (SCCRX's mask)

0xb8 is the LOW lane of the wide 0xaab8 -- i.e. the byte belonging to the NEXT address,
which is the whole lane hazard this round exists to prevent, reappearing at an arm the
78-row detector could not see.
  M_FALL_SCSIICR    81/82  RED rb scsiicr ALONE  (0xb8 & 0xdf = 0x98)
  M_FALL_PSCALEADJ  81/82  RED `op pscale noig' ALONE  got 1, want 0

## PASS 3c COMPLETE -- THE 82-ROW REPAIR CLOSES THE CLASS

  BASE3             82/82
  M_FALL_SCCICR     81/82  RED rb sccicr      0x18 (= 0xb8 & 0x1f)
  M_FALL_SCCRX      81/82  RED rb sccrx       0x98 (= 0xb8 & 0xdf)
  M_FALL_SCSIICR    81/82  RED rb scsiicr     0x98 (= 0xb8 & 0xdf)
  M_FALL_PSCALEADJ  81/82  RED op pscale noig 1    (the print a decline never reaches)
  RESTORE PART 1 OK; SENTINEL CLEARED; clone back to 4c0cfc6d (b78bb0f blob).

All four predicted at 14:10 before any cell ran, INCLUDING which single row would move
and, for the three storing arms, the exact byte.  Four for four.

## THE SHAPE OF THE RESULT

Each arm is killed by the channel MATCHED TO ITS OWN BODY, not by a copied row:
  three arms STORE  -> a readback catches the neighbour lane
  PSCALEADJ PRINTS  -> the message it should never reach, counted at zero
That is why the count-based rows cannot help: under announce-then-land `latch all'
stays 12 and every `dcl' row stays 1 BY CONSTRUCTION.  The repair understood this and
built per-arm channels rather than one more counter.

## THE CHAIN, END TO END

  60 rows   six clean sweeps (smallest ONE CHARACTER)          -> DO NOT CLOSE
  78 rows   kills all six; but four arms had NO channel        -> 4 x 78/78 escape
  82 rows   per-arm channels                                   -> 4 x 81/82, all killed
