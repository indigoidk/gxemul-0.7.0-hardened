#!/bin/bash
#  cxlaunch_u.sh -- tools/cxlaunch.sh (HEAD) plus two owner directives of 2026-09-26, staged in the scratchpad until
#  the farm jobs that are reading tools/cxlaunch.sh have exited (bash reads a running script incrementally, so the
#  tracked file is not edited under them):
#
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
#       Daybreak's, never as Astra's.
#
#  Overrides, each only so the branches are testable without the network: CX_MODEL, CX_EFFORT, CX_AUP_MODEL (set it
#  EMPTY to disable the fallback), CX_AUP_EFFORT, CX_CODEX_BIN.
#
#  Usage: cxlaunch_u.sh <brief-path> <out-dir> <tag>
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

sz=$(wc -c < "$BRIEF")
echo "brief bytes: $sz"
[ "$sz" -gt 30000 ] && { echo "*** above the argv cap -- use the pointer form"; exit 9; }

cd "$PROJ" || exit 9

run_codex() {    # $1 model, $2 effort
    "$CODEX" exec --sandbox read-only --skip-git-repo-check -m "$1" \
        -c model_reasoning_effort="$2" "$(cat "$BRIEF")" > "$TXT" 2> "$ERR" < /dev/null
    rc=$?
    echo "codex rc=$rc   stdout=$(wc -c < "$TXT") b   stderr=$(wc -c < "$ERR") b   asked: $1 / $2"
    #  the header codex prints names the model and effort it actually ran -- a wrong name is a SEAT FAILURE
    echo "  ran: $(grep -m1 '^model:' "$ERR" 2>/dev/null) / $(grep -m1 '^reasoning effort:' "$ERR" 2>/dev/null)"
}

#  CONTENT CHECK.  Verify by content, never by size -- and NOT by grepping stderr for codex's diagnostics alone.
#
#  *** MEASURED 2026-09-07, on the run that installed tools/cxlaunch.sh: codex STREAMS THE SOURCE IT READS into
#  stderr, so a bare grep over stderr matches any file containing the words -- hence the `^ERROR:` anchor. ***
#
#  *** AND THE ANCHOR IS NOT ENOUGH.  MEASURED 2026-09-26: THREE REAL ANSWERS WERE REPORTED "SEAT WALLED" -- astra549
#  (rc 0, 11,472 b), astra550 (rc 0, 4,265 b), rec529audit (rc 0, 13,442 b) -- because each read an old panel file
#  whose lines BEGIN with a codex wall message ("ERROR: You've hit your usage limit ... 7:01 AM"), and codex streamed
#  those lines into stderr at column 0.  A quoted marker re-arms the tool that reads it (the carrier's own rule). ***
#
#  So the discriminator is the EXIT STATUS and the ANSWER, which quoted text cannot forge: every real wall and every
#  real content-filter refusal on record is rc 1 with an EMPTY stdout (the launch logs of 2026-09-25/26).  rc 0 with an
#  answer is an ANSWER, whatever stderr quotes; only a failed run is classified by its ERROR: lines.
classify() {
    CXERR=$(grep '^ERROR:' "$ERR" 2>/dev/null)
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
    grep -m1 -i 'flagged for possible cybersecurity' "$ERR" | cut -c1-160 | sed 's/^/    /'
    mv -f "$TXT" "$OUT/codex_${TAG}.refused.txt"; mv -f "$ERR" "$OUT/codex_${TAG}.refused.err"
    echo "  *** AUP FALLBACK: re-running ONCE on $AUP_MODEL / $AUP_EFFORT (the refused run is kept as codex_${TAG}.refused.*)"
    run_codex "$AUP_MODEL" "$AUP_EFFORT"; classify
    ANSWERED_BY="$AUP_MODEL"
fi

if [ "$refus" -gt 0 ]; then
    echo "  *** SEAT REFUSED (content filter) on $ANSWERED_BY.  The answer is LOST, whatever the token count says."
    grep -m2 -i 'flagged for possible cybersecurity' "$ERR" | cut -c1-160 | sed 's/^/    /'
    echo "  *** REPHRASE (neutral test-coverage wording) or ROUTE THIS BRIEF TO GROK."
    exit 7
fi
if [ "$wall" -gt 0 ]; then echo "  *** SEAT WALLED ($ANSWERED_BY)."; exit 8; fi
if [ "$body" -eq 0 ]; then echo "  *** EMPTY STDOUT with no refusal/wall text -- seat down, cause NOT established."; exit 6; fi
if [ "$rc" -ne 0 ];  then echo "  *** codex exited $rc -- NOT a clean run."; exit "$rc"; fi
echo "  seat answered. (answered by: $ANSWERED_BY)"
