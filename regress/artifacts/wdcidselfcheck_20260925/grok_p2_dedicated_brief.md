# DEDICATED ADVERSARIAL JOB -- #550 + #551 PASS 2 (read-only)

Read `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\wdcidselfcheck_20260925\p2_brief_550_551.md` in full; it is
the pass-2 brief for two harness rounds, with both final diffs inlined.  The tree is `GXEMUL-SEC/` only.

You are the ADVERSARY, not a reviewer.  Two jobs, and nothing else:

1. **#551: construct the smallest edit to `regress/diff_wdc_identify.c` (as the brief shows it) that keeps gate 2 GREEN
   -- every row, the G row, the H row, the `high byte` pin, the self-mutant lane -- while a row that goes through `chk()`
   or `row_cmp()` can no longer fail.**  Exclude the one already disclosed (a rows- or name-keyed test inside a
   comparator placed before its `rows ++`).  For each candidate, say which gate-2 grep it survives and why, and name the
   row it silences.  If none exists, say so and say what you checked.

2. **#550: find the entry whose NEW reason is still false.**  For each of the ten `EXEMPT` entries and gate 2's
   `ieee_store`, open the probe and the gate the reason names and check the reason against them.  A reason that names
   owed work which already exists, or a gate home that does not exist, is a finding.

Open with `VERDICT: <SHIP | SHIP WITH CHANGES | DO NOT SHIP>` for each round (two lines), then the findings, each with
the file and the grep anchor you checked.  Do not write any file.
