# OPUS SEAT -- concluding recommendation

## ON THE ORIGINAL DIFF (b78bb0f, 60-row detector): DO NOT CLOSE -- stands.
Six measured clean sweeps, smallest ONE CHARACTER, every one inside clause (d)'s
diff-closed enumeration.  Non-equivalence proved for both headline sweeps.

## ON THE REPAIR (78 rows): IT CLOSES THE CLASS I FOUND.
Measured on a frozen instrument, in a rig independent of the round's own:
  BASE2 78/78 | M1 77/78 (latch all) | M2 75/78 (latch all, op mask dcl, rb mask)
  M6 77/78 (rb mask ALONE) | M7/M8/M9 confirmatory
`latch all' is a genuine class closer: it converts a pairwise-distinctness suite into a
CARDINALITY assertion and catches any collision in the 12-bit space, not one pair of 66.

## WHAT I WOULD STILL ASK FOR BEFORE CLOSING -- three rows and one sentence.

1. THREE READBACK ROWS at SCCICR (0x1d), SCCRX (0x1f), SCSIICR (0x2f), copying the
   `rb mask' pattern verbatim (guest ST_B at the legal width -- byte accesses skip the
   m88k alignment check, so odd offsets are fine; debugger `put h' for the wide write;
   guest LD_BU to read back).  MEASURED REASON: M6 shows that under announce-then-land
   the announce SURVIVES, so `latch all' reads 12 and the arm's `dcl' row reads 1 --
   the readback is the ONLY channel, and those three arms have none while their bodies
   are `= idata & 0x1f/0xdf' FOLLOWED BY reassert_interrupts().

2. ONE SENTENCE in the shipped DOES-NOT-CATCH list for PSCALEADJ, whose body only
   prints, so it genuinely needs no readback and its `dcl' row is the honest channel.

   *** This is the round's OWN undischarged obligation: its PRETABLE says the four-arm
   escape "is the sentence owed", the CATCHES list GREW 19 -> 24 lines, the
   DOES-NOT-CATCH list is BYTE-IDENTICAL to b78bb0f, and the sentence is nowhere in the
   probe.  Under the round's own reading of clause (e), an escape is "outside the
   contract" only if the CONTRACT says so. ***

## HOUSEKEEPING
* build/ and build-asan/ still hold b78bb0f while SEC and est/ carry the repair.  Both
  build trees are self-consistent (binary newer than their own source), so there is no
  stale-binary trap today -- but a measurement taken in build/ right now tests pre-repair
  code, and the no-VPATH rule wants the propagation.
* The ledger row still reads "Detector 60 rows ... seven mutants zero sweeps ... Owes
  pass 2"; it should carry the 78-row repair and this pass.
