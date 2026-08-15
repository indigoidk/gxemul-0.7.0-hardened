#!/bin/bash
# Shared helpers for the regression gates.
#
# Two rules encoded here, both learned by getting them wrong:
#
#  1. RUN UNBUFFERED. When gxemul's stdout is a pipe, libc switches to 4 KB block
#     buffering. `timeout` then kills it with SIGTERM and the partial block is lost, so a
#     guest that produced 3 KB of perfectly good boot output scores ZERO bytes while one
#     that produced 5 KB scores 4096. An early version of this harness compared those
#     numbers across builds and "found" a capability regression that was pure buffering.
#     Every emulator invocation goes through run_emu() or run_emu_progress(), both of which
#     force stdbuf -o0 -e0.  (#419 note: run_emu() itself now has NO CALLERS -- gate 7 was
#     its last one.  It is kept because the rule is general and a future gate will want the
#     simple form, but do not cite it as the universal path: run_emu_progress() is.)
#
#  2. A MISSING INPUT IS A HARD ERROR, NEVER A ZERO SCORE. The same early version had no
#     existence check on the baseline binaries, so a wrong path looked exactly like a
#     total behavioural failure. need_file() aborts the gate instead.
#
# Verdicts are PASS / FAIL / SKIP. A SKIP is never counted as a PASS.

ROOT=${ROOT:-/mnt/c/DocumentNoSnc/CC/GXEMUL}
IMAGES=$ROOT/_images
LOGDIR=${LOGDIR:-/tmp/gxregress}
mkdir -p "$LOGDIR"

C_OK=$'\033[32m'; C_BAD=$'\033[31m'; C_SKIP=$'\033[33m'; C_OFF=$'\033[0m'
[ -t 1 ] || { C_OK=""; C_BAD=""; C_SKIP=""; C_OFF=""; }

# Exit codes. SKIP is 77, NOT 2, because bash exits 2 on a SYNTAX ERROR -- so with 2 as
# the skip code a typo in any gate was silently downgraded to "coverage gap" and run.sh
# still exited 0. Anything non-zero that is not 77 is a failure.
EXIT_SKIP=77

GATE_NAME=""
_fails=0
_checks=0

gate_begin() { GATE_NAME=$1; _fails=0; _checks=0
    echo "############################################################"
    echo "## GATE: $GATE_NAME"
    echo "############################################################"
}

# check <description> <actual> <expected>
check() {
    _checks=$((_checks+1))
    if [ "$2" = "$3" ]; then
        printf "  ${C_OK}ok${C_OFF}   %-52s %s\n" "$1" "$2"
    else
        printf "  ${C_BAD}FAIL${C_OFF} %-52s got=%s want=%s\n" "$1" "$2" "$3"
        _fails=$((_fails+1))
    fi
}

# check_min <description> <actual> <minimum>
check_min() {
    _checks=$((_checks+1))
    if [ "$2" -ge "$3" ] 2>/dev/null; then
        printf "  ${C_OK}ok${C_OFF}   %-52s %s (>= %s)\n" "$1" "$2" "$3"
    else
        printf "  ${C_BAD}FAIL${C_OFF} %-52s got=%s want>=%s\n" "$1" "$2" "$3"
        _fails=$((_fails+1))
    fi
}

note() { printf "  --   %s\n" "$*"; }

# A gate may declare that part of its coverage did not run (a rig whose image is absent,
# say). That must not be absorbed into a PASS: it downgrades the whole gate to SKIP, so a
# missing input can never be reported as evidence of correctness.
_degraded=0
degrade() { _degraded=1; printf "  ${C_SKIP}skip${C_OFF} %s\n" "$*"; }

gate_end() {
    echo
    if [ "$_checks" = 0 ]; then
        echo "${C_SKIP}$GATE_NAME: SKIP${C_OFF} (no checks ran)"; return $EXIT_SKIP
    elif [ "$_fails" != 0 ]; then
        echo "${C_BAD}$GATE_NAME: FAIL${C_OFF} ($_fails of $_checks checks)"; return 1
    elif [ "$_degraded" != 0 ]; then
        echo "${C_SKIP}$GATE_NAME: SKIP${C_OFF} ($_checks checks passed, but part of the gate could not run)"
        return $EXIT_SKIP
    else
        echo "${C_OK}$GATE_NAME: PASS${C_OFF} ($_checks checks)"; return 0
    fi
}

#  #371: gate_skip() exits with the SKIP code, which run.sh maps to
#  REGRESS_PASS_WITH_GAPS -- a green-ish verdict. It never consulted the running
#  failure counter, so a gate that had ALREADY recorded red checks and then hit a
#  gate_skip (a probe that produced no result line, a missing rig image) reported
#  those reds as a skip and they vanished from the battery. Measured on a
#  synthetic gate: one FAIL then gate_skip exited 77, PASS_WITH_GAPS. This is the
#  same "a green row means nothing" class the gate rows themselves guard against,
#  in the harness's own control flow.
#
#  So a gate_skip AFTER failures is a FAIL, not a skip: the skip cannot un-record
#  what already failed. A gate_skip with a clean slate stays a genuine skip (a
#  preflight that could not run at all -- need_file/need_exec). degrade() was
#  already correct: gate_end() tests _fails before _degraded, so a degraded gate
#  with recorded failures already reports FAIL. Nothing there to change.
gate_skip() {
    echo
    if [ "${_fails:-0}" != 0 ]; then
        echo "${C_BAD}$GATE_NAME: FAIL${C_OFF} ($_fails of $_checks checks failed" \
             "before this section could not run: $*)"
        exit 1
    fi
    echo "${C_SKIP}$GATE_NAME: SKIP${C_OFF} -- $*"; exit $EXIT_SKIP
}

need_file() {
    for f in "$@"; do
        [ -e "$f" ] || gate_skip "missing required input: $f"
    done
}

need_exec() {
    for f in "$@"; do
        [ -x "$f" ] || gate_skip "missing or non-executable binary: $f"
    done
}

# run_emu <seconds> <logfile> <binary> [args...]
# Always unbuffered, always with stdin closed so a guest prompt cannot wedge the run.
run_emu() {
    local secs=$1 log=$2; shift 2
    ( cd "$IMAGES" 2>/dev/null || cd /; timeout "$secs" stdbuf -o0 -e0 "$@" </dev/null ) \
        > "$log" 2>&1
    return 0
}

# run_emu_progress <backstop_s> <budget_instrs> <stall_s> <marker_re> <logfile> <binary> [args...]
#
# #419: run_emu()'s wall-clock budget is a LOAD-SENSITIVE ORACLE. Under host load the guest
# makes less progress in the same seconds, the marker never appears, and the row FAILs
# INDISTINGUISHABLY FROM A REAL CAPABILITY REGRESSION -- measured twice, from panel seats and
# from interactive greps. This runs the emulator against a budget of GUEST WORK instead, and
# -- the part that actually fixes the defect -- it REPORTS WHY IT STOPPED.
#
# Echoes one line: "reason=<MARKER|BUDGET|STALLED|BACKSTOP|ABSENT> ninstrs=<N> wall=<S>"
#
#   MARKER    the regex matched. Stop AT ONCE: today's run burns its whole budget AFTER
#             login because the guest never exits, so this is also where the speed-up is.
#   BUDGET    the guest executed <budget_instrs> and still never matched. It was given a full
#             allowance of WORK, not of host seconds, so LOAD CANNOT EXPLAIN IT -> the caller
#             may score it FAIL with confidence.
#   STALLED   no instruction progress for <stall_s>. A slow host still executes instructions;
#             a hung guest does not. This is what makes a boot hang DISTINGUISHABLE from load,
#             and it is upstream 0.7.0's exact signature on luna88k.
#   BACKSTOP  wall clock expired while instructions were still advancing. The only genuinely
#             load-ambiguous outcome, and the only one a caller may treat as inconclusive.
#   ABSENT    no -N record ever appeared. A HARNESS FAULT, and it must be scored RED: drop
#             `-N` from the args, or break the extraction by one character, and every leg
#             would otherwise fall to BACKSTOP for ever while the battery stayed green and
#             the capability rows tested nothing.
#
# *** DELIBERATELY POLLS A FILE INSTEAD OF PIPING. Rule 1 at the top of this file exists
# because a lost 4 KB block once scored a good boot as ZERO and it was reported as a
# capability regression. `stdbuf -o0` fixes GXEMUL's buffering, but a `gxemul | grep` reader
# block-buffers ITS OWN stdout and re-creates the identical bug one process later. Worse, a
# SIGPIPE-based stop only fires on the emulator's NEXT WRITE -- which never comes for a wedged
# guest, precisely the case the stop exists to catch. Polling a file has neither failure mode,
# and the log is complete on disk however the run ends.
#
# IT HAS A THIRD, THOUGH, AND THE FIRST WINDOW SIZE HIT IT: a tail window smaller than the
# gap between two -N records loses the oracle entirely and reports ABSENT for a perfectly
# healthy guest. See the window comment below. ***
#
# MEASURED BASIS (eleven luna88k boots, 2026-08-14). Instructions-to-login spans
# 7,315,767,413 (loaded) to 7,785,570,754 -- 3.57 % across eight idle runs, 6.42 % across an
# 8x host-speed range. Dropping the page cache did NOT widen it. Load moves the count DOWN
# ~4 %, so the count is not pure guest work, but it errs in the SAFE direction for a ceiling.
#
# *** THE MECHANISM FOR THAT ~4 % IS NOT ESTABLISHED, and an earlier version of this comment
# asserted one that the source contradicts. It claimed the m88k idle fold credits 8191
# instructions per wall-paced usleep(500) iteration. The constant is real
# (N_DYNTRANS_IDLE_BREAK = N_SAFE_DYNTRANS_LIMIT = (1<<13)-1 = 8191, added at
# cpu_m88k_instr.c:2611 and :2660) but it is SUBTRACTED BACK at cpu_dyntrans.c:377 before
# n_instrs is accumulated at :392, so the net credit per fold is ~0, not 8191. The DIRECTION
# is measured and the conclusion rests on the measurement; the explanation does not. Do not
# re-assert a mechanism here without reading both sites. ***
#
# The decisive run: under 8 busy loops on 8 cores the guest STILL reached login, at
# 7,349,301,148 instructions in 742 s -- the same run that scored 1:1:0 and FAILed at the old
# 300 s wall budget. That is 9.9 M instr/s, which is the slowest rate measured here.
run_emu_progress() {
    local backstop=$1 budget=$2 stall=$3 marker=$4 log=$5; shift 5
    local t0 last_n=0 last_change n now reason= pid

    : > "$log"
    t0=$(date +%s); last_change=$t0
    # *** DO NOT WRAP THIS IN A SUBSHELL. `$!` would then be the SUBSHELL's pid, and killing
    # it reaps the wrapper while ORPHANING the emulator. Measured on the first gate run of
    # #419: the pristine leg was correctly classified STALLED at 120 s, its "kill" removed
    # only the subshell, and the emulator was still burning 99.9 % of a core four minutes
    # later while the next two legs measured themselves under that self-inflicted load.
    # Starting `timeout` directly makes `$!` the process we actually need to signal. ***
    local oldpwd=$PWD
    cd "$IMAGES" 2>/dev/null || cd /
    timeout "$backstop" stdbuf -o0 -e0 "$@" </dev/null > "$log" 2>&1 &
    pid=$!
    cd "$oldpwd" || true

    while kill -0 "$pid" 2>/dev/null; do
        # tail -c keeps this O(1) in log size rather than O(n) per poll.
        #
        # *** THE WINDOW WAS 2048 AND THAT WAS TOO SMALL -- measured, not reasoned.
        # A guest emitting one -N record per 2 s with ~6 KB of console output between
        # records scored ABSENT with instrs=0: a healthy executing build reported as a
        # harness fault AND a capability regression, which is exactly the misclassification
        # this function exists to remove.  On the real luna88k log the max inter-record gap
        # is 2334 bytes -- ALREADY LARGER THAN THE OLD WINDOW.  It did not bite only because
        # the miss must persist for the whole stall period.  64 KB is ~28x the observed
        # worst gap and still O(1) per poll. ***
        n=$(tail -c 65536 "$log" 2>/dev/null | grep -ao '\[ *[0-9]\+ instrs' | tail -1 | tr -dc '0-9')
        n=${n:-$last_n}
        now=$(date +%s)
        [ "$n" != "$last_n" ] && { last_n=$n; last_change=$now; }
        if grep -aq "$marker" "$log" 2>/dev/null; then reason=MARKER; break; fi
        if [ "${n:-0}" -gt "$budget" ] 2>/dev/null;  then reason=BUDGET; break; fi
        if [ $((now - last_change)) -ge "$stall" ];  then reason=STALLED; break; fi
        sleep 1
    done

    # The emulator outlives the poll loop unless it is killed here, and killing `timeout`
    # alone is not enough to rely on: reap its children explicitly by pid. Do NOT use
    # `pkill -f <pattern>` for this -- the pattern appears in the invoking shell's own
    # command line, so pkill SIGTERMs itself before finishing the job (measured: it exited
    # 15 having killed nothing).
    local kid
    for kid in $(pgrep -P "$pid" 2>/dev/null); do kill -TERM "$kid" 2>/dev/null; done
    kill -TERM "$pid" 2>/dev/null
    sleep 1
    for kid in $(pgrep -P "$pid" 2>/dev/null); do kill -9 "$kid" 2>/dev/null; done
    kill -9 "$pid" 2>/dev/null
    wait "$pid" 2>/dev/null

    if [ -z "$reason" ]; then
        # *** RE-CHECK THE LOG BEFORE DEFAULTING TO BACKSTOP.  Measured 3/3,
        # deterministic: the poll period is ~1006 ms, so a marker landing in the final
        # poll window was scored BACKSTOP even though the guest had reached it -- the
        # caller then called a SUCCESSFUL BOOT a regression while the marker-count row
        # simultaneously passed on 1:1:1.  Two contradictory rows from one run. ***
        if grep -aq "$marker" "$log" 2>/dev/null; then
            reason=MARKER
        else
            # The process ended on its own or the backstop's timeout(1) reaped it.
            reason=BACKSTOP
        fi
        # Same race on the count: a run that finishes inside one poll interval has a
        # valid record on disk that no poll ever observed.
        n=$(tail -c 65536 "$log" 2>/dev/null | grep -ao '\[ *[0-9]\+ instrs' | tail -1 | tr -dc '0-9')
        [ -n "$n" ] && [ "${n:-0}" -gt "${last_n:-0}" ] 2>/dev/null && last_n=$n
    fi
    # An absent oracle stream outranks every other reason: if -N produced nothing then
    # nothing was measured, whatever else the run appeared to do.
    [ "${last_n:-0}" -eq 0 ] && [ "$reason" != MARKER ] && reason=ABSENT

    echo "reason=$reason ninstrs=$last_n wall=$(( $(date +%s) - t0 ))"
}

# count <logfile> <pattern>   -- number of matching lines, 0 if the file is absent.
#
# NOT `[ -f x ] && grep -ac ... || echo 0`. On zero matches grep prints "0" AND exits 1,
# so the || arm fires too and the function emits TWO lines ("0\n0"). Measured: 3 bytes,
# 2 lines. That silently corrupted every marker string built from it, and made gate 6's
# one deliberate expected-negative assertion impossible to satisfy.
count() {
    [ -f "$1" ] || { echo 0; return; }
    local c
    c=$(grep -ac -- "$2" "$1" 2>/dev/null)
    echo "${c:-0}"
}
