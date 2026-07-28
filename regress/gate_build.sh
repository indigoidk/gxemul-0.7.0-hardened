#!/bin/bash
# GATE 1 -- both trees rebuild clean from committed source.
#
# There is NO VPATH in this project. `build/` is an in-place copy compiled from est/, and
# /tmp/gxsec-build is an in-place copy compiled from GXEMUL-SEC/. An edit that is not
# propagated into the compile tree silently tests the OLD binary, so this gate re-syncs
# both from their authoritative tree before building.
#
# Two failure modes this gate is shaped to catch, both of which have happened:
#
#  * cpus/*.o must be deleted explicitly. cpu_mips_instr.c is #included into cpu_mips.o
#    rather than compiled separately, so make does not see it as a dependency and a stale
#    object survives an ordinary rebuild.
#  * /tmp/gxsec-build's Makefile is GENERATED from Makefile.skel and is not tracked. A
#    tree recreated with `cp -a` has none, and make then exits rc=2 having built nothing
#    -- which looks like "0 errors" if you only grep for the word error. The object COUNT
#    is the real check, which is why it is asserted rather than reported.
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
. "$HERE/lib.sh"

EST=$ROOT/est
SEC=$ROOT/GXEMUL-SEC
PMAX_TREE=$ROOT/build
ARC_TREE=/tmp/gxsec-build
RIG=$ROOT/gxemul_arc_rig

gate_begin "clean-build"
need_file "$EST/src" "$SEC/src" "$PMAX_TREE" "$ARC_TREE"

build_tree() {   # label, source tree, compile tree, expected object count
    local lab=$1 src=$2 tree=$3 want=$4
    local log=$LOGDIR/build_$lab.log

    ( cd "$src/src" && find . \( -name '*.c' -o -name '*.h' -o -name '*.cc' \) \
        -exec cp -f --parents {} "$tree/src/" \; ) 2>/dev/null

    # VERIFY THE SYNC. The copy above discards its exit status and all stderr, and
    # `find -exec ... \;` continues past per-file failures -- so a single unwritable file
    # in the compile tree would silently leave the OLD source in place and the gate would
    # then report a clean build of the wrong code. That is precisely the failure this gate
    # exists to prevent, so it is asserted rather than assumed.
    local unsynced
    unsynced=$(diff -rq --include='*.c' --include='*.h' --include='*.cc' \
        "$src/src" "$tree/src" 2>/dev/null | grep -c '^')
    check "$lab: source tree fully synced into compile tree" "$unsynced" "0"
    [ "$unsynced" = 0 ] || diff -rq --include='*.c' --include='*.h' --include='*.cc' \
        "$src/src" "$tree/src" 2>/dev/null | head -8 | sed 's/^/       /'

    cd "$tree" || return 1
    [ -f Makefile ] || { note "$lab: no Makefile, running ./configure"
                         ./configure > "$LOGDIR/configure_$lab.log" 2>&1; }
    find src -name '*.o' -delete
    rm -f gxemul
    make -j12 > "$log" 2>&1
    local rc=$?
    local warn err objs
    warn=$(grep -ciE 'warning:' "$log")
    err=$(grep -ciE 'error:' "$log")
    objs=$(find src -name '*.o' | wc -l)

    check     "$lab: make exit status"  "$rc"   "0"
    check     "$lab: warnings"          "$warn" "0"
    check     "$lab: compiler errors"   "$err"  "0"
    # EXACT, not >=. The object count is the documented tell for "make exited 2 having
    # built nothing", and >= would also miss an object that should have been removed.
    check     "$lab: objects built"     "$objs" "$want"
    check     "$lab: binary produced"   "$([ -x gxemul ] && echo yes || echo no)" "yes"
    [ "$warn" = 0 ] || grep -iE 'warning:' "$log" | head -12 | sed 's/^/       /'
    [ "$err"  = 0 ] || grep -iE 'error:'   "$log" | head -12 | sed 's/^/       /'
}

# ---- the twin trees must agree outside the known divergent set ----------
# est/ and GXEMUL-SEC/ are separate source trees, each compiled into its own build tree.
# Nothing else in this harness would notice a correction applied to one and not the other:
# both would build clean, both would boot, and pmax would quietly run the old code. The
# divergence set is a fixed, documented list, so anything outside it is an un-propagated
# edit and is asserted here rather than left to be discovered later.
DIVERGENT="devices/dev_jazz.c
devices/Makefile.skel
disk/diskimage.c
machines/machine_arc.c
promemul/arcbios.c
devices/dev_ne2000.c"

note "checking est/ vs GXEMUL-SEC/ divergence"
diff -rq --include='*.c' --include='*.h' --include='*.cc' --include='*.skel' \
    "$EST/src" "$SEC/src" 2>/dev/null \
    | sed -E 's|^Files .*/est/src/(.*) and .*|\1|; s|^Only in .*/src/?(.*): (.*)|\1/\2|; s|^//|/|' \
    | sed 's|^/||' | sort > "$LOGDIR/divergent_actual.txt"
echo "$DIVERGENT" | sort > "$LOGDIR/divergent_expected.txt"
unexpected=$(comm -23 "$LOGDIR/divergent_actual.txt" "$LOGDIR/divergent_expected.txt")
n_unexpected=$(printf '%s' "$unexpected" | grep -c '^' )
if [ -n "$unexpected" ]; then
    note "UNEXPECTED divergence (likely an un-propagated correction):"
    printf '%s\n' "$unexpected" | sed 's/^/         /'
fi
check "no divergence outside the documented set" "$n_unexpected" "0"
note "divergent files seen: $(tr '\n' ' ' < "$LOGDIR/divergent_actual.txt")"
echo

build_tree pmax "$EST" "$PMAX_TREE" 223
build_tree arc  "$SEC" "$ARC_TREE"  224

# Publish the arc binary where the rigs expect it, but only if it really built.
if [ -x "$ARC_TREE/gxemul" ]; then
    cp -f "$ARC_TREE/gxemul" /tmp/gxsec-gxemul
    [ -d "$RIG" ] && cp -f "$ARC_TREE/gxemul" "$RIG/gxsec-gxemul"
    note "arc binary published to rig and /tmp/gxsec-gxemul"
fi

gate_end
exit $?
