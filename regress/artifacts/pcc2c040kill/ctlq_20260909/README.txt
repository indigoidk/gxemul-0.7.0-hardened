ctlq_20260909 -- `pcc2c040ctlq': the accept row that could not fail, MEASURED and REPAIRED
Opus 5 measuring seat.  Follow-up under #512 (pcc2c040kill), filed from the 2026-09-09 Opus
review seat's Q5 finding (../opus_review_20260909.md).

WHAT THIS DIRECTORY IS
  The measurement that converts that review's PREDICTION into a result, plus the repaired
  instrument.  The review said in terms that the grade "should follow the measurement, not this
  prediction -- writing a predicted sweep into a measured column is the frozen-number class."
  This is that measurement.  The prediction held exactly.

THE DEFECT IN THE DETECTOR (not in the emulator -- #512's fix is correct and unchanged)
  regress/pcc2_c040_probe.py, the `genctl ctlq' CONTROL row:

      ctl_saw_c040 = ("C040 interrupt assertions" in t)
      row("genctl ctlq", "no" if not ctl_saw_c040 else "yes", "no",
          "CONTROL: the benign write must NOT reach the C040 arm")

  "C040 interrupt assertions" is the PRE-FIX fatal() text.  #512 replaced it with the announce
  the probe binds twenty lines later as SAYS = "C040 (MC68040 EIPL)".  So on every post-fix build
  `ctl_saw_c040' is False no matter what the device does, and the row is green unconditionally.

  That matters because of WHICH row it is.  #512 removed a host-fatal guard, and the
  de-escalation clause makes the detector shipping with such a fix pin the ACCEPT SIDE of the
  removed predicate.  `genctl ctlq' is the sole carrier of that obligation for the benign bit:
  it drives BENIGN = 0x10 through the identical instruction, register and width, and is exactly
  the row that must redden when the guard grows.  The accept-row failability rule: a row
  "is not discharged by existing -- it is discharged by a MEASURED KILL".

THE MEASUREMENT
  M_widen, one line, guard-only (the latch operand is a compile-time constant the guard cannot
  feed, so guard-only is the form the carrier's discriminator selects here):

      -	if (d->pcctwo_reg[PCCTWO_GENCTL] & PCC2_C040) {
      +	if (d->pcctwo_reg[PCCTWO_GENCTL] & (PCC2_C040 | 0x10)) {

      SHIPPED probe   16/16   *** CLEAN SWEEP ***     shipped_M_widen.raw
      REPAIRED probe  15/16   genctl ctlq red         repaired_M_widen.raw
      REPAIRED @ base 16/16                           repaired_BASE.raw

  Full table, spot checks and the mtime order proof: TABLE.out.

THE REPAIR -- one string, no new row, no new session, denominator unchanged at 16
  ctl_saw_c040 = ("C040 interrupt assertions" in t)   ->   ctl_saw_c040 = (SAYS in t)
  plus a hoist of the SAYS definition above the CONTROL block (so there is ONE binding for the
  announce text rather than a second literal that would drift), plus the dated provenance comment
  the oracle-correction rule requires.  Total: 1 functional line, 3 lines moved, a comment block.

  Apply it to the tracked file from ./pcc2_c040_probe.REPAIRED.py.

  *** DO NOT ALSO "FIX" `c040 attrib'. ***  It keys on the SAME retired string and is CORRECT
  that way: the death it attributes is the REINSTATED pre-fix kill (M_b_reinstate), which carries
  the old text.  The two rows key on one string for opposite and both-valid reasons -- the
  2026-09-09 review's hygiene note 3, confirmed here and worth repeating because the obvious
  tidy-up would destroy a measured kill.

WHAT THE REPAIRED ROW DOES AND DOES NOT PIN -- stated rather than glossed
  It pins the accept side against a guard widened onto a GENCTL bit whose value THIS SESSION
  drives, which is 0x10.  It does not pin every widening:
    * onto MIEN (0x02)  -- caught, but by accident and elsewhere: `irq live' suppresses.
    * onto DR0  (0x80)  -- caught by NO row in this detector.
  That bound is written into the probe's own comment so a future reader gets it at the row rather
  than from this file.  It is clause-(e) coverage debt, not a floor breach: nothing drives 0x80.

GRADING -- for the main loop to rule on, with the measurement now in hand
  The review said "L3 (undischarged obligation) at minimum and arguably L2".  What the
  measurement adds: the row is the SOLE CARRIER of the de-escalation accept obligation for the
  benign bit, and a vacuous sole carrier makes the round's record false -- which is L3 by its
  definition.  It is also a clean sweep of the shipped detector by a mutant inside the accept-side
  enumeration the fix itself created, which is the L2 shape.  I do not rule between them; the
  disposition is the same either way (repair the detector), and both are in-round obligations
  rather than filings.  The grade is the main loop's.

FILES
  pcc2_c040_probe.REPAIRED.py   the repaired instrument (md5 cbe1945cffe7f3441cc93d5489bdc692)
  TABLE.out                     the kill table, spot checks, order proof, hygiene
  shipped_BASE.raw              shipped probe @ base            16/16
  shipped_M_widen.raw           shipped probe @ M_widen         16/16   THE HOLE
  repaired_BASE.raw             repaired probe @ base           16/16
  repaired_M_widen.raw          repaired probe @ M_widen        15/16   THE KILL
  repaired_M_return.raw         repaired probe @ M_return       14/16
  repaired_M_latchinside.raw    repaired probe @ M_latchinside  15/16
  repaired_M_d1_noassert.raw    repaired probe @ M_d1_noassert  14/16
  00_setup.sh                   clone + baseline identity + baseline rebuild
  mutate.py                     the mutator; restores from SEC first, NOT-FOUND is a hard FAIL
  run_mutant.sh                 restore -> mutate -> rm .o -> make -> freshness -> run frozen probe
  make_repaired.py              generates the repaired probe from the frozen shipped copy
  99_restore.sh                 restore, rebuild, two-part clearance, clear the sentinel

REPRODUCING
  bash 00_setup.sh
  bash run_mutant.sh M_widen <frozen-shipped-probe> shipped_M_widen
  bash run_mutant.sh M_widen <repaired-probe>       repaired_M_widen
  bash 99_restore.sh
  The scripts carry absolute /tmp/gxopusctlq and /mnt/c/... paths from this run; they are kept as
  the RECORD OF WHAT RAN, not as a portable harness.

NO TRACKED FILE WAS EDITED BY THIS SEAT.  All work was in the scratch clone; build/ was read by
cp -a and never written, and was verified cmp-clean with a fresh binary afterwards.
