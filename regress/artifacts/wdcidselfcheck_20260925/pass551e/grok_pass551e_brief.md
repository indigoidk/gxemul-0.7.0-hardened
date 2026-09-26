# DEDICATED ADVERSARIAL JOB -- #551e's enumeration-verifying pass (read-only)

Read `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\wdcidselfcheck_20260925\pass551e\pass551e_brief.md` in full --
the test harness self-check after the adjudication of #551d's pass, with the contract (four disclosed classes), the
self-check with its new call-count pin, the trailer, the diff and the measurement inlined.  The tree is `GXEMUL-SEC/`
only; its working `regress/diff_wdc_identify.c` is an EARLIER version, so review the inlined code.

You are the ADVERSARY for two questions:

1. **The smallest SINGLE edit** to the #551e file that keeps every gate-2 check green (the printed failure count 0, the
   one `WDC_IDENTIFY_PASS`, the sixteen named rows, `high byte` once, the G line, the `@@SELFCHECK@@` token, the
   self-mutant lane) while a row that goes through `chk()` or `row_cmp()` can no longer fail -- OUTSIDE the four classes
   the contract names.  Or a class of green edits the contract does not name.  Last pass you found the trailer scoring
   the difference; that is now class (3).  **Attack what is not in a class.**
2. **The adjudication's caution:** can an IN-FILE pin on `main()`'s trailer survive one inlining edit AND one inserted
   conditional reset (`if (failures == cmp_fails) failures = cmp_fails = 0;`)?  If you can construct one, show it.

For each candidate, say which gate-2 check it survives and why, and name the row it silences.  If none exists, list every
shape you tried -- a zero needs its denominator.  Open with `VERDICT: <SHIP | SHIP WITH CHANGES | DO NOT SHIP>`.  Do not
write any file.
