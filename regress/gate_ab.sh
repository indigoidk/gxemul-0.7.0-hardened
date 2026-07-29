#!/bin/bash
# GATE 6 -- three-way A/B against pristine 0.7.0 and the pre-batch fork.
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
#  * Every run goes through run_emu(), which forces stdbuf -o0. On a pipe, gxemul's stdout
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

luna_markers() {   # binary, tag
    local log=$LOGDIR/ab_luna_$2.log
    run_emu 300 "$log" "$1" -e luna-88k -d "$LUNA_IMG" boot
    echo "$(count "$log" 'LUNA-88K BOOT'):$(count "$log" 'M88100'):$(count "$log" 'login:')"
}

if [ ! -f "$IMAGES/liveimage-luna88k-raw-20250518.img" ]; then
    degrade "luna88k image absent -- the only cross-build behavioural comparison did not run"
else
    note "luna88k (m88k): 'LUNA-88K BOOT':'M88100':'login:' marker counts"
    PRI=$(luna_markers "$PRISTINE_DIR/gxemul" pristine)
    PRE=$(luna_markers "$PREBATCH_DIR/gxemul" prebatch)
    HD=$(luna_markers "$ROOT/build/gxemul"   head)
    printf "       %-10s %s\n" pristine "$PRI"
    printf "       %-10s %s\n" prebatch "$PRE"
    printf "       %-10s %s\n" HEAD     "$HD"

    # Upstream 0.7.0 does NOT boot OpenBSD/luna88k -- measured, unbuffered, 300 s: it
    # emits its 699-byte banner and no guest output whatsoever. That is the expected
    # baseline, so it is asserted rather than treated as a failure. If it ever starts
    # booting, this check fires and the note below needs revisiting.
    check "pristine 0.7.0 does not boot luna88k (expected)" "$PRI" "0:0:0"
    check "HEAD matches pre-batch on luna88k"               "$HD"  "$PRE"
    check "HEAD boots luna88k to a login prompt"            "$HD"  "1:1:1"
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
