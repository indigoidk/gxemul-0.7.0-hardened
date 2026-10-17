# V4 PASS -- `cxlaunchquotation` / `cxlaunchdaybreak`: the codex launcher `tools/cxlaunch.sh`, v4 = the CLASS CLOSURE

Four seats, by the owner's roster of 2026-10-16: Fable 5.1, GPT-6 Astra, Grok 4.7, GLM 5.3.  Opus, agy, kimi, deepseek and
minimax are DELIBERATELY NOT FIRED under that roster.  An ordinary review of a shell wrapper that launches a read-only
review CLI and classifies its exit, and of the test harness that pins it.  READ-ONLY: write nothing to any project tree.
The tree is `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC`; the v4 launcher is `tools/cxlaunch.sh` in the WORKING TREE (uncommitted;
v3 is preserved as `regress/artifacts/cxlaunchland_20261016/cxlaunch_landed_v3.sh` -- v4 changes COMMENTS only); the
controls and mutant table are `run_controls_v4.sh`, `run_mutants_v4.sh` and `mut_launcher_v4.py` beside it, the census
`census_v4.py` / `CENSUS_v4.txt`; the v3-pass answers are in `v3pass/`.  Everything a packet-fed seat needs is inlined below.

**Why v4 is a class closure, not another repair.**  Pass 2, the adjudication pass and the v3 pass each found one-edit
mutants that passed every control of the version before -- the same class three times: a decision of the launcher whose
EDGE no fixture straddled.  By the repair-chain rule the next repair owes the class: v4 enumerates EVERY decision the
launcher makes, pins each at its edges, and writes the rest into a CONTRACT in `run_controls_v4.sh`'s header (inlined in
section 3b).  **This pass's job is to VERIFY THE ENUMERATION** -- is any decision of the launcher missing from the CONTRACT,
or listed as pinned while a one-edit mutant of it still passes all 116 controls?  The chain closes on the first pass whose
zero floor breaches survive adjudication; if you find none, name the decisions you checked.  Check the premises in 2b; do
not ratify them.

<TOKEN_LINE>

## 1. The v3-pass verdicts

* **GPT-6 Astra -- SHIP WITH CHANGES (3)** (`v3pass/codex_cxlandv3.txt`).
* **Grok 4.7 -- SHIP WITH CHANGES (3)** (`v3pass/grok_cxlandv3.txt`).
* **GLM 5.3 -- SHIP WITH CHANGES (2)** (`v3pass/glm_cxlandv3.txt`).
* **Fable 5.1 -- SEAT FAILURE, the second running**: the agent stalled (stream watchdog, no progress for 600 s) after reading
  the launcher and before writing anything -- most likely the whole kill table run as ONE foreground command.  Not counted as
  agreement; re-fired on this pass with the hazard named.

## 2. Every finding, numbered, with my disposition

| # | seats | finding | disposition |
|---|---|---|---|
| V1 | Astra | the window `NR > 12` -> `NR > 3` passes all 70, and would leave the one real warning-prefixed header on record (banner at line 4) UNVERIFIED | **PINNED**: W12 (an opening block whose first rule is line 12: read, a mismatch exits 5), W13 (first rule at 13: not read, UNVERIFIED), X13 (the first 14 lines of that real file, asked as gpt-6-other: exits 5).  Mutants `m_win11`, `m_win13`, `m_win3` |
| V2 | GLM, Grok | the window pinned only up to `NR > 20` (X9's quoted block starts at line 21) | **PINNED** by W13: any widening reads W13's block and exits 5 |
| V3 | GLM | the 30-line cap pinned by nothing (`print` unconditional passes all 70) | **PINNED**: K30 (an unterminated block, `model: gpt-6-other` at body line 30: read, exits 5) / K31 (line 31: not read, UNVERIFIED).  Mutants `m_cap29`, `m_cap31`, `m_nocap` |
| V4 | Astra | the refusal guards `-gt 0` -> `-eq 1` (both sites) and the wall guard `-gt 0` -> `-gt 1` pass: every fixture carried refusal count 1 and wall count 2+ | **PINNED**: R2X (a REAL doubled refusal -- `fx/R2.stderr`, copied from `_scratchpad/panel_20260919_013302/codex_adv540p2.REFUSED1.err`, two coloured refusal lines -- fallback off: exits 7), D3 (the same, fallback on: Daybreak re-run, two calls, Daybreak credited), W1L (ONE wall line: exits 8).  Mutants `m_refeq1`, `m_fbeq1`, `m_wallgt1` |
| V5 | Grok | the fallback test `-gt 0` -> `-ge 0`, or widened with the wall count, passes all 70: every row but D1/D2 DISABLES the fallback, while production would re-run Daybreak on every answer and rename it `.refused` | **PINNED**: FB1 (N1, an answer, with the fallback LEFT ON as production runs it: exits 0, ONE call, nothing renamed) and FB2 (P1, a wall, fallback on: exits 8, ONE call).  Mutants `m_fbge0`, `m_fbwall` |
| V6 | Astra, Grok | refusal-then-refusal unrowed; an `if` -> `while` or a doubled fallback run would not be seen | **PINNED**: D4 (Astra refuses, Daybreak refuses: exits 7, EXACTLY two calls); every launcher run is under `timeout 120`, so a looping mutant exits 124 and reds instead of hanging.  Mutant `m_twice` |
| V7 | GLM | exit 9 is pinned by nothing | **PINNED**: X14 (a brief of exactly 30,000 bytes: proceeds) / X15 (30,001: exits 9, codex never called).  Mutants `m_argv1`, `m_argv2`.  The hardcoded `cd "$PROJ" || exit 9` is DISCLOSED (untestable without editing the file) |
| V8 | Astra, Grok | the header comment (line 41) still says a `model:` line elsewhere "never names the model" | **FIXED**: "it can name a model, and it is never READ" |
| V9 | Astra, Grok | `mut_launcher_v3.py` says "inside the recorded N4 residual"; it and `run_mutants_v3.sh` name `run_mutants.sh` | **FIXED** in the v3 files (comment-only) and in the v4 ones |
| V10 | Astra | "no stderr on record carries both a refusal and a wall" is false: rc-0 answered runs quote both (pass2/codex_cxland.err) | **QUALIFIED, measured**: on a run that ENTERS classification (rc != 0 or empty stdout) -- 0 of 410 in `CENSUS_v4.txt`; rc-0 answered runs that quote both exist and are never classified |
| V11 | Astra | the witness calls N1 and N2 "a real answer" | **FIXED**: N1 is a captured real Astra answer whose stderr quotes a wall line; N2 is a synthetic answer carrying the four wall words |
| V12 | Grok | the G9 bracket asserted the stale line numbers ARE the cxlaunch entries; at c64445fa they are `asanfifteen`'s body, `stagetokenscontrols` and the `armvecrecurse` row | **FIXED** (section 5c): says what the lines are, and names the entries MEANT by id |
| V13 | GLM | the OB bracket says "header block", not "OPENING header block" | **FIXED** |
| V14 | Grok | the hold question names a CHANGELOG block the records preview did not contain | **FIXED**: the block is drafted (section 5d) |
| V15 | GLM | `grep -m1` -> `-m2` and the closing rule's `exit` -> `next` are unpinned | **DISCLOSED** in the CONTRACT, with a measurement: 0 of 972 opening blocks in 2,422 codex `.err` files lack exactly one `model:` line (`CENSUS_v4.txt`) |
| V16 | main loop | the seat entries this landing writes | answered seats carry `d` ✓ (their changes applied, one by one), seat failures and seats not fired carry none (they render `…`, which is what they were) |

## 2b. Premises to CHECK (stated as questions)

* **The CONTRACT's completeness.**  Section 3b's header lists ten decisions.  Is there a decision the launcher makes that
  it does not list -- read the whole of `tools/cxlaunch.sh` (or section 3a plus the v3 file) for every `if`, `[ ... ]`,
  `grep`, `exit` and constant?
* **Fixture realism.**  W12/W13 and K30/K31 are synthetic blocks; X13 and R2X are real files.  Is any synthetic edge
  fixture a shape a real codex run CANNOT produce, so that the row pins nothing real?
* **`timeout 120`.**  Is any honest run near 120 s?  (They take about one second each.)
