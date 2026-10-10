# Records check, 2026-10-09: confirm or correct two rulings before they are written into the ledger

Open your answer with ONE line: `VERDICT: CONFIRM / CONFIRM WITH CHANGES (<n>) / REJECT -- <one line>`, then one section
per ruling.  This is a records and test-coverage check of the GXemul hardened fork; read the files named below (repo
root `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\`, HEAD `23012be9`).  The working tree carries another session's
uncommitted edits to `src/devices/dev_pcc2.c`: read product code at HEAD (`git show HEAD:src/devices/dev_pcc2.c`).
Ignore any `src/` outside GXEMUL-SEC (pristine 2021 upstream copies).  Please do not simply agree: name any stated fact
that the files contradict, any grade the carrier's written rules do not support, and any record or test row the ruling
leaves out.

## Ruling 1 -- `n6`'s rule question: RULED (a)

The question (tools/pipeline/fable_queue.md, heading `### \`n6\`` in BATCH 8n): is ledger row `n6`'s 2026-08-30 fable5
assess entry (a) a seat answer that re-opened the stage, (b) a single-seat re-read, or (c) an adjudication record?
The ruling and its four reasons: `regress/artifacts/fablequeue8n_20261009/regress_harness/fable5_regress_harness.md`,
section 4.  Check it against `tools/pipeline/ledger.json` row `n6` (entries 3-5), `tools/pipeline/stage_tokens.py`
(`live_holds()`, `is_answer()`), and `regress/artifacts/stagetokens/controls_534/run_controls.py` (the `t_selflate`
case).  The same file's section 1 finding 4 says 365 matrix cells with `d: "OK"` render in the seat-failure class:
check `tools/pipeline/gen_dashboard.py` (`D_CLASS`) and say whether that is right.

## Ruling 2 -- the pcc2 C040 regression table: X floor, W debt

Credited ruling: `regress/artifacts/pcc2c040kill/assertrow_review_20261009/fable5_ruling_v2_20261009.md` (the v1 file in
that directory was written by a different model after a refusal and is NOT credited; `RULING_PROVENANCE.txt`).
Measured there: the committed `regress/pcc2_c040_probe.py` scores 18/18 on the unchanged build (`probe_base.raw`), and
18/18 on each of two one-line variants of the C040 arm in `src/devices/dev_pcc2.c`: (X) `assert = 0;` -> `assert ^= 1;`
(`probe_xor.raw`) and (W) `d->warned |= ...` -> `d->warned = ...` (`probe_eq.raw`); `build_and_run.sh.txt` shows how.
The ruling: X is a floor cell owed a row now (a regress-only follow-up adding one free-running row, `c040 idle`, with a
state control); W is clause-(e) coverage debt, filed MED and disclosed in the probe's contract; the stale comment beside
the C040 arm in `dev_pcc2.c` is corrected by the separate #560 comment batch, not by the follow-up; and ledger row
`pcc2c040assertrow` (state `held`) goes to `in work`, its review hold discharged.
Check against the carrier's rules in `C:\DocumentNoSnc\cc\GXEMUL\CLAUDE.md` (anchors: `DEPENDS ON enumerates exactly
two things`, `A DERIVED INPUT IS GRADED BY WHAT THE BODY TESTS ON IT`, `THE LATE-DISSENT RULE`) and the row's
`hold_question` and entries 0-11.

## Questions
1. For each ruling: which stated fact, if any, do the files contradict?
2. Is X's floor grade and W's debt grade what the carrier's rules, as written, give?  If you disagree, which rule decides it?
3. Is any consequence missing -- a record that must change, a row owed, a disclosure?
4. Anything ELSE you noticed.
