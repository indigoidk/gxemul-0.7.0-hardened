# DEDICATED ADVERSARIAL JOB -- #551c's own pass (read-only)

Read `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\wdcidselfcheck_20260925\pass551c\pass551c_brief.md` in full --
the test harness self-check's repair, with the diff and its measurement inlined.  The tree is `GXEMUL-SEC/` only.

You are the ADVERSARY for this one question: **the smallest edit to the #551c version of
`regress/diff_wdc_identify.c` that keeps every gate-2 check green (the G line, the `@@SELFCHECK@@` token, the
`high byte` count of 1, the self-mutant lane) while a row that goes through `chk()` or `row_cmp()` can no longer
fail -- OUTSIDE the disclosed classes** (a test keyed on a value, a name, a position or the self-check's own phase that
the probes do not share; an edit of the code that feeds the comparators; an edit of the self-check block itself; a reset
of BOTH tallies).  For each candidate, say which gate-2 check it survives and why, and name the row it silences.  If
none exists, list the shapes you tried.

Open with `VERDICT: <SHIP | SHIP WITH CHANGES | DO NOT SHIP>`, then the findings, each with the grep anchor you checked.
Do not write any file.
