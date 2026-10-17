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
#  Usage: cxlaunch.sh <brief-path> <out-dir> <tag>
set -u
BRIEF="$1"; OUT="$2"; TAG="$3"
PROJ=/c/DocumentNoSnc/CC/GXEMUL
CODEX="$HOME/AppData/Local/Programs/OpenAI/Codex/bin/codex"
mkdir -p "$OUT"
TXT="$OUT/codex_${TAG}.txt"; ERR="$OUT/codex_${TAG}.err"

sz=$(wc -c < "$BRIEF")
echo "brief bytes: $sz"
[ "$sz" -gt 30000 ] && { echo "*** above the argv cap -- use the pointer form"; exit 9; }

cd "$PROJ" || exit 9
"$CODEX" exec --sandbox read-only --skip-git-repo-check -m gpt-6-astra \
    -c model_reasoning_effort="max" "$(cat "$BRIEF")" > "$TXT" 2> "$ERR" < /dev/null
rc=$?

echo "codex rc=$rc   stdout=$(wc -c < "$TXT") b   stderr=$(wc -c < "$ERR") b"

#  CONTENT CHECK.  Verify by content, never by size -- but NOT by grepping stderr freely.
#
#  *** MEASURED 2026-09-07, on the run that installed this file: codex STREAMS THE SOURCE IT READS
#  into stderr, so a bare wall-grep over stderr matches any file containing the words.  It reported
#  `wall: 3` on a healthy run, and all three hits were THIS PROJECT'S OWN LEDGER TEXT ABOUT SEAT
#  WALLS -- one of them the line "whose quotation of the pattern MATCHES".  The carrier already
#  names this: quoting a machine-read marker re-arms the tool that reads it. ***
#
#  So: codex's OWN diagnostics are `ERROR: ...` at line start.  Anchor every stderr test on that.
#  stdout is the seat's answer and may be grepped freely.
CXERR=$(grep '^ERROR:' "$ERR" 2>/dev/null)
refus=$(printf '%s' "$CXERR" | grep -ic 'flagged for possible cybersecurity\|cannot help with\|can.t help with\|I won.t help')
wall=$(printf '%s%s' "$CXERR" "$(cat "$TXT" 2>/dev/null)" | grep -ic 'usage limit\|quota\|rate limit\|not authenticated')
verd=$(grep -ic 'VERDICT' "$TXT" 2>/dev/null)
body=$(wc -c < "$TXT")

echo "  verdict-in-stdout: $verd   refusal(ERROR: lines): $refus   wall(ERROR: + stdout): $wall"

if [ "$refus" -gt 0 ]; then
    echo "  *** SEAT REFUSED (content filter).  The answer is LOST, whatever the token count says."
    grep -m2 -i 'flagged for possible cybersecurity' "$ERR" | sed 's/^/    /'
    echo "  *** ROUTE THIS BRIEF TO GROK -- the carrier records that path as working."
    exit 7
fi
if [ "$wall" -gt 0 ]; then echo "  *** SEAT WALLED."; exit 8; fi
if [ "$body" -eq 0 ]; then echo "  *** EMPTY STDOUT with no refusal/wall text -- seat down, cause NOT established."; exit 6; fi
if [ "$rc" -ne 0 ];  then echo "  *** codex exited $rc -- NOT a clean run."; exit "$rc"; fi
echo "  seat answered."
