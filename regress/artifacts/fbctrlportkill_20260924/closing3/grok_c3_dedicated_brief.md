# DEDICATED ADVERSARIAL JOB -- #549 VERIFYING PASS (read-only)

Read `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\fbctrlportkill_20260924\closing3\c3_brief.md` in full: the
repair's own pass, with the v4 -> v5 probe diff, the gate diff and kill table 5 (212 edits, every prediction held)
inlined.  The tree is `GXEMUL-SEC/` only.  The probe is `regress/fbctrl_port_probe.py`; the device is
`src/devices/dev_fbctrl.c`.

You found the X3 truncation alias and X7's missing name row on the last pass.  You are the ADVERSARY here, not a
reviewer.  Two jobs, nothing else:

1. **Find a clean-sweep mutant of the FIX's floor that scores 111/111.**  The floor: the PORT arm's access direction,
   `idata >= DEV_FBCTRL_NPORTS` (value, width, class), `!d->warned_port`, and what the arm writes to `current_port` --
   alone or at a joint cell of those.  Write the edit as a one-line change to the arm (the arm is inlined in the brief's
   section 2), name the row(s) you expect to stay green and WHY each cannot see it.  If you find none, list the edit
   shapes you tried -- a zero is only a zero with its denominator.
2. **Find a cell the header's enumeration CLAIMS that no row holds**, or a row credited to a cell it cannot see.
   Read the CONTRACT in the probe diff and check each listed holder against the session's program in the probe.

Open with `VERDICT: <SHIP | SHIP WITH CHANGES | DO NOT SHIP>`, then the findings, each with the file and grep anchor.
Do not write any file.
