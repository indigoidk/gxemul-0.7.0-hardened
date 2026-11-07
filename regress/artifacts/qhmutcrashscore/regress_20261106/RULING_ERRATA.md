# RULING_ERRATA.md -- corrections to the regress ruling beside it, as its own adjudication directs

`RULING.md`, beside this file, is Fable 5.1's regress ruling on `qhmutcrashscore` as written on 2026-11-06, banked byte
for byte.  Two confirming reviews of it -- GPT-6 Astra's (`reviews/codex_ASTRACONF_KDC.txt`, six points) and Grok 4.7's
(`reviews/grok_KDC.txt`, four) -- found its prose looser than its checks.  Fable 5.1's adjudication of them (`ADJ_KDC.md`,
answering `ADJ_KDC.brief.txt`: `FABLEADJ_KDC: 10 ACCEPTED 0 REJECTED VERDICT:LAND-AFTER-RECORDS`) accepted all ten points
and listed eight corrections to the ruling, its R1.1 to R1.8.  They are here, beside the ruling rather than inside it, by
the coordinator's instruction of 2026-11-06.  Each item quotes the sentence it refutes, verbatim with its line in
`RULING.md`, then gives the correction in the adjudication's words.  None changes a score, a kill or the floor count:
floor breaches 0, VERDICT LAND unchanged.  Written by the landing kit (an Opus 5.5 agent) from `ADJ_KDC.md`; paths are
relative to `regress/artifacts/qhmutcrashscore/` unless they name the kit.  The ruling and the adjudication call the
round `#585`, the number the kit was built with when they were written; it lands under the number in its own CHANGELOG
heading, because another round took `#585` first.

## E1 (R1.1; Astra 6, Grok 2) -- the unit's file count

Refutes:
* `:7` -- "the REVIEWED build stages it (`_scratchpad/wkdc/landing/unit/files/`, 88 files)"

Correction: 78 files under `unit/files/` at review time (the kit's pretest log, `_scratchpad/wkdc/landing/PRETEST_reviewed.out:2`, "staged: 78 paths (unit: 78)" -- a kit file, not in the repository); 88 was the whole `unit/` (+8 under `insitu/`, `commit.msg`, `UNIT.json`).  The unit grew to 79 when the ruling and its question were banked (less `fable_queue.md`, which regenerates to HEAD's bytes once this round holds nothing), and again when the adjudication was.

## E2 (R1.2; Grok 1) -- "byte-identical" without its qualifier

Refutes:
* `:16` -- "the STAGED gate's whole output in the Q2 legs is byte-identical to the measured copy's W2_FIX output on allcrash, mixed and allkill"
* `:25` -- "`M_q2b`'s gate output is byte-identical to HEAD's on allcrash, mixed AND allkill" (check 10; Grok's review and the adjudication cite it as `:29`, which is check 14's line)
* `:37` -- "`M_q2b` reproduces HEAD's gate output byte for byte on"
* `:103` -- "cite `M_q2b`'s byte-identity to HEAD under (b)" (Grok's review and the adjudication cite it as `:104`)

Correction: the gate's own output SECTION (what `wkdc_20261105/controls/compare.py:21-25` scores) is byte-identical on all three stub sets; the whole log differs in the `gate script:` header, the ground-truth section's shell crash reports (pids, driver path) and the `W2_GATE3_DONE` tag -- as check 7 said.

## E3 (R1.3; Astra 2) -- Argon's Q2 claim, quoted as words it did not write

Refutes:
* `:24` -- "so the seat's "keeps every leg green" is false"

Correction: the seat's completed-set claim (`allkill` and `real` stay green, `landing_20261105/pass2/argon_kdc_p2.txt:18`) is TRUE and measured; its dead-run claim (crashed runs score as detections) is FALSE -- the literal edit falls through and prints `0` twice (`landing_20261105/pass2/q2/g3/W2_M_q2a.allcrash.log:18-19`), 11 of 19 rows red.  'Keeps every leg green' was the coordinator's paraphrase, not the seat's words.

## E4 (R1.4; Astra 3, Grok 3) -- what the FINAL in-situ sentence asserts against what the script checks

Refutes:
* `:28` -- "`build_kit.py` refuses FINAL without a log ending `INSITU_G3_SUMMARY PASS` / `INSITU_G3_DONE`"
* `:28` -- "asserts exactly what `insitu_gate3.sh` checks"

Correction: it asserted MORE on one point and LESS on two: 'ending `DIFF_FAIL`/`DIFF_PASS`' where the script as reviewed tested presence at line start (`grep -aq '^DIFF_PASS'`, `grep -aq '^DIFF_FAIL'`); silent on the crash leg's control row and on `build/`'s input md5s, both of which the script fails on.  The FINAL refusal is the kit's `records_wkdc.py` (run by `build_kit.py`), and it required `INSITU_G3_SUMMARY PASS` anywhere plus `INSITU_G3_DONE` last, not the terminal pair.  APPLIED IN THE UNIT, by the adjudication's R2.2 and R2.5: `insitu_gate3.sh` (committed beside `INSITU_G3.out`) now tests each run log's LAST non-blank line, so the sentence's 'ending' is what the script checks; the sentence also names the control row and the md5s; and the FINAL build requires the log's last two non-blank lines to be exactly `INSITU_G3_SUMMARY PASS` then `INSITU_G3_DONE`.

## E5 (R1.5; Astra 5) -- check 14's predicted mechanism for a moved `rc`

Refutes:
* `:29` -- "move `local rc=$?` below the grep -> `rc=1` against the seven pinned `rc=136` rows"

Correction: -> `$rc` unbound in the guard under `set -u` (the gate's `set -u`; `rc` is declared only by `local rc=$?`): the `$(...)` subshell dies, `got=` is empty, the seven pinned rows red.  The conclusion -- the cell lands on existing rows -- is unchanged; the mechanism was wrong.

## E6 (R1.6; Astra 1) -- floor (c) graded one object where its three siblings graded another

Refutes:
* `:41` -- "* **(c)** null medium: for a gate that runs a detector, a detector that never answers"
* `:46` -- "A clause saying so in the block would preempt the objection; not required."

Correction: two objects, each in a carrier form.  (c) for GATE 3 as a detector: MEASURED at `W2_FIX.allcrash.log` / `W2_FIX.mixed.log` (the differential never answers; the fixed gate reds every such run).  (c) for the W2 CONTROLS, the detector defending this fix: BY CONSTRUCTION via `compare.py:100-101` (a row whose line is not found reds) and `:103` (the allkill/real SAME rows red when FIX's text is empty against HEAD's non-empty text); null-gate leg NOT RUN.  The construction holds against a LIVE HEAD leg: with both legs dead the allkill/real rows pass (`"" == ""`), the `all([])` shape.  The sentence "A clause saying so in the block would preempt the objection; not required." is WITHDRAWN: the round block now names both objects.

## E7 (R1.7; Grok 4) -- MEASURED stamped over four cells that were only read

Refutes:
* `:48` -- "rest of the DEPENDS-ON closure lands on existing rows (check 14).  MEASURED."

Correction: M_q2a (11 red) and M_q2b (13 red) MEASURED (`landing_20261105/pass2/q2/Q2_CONTROLS.txt`); the other four DEPENDS-ON cells BY READING (check 14), not run; each lands on an existing row.

## E8 (R1.8; Astra 4) -- "pinned nowhere"

Refutes:
* `:79` -- "and is pinned nowhere (PRETEST), so nothing else reds."

Correction: is pinned by no gate or checker in the tree (git grep at HEAD), and IS pinned by the round's own comparators -- `wkdc_20261105/controls/compare.py`'s `gwant` verdict table and `landing_20261105/insitu_gate3.sh`'s four leg-verdict tests (`(15 checks)`, `(7 of 15 checks)`; the adjudication read them at `:78,79,89,93`, before R2.2 moved the script's lines) -- which the eighth mutant's round must update.
