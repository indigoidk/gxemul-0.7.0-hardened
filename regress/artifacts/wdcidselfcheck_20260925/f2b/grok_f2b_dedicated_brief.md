# DEDICATED ADVERSARIAL JOB -- #550 + #551 §F2 on pass 2 (read-only)

Read `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\wdcidselfcheck_20260925\f2b\f2b_brief_550_551.md` in full --
the consolidated findings of pass 2, my disposition on each, and the repair diffs.  The tree is `GXEMUL-SEC/` only.

You found two of these findings yourself on pass 2 (the Alpha "no gate runs an Alpha machine" sentence, and the
value-keyed `want-165`).  Be HARDER on the dispositions of your own findings than on anyone else's.

Two jobs, nothing else:

1. **Break the repair.**  In the FINAL `diff_wdc_identify.c` (#551b: the wide `row_cmp()` probes and the `sc_g` verdict
   flag), find the smallest edit that keeps gate 2 GREEN -- the G line, the `@@SELFCHECK@@` token, the `high byte` pin, the
   self-mutant lane, the row-name pins -- while a covered row can no longer fail, OUTSIDE the disclosed classes (a
   value-, name- or position-keyed test inside a comparator; an edit of the code that feeds them).  Also: does `sc_g`
   change any healthy run's output?
2. **Find the v3 sentence that is still false.**  For each #550 v3 hunk, check the new sentence against the file it
   names.  A correction that writes a new false sentence while fixing an old one is the finding.

Open with `VERDICT #550: <SHIP | SHIP WITH CHANGES | DO NOT SHIP>` and `VERDICT #551: <...>`, then the findings, each
with the file and grep anchor you checked.  Do not write any file.
