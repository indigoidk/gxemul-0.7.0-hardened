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
#     Every emulator invocation goes through run_emu(), which forces stdbuf -o0 -e0.
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
