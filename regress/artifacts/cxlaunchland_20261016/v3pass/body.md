
## 3. The repair, v2 -> v3

### 3a. tools/cxlaunch.sh (`cxlaunch_landed_v2.sh` -> the working tree; 24 changed lines)

```diff
--- /c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/cxlaunchland_20261016/cxlaunch_landed_v2.sh	2026-10-16 23:36:29.485179100 -0500
+++ /c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/tools/cxlaunch.sh	2026-10-16 23:36:29.511982700 -0500
@@ -47,9 +47,9 @@
 #      `ERROR:` line does not fix it: in N4 that line is itself a quotation.
 #    * its refusal twin: a quoted `flagged for possible cybersecurity` line on rc != 0 -> the Daybreak re-run fires
 #      and the first answer is renamed codex_<tag>.refused.* (Grok 4.7).
-#    * a run whose stderr carries NO codex header block is reported "model UNVERIFIED" and is not failed -- 0 of 330
-#      launcher-captured answered runs on record lack it (counted on pass 2); failing it would lose every answer to a
-#      CLI format change.
+#    * a run whose stderr carries NO opening codex header block is reported "model UNVERIFIED" and is not failed -- 0 of
+#      330 launcher-captured answered runs on record lack it (counted on pass 2); failing it would lose every answer to a
+#      CLI format change.  A block whose closing rule never comes is read for 30 lines at most.
 #    * the ANSI strip widens both residuals above to colour-prefixed quoted lines on a failed or empty run (GLM 5.3,
 #      pass 2): a quoted line whose only prefix was colour becomes column-0 -- still inside the classify-on-failure gate.
 #    * a REFUSED first run's header is printed (`ran:`) but not compared; its answer is discarded, and the fallback's
@@ -63,7 +63,8 @@
 #  Exit status: 0 answered; 5 a different model ran; 6 empty stdout with no refusal or wall text; 7 refused (after
 #  the fallback, if any); 8 walled; 9 the brief is above the argv cap or the project dir is missing; otherwise
 #  codex's own nonzero rc.  An answered run whose model is unverified still exits 0, and says so instead of naming
-#  a model.  Controls: regress/artifacts/cxlaunchland_20261016/ (RECEIPT.txt).
+#  a model.  Controls: regress/artifacts/cxlaunchland_20261016/run_controls_v3.sh (RECEIPT_v3.txt; the kill table is
+#  KILLTABLE_v3.txt -- RECEIPT.txt and RECEIPT_v2.txt are the pass-2 and adjudication-pass receipts of earlier versions).
 #
 #  Usage: cxlaunch.sh <brief-path> <out-dir> <tag>
 set -u
@@ -90,10 +91,17 @@
     "$CODEX" exec --sandbox read-only --skip-git-repo-check -m "$1" \
         -c model_reasoning_effort="$2" "$(cat "$BRIEF")" > "$TXT" 2> "$ERR" < /dev/null
     rc=$?
-    #  codex's HEADER BLOCK -- `OpenAI Codex vX`, then the lines between the next two `--------` rules -- names the model
-    #  and effort it actually ran.  Read only that block (on record its `model:` line is line 5 of stderr in 599 of 600
-    #  codex .err files and line 7 in one, Astra); a `model:` line anywhere else is streamed source or the brief.
-    HDR=$(strip_ansi "$ERR" | awk '/^OpenAI Codex/ { h = 1; next } h == 1 && /^--------/ { h = 2; next } h == 2 && /^--------/ { exit } h == 2')
+    #  codex's OPENING header block -- `OpenAI Codex vX`, then the lines between the next two `--------` rules -- names the
+    #  model and effort it actually ran.  Read only that block, and only at the TOP of stderr: the banner and its first
+    #  rule must appear by line 12 and the block is read for at most 30 lines.  On record the block's `model:` line is
+    #  line 5 of stderr in 599 of 600 codex .err files and line 7 in one (two pre-header lines; Astra).  A `model:` line
+    #  anywhere else is streamed source or the brief and is never READ -- including a complete QUOTED header block, which
+    #  N1's own stderr carries at line 5528 (GPT-6 Astra, adjudication pass: v2 matched the banner anywhere).
+    HDR=$(strip_ansi "$ERR" | awk 'NR > 12 && h < 2 { exit }
+        h == 0 && /^OpenAI Codex/ { h = 1; next }
+        h == 1 && /^--------/ { h = 2; next }
+        h == 2 && /^--------/ { exit }
+        h == 2 { if (++n > 30) exit; print }')
     RAN=$(printf '%s\n' "$HDR" | grep -m1 '^model:' | sed 's/^model:[[:space:]]*//; s/[[:space:]]*$//')
     echo "codex rc=$rc   stdout=$(wc -c < "$TXT") b   stderr=$(wc -c < "$ERR") b   asked: $1 / $2"
     echo "  ran: ${RAN:+model: $RAN} / $(printf '%s\n' "$HDR" | grep -m1 '^reasoning effort:')"
```

### 3b. the controls (`run_controls_v2.sh` -> `run_controls_v3.sh`)

```diff
--- /c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/cxlaunchland_20261016/run_controls_v2.sh
+++ /c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/cxlaunchland_20261016/run_controls_v3.sh
@@ -1,7 +1,7 @@
 #!/bin/bash
 #  Controls for the tools/cxlaunch.sh landing of 2026-10-16 (ledger `cxlaunchquotation`, `cxlaunchdaybreak`; RULINGS_C_records.md
-#  F1), v2 after the four-seat pass 2.  Every row runs a launcher against a FAKE codex that replays a fixture -- nothing here
-#  calls the network -- on THREE launchers, and compares each exit status with the expected one:
+#  F1), v3 after the four-seat pass 2 and the adjudication pass.  Every row runs a launcher against a FAKE codex that replays a
+#  fixture -- nothing here calls the network -- on THREE launchers, and compares each exit status with the expected one:
 #
 #    tracked  cxlaunch_tracked.sh  = `git show HEAD:tools/cxlaunch.sh` before the landing (md5 cb180d9d...), the file the
 #             landing REPLACES -- driven through $HOME, since it names its codex binary under $HOME and has no override
@@ -20,16 +20,22 @@
 #    X6  rc 0, an answer, NO codex header block but a quoted `model: gpt-6-other' line (pins header-block parsing)
 #    X8  rc 1, empty, a NUL byte in stderr BEFORE the column-0 wall lines (pins `grep -a': the real 2026-09-19 wall
 #        that was recorded exit 6, _scratchpad/cxfarm3_20260919/out/codex_l1_batterypreflight.err -- Grok 4.7, pass 2)
+#    X9  rc 0, an answer, NO opening header but a complete QUOTED header block naming gpt-6-astra after line 12 -- it must
+#        NOT verify (v2 matched the banner anywhere: N1's own stderr quotes four such blocks, from line 5528; GPT-6 Astra)
+#    X10 the same, the quoted block naming gpt-6-other -- it must NOT exit 5
 #    E0  every run of every column reached the FAKE: its argument log exists (a launcher that ignores the override would
 #        run the REAL CLI -- the tracked file names its binary under $HOME, and a pass-2 seat ran it unmodified once)
-#    E1/E2  the arguments the fake codex RECEIVED: -m and the effort, once for N1, twice (Astra, then Daybreak) for D1
+#    E1/E2  the EXACT arguments the fake codex received, one per line: exec, --sandbox read-only, --skip-git-repo-check,
+#        -m <model>, -c model_reasoning_effort=ultra and the brief -- once for N1, twice (Astra, then Daybreak) for D1
+#        (v2 matched a substring, so `ultrax' passed, and it never read the sandbox flag or the brief; Astra, GLM 5.3)
 #  NOT pinned, by Fable 5.1's ruling on pass 2 (filed in `cxlaunchunpinned'): `-ne 0' -> `-eq 1' in the classify gate is
-#  observable only at rc not in {0, 1} WITH an answer -- inside the recorded N4 residual, so a pin would assert the
-#  residual's wrong exit as expected; the strip narrowed to SGR (`[0-9;]*m') and wall-before-refusal precedence each need
-#  a stderr shape with 0 instances on record (no non-SGR CSI or OSC in 2,372 .err files; no refusal+wall co-occurrence).
+#  observable only at an rc outside {0, 1} WITH an answer -- a sibling of the N4 residual (N4 itself is rc 1, where the two
+#  forms agree; GLM 5.3), with 0 instances on record; the strip narrowed to SGR (`[0-9;]*m') and wall-before-refusal
+#  precedence each need a stderr shape with 0 instances on record (no non-SGR CSI or OSC in 2,372 .err files; no
+#  refusal+wall co-occurrence).
 #
 #  Exit 0 only if every expectation holds (v1 ended on an echo and exited 0 whatever the tally -- GPT-6 Astra, pass 2).
-#  Usage: bash run_controls.sh     ($CXL_AFTER overrides the after launcher; writes only to a scratch dir it removes)
+#  Usage: bash run_controls_v3.sh     ($CXL_AFTER overrides the after launcher; writes only to a scratch dir it removes)
 set -u
 HERE=$(cd "$(dirname "$0")" && pwd)
 REPO=$(cd "$HERE/../../.." && pwd)
@@ -71,6 +77,15 @@
 mkfx X2 0 "$T/ans_noverdict.txt" "$HERE/fx/P1.stderr"
 printf 'streamed source, quoted while the review read a file:\nmodel: gpt-6-other\nreasoning effort: low\n' | mkfx X6 0 "$T/ans_verdict.txt" -
 { printf 'streamed binary from a file the review read: \000\001\002 end\n'; cat "$HERE/fx/P1.stderr"; } | mkfx X8 1 "" -
+#  X9/X10: twenty lines of streamed text, then a complete codex header block QUOTED from a file the review read (the shape
+#  N1's stderr carries from line 5528) -- and no opening header at all
+latehdr() {    # $1 the quoted block's model
+    i=1; while [ $i -le 20 ]; do printf 'streamed line %d of a file the review read\n' $i; i=$((i + 1)); done
+    printf 'OpenAI Codex v0.153.4\n--------\nworkdir: C:\\DocumentNoSnc\\CC\\GXEMUL\nmodel: %s\nprovider: openai\n' "$1"
+    printf 'reasoning effort: ultra\n--------\nuser\nthe quoted session brief\n'
+}
+latehdr gpt-6-astra | mkfx X9 0 "$T/ans_verdict.txt" -
+latehdr gpt-6-other | mkfx X10 0 "$T/ans_verdict.txt" -
 
 #  the fake codex: replays $FX (or $FX2 when the requested -m equals $FX2_MODEL) and logs its arguments to $FX_ARGS
 cat > "$T/fakecodex.sh" <<'EOF'
@@ -80,7 +95,7 @@
     if [ "$prev" = "-m" ] && [ -n "${FX2_MODEL:-}" ] && [ "$a" = "$FX2_MODEL" ]; then D="$FX2"; fi
     prev="$a"
 done
-[ -n "${FX_ARGS:-}" ] && printf '%s\n' "${*:1:8}" >> "$FX_ARGS"
+[ -n "${FX_ARGS:-}" ] && { printf 'CALL\n'; for a in "$@"; do printf 'ARG %s\n' "$a"; done; } >> "$FX_ARGS"
 cat "$D/stdout"; cat "$D/stderr" 1>&2; exit "$(cat "$D/rc")"
 EOF
 chmod +x "$T/fakecodex.sh"
@@ -115,7 +130,7 @@
     if [ "$2" = 0 ]; then pass=$((pass + 1)); echo "$1  ok"; else echo "$1  NO"; fi
 }
 
-echo "# cxlaunch landing controls (v2), $(date '+%Y-%m-%d %H:%M:%S')"
+echo "# cxlaunch landing controls (v3), $(date '+%Y-%m-%d %H:%M:%S')"
 echo "# tracked: $(md5sum < "$TRACKED" | cut -c1-32)  cxlaunch_tracked.sh"
 echo "# before:  $(md5sum < "$BEFORE" | cut -c1-32)  cxlaunch_before.sh"
 echo "# after:   $(md5sum < "$AFTER" | cut -c1-32)  $AFTER"
@@ -138,17 +153,26 @@
 three X5 8 0 5 FX="$T/fx/N1" CX_AUP_MODEL= CX_MODEL=gpt-5-astra
 three X6 0 0 0 FX="$T/fx/X6" CX_AUP_MODEL=
 three X8 6 6 8 FX="$T/fx/X8" CX_AUP_MODEL=
+three X9 0 0 0 FX="$T/fx/X9" CX_AUP_MODEL=
+three X10 0 0 0 FX="$T/fx/X10" CX_AUP_MODEL=
 #  E0: the fake ran for every row of every column; the run count is pinned, so a deleted row is visible
 nruns=$(ls "$T"/log_* 2>/dev/null | wc -l); nargs=$(ls "$T"/args_* 2>/dev/null | wc -l)
 miss=""; for f in "$T"/log_*; do b=${f##*/log_}; b=${b%.txt}; [ -s "$T/args_$b" ] || miss="$miss $b"; done
-[ "$nruns" = 57 ] && [ "$nargs" = "$nruns" ]; check "E0  all  the fake codex logged $nargs of $nruns runs (19 rows x 3, pinned)${miss:+ -- NOT reached:$miss}" $?
+[ "$nruns" = 63 ] && [ "$nargs" = "$nruns" ]; check "E0  all  the fake codex logged $nargs of $nruns runs (21 rows x 3, pinned)${miss:+ -- NOT reached:$miss}" $?
 #  content, not exit status -- on the AFTER logs
 grep -q 'model UNVERIFIED' "$T/log_M2_after.txt" && ! grep -q 'answered by:' "$T/log_M2_after.txt"; check "M2  after  says model UNVERIFIED and names no model" $?
 grep -q 'model UNVERIFIED' "$T/log_X6_after.txt" && ! grep -q 'answered by:' "$T/log_X6_after.txt"; check "X6  after  a quoted model: line is NOT read as the header" $?
 [ -s "$T/out_D1_after/codex_D1.refused.err" ] && grep -q 'answered by: gpt-daybreak-blue-latest' "$T/log_D1_after.txt"; check "D1  after  refused run kept, Daybreak credited" $?
-[ "$(wc -l < "$T/args_N1_after")" = 1 ] && grep -q -- '-m gpt-6-astra -c model_reasoning_effort=ultra' "$T/args_N1_after"; check "E1  after  N1: one call, -m gpt-6-astra, effort ultra" $?
-[ "$(wc -l < "$T/args_D1_after")" = 2 ] && sed -n 1p "$T/args_D1_after" | grep -q -- '-m gpt-6-astra -c model_reasoning_effort=ultra' \
-    && sed -n 2p "$T/args_D1_after" | grep -q -- '-m gpt-daybreak-blue-latest -c model_reasoning_effort=ultra'; check "E2  after  D1: two calls, Astra then Daybreak, effort ultra each" $?
+grep -q 'model UNVERIFIED' "$T/log_X9_after.txt" && ! grep -q 'answered by:' "$T/log_X9_after.txt"; check "X9  after  a late QUOTED header block is NOT read as the header" $?
+#  E1/E2: the exact argument sequence of each call, one argument per line, compared whole
+callseq() {    # $1 model -- the sequence one call must receive
+    printf 'CALL\nARG exec\nARG --sandbox\nARG read-only\nARG --skip-git-repo-check\nARG -m\nARG %s\nARG -c\n' "$1"
+    printf 'ARG model_reasoning_effort=ultra\nARG control brief\n'
+}
+callseq gpt-6-astra > "$T/want_E1"
+{ callseq gpt-6-astra; callseq gpt-daybreak-blue-latest; } > "$T/want_E2"
+cmp -s "$T/want_E1" "$T/args_N1_after"; check "E1  after  N1: exactly one call, exactly exec --sandbox read-only ... -m gpt-6-astra, effort ultra, the brief" $?
+cmp -s "$T/want_E2" "$T/args_D1_after"; check "E2  after  D1: exactly two calls, Astra then Daybreak, the same exact arguments each" $?
 echo "CONTROLS: $pass/$total as expected"
 echo "CXLAND_CONTROLS_DONE"
 [ "$pass" = "$total" ]
```

### 3c. the mutant generator, whole (`mut_launcher_v3.py`)

```python
#!/usr/bin/env python3
"""mut_launcher_v3.py <launcher.sh> <out dir> -- write one-edit mutants of tools/cxlaunch.sh (2026-10-16 landing, v3) for the
controls' kill table (run_mutants.sh).  Each mutant names the control expected to catch it, or UNPINNED with the reason it
is deliberately not pinned (Fable 5.1, pass 2: inside the recorded N4 residual, or a shape with 0 instances on record).
A find-text that is absent is an apparatus failure, never a silent skip."""
import io, os, sys

src, out = sys.argv[1], sys.argv[2]
t = io.open(src, encoding="utf-8", newline="").read()
#  the v3 launcher's opening-header awk, read from the launcher itself so the find-text cannot drift
V3AWK = 'HDR=$(strip_ansi "$ERR" | awk \'NR > 12 && h < 2 { exit }\n        h == 0 && /^OpenAI Codex/ { h = 1; next }\n        h == 1 && /^--------/ { h = 2; next }\n        h == 2 && /^--------/ { exit }\n        h == 2 { if (++n > 30) exit; print }\')'
MUTANTS = [
    ("m_anchor", "X1", "grep -a '^ERROR:'", "grep -a 'ERROR:'"),
    ("m_bodyverd", "X2", 'if [ "$rc" -ne 0 ] || [ "$body" -eq 0 ]; then', 'if [ "$rc" -ne 0 ] || [ "$verd" -eq 0 ]; then'),
    ("m_suffix", "X5", '[ "$RAN" != "$ANSWERED_BY" ]', '[ "${RAN##*-}" != "${ANSWERED_BY##*-}" ]'),
    ("m_effort", "E1 E2", '-c model_reasoning_effort="$2"', '-c model_reasoning_effort="$1"'),
    ("m_head40", "X6", V3AWK, 'HDR=$(strip_ansi "$ERR" | head -n 40)'),
    ("m_v2awk", "X9 X10", V3AWK,
     """HDR=$(strip_ansi "$ERR" | awk '/^OpenAI Codex/ { h = 1; next } h == 1 && /^--------/ { h = 2; next } h == 2 && /^--------/ { exit } h == 2')"""),
    ("m_effortx", "E1 E2", '-c model_reasoning_effort="$2"', '-c model_reasoning_effort="$2x"'),
    ("m_sandbox", "E1 E2", "--sandbox read-only", "--sandbox workspace-write"),
    ("m_brief", "E1 E2", '"$(cat "$BRIEF")"', '"$BRIEF"'),
    ("m_noa", "X8", "grep -a '^ERROR:'", "grep '^ERROR:'"),
    ("m_nostrip", "Q3 A1", 'strip_ansi() { sed "s/${ESC}\\[[0-9;]*[A-Za-z]//g" "$1" 2>/dev/null; }', 'strip_ansi() { cat "$1" 2>/dev/null; }'),
    ("m_noident", "M1 D2 X5", 'if [ -n "$RAN" ] && [ "$RAN" != "$ANSWERED_BY" ]; then', "if false; then"),
    ("m_nofallback", "D1 D2 E2", 'AUP_MODEL="${CX_AUP_MODEL-gpt-daybreak-blue-latest}"', 'AUP_MODEL=""'),
    ("m_nogate", "N1 X2", 'if [ "$rc" -ne 0 ] || [ "$body" -eq 0 ]; then', "if true; then"),
    ("m_claimmodel", "M2 X6", 'echo "  seat answered -- model UNVERIFIED: no codex header block in stderr (requested: $ANSWERED_BY)"',
     'echo "  seat answered. (answered by: $ANSWERED_BY)"'),
    ("m_eq1", "UNPINNED (only an rc outside {0,1} WITH an answer -- a sibling of N4, 0 on record)",
     'if [ "$rc" -ne 0 ] || [ "$body" -eq 0 ]; then', 'if [ "$rc" -eq 1 ] || [ "$body" -eq 0 ]; then'),
    ("m_sgr", "UNPINNED (non-SGR CSI: 0 of 2,372 .err files on record)",
     'strip_ansi() { sed "s/${ESC}\\[[0-9;]*[A-Za-z]//g" "$1" 2>/dev/null; }', 'strip_ansi() { sed "s/${ESC}\\[[0-9;]*m//g" "$1" 2>/dev/null; }'),
    ("m_prec", "UNPINNED (a refusal and a wall in one stderr: 0 on record)",
     r"""        wall=$(printf '%s' "$CXERR" | grep -ic 'usage limit\|quota\|rate limit\|not authenticated')""",
     r"""        wall=$(printf '%s' "$CXERR" | grep -ic 'usage limit\|quota\|rate limit\|not authenticated'); [ "$wall" -gt 0 ] && refus=0"""),
]
os.makedirs(out, exist_ok=True)
bad = 0
with io.open(os.path.join(out, "MUTANTS.list"), "w", encoding="utf-8", newline="\n") as lst:
    for name, catches, find, repl in MUTANTS:
        n = t.count(find)
        if n != 1:
            print("MUTANT_TEXT_NOT_FOUND %s (found %d)" % (name, n)); bad += 1; continue
        io.open(os.path.join(out, name + ".sh"), "w", encoding="utf-8", newline="").write(t.replace(find, repl))
        lst.write("%s\t%s\n" % (name, catches))
print("mutants written: %d of %d" % (len(MUTANTS) - bad, len(MUTANTS)))
sys.exit(1 if bad else 0)
```

## 4. The receipts

### 4a. `RECEIPT_v3.txt` -- its result lines (the indented per-run launcher output is omitted here; it is in the file)

```
# cxlaunch landing controls (v3), 2026-10-16 23:51:04
# tracked: cb180d9d58da2c0b05defe48c65b7ad0  cxlaunch_tracked.sh
# before:  3c51a7579065c5e6bebd5fd59d32b3ed  cxlaunch_before.sh
# after:   5314dc5cfcd443bd7f38e5f573977353  /c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/tools/cxlaunch.sh
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
E0  all  the fake codex logged 63 of 63 runs (21 rows x 3, pinned)  ok
M2  after  says model UNVERIFIED and names no model  ok
X6  after  a quoted model: line is NOT read as the header  ok
D1  after  refused run kept, Daybreak credited  ok
X9  after  a late QUOTED header block is NOT read as the header  ok
E1  after  N1: exactly one call, exactly exec --sandbox read-only ... -m gpt-6-astra, effort ultra, the brief  ok
E2  after  D1: exactly two calls, Astra then Daybreak, the same exact arguments each  ok
CONTROLS: 70/70 as expected
CXLAND_CONTROLS_DONE
```

### 4b. `KILLTABLE_v3.txt`, whole

```
mutants written: 18 of 18
# kill table for /c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/tools/cxlaunch.sh (5314dc5cfcd443bd7f38e5f573977353), 2026-10-16 23:51:48
BASE      CONTROLS: 70/70 as expected
m_anchor      69/70    killed by: X1                                                  [X1]
m_bodyverd    69/70    killed by: X2                                                  [X2]
m_suffix      69/70    killed by: X5                                                  [X5]
m_effort      68/70    killed by: E1 E2                                               [E1 E2]
m_head40      66/70    killed by: X10 X6 X9                                           [X6]
m_v2awk       68/70    killed by: X10 X9                                              [X9 X10]
m_effortx     68/70    killed by: E1 E2                                               [E1 E2]
m_sandbox     68/70    killed by: E1 E2                                               [E1 E2]
m_brief       68/70    killed by: E1 E2                                               [E1 E2]
m_noa         69/70    killed by: X8                                                  [X8]
m_nostrip     68/70    killed by: A1 Q3                                               [Q3 A1]
m_noident     67/70    killed by: D2 M1 X5                                            [M1 D2 X5]
m_nofallback  66/70    killed by: D1 D2 E2                                            [D1 D2 E2]
m_nogate      66/70    killed by: M1 N1 X2 X5                                         [N1 X2]
m_claimmodel  67/70    killed by: M2 X6 X9                                            [M2 X6]
m_eq1         70/70    escapes (as recorded)                                          [UNPINNED (only an rc outside {0,1} WITH an answer -- a sibling of N4, 0 on record)]
m_sgr         70/70    escapes (as recorded)                                          [UNPINNED (non-SGR CSI: 0 of 2,372 .err files on record)]
m_prec        70/70    escapes (as recorded)                                          [UNPINNED (a refusal and a wall in one stderr: 0 on record)]
KILL TABLE: 18/18 as recorded
CXLAND_MUTANTS_DONE
```

## 5. The records this landing writes AT COMMIT (previews against HEAD)

### 5a. OUTSTANDING_BUGS.md

```diff
--- ob_head.md
+++ ob_f1_preview.md
@@ -16561,6 +16561,10 @@
 
 `tools/cxlaunch.sh` anchors stderr tests on codex's own `^ERROR:` lines and greps stdout freely;
 exit 7 refusal, 8 wall, 6 empty-with-neither, else `rc`. Controlled in four states.
+*[2026-10-16, the `cxlaunchquotation` landing: the two lines above are kept as written and are NO LONGER TRUE -- "greps
+stdout freely" was the very defect `cxlaunchquotation` was filed for.  The landed file classifies codex's `^ERROR:` lines
+(ANSI-stripped, read with `grep -a`) ONLY when rc != 0 or stdout is empty, never greps stdout for wall words, re-runs a
+refused brief once on Daybreak, and exits 5 when codex's header block names a different model.  Controls: `regress/artifacts/cxlaunchland_20261016/RECEIPT_v3.txt`.]*
 
 *`panel.sh` already had a better, POSITION-based discriminator (head/tail 400 bytes) with the
 incident that taught it recorded in its own comment. A claim here that it did not was false and is
@@ -22509,6 +22513,10 @@
 tool that reads it).  Fix shape: key the stderr test on codex's own error block at the END of the stream, and give the
 stdout patterns word boundaries; negative-control both directions (a real wall still reds; these two runs do not).
 Found while confirming `#550`.
+**MERGED 2026-10-16 into the `cxlaunchquotation` landing, with its fix shape WITHDRAWN** (the three-seat ruling,
+regress/artifacts/adj_20261016/RULINGS_C_records.md F1): keying on codex's LAST `ERROR:` line does not work -- in fixture
+N4 that line is itself a quotation -- so the landed rule keys on the exit status and an empty stdout instead.  This filing
+never had a ledger row; both of its false positives are controlled in `regress/artifacts/cxlaunchland_20261016/RECEIPT_v3.txt` (N1, N2).
 
 ## 2026-09-25 — GXEMUL [087a90]: `#551` wdcidselfcheck; what its review files
 
@@ -24674,6 +24682,9 @@
 once".  The fallback the owner ruled (2026-10-01: `gpt-daybreak-blue-latest` on an Astra AUP refusal) exists only in
 `_scratchpad/codexpack_20260928/cxlaunch_pack.run-*.sh`.  Fix: give `cxlaunch.sh` the pack runner's fallback, and
 correct the comment when `panel.sh` is next reviewed (it carries unreviewed deltas).
+**CLOSED 2026-10-16** (the landing; the heading above is kept as written -- it was true of the tracked file until then).
+The fallback is controlled by D1, D2 and E2 in `regress/artifacts/cxlaunchland_20261016/RECEIPT_v3.txt`; the real-run receipt of it firing is
+`regress/artifacts/codexpack_20260928/dossier_gdromdma/dossier_gdromdma.launch.log`.  `panel.sh`'s comment is still owed.
 
 ### 2026-10-09 -- `ppcrlwhighhalf` / `ppcwitnessmaskoracle`: the oracle repair committed alone, the rung-3 witness on committed HEAD
 
@@ -24722,6 +24733,9 @@
 * **`cxlaunchquotation` (LOW, open)** -- `tools/cxlaunch.sh`'s wall check greps the seat's answer for `quota`, so an
   answer containing "quotation" is reported SEAT WALLED (rc 8).  Measured 2026-10-09 on a complete GPT-6 Astra answer.
   Word-anchor it and test stdout only when no verdict line is present; controls both ways.
+  **CLOSED 2026-10-16 by the landing, and the fix prescribed above was REPLACED, not applied** (RULINGS_C F1): stdout is
+  never grepped for wall words; codex's `^ERROR:` lines are classified only when rc != 0 or stdout is empty.  The tracked
+  file the landing replaced exits 8 on N1 and N2 and the landed one 0 (`regress/artifacts/cxlaunchland_20261016/RECEIPT_v3.txt`).
 * **`fablequeueregress` (MEDIUM, open)** gains Fable 5.1's stagetokens finding 5: section I's regress guarantee is
   narrower than its docstring -- precommit I2 (the codex wall), not I, forces a held regress review into the queue.
 
@@ -24761,3 +24775,11 @@
   supervisor trap in a slot naming a residual vector (11..113, 116..127) or 114/115 -- is unrowed.  `&& !(cpu->delay_slot
   && is_trap)` at :799 is a PREDICTED 84/84 escape, not measured (Fable 5.1, pass 16, `pass16/fable5_m88kp16.md` section
   4).  Pin if ever rowed: `residtbdslot` = `[BR_N_PLUS16, TB1_0_R3_50]`, r3 = 1, expected HALT naming 0x032.
+
+### 2026-10-16 -- the codex launcher landed in `tools/cxlaunch.sh` (`cxlaunchquotation`, `cxlaunchdaybreak` closed); one row filed
+
+* **`cxlaunchunpinned` (LOW, open)** -- the landing's controls leave three one-edit escapes of `tools/cxlaunch.sh`
+  UNPINNED BY RULING (Fable 5.1, pass 2), each MEASURED to escape in `regress/artifacts/cxlaunchland_20261016/KILLTABLE_v3.txt`: `-ne 0` -> `-eq 1`
+  in the classify gate (observable only at an rc outside {0, 1} WITH an answer -- a sibling of the recorded N4 residual,
+  which is rc 1, where the two forms agree; 0 instances on record); the ANSI strip narrowed to SGR `[0-9;]*m` (no non-SGR CSI or OSC in 2,372 codex
+  `.err` files); wall-before-refusal precedence (no stderr on record carries both).  Pin each the day a real instance appears.
```

### 5b. the ledger rows

```
# ledger changes the tools/cxlaunch.sh landing makes, against HEAD (a preview; applied at commit)

== cxlaunchdaybreak 
  closure: {"by": "opus5-mainloop", "badge": "A", "note": "CLOSED by the same landing: a content-filter refusal on Astra is re-run once on gpt-daybreak-blue-latest, the refused run kept as .refused.*, the answer credited to Daybreak (D1, D2, E2 in RECEIPT_v3.txt; the real-run receipt is codexpack_20260928/dossier_gdromdma/dossier_gdromdma.launch.log)."}
  + entry: {"phase": "regress", "seat": "fable5", "date": "2026-10-16", "grade": "UNKNOWN", "grader": "", "ev": "not fired", "note": "[HELD AWAITING SEAT: fable5] cxlaunchdaybreak closed by the tools/cxlaunch.sh landing and owes the REGRESS review, a distinct phase under the regress-is-fable-only directive, batched to the Sunday flagship sign-off after the battery.  The question is in the row's hold_question."}
  hold_question: "REGRESS (held 2026-10-16 at the tools/cxlaunch.sh landing): does regress/artifacts/cxlaunchland_20261016/RECEIPT_v3.txt still run the TRACKED file the landing replaced, the farm copy and the landed launcher against the same fixtures and get the recorded exits -- in particular N1/N2 8 -> 0 (the quoted-wall false positive), D1 7 -> 0 (the Daybreak fallback), X8 6 -> 8 (a NUL in stderr) -- and does regress/artifacts/cxlaunchland_20261016/KILLTABLE_v3.txt still kill every pinned mutant while the three filed in cxlaunchunpinned escape as recorded?  Is the record (the launcher's header, the CHANGELOG block, the OB corrections) true of what shipped?"
  state: "closed"
  witness: "harness:regress/artifacts/cxlaunchland_20261016/RECEIPT_v3.txt -- D1: the tracked launcher exits 7 on a refusal (no fallback), the landed one re-runs it once on gpt-daybreak-blue-latest and credits Daybreak (exit 0); E2 pins both calls' exact argument sequences (sandbox flag, model, effort and brief included); the real-run receipt is regress/artifacts/codexpack_20260928/dossier_gdromdma/dossier_gdromdma.launch.log"

== cxlaunchquotation 
  closure: {"by": "opus5-mainloop", "badge": "A", "note": "CLOSED by the tools/cxlaunch.sh landing: the production rule (codex's ^ERROR: lines, ANSI-stripped and read with grep -a, classified ONLY when rc != 0 or stdout is empty; stdout never grepped for wall words) replaces the classifier that scored a complete answer WALLED for the word 'quota' or a quoted wall line.  Witness: the tracked file exits 8 on N1/N2, the landed one 0 (RECEIPT_v3.txt).  Three passes on the landed file -- pass 2, the adjudication pass and the v3 pass, the owner's four-seat roster each time (Fable 5.1 stalled on the adjudication pass and was re-fired on v3; Opus, agy, kimi, deepseek and minimax not fired)."}
  + entry: {"phase": "regress", "seat": "fable5", "date": "2026-10-16", "grade": "UNKNOWN", "grader": "", "ev": "not fired", "note": "[HELD AWAITING SEAT: fable5] cxlaunchquotation closed by the tools/cxlaunch.sh landing and owes the REGRESS review, a distinct phase under the regress-is-fable-only directive, batched to the Sunday flagship sign-off after the battery.  The question is in the row's hold_question."}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "codex", "note": "PASS 2 (the landed launcher, v1): SHIP WITH CHANGES (2) -- GPT-6 Astra (ultra, `ran: model: gpt-6-astra'): read the model only from codex's header block and stop crediting 'answered by' when it is absent; make the controls exit non-zero on a bad tally and pin the `^ERROR:' anchor and the effort argument.  Both applied in v2.", "ev": "regress/artifacts/cxlaunchland_20261016/pass2/codex_cxland.txt"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "glm", "note": "PASS 2: SHIP WITH CHANGES (2) -- GLM 5.3 (glm-5.3:cloud): reword the UNVERIFIED note to what was searched and put a count behind the header window; record that the ANSI strip widens both residuals.  Applied (v2 dropped the window for the header block; the residual is in the launcher's header).", "ev": "regress/artifacts/cxlaunchland_20261016/pass2/glm_cxland.txt"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "grok", "note": "PASS 2: SHIP WITH CHANGES (1) -- Grok 4.7 (xhigh): grep without -a reads a NUL-bearing stderr as binary and drops the wall lines -- the real 2026-09-19 battery-preflight wall was recorded exit 6.  Measured on that file and fixed (grep -a, control X8).", "ev": "regress/artifacts/cxlaunchland_20261016/pass2/grok_cxland.txt"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "fable5", "note": "PASS 2: SHIP WITH CHANGES (2) -- Fable 5.1, in two parts: its first run FELL BACK to claude-opus-4-8 after two refusals (FALLBACK_opus48_cxland.md, credited as Opus 4.8, and that run executed the TRACKED launcher unmodified and fired nine real Astra calls -- disclosed, no tree writes); resumed, Fable 5.1 wrote v2 itself: C1 add the tracked file as the pre-fix column, C2 correct two bug-file statements by content, pin four escapes and leave two unpinned.  All applied.", "ev": "regress/artifacts/cxlaunchland_20261016/pass2/fable5_cxland_v2.md"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "codex", "note": "ADJUDICATION PASS (v2): SHIP WITH CHANGES (3) -- GPT-6 Astra: the header-block awk matched the banner ANYWHERE (N1's own stderr quotes four complete headers from line 5528), so v3 reads only the OPENING block; E1/E2 matched a substring, so `ultrax' passed -- v3 compares the exact argument sequence; and the record edits the packet called done were not yet in the tree.", "ev": "regress/artifacts/cxlaunchland_20261016/f2/codex_cxlandf2.txt"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "grok", "note": "ADJUDICATION PASS (v2): SHIP WITH CHANGES (3) -- Grok 4.7: launcher, controls and kill table hold; the three changes are the records the packet described as written (F10, F19, the cxlaunchunpinned filing), which were prepared but not yet applied.", "ev": "regress/artifacts/cxlaunchland_20261016/f2/grok_cxlandf2.txt"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "glm", "note": "ADJUDICATION PASS (v2): SHIP WITH CHANGES (3) -- GLM 5.3, answering under the Fable seat's token (the packet listed all four; the transport is glm-5.3:cloud): cite RECEIPT_v2 not RECEIPT in the header, correct m_eq1's reason (N4 is rc 1; the observable shape is an rc outside {0,1} with an answer), pin --sandbox read-only and the brief.  All applied in v3.", "ev": "regress/artifacts/cxlaunchland_20261016/f2/glm_cxlandf2.txt"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "fable5", "note": "ADJUDICATION PASS (v2): SEAT FAILURE -- the Fable 5.1 agent STALLED (stream watchdog, no progress for 600 s) after its opening line; no answer file.  Re-fired on the v3 pass, not counted as agreement."}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "opus5", "note": "PASS 2 and the adjudication pass, NOT FIRED: outside the owner's four-seat roster; the measurements an Opus seat would make were the main loop's kill tables, each with its receipt."}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "agy", "note": "PASS 2 and the adjudication pass, NOT FIRED: agy is not on the owner's roster for this landing."}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "kimi", "note": "PASS 2 and the adjudication pass, NOT FIRED: the kimi seat sat outside the roster; nothing was sent."}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "deepseek", "note": "PASS 2 and the adjudication pass, NOT FIRED: GLM 5.3 was the one packet-fed seat fired."}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "minimax", "note": "PASS 2 and the adjudication pass, NOT FIRED: minimax-m3 was not given either packet; the roster, not a wall."}
  hold_question: "REGRESS (held 2026-10-16 at the tools/cxlaunch.sh landing): does regress/artifacts/cxlaunchland_20261016/RECEIPT_v3.txt still run the TRACKED file the landing replaced, the farm copy and the landed launcher against the same fixtures and get the recorded exits -- in particular N1/N2 8 -> 0 (the quoted-wall false positive), D1 7 -> 0 (the Daybreak fallback), X8 6 -> 8 (a NUL in stderr) -- and does regress/artifacts/cxlaunchland_20261016/KILLTABLE_v3.txt still kill every pinned mutant while the three filed in cxlaunchunpinned escape as recorded?  Is the record (the launcher's header, the CHANGELOG block, the OB corrections) true of what shipped?"
  state: "closed"
  state_note: "filed 2026-10-09: measured on GPT-6 Astra's check of the asiceventaddr convergence -- a complete 10,466-byte answer with its verdict line, no `ERROR:` line on stderr, and the launcher printed 'SEAT WALLED' (LAUNCH_RC=8) because the answer's own sentence '... its quotation must retain ...' matched `grep -ic 'quota'` (the answer: regress/artifacts/fablequeue8n_20261009/astra_confirm/codex_astra_asicconverge.txt; the launcher's own output: cxlaunch_asicconverge_stdout.txt beside it).  tools/cxlaunch.sh:44 builds `wall` from the `ERROR:` lines PLUS the whole stdout, so any answer that uses the words quota / quotation / rate limit / usage limit reads as a wall -- the carrier's quoting-re-arms-the-reader class, one level down (the script's own comment at :33-41 diagnoses the stderr half and kept the stdout half).  Fix: word-anchor the pattern and test stdout only when no verdict line is present; owes controls both ways (a real 403/quota notice still reds; an answer containing 'quotation' does not).  LOW: a human reads the answer; an unattended runner would discard it.\n\n[2026-10-16] CLOSED by the tools/cxlaunch.sh landing -- and the fix this note prescribes (\"word-anchor the pattern and test stdout only when no verdict line is present\") was REPLACED by the three-seat ruling's production rule, not applied: stdout is never grepped for wall words; codex's ^ERROR: lines are classified only when rc != 0 or stdout is empty (regress/artifacts/adj_20261016/RULINGS_C_records.md F1).  Merges the 2026-09-26 filing cxlaunchwallfp (no ledger row)."
  witness: "harness:regress/artifacts/cxlaunchland_20261016/RECEIPT_v3.txt -- the TRACKED launcher (cb180d9d) exits 8 on N1 and N2, a real answer scored WALLED for a quoted wall line and for the word 'quota' in the answer, and the landed file exits 0 on both; regress/artifacts/cxlaunchland_20261016/KILLTABLE_v3.txt kills every pinned one-edit mutant of the landed file"

== cxlaunchunpinned (NEW ROW)
  commits: ""
  id: "cxlaunchunpinned"
  sev: "LOW"
  state: "open"
  state_note: "filed 2026-10-16 from the landing's pass 2 (Fable 5.1, regress/artifacts/cxlaunchland_20261016/pass2/fable5_cxland_v2.md): each is MEASURED to escape the landed controls in regress/artifacts/cxlaunchland_20261016/KILLTABLE_v3.txt.  Pin each the day a real instance appears: a codex run exiting outside {0, 1} with an answer and a quoted wall line; a non-SGR CSI or OSC sequence before a codex diagnostic; a stderr carrying both a refusal and a wall line."
  title: "tools/cxlaunch.sh: three one-edit escapes are unpinned by ruling -- `-ne 0` -> `-eq 1` in the classify gate (an rc outside {0, 1} with an answer, a sibling of the N4 residual), the ANSI strip narrowed to SGR, and wall-before-refusal precedence (0 instances of each on record)"
  witness: null
```

### 5c. regress/artifacts/adj_20261016/RULINGS_C_records.md (G9)

```diff
--- rulingsC_head.md	2026-10-16 23:51:34.754772700 -0500
+++ rulingsC_f1_preview.md	2026-10-16 23:51:35.147397900 -0500
@@ -35,6 +35,10 @@
 - MERGE the prior filing `cxlaunchwallfp` (OUTSTANDING_BUGS.md:22494-22503, 2026-09-26, no ledger row) into this
   landing (Fable); correct OB:24714-24716 and ledger :62489 to this rule; closes `cxlaunchdaybreak` (ultra + Daybreak
   ride along).
+  *[2026-10-16, at the launcher landing (Grok 4.7, adjudication pass): these line citations did not hold even at this
+  file's own commit c64445fa -- read them by id.  `OUTSTANDING_BUGS.md:22494-22503` is the `cxlaunchwallfp` entry,
+  `OB:24714-24716` the `cxlaunchquotation` entry ("Word-anchor it and test stdout only when no verdict line is
+  present"), and ledger `:62489` the `cxlaunchquotation` row.]*
 - NEW, from Astra: the launcher prints the model it RAN but `ANSWERED_BY` is the model it ASKED for -- the "a wrong name is
   a SEAT FAILURE" comment is unenforced.  File as a rider on the landing (compare the `^model:` header to the request).
 
```

