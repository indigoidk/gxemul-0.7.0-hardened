You are reviewing a test-coverage change in a C hardware emulator (GXemul) before it is committed.  Read-only review.

Read `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\fbdrainwire_20260924\p2_brief.md` first: it inlines the
whole diff (6 files, 9 hunks, against HEAD) and every measured premise.  The tree is
`C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\` -- ignore any other `src/` directory.  In the working tree,
`regress/gate_arm.sh` and `tools/pipeline/check_probe_wiring.py` also carry another unit's uncommitted lines; review the
diff in the brief, which is exactly what will be committed.

FIRST LINE: `VERDICT: <SHIP | SHIP WITH CHANGES | DO NOT SHIP>`, then numbered findings.

Your job is the adversarial one, and only that:

1. For each property the diff CLAIMS -- the gate-14 rows (the four-timer drain block and its contract comment) and
   gate 2's R6 row in `regress/diff_fbpending_bound.c` -- name the SMALLEST concrete edit (file, line, exact tokens) to
   `src/devices/dev_footbridge.c`, to `regress/fbpending_drain_probe.py`, or to the gate block itself, that breaks the
   property and still passes every row.  Say whether the contract's NOT CLAIMED list already discloses it.
2. Check every sentence the diff ADDS against the source and against the measured premises.  A sentence that is true only
   for the case measured, or that overstates what a row observes, is a finding.  Pass 1 found two such sentences in
   drafts that were written to correct false sentences.
3. Check the shell in the gate block: quoting, `continue` inside the loop, `|| fdrc=$?`, the `grep -x` and `grep -E`
   patterns against the probe's real output format (`"  %-4s %-46s %s"` rows, `FBDRAIN_*=` lines), the awk field.

Settle by reading the files or by arithmetic.  Say plainly what is a reading and what is a measurement.  No files may be
changed.
