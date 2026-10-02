# ADJUDICATION PASS -- PREDICTION, WRITTEN BEFORE THE BUILD

Written at the timestamp of this file.  The build logs and probe logs that follow are all
strictly later; that mtime ordering is the order discriminator, per the oracle-correction rule.

Base is ALREADY measured at 188/188 (opus_pass1_work/logs/probe_base.raw, CRIMEP_DONE).

## What is being settled

O4 DERIVED, without a run, that on the decline x latch-SET axis "REV and TIME are open".
TIME was MEASURED open (`M3_timelatch', 188/188).  REV was NOT measured.  A derivation that
has been right once is still a derivation.

## M5_revlatch -- the REV twin of M3

    goto moved inside the latch block; then  if (relative_addr != CRIME_REV) goto crime_declined;

PREDICTION: **ESCAPE, 188/188.**  Warrant: the REV arm's body is the pc-window redirect, and
the probe's REV-window rows (`revP ...', `free revP said') drive their refusal FIRST in the
session, so the latch is CLEAR when they measure and the mutant declines exactly as the fix
does.  No row drives a SECOND refusal at REV with the window pc.

## M6_istlatch -- THE NEGATIVE CONTROL, and the run is worthless without it

    same shape, INTSTAT instead of REV.

PREDICTION: **KILLED.**  Warrant: `M1_gotolatch' (the unrestricted form) killed 10 rows across
CONTROL/INTSTAT/INTMASK/default, so rows exist that reach INTSTAT with the latch already set.

WHY THE CONTROL IS NOT OPTIONAL: without it, an M5 escape is ambiguous between
  (a) REV is an open cell of the label x latch product   -- the claim, and
  (b) a single-label latch-conditional goto is invisible to this detector PER SE,
and (b) would make M3's escape a much larger finding than the round has recorded.
If BOTH escape, the finding is (b) and O4's cell count is beside the point.

## Falsifier

If M5 is KILLED, O4's REV half is WRONG and the class-closure demand shrinks to one cell (TIME).
