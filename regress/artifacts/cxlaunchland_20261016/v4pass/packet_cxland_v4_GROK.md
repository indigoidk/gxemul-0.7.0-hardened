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

**Liveness:** open your answer with the token `GROK_CXLANDV4_20261017` on its own line, then your verdict line.

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

## 3. The repair, v3 -> v4

### 3a. tools/cxlaunch.sh -- comments only (10 changed lines)

```diff
--- /c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/cxlaunchland_20261016/cxlaunch_landed_v3.sh
+++ /c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/tools/cxlaunch.sh
@@ -37,8 +37,9 @@
 #    4. (2026-10-16, GPT-6 Astra) the `model:` line of codex's HEADER BLOCK is COMPARED to the model asked for.  This
 #       file printed both and compared neither, so "a wrong name is a SEAT FAILURE" was unenforced.  On record: 322
 #       asked/ran pairs across 519 launch logs under the project root, 319 across 493 inside GXEMUL-SEC (Astra), no
-#       header absent and no mismatch -- so a mismatch is new, and it exits 5.  Only the header block is read (pass 2,
-#       Astra): a `model:` line anywhere else in stderr is streamed source or the brief, and never names the model.
+#       header absent and no mismatch -- so a mismatch is new, and it exits 5.  Only the OPENING header block is read
+#       (pass 2 and the adjudication pass, Astra): a `model:` line anywhere else in stderr is streamed source or the
+#       brief -- it can name a model, and it is never READ (GLM 5.3 and Grok 4.7, v3 pass).
 #
 #  KNOWN RESIDUALS -- recorded, NOT fixed (the ruling's own wording; no real run has either shape, 0 of 387 launch
 #  lines are off the diagonal of {rc 0 with stdout, rc 1 with empty stdout} -- adj_20261016/fable5/meas_C/
@@ -63,8 +64,9 @@
 #  Exit status: 0 answered; 5 a different model ran; 6 empty stdout with no refusal or wall text; 7 refused (after
 #  the fallback, if any); 8 walled; 9 the brief is above the argv cap or the project dir is missing; otherwise
 #  codex's own nonzero rc.  An answered run whose model is unverified still exits 0, and says so instead of naming
-#  a model.  Controls: regress/artifacts/cxlaunchland_20261016/run_controls_v3.sh (RECEIPT_v3.txt; the kill table is
-#  KILLTABLE_v3.txt -- RECEIPT.txt and RECEIPT_v2.txt are the pass-2 and adjudication-pass receipts of earlier versions).
+#  a model.  Controls: regress/artifacts/cxlaunchland_20261016/run_controls_v4.sh (RECEIPT_v4.txt; the kill table is
+#  KILLTABLE_v4.txt; its header is the CONTRACT -- which edge of each decision this file makes is pinned, and which is
+#  deliberately not).  RECEIPT.txt, RECEIPT_v2.txt and RECEIPT_v3.txt are the receipts of the earlier versions.
 #
 #  Usage: cxlaunch.sh <brief-path> <out-dir> <tag>
 set -u
```

### 3b. the controls, `run_controls_v3.sh` -> `run_controls_v4.sh` (the CONTRACT is in the header)

```diff
--- /c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/cxlaunchland_20261016/run_controls_v3.sh
+++ /c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/cxlaunchland_20261016/run_controls_v4.sh
@@ -1,6 +1,6 @@
 #!/bin/bash
 #  Controls for the tools/cxlaunch.sh landing of 2026-10-16 (ledger `cxlaunchquotation`, `cxlaunchdaybreak`; RULINGS_C_records.md
-#  F1), v3 after the four-seat pass 2 and the adjudication pass.  Every row runs a launcher against a FAKE codex that replays a
+#  F1), v4 after the four-seat pass 2, the adjudication pass and the v3 pass.  Every row runs a launcher against a FAKE codex that replays a
 #  fixture -- nothing here calls the network -- on THREE launchers, and compares each exit status with the expected one:
 #
 #    tracked  cxlaunch_tracked.sh  = `git show HEAD:tools/cxlaunch.sh` before the landing (md5 cb180d9d...), the file the
@@ -28,14 +28,53 @@
 #    E1/E2  the EXACT arguments the fake codex received, one per line: exec, --sandbox read-only, --skip-git-repo-check,
 #        -m <model>, -c model_reasoning_effort=ultra and the brief -- once for N1, twice (Astra, then Daybreak) for D1
 #        (v2 matched a substring, so `ultrax' passed, and it never read the sandbox flag or the brief; Astra, GLM 5.3)
-#  NOT pinned, by Fable 5.1's ruling on pass 2 (filed in `cxlaunchunpinned'): `-ne 0' -> `-eq 1' in the classify gate is
-#  observable only at an rc outside {0, 1} WITH an answer -- a sibling of the N4 residual (N4 itself is rc 1, where the two
-#  forms agree; GLM 5.3), with 0 instances on record; the strip narrowed to SGR (`[0-9;]*m') and wall-before-refusal
-#  precedence each need a stderr shape with 0 instances on record (no non-SGR CSI or OSC in 2,372 .err files; no
-#  refusal+wall co-occurrence).
+#  v4 -- the v3 pass (GPT-6 Astra, Grok 4.7, GLM 5.3) found one-edit mutants passing all 70 v3 controls at the window and
+#  cap constants, the refusal and wall multiplicity guards and the fallback predicate: the same class as the two passes
+#  before it, so v4 is the CLASS CLOSURE -- every decision the file makes is pinned at its edges or disclosed below:
+#    W12 an OPENING header whose first rule is line 12, naming gpt-6-other -> 5        (the window's last accepted line)
+#    W13 the same block one line lower, first rule at line 13              -> 0, UNVERIFIED (its first refused line)
+#    X13 the one real warning-prefixed header on record, banner at line 4 (the first 14 lines of
+#        regress/artifacts/ppcrldimimask/codex_book1check_20260910.err), asked as gpt-6-other -> 5
+#    K30 an UNTERMINATED opening block whose `model: gpt-6-other' is body line 30 -> 5  (the cap's last read line)
+#    K31 the same, the model at body line 31                               -> 0, UNVERIFIED (the first unread line)
+#    R2X a REAL doubled refusal (fx/R2.stderr, copied from _scratchpad/panel_20260919_013302/codex_adv540p2.REFUSED1.err:
+#        two coloured refusal lines), the fallback disabled                -> 7             (refusal count 2, not 1)
+#    D3  the same, the fallback on and Daybreak answering                  -> 0, two calls, Daybreak credited
+#    D4  Astra refuses, then Daybreak refuses                              -> 7, EXACTLY two calls
+#    W1L ONE column-0 wall line                                            -> 8             (wall count 1, not 2)
+#    FB1 N1 (an answer) with the fallback LEFT ON, as production runs it   -> 0, ONE call, nothing renamed .refused
+#    FB2 P1 (a wall) with the fallback left on                             -> 8, ONE call
+#    X14 a brief of exactly 30,000 bytes                                   -> 0             (the argv cap's last size)
+#    X15 a brief of 30,001 bytes                                           -> 9, and codex is never called
+#    Every launcher run is under `timeout 120': a mutant that loops (a fallback that re-runs) exits 124 and reds.
+#
+#  THE CONTRACT -- each decision the landed launcher makes, the rows that pin its edges, and what is deliberately not:
+#    opening-header window `NR > 12 && h < 2'  W12 / W13 (first rule at line 12 read, at 13 not); X13 (the real banner-at-4
+#                                              header); X9, X10 (no opening block, a quoted one at line 21)
+#    header body cap `++n > 30'                K30 / K31 (a model at body line 30 read, at 31 not)
+#    the first `model:' of the opening block   M1, X5 -- N1's opening astra block wins over its four quoted blocks from line
+#                                              5528.  DISCLOSED: `-m1' -> `-m2' and the closing rule's `exit' -> `next'
+#                                              need a block with two model lines or none -- 0 of 972 opening blocks in
+#                                              2,422 codex .err files (CENSUS_v4.txt)
+#    classify gate `rc -ne 0 || body -eq 0'    N1, N2, X2, N4.  DISCLOSED: `-ne 0' -> `-eq 1' (m_eq1) is observable only at
+#                                              an rc outside {0, 1} WITH an answer -- a sibling of the N4 residual (rc 1,
+#                                              where the two agree; GLM 5.3) -- 0 of 394 launcher rows (Astra, v3 pass)
+#    `^ERROR:' anchor, grep -a, ANSI strip     X1; X8; A1, Q3.  DISCLOSED: the strip narrowed to SGR `[0-9;]*m' (m_sgr) --
+#                                              0 non-SGR CSI or OSC in 4,851 .err files (Astra, v3 pass)
+#    refusal count `refus -gt 0', at BOTH      P2, Q1, A1, D1 (count 1); R2X (2, the final guard); D3 (2, the fallback)
+#    wall count `wall -gt 0'                   W1L (count 1); P1, Q2, Q3, X8 (2); N4 (6)
+#    refusal before wall (precedence)          DISCLOSED (m_prec): a refusal and a wall line in one stderr ON A RUN THAT
+#                                              ENTERS CLASSIFICATION -- 0 of the 410 such runs in CENSUS_v4.txt.  rc-0
+#                                              answered runs that QUOTE both exist (pass2/codex_cxland.err, Astra) and
+#                                              classification never reads them
+#    the fallback trigger                      D1, D2 fire; FB1, FB2 do not (an answer, a wall, the fallback on); D4 fires
+#                                              ONCE (exactly two calls); its arguments: E1, E2, compared whole
+#    identity `RAN != ANSWERED_BY'             M1, D2, X5, W12, K30, X13 -> 5; M2, X6, X9, W13, K31 -> UNVERIFIED, 0
+#    argv cap `sz -gt 30000'                   X14 (30,000 accepted) / X15 (30,001: exit 9, no call)
+#    DISCLOSED, untestable without editing the file: the hardcoded `cd "$PROJ" || exit 9'.
 #
 #  Exit 0 only if every expectation holds (v1 ended on an echo and exited 0 whatever the tally -- GPT-6 Astra, pass 2).
-#  Usage: bash run_controls_v3.sh     ($CXL_AFTER overrides the after launcher; writes only to a scratch dir it removes)
+#  Usage: bash run_controls_v4.sh     ($CXL_AFTER overrides the after launcher; writes only to a scratch dir it removes)
 set -u
 HERE=$(cd "$(dirname "$0")" && pwd)
 REPO=$(cd "$HERE/../../.." && pwd)
@@ -86,6 +125,26 @@
 }
 latehdr gpt-6-astra | mkfx X9 0 "$T/ans_verdict.txt" -
 latehdr gpt-6-other | mkfx X10 0 "$T/ans_verdict.txt" -
+#  v4 (the v3 pass): the window's and the cap's EDGES, the real warning-prefixed header, a real doubled refusal, one wall line
+hdrat() {    # $1 lines before the banner, $2 the block's model -- a CLOSED opening block whose banner is line $1+1
+    i=1; while [ $i -le "$1" ]; do printf 'startup line %d\n' $i; i=$((i + 1)); done
+    printf 'OpenAI Codex v0.153.4\n--------\nworkdir: C:\\DocumentNoSnc\\CC\\GXEMUL\nmodel: %s\nprovider: openai\n' "$2"
+    printf 'reasoning effort: ultra\n--------\nuser\nthe session brief\n'
+}
+hdrat 10 gpt-6-other | mkfx W12 0 "$T/ans_verdict.txt" -      # banner line 11, first rule line 12: inside the window
+hdrat 11 gpt-6-other | mkfx W13 0 "$T/ans_verdict.txt" -      # banner line 12, first rule line 13: outside it
+head -14 "$REPO/regress/artifacts/ppcrldimimask/codex_book1check_20260910.err" | mkfx X13 0 "$T/ans_verdict.txt" -
+capat() {    # $1 body lines before the block's `model:' line -- an UNTERMINATED opening block
+    printf 'OpenAI Codex v0.153.4\n--------\n'
+    i=1; while [ $i -le "$1" ]; do printf 'body line %d\n' $i; i=$((i + 1)); done
+    printf 'model: gpt-6-other\nreasoning effort: ultra\n'
+    i=1; while [ $i -le 20 ]; do printf 'streamed line %d\n' $i; i=$((i + 1)); done
+}
+capat 29 | mkfx K30 0 "$T/ans_verdict.txt" -                  # the model is body line 30: read
+capat 30 | mkfx K31 0 "$T/ans_verdict.txt" -                  # the model is body line 31: not read
+mkfx R2 1 "" "$HERE/fx/R2.stderr"
+head -1 "$HERE/fx/P1.stderr" | mkfx W1L 1 "" -
+printf 'OpenAI Codex v0.153.4\n--------\nmodel: gpt-6-astra\nreasoning effort: ultra\n--------\n' | mkfx ANS 0 "$T/ans_verdict.txt" -
 
 #  the fake codex: replays $FX (or $FX2 when the requested -m equals $FX2_MODEL) and logs its arguments to $FX_ARGS
 cat > "$T/fakecodex.sh" <<'EOF'
@@ -104,6 +163,8 @@
 cp "$T/fakecodex.sh" "$T/home/AppData/Local/Programs/OpenAI/Codex/bin/codex"
 chmod +x "$T/home/AppData/Local/Programs/OpenAI/Codex/bin/codex"
 printf 'control brief\n' > "$T/brief.md"
+printf '%30000s' '' | tr ' ' b > "$T/brief30000.md"
+printf '%30001s' '' | tr ' ' b > "$T/brief30001.md"
 
 pass=0; total=0
 run() {    # $1 row, $2 launcher label, $3 launcher, $4 expected exit, then env assignments
@@ -112,7 +173,7 @@
     ( export CX_CODEX_BIN="$T/fakecodex.sh" FX2= FX2_MODEL= FX_ARGS="$T/args_${row}_${lab}"
       [ "$lab" = tracked ] && export HOME="$T/home"
       for kv in "$@"; do export "$kv"; done
-      bash "$sh" "$T/brief.md" "$out" "$row" ) > "$T/log_${row}_${lab}.txt" 2>&1
+      timeout 120 bash "$sh" "${BRIEF_OVERRIDE:-$T/brief.md}" "$out" "$row" ) > "$T/log_${row}_${lab}.txt" 2>&1
     local got=$?
     total=$((total + 1))
     local ok="NO"; [ "$got" = "$want" ] && { ok="ok"; pass=$((pass + 1)); }
@@ -130,7 +191,7 @@
     if [ "$2" = 0 ]; then pass=$((pass + 1)); echo "$1  ok"; else echo "$1  NO"; fi
 }
 
-echo "# cxlaunch landing controls (v3), $(date '+%Y-%m-%d %H:%M:%S')"
+echo "# cxlaunch landing controls (v4), $(date '+%Y-%m-%d %H:%M:%S')"
 echo "# tracked: $(md5sum < "$TRACKED" | cut -c1-32)  cxlaunch_tracked.sh"
 echo "# before:  $(md5sum < "$BEFORE" | cut -c1-32)  cxlaunch_before.sh"
 echo "# after:   $(md5sum < "$AFTER" | cut -c1-32)  $AFTER"
@@ -155,15 +216,41 @@
 three X8 6 6 8 FX="$T/fx/X8" CX_AUP_MODEL=
 three X9 0 0 0 FX="$T/fx/X9" CX_AUP_MODEL=
 three X10 0 0 0 FX="$T/fx/X10" CX_AUP_MODEL=
+three W12 0 0 5 FX="$T/fx/W12" CX_AUP_MODEL=
+three W13 0 0 0 FX="$T/fx/W13" CX_AUP_MODEL=
+three X13 0 0 5 FX="$T/fx/X13" CX_AUP_MODEL= CX_MODEL=gpt-6-other
+three K30 0 0 5 FX="$T/fx/K30" CX_AUP_MODEL=
+three K31 0 0 0 FX="$T/fx/K31" CX_AUP_MODEL=
+three R2X 6 6 7 FX="$T/fx/R2" CX_AUP_MODEL=
+three D3 6 6 0 FX="$T/fx/R2" FX2="$T/fx/DB_OK" FX2_MODEL=gpt-daybreak-blue-latest
+three D4 7 7 7 FX="$T/fx/P2" FX2="$T/fx/P2" FX2_MODEL=gpt-daybreak-blue-latest
+three W1L 8 8 8 FX="$T/fx/W1L" CX_AUP_MODEL=
+#  FB1/FB2 leave CX_AUP_MODEL UNSET: the fallback on, as production runs it (every other row disables it)
+three FB1 8 0 0 FX="$T/fx/N1"
+three FB2 8 8 8 FX="$T/fx/P1"
+three X14 0 0 0 FX="$T/fx/ANS" CX_AUP_MODEL= BRIEF_OVERRIDE="$T/brief30000.md"
+three X15 9 9 9 FX="$T/fx/ANS" CX_AUP_MODEL= BRIEF_OVERRIDE="$T/brief30001.md"
 #  E0: the fake ran for every row of every column; the run count is pinned, so a deleted row is visible
-nruns=$(ls "$T"/log_* 2>/dev/null | wc -l); nargs=$(ls "$T"/args_* 2>/dev/null | wc -l)
-miss=""; for f in "$T"/log_*; do b=${f##*/log_}; b=${b%.txt}; [ -s "$T/args_$b" ] || miss="$miss $b"; done
-[ "$nruns" = 63 ] && [ "$nargs" = "$nruns" ]; check "E0  all  the fake codex logged $nargs of $nruns runs (21 rows x 3, pinned)${miss:+ -- NOT reached:$miss}" $?
+#  v4: X15's three runs must exit 9 BEFORE codex, so they are the one row whose argument log must be ABSENT; the per-row
+#  lists decide the check (the v3 form decided on two counts and only decorated with the list -- GLM 5.3, adjudication pass)
+nruns=$(ls "$T"/log_* 2>/dev/null | wc -l)
+miss=""; extra=""
+for f in "$T"/log_*; do b=${f##*/log_}; b=${b%.txt}
+    case "$b" in X15_*) [ -e "$T/args_$b" ] && extra="$extra $b" ;; *) [ -s "$T/args_$b" ] || miss="$miss $b" ;; esac
+done
+[ "$nruns" = 102 ] && [ -z "$miss" ] && [ -z "$extra" ]; check "E0  all  the fake codex was reached by every run but X15's, and by none of X15's (34 rows x 3 = $nruns of 102, pinned)${miss:+ -- NOT reached:$miss}${extra:+ -- X15 REACHED it:$extra}" $?
 #  content, not exit status -- on the AFTER logs
 grep -q 'model UNVERIFIED' "$T/log_M2_after.txt" && ! grep -q 'answered by:' "$T/log_M2_after.txt"; check "M2  after  says model UNVERIFIED and names no model" $?
 grep -q 'model UNVERIFIED' "$T/log_X6_after.txt" && ! grep -q 'answered by:' "$T/log_X6_after.txt"; check "X6  after  a quoted model: line is NOT read as the header" $?
 [ -s "$T/out_D1_after/codex_D1.refused.err" ] && grep -q 'answered by: gpt-daybreak-blue-latest' "$T/log_D1_after.txt"; check "D1  after  refused run kept, Daybreak credited" $?
 grep -q 'model UNVERIFIED' "$T/log_X9_after.txt" && ! grep -q 'answered by:' "$T/log_X9_after.txt"; check "X9  after  a late QUOTED header block is NOT read as the header" $?
+grep -q 'model UNVERIFIED' "$T/log_W13_after.txt" && ! grep -q 'answered by:' "$T/log_W13_after.txt"; check "W13 after  a header whose first rule is line 13 is NOT read" $?
+grep -q 'model UNVERIFIED' "$T/log_K31_after.txt" && ! grep -q 'answered by:' "$T/log_K31_after.txt"; check "K31 after  a model line at body line 31 of an unterminated block is NOT read" $?
+[ "$(grep -c '^CALL$' "$T/args_FB1_after" 2>/dev/null)" = 1 ] && ! ls "$T/out_FB1_after"/*.refused.* >/dev/null 2>&1; check "FB1 after  the fallback on, an answer: ONE call, nothing renamed .refused" $?
+[ "$(grep -c '^CALL$' "$T/args_FB2_after" 2>/dev/null)" = 1 ]; check "FB2 after  the fallback on, a wall: ONE call" $?
+[ "$(grep -c '^CALL$' "$T/args_D4_after" 2>/dev/null)" = 2 ]; check "D4  after  refused, then refused on Daybreak: EXACTLY two calls" $?
+[ "$(grep -c '^CALL$' "$T/args_D3_after" 2>/dev/null)" = 2 ] && grep -q 'answered by: gpt-daybreak-blue-latest' "$T/log_D3_after.txt"; check "D3  after  a doubled refusal re-runs on Daybreak: two calls, Daybreak credited" $?
+[ ! -e "$T/args_X15_after" ]; check "X15 after  a 30,001-byte brief never reaches codex" $?
 #  E1/E2: the exact argument sequence of each call, one argument per line, compared whole
 callseq() {    # $1 model -- the sequence one call must receive
     printf 'CALL\nARG exec\nARG --sandbox\nARG read-only\nARG --skip-git-repo-check\nARG -m\nARG %s\nARG -c\n' "$1"
```

### 3c. the mutant list, `mut_launcher_v3.py` -> `mut_launcher_v4.py`

```diff
--- /c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/cxlaunchland_20261016/mut_launcher_v3.py
+++ /c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/cxlaunchland_20261016/mut_launcher_v4.py
@@ -1,7 +1,8 @@
 #!/usr/bin/env python3
-"""mut_launcher_v3.py <launcher.sh> <out dir> -- write one-edit mutants of tools/cxlaunch.sh (2026-10-16 landing, v3) for the
-controls' kill table (run_mutants_v3.sh).  Each mutant names the control expected to catch it, or UNPINNED with the reason it
-is deliberately not pinned (Fable 5.1, pass 2: a sibling of the recorded N4 residual, or a shape with 0 instances on record).
+"""mut_launcher_v4.py <launcher.sh> <out dir> -- write one-edit mutants of tools/cxlaunch.sh (2026-10-17 landing, v4) for the
+controls' kill table (run_mutants_v4.sh).  Each mutant names the control expected to catch it, or UNPINNED with the reason it
+is deliberately not pinned (a sibling of the recorded N4 residual, or a shape with 0 instances on record -- CENSUS_v4.txt and
+the v4 controls' CONTRACT).  One mutant, m_twice, inserts a line (the fallback run twice): still one edit.
 A find-text that is absent is an apparatus failure, never a silent skip."""
 import io, os, sys
 
@@ -31,9 +32,26 @@
      'if [ "$rc" -ne 0 ] || [ "$body" -eq 0 ]; then', 'if [ "$rc" -eq 1 ] || [ "$body" -eq 0 ]; then'),
     ("m_sgr", "UNPINNED (non-SGR CSI: 0 of 2,372 .err files on record)",
      'strip_ansi() { sed "s/${ESC}\\[[0-9;]*[A-Za-z]//g" "$1" 2>/dev/null; }', 'strip_ansi() { sed "s/${ESC}\\[[0-9;]*m//g" "$1" 2>/dev/null; }'),
-    ("m_prec", "UNPINNED (a refusal and a wall in one stderr: 0 on record)",
+    ("m_prec", "UNPINNED (a refusal and a wall line in one stderr on a run that ENTERS classification: 0 of 410 in CENSUS_v4.txt)",
      r"""        wall=$(printf '%s' "$CXERR" | grep -ic 'usage limit\|quota\|rate limit\|not authenticated')""",
      r"""        wall=$(printf '%s' "$CXERR" | grep -ic 'usage limit\|quota\|rate limit\|not authenticated'); [ "$wall" -gt 0 ] && refus=0"""),
+    #  v4 -- the v3 pass's floor breaches (GPT-6 Astra, Grok 4.7, GLM 5.3) and their edges
+    ("m_win11", "W12", "NR > 12 && h < 2", "NR > 11 && h < 2"),
+    ("m_win13", "W13", "NR > 12 && h < 2", "NR > 13 && h < 2"),
+    ("m_win3", "W12 X13", "NR > 12 && h < 2", "NR > 3 && h < 2"),
+    ("m_cap29", "K30", "if (++n > 30) exit", "if (++n > 29) exit"),
+    ("m_cap31", "K31", "if (++n > 30) exit", "if (++n > 31) exit"),
+    ("m_nocap", "K31", "h == 2 { if (++n > 30) exit; print }", "h == 2 { print }"),
+    ("m_fbeq1", "D3", 'if [ "$refus" -gt 0 ] && [ -n "$AUP_MODEL" ]', 'if [ "$refus" -eq 1 ] && [ -n "$AUP_MODEL" ]'),
+    ("m_refeq1", "R2X", 'if [ "$refus" -gt 0 ]; then', 'if [ "$refus" -eq 1 ]; then'),
+    ("m_wallgt1", "W1L", 'if [ "$wall" -gt 0 ]; then', 'if [ "$wall" -gt 1 ]; then'),
+    ("m_fbge0", "FB1", 'if [ "$refus" -gt 0 ] && [ -n "$AUP_MODEL" ]', 'if [ "$refus" -ge 0 ] && [ -n "$AUP_MODEL" ]'),
+    ("m_fbwall", "FB2", 'if [ "$refus" -gt 0 ] && [ -n "$AUP_MODEL" ]',
+     'if { [ "$refus" -gt 0 ] || [ "$wall" -gt 0 ]; } && [ -n "$AUP_MODEL" ]'),
+    ("m_twice", "D4 E2", '    run_codex "$AUP_MODEL" "$AUP_EFFORT"; classify\n',
+     '    run_codex "$AUP_MODEL" "$AUP_EFFORT"; classify\n    run_codex "$AUP_MODEL" "$AUP_EFFORT"; classify\n'),
+    ("m_argv1", "X15", '[ "$sz" -gt 30000 ]', '[ "$sz" -gt 30001 ]'),
+    ("m_argv2", "X14", '[ "$sz" -gt 30000 ]', '[ "$sz" -gt 29999 ]'),
 ]
 os.makedirs(out, exist_ok=True)
 bad = 0
```

### 3d. `CENSUS_v4.txt` (`census_v4.py`)

```
roots: C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC C:\DocumentNoSnc\cc\GXEMUL\_scratchpad
codex .err files read: 2422
opening blocks by the landed rule: 972 of 2422 files | no model line: 0 | two or more: 0 | unclosed: 0
files with a banner in their first 200 lines but no opening block: 0 of 2422
classification population (sibling .txt empty or absent): 410 of 2422 | carrying BOTH a column-0 refusal and a column-0 wall ERROR line: 0
CENSUS_V4_DONE
```

## 4. The receipts

### 4a. `RECEIPT_v4.txt` -- its result lines (the indented per-run launcher output is omitted; it is in the file)

```
# cxlaunch landing controls (v4), 2026-10-17 01:27:37
# tracked: cb180d9d58da2c0b05defe48c65b7ad0  cxlaunch_tracked.sh
# before:  3c51a7579065c5e6bebd5fd59d32b3ed  cxlaunch_before.sh
# after:   ee4f5aec4955430904886604384da247  /c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/tools/cxlaunch.sh
P1  tracked exit=8  want=8  ok
P1  before  exit=8  want=8  ok
P1  after   exit=8  want=8  ok
P2  tracked exit=7  want=7  ok
P2  before  exit=7  want=7  ok
P2  after   exit=7  want=7  ok
N1  tracked exit=8  want=8  ok
N1  before  exit=0  want=0  ok
N1  after   exit=0  want=0  ok
N2  tracked exit=8  want=8  ok
N2  before  exit=0  want=0  ok
N2  after   exit=0  want=0  ok
N3  tracked exit=6  want=6  ok
N3  before  exit=6  want=6  ok
N3  after   exit=6  want=6  ok
N4  tracked exit=8  want=8  ok
N4  before  exit=8  want=8  ok
N4  after   exit=8  want=8  ok
Q1  tracked exit=7  want=7  ok
Q1  before  exit=7  want=7  ok
Q1  after   exit=7  want=7  ok
Q2  tracked exit=8  want=8  ok
Q2  before  exit=8  want=8  ok
Q2  after   exit=8  want=8  ok
Q3  tracked exit=6  want=6  ok
Q3  before  exit=6  want=6  ok
Q3  after   exit=8  want=8  ok
A1  tracked exit=6  want=6  ok
A1  before  exit=6  want=6  ok
A1  after   exit=7  want=7  ok
M1  tracked exit=8  want=8  ok
M1  before  exit=0  want=0  ok
M1  after   exit=5  want=5  ok
M2  tracked exit=8  want=8  ok
M2  before  exit=0  want=0  ok
M2  after   exit=0  want=0  ok
D1  tracked exit=7  want=7  ok
D1  before  exit=0  want=0  ok
D1  after   exit=0  want=0  ok
D2  tracked exit=7  want=7  ok
D2  before  exit=0  want=0  ok
D2  after   exit=5  want=5  ok
X1  tracked exit=6  want=6  ok
X1  before  exit=6  want=6  ok
X1  after   exit=6  want=6  ok
X2  tracked exit=8  want=8  ok
X2  before  exit=0  want=0  ok
X2  after   exit=0  want=0  ok
X5  tracked exit=8  want=8  ok
X5  before  exit=0  want=0  ok
X5  after   exit=5  want=5  ok
X6  tracked exit=0  want=0  ok
X6  before  exit=0  want=0  ok
X6  after   exit=0  want=0  ok
X8  tracked exit=6  want=6  ok
X8  before  exit=6  want=6  ok
X8  after   exit=8  want=8  ok
X9  tracked exit=0  want=0  ok
X9  before  exit=0  want=0  ok
X9  after   exit=0  want=0  ok
X10 tracked exit=0  want=0  ok
X10 before  exit=0  want=0  ok
X10 after   exit=0  want=0  ok
W12 tracked exit=0  want=0  ok
W12 before  exit=0  want=0  ok
W12 after   exit=5  want=5  ok
W13 tracked exit=0  want=0  ok
W13 before  exit=0  want=0  ok
W13 after   exit=0  want=0  ok
X13 tracked exit=0  want=0  ok
X13 before  exit=0  want=0  ok
X13 after   exit=5  want=5  ok
K30 tracked exit=0  want=0  ok
K30 before  exit=0  want=0  ok
K30 after   exit=5  want=5  ok
K31 tracked exit=0  want=0  ok
K31 before  exit=0  want=0  ok
K31 after   exit=0  want=0  ok
R2X tracked exit=6  want=6  ok
R2X before  exit=6  want=6  ok
R2X after   exit=7  want=7  ok
D3  tracked exit=6  want=6  ok
D3  before  exit=6  want=6  ok
D3  after   exit=0  want=0  ok
D4  tracked exit=7  want=7  ok
D4  before  exit=7  want=7  ok
D4  after   exit=7  want=7  ok
W1L tracked exit=8  want=8  ok
W1L before  exit=8  want=8  ok
W1L after   exit=8  want=8  ok
FB1 tracked exit=8  want=8  ok
FB1 before  exit=0  want=0  ok
FB1 after   exit=0  want=0  ok
FB2 tracked exit=8  want=8  ok
FB2 before  exit=8  want=8  ok
FB2 after   exit=8  want=8  ok
X14 tracked exit=0  want=0  ok
X14 before  exit=0  want=0  ok
X14 after   exit=0  want=0  ok
X15 tracked exit=9  want=9  ok
X15 before  exit=9  want=9  ok
X15 after   exit=9  want=9  ok
E0  all  the fake codex was reached by every run but X15's, and by none of X15's (34 rows x 3 = 102 of 102, pinned)  ok
M2  after  says model UNVERIFIED and names no model  ok
X6  after  a quoted model: line is NOT read as the header  ok
D1  after  refused run kept, Daybreak credited  ok
X9  after  a late QUOTED header block is NOT read as the header  ok
W13 after  a header whose first rule is line 13 is NOT read  ok
K31 after  a model line at body line 31 of an unterminated block is NOT read  ok
FB1 after  the fallback on, an answer: ONE call, nothing renamed .refused  ok
FB2 after  the fallback on, a wall: ONE call  ok
D4  after  refused, then refused on Daybreak: EXACTLY two calls  ok
D3  after  a doubled refusal re-runs on Daybreak: two calls, Daybreak credited  ok
X15 after  a 30,001-byte brief never reaches codex  ok
E1  after  N1: exactly one call, exactly exec --sandbox read-only ... -m gpt-6-astra, effort ultra, the brief  ok
E2  after  D1: exactly two calls, Astra then Daybreak, the same exact arguments each  ok
CONTROLS: 116/116 as expected
CXLAND_CONTROLS_DONE
```

### 4b. `KILLTABLE_v4.txt`, whole

```
mutants written: 32 of 32
# kill table for /c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/tools/cxlaunch.sh (ee4f5aec4955430904886604384da247), 2026-10-17 01:28:35
BASE      CONTROLS: 116/116 as expected
m_anchor      115/116  killed by: X1                                                  [X1]
m_bodyverd    115/116  killed by: X2                                                  [X2]
m_suffix      115/116  killed by: X5                                                  [X5]
m_effort      114/116  killed by: E1 E2                                               [E1 E2]
m_head40      108/116  killed by: K31 W13 X10 X6 X9                                   [X6]
m_v2awk       110/116  killed by: K31 W13 X10 X9                                      [X9 X10]
m_effortx     114/116  killed by: E1 E2                                               [E1 E2]
m_sandbox     114/116  killed by: E1 E2                                               [E1 E2]
m_brief       114/116  killed by: E1 E2                                               [E1 E2]
m_noa         115/116  killed by: X8                                                  [X8]
m_nostrip     111/116  killed by: A1 D3 Q3 R2X                                        [Q3 A1]
m_noident     110/116  killed by: D2 K30 M1 W12 X13 X5                                [M1 D2 X5]
m_nofallback  109/116  killed by: D1 D2 D3 D4 E2                                      [D1 D2 E2]
m_nogate      111/116  killed by: FB1 M1 N1 X2 X5                                     [N1 X2]
m_claimmodel  111/116  killed by: K31 M2 W13 X6 X9                                    [M2 X6]
m_eq1         116/116  escapes (as recorded)                                          [UNPINNED (only an rc outside {0,1} WITH an answer -- a sibling of N4, 0 on record)]
m_sgr         116/116  escapes (as recorded)                                          [UNPINNED (non-SGR CSI: 0 of 2,372 .err files on record)]
m_prec        116/116  escapes (as recorded)                                          [UNPINNED (a refusal and a wall line in one stderr on a run that ENTERS classification: 0 of 410 in CENSUS_v4.txt)]
m_win11       115/116  killed by: W12                                                 [W12]
m_win13       114/116  killed by: W13                                                 [W13]
m_win3        114/116  killed by: W12 X13                                             [W12 X13]
m_cap29       115/116  killed by: K30                                                 [K30]
m_cap31       114/116  killed by: K31                                                 [K31]
m_nocap       114/116  killed by: K31                                                 [K31]
m_fbeq1       114/116  killed by: D3                                                  [D3]
m_refeq1      115/116  killed by: R2X                                                 [R2X]
m_wallgt1     115/116  killed by: W1L                                                 [W1L]
m_fbge0       113/116  killed by: FB1 FB2                                             [FB1]
m_fbwall      115/116  killed by: FB2                                                 [FB2]
m_twice       113/116  killed by: D3 D4 E2                                            [D4 E2]
m_argv1       113/116  killed by: X15                                                 [X15]
m_argv2       114/116  killed by: X14                                                 [X14]
KILL TABLE: 32/32 as recorded
CXLAND_MUTANTS_DONE
```

## 5. The records this landing writes AT COMMIT (previews against HEAD 8bf8b5a1)

### 5a. OUTSTANDING_BUGS.md

```diff
--- ob_head.md
+++ ob_f1_preview.md
@@ -16561,6 +16561,11 @@
 
 `tools/cxlaunch.sh` anchors stderr tests on codex's own `^ERROR:` lines and greps stdout freely;
 exit 7 refusal, 8 wall, 6 empty-with-neither, else `rc`. Controlled in four states.
+*[2026-10-17, the `cxlaunchquotation` landing: the two lines above are kept as written and are NO LONGER TRUE -- "greps
+stdout freely" was the very defect `cxlaunchquotation` was filed for.  The landed file classifies codex's `^ERROR:` lines
+(ANSI-stripped, read with `grep -a`) ONLY when rc != 0 or stdout is empty, never greps stdout for wall words, re-runs a
+refused brief once on Daybreak, and exits 5 when codex's OPENING header block names a different model.  Controls:
+`regress/artifacts/cxlaunchland_20261016/RECEIPT_v4.txt`.]*
 
 *`panel.sh` already had a better, POSITION-based discriminator (head/tail 400 bytes) with the
 incident that taught it recorded in its own comment. A claim here that it did not was false and is
@@ -22509,6 +22514,10 @@
 tool that reads it).  Fix shape: key the stderr test on codex's own error block at the END of the stream, and give the
 stdout patterns word boundaries; negative-control both directions (a real wall still reds; these two runs do not).
 Found while confirming `#550`.
+**MERGED 2026-10-17 into the `cxlaunchquotation` landing, with its fix shape WITHDRAWN** (the three-seat ruling,
+regress/artifacts/adj_20261016/RULINGS_C_records.md F1): keying on codex's LAST `ERROR:` line does not work -- in fixture
+N4 that line is itself a quotation -- so the landed rule keys on the exit status and an empty stdout instead.  This filing
+never had a ledger row; both of its false positives are controlled in `regress/artifacts/cxlaunchland_20261016/RECEIPT_v4.txt` (N1, N2).
 
 ## 2026-09-25 — GXEMUL [087a90]: `#551` wdcidselfcheck; what its review files
 
@@ -24674,6 +24683,11 @@
 once".  The fallback the owner ruled (2026-10-01: `gpt-daybreak-blue-latest` on an Astra AUP refusal) exists only in
 `_scratchpad/codexpack_20260928/cxlaunch_pack.run-*.sh`.  Fix: give `cxlaunch.sh` the pack runner's fallback, and
 correct the comment when `panel.sh` is next reviewed (it carries unreviewed deltas).
+**CLOSED 2026-10-17** (the landing; the heading above is kept as written -- it was true of the tracked file until then).
+The fallback is controlled in `regress/artifacts/cxlaunchland_20261016/RECEIPT_v4.txt` by D1, D2, D3 (a real doubled refusal) and D4 (fires ONCE on a second
+refusal), by FB1/FB2 (it does not fire on an answer or a wall), and by E1/E2 (the exact arguments of both calls); the
+real-run receipt of it firing is `regress/artifacts/codexpack_20260928/dossier_gdromdma/dossier_gdromdma.launch.log`.
+`panel.sh`'s comment is still owed.
 
 ### 2026-10-09 -- `ppcrlwhighhalf` / `ppcwitnessmaskoracle`: the oracle repair committed alone, the rung-3 witness on committed HEAD
 
@@ -24722,6 +24736,10 @@
 * **`cxlaunchquotation` (LOW, open)** -- `tools/cxlaunch.sh`'s wall check greps the seat's answer for `quota`, so an
   answer containing "quotation" is reported SEAT WALLED (rc 8).  Measured 2026-10-09 on a complete GPT-6 Astra answer.
   Word-anchor it and test stdout only when no verdict line is present; controls both ways.
+  **CLOSED 2026-10-17 by the landing, and the fix prescribed above was REPLACED, not applied** (RULINGS_C F1): stdout is
+  never grepped for wall words; codex's `^ERROR:` lines are classified only when rc != 0 or stdout is empty.  The tracked
+  file the landing replaced exits 8 on N1 (a captured real answer whose stderr quotes a codex wall line) and N2 (a
+  synthetic answer carrying the four wall words), and the landed one 0 (`regress/artifacts/cxlaunchland_20261016/RECEIPT_v4.txt`).
 * **`fablequeueregress` (MEDIUM, open)** gains Fable 5.1's stagetokens finding 5: section I's regress guarantee is
   narrower than its docstring -- precommit I2 (the codex wall), not I, forces a held regress review into the queue.
 
@@ -24761,3 +24779,14 @@
   supervisor trap in a slot naming a residual vector (11..113, 116..127) or 114/115 -- is unrowed.  `&& !(cpu->delay_slot
   && is_trap)` at :799 is a PREDICTED 84/84 escape, not measured (Fable 5.1, pass 16, `pass16/fable5_m88kp16.md` section
   4).  Pin if ever rowed: `residtbdslot` = `[BR_N_PLUS16, TB1_0_R3_50]`, r3 = 1, expected HALT naming 0x032.
+
+### 2026-10-17 -- the codex launcher landed in `tools/cxlaunch.sh` (`cxlaunchquotation`, `cxlaunchdaybreak` closed); one row filed
+
+* **`cxlaunchunpinned` (LOW, open)** -- three one-edit escapes of `tools/cxlaunch.sh` stay UNPINNED BY RULING (Fable
+  5.1, pass 2), each MEASURED to escape in `regress/artifacts/cxlaunchland_20261016/KILLTABLE_v4.txt` and each disclosed in the CONTRACT of
+  `run_controls_v4.sh`: `-ne 0` -> `-eq 1` in the classify gate (observable only at an rc outside {0, 1} WITH an answer --
+  a sibling of the recorded N4 residual, which is rc 1, where the two forms agree; 0 of 394 launcher rows, GPT-6 Astra, v3
+  pass); the ANSI strip narrowed to SGR `[0-9;]*m` (0 non-SGR CSI or OSC in 4,851 .err files, the same census); and
+  refusal-before-wall precedence (a refusal and a wall line in one stderr ON A RUN THAT ENTERS CLASSIFICATION: 0 of 410,
+  `regress/artifacts/cxlaunchland_20261016/CENSUS_v4.txt`; rc-0 answered runs that QUOTE both exist and are never classified).  Pin each the day a real
+  instance appears.
```

### 5b. the ledger rows

```
# ledger changes the tools/cxlaunch.sh landing makes, against HEAD (a preview; applied at commit)

== cxlaunchdaybreak 
  closure: {"by": "opus5-mainloop", "badge": "A", "note": "CLOSED by the same landing: a content-filter refusal on Astra is re-run ONCE on gpt-daybreak-blue-latest, the refused run kept as .refused.*, the answer credited to Daybreak; it does not fire on an answer or a wall (D1, D2, D3, D4, FB1, FB2, E1, E2 in RECEIPT_v4.txt; the real-run receipt is codexpack_20260928/dossier_gdromdma/dossier_gdromdma.launch.log)."}
  + entry: {"phase": "regress", "seat": "fable5", "date": "2026-10-17", "grade": "UNKNOWN", "grader": "", "ev": "not fired", "note": "[HELD AWAITING SEAT: fable5] cxlaunchdaybreak closed by the tools/cxlaunch.sh landing and owes the REGRESS review, a distinct phase under the regress-is-fable-only directive, batched to the Sunday flagship sign-off after the battery.  The question is in the row's hold_question."}
  hold_question: "REGRESS (held 2026-10-17 at the tools/cxlaunch.sh landing): does regress/artifacts/cxlaunchland_20261016/RECEIPT_v4.txt still run the TRACKED file the landing replaced, the farm copy and the landed launcher against the same fixtures and get the recorded exits -- in particular N1/N2 8 -> 0 (the quoted-wall false positive), D1 7 -> 0 (the Daybreak fallback), X8 6 -> 8 (a NUL in stderr) and the v4 edge rows (W12/W13, K30/K31, R2X/D3, W1L, FB1/FB2, X14/X15) -- and does regress/artifacts/cxlaunchland_20261016/KILLTABLE_v4.txt still kill every pinned mutant while the three filed in cxlaunchunpinned escape as recorded?  Is the record (the launcher's header, the controls' CONTRACT, the CHANGELOG block, the OB corrections) true of what shipped?"
  state: "closed"
  witness: "harness:regress/artifacts/cxlaunchland_20261016/RECEIPT_v4.txt -- D1: the tracked launcher exits 7 on a refusal (no fallback), the landed one re-runs it once on gpt-daybreak-blue-latest and credits Daybreak (exit 0); D3 (a real doubled refusal), D4 (exactly two calls on a second refusal), FB1/FB2 (no re-run on an answer or a wall) and E1/E2 (both calls' exact arguments) pin it; the real-run receipt is regress/artifacts/codexpack_20260928/dossier_gdromdma/dossier_gdromdma.launch.log"

== cxlaunchquotation 
  closure: {"by": "opus5-mainloop", "badge": "A", "note": "CLOSED by the tools/cxlaunch.sh landing: the production rule (codex's ^ERROR: lines, ANSI-stripped and read with grep -a, classified ONLY when rc != 0 or stdout is empty; stdout never grepped for wall words) replaces the classifier that scored a complete answer WALLED for the word 'quota' or a quoted wall line.  Witness: the tracked file exits 8 on N1/N2, the landed one 0 (RECEIPT_v4.txt).  The controls' CONTRACT (run_controls_v4.sh) names every decision's pinned edges and the three disclosed escapes.  Four passes on the landed file -- pass 2, the adjudication pass, the v3 pass and the v4 pass, the owner's four-seat roster each time (Fable 5.1 stalled on the adjudication and v3 passes; Opus, agy, kimi, deepseek and minimax not fired)."}
  + entry: {"phase": "regress", "seat": "fable5", "date": "2026-10-17", "grade": "UNKNOWN", "grader": "", "ev": "not fired", "note": "[HELD AWAITING SEAT: fable5] cxlaunchquotation closed by the tools/cxlaunch.sh landing and owes the REGRESS review, a distinct phase under the regress-is-fable-only directive, batched to the Sunday flagship sign-off after the battery.  The question is in the row's hold_question."}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "codex", "note": "PASS 2 (the landed launcher, v1): SHIP WITH CHANGES (2) -- GPT-6 Astra (ultra, `ran: model: gpt-6-astra'): read the model only from codex's header block and stop crediting 'answered by' when it is absent; make the controls exit non-zero on a bad tally and pin the `^ERROR:' anchor and the effort argument.  Both applied in v2.", "ev": "regress/artifacts/cxlaunchland_20261016/pass2/codex_cxland.txt", "d": "✓"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "glm", "note": "PASS 2: SHIP WITH CHANGES (2) -- GLM 5.3 (glm-5.3:cloud): reword the UNVERIFIED note to what was searched and put a count behind the header window; record that the ANSI strip widens both residuals.  Applied (v2 dropped the window for the header block; the residual is in the launcher's header).", "ev": "regress/artifacts/cxlaunchland_20261016/pass2/glm_cxland.txt", "d": "✓"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "grok", "note": "PASS 2: SHIP WITH CHANGES (1) -- Grok 4.7 (xhigh): grep without -a reads a NUL-bearing stderr as binary and drops the wall lines -- the real 2026-09-19 battery-preflight wall was recorded exit 6.  Measured on that file and fixed (grep -a, control X8).", "ev": "regress/artifacts/cxlaunchland_20261016/pass2/grok_cxland.txt", "d": "✓"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "fable5", "note": "PASS 2: SHIP WITH CHANGES (2) -- Fable 5.1, in two parts: its first run FELL BACK to claude-opus-4-8 after two refusals (FALLBACK_opus48_cxland.md, credited as Opus 4.8, and that run executed the TRACKED launcher unmodified and fired nine real Astra calls -- disclosed, no tree writes); resumed, Fable 5.1 wrote v2 itself: C1 add the tracked file as the pre-fix column, C2 correct two bug-file statements by content, pin four escapes and leave two unpinned.  All applied.", "ev": "regress/artifacts/cxlaunchland_20261016/pass2/fable5_cxland_v2.md", "d": "✓"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "codex", "note": "ADJUDICATION PASS (v2): SHIP WITH CHANGES (3) -- GPT-6 Astra: the header-block awk matched the banner ANYWHERE (N1's own stderr quotes four complete headers from line 5528), so v3 reads only the OPENING block; E1/E2 matched a substring, so `ultrax' passed -- v3 compares the exact argument sequence; and the record edits the packet called done were not yet in the tree.", "ev": "regress/artifacts/cxlaunchland_20261016/f2/codex_cxlandf2.txt", "d": "✓"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "grok", "note": "ADJUDICATION PASS (v2): SHIP WITH CHANGES (3) -- Grok 4.7: launcher, controls and kill table hold; the three changes are the records the packet described as written (F10, F19, the cxlaunchunpinned filing), which were prepared but not yet applied.", "ev": "regress/artifacts/cxlaunchland_20261016/f2/grok_cxlandf2.txt", "d": "✓"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "glm", "note": "ADJUDICATION PASS (v2): SHIP WITH CHANGES (3) -- GLM 5.3, answering under the Fable seat's token (the packet listed all four; the transport is glm-5.3:cloud): cite RECEIPT_v2 not RECEIPT in the header, correct m_eq1's reason (N4 is rc 1; the observable shape is an rc outside {0,1} with an answer), pin --sandbox read-only and the brief.  All applied in v3.", "ev": "regress/artifacts/cxlaunchland_20261016/f2/glm_cxlandf2.txt", "d": "✓"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "fable5", "note": "ADJUDICATION PASS (v2): SEAT FAILURE -- the Fable 5.1 agent STALLED (stream watchdog, no progress for 600 s) after its opening line; no answer file.  Re-fired on the v3 pass, not counted as agreement."}
  + entry: {"date": "2026-10-17", "phase": "review", "seat": "codex", "note": "V3 PASS: SHIP WITH CHANGES (3) -- GPT-6 Astra: FLOOR BREACHES in v3's controls -- `NR > 12' -> `NR > 3' (the one real warning-prefixed header on record would go UNVERIFIED), the refusal guards `-gt 0' -> `-eq 1' at both sites and the wall guard `-gt 0' -> `-gt 1' (every fixture carried count 1 or 2+), refusal-then-refusal unrowed; the header comment's 'never names the model' survived; and 'no stderr on record carries both' is false for rc-0 answers.  All addressed in v4 (the class closure).", "ev": "regress/artifacts/cxlaunchland_20261016/v3pass/codex_cxlandv3.txt", "d": "✓"}
  + entry: {"date": "2026-10-17", "phase": "review", "seat": "grok", "note": "V3 PASS: SHIP WITH CHANGES (3) -- Grok 4.7: FLOOR BREACH -- the fallback test `-gt 0' -> `-ge 0' (or widened with the wall count) passes all 70 because every row but D1/D2 disables the fallback, while production would re-run Daybreak on every answer; the window pinned only up to 20; the G9 bracket named the stale lines wrong.  All addressed in v4 (FB1/FB2 run with the fallback on).", "ev": "regress/artifacts/cxlaunchland_20261016/v3pass/grok_cxlandv3.txt", "d": "✓"}
  + entry: {"date": "2026-10-17", "phase": "review", "seat": "glm", "note": "V3 PASS: SHIP WITH CHANGES (2) -- GLM 5.3: FLOOR BREACHES -- a window widened up to `NR > 20' passes (X9's quoted block sits at line 21), and the 30-line cap is pinned by nothing (`print' unconditional passes all 70).  Both addressed in v4 (W12/W13 and K30/K31 at the edges).", "ev": "regress/artifacts/cxlaunchland_20261016/v3pass/glm_cxlandv3.txt", "d": "✓"}
  + entry: {"date": "2026-10-17", "phase": "review", "seat": "fable5", "note": "V3 PASS: SEAT FAILURE -- the Fable 5.1 agent STALLED again (stream watchdog, 600 s), after reading the launcher and before writing an answer; most likely the whole 18-mutant kill table run as ONE foreground command (about 13 minutes).  Re-fired on the v4 pass with that hazard named."}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "opus5", "note": "PASS 2 through the v4 pass, NOT FIRED: outside the owner's four-seat roster; the measurements an Opus seat would make were the main loop's control and kill-table runs, each receipted."}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "agy", "note": "PASS 2 through the v4 pass, NOT FIRED: agy is not on the owner's roster for this landing."}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "kimi", "note": "PASS 2 through the v4 pass, NOT FIRED: the kimi seat sat outside the roster; nothing was sent."}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "deepseek", "note": "PASS 2 through the v4 pass, NOT FIRED: GLM 5.3 was the one packet-fed seat fired."}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "minimax", "note": "PASS 2 through the v4 pass, NOT FIRED: minimax-m3 was not given any packet; the roster, not a wall."}
  hold_question: "REGRESS (held 2026-10-17 at the tools/cxlaunch.sh landing): does regress/artifacts/cxlaunchland_20261016/RECEIPT_v4.txt still run the TRACKED file the landing replaced, the farm copy and the landed launcher against the same fixtures and get the recorded exits -- in particular N1/N2 8 -> 0 (the quoted-wall false positive), D1 7 -> 0 (the Daybreak fallback), X8 6 -> 8 (a NUL in stderr) and the v4 edge rows (W12/W13, K30/K31, R2X/D3, W1L, FB1/FB2, X14/X15) -- and does regress/artifacts/cxlaunchland_20261016/KILLTABLE_v4.txt still kill every pinned mutant while the three filed in cxlaunchunpinned escape as recorded?  Is the record (the launcher's header, the controls' CONTRACT, the CHANGELOG block, the OB corrections) true of what shipped?"
  state: "closed"
  state_note: "filed 2026-10-09: measured on GPT-6 Astra's check of the asiceventaddr convergence -- a complete 10,466-byte answer with its verdict line, no `ERROR:` line on stderr, and the launcher printed 'SEAT WALLED' (LAUNCH_RC=8) because the answer's own sentence '... its quotation must retain ...' matched `grep -ic 'quota'` (the answer: regress/artifacts/fablequeue8n_20261009/astra_confirm/codex_astra_asicconverge.txt; the launcher's own output: cxlaunch_asicconverge_stdout.txt beside it).  tools/cxlaunch.sh:44 builds `wall` from the `ERROR:` lines PLUS the whole stdout, so any answer that uses the words quota / quotation / rate limit / usage limit reads as a wall -- the carrier's quoting-re-arms-the-reader class, one level down (the script's own comment at :33-41 diagnoses the stderr half and kept the stdout half).  Fix: word-anchor the pattern and test stdout only when no verdict line is present; owes controls both ways (a real 403/quota notice still reds; an answer containing 'quotation' does not).  LOW: a human reads the answer; an unattended runner would discard it.\n\n[2026-10-17] CLOSED by the tools/cxlaunch.sh landing -- and the fix this note prescribes (\"word-anchor the pattern and test stdout only when no verdict line is present\") was REPLACED by the three-seat ruling's production rule, not applied: stdout is never grepped for wall words; codex's ^ERROR: lines are classified only when rc != 0 or stdout is empty (regress/artifacts/adj_20261016/RULINGS_C_records.md F1).  Merges the 2026-09-26 filing cxlaunchwallfp (no ledger row)."
  witness: "harness:regress/artifacts/cxlaunchland_20261016/RECEIPT_v4.txt -- the TRACKED launcher (cb180d9d) exits 8 on N1, a captured real Astra answer whose stderr quotes a codex wall line, and on N2, a synthetic answer carrying the four wall words ('quota' among them); the landed file exits 0 on both; regress/artifacts/cxlaunchland_20261016/KILLTABLE_v4.txt kills every pinned one-edit mutant of the landed file"

== cxlaunchunpinned (NEW ROW)
  commits: ""
  id: "cxlaunchunpinned"
  sev: "LOW"
  state: "open"
  state_note: "filed 2026-10-17 from the landing's pass 2 (Fable 5.1, regress/artifacts/cxlaunchland_20261016/pass2/fable5_cxland_v2.md) and re-checked on the v3 pass: each is MEASURED to escape the landed controls in regress/artifacts/cxlaunchland_20261016/KILLTABLE_v4.txt and is disclosed in the CONTRACT of run_controls_v4.sh.  Censuses: 0 of 394 launcher rows exit outside {0, 1} (GPT-6 Astra); 0 non-SGR CSI or OSC in 4,851 .err files (Astra); 0 of 410 runs that enter classification carry both a refusal and a wall line (regress/artifacts/cxlaunchland_20261016/CENSUS_v4.txt).  Pin each the day a real instance appears: a codex run exiting outside {0, 1} with an answer and a quoted wall line; a non-SGR CSI or OSC sequence before a codex diagnostic; a classified stderr carrying both a refusal and a wall line."
  title: "tools/cxlaunch.sh: three one-edit escapes are unpinned by ruling -- `-ne 0` -> `-eq 1` in the classify gate (an rc outside {0, 1} with an answer, a sibling of the N4 residual), the ANSI strip narrowed to SGR, and refusal-before-wall precedence (0 instances of each on record)"
  witness: null
```

### 5c. regress/artifacts/adj_20261016/RULINGS_C_records.md (V12)

```diff
--- rulingsC_head.md
+++ rulingsC_f1_preview.md
@@ -35,6 +35,12 @@
 - MERGE the prior filing `cxlaunchwallfp` (OUTSTANDING_BUGS.md:22494-22503, 2026-09-26, no ledger row) into this
   landing (Fable); correct OB:24714-24716 and ledger :62489 to this rule; closes `cxlaunchdaybreak` (ultra + Daybreak
   ride along).
+  *[2026-10-17, at the launcher landing (Grok 4.7, adjudication and v3 passes): these line citations did not hold even
+  at this file's own commit c64445fa, where `OUTSTANDING_BUGS.md:22494-22503` runs from the body of `asanfifteen` into
+  the first two lines of `cxlaunchwallfp`, `:24714-24716` is `stagetokenscontrols`, and ledger `:62489` is the
+  `armvecrecurse` row.  The entries MEANT, by id: the `cxlaunchwallfp` bug-file entry, the `cxlaunchquotation` bug-file
+  entry ("Word-anchor it and test stdout only when no verdict line is present") and the `cxlaunchquotation` ledger
+  row.]*
 - NEW, from Astra: the launcher prints the model it RAN but `ANSWERED_BY` is the model it ASKED for -- the "a wrong name is
   a SEAT FAILURE" comment is unenforced.  File as a rider on the landing (compare the `^model:` header to the request).
 
```

### 5d. the CHANGELOG block (a DRAFT: its v4-pass sentence is written from this pass's answers)

# `cxlaunchquotation` + `cxlaunchdaybreak` (2026-10-17): the codex launcher lands in `tools/cxlaunch.sh` -- a complete answer is never scored WALLED for quoting a wall line, a content-filter refusal on Astra is re-run ONCE on Daybreak, and a different model named by codex's OPENING header exits 5; the controls carry a CONTRACT naming every decision's pinned edges (v4, 116 checks, 32 mutants)

**Ruled before any code** by Fable 5.1, GPT-6 Astra and Grok 4.7 (`regress/artifacts/adj_20261016/RULINGS_C_records.md`,
F1): codex's `^ERROR:` lines are classified ONLY when rc != 0 or stdout is empty, and stdout is never grepped for wall
words -- the discriminator is the exit status and the answer, which quoted text cannot forge.  Every real wall and refusal
on record is rc 1 with an empty stdout, and every rc-0 run carries an answer.

* `tools/cxlaunch.sh`: until this landing the tracked file ran Astra at `max` with the 2026-09-07 classifier while most farm
  jobs ran an untracked scratchpad copy -- and the carrier described the copy's behaviour as the tracked file's.  The landed
  file: ANSI colour stripped and `grep -a` before the `^ERROR:` anchor (a real coloured refusal read exit 6 unstripped; a
  real NUL-bearing wall read exit 6 without `-a`); the Daybreak fallback (`gpt-daybreak-blue-latest`, the refused run kept
  as `.refused.*`, the answer credited to Daybreak); the model read ONLY from codex's OPENING header block -- banner and
  first rule by line 12, the block for at most 30 lines -- and compared with the model asked for (exit 5 on a mismatch,
  "model UNVERIFIED", exit 0, with no opening block); the effort `ultra`.  Its header records the residuals (N4 and its
  refusal twin), exit 5's novelty to the pack runner, and the controls.
* Controls `regress/artifacts/cxlaunchland_20261016/run_controls_v4.sh`: every row drives three launchers -- the TRACKED file
  the landing replaced (the pre-fix column), the farm copy, and the landed file -- against a fake codex replaying a fixture.
  116/116 (`RECEIPT_v4.txt`): N1/N2 8 -> 0 (the quoted-wall false positive), D1 7 -> 0 (the fallback), X8 6 -> 8 (a NUL in
  stderr), and the v4 edges (W12/W13 the window, K30/K31 the cap, R2X/D3 a real doubled refusal at both guards, W1L one wall
  line, FB1/FB2 the fallback left on, D4 exactly two calls, X14/X15 the argv cap).  Its header is the CONTRACT: each decision
  the launcher makes, the rows that pin its edges, and what is deliberately not pinned, with `CENSUS_v4.txt` (2,422 codex
  `.err` files: 0 of 972 opening blocks without exactly one model line; 0 of 410 classified runs carrying both a refusal and
  a wall line) behind the disclosures.  Kill table `run_mutants_v4.sh`: 32/32 as recorded (`KILLTABLE_v4.txt`) --
  29 one-edit mutants killed by the controls their lines name, the three escapes filed as `cxlaunchunpinned`.
* Records: `cxlaunchquotation` and `cxlaunchdaybreak` closed (witness `harness:`; REGRESS reviews HELD for the flagship);
  `cxlaunchwallfp` (2026-09-26, no ledger row) merged with its tail-key fix WITHDRAWN; the bug file's stale "greps stdout
  freely" and "has no Daybreak fallback" statements bracketed by content; `cxlaunchunpinned` (LOW) filed; RULINGS_C's
  drifted line citations re-cited by id.

**Pass 2** (`pass2/`, on v1): Astra SWC 2, GLM SWC 2, Grok SWC 1 (the NUL-bearing wall, measured), Fable SWC 2 (its first run
fell back to claude-opus-4-8 after two refusals -- disclosed, credited as Opus 4.8; resumed, Fable 5.1 wrote v2).
**Adjudication pass** (`f2/`, on v2): Astra SWC 3 (the header awk matched the banner ANYWHERE -- N1's own stderr quotes four
headers; E1/E2 matched a substring), Grok SWC 3 and GLM SWC 3 (records described as written; the receipt citation;
`m_eq1`'s reason); Fable SEAT FAILURE (a stall).  **V3 pass** (`v3pass/`): Astra SWC 3, Grok SWC 3, GLM SWC 2 -- each found
one-edit mutants passing all 70 v3 controls (the window and cap constants, the refusal and wall multiplicity guards, the
fallback predicate), the same class as the two passes before, so v4 is the CLASS CLOSURE; Fable SEAT FAILURE (a second
stall).  **V4 pass** (`v4pass/`): [to be written].  Opus, agy, kimi, deepseek and minimax not fired, by the owner's roster
of 2026-10-16.

## 6. Questions -- verdict line first (`VERDICT: CLOSE` / `SHIP WITH CHANGES (n)` / `DO NOT SHIP`), then answer each by number; say plainly what you could not check

1. **Your own findings.**  For each finding of yours in section 2 (V1-V16): is my disposition right, and is the FIX right
   -- not only the finding?
2. **The enumeration.**  Is the CONTRACT complete (section 2b's first question)?  Name every decision you checked.
3. **The kill table and the floor.**  Is any mutant killed for a reason OTHER than the one its line names?  Is there a
   one-edit mutant of the v4 launcher, NOT in the table, that passes all 116 controls and breaks a ruled property?  If you
   find none, name the shapes you swept.
4. **The records (section 5).**  Is that text true of what ships?  Name any sentence that is false.
5. **Which of my accepted dispositions is wrong?**  There are 16 in section 2; name the count you checked.
