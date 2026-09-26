You are reviewing an error-handling correction in a C hardware emulator (GXemul, change #549) before it is committed.
Read-only review.  Read `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\fbctrlportkill_20260924\p2_brief.md`:
it inlines the whole diff and every measurement.  The tree is `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\`; ignore any other
`src/`.  Scope your reading to `GXEMUL-SEC/src/`, `GXEMUL-SEC/regress/*.py` and `*.sh`, and that brief; do not read
`tools/pipeline/ledger.json`.

FIRST LINE: `VERDICT: <SHIP | SHIP WITH CHANGES | DO NOT SHIP>`, then numbered findings.

1. For each property the diff claims, name the smallest concrete source edit (file, exact tokens) outside the 25
   variants in the brief's table that breaks the property and still passes every detector row; say which row stays green.
2. Check every sentence the diff adds against the source and the measurements; a sentence true only for the measured
   case is a finding.
3. Check the gate-16 shell block: the parse guard, the pins, and the moved kernel check.
Say plainly what is a reading and what is a measurement.  No files may be changed.
