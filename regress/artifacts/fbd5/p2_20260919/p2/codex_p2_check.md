# Dedicated codex reading, #545 (fbdeclinefive) PASS 2 -- the smallest edit that breaks the shipped detector and still passes

Read `C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\fbd5\p2\brief_fbd5_p2.md` (the pass-2 brief: the design, settled premises,
the diff inline or by frozen path, the kill table), then the patched tree `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\`:
`src/devices/dev_footbridge.c`, `regress/footbridge_sites_probe.py`, `regress/fbpending_drain_probe.py`,
`regress/fbpending_witness.py`, `regress/diff_footbridge.c`, and the footbridge section of `regress/gate_arm.sh`.  Do not read
`regress/artifacts/`, `tools/pipeline/ledger.json`, CHANGELOG.md or OUTSTANDING_BUGS.md.  Read-only; run nothing.
Ordinary engineering language: declines, terminating calls, latches, detector rows.  VERDICT LINE FIRST.

## QUESTIONS
1. For each of the five declined sites and each predicate the fix depends on (the five latch tests, `writeflag`), name the
   smallest source edit that leaves EVERY row green -- the guest rows (sites probe arm S, legs H1/H2), the offline P-rows
   and the gate pins -- and say which row you expected to catch it and why it does not.  If none exists for a site, say so
   and name the row that closes it.  Candidates the table did NOT build are listed in the brief's Q2.
2. The harness legs: in each of the three launchers, is `dead` observed before teardown, is the prologue check scored, and
   what is the smallest edit to a leg that keeps it green while proving nothing?
3. The gate pins: can a duplicated green line, a reordered row, or an edited label satisfy any pin while the underlying
   row is red or absent?
4. Anything else you found while verifying (standing licence).
End with: model, files read, nothing run.
