#!/usr/bin/env bash
# panel.sh -- convene the multi-LLM review panel on a brief, in one command.
#
# Fires the five scriptable seats CONCURRENTLY on a brief file, waits, and
# verifies each actually answered (the "246 KB file that was only the echoed
# prompt" trap is real -- see CLAUDE.md). The sixth seat, Claude Opus 5, is
# NOT scriptable from here: launch it with the Agent tool, model "opus". This
# script prints that reminder.
#
#   Usage:  ./panel.sh <brief_file> [out_dir]
#           ./panel.sh _scratchpad/r101_brief.md
#
# Run from Windows git-bash (the CLI seats are Windows binaries and the Ollama
# API lives on the Windows host; WSL cannot reach either). Every task, research
# task, and review gets a panel: pass 1 on the design brief BEFORE any edit,
# pass 2 on the actual diff AFTER. Resolve disagreements EMPIRICALLY (instrument
# and boot), never by vote -- the majority has been wrong on mechanism many times.
#
# DIFF-REVIEW PASSES: the CLI seats (Codex, agy, Kimi) and Opus read the repo
# directly, so a brief that POINTS at file paths works for them. The three
# Ollama cloud seats CANNOT read files -- they see only the prompt text. So for
# a pass-2 diff review, pass a brief that INLINES the diff (e.g.
# `cat brief.md the.diff > brief_inline.md`) or they review only the
# description. MiniMax3 in particular will emit read_file tool-calls and produce
# nothing if the diff is not inlined (observed 2026-08-10).
set -u

#  PROJ is the PROJECT ROOT.  It used to equal this script's directory,
#  which stopped being true when the harness moved into GXEMUL-SEC/tools/.
TOOLS="$(cd "$(dirname "$0")" && pwd)"
PROJ="${GXROOT:-$(cd "$TOOLS/.." && cd .. && pwd)}"
BRIEF="${1:?usage: panel.sh <brief_file> [out_dir]}"
[ -f "$BRIEF" ] || { echo "no such brief: $BRIEF" >&2; exit 1; }
OUT="${2:-$PROJ/_scratchpad/panel_$(date +%Y%m%d_%H%M%S)}"
mkdir -p "$OUT"
BRIEF_ABS="$(cd "$(dirname "$BRIEF")" && pwd)/$(basename "$BRIEF")"

# pkbrief (2026-08-15): the three Ollama seats are PACKET-FED and stall on a brief that
# contains file-reading instructions for the other seat class -- measured three times, the
# same 90-150 byte signature.  If a sibling <brief>.packet.md exists, THEY get that file
# instead.  Proof of the mechanism: the same seat answered 6,749 bytes on a packet-only
# brief minutes after stalling at 90 bytes on the mixed one.
PACKET_BRIEF="$BRIEF_ABS"
if [ -f "${BRIEF_ABS%.md}.packet.md" ]; then
    PACKET_BRIEF="${BRIEF_ABS%.md}.packet.md"
    echo "packet brief for the Ollama seats: $PACKET_BRIEF"
fi

#  ---------------------------------------------------------------------------
#  *** A SEAT MUST NOT RUN A GATE, AND ONE OF THEM WILL TRY. ***
#
#  Measured 2026-08-17: the agy seat, given a diff-review brief, decided to run
#  gate_offline.sh itself, backgrounded it, and then spun -- "I am waiting for
#  gate_offline.sh to complete", eleven times -- until its own print timeout killed
#  it at 657 bytes.  A SEAT FAILURE with no review in it.
#
#  Two harms, and the second is worse than the lost seat:
#    * a gate takes minutes, longer than a seat's response budget, so the seat
#      deadlocks itself and returns nothing;
#    * it ran CONCURRENTLY with the operator's own gate 2 in the SAME $LOGDIR, which
#      is the one thing this harness cannot survive.  The operator's committed
#      "PASS (222 checks)" had been read from a log directory another process was
#      writing.  Re-run alone with an isolated LOGDIR it was identical -- so the claim
#      held, BY LUCK RATHER THAN BY PROCESS, which is not a thing to leave in place.
#
#  So every seat gets this appended, in a DERIVED copy.  The caller's brief is never
#  modified: mutating an input to say something about it is its own bad habit, and a
#  brief the operator can no longer diff against what they wrote is worse than a lost
#  seat.  Briefs already inline their measurements precisely so no seat needs to run
#  anything; this says so out loud, because a seat that CAN run a gate eventually will.
SEATRULE_TXT='

## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.'
_derive() {   # $1 = source brief, $2 = destination
    cp "$1" "$2" && printf '%s\n' "$SEATRULE_TXT" >> "$2"
}
_derive "$BRIEF_ABS"   "$OUT/brief_sent.md"        && BRIEF_ABS="$OUT/brief_sent.md"
_derive "$PACKET_BRIEF" "$OUT/brief_sent.packet.md" && PACKET_BRIEF="$OUT/brief_sent.packet.md"
BRIEF="$BRIEF_ABS"
#  The derived copies live in the panel dir beside the answers, so what each seat was
#  actually sent is recoverable months later -- which the original brief alone is not,
#  since this rule is appended rather than authored.

# --- seat configuration (edit here, not in the body) -------------------------
CODEX="$HOME/AppData/Local/Programs/OpenAI/Codex/bin/codex"
AGY="$HOME/AppData/Local/agy/bin/agy"
KIMI="$HOME/.kimi-code/bin/kimi"
GROK="$HOME/.grok/bin/grok.exe"
GROK_MODEL="grok-4.6"       # `grok models` lists exactly one model today, and
GROK_EFFORT="xhigh"         # grok-4.6 is both it and the default. Re-check after
                            # any CLI upgrade -- a wrong ID is a SEAT FAILURE.
                            #
                            # xhigh set 2026-08-13 by user directive, and VERIFIED
                            # to be a real tier rather than assumed: passing a
                            # deliberately bogus value makes the CLI name its own
                            # list -- "use one of: xhigh, high, medium, low" -- so
                            # the flag IS validated and xhigh is the top of it.
                            # (That discriminator matters: if a bad value were
                            # silently ignored, acceptance would prove nothing and
                            # the seat would quietly run at the default, which is
                            # exactly the trap the agy seat was in.)
                            # NOTE a bad effort value EXITS 0 while printing an
                            # error, so it cannot be caught by exit status -- it
                            # shows up as a tiny file, which the seat check below
                            # reports as a non-answer.
CODEX_EFFORT="xhigh"        # the user's intent is "ultra"; xhigh is the highest
                            # value the CLI reliably accepts (proven this repo).
AGY_MODEL="gemini-3.7-flash-high"   # user directive 2026-08-13: agy 3.7, high effort.
AGY_EFFORT="high"           # BOTH are passed on purpose. `agy models` lists the
                            # effort tier baked into the model name (-high/-medium/
                            # -low) AND the CLI has a separate --effort flag, so
                            # naming only one leaves the other at its default.
                            # Until now this script passed NEITHER while its own
                            # banner printed "agy(high)" -- the label was an
                            # overclaim, which is the class of defect this project
                            # treats as a real one. Health-tested before wiring in:
                            #   agy --model gemini-3.7-flash-high --effort high \
                            #       --print "..."   ->  answered.
                            # `agy models` is the authority on valid names; a wrong
                            # one is a SEAT FAILURE, so re-check after any upgrade.
OLLAMA1="glm-5.2:cloud"
OLLAMA2="deepseek-v4-pro:cloud"   # DeepSeek is BACK: v3.2 was retired 2026-07-15
                                  # but v4-pro is live (verified answering). NOTE
                                  # the exact tag -- "deepseek-v4:cloud" does NOT
                                  # resolve, only "-pro".
OLLAMA3="minimax-m3:cloud"        # all three are THINKING models; send no
                                  # num_predict cap (panel_ollama.py doesn't) or
                                  # the budget is eaten by hidden reasoning and
                                  # the response comes back empty.
                                  # Recheck tags: curl -s localhost:11434/api/tags

# argv on Windows caps near 32 KB; the "$(cat brief)" seats fail above it.
BSZ=$(wc -c < "$BRIEF")
if [ "$BSZ" -gt 30000 ]; then
    echo "WARNING: brief is ${BSZ} bytes (>30KB). Codex/Kimi take it on argv and"
    echo "         may fail with 'Argument list too long'. Trim, or point those"
    echo "         seats at the file path instead of piping its contents."
fi

echo "panel: brief=$BRIEF  out=$OUT"
#  Report what is ACTUALLY passed, not a hardcoded label. The old line said
#  "agy(high)" while passing no model and no effort at all.
#  ---------------------------------------------------------------------------
#  OLLAMA PREFLIGHT.  Three of the nine seats live behind one local server, so if
#  that server is down ALL THREE fail together -- and they fail with a 155-byte
#  ConnectionRefusedError file each, which looks exactly like three dead seats.
#
#  Measured 2026-08-16: the server was not running, three seats "failed", and the
#  cause took a health test to find because the seat check reports SUSPECT on file
#  SIZE and cannot tell a refused connection from a quota wall.  A one-line probe
#  distinguishes "the roster is short" from "one process is not running", which are
#  different problems with different fixes and must not render the same.
#
#  Deliberately a WARNING, not an abort: the six non-Ollama seats are still worth
#  firing, and the seat check will record the three as failures by name.  What this
#  buys is that the REASON is on screen before the panel runs, not after.
if ! curl -s --max-time 5 http://localhost:11434/api/tags > /dev/null 2>&1; then
	echo "*** OLLAMA IS NOT ANSWERING on localhost:11434 -- glm, deepseek and minimax"
	echo "*** will all fail together with ConnectionRefused, which is NOT three seat"
	echo "*** failures, it is one dead server.  Start it and re-fire those three:"
	echo "***     ollama serve      (or: Start-Process ollama -ArgumentList serve)"
	echo "***     python panel_ollama.py <model> <out.txt> <packet>"
	echo
fi

#  ---------------------------------------------------------------------------
#  *** A SEAT MUST NOT RUN A GATE, AND ONE OF THEM WILL TRY. ***
#
#  Measured 2026-08-17: the agy seat, given a diff-review brief, decided to run
#  `gate_offline.sh` itself, backgrounded it, and then spun -- "I am waiting for
#  gate_offline.sh to complete" eleven times -- until its own print timeout killed
#  it at 657 bytes.  A SEAT FAILURE with no review in it.
#
#  Two harms, and the second is worse than the lost seat:
#    * gate 2 takes minutes, longer than a seat's patience, so the seat deadlocks;
#    * it ran CONCURRENTLY with the operator's own gate 2 in the SAME $LOGDIR, which
#      is the one thing this harness cannot survive.  The operator's committed
#      "PASS (222 checks)" was read from a directory another process was writing.
#      Re-run alone it was identical -- so the claim held, BY LUCK, NOT PROCESS.
#
#  Hence the line below, in every brief this script sends.  Briefs already inline the
#  measurements precisely so no seat needs to run anything; this says it out loud,
#  because a seat that CAN run a gate eventually will.
echo "seats: codex($CODEX_EFFORT) agy($AGY_MODEL/$AGY_EFFORT) kimi3 grok($GROK_MODEL/$GROK_EFFORT) ollama($OLLAMA1) ollama($OLLAMA2) ollama($OLLAMA3) | + Opus via Agent tool"

# --- launch the five scriptable seats concurrently ---------------------------
AGY_PROMPT="Read $BRIEF_ABS and review it adversarially exactly as its own \
Questions/Review-asks section directs. Verify every cited claim against the \
source under $PROJ/GXEMUL-SEC with file:line evidence. End with GO / NO-GO / \
GO-WITH-CHANGES."

"$CODEX" exec --sandbox read-only --skip-git-repo-check -m gpt-5.6-sol \
    -c model_reasoning_effort="$CODEX_EFFORT" "$(cat "$BRIEF")" \
    </dev/null > "$OUT/codex.txt" 2>&1 &
P_CODEX=$!

"$AGY" --dangerously-skip-permissions --add-dir "$PROJ" --print-timeout 30m \
    --model "$AGY_MODEL" --effort "$AGY_EFFORT" \
    --print "$AGY_PROMPT" > "$OUT/agy.txt" 2>&1 &
P_AGY=$!

"$KIMI" -p "$(cat "$BRIEF")" -m kimi-code/k3 > "$OUT/kimi.txt" 2>&1 &
P_KIMI=$!

#  GROK 4.6 -- added 2026-08-13 by user directive. Note what it does DIFFERENTLY
#  from every other CLI seat, because it is the reason this seat is wired the way
#  it is: --prompt-file takes the brief FROM A FILE, so the ~32 KB Windows argv
#  cap does not apply. Codex died today with "Argument list too long" on a 36 KB
#  brief passed as an argument; this seat cannot hit that. It is therefore the
#  seat to trust with a big inlined diff.
#  --permission-mode plan keeps it READ-ONLY (verified: it read a repo file and
#  answered correctly without prompting or hanging), and --cwd lets it consult
#  the source the way Codex and agy do, rather than only the brief.
#  `grok models` is the authority on model IDs; today it lists exactly one.
"$GROK" --prompt-file "$BRIEF_ABS" -m "$GROK_MODEL" --effort "$GROK_EFFORT" \
    --permission-mode plan --cwd "$PROJ" \
    </dev/null > "$OUT/grok.txt" 2>&1 &
P_GROK=$!

python "$TOOLS/panel_ollama.py" "$OLLAMA1" "$OUT/ollama_glm.txt" "$PACKET_BRIEF" \
    > "$OUT/ollama_glm.err" 2>&1 &
P_O1=$!

python "$TOOLS/panel_ollama.py" "$OLLAMA2" "$OUT/ollama_deepseek.txt" "$PACKET_BRIEF" \
    > "$OUT/ollama_deepseek.err" 2>&1 &
P_O2=$!

python "$TOOLS/panel_ollama.py" "$OLLAMA3" "$OUT/ollama_minimax.txt" "$PACKET_BRIEF" \
    > "$OUT/ollama_minimax.err" 2>&1 &
P_O3=$!

echo "launched: codex=$P_CODEX agy=$P_AGY kimi=$P_KIMI grok=$P_GROK ollama1=$P_O1 ollama2=$P_O2 ollama3=$P_O3"
echo "waiting for the seven scriptable seats..."
wait $P_CODEX $P_AGY $P_KIMI $P_GROK $P_O1 $P_O2 $P_O3

# --- verify each seat produced a real answer ---------------------------------
# A seat "answered" if its file is non-trivial AND is not merely the brief
# echoed back. Heuristic only -- always eyeball the flagged ones.
#  ALL FOUR EXITS USE say(), and the first version of this change got that wrong
#  in the most embarrassing possible direction: only the HEALTHY path was
#  converted, so SEATS.txt recorded every seat that answered and silently dropped
#  every seat that did not.  A file that keeps the good news and loses the bad is
#  worse than no file, because it reads as a complete roster.  Caught by testing
#  the change against a fake grok.txt of exactly the 523 bytes the real one wrote.
check() {   # name file
    local name="$1" f="$2" sz vibe head
    if [ ! -s "$f" ]; then say "  $name: MISSING/EMPTY"; return; fi
    sz=$(wc -c < "$f")
    #  Error sentinels are only meaningful at the START of the file or as our
    #  own OLLAMA_SEAT_ERROR marker -- NOT anywhere in the text, or a review
    #  that merely quotes "was retired" or "usage:" gets mis-flagged (it did,
    #  on the first live run). Anchor to the first 400 bytes.
    head=$(head -c 400 "$f")
    if printf '%s' "$head" | grep -qiE "OLLAMA_SEAT_ERROR|error: model|was retired|Argument list too long"; then
        say "  $name: ERROR (${sz}b) -- $(printf '%s' "$head" | grep -ioE 'OLLAMA_SEAT_ERROR.*|was retired[^"]*|Argument list too long' | head -1)"
        return
    fi
    if [ "$sz" -lt 800 ]; then say "  $name: SUSPECT (only ${sz}b -- may be thinking-only or a tool-call misfire)"; return; fi
    # ASSESS/REAL/NOT-A-BUG etc. are the assessment-phase verdict tokens; without
    # them two correct packet answers were false-flagged CHECK on 2026-08-15.
    if grep -qiE "GO-WITH-CHANGES|NO-GO|\bGO\b|verdict|refut|confirm|ASSESS [a-z0-9#()]+:|NOT-A-BUG|ALREADY-FIXED|PARTLY-FIXED|\bREAL\b|\bUNKNOWN\b" "$f"; then
        vibe="answered"
    else
        vibe="CHECK (no verdict token)"
    fi
    say "  $name: ${sz}b  $vibe"
}
#  THE SEAT VERDICT MUST SURVIVE THE LAUNCH MODE, and until 2026-08-16 it did not.
#  Everything below went to stdout ONLY.  Launch this script backgrounded from a
#  harness -- `nohup ./panel.sh brief &` -- and the waiter is killed with the
#  launching shell: the seat check never prints, the panel directory fills with
#  answers, and the run looks COMPLETE.
#
#  *** THE ORIGINAL DIAGNOSIS HERE WAS WRONG AND IS CORRECTED IN PLACE. ***  It said
#  backgrounding "truncates at least the grok seat", on the evidence of two 523- and
#  265-byte files.  Those files FINISHED -- 10,226 and 12,579 bytes, real verdicts,
#  timestamps 02:53:27 and 02:57:00 -- and the foreground "control" completed at
#  02:54:34, BETWEEN them.  I read partial files at ~02:4x and called them truncated.
#  What backgrounding actually kills is THIS SCRIPT, the waiter; the seats run on
#  unattended.  A control run does not license a causal claim when the thing it
#  controls for is TIME, and the file mtimes would have said so in one command.
#
#  The fix below matters MORE under the corrected story, not less: with the waiter
#  dead nothing reports the seats' state at all, so a still-being-written file is
#  indistinguishable from a finished one.  That is exactly what a persisted verdict
#  and a PANEL_COMPLETE sentinel resolve.
#
#  This is the same defect as the `tail -N` note further down, one level out: a
#  verdict that lives only in a stream is a verdict you can lose by accident.  So
#  every load-bearing line is ALSO written to $OUT/SEATS.txt, which sits next to
#  the answers it grades and is the first thing a fresh session should read.
SEATFILE="$OUT/SEATS.txt"
: > "$SEATFILE"
say() { printf '%s
' "$*"; printf '%s
' "$*" >> "$SEATFILE"; }
say "---- seat check ($OUT) ----"
check "codex    " "$OUT/codex.txt"
check "agy      " "$OUT/agy.txt"
check "kimi     " "$OUT/kimi.txt"
check "grok     " "$OUT/grok.txt"
check "glm      " "$OUT/ollama_glm.txt"
check "deepseek " "$OUT/ollama_deepseek.txt"
check "minimax  " "$OUT/ollama_minimax.txt"
say "---------------------------"
echo "SEATS 7 AND 8 -- launch BOTH now via the Agent tool, in the same turn:"
echo "  Opus 5  (model: \"opus\")   reads the repo directly; the seat most likely"
echo "                             to compile and measure, and it has overturned"
echo "                             confident readings -- including the lead's."
echo "  Fable 5 (model: \"fable\")  an independent review seat, separate from the"
echo "                             main loop's own adjudicating role."
echo "Neither can be started from this script. There is no opus/fable CLI."
echo
echo "If the pass reviews a DIFF, inline the diff into the brief first:"
echo "  cat brief.md the.diff > brief_inline.md   -- the three cloud seats"
echo "cannot read files and will emit file-read tool-call syntax instead."
echo
echo "A seat measuring against build/ races this loop's own rebuilds: a"
echo "contaminated run shows rows as DEAD/None, not as wrong values. Tell"
echo "measuring seats to copy the tree first, or to hold off while it builds."
echo
echo "Then: collect all eight, resolve splits by MEASUREMENT not vote, and record"
echo "any residual/dissent into GXEMUL-SEC/OUTSTANDING_BUGS.md at round end."
echo

#  One-line recap, printed LAST on purpose. The detailed seat check above is
#  followed by ~18 lines of reminder text, so a caller that pipes this script
#  through `tail -N` for a modest N loses the check entirely -- which happened
#  on three separate rounds before anyone noticed the habit. Whatever survives
#  the tail, this line does.
#  DERIVE the denominator from the seat list. It was hardcoded "6" and stayed 6
#  when a seventh seat was added, so the very run that proved grok working printed
#  "1/6 ... no answer from: ... grok". A count nobody derives is a count that goes
#  stale the first time the thing it counts changes -- the same defect as the
#  banner that printed "agy(high)" while passing no flags.
ok=0; miss=""; total=0; rated=""
for s in codex:codex agy:agy kimi:kimi grok:grok glm:ollama_glm \
         deepseek:ollama_deepseek minimax:ollama_minimax; do
    n=${s%%:*}; f="$OUT/${s##*:}.txt"
    total=$((total+1))
    if [ -s "$f" ] && [ "$(wc -c < "$f")" -ge 800 ]; then
        ok=$((ok+1))
    else
        miss="$miss $n"
        #  DISTINGUISH AN OPERATIONAL FAILURE FROM A REAL NON-ANSWER, for ANY
        #  seat rather than one vendor's spelling. Four have now died this way and
        #  each announced it differently:
        #     Ollama x3  HTTP 429, when two panels are fired within ~10 minutes
        #     Kimi 3     HTTP 403, usage limit for the billing cycle
        #     Fable 5    "You've reached your Fable 5 limit"
        #     Codex      "Argument list too long" (argv cap, not a quota)
        #  Grok 4.6 is new and free as of 2026-08-13 with NO published limit and no
        #  `usage` subcommand to query -- so its failure text is UNKNOWN and this
        #  pattern is deliberately broad. A seat that hit a wall did NOT consider
        #  the brief and had nothing to say; counting it as agreement is the exact
        #  mistake this block exists to prevent.
        #  "unknown effort level"/"unknown model" are MISCONFIGURATION, not a wall,
        #  but they belong here for the same reason: a seat that never ran did not
        #  consider the brief. They also exit 0 while printing the error, so exit
        #  status cannot catch them -- only the text can.
        if grep -qsiE "429|too many requests|rate.?limit|quota|usage limit|billing|reached your .*limit|Argument list too long|401|403|unknown effort level|unknown model|no such model" "$f"; then
            rated="$rated $n"
        fi
    fi
done
say "SEATS: $ok/$total scriptable produced output${miss:+ -- no answer from:$miss}"
[ -n "$rated" ] && say "       *** RATE-LIMITED (HTTP 429), NOT a considered non-answer:$rated"
[ -n "$rated" ] && say "       *** re-run those seats before treating this panel as complete."
say "       (a non-answering seat is a SEAT FAILURE, never counted as agreement)"

#  A FOREGROUND RUN IS PART OF THE CONTRACT.  See the SEATFILE comment above: a
#  backgrounded launch loses the waiter and truncates at least the grok seat.  If
#  this line is not in $OUT/SEATS.txt, the script did not finish and the panel is
#  NOT complete no matter how large the answer files are.
say "PANEL_COMPLETE $(date '+%Y-%m-%d %H:%M:%S')"
