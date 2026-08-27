"""ORACLE CORRECTION, step 1: re-pin `row_stale_phase_write`'s liveness assertion.

The rule is about ORDER.  Re-pin FIRST, measure the COMMITTED build RED under the new
expectation, and only THEN change the code -- because a re-pin done after the fix is
observationally identical to fitting the test to the binary.

WHAT CHANGES.  The row's liveness control currently asserts the DEFECT state: that the
phase is still PHASE_CMDOUT after a WRITE command.  That was correct when it shipped --
it stopped the row passing vacuously.  Option F resets the phase, so the assertion
inverts.

WHAT DOES NOT CHANGE.  The row's other two assertions -- no CDB dispatch, and the sector
survives -- are about the DISPATCH GUARD, not the phase, and stay exactly as they are.
They must still red under the phase-only mutant afterwards, or this round has traded a
real oracle for a tautology.

The re-pin is deliberately `!= PHASE_CMDOUT` rather than a specific value: what the round
establishes is that the phase does not survive a new command, and pinning WHICH value it
takes would over-specify a choice the fix has not made yet.
"""
import io

NL, T = chr(10), chr(9)
P = r"C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\diff_wdc_identify.c"
s = io.open(P, encoding="utf-8", newline="").read()

OLD = (T + "rows ++;" + NL +
       T + "if (d.atapi_phase != PHASE_CMDOUT || d.atapi_cmd_in_progress != 0 ||" + NL +
       T + "    d.write_in_progress == 0) {" + NL +
       T*2 + "printf(\"  FAIL %-38s phase %i flag %i wip %i" + chr(92) + "n\"," + NL +
       T*3 + "\"LIVENESS: stale CMDOUT with a write\"," + NL +
       T*3 + "d.atapi_phase, d.atapi_cmd_in_progress," + NL +
       T*3 + "d.write_in_progress);" + NL +
       T*2 + "failures ++;" + NL +
       T + "} else {" + NL +
       T*2 + "printf(\"  ok   %-38s phase 0x%x" + chr(92) + "n\"," + NL +
       T*3 + "\"LIVENESS: stale CMDOUT with a write\", d.atapi_phase);" + NL +
       T + "}" + NL)
assert s.count(OLD) == 1, "liveness anchor %d" % s.count(OLD)

NEW = (T + "/*  *** ORACLE CORRECTION, 2026-08-27.  THIS ROW USED TO PIN THE DEFECT." + NL +
       T + "    The old assertion was:" + NL +
       T + "" + NL +
       T + "      LIVENESS: stale CMDOUT with a write   -- wants phase == PHASE_CMDOUT" + NL +
       T + "" + NL +
       T + "    and it was CORRECT WHEN IT SHIPPED.  A phase-only dispatch guard has to" + NL +
       T + "    be shown a state where the phase is stale, or the row proves nothing;" + NL +
       T + "    pinning that state is what stopped it passing vacuously. ***" + NL +
       T + "" + NL +
       T + "    `#479` RESETS THE PHASE at the top of `wdc_command`, so the assertion" + NL +
       T + "    inverts: after a new command the previous command's phase must NOT" + NL +
       T + "    survive.  A seat asked whether the fix would break this row before any" + NL +
       T + "    code was written, which is the only reason this is an oracle correction" + NL +
       T + "    and not a laundering." + NL +
       T + "" + NL +
       T + "    PROVENANCE, quoted rather than summarised so a future seat can" + NL +
       T + "    re-derive it -- `wdc_command()` opens:" + NL +
       T + "" + NL +
       T + "        d->cur_command = idata;" + NL +
       T + "        d->atapi_cmd_in_progress = 0;" + NL +
       T + "        d->error = 0;" + NL +
       T + "" + NL +
       T + "    It clears the flag and the error and NOT the phase.  That is the" + NL +
       T + "    defect; this row is its oracle." + NL +
       T + "" + NL +
       T + "    `!= PHASE_CMDOUT` and not a specific value ON PURPOSE: what the round" + NL +
       T + "    establishes is that the phase does not SURVIVE a new command.  Pinning" + NL +
       T + "    which value it takes would over-specify a choice the fix has not made." + NL +
       T + "" + NL +
       T + "    THE OTHER TWO ASSERTIONS IN THIS ROW ARE UNCHANGED -- they are about" + NL +
       T + "    the dispatch guard, not the phase, and they must still red under the" + NL +
       T + "    phase-only mutant afterwards.  A re-pin that removes the last failing" + NL +
       T + "    row is not finished.  */" + NL +
       T + "rows ++;" + NL +
       T + "if (d.atapi_phase == PHASE_CMDOUT || d.atapi_cmd_in_progress != 0 ||" + NL +
       T + "    d.write_in_progress == 0) {" + NL +
       T*2 + "printf(\"  FAIL %-38s phase %i flag %i wip %i" + chr(92) + "n\"," + NL +
       T*3 + "\"a new command does not leave CMDOUT\"," + NL +
       T*3 + "d.atapi_phase, d.atapi_cmd_in_progress," + NL +
       T*3 + "d.write_in_progress);" + NL +
       T*2 + "failures ++;" + NL +
       T + "} else {" + NL +
       T*2 + "printf(\"  ok   %-38s phase 0x%x" + chr(92) + "n\"," + NL +
       T*3 + "\"a new command does not leave CMDOUT\", d.atapi_phase);" + NL +
       T + "}" + NL)

lbl = "a new command does not leave CMDOUT"
assert len(lbl) < 38, "label %d chars" % len(lbl)
print("  label ok (%d < 38): %s" % (len(lbl), lbl))

s = s.replace(OLD, NEW, 1)
io.open(P, "w", encoding="utf-8", newline="").write(s)
print("  re-pinned. The COMMITTED build must now go RED on this row.")
