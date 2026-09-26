# DEDICATED ADVERSARIAL JOB -- #551d's own pass (read-only)

Read `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\wdcidselfcheck_20260925\pass551d\pass551d_brief.md` in full --
the test harness self-check's second repair, with the whole self-check, the trailer, the diff and the measurement
inlined, and every earlier seat's findings shared in its section 3.  The tree is `GXEMUL-SEC/` only; its working
`regress/diff_wdc_identify.c` is an EARLIER version, so review the inlined code.

You are the ADVERSARY for this one question: **the smallest edit to the #551d version of
`regress/diff_wdc_identify.c` that keeps every gate-2 check green (the G line, the `@@SELFCHECK@@` token, the
`high byte` count of 1, the one `WDC_IDENTIFY_PASS`, the self-mutant lane) while a row that goes through `chk()` or
`row_cmp()` can no longer fail -- OUTSIDE the disclosed classes** (a test keyed on a value, a name, a position or
the self-check's own phase that the probes do not share; an edit of the code that feeds the comparators; an edit of
the self-check block itself; a reset of BOTH tallies).  Last time you and the Opus seat found the two-character
trailer edit; this repair makes the verdict and the exit status read `cmp_fails` directly and makes every probe
check `cmp_fails`'s change.  **Attack THAT.**  For each candidate, say which gate-2 check it survives and why, and
name the row it silences.  If none exists, list every shape you tried -- a zero needs its denominator.

Open with `VERDICT: <SHIP | SHIP WITH CHANGES | DO NOT SHIP>`, then the findings, each with the grep anchor you
checked.  Do not write any file.
