You are reviewing a re-dating of eleven dated test exemptions (GXemul change #550) before it is committed.  Read-only
review.  Read `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\exemptredate_20260925\p1_brief.md`: it inlines
every fact, the exact three-file diff and the measurements.  The tree is `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\`;
ignore any other `src/`.  Scope your reading to that brief, `GXEMUL-SEC/regress/*.c`, `*.py`, `*.sh` and
`GXEMUL-SEC/tools/pipeline/check_probe_wiring.py`; do not read `tools/pipeline/ledger.json` or other `regress/artifacts/`
directories.

FIRST LINE: `VERDICT: <SHIP | SHIP WITH CHANGES | DO NOT SHIP>`, then numbered findings.
1. For each re-dated entry, is the stated reason true of the tree today?  Check it against the files.
2. What is the smallest edit to this diff that the checker, its selftest and gate 2 would all still pass, while an entry
   no longer falls due alone, on a date someone chose?
3. Is there an entry that should be DELETED rather than re-dated, because its prerequisite already exists?
Say plainly what is a reading and what is a measurement.  No files may be changed.
