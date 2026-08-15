#!/bin/bash
# GATE 7 -- three-way A/B against pristine 0.7.0 and the pre-batch fork.
#
#   pristine   39748e3   unmodified upstream GXemul 0.7.0
#   prebatch   2ffc91e   the fork immediately before the current batch
#   HEAD                 what is being shipped
#
# TWO DIFFERENT QUESTIONS. Conflating them is the trap this gate exists to avoid:
#
#   vs PRISTINE  = CAPABILITY PRESERVATION. The fork carries ~290 deliberate corrections,
#                  so differences are EXPECTED and are not regressions. The only thing
#                  that counts against us is a machine that ran under upstream and no
#                  longer runs.
#
#   vs PREBATCH  = CHANGE-SET VERIFICATION. Everything not touched by the batch should be
#                  identical, and anything that moved must be attributable to a specific
#                  correction.
#
# `gate_ab.sh --build` (re)creates the two baselines first; without it they are reused.
#
# METHOD NOTES, both learned the hard way:
#
#  * Every run goes through run_emu_progress() (#419; run_emu() no longer has any caller),
#    which forces stdbuf -o0. On a pipe, gxemul's stdout
#    is 4 KB block-buffered and `timeout`'s SIGTERM discards a partial block -- so a guest
#    that produced 3 KB of good output scores ZERO. An earlier version of this comparison
#    reported a "capability regression" on luna88k that was entirely a lost buffer.
#  * Comparison is on SEMANTIC MARKERS, never on byte counts. Under a wall-clock timeout a
#    byte count measures how fast the host happened to be, not what the guest did.
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
. "$HERE/lib.sh"

SEC=$ROOT/GXEMUL-SEC
PRISTINE_DIR=/tmp/gx-pristine
PREBATCH_DIR=/tmp/gx-prebatch
PRISTINE_REF=39748e3
PREBATCH_REF=2ffc91e

build_baseline() {   # ref, dir, label
    local ref=$1 dir=$2 lab=$3
    echo "  building $lab ($ref) -> $dir"
    rm -rf "$dir"; mkdir -p "$dir"
    ( cd "$SEC" && git archive "$ref" ) | tar -x -C "$dir"
    # The repo does not track the exec bit (index mode 100644), so a tree produced by
    # `git archive` has a non-executable configure: it fails rc=126 and the generator
    # scripts die with make-level "Error 127". Note that greping the log for 'error:'
    # MISSES that, because make spells it "Error 127" -- the object count is the real tell.
    chmod +x "$dir/configure" 2>/dev/null
    find "$dir" -name '*.sh' -exec chmod +x {} + 2>/dev/null
    ( cd "$dir" && sh ./configure > configure.log 2>&1 && make -j12 > build.log 2>&1 )
    local objs; objs=$(find "$dir/src" -name '*.o' 2>/dev/null | wc -l)
    echo "    objects=$objs  binary=$([ -x "$dir/gxemul" ] && stat -c%s "$dir/gxemul" || echo NONE)"
    [ -x "$dir/gxemul" ] || { echo "    BUILD FAILED:"
        grep -E "Error [0-9]+|No rule|undefined reference" "$dir/build.log" | head -8; }
}

if [ "${1:-}" = "--build" ]; then
    echo "## building baselines"
    build_baseline "$PRISTINE_REF" "$PRISTINE_DIR" pristine
    build_baseline "$PREBATCH_REF" "$PREBATCH_DIR" prebatch
    echo
fi

gate_begin "a-b-baselines"
need_exec "$PRISTINE_DIR/gxemul" "$PREBATCH_DIR/gxemul" "$ROOT/build/gxemul"

# probe <label> <binary> <logfile> <args...>  -> prints "marker=N ..." for the rig
# NOTE THE R: PREFIX. It opens the base image read-only and routes every guest write into
# a temporary overlay that is discarded when the run ends.
#
# Without it this function booted THREE DIFFERENT BUILDS SEQUENTIALLY AGAINST ONE SHARED,
# WRITABLE 2 GB IMAGE, so the runs were not independent: each build inherited whatever
# filesystem state the previous one left behind, including an unclean unmount when the
# 300 s timeout killed a guest that had reached its login prompt. The symptom was a
# non-deterministic FAIL -- HEAD came back 1:1:0 having passed 1:1:1 twice at the same
# commit with no code change. The image's mtime confirmed it: it tracked the most recent
# boot, not the download.
#
# Timing was ruled out separately by measurement: both builds reach `login:` in about
# 100 s against a 300 s budget, so this was never a marginal timeout.
LUNA_IMG="R:$IMAGES/liveimage-luna88k-raw-20250518.img"

# #419: the 300 s wall budget above was replaced by a budget of GUEST WORK. See
# run_emu_progress() in lib.sh for the measurements. Three constants, each measured:
#
#   LUNA_BUDGET 12 G   Observed instructions-to-login spans 7.316-7.786 G over eleven boots.
#                      12 G is +54 % over the observed max. It bounds ONLY the failure path --
#                      a healthy boot stops at the MARKER long before it -- so over-provisioning
#                      costs nothing on the success path and removes per-host recalibration.
#                      8.5 G was rejected: it sits only ~5 % above the theoretical ceiling a
#                      maximally-precise usleep host would reach (~8.06 G).
#   LUNA_STALL  120 s  At the SLOWEST rate measured here (9.9 M instr/s -- 7,349,301,148
#                      instructions in 742 s, host saturated) one -N record arrives every
#                      3.4 s. That is a HANG, not a slow host -- but the claim is empirical,
#                      not absolute: this detector still reads `date +%s`, so a host that
#                      SUSPENDS or starves the process for two minutes looks identical.
#                      *** THE MULTIPLIER WAS OVERSTATED AS 35x. 3.4 s is a MEAN derived from
#                      total instructions over total wall time; the WORST observed gap is what
#                      matters, and measured directly on the pty path under saturation it is
#                      7.06 s (n=219: min 0.47, median 3.86, p90 5.54, p99 6.23). So the
#                      honest multiplier is 17x, not 35x. Still ample -- but a mean is not a
#                      worst case, and quoting one as the other is how a margin gets believed
#                      to be twice its real size. ***
#   LUNA_BACKSTOP 1800 s  2.4x the worst boot ever measured here (742 s, 8 busy loops on 8
#                      cores, which still reached login 1:1:1).
LUNA_BUDGET=12000000000
LUNA_STALL=120
LUNA_BACKSTOP=1800

# *** THE CONSTANTS NEEDED THEIR OWN ROWS.  Measured in pass 2: multiplying LUNA_BUDGET by
# 1000, or LUNA_BACKSTOP by 4000, or disabling LUNA_STALL entirely, left ALL FOURTEEN CHECKS
# GREEN.  The selftest below exercises run_emu_progress() with LITERAL arguments, so it proves
# the function works while proving nothing about the values this gate actually passes it --
# the rows guard a different instance of the thing they appear to guard.
#
# These bounds are derived, not taste: the observed maximum instructions-to-login is
# 7,785,570,754, so a budget below ~1.05x that would false-FAIL a healthy boot and one above
# ~2x stops bounding anything.  The stall threshold must exceed several -N record intervals
# (~3.4 s at the slowest rate measured) and stay far below the backstop.  The backstop must
# exceed the worst boot measured (742 s) with margin.  A static check costs no boot. ***
LUNA_OBSERVED_MAX=7785570754
check_min "budget is above the observed max instructions-to-login" \
          "$LUNA_BUDGET" "$(( LUNA_OBSERVED_MAX * 105 / 100 ))"
check     "budget still bounds something (<= 2x observed max)" \
          "$([ "$LUNA_BUDGET" -le "$(( LUNA_OBSERVED_MAX * 2 ))" ] && echo yes || echo "no: $LUNA_BUDGET")" yes
check     "stall threshold is many -N intervals but well under the backstop" \
          "$([ "$LUNA_STALL" -ge 30 ] && [ "$LUNA_STALL" -le $(( LUNA_BACKSTOP / 4 )) ] && echo yes || echo "no: $LUNA_STALL")" yes
check     "backstop exceeds the worst boot measured (742 s) with margin" \
          "$([ "$LUNA_BACKSTOP" -ge 1200 ] && [ "$LUNA_BACKSTOP" -le 3600 ] && echo yes || echo "no: $LUNA_BACKSTOP")" yes

# #419 SELFTEST. The classifier decides whether a row is a regression, a hang, a harness fault
# or merely a slow host, so it needs its own rows -- and they must NOT need the rig, or they
# would cost 15 minutes and never be run. Fake "emulators" drive every reason in seconds.
#
# WHY THIS IS NOT OPTIONAL: the BUDGET and STALLED branches are ONLY EVER ENTERED BY A FAILING
# RUN, because a healthy boot stops at MARKER long before either. So nothing on a green run
# exercises them, and a mutation that breaks them is invisible to every capability row here.
#
# *** AND THE HARDEST CASE IS THE ONE THAT LOOKS HEALTHY. Remove `-N` and the guest still
# boots, still prints every marker, and still classifies as MARKER -- there is nothing wrong
# with the boot. What is wrong is that the budget and stall protections were never armed, and
# the ONLY observable difference is that the instruction count stayed at zero. Pass 2 caught
# this surviving: the fake originally written for it never printed `login:`, so it had been
# built to match the guard rather than the threat. ***
selftest_progress() {
    local d=$LOGDIR/r419fake; mkdir -p "$d"

    # Prints instruction records, then the marker. -> MARKER
    printf '#!/bin/sh\nfor i in 1 2 3; do echo "[ $((i*100000000)) instrs; i/s=1 avg=1]"; sleep 0.2; done\necho "login: "\nsleep 30\n' > "$d/f_marker"
    # Prints ever-advancing records and never the marker. -> BUDGET (with a tiny budget)
    printf '#!/bin/sh\ni=1\nwhile :; do echo "[ $((i*100000000)) instrs; i/s=1 avg=1]"; i=$((i+1)); sleep 0.2; done\n' > "$d/f_budget"
    # One record, then silence while staying alive. -> STALLED
    printf '#!/bin/sh\necho "[ 100000000 instrs; i/s=1 avg=1]"\nsleep 60\n' > "$d/f_stall"
    # Prints two markers but NO instruction record, and never reaches the milestone. -> ABSENT
    printf '#!/bin/sh\necho "LUNA-88K BOOT"\necho "M88100"\nsleep 60\n' > "$d/f_absent"
    # *** THE ONE THAT MATTERS: a guest that BOOTS PERFECTLY with no instruction stream --
    # exactly what removing `-N` produces. It reaches the milestone, so `reason` is MARKER and
    # every reason-based check passes; only the instruction COUNT reveals that the budget and
    # stall protections were never armed. Pass 2 found this surviving; the fake above had been
    # written to match the guard rather than the threat, because it never printed `login:`. ***
    printf '#!/bin/sh\necho "LUNA-88K BOOT"\necho "M88100"\necho "login: "\nsleep 30\n' > "$d/f_nostream"
    chmod +x "$d"/f_*

    local o r n
    o=$(run_emu_progress 20 500000000 5 'login:' "$d/o_marker.log" "$d/f_marker")
    r=${o#reason=}; r=${r%% *}
    check "progress selftest: marker stops the run" "$r" "MARKER"

    o=$(run_emu_progress 20 500000000 5 'login:' "$d/o_budget.log" "$d/f_budget")
    r=${o#reason=}; r=${r%% *}
    check "progress selftest: instruction budget stops the run" "$r" "BUDGET"

    o=$(run_emu_progress 20 500000000 3 'login:' "$d/o_stall.log" "$d/f_stall")
    r=${o#reason=}; r=${r%% *}
    check "progress selftest: a stalled guest is STALLED, not slow" "$r" "STALLED"

    # If this row ever reads MARKER or BACKSTOP, a broken -N would score as an ordinary
    # timeout and the gate would go quietly green while measuring nothing.
    o=$(run_emu_progress 8 500000000 30 'login:' "$d/o_absent.log" "$d/f_absent")
    r=${o#reason=}; r=${r%% *}
    check "progress selftest: markers without an instruction stream are ABSENT" "$r" "ABSENT"

    # A guest that BOOTS with no instruction stream is the dropped-`-N` shape, and its reason
    # is legitimately MARKER -- there is nothing wrong with the boot. The only signal that the
    # oracle was never armed is that the count stayed at zero, so THAT is what the real rows
    # assert. This row exists to keep the two facts nailed together: reason MARKER, count 0.
    o=$(run_emu_progress 20 500000000 10 'login:' "$d/o_nostream.log" "$d/f_nostream")
    r=${o#reason=}; r=${r%% *}
    n=${o#*ninstrs=}; n=${n%% *}
    check "progress selftest: a boot with no -N stream still reads MARKER" "$r" "MARKER"
    check "progress selftest: ...and is caught only by a zero instruction count" "$n" "0"

    # A CRASH IS NOT A TIMEOUT. Measured on the previously shipped code: a fake emitting one
    # record then exiting 3 reported BACKSTOP -- putting a dead build into the single reason
    # a caller is allowed to excuse as host load. timeout(1) returns 124 if and only if IT
    # fired, so the exit status is what separates the two.
    printf '#!/bin/sh\necho "[ 100000000 instrs; i/s=1 avg=1]"\nexit 3\n' > "$d/f_crash"
    chmod +x "$d/f_crash"
    o=$(run_emu_progress 20 500000000 10 'login:' "$d/o_crash.log" "$d/f_crash")
    r=${o#reason=}; r=${r%% *}
    check "progress selftest: a crashed emulator is EXITED, not BACKSTOP" "$r" "EXITED"
}
selftest_progress

# Sets R_REASON / R_INSTRS / R_MARKERS. Globals rather than a return value because the
# caller needs all three to score a row, and the reason is the whole point of #419.
luna_run() {   # binary, tag
    local log=$LOGDIR/ab_luna_$2.log out
    out=$(run_emu_progress "$LUNA_BACKSTOP" "$LUNA_BUDGET" "$LUNA_STALL" 'login:' \
              "$log" "$1" -N -e luna-88k -d "$LUNA_IMG" boot)
    R_REASON=${out#reason=}; R_REASON=${R_REASON%% *}
    R_INSTRS=${out#*ninstrs=}; R_INSTRS=${R_INSTRS%% *}
    R_MARKERS="$(count "$log" 'LUNA-88K BOOT'):$(count "$log" 'M88100'):$(count "$log" 'login:')"
    printf "       %-10s %-9s instrs=%-14s %s\n" "$2" "$R_REASON" "$R_INSTRS" "$R_MARKERS"
}

if [ ! -f "$IMAGES/liveimage-luna88k-raw-20250518.img" ]; then
    degrade "luna88k image absent -- the only cross-build behavioural comparison did not run"
else
    note "luna88k (m88k): stop reason + 'LUNA-88K BOOT':'M88100':'login:' marker counts"
    luna_run "$PRISTINE_DIR/gxemul" pristine; PRI=$R_MARKERS; PRI_R=$R_REASON; PRI_N=$R_INSTRS
    luna_run "$PREBATCH_DIR/gxemul" prebatch; PRE=$R_MARKERS; PRE_R=$R_REASON; PRE_N=$R_INSTRS
    luna_run "$ROOT/build/gxemul"   head;     HD=$R_MARKERS;  HD_R=$R_REASON;  HD_N=$R_INSTRS

    # #419 SCORING. The defect was that a load-induced timeout could not be told apart from a
    # capability regression. The naive cure -- calling every timeout INCONCLUSIVE -- was
    # MEASURED to be strictly worse: `degrade` and `gate_skip` both exit 77 -> SKIP ->
    # REGRESS_PASS_WITH_GAPS (exit 3), so a HEAD that hangs before login would turn today's
    # hard REGRESS_FAIL (exit 1) into a green-ish result. Green is what gets read. So the
    # reasons are scored individually and only ONE of them is ever inconclusive.
    #
    # ROW-SCOPED END CONDITIONS, and this is the subtle part: the signal that means "hung" for
    # HEAD is the EXPECTED state for pristine. Upstream 0.7.0 emits ZERO -N records on luna88k
    # (measured, five runs, 768-byte logs), so it can never complete an instruction budget --
    # scoring it by budget would turn a long-standing PASS into a permanent not-run.
    check "pristine 0.7.0 does not boot luna88k (expected)" "$PRI" "0:0:0"
    # #419 pass 2: assert the COUNT, not the reason. Scoring this by reason accepted STALLED
    # too, so "one instruction record followed by silence" would have passed a row whose name
    # claims there is no instruction stream at all. The row now says what it means.
    check "pristine emits no instruction records at all" "$PRI_N" "0"
    # PRI_R was assigned and never read after pass 2 removed its only consumer -- a seat
    # caught the dead variable. It is worth asserting rather than deleting: ABSENT proves
    # the no-stream path classified it, whereas BACKSTOP would mean the run sat for the full
    # 1800 s and nothing noticed.
    check "pristine is classified by the absent-stream path, not the backstop" "$PRI_R" "ABSENT"

    # An absent stream from a build that is supposed to RUN is a harness fault -- the `-N`
    # argument or the extraction broke -- and a harness fault must be red, never inconclusive.
    #
    # *** #419 pass 2: THIS ASSERTS THE COUNT BECAUSE ASSERTING THE REASON DID NOT WORK.
    # `reason` is only ABSENT when the run did NOT reach the marker, so a build that boots
    # normally with `-N` removed classifies as MARKER and sailed straight through the previous
    # spelling of this check. Dropping `-N`, or breaking the extraction by one character, would
    # then leave every capability row green while the budget and stall protections this round
    # exists for were silently gone. A seat found it; the selftest had missed it because the
    # fake built for this case omitted `login:` -- it was written to match the guard rather
    # than the threat. ***
    for pair in "prebatch:$PRE_N" "HEAD:$HD_N"; do
        if [ "${pair#*:}" -gt 0 ] 2>/dev/null; then
            check "${pair%%:*}: -N instruction stream was actually observed" present present
        else
            check "${pair%%:*}: -N instruction stream was actually observed" "0 records" present
        fi
    done

    # BUDGET means the guest was given a full allowance of WORK and still never booted. Host
    # load cannot produce that, so it is a real negative and stays a hard failure.
    # STALLED means the guest stopped executing entirely -- a hang, not a slow host.
    for pair in "prebatch:$PRE_R" "HEAD:$HD_R"; do
        case "${pair#*:}" in
        BUDGET|STALLED)
            check "${pair%%:*}: stopped for a reason load cannot cause" "${pair#*:}" MARKER ;;
        esac
    done

    # The ONLY load-ambiguous outcome: wall clock expired while instructions were still
    # advancing. Even here it is inconclusive ONLY if prebatch was hit too -- gate_ab already
    # boots all three builds, so the load signal is free. If prebatch reached its marker the
    # host was demonstrably fine, and HEAD alone failing is a REGRESSION, not a casualty.
    if [ "$HD_R" = BACKSTOP ]; then
        if [ "$PRE_R" = MARKER ]; then
            check "HEAD hit the wall backstop while prebatch booted (regression, not load)" \
                  "BACKSTOP@$HD_N" "MARKER"
        else
            degrade "both HEAD and prebatch hit the ${LUNA_BACKSTOP}s backstop with instructions still advancing (HEAD $HD_N, prebatch $PRE_N) -- host too slow to decide; NOT a pass"
        fi
    fi

    check "HEAD matches pre-batch on luna88k"               "$HD"  "$PRE"
    check "HEAD boots luna88k to a login prompt"            "$HD"  "1:1:1"

    # Upstream 0.7.0 does NOT boot OpenBSD/luna88k -- measured, unbuffered: it emits its
    # banner -- 768 bytes of log, measured across five runs -- and no guest output whatsoever.
    # That is the expected baseline, so it is
    # asserted rather than treated as a failure. If it ever starts booting, the check above
    # fires and this note needs revisiting.
    #
    # #419 measured WHY, and it matters for the scoring above: pristine does not exit and does
    # not idle -- it SPINS, burning 100 % of one core, emitting fewer than 33,554,432
    # instructions in 300 s (< 111,848 instr/s). So "the process is still alive" carries no
    # information here, and an instruction budget could never complete: 12 G would take over
    # 29 hours. The stall detector catches it in LUNA_STALL seconds (120) instead -- a
    # prototype used 30 s and this note claimed that figure for months longer than it was
    # true; the shipped gate uses one constant for all three legs.
fi
echo

# CAPABILITY PRESERVATION: every machine alias UPSTREAM advertises must still be
# advertised by HEAD.
#
# This replaces an alias check that could not fail. The old one harvested the alias list
# from HEAD's own -H and then grepped each machine's output for "Unknown machine" -- a
# string that appears NOWHERE in src/ (verified: 0 occurrences; the real message is
# "Unknown subtype", capitalised, so the lower-case pattern missed it too). `unknown` was
# therefore 0 for every possible input. Worse, harvesting from HEAD meant a dropped
# machine was absent from the list and never probed, so the one thing it claimed to detect
# was the one thing it structurally could not.
#
# Comparing the two advertised lists is a genuine assertion, needs no media, and is fast.
note "machine-alias capability: upstream's list must still be advertised by HEAD"
alias_list() { "$1" -H 2>&1 | grep -oE '"[a-z0-9_.-]+"' | tr -d '"' | sort -u; }
alias_list "$PRISTINE_DIR/gxemul" > "$LOGDIR/alias_pristine.txt"
alias_list "$ROOT/build/gxemul"   > "$LOGDIR/alias_head.txt"
n_pri=$(wc -l < "$LOGDIR/alias_pristine.txt")
n_head=$(wc -l < "$LOGDIR/alias_head.txt")
comm -23 "$LOGDIR/alias_pristine.txt" "$LOGDIR/alias_head.txt" > "$LOGDIR/alias_lost.txt"
comm -13 "$LOGDIR/alias_pristine.txt" "$LOGDIR/alias_head.txt" > "$LOGDIR/alias_gained.txt"
n_lost=$(wc -l < "$LOGDIR/alias_lost.txt")
n_gained=$(wc -l < "$LOGDIR/alias_gained.txt")
note "upstream advertises $n_pri, HEAD advertises $n_head"
[ "$n_gained" -gt 0 ] && note "added by the fork (expected, not a regression): $(tr '\n' ' ' < "$LOGDIR/alias_gained.txt")"
[ "$n_lost"   -gt 0 ] && note "MISSING FROM HEAD: $(tr '\n' ' ' < "$LOGDIR/alias_lost.txt")"
# A floor, so a broken -H or a broken regex cannot pass by yielding an empty list.
check_min "upstream alias list is non-trivial"   "$n_pri" 40
check     "machines upstream had that HEAD lost" "$n_lost" "0"

gate_end
exit $?
