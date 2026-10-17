# PASS 2 -- `cxlaunchquotation` / `cxlaunchdaybreak`: the production codex launcher landed in tracked `tools/cxlaunch.sh`

Four seats, by the owner's roster of 2026-10-16: Fable 5.1, GPT-6 Astra, Grok 4.7, GLM 5.3.  Opus, agy, kimi, deepseek and
minimax are DELIBERATELY NOT FIRED under that roster.  This is an ordinary review of a test-harness script (a launcher that
runs one read-only review job and classifies how it ended).  READ-ONLY: write nothing to any project tree.  The tree under
review is `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC` (HEAD plus the uncommitted `tools/cxlaunch.sh` and
`regress/artifacts/cxlaunchland_20261016/`); ignore the pristine upstream copy at `C:/DocumentNoSnc/cc/GXEMUL/src/`.
Everything a packet-fed seat needs is inlined below.

**Please do not simply ratify -- check the premises, not just the derivations.**  A recent panel had seven of nine seats
confirm a premise a brief stated wrongly.

Open with your seat token -- `FABLE_CXLAND_20261016` / `ASTRA_CXLAND_20261016` / `GROK_CXLAND_20261016` /
`GLM_CXLAND_20261016` -- then ONE line: `VERDICT: SHIP / SHIP WITH CHANGES (<n>) / DO NOT SHIP (<one line>)`.

## 1. What the three-seat adjudication ruled (RULINGS_C_records.md, F1 -- Fable 5.1, GPT-6 Astra, Grok 4.7, all UPHOLD)

* Land the PRODUCTION rule into tracked `tools/cxlaunch.sh`: stderr's codex `ERROR:` lines are classified ONLY WHEN
  `rc != 0` OR stdout is EMPTY; `rc 0` with a non-empty stdout is an ANSWER, whatever stderr quotes.  The landed comment
  must state that actual condition (Grok), not "only a failed run".
* Correct the packet's claim that the production copy "has run every Astra job since 2026-09-26" (Astra found a 10-09 run
  that used the old classifier and walled a real answer); cite the 09-28 dossier receipt as the real Daybreak-fallback
  evidence, separately from the classifier fixtures.
* ADD an ANSI strip before the `^ERROR:` anchor (Fable): 7 of 453 `panel.sh` codex.txt files carry a coloured column-0
  `ERROR:`, and under the production rule a coloured real wall reads exit 6 "seat down" (Fable's fixture Q3).
* Controls: the six Option-C fixtures (P1 P2 N1-N4), Fable's Q1-Q3; and two residuals RECORDED, NOT FIXED: N4 (rc 1 with
  an answer and quoted wall text -> exit 8) and its refusal twin (a quoted refusal line on rc != 0 -> the Daybreak re-run
  fires and the first answer is renamed `.refused.*`).  The "read only codex's final ERROR: line" refinement was WITHDRAWN
  (in N4 the final ERROR: line is itself a quotation).
* RIDER (Astra): the launcher prints the model it RAN but credited the model it ASKED for -- "a wrong name is a SEAT
  FAILURE" was unenforced; compare codex's `model:` header to the request.
* Records: merge the 2026-09-26 filing `cxlaunchwallfp` (no ledger row) into this landing; close `cxlaunchdaybreak` (the
  ultra effort and the Daybreak fallback ride along).

## 2. Settled premises (warrants inline; challenge any of them)

* Fable 5.1's launch-log census (`adj_20261016/fable5/meas_C/launchlog_census.txt`): 387 `codex rc=` lines across 376
  files -- 362 rc 0 with a non-empty stdout, 25 rc 1 with an empty stdout, ZERO off that diagonal.
* Fable's ANSI census (`meas_C/ansi_census.txt`): 7 of 453 panel.sh codex.txt files carry `ESC[1m ESC[31m ERROR: ESC[0m
  ESC[0m`; 0 of 593 launcher `.err` files.
* Measured by me for the rider, 2026-10-16: 519 `*.launch.log` files, 322 `asked:` / `ran:` pairs -- 312 asked and ran
  `gpt-6-astra`, 10 asked and ran `gpt-daybreak-blue-latest`; no pair with the header absent, no mismatch.  The header
  names the asked slug exactly, including the `-latest` alias.
* Codex's stderr opens with `Reading additional input from stdin...` then a header block (`OpenAI Codex v0.153.4`,
  `--------`, `workdir:`, `model: <slug>`, `provider:`, `approval:`, `sandbox:`, `reasoning effort: <e>`, ...) before the
  brief text and any streamed source -- measured on the N1 fixture (`exemptredate_20260925/final550/codex_astra550.err`).
  NOTE the effort header can differ from the request (`asked: ... / ultra` with `reasoning effort: max` in N1), which is
  why only the MODEL is compared.
* The exit codes the old tracked file returned besides codex's own were 6, 7, 8 and 9; exit 5 is new (a different
  model ran).  `grep` finds no caller of `tools/cxlaunch.sh` that branches on its exit status (its only mentions are
  `panel.sh`'s CODEX_EFFORT comment and the carrier).

## 3. What I did NOT do, and why -- check these dispositions

* Absent `model:` header on an ANSWERED run is reported UNVERIFIED and NOT failed (0 of 322 on record).  Failing it would
  turn a CLI format change into a lost answer on every run; not failing it means the identity check goes quiet if the
  header ever disappears.  Is the trade right, or is this the check-that-cannot-fail shape?
* N4 and its refusal twin stay residuals (the ruling's own wording).
* `PROJ=/c/DocumentNoSnc/CC/GXEMUL` stays hardcoded (the tracked file already hardcoded it; the carrier's derive-the-root
  rule was not part of the ruling).
