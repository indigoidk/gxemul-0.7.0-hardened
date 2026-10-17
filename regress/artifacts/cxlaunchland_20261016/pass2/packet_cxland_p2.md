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

## 4. The delta from the production copy the farm ran (`cxlaunch_before.sh`, md5 3c51a757) to the landed file -- `diff -u`, 6 hunks

```diff
--- /c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/cxlaunchland_20261016/cxlaunch_before.sh	2026-10-16 21:18:51.844006600 -0500
+++ /c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/tools/cxlaunch.sh	2026-10-16 21:18:00.242370200 -0500
@@ -1,8 +1,21 @@
 #!/bin/bash
-#  cxlaunch_u.sh -- tools/cxlaunch.sh (HEAD) plus two owner directives of 2026-09-26, staged in the scratchpad until
-#  the farm jobs that are reading tools/cxlaunch.sh have exited (bash reads a running script incrementally, so the
-#  tracked file is not edited under them):
+#  A codex launcher that CANNOT report a refused seat as a clean run.
 #
+#  *** THE TWO DEFECTS THIS REPLACES, both mine, both measured 2026-09-07 on the lcaconfwidth
+#  census. ***
+#    1. The content check grepped the .txt for refusal text.  A codex CONTENT-FILTER REFUSAL writes
+#       NOTHING to stdout and puts "ERROR: This content was flagged..." on STDERR -- so the check
+#       reported `refusal hits: 0` on a refusal.  A check that looks in the wrong stream answers the
+#       same whether or not the thing it tests is true.
+#    2. The script ended on a successful command, so it exited 0 while holding `codex rc=1`.  The
+#       harness then reported the task as COMPLETED.  A failure laundered into a clean completion.
+#
+#  *** LANDED HERE 2026-10-16 (ledger `cxlaunchquotation`; ruled by Fable 5.1, GPT-6 Astra and Grok 4.7 in
+#  regress/artifacts/adj_20261016/RULINGS_C_records.md, F1).  Until then THIS file ran Astra at `max` with the
+#  2026-09-07 classifier, while most farm jobs ran an UNTRACKED scratchpad copy (cxlaunch_u.sh) carrying the two
+#  owner directives of 2026-09-26 -- and the carrier described the copy's behaviour as this file's.  Not every job
+#  ran the copy: the 2026-10-09 asicconverge confirm used the old classifier and reported an rc-0, 10,466-byte answer
+#  as WALLED (fablequeue8n_20261009/astra_confirm/cxlaunch_asicconverge_stdout.txt). ***
 #    1. "Astra (ultra) can replace codex 5.6 sol" -- the effort is `ultra`.  MEASURED 2026-09-26 before use: the
 #       server's enum lists 'none'..'xhigh','max' and rejects a bogus value with 400 invalid_enum_value; `ultra` is
 #       accepted (rc 0, header `reasoning effort: ultra`, liveness token and a verbatim CHECKPOINT.md quote returned).
@@ -13,12 +26,34 @@
 #       (gpt-daybreak-blue-latest, the CLI's only Daybreak slug: "frontier agentic coding model for broad defensive
 #       cybersecurity work"; liveness-verified 2026-09-26).  The refused run's files are KEPT as
 #       codex_<tag>.refused.{txt,err}, and the log names which model answered -- a Daybreak answer is recorded as
-#       Daybreak's, never as Astra's.
+#       Daybreak's, never as Astra's.  The receipt of the fallback firing on a REAL refusal is
+#       regress/artifacts/codexpack_20260928/dossier_gdromdma/dossier_gdromdma.launch.log; the controls below test
+#       the classifier on fixtures, which is a different claim.
+#    3. (2026-10-16, Fable 5.1) codex's diagnostics are matched AFTER ANSI colour is stripped.  7 of 453 panel.sh
+#       codex.txt files carry a column-0 `ERROR:` coloured as ESC[1m ESC[31m ERROR: ESC[0m
+#       (adj_20261016/fable5/meas_C/ansi_census.txt; 0 of 593 launcher .err files), and the unstripped anchor read
+#       such a real wall as exit 6 "seat down" (Fable's Q3).
+#    4. (2026-10-16, GPT-6 Astra) the `model:` header codex prints is COMPARED to the model asked for.  This file
+#       printed both and compared neither, so "a wrong name is a SEAT FAILURE" was unenforced.  322 asked/ran pairs
+#       across 519 launch logs on 2026-10-16: no header absent, no mismatch -- so a mismatch is new, and it exits 5.
+#
+#  KNOWN RESIDUALS -- recorded, NOT fixed (the ruling's own wording; no real run has either shape, 0 of 387 launch
+#  lines are off the diagonal of {rc 0 with stdout, rc 1 with empty stdout} -- adj_20261016/fable5/meas_C/
+#  launchlog_census.txt):
+#    * rc != 0 WITH an answer AND column-0 quoted wall text -> exit 8 (fixture N4).  Reading only codex's LAST
+#      `ERROR:` line does not fix it: in N4 that line is itself a quotation.
+#    * its refusal twin: a quoted `flagged for possible cybersecurity` line on rc != 0 -> the Daybreak re-run fires
+#      and the first answer is renamed codex_<tag>.refused.* (Grok 4.7).
+#    * a run whose stderr carries NO `model:` header is reported UNVERIFIED and is not failed (none on record).
 #
 #  Overrides, each only so the branches are testable without the network: CX_MODEL, CX_EFFORT, CX_AUP_MODEL (set it
 #  EMPTY to disable the fallback), CX_AUP_EFFORT, CX_CODEX_BIN.
 #
-#  Usage: cxlaunch_u.sh <brief-path> <out-dir> <tag>
+#  Exit status: 0 answered; 5 a different model ran; 6 empty stdout with no refusal or wall text; 7 refused (after
+#  the fallback, if any); 8 walled; 9 the brief is above the argv cap or the project dir is missing; otherwise
+#  codex's own nonzero rc.  Controls: regress/artifacts/cxlaunchland_20261016/ (RECEIPT.txt).
+#
+#  Usage: cxlaunch.sh <brief-path> <out-dir> <tag>
 set -u
 BRIEF="$1"; OUT="$2"; TAG="$3"
 PROJ=/c/DocumentNoSnc/CC/GXEMUL
@@ -29,6 +64,7 @@
 AUP_EFFORT="${CX_AUP_EFFORT:-ultra}"
 mkdir -p "$OUT"
 TXT="$OUT/codex_${TAG}.txt"; ERR="$OUT/codex_${TAG}.err"
+ESC=$(printf '\033')
 
 sz=$(wc -c < "$BRIEF")
 echo "brief bytes: $sz"
@@ -36,30 +72,35 @@
 
 cd "$PROJ" || exit 9
 
+strip_ansi() { sed "s/${ESC}\[[0-9;]*[A-Za-z]//g" "$1" 2>/dev/null; }
+
 run_codex() {    # $1 model, $2 effort
     "$CODEX" exec --sandbox read-only --skip-git-repo-check -m "$1" \
         -c model_reasoning_effort="$2" "$(cat "$BRIEF")" > "$TXT" 2> "$ERR" < /dev/null
     rc=$?
+    #  the header codex prints (in its first dozen stderr lines, before the brief and any streamed source) names the
+    #  model and effort it actually ran
+    RAN=$(strip_ansi "$ERR" | head -n 40 | grep -m1 '^model:' | sed 's/^model:[[:space:]]*//; s/[[:space:]]*$//')
     echo "codex rc=$rc   stdout=$(wc -c < "$TXT") b   stderr=$(wc -c < "$ERR") b   asked: $1 / $2"
-    #  the header codex prints names the model and effort it actually ran -- a wrong name is a SEAT FAILURE
-    echo "  ran: $(grep -m1 '^model:' "$ERR" 2>/dev/null) / $(grep -m1 '^reasoning effort:' "$ERR" 2>/dev/null)"
+    echo "  ran: ${RAN:+model: $RAN} / $(strip_ansi "$ERR" | head -n 40 | grep -m1 '^reasoning effort:')"
 }
 
 #  CONTENT CHECK.  Verify by content, never by size -- and NOT by grepping stderr for codex's diagnostics alone.
 #
-#  *** MEASURED 2026-09-07, on the run that installed tools/cxlaunch.sh: codex STREAMS THE SOURCE IT READS into
-#  stderr, so a bare grep over stderr matches any file containing the words -- hence the `^ERROR:` anchor. ***
+#  *** MEASURED 2026-09-07, on the run that installed this file: codex STREAMS THE SOURCE IT READS into stderr, so a
+#  bare grep over stderr matches any file containing the words -- hence the `^ERROR:` anchor. ***
 #
 #  *** AND THE ANCHOR IS NOT ENOUGH.  MEASURED 2026-09-26: THREE REAL ANSWERS WERE REPORTED "SEAT WALLED" -- astra549
 #  (rc 0, 11,472 b), astra550 (rc 0, 4,265 b), rec529audit (rc 0, 13,442 b) -- because each read an old panel file
 #  whose lines BEGIN with a codex wall message ("ERROR: You've hit your usage limit ... 7:01 AM"), and codex streamed
 #  those lines into stderr at column 0.  A quoted marker re-arms the tool that reads it (the carrier's own rule). ***
 #
-#  So the discriminator is the EXIT STATUS and the ANSWER, which quoted text cannot forge: every real wall and every
-#  real content-filter refusal on record is rc 1 with an EMPTY stdout (the launch logs of 2026-09-25/26).  rc 0 with an
-#  answer is an ANSWER, whatever stderr quotes; only a failed run is classified by its ERROR: lines.
+#  So the discriminator is the EXIT STATUS and the ANSWER, which quoted text cannot forge.  stderr's `ERROR:` lines are
+#  classified ONLY WHEN rc != 0 OR stdout IS EMPTY; rc 0 with a non-empty stdout is an ANSWER, whatever stderr quotes.
+#  Every real wall and refusal on record is rc 1 with an EMPTY stdout, and every rc-0 run carries an answer: 362 + 25
+#  of 387 launch lines, nothing off that diagonal (launchlog_census.txt) -- the residuals above are the off-diagonal.
 classify() {
-    CXERR=$(grep '^ERROR:' "$ERR" 2>/dev/null)
+    CXERR=$(strip_ansi "$ERR" | grep '^ERROR:')
     verd=$(grep -ic 'VERDICT' "$TXT" 2>/dev/null)
     body=$(wc -c < "$TXT")
     refus=0; wall=0
@@ -78,7 +119,7 @@
 
 if [ "$refus" -gt 0 ] && [ -n "$AUP_MODEL" ] && [ "$AUP_MODEL" != "$MODEL" ]; then
     echo "  *** SEAT REFUSED on $MODEL (content filter):"
-    grep -m1 -i 'flagged for possible cybersecurity' "$ERR" | cut -c1-160 | sed 's/^/    /'
+    printf '%s\n' "$CXERR" | grep -m1 -i 'flagged for possible cybersecurity' | cut -c1-160 | sed 's/^/    /'
     mv -f "$TXT" "$OUT/codex_${TAG}.refused.txt"; mv -f "$ERR" "$OUT/codex_${TAG}.refused.err"
     echo "  *** AUP FALLBACK: re-running ONCE on $AUP_MODEL / $AUP_EFFORT (the refused run is kept as codex_${TAG}.refused.*)"
     run_codex "$AUP_MODEL" "$AUP_EFFORT"; classify
@@ -87,11 +128,16 @@
 
 if [ "$refus" -gt 0 ]; then
     echo "  *** SEAT REFUSED (content filter) on $ANSWERED_BY.  The answer is LOST, whatever the token count says."
-    grep -m2 -i 'flagged for possible cybersecurity' "$ERR" | cut -c1-160 | sed 's/^/    /'
+    printf '%s\n' "$CXERR" | grep -m2 -i 'flagged for possible cybersecurity' | cut -c1-160 | sed 's/^/    /'
     echo "  *** REPHRASE (neutral test-coverage wording) or ROUTE THIS BRIEF TO GROK."
     exit 7
 fi
 if [ "$wall" -gt 0 ]; then echo "  *** SEAT WALLED ($ANSWERED_BY)."; exit 8; fi
 if [ "$body" -eq 0 ]; then echo "  *** EMPTY STDOUT with no refusal/wall text -- seat down, cause NOT established."; exit 6; fi
+if [ -n "$RAN" ] && [ "$RAN" != "$ANSWERED_BY" ]; then
+    echo "  *** A DIFFERENT MODEL RAN: asked $ANSWERED_BY, codex's header says $RAN -- a SEAT FAILURE; the answer is not $ANSWERED_BY's."
+    exit 5
+fi
+[ -z "$RAN" ] && echo "  note: no model: header in stderr -- the answering model is UNVERIFIED"
 if [ "$rc" -ne 0 ];  then echo "  *** codex exited $rc -- NOT a clean run."; exit "$rc"; fi
 echo "  seat answered. (answered by: $ANSWERED_BY)"
```

## 5. The landed `tools/cxlaunch.sh`, whole (the tracked file it replaces ran Astra at `max` with the 2026-09-07 classifier)

```bash
#!/bin/bash
#  A codex launcher that CANNOT report a refused seat as a clean run.
#
#  *** THE TWO DEFECTS THIS REPLACES, both mine, both measured 2026-09-07 on the lcaconfwidth
#  census. ***
#    1. The content check grepped the .txt for refusal text.  A codex CONTENT-FILTER REFUSAL writes
#       NOTHING to stdout and puts "ERROR: This content was flagged..." on STDERR -- so the check
#       reported `refusal hits: 0` on a refusal.  A check that looks in the wrong stream answers the
#       same whether or not the thing it tests is true.
#    2. The script ended on a successful command, so it exited 0 while holding `codex rc=1`.  The
#       harness then reported the task as COMPLETED.  A failure laundered into a clean completion.
#
#  *** LANDED HERE 2026-10-16 (ledger `cxlaunchquotation`; ruled by Fable 5.1, GPT-6 Astra and Grok 4.7 in
#  regress/artifacts/adj_20261016/RULINGS_C_records.md, F1).  Until then THIS file ran Astra at `max` with the
#  2026-09-07 classifier, while most farm jobs ran an UNTRACKED scratchpad copy (cxlaunch_u.sh) carrying the two
#  owner directives of 2026-09-26 -- and the carrier described the copy's behaviour as this file's.  Not every job
#  ran the copy: the 2026-10-09 asicconverge confirm used the old classifier and reported an rc-0, 10,466-byte answer
#  as WALLED (fablequeue8n_20261009/astra_confirm/cxlaunch_asicconverge_stdout.txt). ***
#    1. "Astra (ultra) can replace codex 5.6 sol" -- the effort is `ultra`.  MEASURED 2026-09-26 before use: the
#       server's enum lists 'none'..'xhigh','max' and rejects a bogus value with 400 invalid_enum_value; `ultra` is
#       accepted (rc 0, header `reasoning effort: ultra`, liveness token and a verbatim CHECKPOINT.md quote returned).
#       The CLI's own model cache describes it as "Maximum reasoning with automatic task delegation" -- max plus
#       delegation, so it is a CLI tier above max, not a server one.
#    2. "use daybreak ... if encountering AUP error" -- on a content-filter refusal (codex's own `ERROR: This content
#       was flagged for possible cybersecurity risk` on stderr) the brief is re-run ONCE on the Daybreak model
#       (gpt-daybreak-blue-latest, the CLI's only Daybreak slug: "frontier agentic coding model for broad defensive
#       cybersecurity work"; liveness-verified 2026-09-26).  The refused run's files are KEPT as
#       codex_<tag>.refused.{txt,err}, and the log names which model answered -- a Daybreak answer is recorded as
#       Daybreak's, never as Astra's.  The receipt of the fallback firing on a REAL refusal is
#       regress/artifacts/codexpack_20260928/dossier_gdromdma/dossier_gdromdma.launch.log; the controls below test
#       the classifier on fixtures, which is a different claim.
#    3. (2026-10-16, Fable 5.1) codex's diagnostics are matched AFTER ANSI colour is stripped.  7 of 453 panel.sh
#       codex.txt files carry a column-0 `ERROR:` coloured as ESC[1m ESC[31m ERROR: ESC[0m
#       (adj_20261016/fable5/meas_C/ansi_census.txt; 0 of 593 launcher .err files), and the unstripped anchor read
#       such a real wall as exit 6 "seat down" (Fable's Q3).
#    4. (2026-10-16, GPT-6 Astra) the `model:` header codex prints is COMPARED to the model asked for.  This file
#       printed both and compared neither, so "a wrong name is a SEAT FAILURE" was unenforced.  322 asked/ran pairs
#       across 519 launch logs on 2026-10-16: no header absent, no mismatch -- so a mismatch is new, and it exits 5.
#
#  KNOWN RESIDUALS -- recorded, NOT fixed (the ruling's own wording; no real run has either shape, 0 of 387 launch
#  lines are off the diagonal of {rc 0 with stdout, rc 1 with empty stdout} -- adj_20261016/fable5/meas_C/
#  launchlog_census.txt):
#    * rc != 0 WITH an answer AND column-0 quoted wall text -> exit 8 (fixture N4).  Reading only codex's LAST
#      `ERROR:` line does not fix it: in N4 that line is itself a quotation.
#    * its refusal twin: a quoted `flagged for possible cybersecurity` line on rc != 0 -> the Daybreak re-run fires
#      and the first answer is renamed codex_<tag>.refused.* (Grok 4.7).
#    * a run whose stderr carries NO `model:` header is reported UNVERIFIED and is not failed (none on record).
#
#  Overrides, each only so the branches are testable without the network: CX_MODEL, CX_EFFORT, CX_AUP_MODEL (set it
#  EMPTY to disable the fallback), CX_AUP_EFFORT, CX_CODEX_BIN.
#
#  Exit status: 0 answered; 5 a different model ran; 6 empty stdout with no refusal or wall text; 7 refused (after
#  the fallback, if any); 8 walled; 9 the brief is above the argv cap or the project dir is missing; otherwise
#  codex's own nonzero rc.  Controls: regress/artifacts/cxlaunchland_20261016/ (RECEIPT.txt).
#
#  Usage: cxlaunch.sh <brief-path> <out-dir> <tag>
set -u
BRIEF="$1"; OUT="$2"; TAG="$3"
PROJ=/c/DocumentNoSnc/CC/GXEMUL
CODEX="${CX_CODEX_BIN:-$HOME/AppData/Local/Programs/OpenAI/Codex/bin/codex}"
MODEL="${CX_MODEL:-gpt-6-astra}"
EFFORT="${CX_EFFORT:-ultra}"
AUP_MODEL="${CX_AUP_MODEL-gpt-daybreak-blue-latest}"
AUP_EFFORT="${CX_AUP_EFFORT:-ultra}"
mkdir -p "$OUT"
TXT="$OUT/codex_${TAG}.txt"; ERR="$OUT/codex_${TAG}.err"
ESC=$(printf '\033')

sz=$(wc -c < "$BRIEF")
echo "brief bytes: $sz"
[ "$sz" -gt 30000 ] && { echo "*** above the argv cap -- use the pointer form"; exit 9; }

cd "$PROJ" || exit 9

strip_ansi() { sed "s/${ESC}\[[0-9;]*[A-Za-z]//g" "$1" 2>/dev/null; }

run_codex() {    # $1 model, $2 effort
    "$CODEX" exec --sandbox read-only --skip-git-repo-check -m "$1" \
        -c model_reasoning_effort="$2" "$(cat "$BRIEF")" > "$TXT" 2> "$ERR" < /dev/null
    rc=$?
    #  the header codex prints (in its first dozen stderr lines, before the brief and any streamed source) names the
    #  model and effort it actually ran
    RAN=$(strip_ansi "$ERR" | head -n 40 | grep -m1 '^model:' | sed 's/^model:[[:space:]]*//; s/[[:space:]]*$//')
    echo "codex rc=$rc   stdout=$(wc -c < "$TXT") b   stderr=$(wc -c < "$ERR") b   asked: $1 / $2"
    echo "  ran: ${RAN:+model: $RAN} / $(strip_ansi "$ERR" | head -n 40 | grep -m1 '^reasoning effort:')"
}

#  CONTENT CHECK.  Verify by content, never by size -- and NOT by grepping stderr for codex's diagnostics alone.
#
#  *** MEASURED 2026-09-07, on the run that installed this file: codex STREAMS THE SOURCE IT READS into stderr, so a
#  bare grep over stderr matches any file containing the words -- hence the `^ERROR:` anchor. ***
#
#  *** AND THE ANCHOR IS NOT ENOUGH.  MEASURED 2026-09-26: THREE REAL ANSWERS WERE REPORTED "SEAT WALLED" -- astra549
#  (rc 0, 11,472 b), astra550 (rc 0, 4,265 b), rec529audit (rc 0, 13,442 b) -- because each read an old panel file
#  whose lines BEGIN with a codex wall message ("ERROR: You've hit your usage limit ... 7:01 AM"), and codex streamed
#  those lines into stderr at column 0.  A quoted marker re-arms the tool that reads it (the carrier's own rule). ***
#
#  So the discriminator is the EXIT STATUS and the ANSWER, which quoted text cannot forge.  stderr's `ERROR:` lines are
#  classified ONLY WHEN rc != 0 OR stdout IS EMPTY; rc 0 with a non-empty stdout is an ANSWER, whatever stderr quotes.
#  Every real wall and refusal on record is rc 1 with an EMPTY stdout, and every rc-0 run carries an answer: 362 + 25
#  of 387 launch lines, nothing off that diagonal (launchlog_census.txt) -- the residuals above are the off-diagonal.
classify() {
    CXERR=$(strip_ansi "$ERR" | grep '^ERROR:')
    verd=$(grep -ic 'VERDICT' "$TXT" 2>/dev/null)
    body=$(wc -c < "$TXT")
    refus=0; wall=0
    if [ "$rc" -ne 0 ] || [ "$body" -eq 0 ]; then
        refus=$(printf '%s' "$CXERR" | grep -ic 'flagged for possible cybersecurity\|cannot help with\|can.t help with\|I won.t help')
        wall=$(printf '%s' "$CXERR" | grep -ic 'usage limit\|quota\|rate limit\|not authenticated')
    else
        q=$(printf '%s' "$CXERR" | grep -c .)
        [ "$q" -gt 0 ] && echo "  note: $q ERROR:-shaped line(s) in stderr IGNORED -- rc 0 with an answer, so they are quoted source"
    fi
    echo "  verdict-in-stdout: $verd   refusal: $refus   wall: $wall   (classified only when rc != 0 or stdout is empty)"
}

run_codex "$MODEL" "$EFFORT"; classify
ANSWERED_BY="$MODEL"

if [ "$refus" -gt 0 ] && [ -n "$AUP_MODEL" ] && [ "$AUP_MODEL" != "$MODEL" ]; then
    echo "  *** SEAT REFUSED on $MODEL (content filter):"
    printf '%s\n' "$CXERR" | grep -m1 -i 'flagged for possible cybersecurity' | cut -c1-160 | sed 's/^/    /'
    mv -f "$TXT" "$OUT/codex_${TAG}.refused.txt"; mv -f "$ERR" "$OUT/codex_${TAG}.refused.err"
    echo "  *** AUP FALLBACK: re-running ONCE on $AUP_MODEL / $AUP_EFFORT (the refused run is kept as codex_${TAG}.refused.*)"
    run_codex "$AUP_MODEL" "$AUP_EFFORT"; classify
    ANSWERED_BY="$AUP_MODEL"
fi

if [ "$refus" -gt 0 ]; then
    echo "  *** SEAT REFUSED (content filter) on $ANSWERED_BY.  The answer is LOST, whatever the token count says."
    printf '%s\n' "$CXERR" | grep -m2 -i 'flagged for possible cybersecurity' | cut -c1-160 | sed 's/^/    /'
    echo "  *** REPHRASE (neutral test-coverage wording) or ROUTE THIS BRIEF TO GROK."
    exit 7
fi
if [ "$wall" -gt 0 ]; then echo "  *** SEAT WALLED ($ANSWERED_BY)."; exit 8; fi
if [ "$body" -eq 0 ]; then echo "  *** EMPTY STDOUT with no refusal/wall text -- seat down, cause NOT established."; exit 6; fi
if [ -n "$RAN" ] && [ "$RAN" != "$ANSWERED_BY" ]; then
    echo "  *** A DIFFERENT MODEL RAN: asked $ANSWERED_BY, codex's header says $RAN -- a SEAT FAILURE; the answer is not $ANSWERED_BY's."
    exit 5
fi
[ -z "$RAN" ] && echo "  note: no model: header in stderr -- the answering model is UNVERIFIED"
if [ "$rc" -ne 0 ];  then echo "  *** codex exited $rc -- NOT a clean run."; exit "$rc"; fi
echo "  seat answered. (answered by: $ANSWERED_BY)"
```

## 6. The controls -- `regress/artifacts/cxlaunchland_20261016/run_controls.sh` against a FAKE codex, RECEIPT.txt verbatim

```
# cxlaunch landing controls, 2026-10-16 21:20:17
# before: 3c51a7579065c5e6bebd5fd59d32b3ed  cxlaunch_before.sh
# after:  47d47097ca4a34573ebb103374f659c1  tools/cxlaunch.sh
P1  before exit=8  want=8  ok
      codex rc=1   stdout=0 b   stderr=296 b   asked: gpt-6-astra / ultra
        ran:  / 
        verdict-in-stdout: 0   refusal: 0   wall: 2   (classified only when rc != 0 or stdout is empty)
        *** SEAT WALLED (gpt-6-astra).
P1  after  exit=8  want=8  ok
      codex rc=1   stdout=0 b   stderr=296 b   asked: gpt-6-astra / ultra
        ran:  / 
        verdict-in-stdout: 0   refusal: 0   wall: 2   (classified only when rc != 0 or stdout is empty)
        *** SEAT WALLED (gpt-6-astra).
P2  before exit=7  want=7  ok
      codex rc=1   stdout=0 b   stderr=115 b   asked: gpt-6-astra / ultra
        ran:  / 
        verdict-in-stdout: 0   refusal: 1   wall: 0   (classified only when rc != 0 or stdout is empty)
        *** SEAT REFUSED (content filter) on gpt-6-astra.  The answer is LOST, whatever the token count says.
          ERROR: This content was flagged for possible cybersecurity risk. If this seems wrong, try rephrasing your request.
        *** REPHRASE (neutral test-coverage wording) or ROUTE THIS BRIEF TO GROK.
P2  after  exit=7  want=7  ok
      codex rc=1   stdout=0 b   stderr=115 b   asked: gpt-6-astra / ultra
        ran:  / 
        verdict-in-stdout: 0   refusal: 1   wall: 0   (classified only when rc != 0 or stdout is empty)
        *** SEAT REFUSED (content filter) on gpt-6-astra.  The answer is LOST, whatever the token count says.
          ERROR: This content was flagged for possible cybersecurity risk. If this seems wrong, try rephrasing your request.
        *** REPHRASE (neutral test-coverage wording) or ROUTE THIS BRIEF TO GROK.
N1  before exit=0  want=0  ok
      codex rc=0   stdout=4265 b   stderr=585565 b   asked: gpt-6-astra / ultra
        ran: model: gpt-6-astra / reasoning effort: max
        note: 6 ERROR:-shaped line(s) in stderr IGNORED -- rc 0 with an answer, so they are quoted source
        verdict-in-stdout: 2   refusal: 0   wall: 0   (classified only when rc != 0 or stdout is empty)
        seat answered. (answered by: gpt-6-astra)
N1  after  exit=0  want=0  ok
      codex rc=0   stdout=4265 b   stderr=585565 b   asked: gpt-6-astra / ultra
        ran: model: gpt-6-astra / reasoning effort: max
        note: 6 ERROR:-shaped line(s) in stderr IGNORED -- rc 0 with an answer, so they are quoted source
        verdict-in-stdout: 2   refusal: 0   wall: 0   (classified only when rc != 0 or stdout is empty)
        seat answered. (answered by: gpt-6-astra)
N2  before exit=0  want=0  ok
      codex rc=0   stdout=100 b   stderr=0 b   asked: gpt-6-astra / ultra
        ran:  / 
        verdict-in-stdout: 0   refusal: 0   wall: 0   (classified only when rc != 0 or stdout is empty)
        seat answered. (answered by: gpt-6-astra)
N2  after  exit=0  want=0  ok
      codex rc=0   stdout=100 b   stderr=0 b   asked: gpt-6-astra / ultra
        ran:  / 
        verdict-in-stdout: 0   refusal: 0   wall: 0   (classified only when rc != 0 or stdout is empty)
        note: no model: header in stderr -- the answering model is UNVERIFIED
        seat answered. (answered by: gpt-6-astra)
N3  before exit=6  want=6  ok
      codex rc=0   stdout=0 b   stderr=0 b   asked: gpt-6-astra / ultra
        ran:  / 
        verdict-in-stdout: 0   refusal: 0   wall: 0   (classified only when rc != 0 or stdout is empty)
        *** EMPTY STDOUT with no refusal/wall text -- seat down, cause NOT established.
N3  after  exit=6  want=6  ok
      codex rc=0   stdout=0 b   stderr=0 b   asked: gpt-6-astra / ultra
        ran:  / 
        verdict-in-stdout: 0   refusal: 0   wall: 0   (classified only when rc != 0 or stdout is empty)
        *** EMPTY STDOUT with no refusal/wall text -- seat down, cause NOT established.
N4  before exit=8  want=8  ok
      codex rc=1   stdout=4265 b   stderr=585565 b   asked: gpt-6-astra / ultra
        ran: model: gpt-6-astra / reasoning effort: max
        verdict-in-stdout: 2   refusal: 0   wall: 6   (classified only when rc != 0 or stdout is empty)
        *** SEAT WALLED (gpt-6-astra).
N4  after  exit=8  want=8  ok
      codex rc=1   stdout=4265 b   stderr=585565 b   asked: gpt-6-astra / ultra
        ran: model: gpt-6-astra / reasoning effort: max
        verdict-in-stdout: 2   refusal: 0   wall: 6   (classified only when rc != 0 or stdout is empty)
        *** SEAT WALLED (gpt-6-astra).
Q1  before exit=7  want=7  ok
      codex rc=1   stdout=0 b   stderr=161 b   asked: gpt-6-astra / ultra
        ran:  / 
        verdict-in-stdout: 0   refusal: 1   wall: 0   (classified only when rc != 0 or stdout is empty)
        *** SEAT REFUSED (content filter) on gpt-6-astra.  The answer is LOST, whatever the token count says.
          path/to/old_panel/codex.txt:17:ERROR: This content was flagged for possible cybersecurity risk.
          ERROR: This content was flagged for possible cybersecurity risk.
        *** REPHRASE (neutral test-coverage wording) or ROUTE THIS BRIEF TO GROK.
Q1  after  exit=7  want=7  ok
      codex rc=1   stdout=0 b   stderr=161 b   asked: gpt-6-astra / ultra
        ran:  / 
        verdict-in-stdout: 0   refusal: 1   wall: 0   (classified only when rc != 0 or stdout is empty)
        *** SEAT REFUSED (content filter) on gpt-6-astra.  The answer is LOST, whatever the token count says.
          ERROR: This content was flagged for possible cybersecurity risk.
        *** REPHRASE (neutral test-coverage wording) or ROUTE THIS BRIEF TO GROK.
Q2  before exit=8  want=8  ok
      codex rc=0   stdout=0 b   stderr=296 b   asked: gpt-6-astra / ultra
        ran:  / 
        verdict-in-stdout: 0   refusal: 0   wall: 2   (classified only when rc != 0 or stdout is empty)
        *** SEAT WALLED (gpt-6-astra).
Q2  after  exit=8  want=8  ok
      codex rc=0   stdout=0 b   stderr=296 b   asked: gpt-6-astra / ultra
        ran:  / 
        verdict-in-stdout: 0   refusal: 0   wall: 2   (classified only when rc != 0 or stdout is empty)
        *** SEAT WALLED (gpt-6-astra).
Q3  before exit=6  want=6  ok
      codex rc=1   stdout=0 b   stderr=330 b   asked: gpt-6-astra / ultra
        ran:  / 
        verdict-in-stdout: 0   refusal: 0   wall: 0   (classified only when rc != 0 or stdout is empty)
        *** EMPTY STDOUT with no refusal/wall text -- seat down, cause NOT established.
Q3  after  exit=8  want=8  ok
      codex rc=1   stdout=0 b   stderr=330 b   asked: gpt-6-astra / ultra
        ran:  / 
        verdict-in-stdout: 0   refusal: 0   wall: 2   (classified only when rc != 0 or stdout is empty)
        *** SEAT WALLED (gpt-6-astra).
A1  before exit=6  want=6  ok
      codex rc=1   stdout=0 b   stderr=132 b   asked: gpt-6-astra / ultra
        ran:  / 
        verdict-in-stdout: 0   refusal: 0   wall: 0   (classified only when rc != 0 or stdout is empty)
        *** EMPTY STDOUT with no refusal/wall text -- seat down, cause NOT established.
A1  after  exit=7  want=7  ok
      codex rc=1   stdout=0 b   stderr=132 b   asked: gpt-6-astra / ultra
        ran:  / 
        verdict-in-stdout: 0   refusal: 1   wall: 0   (classified only when rc != 0 or stdout is empty)
        *** SEAT REFUSED (content filter) on gpt-6-astra.  The answer is LOST, whatever the token count says.
          ERROR: This content was flagged for possible cybersecurity risk. If this seems wrong, try rephrasing your request.
        *** REPHRASE (neutral test-coverage wording) or ROUTE THIS BRIEF TO GROK.
M1  before exit=0  want=0  ok
      codex rc=0   stdout=4265 b   stderr=585565 b   asked: gpt-6-other / ultra
        ran: model: gpt-6-astra / reasoning effort: max
        note: 6 ERROR:-shaped line(s) in stderr IGNORED -- rc 0 with an answer, so they are quoted source
        verdict-in-stdout: 2   refusal: 0   wall: 0   (classified only when rc != 0 or stdout is empty)
        seat answered. (answered by: gpt-6-other)
M1  after  exit=5  want=5  ok
      codex rc=0   stdout=4265 b   stderr=585565 b   asked: gpt-6-other / ultra
        ran: model: gpt-6-astra / reasoning effort: max
        note: 6 ERROR:-shaped line(s) in stderr IGNORED -- rc 0 with an answer, so they are quoted source
        verdict-in-stdout: 2   refusal: 0   wall: 0   (classified only when rc != 0 or stdout is empty)
        *** A DIFFERENT MODEL RAN: asked gpt-6-other, codex's header says gpt-6-astra -- a SEAT FAILURE; the answer is not gpt-6-other's.
M2  before exit=0  want=0  ok
      codex rc=0   stdout=100 b   stderr=0 b   asked: gpt-6-astra / ultra
        ran:  / 
        verdict-in-stdout: 0   refusal: 0   wall: 0   (classified only when rc != 0 or stdout is empty)
        seat answered. (answered by: gpt-6-astra)
M2  after  exit=0  want=0  ok
      codex rc=0   stdout=100 b   stderr=0 b   asked: gpt-6-astra / ultra
        ran:  / 
        verdict-in-stdout: 0   refusal: 0   wall: 0   (classified only when rc != 0 or stdout is empty)
        note: no model: header in stderr -- the answering model is UNVERIFIED
        seat answered. (answered by: gpt-6-astra)
D1  before exit=0  want=0  ok
      codex rc=1   stdout=0 b   stderr=115 b   asked: gpt-6-astra / ultra
        ran:  / 
        verdict-in-stdout: 0   refusal: 1   wall: 0   (classified only when rc != 0 or stdout is empty)
        *** SEAT REFUSED on gpt-6-astra (content filter):
          ERROR: This content was flagged for possible cybersecurity risk. If this seems wrong, try rephrasing your request.
        *** AUP FALLBACK: re-running ONCE on gpt-daybreak-blue-latest / ultra (the refused run is kept as codex_D1.refused.*)
      codex rc=0   stdout=100 b   stderr=96 b   asked: gpt-daybreak-blue-latest / ultra
        ran: model: gpt-daybreak-blue-latest / reasoning effort: ultra
        verdict-in-stdout: 0   refusal: 0   wall: 0   (classified only when rc != 0 or stdout is empty)
        seat answered. (answered by: gpt-daybreak-blue-latest)
D1  after  exit=0  want=0  ok
      codex rc=1   stdout=0 b   stderr=115 b   asked: gpt-6-astra / ultra
        ran:  / 
        verdict-in-stdout: 0   refusal: 1   wall: 0   (classified only when rc != 0 or stdout is empty)
        *** SEAT REFUSED on gpt-6-astra (content filter):
          ERROR: This content was flagged for possible cybersecurity risk. If this seems wrong, try rephrasing your request.
        *** AUP FALLBACK: re-running ONCE on gpt-daybreak-blue-latest / ultra (the refused run is kept as codex_D1.refused.*)
      codex rc=0   stdout=100 b   stderr=96 b   asked: gpt-daybreak-blue-latest / ultra
        ran: model: gpt-daybreak-blue-latest / reasoning effort: ultra
        verdict-in-stdout: 0   refusal: 0   wall: 0   (classified only when rc != 0 or stdout is empty)
        seat answered. (answered by: gpt-daybreak-blue-latest)
D2  before exit=0  want=0  ok
      codex rc=1   stdout=0 b   stderr=115 b   asked: gpt-6-astra / ultra
        ran:  / 
        verdict-in-stdout: 0   refusal: 1   wall: 0   (classified only when rc != 0 or stdout is empty)
        *** SEAT REFUSED on gpt-6-astra (content filter):
          ERROR: This content was flagged for possible cybersecurity risk. If this seems wrong, try rephrasing your request.
        *** AUP FALLBACK: re-running ONCE on gpt-daybreak-blue-latest / ultra (the refused run is kept as codex_D2.refused.*)
      codex rc=0   stdout=100 b   stderr=83 b   asked: gpt-daybreak-blue-latest / ultra
        ran: model: gpt-6-astra / reasoning effort: ultra
        verdict-in-stdout: 0   refusal: 0   wall: 0   (classified only when rc != 0 or stdout is empty)
        seat answered. (answered by: gpt-daybreak-blue-latest)
D2  after  exit=5  want=5  ok
      codex rc=1   stdout=0 b   stderr=115 b   asked: gpt-6-astra / ultra
        ran:  / 
        verdict-in-stdout: 0   refusal: 1   wall: 0   (classified only when rc != 0 or stdout is empty)
        *** SEAT REFUSED on gpt-6-astra (content filter):
          ERROR: This content was flagged for possible cybersecurity risk. If this seems wrong, try rephrasing your request.
        *** AUP FALLBACK: re-running ONCE on gpt-daybreak-blue-latest / ultra (the refused run is kept as codex_D2.refused.*)
      codex rc=0   stdout=100 b   stderr=83 b   asked: gpt-daybreak-blue-latest / ultra
        ran: model: gpt-6-astra / reasoning effort: ultra
        verdict-in-stdout: 0   refusal: 0   wall: 0   (classified only when rc != 0 or stdout is empty)
        *** A DIFFERENT MODEL RAN: asked gpt-daybreak-blue-latest, codex's header says gpt-6-astra -- a SEAT FAILURE; the answer is not gpt-daybreak-blue-latest's.
M2  after  UNVERIFIED note printed  ok
D1  after  refused run kept, Daybreak credited  ok
CONTROLS: 30/30 as expected
CXLAND_CONTROLS_DONE
```

## 7. Questions -- verdict line first, then answer each by number; say plainly what you could not check

1. **The rule.**  Does the landed file implement the ruled condition exactly -- `ERROR:` lines classified only when
   `rc != 0` OR stdout is empty?  Is there any path where a REAL wall or refusal (rc 1, empty stdout, codex's own
   `ERROR:` at column 0) now ends as exit 0, or where an rc-0 answer with a non-empty stdout ends as 7 or 8?
2. **The ANSI strip.**  `sed "s/${ESC}\[[0-9;]*[A-Za-z]//g"` over the whole stderr, then `grep '^ERROR:'`.  Is the
   expression right for the measured shape (`ESC[1m ESC[31m ERROR: ESC[0m ESC[0m`)?  Name any ANSI form it misses
   (OSC `ESC]...`, a lone `ESC[K`, a carriage return) that could leave a real codex diagnostic unmatched, and say
   whether that form has any instance on record or is hypothetical.  Can the strip CREATE a column-0 `ERROR:` that was
   not one before (e.g. a quoted line whose only prefix was a colour code)?  If so, is that a regression against the
   production copy, and does the classify-only-on-failure condition bound it?
3. **The identity check.**  Exit 5 when the header names a model other than the one asked, compared AFTER the Daybreak
   fallback against the fallback model.  Is `head -n 40` a safe window for the header?  Can a quoted `model:` line from
   streamed source ever be read as the header (the header precedes the brief in every log on record)?  And section 3's
   first bullet: is UNVERIFIED-not-failed right?
4. **The controls (section 6).**  Each behaviour the landing changes should red on the BEFORE launcher and green on the
   AFTER launcher: Q3 and A1 (the ANSI strip), M1 and D2 (the identity check).  Is any control vacuous -- green on both
   for a reason other than the one it names?  **What is the smallest edit to the landed file that passes all 30 controls
   and breaks a ruled property?**  (A sketch is fine; do not build anything.)
5. **Records.**  The landing will close `cxlaunchquotation` (witness `harness:regress/artifacts/cxlaunchland_20261016/
   RECEIPT.txt`) and `cxlaunchdaybreak`, and mark the bug-file entry `cxlaunchwallfp` MERGED into it (its "key the stderr
   test on codex's error block at the END of the stream" fix shape is the refinement the ruling withdrew).  Anything wrong
   with closing them on this evidence?
6. **Which of my dispositions is wrong?**  Name the count you checked.
