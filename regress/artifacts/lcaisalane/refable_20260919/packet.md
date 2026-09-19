# First-hand re-adjudication: two CLOSED rounds (#530 pass 2 + its adjudication pass, and #538 pass 2)

**Why this exists (measured, 2026-09-19).**  In the two earlier runs of this seat on these rounds, the model ended a
turn with a refusal partway through; the agent tool then finished the answer with a different model
(claude-opus-4-8) and the answer still carried this seat's identity line.  Checked from the subagent transcripts'
per-message `model` and `stop_reason` fields.  So the rulings on record are NOT this seat's.  They are kept as
another model's reading, quoted below so you can agree or disagree with them -- **rule on your own reading of the
evidence; do not defer to them.**

**Vocabulary for your answer, please:** this is ordinary regression-test adequacy review of an open-source emulator's
test suite.  Write "variant" (a one-edit change to the fixed code), "detected / undetected by the table", "the
emulator process terminates", "regression table".  Keep the answer short: two rulings and their reasons.

**Tree:** `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\` at HEAD a11eaac.  Read ONLY the files named below (absolute paths
under that tree unless given in full).  Pristine 2021 copies of `src/` elsewhere under the project root are NOT this
fork.  READ-ONLY: write only your answer file.

## The rule both rulings apply (your own, from #540 pass 1; binding)

An axis is FLOOR when (i) the handler body's own code induces a partition on it -- a test, or an index/selector it
computes from its inputs -- and (ii) that partition flows into an operand of the edited statement or is re-tested on
its output path.  Floor cells owe a table row; anything else is clause (e): disclosed in the test's contract.

## (A) #530 -- the width row of `regress/lca_widewrite_probe.py`, after pass 2

`#530` (commit 8bd97e4) made `DEVICE_ACCESS(lca_isa)` in `src/devices/dev_lca.c` service a WIDE write (a len > 8
chunk, which the guest's PROM GETENV call produces) instead of declining it, and shipped ONE width row: one 16-byte
write at lane 3.  At pass 2 a measuring seat built seven one-edit variants of the fixed handler that the row does not
detect (`regress/artifacts/lcalenzerodrop/opus_p2_20260918/RESULTS.txt`, with `PREDICTIONS.txt` and `variants/`).

**The ruling on record (another model's):** exactly ONE floor cell -- variant `vc`, `&& (len <= 8 || (P & 3) == 3)`,
services wide writes at the rowed lane only.  LANE is a floor axis because the body's `data[ofs]` distinguishes all
four lanes, so the floor is {write arm} x {lane 0-3}.  The other six are disclosed against already-ruled classes:
width cut-offs above 16 (the body tests `len` only against 0), ports (`p_port10`), the discarded sparse bits
(`lcaisasize`), chunk position (a stateless handler).  "The popular two-cell fix is a covering, not a closure."

**Question A:** under the rule above, which of the seven are floor cells and which are disclosed?  Agree or disagree
with each disposition, reading the handler (`src/devices/dev_lca.c`, `DEVICE_ACCESS(lca_isa)`) yourself.

## (B) #538 -- the closure that shipped for (A)

`#538` (commit a11eaac, detector-only) extended `regress/lca_widewrite_probe.py` to four lane cells, one per lane,
each in its own emulator session, 13 rows.  Its regression table:
`regress/artifacts/lcalenzerodrop/closure538_20260918/` -- `PRETABLE.out` (predictions, written first),
`logs/TABLE.out` (the measured legs), and `rerun_20260919_0030/` (the same table re-run on the final instrument).

**The ruling on record (another model's):** "CLOSES -- the lane floor is 0/4 open (vc_ne0..3 each detected exactly by
its own lane's row; the lane-1 covering variant detected at `low16`); contingent on a one-instrument re-run" (the
re-run is the directory above).

**Question B:** does the shipped detector close the lane floor from (A) -- is any floor cell left undetected?  Check
the measured table against the predictions yourself.

## Your answer

Write it to `C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\refable_530_538\fable5_rulings.md` and return it as your final
message.  Open with these three lines:

    FABLE_SEAT_ALIVE_20260919_REFABLE
    <your exact model id> | <the first line of C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\CHECKPOINT.md, verbatim>
    VERDICT: A <AGREE | DISAGREE: which> ; B <CLOSES | DOES-NOT-CLOSE: which cell>

Then the reasons, each claim marked MEASURED (name the file), READ (file:line) or INFERRED.
