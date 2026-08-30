#!/usr/bin/env bash
# Emits the panel/round reminder as hook JSON. $1 = session | task
# Wired from .claude/settings.local.json for SessionStart and TaskCompleted.
case "${1:-session}" in
session)
  cat <<'JSON'
{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"GXemul hardened fork: the NINE-seat review panel is MANDATORY on every task, research task, and review -- pass 1 on the design brief BEFORE editing, pass 2 on the diff AFTER. Invoke it as `bash GXEMUL-SEC/tools/panel.sh <ABSOLUTE brief path>`, NEVER ./panel.sh -- the session cwd drifts and a relative launch dies silently with zero seats, which looks like a completed run. It fires SEVEN scriptable transports: Codex 5.6-SOL xhigh, agy high, Kimi 3 (the CLI is the seat again since 2026-08-29), Grok 4.6 xhigh, and three Ollama cloud thinking models (glm-5.3:cloud, deepseek-v4-pro:cloud, minimax-m3:cloud -- never send a num_predict cap). Launch two more in the SAME turn via the Agent tool: Opus 5 (model opus, the compile-and-measure seat) and Fable 5 (model fable). Fable also ADJUDICATES the panel's task suggestions in its main-loop role. For diff-review passes INLINE the diff into the brief -- the cloud seats cannot read files. Resolve disagreements by MEASUREMENT, never by vote. VERIFY EACH SEAT ANSWERED BY CONTENT, NEVER BY SIZE -- a thinking burn returns an empty response wrapped in 100+ KB of hidden reasoning and a size check scores it the best answer in the panel. Full workflow + the self-sustaining monitor loop in CLAUDE.md; run a whole round with /round."}}
JSON
  ;;
task)
  cat <<'JSON'
{"systemMessage":"Task completed -> monitor cycle: (1) panel-review the finished work AND ask it for new tasks; (2) Fable adjudicates each suggestion, adds the worthwhile ones; (3) hand parallel read-only scoping to subagents; (4) claim the next task. Do not stop.","hookSpecificOutput":{"hookEventName":"TaskCompleted","additionalContext":"A task was just marked completed. Run the self-sustaining monitor cycle (see CLAUDE.md 'The self-sustaining monitor loop'), do NOT stop: (1) convene the full NINE-seat panel (./panel.sh for six + Opus and Fable via the Agent tool) to review the completed work AND surface new tasks -- residual defects, sibling bugs, instrument gaps; after-panel findings have repeatedly become the next rounds. (2) Fable (you, the main model) ADJUDICATES each suggested task -- worth adding? real/reachable/in-scope/test-first-able vs noise/duplicate -- add the worthwhile ones with TaskCreate, drop the rest with a one-line reason. (3) For each added task decide whether a subagent can start it NOW in parallel: read-only scoping/idiom/reachability investigation and brief-drafting parallelize freely (spawn a background subagent to de-risk before the panel convenes); builds/probes/gates are serial behind the single tree/rig/gate writer. (4) Claim the next task and run reproduce -> panel pass 1 -> implement -> panel pass 2 -> single clean gate -> commit. Never two gate/harness runs at once."}}
JSON
  ;;
wakeup)
  # Fires from PostToolUse on ScheduleWakeup, so the stamp is written by the
  # HARNESS rather than by anyone remembering to write it. That is the whole
  # point: the stop check below can then tell "about to stall" from "armed and
  # legitimately waiting", which it could not do before and which made it nag on
  # every stop -- four in a row, each time when a wakeup was in fact armed.
  BASE="${CLAUDE_PROJECT_DIR:-${TMPDIR:-/tmp}}"
  [ -d "$BASE/.claude" ] || BASE="${TMPDIR:-/tmp}"
  { date +%s > "$BASE/.loop_wakeup_stamp"; } 2>/dev/null
  exit 0
  ;;
stop)
  # Fires when the main loop stops. This exists because the loop once stalled
  # for exactly one reason: a turn ended without re-arming the wakeup, and no
  # hook watched that event. SessionStart and TaskCompleted could not catch it.
  #
  # Rate-limited to at most one nudge per 90s via a stamp file, deliberately:
  # a Stop hook that always blocks can wedge a session, so a genuine stop
  # succeeds on the immediately following attempt. One nudge, then it yields.
  # FAIL OPEN. If the stamp cannot be written the rate limit never advances,
  # which would block every stop and wedge the session -- the exact hazard this
  # design is guarding against. Caught while testing with CLAUDE_PROJECT_DIR
  # unset, where the path resolved to /.claude/... and the write failed
  # silently. So: pick a writable base, and if the write does not land, do not
  # block at all.
  BASE="${CLAUDE_PROJECT_DIR:-${TMPDIR:-/tmp}}"
  [ -d "$BASE/.claude" ] || BASE="${TMPDIR:-/tmp}"

  # If a wakeup was armed in the last 15 minutes the loop is NOT stalling, it is
  # waiting -- so say nothing and let the turn end. Without this the nudge fired
  # on every stop regardless, which is noise rather than a safeguard: a check
  # that always fires carries no information, the same defect this project keeps
  # finding in rows that always pass.
  WSTAMP="$BASE/.loop_wakeup_stamp"
  if [ -f "$WSTAMP" ]; then
    WLAST=$(cat "$WSTAMP" 2>/dev/null || echo 0)
    case "$WLAST" in ''|*[!0-9]*) WLAST=0 ;; esac
    if [ $(( $(date +%s) - WLAST )) -lt 900 ]; then
      exit 0
    fi
  fi

  STAMP="$BASE/.loop_stop_stamp"
  NOW=$(date +%s)
  LAST=0
  [ -f "$STAMP" ] && LAST=$(cat "$STAMP" 2>/dev/null || echo 0)
  case "$LAST" in ''|*[!0-9]*) LAST=0 ;; esac
  #  The redirect is inside the group so the SHELL's own "No such file"
  #  message is suppressed too -- putting 2>/dev/null on printf alone leaves it
  #  on stderr, which would surface as hook noise on every stop.
  if [ $((NOW - LAST)) -gt 90 ] && { printf '%s' "$NOW" > "$STAMP"; } 2>/dev/null; then
    cat <<'JSON'
{"decision":"block","reason":"LOOP CONTINUITY CHECK before stopping. The queue is worked as a continuous loop, so stopping is only correct when the queue is empty or a human decision is genuinely required (a destructive action or a real scope change). Check, in order: (1) Is a wakeup armed? If this turn handled a task-notification and the loop should continue, ScheduleWakeup must be re-armed with the same /loop prompt -- dropping it is what stalled the loop before, and it is the single most common failure here. (2) Is the in-flight task actually blocked, or merely waiting? If a panel, gate or battery is running, that is WAITING, not blocked -- do non-contending work (docs, queue triage, read-only scoping) instead of stopping. (3) If the in-flight task IS genuinely blocked -- it needs a build tree another process holds, or a measurement that has not returned -- then FORK: claim a different pending task and work that instead. Blocked on one item is not blocked on the queue. (4) Only if none of those apply, stop again and this will let you through."}
JSON
  fi
  ;;
esac
