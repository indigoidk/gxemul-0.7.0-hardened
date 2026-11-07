# ADJUDICATION -- qhmutcrashscore (#585), the two confirming reviews of the regress ruling -- Fable 5.1, 2026-11-06

FABLE_LIVE_20261106_ADJ_KDC
# CHECKPOINT -- 2026-11-04 17:0x RUNNING (087a90 sections rewritten; the peer's sections below are untouched)

**Scope.**  Read-only.  Ruling: `_scratchpad/fable_20261106/kdc/RULING.md` (banked in the unit as
`regress/artifacts/qhmutcrashscore/regress_20261106/RULING.md`).  Reviews: Astra `codex_ASTRACONF_KDC.txt` (6 points),
Grok `grok_KDC.txt` (4 points).  Both dissent on records and both keep floor breaches at 0 and the verdict at LAND.  Every
point below was CHECKED against a file, not judged: the nine `diff`s and six `section()` comparisons are mine (python over
the preserved logs, the same `section()` as `controls/compare.py:21-25`); the counts are `find | wc -l`; the rest is
`awk`/`grep -n`.  Nothing built, no gate, no panel.  Repo HEAD `ab39ba0d`; the kit is REVIEWED mode (`BUILD.out:17`),
`INSITU_G3.out` still absent (`BUILD.out:7`).

## The points, one verdict each

| # | seat | point | verdict | what decides it |
|---|---|---|---|---|
| A1 | Astra | floor (c) changes object: (a)/(b)/(d) grade the W2 CONTROLS against defective gates, (c) grades the fixed GATE against a dead differential; record the controls' (c) as by-construction, null-gate leg not run | **ACCEPT** the finding; the proposed REPLACEMENT is amended (below) | `RULING.md:33` names BOTH objects in one header ("the gate's guard, defended by the W2 controls") and `:41-46` then grades only the gate; the block does the same (`unit/files/CHANGELOG.md:37-41`: (a),(b),(d) are the controls' legs, (c) is the gate's).  `CLAUDE.md:1358-1360` gives the two permitted forms.  For the controls: `compare.py:100-101` reds any row whose line is not found (every mixed/allcrash row and both GATE VERDICT rows), `:103` reds the allkill/real SAME rows when FIX's text is empty against HEAD's non-empty text -- so a dead FIX gate reds every row by construction.  **Caveat the by-construction form must carry:** with BOTH legs dead the allkill/real rows PASS (`"" == ""` at `:103`, `hre` is None) -- the `all([])` shape `CLAUDE.md:1363-1364` names; the construction holds against a live HEAD leg.  The dead-differential measurement is NOT merely "behavioural evidence": it is clause (c) for gate 3 AS A DETECTOR (the carrier's runtime-probe form, every session dies), and the gate is the round's product -- so the record keeps it, named as the gate's (c), and ADDS the controls' (c).  My ruling saw the dual role (`:44-46`) and waved it off as "not required"; that was the soft spot. |
| A2 | Astra | Q2 misattributes Argon: it said `allkill` and `real` stay green, not "every leg green" | **ACCEPT** | `argon_kdc_p2.txt:18`: "the `allkill` and `real` completed sets ... keeping them perfectly green" -- TRUE as measured (`Q2_CONTROLS.txt`: M_q2a allkill byte-identical, allcrash/mixed GATE VERDICT ok).  Its dead-run claim ("would once again score as successful detections") is FALSE: `W2_M_q2a.allcrash.log:18-19` prints `got=0` / `0 want=0`, 11 of 19 rows red.  "Keeps every leg green" is the coordinator's paraphrase (`review.json:10` disposition, `:37` changelog), which my `RULING.md:24` put in quotation marks as the seat's words.  The same paraphrase is in the unit at `unit/files/CHANGELOG.md:46` and the ledger review entry (`unit/files/tools/pipeline/ledger.json:76359`). |
| A3 | Astra | check 13 overstates: the FINAL sentence says logs "ending" in verdicts, the script checks presence; `records_wkdc.py:69` accepts PASS anywhere + DONE last, not the terminal pair | **ACCEPT**, both halves | Sentence: `records_wkdc.py:405` (was `:300` in `pc/bk_20261106_ruling/records_wkdc.py`, so my `:297-302` citation was right when written) "every mutant's log ending `DIFF_FAIL`".  Script: `insitu_gate3.sh:83` `grep -aq '^DIFF_PASS'`, `:86` `grep -aq '^DIFF_FAIL'` -- presence at line start, never the last line.  The research's W2 driver DID measure the last line (`W2_FIX.real.log` ground truth: "LAST LINE OF ITS LOG"), which is where the word came from; the in-situ script does not.  `records_wkdc.py:69`: `"INSITU_G3_SUMMARY PASS" not in itxt or not itxt.rstrip().endswith("INSITU_G3_DONE")` -- anywhere + suffix; `insitu_gate3.sh:99-100` writes them as the last two lines, so the check is weaker than the writer, not wrong.  (Also: the refusal lives in `records_wkdc.py`, run by `build_kit.py`; my `:28` credited `build_kit.py`.) |
| A4 | Astra | "check count pinned nowhere" is too broad | **ACCEPT** | `compare.py:80` pins `PASS (15 checks` / `FAIL (7 of 15` / `FAIL (1 of 15` / `FAIL (5 of 15`; `insitu_gate3.sh:78,79,89,93` pin `(15 checks)` and `(7 of 15 checks)`.  In the TREE at HEAD nothing pins it (`git grep` over `regress/ tools/` minus artifacts: `run.sh:10` lists the gate, `gate_build.sh:308` is a comment about a different gate) -- which is what my "(PRETEST)" gestured at and the sentence did not say.  The filed row repeats the broad form: `records_wkdc.py:265` "no gate or checker pins it, so nothing else reds" -> the ledger's `g3nologselfpin` state_note. |
| A5 | Astra | check 14's relocation prediction (`rc=1`) is wrong: under `set -u` the moved `local rc=$?` leaves `$rc` unbound in the guard | **ACCEPT** | `selftest_mutation.sh:35` `set -u`; `rc` is declared ONLY at `:173` (grep over the staged gate and `lib.sh`: `:169` comment, `:173`, `:182`).  Moving `:173` below `:182` makes `echo "NOLOG rc=$rc"` an unbound expansion inside `out=$(...)` (`:196`): the subshell dies, stdout is empty, `check` gets `got=` against `want=0` -- the seven pinned rows still red, by a different mechanism than my `rc=1`.  Conclusion of check 14 unchanged; its stated mechanism corrected. |
| A6 | Astra | reviewed unit is not 88 files | **ACCEPT** -- same point as G2 | `PRETEST_reviewed.out:2` "staged: 78 paths (unit: 78)" at 15:40, before my 15:59 ruling; `PRETEST.md:67` "78 files".  88 = 78 + 8 under `unit/insitu/` (counted: 3 HEAD, 3 STAGED, `MD5.txt`, the stub) + `commit.msg` + `UNIT.json` -- the whole `unit/`, written against `unit/files/`.  Now 79 (`BUILD.out:16`, `PRETEST_ruled.out:2`, `UNIT.json` files=79): + `RULING.md` + `FABLE_QUEUE_item7.md`, - `fable_queue.md` (`BUILD.out:10`); whole `unit/` now 89. |
| G1 | Grok | "byte-identical" is false of the whole logs | **ACCEPT** as a precision repair to the ruling; the measured claim stands | Measured here: the `section()` between "the gate's own output" and "ground truth" is byte-identical on ALL SIX pairs (STAGED/FIX and M_q2b/HEAD on allcrash, mixed, allkill), header stripped or not.  The whole logs differ exactly where Grok says: line 1 (`gate script:` path + md5), the GROUND-TRUTH section's shell crash reports (pids, driver path -- allcrash `:37,39,41,43`, mixed `:39,41`), and the `W2_GATE3_DONE` tag (`:51` / `:46` / `:44`).  My checks 1 and 10 and floor (b) said "gate output" without the qualifier that my check 7 carried; a reader handed the cited LOG diffs it and finds differences.  The block already carries Grok's "say instead" (`unit/files/CHANGELOG.md:38`: "line for line ... only the header ..., the shell's crash reports ... and the done tag differ"), so no unit repair. |
| G2 | Grok | the unit is 78 under `unit/files/`; 88 is the whole `unit/` | **ACCEPT** -- same point as A6 | as A6; Grok's arithmetic (78 + 8 + 2) verified. |
| G3 | Grok | the in-situ sentence is a SUBSET of the script (control row `:92`, md5s `:95` unasserted) and the "ending" claim is unchecked | **ACCEPT** -- the other half of A3's check 13 | `insitu_gate3.sh:92` (crash leg's control row `ok ... 1`) and `:95` (`build/` input md5s before == after) are failed by the script and said nowhere in `records_wkdc.py:403-407`.  So my "asserts exactly what the script checks" was wrong in both directions: a superset on "ending", a subset on these two. |
| G4 | Grok | floor (d) stamps MEASURED on four cells that were only read | **ACCEPT** | `RULING.md:47-48` ends "...lands on existing rows (check 14).  MEASURED."; `:29` (check 14) itself says "by reading; the two measured are Q2's".  Only `M_q2a` (11 red) and `M_q2b` (13 red) ran (`Q2_CONTROLS.txt`; `RUN_Q2.log`).  The block's (d) (`CHANGELOG.md:41`) names only the two as measured, so the unit is right and the ruling is what needs the word. |

**Where both seats raise the same point:** A6 = G2 (the 88); A3 and G3 are the two halves of one wrong sentence in check 13
(a superset claim and a subset claim about the same `records_wkdc.py:403-407` / `insitu_gate3.sh:78-95` pair).

**Harder on my own ruling than on theirs.**  Nine distinct errors, all mine, all records: one count copied from the wrong
directory (A6/G2); one quotation that was a paraphrase (A2); one "exactly" over a pair that matched in neither direction
(A3/G3); one "nowhere" that meant "nowhere in the tree" (A4); one predicted mechanism that `set -u` forbids (A5); one
unqualified "byte-identical" two checks after a qualified one (G1); one MEASURED stamped over four read cells (G4), which is
the carrier's prediction-in-a-measured-column class inside a ruling that cited that class; and one floor clause graded on a
different object from its three siblings, with the dual role noticed and dismissed (A1).  None changes a score, a kill, or
the floor count: every number the ruling quoted from a log is still in that log, and every mechanism it predicted still
reds the row it named.  **Floor breaches: 0 -- unchanged.**  What the seats found is that the ruling's PROSE was looser
than its CHECKS, which is the class this project files under L4.

## FINAL DISPOSITION: LAND AFTER RECORD REPAIRS

No detector or code repair is owed: no point names an escaping mutant, a vacuous row, or a wrong line in
`regress/selftest_mutation.sh`.  All repairs are L4 (wrong or under-qualified records), corrected IN PLACE quoting what
they refute, before the FINAL build.  The kit derives the CHANGELOG, the ledger entries and the banked ruling from
`review.json`, `records_wkdc.py` and `kdc/RULING.md`, so the edits land in those three sources and `build_kit.py` is
re-run (REVIEWED mode now; FINAL after step 4).

**R1 -- the ruling (`_scratchpad/fable_20261106/kdc/RULING.md`): append one dated CORRECTIONS section, each item quoting the
sentence it refutes; the banked copy follows on rebuild.**
1. `:7` "88 files" -> "78 files under `unit/files/` at review time (`PRETEST_reviewed.out:2`); 88 was the whole `unit/`
   (+8 `insitu/`, `commit.msg`, `UNIT.json`); 79 after the ruling and its question were banked (`BUILD.out:16`)."  [A6, G2]
2. `:16`, `:29` (check 10), `:37-38`, `:104` "byte-identical ... gate output" -> "the gate's own output SECTION (what
   `compare.py:21-25` scores) is byte-identical on all three stub sets; the whole log differs in the `gate script:` header,
   the ground-truth section's shell crash reports (pids, driver path) and the `W2_GATE3_DONE` tag -- as check 7 said."  [G1]
3. `:24` "so the seat's 'keeps every leg green' is false" -> "the seat's completed-set claim (`allkill` and `real` stay
   green, `argon_kdc_p2.txt:18`) is TRUE and measured; its dead-run claim (crashed runs score as detections) is FALSE --
   the literal edit falls through and prints `0` twice (`W2_M_q2a.allcrash.log:18-19`), 11 of 19 rows red.  'Keeps every
   leg green' was the coordinator's paraphrase, not the seat's words."  [A2]
4. `:28` (check 13) "asserts exactly what `insitu_gate3.sh` checks" -> "asserts MORE on one point and LESS on two: 'ending
   `DIFF_FAIL`/`DIFF_PASS`' where `insitu_gate3.sh:83,86` test presence at line start; silent on the crash leg's control
   row (`:92`) and `build/`'s input md5s (`:95`), both of which the script fails on.  The FINAL refusal is
   `records_wkdc.py:64-70` (run by `build_kit.py`) and requires `INSITU_G3_SUMMARY PASS` anywhere plus `INSITU_G3_DONE`
   last, not the terminal pair (`:69`)."  [A3, G3]
5. `:29` (check 14) "move `local rc=$?` below the grep -> `rc=1`" -> "-> `$rc` unbound at `:182` under `set -u` (`:35`;
   `rc` is declared only at `:173`): the `$(...)` subshell dies, `got=` is empty, the seven pinned rows red."  [A5]
6. `:41-46` floor (c) -> two objects, each in a carrier form (`CLAUDE.md:1358-1360`): "(c) for GATE 3 as a detector:
   MEASURED at `W2_FIX.allcrash.log` / `W2_FIX.mixed.log` (the differential never answers; the fixed gate reds every such
   run).  (c) for the W2 CONTROLS, the detector defending this fix: BY CONSTRUCTION via `compare.py:100-101` (a row whose
   line is not found reds) and `:103` (the allkill/real SAME rows red when FIX's text is empty against HEAD's non-empty
   text); null-gate leg NOT RUN.  The construction holds against a LIVE HEAD leg: with both legs dead the allkill/real rows
   pass (`"" == ""`), the `all([])` shape."  Delete "A clause saying so in the block would preempt the objection; not
   required."  [A1]
7. `:47-48` floor (d) "... (check 14).  MEASURED." -> "M_q2a (11 red) and M_q2b (13 red) MEASURED (`Q2_CONTROLS.txt`); the
   other four DEPENDS-ON cells BY READING (check 14), not run; each lands on an existing row."  [G4]
8. `:78` "is pinned nowhere (PRETEST)" -> "is pinned by no gate or checker in the tree (git grep at HEAD), and IS pinned by
   the round's own comparators -- `controls/compare.py:80`, `landing/insitu_gate3.sh:78,79,89,93` -- which the eighth
   mutant's round must update."  [A4]

**R2 -- the unit (sources, then `build_kit.py`): all pre-FINAL, R2.2 also pre-step-4.**
1. `review.json:10` ("disposition") and `:37` ("changelog"): "was claimed to keep every leg green" -> "claimed to keep the
   completed sets (`allkill`, `real`) green -- true, measured -- and to score dead runs as detections -- measured false:
   the edit falls through and prints `0` twice, 11 of 19 control rows red".  This regenerates `CHANGELOG.md:46` and the
   ledger review entry (`ledger.json:76359`).  [A2]
2. `records_wkdc.py:405` "every mutant's log ending `DIFF_FAIL` and the control's `DIFF_PASS`" -> EITHER "every mutant's
   log carrying a `DIFF_FAIL` line and the control's a `DIFF_PASS` line" (what `insitu_gate3.sh:83-88` tests) OR, preferred
   since step 4 has not run, make `insitu_gate3.sh:83` and `:86` test the LAST non-blank line (`tail -n1 ... | grep -q
   '^DIFF_PASS'`) -- the research's W2 driver's own ground-truth column -- and keep the sentence.  One of the two, not
   neither.  Optionally add "(the script also requires the crash leg's control row `ok 1` and `build/`'s input md5s
   unchanged)".  [A3, G3]
3. `records_wkdc.py:455-457` (`FLOOR_CX`): append the controls' (c) in R1.6's by-construction form, with the live-HEAD
   caveat, after the existing dual-role clause; keep that clause and name its object as gate 3.  [A1]
4. `records_wkdc.py:265` (`g3nologselfpin` state_note) "no gate or checker pins it, so nothing else reds" -> "no gate or
   checker in the tree pins it; the round's own comparators (`controls/compare.py:80`, `landing/insitu_gate3.sh:78,79,89,93`)
   pin 15 and must be updated with the eighth mutant".  [A4]
5. Optional hardening, no error: `records_wkdc.py:69` require the last two non-blank lines to be exactly
   `INSITU_G3_SUMMARY PASS` then `INSITU_G3_DONE` (what `insitu_gate3.sh:99-100` writes).  [A3]

**Unchanged obligations, not new:** the kit's step 4 (`INSITU_G3.out`, alone on the machine; on FAIL do not land); the
re-date of the four peer exemptions if landing slips past today (ruling's owed item 2); `g3nologselfpin` filed LOW
(done, `BUILD.out:8`); the anywhere-vs-last-line note in `killdrivercrash`'s question (done, `records_wkdc.py:299-307`).

**Grades.**  R1.1-R1.8, R2.1, R2.3, R2.4: L4 wrong record, in place.  R2.2: L4 -- the FINAL sentence would assert a
measurement ("ending") the in-situ script does not make; either leg of the repair discharges it.  R2.5: no grade,
optional.  No L1, L2 or L3: the floor stands at 0 breaches on the shipped detector, and nothing a seat raised reaches a row
or a line of the gate.

FABLEADJ_KDC: 10 ACCEPTED 0 REJECTED VERDICT:LAND-AFTER-RECORDS
