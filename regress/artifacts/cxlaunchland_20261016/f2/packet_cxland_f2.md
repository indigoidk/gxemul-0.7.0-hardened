# ADJUDICATION PASS (§F2) -- the `tools/cxlaunch.sh` landing: the four seats' pass-2 findings, my dispositions, and the repair

Four seats, by the owner's roster of 2026-10-16: Fable 5.1, GPT-6 Astra, Grok 4.7, GLM 5.3.  Opus, agy, kimi, deepseek and
minimax are DELIBERATELY NOT FIRED under that roster.  An ordinary review of a test-harness script (a launcher that runs one
read-only review job through a CLI and classifies how it ended).  READ-ONLY: write nothing to any project tree.  The tree is
`C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC`; the REPAIRED launcher is now the working-tree `tools/cxlaunch.sh` (v2), and its
controls and kill table are in `regress/artifacts/cxlaunchland_20261016/` (`run_controls_v2.sh`, `RECEIPT_v2.txt`,
`mut_launcher.py`, `run_mutants.sh`, `KILLTABLE.txt`).  Everything a packet-fed seat needs is inlined.

**This pass SHARES every seat's findings with every seat.**  Rule on your OWN findings harder than on anyone else's --
including whether the FIX I made for it is right, not only whether the finding was.  **The load-bearing question is
section 5's: which of my accepted dispositions is wrong?**

Open with your seat token -- `FABLE_CXLANDF2_20261016` / `ASTRA_CXLANDF2_20261016` / `GROK_CXLANDF2_20261016` /
`GLM_CXLANDF2_20261016` -- then ONE line: `VERDICT: SHIP / SHIP WITH CHANGES (<n>) / DO NOT SHIP (<one line>)`.

## 1. The pass-2 verdicts (answers in `regress/artifacts/cxlaunchland_20261016/pass2/`)

* **GPT-6 Astra -- SHIP WITH CHANGES (2)** (`codex_cxland.txt`).
* **GLM 5.3 -- SHIP WITH CHANGES (2)** (`glm_cxland.txt`).
* **Grok 4.7 -- SHIP WITH CHANGES (1)** (`grok_cxland.txt`).
* **Fable 5.1 -- SHIP WITH CHANGES (2)** (`fable5_cxland_v2.md`).  ITS FIRST RUN FELL BACK: two Fable refusals, then
  claude-opus-4-8 wrote `FALLBACK_opus48_cxland.md` (credited as Opus 4.8, NOT Fable); the agent was resumed and Fable 5.1
  wrote v2 itself, re-affirming the fallback's findings.  **Fable disclosed that the fallback run executed the TRACKED
  launcher unmodified -- it names its codex binary under `$HOME` and honours no override -- and so launched NINE REAL Astra
  calls on a 13-byte brief before stopping them** (nothing written to any tree).  That hazard is now pinned (E0, below).

## 2. Every finding, numbered, with my disposition

| # | seat | finding | disposition |
|---|---|---|---|
| F1 | Astra | identity: a `model:` line is read from the first 40 stderr lines; with the header absent a QUOTED `model:` line could be read; and an unverified run still printed "answered by: <requested>" | **ACCEPTED, FIXED**: only codex's header BLOCK is read (`OpenAI Codex vX`, then the lines between the next two `--------` rules); an unverified run prints "seat answered -- model UNVERIFIED ... (requested: X)" and still exits 0.  Controls X6, M2 |
| F2 | Astra | the controls driver exits 0 whatever its tally | **ACCEPTED, FIXED**: it exits non-zero unless pass == total |
| F3 | Astra, GLM, Fable, Grok | delete the `^` from `grep '^ERROR:'` -> passes all 30 | **ACCEPTED, PINNED**: X1 (rc 1, empty stdout, only a PREFIXED quotation of a refusal line -> 6) |
| F4 | Astra | `model_reasoning_effort="$2"` -> `"$1"` passes all 30 (the fake ignores arguments) | **ACCEPTED, PINNED**: the fake logs its arguments; E1/E2 assert `-m` and `model_reasoning_effort=ultra` per call |
| F5 | GLM | the UNVERIFIED note misstated its cause; the 40-line window had one fixture behind it | **SUPERSEDED by F1** (no window now); header-line census quoted in the comment (Astra: line 5 in 599 of 600 codex `.err`, line 7 in one) |
| F6 | GLM | the ANSI strip widens the two recorded residuals to colour-prefixed quoted lines | **ACCEPTED as a RECORDED RESIDUAL** in the launcher's header (bounded by classify-on-failure) |
| F7 | GLM | a refused FIRST run's header is never compared | **RECORDED RESIDUAL** (its answer is discarded; the fallback's own run is compared) |
| F8 | GLM | "a coloured real wall" overstated the on-record warrant | **CORRECTED**: the header now cites the real coloured REFUSAL, `_scratchpad/panel_20260919_013302/codex_adv540p2.REFUSED1.err` (unstripped `^ERROR:` 0 lines, stripped 2 -- re-run by me) |
| F9 | Fable (C1) | the controls' baseline was the farm copy, which already had the quotation fix, so no control showed `cxlaunchquotation`'s defect | **ACCEPTED, FIXED**: a THIRD column runs the TRACKED file the landing replaces (`cxlaunch_tracked.sh`, md5 cb180d9d), via a scratch `$HOME` whose codex path is the fake; N1/N2 exit 8 there and 0 after, D1 7 there and 0 after |
| F10 | Fable (C2) | two bug-file statements are now false: the `cxlaunchdaybreak` heading and the rule statement "greps stdout freely"; the ruling's line numbers are stale | **ACCEPTED**: both corrected in place by content, quoting what they refute; the ruling's two targets re-located by id |
| F11 | Fable | `body -eq 0` -> `verd -eq 0` passes all 30 | **ACCEPTED, PINNED**: X2 (rc 0, an answer with NO verdict line, column-0 wall lines on stderr -> 0) |
| F12 | Fable | a suffix-only identity compare passes all 30 | **ACCEPTED, PINNED**: X5 (asked gpt-5-astra, header gpt-6-astra -> 5) |
| F13 | Fable | `-ne 0` -> `-eq 1`, and the strip narrowed to SGR, pass all 30 | **NOT PINNED, by Fable's own ruling**: the first is observable only inside the recorded N4 residual (a pin would assert its wrong exit), the second needs a shape with 0 instances on record; with GLM's precedence escape, FILED as `cxlaunchunpinned`, each measured to ESCAPE in the kill table |
| F14 | GLM | moving the wall exit above the refusal exit passes all 30 | **NOT PINNED** (no stderr on record carries both) -- in `cxlaunchunpinned` |
| F15 | Grok | `grep` without `-a` reads a stderr carrying a NUL as BINARY and prints `Binary file (standard input) matches`: the real 2026-09-19 wall `_scratchpad/cxfarm3_20260919/out/codex_l1_batterypreflight.err` (1,449 NULs from byte 2,318,517; its two column-0 usage-limit lines after them) was recorded exit 6 | **ACCEPTED, FIXED, measured by me on that file**: `grep -a`; X8 (a NUL before the wall lines) exits 6 on both older launchers and 8 after |
| F16 | Grok | exit 5 is new to callers: the farm pack runner special-cases 7 and 8 only and RETRIES a 5 | **RECORDED** in the launcher's header (a different model's answer is not this seat's answer) |
| F17 | Grok, GLM | N1's stderr says `reasoning effort: max` (a max-era run) while the control asks ultra -- so the effort must NOT be compared | **AGREED**; only the model is compared |
| F18 | Astra | census scope: inside GXEMUL-SEC 493 launch logs / 319 pairs, not 519 / 322 | **CORRECTED**: the header states both scopes (519 / 322 under the project root incl. `_scratchpad`) |
| F19 | Grok | `cxlaunchquotation`'s state note still prescribes the replaced fix; `cxlaunchwallfp`'s merge must say its fix was withdrawn | **ACCEPTED**: both written so |

## 3. Disagreements, both sides in their own words

* **Pin the five escapes now, or file them?**  Fable's fallback reading (Opus 4.8): *"above-floor coverage debt, not a
  clause-(d) breach of this landing ... FILE a row to add two pins."*  Fable 5.1 itself (v2): *"CHANGE from my earlier
  'file' to PIN NOW, under L1: the controls are uncommitted, so they are pre-ship construction ... Take four ... Skip two."*
  Astra required the `^` pin and the effort pin as changes.  **I followed Fable's v2** and Astra: four pins plus the
  header-block control, three escapes filed.
* **Does the ANSI strip have an on-record warrant?**  GLM: *"no real codex diagnostic on record is coloured -- the coloured
  walls that exist are quoted panel text -- so the strip's on-record warrant is consistency."*  Fable's fallback reading
  found a real coloured REFUSAL (`codex_adv540p2.REFUSED1.err`), which I re-ran: unstripped 0, stripped 2.  **I hold the
  strip warranted by that real instance.**

## 4. The repair -- `diff -u` of the pass-2 launcher (v1, md5 47d47097) against the working-tree `tools/cxlaunch.sh` (v2, md5 2e611905), 5 hunks

```diff
--- /c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/cxlaunchland_20261016/cxlaunch_landed_v1.sh	2026-10-16 22:31:45.072684900 -0500
+++ /c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/tools/cxlaunch.sh	2026-10-16 22:31:45.093913400 -0500
@@ -31,11 +31,14 @@
 #       the classifier on fixtures, which is a different claim.
 #    3. (2026-10-16, Fable 5.1) codex's diagnostics are matched AFTER ANSI colour is stripped.  7 of 453 panel.sh
 #       codex.txt files carry a column-0 `ERROR:` coloured as ESC[1m ESC[31m ERROR: ESC[0m
-#       (adj_20261016/fable5/meas_C/ansi_census.txt; 0 of 593 launcher .err files), and the unstripped anchor read
-#       such a real wall as exit 6 "seat down" (Fable's Q3).
-#    4. (2026-10-16, GPT-6 Astra) the `model:` header codex prints is COMPARED to the model asked for.  This file
-#       printed both and compared neither, so "a wrong name is a SEAT FAILURE" was unenforced.  322 asked/ran pairs
-#       across 519 launch logs on 2026-10-16: no header absent, no mismatch -- so a mismatch is new, and it exits 5.
+#       (adj_20261016/fable5/meas_C/ansi_census.txt; 0 of 593 launcher .err files), and one is a REAL codex refusal:
+#       _scratchpad/panel_20260919_013302/codex_adv540p2.REFUSED1.err, where `grep '^ERROR:'` finds 0 lines unstripped
+#       and 2 stripped.  Unstripped, such a run reads exit 6 "seat down" (Fable's Q3 is the wall-shaped twin).
+#    4. (2026-10-16, GPT-6 Astra) the `model:` line of codex's HEADER BLOCK is COMPARED to the model asked for.  This
+#       file printed both and compared neither, so "a wrong name is a SEAT FAILURE" was unenforced.  On record: 322
+#       asked/ran pairs across 519 launch logs under the project root, 319 across 493 inside GXEMUL-SEC (Astra), no
+#       header absent and no mismatch -- so a mismatch is new, and it exits 5.  Only the header block is read (pass 2,
+#       Astra): a `model:` line anywhere else in stderr is streamed source or the brief, and never names the model.
 #
 #  KNOWN RESIDUALS -- recorded, NOT fixed (the ruling's own wording; no real run has either shape, 0 of 387 launch
 #  lines are off the diagonal of {rc 0 with stdout, rc 1 with empty stdout} -- adj_20261016/fable5/meas_C/
@@ -44,14 +47,23 @@
 #      `ERROR:` line does not fix it: in N4 that line is itself a quotation.
 #    * its refusal twin: a quoted `flagged for possible cybersecurity` line on rc != 0 -> the Daybreak re-run fires
 #      and the first answer is renamed codex_<tag>.refused.* (Grok 4.7).
-#    * a run whose stderr carries NO `model:` header is reported UNVERIFIED and is not failed (none on record).
+#    * a run whose stderr carries NO codex header block is reported "model UNVERIFIED" and is not failed -- 0 of 330
+#      launcher-captured answered runs on record lack it (counted on pass 2); failing it would lose every answer to a
+#      CLI format change.
+#    * the ANSI strip widens both residuals above to colour-prefixed quoted lines on a failed or empty run (GLM 5.3,
+#      pass 2): a quoted line whose only prefix was colour becomes column-0 -- still inside the classify-on-failure gate.
+#    * a REFUSED first run's header is printed (`ran:`) but not compared; its answer is discarded, and the fallback's
+#      own run is the one compared (GLM 5.3, pass 2).
+#    * exit 5 is new to callers: the farm's pack runner special-cases 7 and 8 only, so it RETRIES a 5 rather than
+#      recording an answer (Grok 4.7, pass 2) -- a different model having answered is not an answer from this seat.
 #
 #  Overrides, each only so the branches are testable without the network: CX_MODEL, CX_EFFORT, CX_AUP_MODEL (set it
 #  EMPTY to disable the fallback), CX_AUP_EFFORT, CX_CODEX_BIN.
 #
 #  Exit status: 0 answered; 5 a different model ran; 6 empty stdout with no refusal or wall text; 7 refused (after
 #  the fallback, if any); 8 walled; 9 the brief is above the argv cap or the project dir is missing; otherwise
-#  codex's own nonzero rc.  Controls: regress/artifacts/cxlaunchland_20261016/ (RECEIPT.txt).
+#  codex's own nonzero rc.  An answered run whose model is unverified still exits 0, and says so instead of naming
+#  a model.  Controls: regress/artifacts/cxlaunchland_20261016/ (RECEIPT.txt).
 #
 #  Usage: cxlaunch.sh <brief-path> <out-dir> <tag>
 set -u
@@ -78,11 +90,13 @@
     "$CODEX" exec --sandbox read-only --skip-git-repo-check -m "$1" \
         -c model_reasoning_effort="$2" "$(cat "$BRIEF")" > "$TXT" 2> "$ERR" < /dev/null
     rc=$?
-    #  the header codex prints (in its first dozen stderr lines, before the brief and any streamed source) names the
-    #  model and effort it actually ran
-    RAN=$(strip_ansi "$ERR" | head -n 40 | grep -m1 '^model:' | sed 's/^model:[[:space:]]*//; s/[[:space:]]*$//')
+    #  codex's HEADER BLOCK -- `OpenAI Codex vX`, then the lines between the next two `--------` rules -- names the model
+    #  and effort it actually ran.  Read only that block (on record its `model:` line is line 5 of stderr in 599 of 600
+    #  codex .err files and line 7 in one, Astra); a `model:` line anywhere else is streamed source or the brief.
+    HDR=$(strip_ansi "$ERR" | awk '/^OpenAI Codex/ { h = 1; next } h == 1 && /^--------/ { h = 2; next } h == 2 && /^--------/ { exit } h == 2')
+    RAN=$(printf '%s\n' "$HDR" | grep -m1 '^model:' | sed 's/^model:[[:space:]]*//; s/[[:space:]]*$//')
     echo "codex rc=$rc   stdout=$(wc -c < "$TXT") b   stderr=$(wc -c < "$ERR") b   asked: $1 / $2"
-    echo "  ran: ${RAN:+model: $RAN} / $(strip_ansi "$ERR" | head -n 40 | grep -m1 '^reasoning effort:')"
+    echo "  ran: ${RAN:+model: $RAN} / $(printf '%s\n' "$HDR" | grep -m1 '^reasoning effort:')"
 }
 
 #  CONTENT CHECK.  Verify by content, never by size -- and NOT by grepping stderr for codex's diagnostics alone.
@@ -100,7 +114,11 @@
 #  Every real wall and refusal on record is rc 1 with an EMPTY stdout, and every rc-0 run carries an answer: 362 + 25
 #  of 387 launch lines, nothing off that diagonal (launchlog_census.txt) -- the residuals above are the off-diagonal.
 classify() {
-    CXERR=$(strip_ansi "$ERR" | grep '^ERROR:')
+    #  `grep -a`: a stderr carrying a NUL byte is "binary" to grep, which then prints `Binary file (standard input)
+    #  matches` instead of the lines.  A real wall was recorded exit 6 "seat down" that way:
+    #  _scratchpad/cxfarm3_20260919/out/codex_l1_batterypreflight.err (rc 1, empty stdout, 1,449 NULs from byte 2,318,517;
+    #  its two column-0 `ERROR: You've hit your usage limit` lines come after them) -- Grok 4.7, pass 2, re-run here.
+    CXERR=$(strip_ansi "$ERR" | grep -a '^ERROR:')
     verd=$(grep -ic 'VERDICT' "$TXT" 2>/dev/null)
     body=$(wc -c < "$TXT")
     refus=0; wall=0
@@ -138,6 +156,9 @@
     echo "  *** A DIFFERENT MODEL RAN: asked $ANSWERED_BY, codex's header says $RAN -- a SEAT FAILURE; the answer is not $ANSWERED_BY's."
     exit 5
 fi
-[ -z "$RAN" ] && echo "  note: no model: header in stderr -- the answering model is UNVERIFIED"
 if [ "$rc" -ne 0 ];  then echo "  *** codex exited $rc -- NOT a clean run."; exit "$rc"; fi
-echo "  seat answered. (answered by: $ANSWERED_BY)"
+if [ -z "$RAN" ]; then
+    echo "  seat answered -- model UNVERIFIED: no codex header block in stderr (requested: $ANSWERED_BY)"
+else
+    echo "  seat answered. (answered by: $ANSWERED_BY)"
+fi
```

### 4a. The v2 controls driver, whole (`run_controls_v2.sh`; the tracked column is the PRE-FIX file, run through a scratch $HOME)

```bash
#!/bin/bash
#  Controls for the tools/cxlaunch.sh landing of 2026-10-16 (ledger `cxlaunchquotation`, `cxlaunchdaybreak`; RULINGS_C_records.md
#  F1), v2 after the four-seat pass 2.  Every row runs a launcher against a FAKE codex that replays a fixture -- nothing here
#  calls the network -- on THREE launchers, and compares each exit status with the expected one:
#
#    tracked  cxlaunch_tracked.sh  = `git show HEAD:tools/cxlaunch.sh` before the landing (md5 cb180d9d...), the file the
#             landing REPLACES -- driven through $HOME, since it names its codex binary under $HOME and has no override
#    before   cxlaunch_before.sh   = the untracked production copy the farm ran (md5 3c51a757...)
#    after    tools/cxlaunch.sh    = the landed file (or $CXL_AFTER, which the mutant table uses)
#
#  The tracked column is the PRE-FIX state (Fable 5.1's pass-2 C1, via its Opus 4.8 fallback): N1 and N2 are the
#  `cxlaunchquotation' false wall (exit 8 there, 0 after), D1 the missing Daybreak fallback (7 there, 0 after).
#
#    P1 P2 N1-N4   the six Option-C fixtures          Q1-Q3  Fable 5.1's boundary fixtures
#    A1  an ANSI-coloured refusal                     M1  N1's real run asked as another model    M2  an answer, no stderr
#    D1  a refusal, then a Daybreak answer            D2  the same, the Daybreak header naming gpt-6-astra
#    X1  rc 1, empty stdout, ONLY a prefixed quotation of a refusal line (pins the `^ERROR:' anchor)
#    X2  rc 0, an answer with NO verdict line, column-0 wall lines on stderr (pins the empty-STDOUT half of the gate)
#    X5  N1's run asked as gpt-5-astra (pins the WHOLE model name: a suffix-only compare passes it)
#    X6  rc 0, an answer, NO codex header block but a quoted `model: gpt-6-other' line (pins header-block parsing)
#    X8  rc 1, empty, a NUL byte in stderr BEFORE the column-0 wall lines (pins `grep -a': the real 2026-09-19 wall
#        that was recorded exit 6, _scratchpad/cxfarm3_20260919/out/codex_l1_batterypreflight.err -- Grok 4.7, pass 2)
#    E0  every run of every column reached the FAKE: its argument log exists (a launcher that ignores the override would
#        run the REAL CLI -- the tracked file names its binary under $HOME, and a pass-2 seat ran it unmodified once)
#    E1/E2  the arguments the fake codex RECEIVED: -m and the effort, once for N1, twice (Astra, then Daybreak) for D1
#  NOT pinned, by Fable 5.1's ruling on pass 2 (filed in `cxlaunchunpinned'): `-ne 0' -> `-eq 1' in the classify gate is
#  observable only at rc not in {0, 1} WITH an answer -- inside the recorded N4 residual, so a pin would assert the
#  residual's wrong exit as expected; the strip narrowed to SGR (`[0-9;]*m') and wall-before-refusal precedence each need
#  a stderr shape with 0 instances on record (no non-SGR CSI or OSC in 2,372 .err files; no refusal+wall co-occurrence).
#
#  Exit 0 only if every expectation holds (v1 ended on an echo and exited 0 whatever the tally -- GPT-6 Astra, pass 2).
#  Usage: bash run_controls.sh     ($CXL_AFTER overrides the after launcher; writes only to a scratch dir it removes)
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
REPO=$(cd "$HERE/../../.." && pwd)
TRACKED="$HERE/cxlaunch_tracked.sh"
BEFORE="$HERE/cxlaunch_before.sh"
AFTER="${CXL_AFTER:-$REPO/tools/cxlaunch.sh}"
N1D="$REPO/regress/artifacts/exemptredate_20260925/final550"
QD="$REPO/regress/artifacts/adj_20261016/fable5/meas_C/cxctl_fable"
for f in "$TRACKED" "$BEFORE" "$AFTER" "$N1D/codex_astra550.txt" "$N1D/codex_astra550.err" "$QD/Q1.stderr" "$QD/Q2.stderr" \
         "$QD/Q3.stderr" "$HERE/fx/P1.stderr" "$HERE/fx/P2.stderr" "$HERE/fx/N2.stdout"; do
    [ -s "$f" ] || { echo "APPARATUS FAIL: missing $f"; exit 9; }
done
T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT
ESC=$(printf '\033')

mkfx() {    # $1 name, $2 rc, $3 stdout source or "", $4 stderr source or "" (or "-" to read stderr from stdin)
    mkdir -p "$T/fx/$1"; echo "$2" > "$T/fx/$1/rc"
    if [ -n "$3" ]; then cp "$3" "$T/fx/$1/stdout"; else : > "$T/fx/$1/stdout"; fi
    if [ "$4" = "-" ]; then cat > "$T/fx/$1/stderr"; elif [ -n "$4" ]; then cp "$4" "$T/fx/$1/stderr"; else : > "$T/fx/$1/stderr"; fi
}
printf 'A complete review answer.\nVERDICT: SHIP\n' > "$T/ans_verdict.txt"
#  NOT the word "verdict" in any case: the launcher counts it case-insensitively, and a first draft of this fixture said
#  "no verdict line" -- so it HAD one, and the kill table measured X2 blind to the mutant it exists for.
printf 'A complete review answer that ends without its summary line.\n' > "$T/ans_noverdict.txt"
mkfx P1 1 "" "$HERE/fx/P1.stderr"
mkfx P2 1 "" "$HERE/fx/P2.stderr"
mkfx N1 0 "$N1D/codex_astra550.txt" "$N1D/codex_astra550.err"
mkfx N2 0 "$HERE/fx/N2.stdout" ""
mkfx N3 0 "" ""
mkfx N4 1 "$N1D/codex_astra550.txt" "$N1D/codex_astra550.err"
mkfx Q1 1 "" "$QD/Q1.stderr"
mkfx Q2 0 "" "$QD/Q2.stderr"
mkfx Q3 1 "" "$QD/Q3.stderr"
sed "s/^ERROR:/${ESC}[1m${ESC}[31mERROR:${ESC}[0m${ESC}[0m/" "$HERE/fx/P2.stderr" | mkfx A1 1 "" -
printf 'OpenAI Codex v0.153.4\n--------\nmodel: gpt-daybreak-blue-latest\nreasoning effort: ultra\n--------\n' | mkfx DB_OK 0 "$HERE/fx/N2.stdout" -
printf 'OpenAI Codex v0.153.4\n--------\nmodel: gpt-6-astra\nreasoning effort: ultra\n--------\n' | mkfx DB_WRONG 0 "$HERE/fx/N2.stdout" -
sed 's/^/regress\/artifacts\/old_panel\/codex.txt:17:/' "$HERE/fx/P2.stderr" | mkfx X1 1 "" -
mkfx X2 0 "$T/ans_noverdict.txt" "$HERE/fx/P1.stderr"
printf 'streamed source, quoted while the review read a file:\nmodel: gpt-6-other\nreasoning effort: low\n' | mkfx X6 0 "$T/ans_verdict.txt" -
{ printf 'streamed binary from a file the review read: \000\001\002 end\n'; cat "$HERE/fx/P1.stderr"; } | mkfx X8 1 "" -

#  the fake codex: replays $FX (or $FX2 when the requested -m equals $FX2_MODEL) and logs its arguments to $FX_ARGS
cat > "$T/fakecodex.sh" <<'EOF'
#!/bin/bash
D="$FX"; prev=""
for a in "$@"; do
    if [ "$prev" = "-m" ] && [ -n "${FX2_MODEL:-}" ] && [ "$a" = "$FX2_MODEL" ]; then D="$FX2"; fi
    prev="$a"
done
[ -n "${FX_ARGS:-}" ] && printf '%s\n' "${*:1:8}" >> "$FX_ARGS"
cat "$D/stdout"; cat "$D/stderr" 1>&2; exit "$(cat "$D/rc")"
EOF
chmod +x "$T/fakecodex.sh"
#  the tracked launcher names $HOME/AppData/Local/Programs/OpenAI/Codex/bin/codex and reads no override, so give it a HOME
mkdir -p "$T/home/AppData/Local/Programs/OpenAI/Codex/bin"
cp "$T/fakecodex.sh" "$T/home/AppData/Local/Programs/OpenAI/Codex/bin/codex"
chmod +x "$T/home/AppData/Local/Programs/OpenAI/Codex/bin/codex"
printf 'control brief\n' > "$T/brief.md"

pass=0; total=0
run() {    # $1 row, $2 launcher label, $3 launcher, $4 expected exit, then env assignments
    local row="$1" lab="$2" sh="$3" want="$4"; shift 4
    local out="$T/out_${row}_${lab}"
    ( export CX_CODEX_BIN="$T/fakecodex.sh" FX2= FX2_MODEL= FX_ARGS="$T/args_${row}_${lab}"
      [ "$lab" = tracked ] && export HOME="$T/home"
      for kv in "$@"; do export "$kv"; done
      bash "$sh" "$T/brief.md" "$out" "$row" ) > "$T/log_${row}_${lab}.txt" 2>&1
    local got=$?
    total=$((total + 1))
    local ok="NO"; [ "$got" = "$want" ] && { ok="ok"; pass=$((pass + 1)); }
    printf '%-3s %-7s exit=%-2s want=%-2s %s\n' "$row" "$lab" "$got" "$want" "$ok"
    sed 's/^/      /' "$T/log_${row}_${lab}.txt" | grep -v '^      brief bytes' | cut -c1-170
}
three() {    # $1 row, $2 want-tracked, $3 want-before, $4 want-after, then env
    local row="$1" wt="$2" wb="$3" wa="$4"; shift 4
    run "$row" tracked "$TRACKED" "$wt" "$@"
    run "$row" before "$BEFORE" "$wb" "$@"
    run "$row" after "$AFTER" "$wa" "$@"
}
check() {    # $1 label, $2 0/1 result
    total=$((total + 1))
    if [ "$2" = 0 ]; then pass=$((pass + 1)); echo "$1  ok"; else echo "$1  NO"; fi
}

echo "# cxlaunch landing controls (v2), $(date '+%Y-%m-%d %H:%M:%S')"
echo "# tracked: $(md5sum < "$TRACKED" | cut -c1-32)  cxlaunch_tracked.sh"
echo "# before:  $(md5sum < "$BEFORE" | cut -c1-32)  cxlaunch_before.sh"
echo "# after:   $(md5sum < "$AFTER" | cut -c1-32)  $AFTER"
three P1 8 8 8 FX="$T/fx/P1" CX_AUP_MODEL=
three P2 7 7 7 FX="$T/fx/P2" CX_AUP_MODEL=
three N1 8 0 0 FX="$T/fx/N1" CX_AUP_MODEL=
three N2 8 0 0 FX="$T/fx/N2" CX_AUP_MODEL=
three N3 6 6 6 FX="$T/fx/N3" CX_AUP_MODEL=
three N4 8 8 8 FX="$T/fx/N4" CX_AUP_MODEL=
three Q1 7 7 7 FX="$T/fx/Q1" CX_AUP_MODEL=
three Q2 8 8 8 FX="$T/fx/Q2" CX_AUP_MODEL=
three Q3 6 6 8 FX="$T/fx/Q3" CX_AUP_MODEL=
three A1 6 6 7 FX="$T/fx/A1" CX_AUP_MODEL=
three M1 8 0 5 FX="$T/fx/N1" CX_AUP_MODEL= CX_MODEL=gpt-6-other
three M2 8 0 0 FX="$T/fx/N2" CX_AUP_MODEL=
three D1 7 0 0 FX="$T/fx/P2" FX2="$T/fx/DB_OK" FX2_MODEL=gpt-daybreak-blue-latest
three D2 7 0 5 FX="$T/fx/P2" FX2="$T/fx/DB_WRONG" FX2_MODEL=gpt-daybreak-blue-latest
three X1 6 6 6 FX="$T/fx/X1" CX_AUP_MODEL=
three X2 8 0 0 FX="$T/fx/X2" CX_AUP_MODEL=
three X5 8 0 5 FX="$T/fx/N1" CX_AUP_MODEL= CX_MODEL=gpt-5-astra
three X6 0 0 0 FX="$T/fx/X6" CX_AUP_MODEL=
three X8 6 6 8 FX="$T/fx/X8" CX_AUP_MODEL=
#  E0: the fake ran for every row of every column; the run count is pinned, so a deleted row is visible
nruns=$(ls "$T"/log_* 2>/dev/null | wc -l); nargs=$(ls "$T"/args_* 2>/dev/null | wc -l)
miss=""; for f in "$T"/log_*; do b=${f##*/log_}; b=${b%.txt}; [ -s "$T/args_$b" ] || miss="$miss $b"; done
[ "$nruns" = 57 ] && [ "$nargs" = "$nruns" ]; check "E0  all  the fake codex logged $nargs of $nruns runs (19 rows x 3, pinned)${miss:+ -- NOT reached:$miss}" $?
#  content, not exit status -- on the AFTER logs
grep -q 'model UNVERIFIED' "$T/log_M2_after.txt" && ! grep -q 'answered by:' "$T/log_M2_after.txt"; check "M2  after  says model UNVERIFIED and names no model" $?
grep -q 'model UNVERIFIED' "$T/log_X6_after.txt" && ! grep -q 'answered by:' "$T/log_X6_after.txt"; check "X6  after  a quoted model: line is NOT read as the header" $?
[ -s "$T/out_D1_after/codex_D1.refused.err" ] && grep -q 'answered by: gpt-daybreak-blue-latest' "$T/log_D1_after.txt"; check "D1  after  refused run kept, Daybreak credited" $?
[ "$(wc -l < "$T/args_N1_after")" = 1 ] && grep -q -- '-m gpt-6-astra -c model_reasoning_effort=ultra' "$T/args_N1_after"; check "E1  after  N1: one call, -m gpt-6-astra, effort ultra" $?
[ "$(wc -l < "$T/args_D1_after")" = 2 ] && sed -n 1p "$T/args_D1_after" | grep -q -- '-m gpt-6-astra -c model_reasoning_effort=ultra' \
    && sed -n 2p "$T/args_D1_after" | grep -q -- '-m gpt-daybreak-blue-latest -c model_reasoning_effort=ultra'; check "E2  after  D1: two calls, Astra then Daybreak, effort ultra each" $?
echo "CONTROLS: $pass/$total as expected"
echo "CXLAND_CONTROLS_DONE"
[ "$pass" = "$total" ]
```

### 4b. RECEIPT_v2.txt -- every exit line and every content check (the launchers' own log lines are in the file)

```
# cxlaunch landing controls (v2), 2026-10-16 22:31:51
# tracked: cb180d9d58da2c0b05defe48c65b7ad0  cxlaunch_tracked.sh
# before:  3c51a7579065c5e6bebd5fd59d32b3ed  cxlaunch_before.sh
# after:   2e6119057940e6f11f13c0b3c23607b7  /c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/tools/cxlaunch.sh
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
E0  all  the fake codex logged 57 of 57 runs (19 rows x 3, pinned)  ok
M2  after  says model UNVERIFIED and names no model  ok
X6  after  a quoted model: line is NOT read as the header  ok
D1  after  refused run kept, Daybreak credited  ok
E1  after  N1: one call, -m gpt-6-astra, effort ultra  ok
E2  after  D1: two calls, Astra then Daybreak, effort ultra each  ok
CONTROLS: 63/63 as expected
CXLAND_CONTROLS_DONE
```

### 4c. KILLTABLE.txt -- `run_mutants.sh` over `mut_launcher.py`'s one-edit mutants of v2

```
mutants written: 14 of 14
# kill table for /c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/tools/cxlaunch.sh (2e6119057940e6f11f13c0b3c23607b7), 2026-10-16 22:32:27
BASE      CONTROLS: 63/63 as expected
m_anchor      62/63    killed by: X1                                                  [X1]
m_bodyverd    62/63    killed by: X2                                                  [X2]
m_suffix      62/63    killed by: X5                                                  [X5]
m_effort      61/63    killed by: E1 E2                                               [E1 E2]
m_head40      61/63    killed by: X6                                                  [X6]
m_noa         62/63    killed by: X8                                                  [X8]
m_nostrip     61/63    killed by: A1 Q3                                               [Q3 A1]
m_noident     60/63    killed by: D2 M1 X5                                            [M1 D2 X5]
m_nofallback  59/63    killed by: D1 D2 E2                                            [D1 D2 E2]
m_nogate      59/63    killed by: M1 N1 X2 X5                                         [N1 X2]
m_claimmodel  61/63    killed by: M2 X6                                               [M2 X6]
m_eq1         63/63    escapes (as recorded)                                          [UNPINNED (only rc not in {0,1} WITH an answer -- the N4 residual)]
m_sgr         63/63    escapes (as recorded)                                          [UNPINNED (non-SGR CSI: 0 of 2,372 .err files on record)]
m_prec        63/63    escapes (as recorded)                                          [UNPINNED (a refusal and a wall in one stderr: 0 on record)]
KILL TABLE: 14/14 as recorded
CXLAND_MUTANTS_DONE
```

## 5. Questions -- verdict line first, then answer each by number; say plainly what you could not check

1. **Your own findings.**  For each finding of yours in section 2: is my disposition right, and is the FIX right?  A fix can
   answer the finding and still be wrong -- check the header-block awk (F1), the `grep -a` (F15), the tracked-column `$HOME`
   route (F9), and the fake's argument log (F4) against the inlined diff and driver.
2. **The repair as material.**  The repair itself owes a pass: read section 4's diff (v1 -> v2) and the v2 controls.  Is
   there a path where the v2 launcher now misclassifies something v1 classified right -- for example, a real codex header
   block the awk misses (a version line not starting `OpenAI Codex`, a rule of a different length), or a stderr where the
   strip plus `grep -a` creates a column-0 `ERROR:` on an rc-0 answer (it should be ignored there -- check)?
3. **The kill table.**  Every PINNED mutant is killed by the control its line names, and the three UNPINNED ones escape as
   recorded.  Is any pinned control killing its mutant for a reason OTHER than the one named?  Is there a one-edit mutant
   of the v2 launcher, NOT in the table, that passes all 63 controls and breaks a ruled property?
4. **Records.**  The closures (`cxlaunchquotation`, `cxlaunchdaybreak`) with witness `RECEIPT_v2.txt` and their HELD regress
   reviews; the in-place corrections (F10, F19); the filing `cxlaunchunpinned` (F13, F14).  Anything wrong?
5. **Which of my accepted dispositions is wrong?**  Name the count you checked (there are 19 findings above).
