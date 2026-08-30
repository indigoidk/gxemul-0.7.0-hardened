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
#  The three cloud seats are proxied through a LOCAL daemon, so the binary matters
#  even though the models are remote.  See the pre-flight below.
OLLAMA_BIN="${OLLAMA_BIN:-$HOME/AppData/Local/Programs/Ollama/ollama.exe}"
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
                            # OLLAMA1 MIGRATED 2026-08-28 by owner directive:
                            # glm-5.2:cloud -> glm-5.3-flash:cloud.  VERIFIED
                            # BEFORE THE EDIT, not after: `ollama pull` succeeded
                            # for this tag and FAILED ("file does not exist") for
                            # the near-miss `glm-5.3flash:cloud`, and an
                            # api/generate liveness call returned its nonce
                            # exactly (done_reason=stop, 25 bytes, no burn).
                            # `curl -s localhost:11434/api/tags` is the authority;
                            # a wrong name is a SEAT FAILURE.  Note the SEAT is
                            # keyed by FILENAME (ollama_glm.txt) throughout the
                            # harness, so check_seats_read.py and seat_verdicts.py
                            # need no edit -- that is the kimi-substitute lesson
                            # applied: record a seat by its transport, not its tag.
#  *** MIGRATED AGAIN 2026-08-29 BY OWNER DIRECTIVE: glm-5.3-flash:cloud ->
#  glm-5.3:cloud. ***  Verified BEFORE the edit, same discipline as the 08-28 move:
#  `ollama pull glm-5.3:cloud` succeeded, and an api/generate call returned the
#  liveness token EXACTLY -- done_reason=stop, eval_count=52, no thinking-burn.
#  The seat is keyed by FILENAME (ollama_glm.txt) everywhere else, so
#  check_seats_read.py and seat_verdicts.py need no edit; record a seat by its
#  transport, not its tag.
OLLAMA1="glm-5.3:cloud"
OLLAMA2="deepseek-v4-pro:cloud"   # DeepSeek is BACK: v3.2 was retired 2026-07-15
                                  # but v4-pro is live (verified answering). NOTE
                                  # the exact tag -- "deepseek-v4:cloud" does NOT
                                  # resolve, only "-pro".
                                  # 2026-08-21 owner directive: the upstream alias
                                  # moved preview -> release. `ollama pull
                                  # deepseek-v4-pro:cloud` refreshed it; the wire
                                  # tag here is UNCHANGED, and the health test
                                  # returned its token with model reported as the
                                  # release build. Re-pull after upstream bumps;
                                  # the tag in this file only names the alias.
OLLAMA3="minimax-m3:cloud"        # all FOUR are THINKING models; send no
                                  # num_predict cap (panel_ollama.py doesn't) or
                                  # the budget is eaten by hidden reasoning and
                                  # the response comes back empty.
                                  # Recheck tags: curl -s localhost:11434/api/tags

#  *** OLLAMA4 ADDED 2026-08-25: THE kimi SUBSTITUTE TRANSPORT. ***  The kimi CLI
#  is 403-walled on its billing cycle, and for several panels this script fired ONLY
#  the CLI -- so every one of those panels ran a seat short while `kimi-k3:cloud`
#  sat LIVE on the same daemon already serving the other three.  Three earlier panel
#  dirs hold a healthy hand-fired ollama_kimi.txt, so the substitute was known to work
#  and simply stopped being used.  A walled transport is not a dead seat: check
#  `curl -s localhost:11434/api/tags` for another road before recording any seat down.
#
#  NOTE this is the kimi SUBSTITUTE, never "the kimi seat".  Record it by transport --
#  `kimi-k3:cloud` -- so a reader can tell which road answered.
#  *** WITHDRAWN 2026-08-29 BY OWNER DIRECTIVE: THE KIMI CLI IS BACK, SO THE SEAT
#  RETURNS TO ITS OWN TRANSPORT. ***  Its 403 was a WEEKLY (7-day) limit, not a
#  billing cycle, and it has cleared -- tested by a real invocation that returned
#  the liveness token, never by reasoning about the date.
#
#  THIS IS A CAPABILITY GAIN, not a tidy-up.  The CLI is FILE-READING; the
#  substitute went through panel_ollama.py and was PACKET-FED.  The doctrine
#  classifies a seat by its TRANSPORT rather than its name, so for the whole time
#  the substitute stood in, "the kimi seat" could not read the repo and any answer
#  crediting it with a repo fact was the conflation the doctrine forbids.
#
#  KEPT, NOT DELETED, because the substitute is the documented recovery path: if the
#  CLI walls again, set OLLAMA4 back to kimi-k3:cloud and the seat is COVERED rather
#  than lost.  That is the sixth seat-failure class -- one transport walled while
#  another is live -- and the whole point is that it is one line away.
OLLAMA4=""

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
O4_BANNER="ollama($OLLAMA4)"
[ -z "$OLLAMA4" ] && O4_BANNER="kimi-substitute:WITHDRAWN (CLI is the seat)"
echo "seats: codex($CODEX_EFFORT) agy($AGY_MODEL/$AGY_EFFORT) kimi3 grok($GROK_MODEL/$GROK_EFFORT) ollama($OLLAMA1) ollama($OLLAMA2) ollama($OLLAMA3) $O4_BANNER | + Opus/Fable via Agent tool"

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

#  *** PRE-FLIGHT THE OLLAMA DAEMON.  Added 2026-08-22, after all THREE cloud seats
#  came back in 155 bytes each -- ConnectionRefusedError(10061) on localhost:11434,
#  because the daemon simply was not running.  Three seats lost in one firing.
#
#  This is a class the seat check could not name.  A quota WALL is the seat refusing
#  and you wait it out; a refused CONNECTION is the transport being absent and one
#  command fixes it.  Reporting the second as the first silently gives up three seats
#  that were available the whole time -- and the panel still prints a tidy summary,
#  which is the "a green row means nothing" shape.
#
#  Cheaper to start it than to lose the panel, so try; if it still will not come up,
#  say so LOUDLY here rather than leaving it to be read out of three error files.
if ! curl -s -m 4 http://localhost:11434/api/tags >/dev/null 2>&1; then
    echo "*** ollama daemon is DOWN (localhost:11434 refused) -- starting it ***"
    ( "$OLLAMA_BIN" serve >/dev/null 2>&1 & ) 2>/dev/null
    for _i in 1 2 3 4 5 6 7 8; do
        sleep 1
        curl -s -m 4 http://localhost:11434/api/tags >/dev/null 2>&1 && break
    done
    if curl -s -m 4 http://localhost:11434/api/tags >/dev/null 2>&1; then
        echo "*** ollama came up; the three cloud seats will be fired normally ***"
    else
        echo "*** !!! OLLAMA STILL DOWN -- THREE SEATS WILL FAIL OPERATIONALLY. !!!"
        echo "*** !!! That is NOT agreement.  Start it by hand and re-fire those"
        echo "*** !!! three seats into THIS panel dir before reading the result:"
        echo "*** !!!   $OLLAMA_BIN serve &"
        echo "*** !!!   python $TOOLS/panel_ollama.py <model> $OUT/<seat>.txt $PACKET_BRIEF"
    fi
fi

python "$TOOLS/panel_ollama.py" "$OLLAMA1" "$OUT/ollama_glm.txt" "$PACKET_BRIEF" \
    > "$OUT/ollama_glm.err" 2>&1 &
P_O1=$!

python "$TOOLS/panel_ollama.py" "$OLLAMA2" "$OUT/ollama_deepseek.txt" "$PACKET_BRIEF" \
    > "$OUT/ollama_deepseek.err" 2>&1 &
P_O2=$!

python "$TOOLS/panel_ollama.py" "$OLLAMA3" "$OUT/ollama_minimax.txt" "$PACKET_BRIEF" \
    > "$OUT/ollama_minimax.err" 2>&1 &
P_O3=$!

#  *** CONDITIONAL, AND THE CONDITION IS LOAD-BEARING. ***  With OLLAMA4 blank an
#  unguarded launch still runs panel_ollama.py with an EMPTY model name: it writes an
#  error file and produces a seat that LOOKS fired.  That is worse than a missing seat,
#  because a phantom answers the seat check.  When the kimi CLI walls again, set
#  OLLAMA4 back to kimi-k3:cloud and this fires exactly as before.
P_O4=""
if [ -n "$OLLAMA4" ]; then
    python "$TOOLS/panel_ollama.py" "$OLLAMA4" "$OUT/ollama_kimi.txt" "$PACKET_BRIEF" \
        > "$OUT/ollama_kimi.err" 2>&1 &
    P_O4=$!
fi

echo "launched: codex=$P_CODEX agy=$P_AGY kimi=$P_KIMI grok=$P_GROK ollama1=$P_O1 ollama2=$P_O2 ollama3=$P_O3 ollama4=${P_O4:-withdrawn}"
NSEATS=8; [ -z "$P_O4" ] && NSEATS=7
echo "waiting for the $NSEATS scriptable seats..."
wait $P_CODEX $P_AGY $P_KIMI $P_GROK $P_O1 $P_O2 $P_O3 $P_O4

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
    #  *** THE ECHO TEST, WHICH THIS FUNCTION'S OWN COMMENT PROMISED SINCE THE FIRST
    #  VERSION AND WHICH DID NOT EXIST.  Measured 2026-08-17: codex printed its banner,
    #  echoed the 9,375-byte brief, then ended with "ERROR: You've hit your usage limit
    #  ... try again at Aug 22nd".  It produced NO REVIEW and was scored "10063b
    #  answered".  BSZ was computed at the top of the script for exactly this test and
    #  then never used -- a documented check that cannot fail, which is worse than no
    #  check because it reassures.
    #
    #  The verdict-token heuristic below could not save it either, and the reason is
    #  worth keeping: THE ECHOED BRIEF CONTAINS THE TOKENS, because a brief that tells
    #  seats to open with "VERDICT:" necessarily has the word "VERDICT" in it.  Every
    #  future brief will too.  So payload size, not content, is the discriminator.
    #  *** ONLY APPLY THE PAYLOAD TEST TO A FILE THAT ACTUALLY CONTAINS THE BRIEF. ***
    #  The first version of this test did not check, and it was WORSE THAN THE BUG IT FIXED.
    #  `sz - BSZ` is negative for any seat that does not echo -- grok reads the brief from a
    #  file, the Ollama seats return only their answer -- so every real answer SHORTER than
    #  the brief was declared ECHO-ONLY. Measured on the very next panel: four genuine
    #  answers mislabelled, deepseek's and glm's verdicts among them. One false negative
    #  traded for four false positives.
    #
    #  It survived four negative controls because ALL FOUR USED THE SAME LARGE BRIEF, whose
    #  real answers all happened to exceed it. A control suite that varies only the seat and
    #  never the brief cannot see a bug that lives in the brief-to-answer RATIO.
    #
    #  The discriminator is possession, not arithmetic: an echoing seat reproduces the brief
    #  verbatim, so look for a distinctive line from it.
    local marker echoed=""
    marker=$(awk 'length($0) > 55 && $0 !~ /^[#*|> -]/ { print; exit }' "$BRIEF" 2>/dev/null)
    if [ -n "$marker" ] && grep -qF "$marker" "$f" 2>/dev/null; then
        echoed="yes"
    fi
    local payload=$((sz - BSZ))
    if [ -n "$echoed" ] && [ "$payload" -lt 800 ]; then
        say "  $name: ECHO-ONLY (${sz}b = brief ${BSZ}b + ${payload}b) -- NOT A REVIEW"
        #  Name the wall if the file says what it was, so the operator does not have to
        #  guess whether this was a quota, an auth failure or a crash.
        local why
        why=$(grep -ioE "You've hit your usage limit[^.]*|usage limit[^.]*|quota[^.]*|rate.?limit[^.]*|reached your [a-z0-9 ]*limit" "$f" | head -1)
        [ -n "$why" ] && say "        wall: $why"
        return
    fi
    #  *** A SEAT CAN ANSWER AT LENGTH AND THEN HIT THE WALL, and until 2026-08-23
    #  nothing here saw that. ***  The branch above only catches the ECHO-ONLY shape --
    #  brief echoed, tiny payload, the codex signature.  Kimi walled with **36 KB of
    #  real content and 98% novel lines**, ending mid-sentence with a 403 usage-limit
    #  notice.  Payload huge, echo absent: invisible to every test above, and the panel
    #  printed it as a healthy answer.  The owner spotted it only because the seat
    #  showed as available in their own UI.
    #
    #  The discriminator is POSITION, the same one seat_verdicts.py already uses: a
    #  walled run ENDS with the notice and nothing after it, whereas a live seat that
    #  merely mentions a limit has it mid-reasoning and ends with substance.
    #  *** 402 WAS MISSING AND IT COST A SEAT ON 2026-08-24. ***  grok walled MID-ANSWER
    #  with `API error (status 402 Payment Required): Grok Build usage balance exhausted`
    #  -- which contains NO "usage limit", NO "quota", NO "billing" and NO 403, so every
    #  pattern here missed it and the seat was scored `CHECK (no verdict token)`: a
    #  FORMAT concern, not a wall.  The panel then reported 6/7 answered when it was 5/7.
    #  A seat that did real work (12 model calls, 1.08M tokens) and then hit a paywall is
    #  a WALL, and reading it as a format miss is the seat-failure-as-agreement shape.
    if tail -c 400 "$f" | grep -qiE "usage limit|quota will be refreshed|rate.?limit|\b403\b|\b402\b|payment required|balance exhausted"; then
        say "  $name: ${sz}b  *** WALLED MID-ANSWER -- content then a wall notice ***"
        why=$(tail -c 400 "$f" | grep -ioE "[^.]*(usage limit|quota|payment required|balance exhausted)[^.]*" | head -1)
        [ -n "$why" ] && say "        wall: $why"
        #  *** RE-FIRE ONCE.  A WALL IS A MOMENT, NOT A STATE. ***  Measured
        #  2026-08-23: kimi walled at 23:01 and answered a liveness test an hour later,
        #  across a date boundary.  The carrier says both previously-dead seats were
        #  revived by ACCOUNT-STATE changes "never by a date" -- that half is now
        #  contradicted, though the advice it carries (TEST IT, never assume) is what
        #  caught this.  Cause not established; recovery measured.  One retry costs a
        #  minute and recovers a seat the round would otherwise silently lose.
        #  *** THIS USED TO PRINT "re-firing once ..." AND NOTHING RE-FIRED. ***
        #  Found 2026-08-26 by an audit of the carrier: every caller of this
        #  function is a bare `check "name" "$file"` whose exit status is
        #  discarded, and no seat command is re-invoked anywhere after the seat
        #  check.  The `return 2` below has never had a consumer.
        #
        #  A stale citation misleads a reader who follows it.  THIS printed a
        #  claim of ACTION, to the operator, at the moment a seat was lost -- so
        #  the one person who could re-fire it by hand was told it had already
        #  been done.  That is the failure this file warns about sixty lines up:
        #  "a documented check that cannot fail ... is worse than no check
        #  because it reassures."
        #
        #  The message is now an INSTRUCTION rather than a false report.  Making
        #  the retry automatic is a real improvement and a real behaviour change
        #  to the script every panel runs, so it is FILED with the two negative
        #  controls it owes: prove the retry fires on a walled seat, and prove a
        #  seat that answered is NOT retried.
        say "        A WALL IS A MOMENT, NOT A STATE -- RE-FIRE THIS SEAT ONCE"
        say "        BY HAND before closing the round.  NOT done automatically."
        #  *** SAY WHERE THE COMMAND IS.  The message used to stop at the line
        #  above, leaving the operator to find one of seven differently-shaped
        #  launches 200 lines up in this file -- at the exact moment a seat has
        #  just been lost, which is the worst moment to make someone go looking.
        #
        #  IT POINTS RATHER THAN DUPLICATES.  Copying the invocation into this
        #  message would create a second copy that drifts from the launch above
        #  it, and this project has already carried a FALSE SEAT ROSTER for days
        #  for exactly that reason.  The carrier seat table is the canonical one
        #  and precommit section J holds it byte-identical to its tracked copy,
        #  so a pointer there cannot go stale in silence.
        say "        The invocation is in the seat table in tools/CLAUDE.md;"
        say "        the brief is $BRIEF and the output goes to $f"
        return 2
    fi

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
#  *** ONLY CHECKED IF IT WAS FIRED.  A WITHDRAWN SEAT IS NOT A DOWN SEAT. ***
#  Unguarded, a missing ollama_kimi.txt scores as a seat failure -- which is the
#  deliberately-not-fired / failed conflation the seat ledger refuses.
if [ -n "$OLLAMA4" ]; then
    check "kimi(sub)" "$OUT/ollama_kimi.txt"
else
    say "  kimi(sub)  WITHDRAWN -- the CLI is the kimi seat (owner directive 2026-08-29)."
    say "             Not a failure.  Restore by setting OLLAMA4=kimi-k3:cloud."
fi
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
#  The substitute joins the roster only when it was actually fired, so a withdrawal
#  does not inflate `total` or land in `$miss`.
SEATLIST="codex:codex agy:agy kimi:kimi grok:grok glm:ollama_glm"
SEATLIST="$SEATLIST deepseek:ollama_deepseek minimax:ollama_minimax"
[ -n "$OLLAMA4" ] && SEATLIST="$SEATLIST kimi_sub:ollama_kimi"
for s in $SEATLIST; do
    n=${s%%:*}; f="$OUT/${s##*:}.txt"
    total=$((total+1))
    #  *** THE WALL SCAN RUNS FIRST, FOR EVERY SEAT, AND UNTIL 2026-08-17 IT COULD NOT
    #  RUN AT ALL FOR THE CASE THAT MATTERS.  It lived only in the `else` arm below, so
    #  any file >= 800 bytes was counted OK and never scanned.  Codex then produced a
    #  10,063-byte file that was the echoed 9,375-byte brief plus
    #  "ERROR: You've hit your usage limit" -- the pattern was ALREADY in the regex and
    #  the regex was simply never applied.  A detector behind a size test cannot see the
    #  failure mode where the file is big BECAUSE nothing was reviewed.
    #
    #  A seat that hit a wall did NOT consider the question and must never be counted as
    #  agreement.  So: wall first, size second.
    _wall=""
    if grep -qsiE "429|402|payment required|balance exhausted|too many requests|rate.?limit|quota|usage limit|billing|reached your .*limit|Argument list too long|401|403|unknown effort level|unknown model|no such model" "$f"; then
        #  Guard against a REVIEW that merely discusses quotas (this project's own
        #  briefs do).  A real wall leaves almost no payload: the file is the echoed
        #  brief plus an error line.  Require BOTH the pattern and a thin payload -- and,
        #  as above, only treat the payload arithmetic as meaningful when the file actually
        #  CONTAINS the brief, or a short genuine answer that happens to discuss quotas gets
        #  called a wall on nothing but being shorter than the prompt.
        _mk=$(awk 'length($0) > 55 && $0 !~ /^[#*|> -]/ { print; exit }' "$BRIEF" 2>/dev/null)
        if [ -s "$f" ] && [ -n "$_mk" ] && grep -qF "$_mk" "$f" 2>/dev/null \
           && [ $(( $(wc -c < "$f") - BSZ )) -lt 800 ]; then
            _wall="yes"
        fi
    fi
    if [ -n "$_wall" ]; then
        miss="$miss $n"
        rated="$rated $n"
    elif [ -s "$f" ] && [ "$(wc -c < "$f")" -ge 800 ]; then
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
#  *** DO NOT NAME A STATUS CODE THIS SCRIPT DID NOT OBSERVE. ***  This line read
#  "RATE-LIMITED (HTTP 429)" for every match, and it printed that for a kimi failure
#  whose actual text was "403 You've reached your usage limit for this billing
#  cycle" -- twice, on two different panels.  The disposition was right and the
#  LABEL was wrong, and the carrier draws a sharp line between failure classes that
#  a mis-named status blurs: a WALL you wait out, a REFUSED CONNECTION one command
#  fixes, a MISCONFIGURATION that exits 0 while printing its own error.
[ -n "$rated" ] && say "       *** WALLED / RATE-LIMITED / MISCONFIGURED -- NOT a considered non-answer:$rated"
[ -n "$rated" ] && say "       *** read each seat file for the ACTUAL status; do not assume 429."
[ -n "$rated" ] && say "       *** re-run those seats before treating this panel as complete."

#  A CLI WALL WITH A LIVE SUBSTITUTE IS ONE SEAT ANSWERED, NOT ONE LOST AND ONE
#  GAINED.  Report it explicitly, because the tally above counts TRANSPORTS.
#
#  *** THIS GUARD READ THE WRONG LIST AND SO COULD NOT FAIL.  Measured 2026-08-27 on
#  the #474 panel. ***  It excluded kimi_sub by grepping $rated -- the seats carrying
#  QUOTA/AUTH text.  A substitute that STALLS (346 bytes of "I will read the tree",
#  no error text) never enters $rated at all; it enters $miss.  So the exclusion was
#  unreachable for the commonest substitute failure, and the script printed COVERED
#  two lines after printing "kimi(sub): SUSPECT (only 346b)".
#
#  That is the check-that-cannot-fail shape the carrier names, in its worst form: a
#  claim of COVERAGE asserted at the moment coverage was lost, so the one person who
#  could re-fire the seat was told it had already answered.  $miss is the list that
#  means "did not answer", whatever the reason, which is what this sentence is about.
#  *** AND THE CLI TEST HAD THE SAME DEFECT ONE BRANCH OVER.  Found by a panel seat
#  reviewing the very commit that fixed the substitute side. ***  Both branches keyed
#  the CLI test on $rated -- seats carrying QUOTA text -- so a kimi CLI that fails
#  WITHOUT a recognised wall pattern (a stall, a crash, a refused connection) lands in
#  $miss and NEITHER branch fires.  The seat is genuinely lost and nothing says so.
#
#  That is the identical shape as the substitute bug, mirror-imaged: the fix moved one
#  predicate to $miss and left its sibling on $rated.  **A fix applied to one side of a
#  symmetric pair is half a fix**, and the half left behind is the one nobody re-reads.
#
#  $miss means "did not answer", whatever the reason, which is what both sentences are
#  actually about.
#  The COVERED / LOST pair below is about the SUBSTITUTE, so it only speaks when the
#  substitute is in the roster.  With it withdrawn, a walled CLI is simply a walled
#  seat and the generic wall reporting above already says so.
if [ -z "$OLLAMA4" ] && printf %s "$miss" | grep -qw kimi; then
    say "       NOTE: the kimi CLI is walled and its kimi-k3:cloud substitute is"
    say "             WITHDRAWN, so this seat is LOST rather than covered.  One line"
    say "             restores it: OLLAMA4=kimi-k3:cloud in this script."
elif printf %s "$miss" | grep -qw kimi && [ -s "$OUT/ollama_kimi.txt" ] \
   && ! printf %s "$miss" | grep -qw kimi_sub; then
    say "       NOTE: the kimi CLI is walled but kimi-k3:cloud ANSWERED -- that seat"
    say "             is COVERED by its substitute transport, not lost."
elif printf %s "$miss" | grep -qw kimi && printf %s "$miss" | grep -qw kimi_sub; then
    say "       *** THE KIMI SEAT IS LOST, NOT COVERED: the CLI is walled AND the"
    say "       *** kimi-k3:cloud substitute did not answer either.  Re-fire the"
    say "       *** substitute with an INLINED brief -- a packet-fed seat stalls on"
    say "       *** any instruction to read files, and that stall is not a wall."
fi
say "       (a non-answering seat is a SEAT FAILURE, never counted as agreement)"

#  A FOREGROUND RUN IS PART OF THE CONTRACT.  See the SEATFILE comment above: a
#  backgrounded launch loses the waiter and truncates at least the grok seat.  If
#  this line is not in $OUT/SEATS.txt, the script did not finish and the panel is
#  NOT complete no matter how large the answer files are.
say "PANEL_COMPLETE $(date '+%Y-%m-%d %H:%M:%S')"
