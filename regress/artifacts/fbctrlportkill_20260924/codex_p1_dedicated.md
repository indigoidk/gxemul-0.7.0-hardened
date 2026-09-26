You are reviewing a proposed error-handling correction in a C hardware emulator (GXemul) before it is written.
Read-only review.

Read `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\fbctrlportkill_20260924\p1_brief.md` first: it inlines the
device source (`src/devices/dev_fbctrl.c`), a measured reproduction, the proposed change and the proposed test rows.  The
tree is `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\` -- ignore any other `src/` directory.  Scope your reading to
`GXEMUL-SEC/src/` and `GXEMUL-SEC/regress/*.py` and `regress/*.sh`; do not read `regress/artifacts/` (other than the one
brief above) or `tools/pipeline/ledger.json`.

FIRST LINE: `VERDICT: <PROCEED | PROCEED WITH CHANGES | DO NOT PROCEED>`, then numbered findings.

Your job is the adversarial test-coverage review, and only that:

1. For the proposed change (the PORT arm refuses a selector >= 8 and keeps the previous one; the DATA arm is unchanged),
   and for each proposed test row, name the SMALLEST concrete edit to the device code (file, exact tokens) that breaks
   the intended behaviour and still passes every proposed row.  Say which row you expect to stay green.  Cover the
   comparison (operator, operand, width, signedness), the once-only latch, and the store.
2. Enumerate what can reach `case DEV_FBCTRL_PORT` and `case DEV_FBCTRL_DATA` on a MIPS test machine: access widths
   (1, 2, 4, 8), offsets inside the 0x20-byte window, byte order, and the `idata` each produces.  After the change, is
   there any sequence of guest accesses that still reaches the DATA arm's terminating call?
3. Check every factual sentence of the brief against the source, including the table of stored values and the claim
   about which machines install the device.  A sentence true only for the case measured is a finding.

Settle by reading the files or by arithmetic.  Say plainly what is a reading and what is a measurement.  No files may be
changed.
