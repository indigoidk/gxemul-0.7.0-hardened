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
#       (adj_20261016/fable5/meas_C/ansi_census.txt; 0 of 593 launcher .err files), and one is a REAL codex refusal:
#       _scratchpad/panel_20260919_013302/codex_adv540p2.REFUSED1.err, where `grep '^ERROR:'` finds 0 lines unstripped
#       and 2 stripped.  Unstripped, such a run reads exit 6 "seat down" (Fable's Q3 is the wall-shaped twin).
#    4. (2026-10-16, GPT-6 Astra) the `model:` line of codex's HEADER BLOCK is COMPARED to the model asked for.  This
#       file printed both and compared neither, so "a wrong name is a SEAT FAILURE" was unenforced.  On record: 322
#       asked/ran pairs across 519 launch logs under the project root, 319 across 493 inside GXEMUL-SEC (Astra), no
#       header absent and no mismatch -- so a mismatch is new, and it exits 5.  Only the OPENING header block is read
#       (pass 2 and the adjudication pass, Astra): a `model:` line anywhere else in stderr is streamed source or the
#       brief -- it can name a model, and it is never READ (GLM 5.3 and Grok 4.7, v3 pass).
#
#  KNOWN RESIDUALS -- recorded, NOT fixed (the ruling's own wording; no real run has either shape, 0 of 387 launch
#  lines are off the diagonal of {rc 0 with stdout, rc 1 with empty stdout} -- adj_20261016/fable5/meas_C/
#  launchlog_census.txt):
#    * rc != 0 WITH an answer AND column-0 quoted wall text -> exit 8 (fixture N4).  Reading only codex's LAST
#      `ERROR:` line does not fix it: in N4 that line is itself a quotation.
#    * its refusal twin: a quoted `flagged for possible cybersecurity` line on rc != 0 -> the Daybreak re-run fires
#      and the first answer is renamed codex_<tag>.refused.* (Grok 4.7).
#    * a run whose stderr carries NO opening codex header block is reported "model UNVERIFIED" and is not failed -- 0 of
#      330 launcher-captured answered runs on record lack it (counted on pass 2); failing it would lose every answer to a
#      CLI format change.  A block whose closing rule never comes is read for 30 lines at most.
#    * the ANSI strip widens both residuals above to colour-prefixed quoted lines on a failed or empty run (GLM 5.3,
#      pass 2): a quoted line whose only prefix was colour becomes column-0 -- still inside the classify-on-failure gate.
#    * a REFUSED first run's header is printed (`ran:`) but not compared; its answer is discarded, and the fallback's
#      own run is the one compared (GLM 5.3, pass 2).
#    * exit 5 is new to callers: the farm's pack runner special-cases 7 and 8 only, so it RETRIES a 5 rather than
#      recording an answer (Grok 4.7, pass 2) -- a different model having answered is not an answer from this seat.
#      The mechanism (_scratchpad/codexpack_20260928/run_pack_body.sh, read 2026-10-17): it reports a 7, STOPs the pack
#      on an 8, and its done_job counts a job done only when the launch log says `seat answered` or `The answer is
#      LOST` -- so a 5 or a 6 is left not done and the next pack run fires it again.  Those two phrases, and the
#      `answered by: <model>` the runner records, are therefore part of this file's contract (controls row PK, v5).
#
#  Overrides, each only so the branches are testable without the network: CX_MODEL, CX_EFFORT, CX_AUP_MODEL (set it
#  EMPTY to disable the fallback), CX_AUP_EFFORT, CX_CODEX_BIN.
#
#  Exit status: 0 answered; 5 a different model ran; 6 empty stdout with no refusal or wall text; 7 refused (after
#  the fallback, if any); 8 walled; 9 the brief is above the argv cap or the project dir is missing; otherwise
#  codex's own nonzero rc.  An answered run whose model is unverified still exits 0, and says so instead of naming
#  a model.  Controls: regress/artifacts/cxlaunchland_20261016/run_controls_v5.sh (RECEIPT_v5.txt; the kill table is
#  KILLTABLE_v5.txt).  Its header is the CONTRACT: the decisions found by reading every predicate, pattern alternative,
#  redirection, constant and caller-read log phrase of this file, each with the rows that pin its edges or the reason
#  it is not pinned.  RECEIPT.txt and RECEIPT_v2.txt to RECEIPT_v4.txt are the receipts of the earlier versions.
#
#  Usage: cxlaunch.sh <brief-path> <out-dir> <tag>   -- ABSOLUTE paths.  The brief's size and `mkdir` resolve in the caller's
#  directory, codex's files after `cd "$PROJ"`, so a relative path breaks: measured 2026-10-17, a relative pointer read 787
#  bytes, then codex got no brief and the run exited 1, NOT a clean run.  Every caller on record passes absolute paths.
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
    #  codex's OPENING header block -- `OpenAI Codex vX`, then the lines between the next two `--------` rules -- names the
    #  model and effort it actually ran.  Read only that block, and only at the TOP of stderr: the banner and its first
    #  rule must appear by line 12 and the block is read for at most 30 lines.  On record the block's `model:` line is
    #  line 5 of stderr in 599 of 600 codex .err files and line 7 in one (two pre-header lines; Astra).  A `model:` line
    #  anywhere else is streamed source or the brief and is never READ -- including a complete QUOTED header block, which
    #  N1's own stderr carries at line 5528 (GPT-6 Astra, adjudication pass: v2 matched the banner anywhere).
    HDR=$(strip_ansi "$ERR" | awk 'NR > 12 && h < 2 { exit }
        h == 0 && /^OpenAI Codex/ { h = 1; next }
        h == 1 && /^--------/ { h = 2; next }
        h == 2 && /--------/ { exit }
        h == 2 { if (++n > 30) exit; print }')
    RAN=$(printf '%s\n' "$HDR" | grep -m1 '^model:' | sed 's/^model:[[:space:]]*//; s/[[:space:]]*$//')
    echo "codex rc=$rc   stdout=$(wc -c < "$TXT") b   stderr=$(wc -c < "$ERR") b   asked: $1 / $2"
    echo "  ran: ${RAN:+model: $RAN} / $(printf '%s\n' "$HDR" | grep -m1 '^reasoning effort:')"
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
    #  `grep -a`: a stderr carrying a NUL byte is "binary" to grep, which then prints `Binary file (standard input)
    #  matches` instead of the lines.  A real wall was recorded exit 6 "seat down" that way:
    #  _scratchpad/cxfarm3_20260919/out/codex_l1_batterypreflight.err (rc 1, empty stdout, 1,449 NULs from byte 2,318,517;
    #  its two column-0 `ERROR: You've hit your usage limit` lines come after them) -- Grok 4.7, pass 2, re-run here.
    CXERR=$(strip_ansi "$ERR" | grep -a '^ERROR:')
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
if [ "$rc" -ne 0 ];  then echo "  *** codex exited $rc -- NOT a clean run."; exit "$rc"; fi
if [ -z "$RAN" ]; then
    echo "  seat answered -- model UNVERIFIED: no codex header block in stderr (requested: $ANSWERED_BY)"
else
    echo "  seat answered. (answered by: $ANSWERED_BY)"
fi
