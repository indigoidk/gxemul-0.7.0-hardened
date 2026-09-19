#!/bin/bash
#  #537 measurement: the fbpending_bound self-mutant lane.  Run under WSL Gentoo:
#     MSYS_NO_PATHCONV=1 wsl -d Gentoo -- bash /mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/t537/run537.sh
#  Writes ONLY under /tmp/sm537 and _scratchpad/t537/out.  Never writes GXEMUL-SEC: every arm that
#  needs a different harness runs from a SCRATCH COPY with its own selfmutant.py (the helper derives
#  SEC from its own location, so a copy is a self-contained tree).
#
#    L0  post-fix   : the working-tree harness + the gate's exact flags        want SELFMUTANT_OK
#    L1  pre-fix    : the HEAD harness (FBBOUND_VERDICT=PASS) + same flags      want SELFMUTANT_SETUP
#                     ("pristine arm did not PASS") -- the fbsmlane symptom, test-first
#    N1  blind      : post-fix harness with R3's `worst_trough >= 1' -> `>= 0'  want SELFMUTANT_FAIL
#                     (the lane must go red when the detector stops seeing the mutant)
#    N2  absolute -I: post-fix harness, -I$SEC/src/devices instead of ../     want SELFMUTANT_SETUP
#                     (both arms compile the PRISTINE copy -> binary-identity check; checks the
#                     comment gate_offline.sh now carries)
#    D0  direct     : the post-fix harness built as gate 2's main lane builds it, run WITH and
#                     WITHOUT the depth argument -- the lane runs it without one, so the
#                     no-depth IDENTITY path must be green on its own
set -u
ROOT=/mnt/c/DocumentNoSnc/CC/GXEMUL
SEC=$ROOT/GXEMUL-SEC
OUT=$ROOT/_scratchpad/t537/out
S=/tmp/sm537
rm -rf "$S" "$OUT"; mkdir -p "$S" "$OUT"

OBJS=$(find "$SEC/../build/src" -name '*.o' ! -name 'main.o' ! -name 'dev_footbridge.o' 2>/dev/null | sort | tr '\n' ' ')
NOBJ=$(printf '%s' "$OBJS" | wc -w)
echo "build/ objects linked: $NOBJ" | tee "$OUT/SUMMARY.txt"
[ "$NOBJ" -gt 100 ] || { echo "ABORT: too few build/ objects ($NOBJ)" | tee -a "$OUT/SUMMARY.txt"; exit 3; }
#  build/ freshness, recorded not asserted: the objects are what the lane links.
echo "build/gxemul mtime: $(stat -c %y "$SEC/../build/gxemul" 2>/dev/null)" | tee -a "$OUT/SUMMARY.txt"

XF_REL="-std=gnu99 -I../src/include -I../src/include/thirdparty -I../src/devices $OBJS -L/usr/X11R6/lib -lX11"

mkcopy() {  # dir harness-source-file -> a self-contained GXEMUL-SEC copy
    local d=$1/GXEMUL-SEC
    mkdir -p "$d/regress/selfmutants"
    cp -a "$SEC/src" "$d/src"
    #  misc.h includes "../../config.h" -- the configure-generated GXEMUL-SEC/config.h.  The helper's own
    #  mirror reaches it through its SYMLINKED src/include (the kernel resolves `..` after the link);
    #  a real copy of src/ does not, so run 1 of this script SETUP'd L1/N1 on a compile error.
    cp "$SEC/config.h" "$d/config.h"
    cp "$SEC/regress/selfmutant.py" "$d/regress/"
    cp "$SEC/regress/selfmutants/fbpending_bound.old" "$SEC/regress/selfmutants/fbpending_bound.new" "$d/regress/selfmutants/"
    cp "$2" "$d/regress/diff_fbpending_bound.c"
}

lane() {  # tag sec-root xflags
    local tag=$1 sc=$2 xf=$3 rc
    ( cd /tmp && SELFMUTANT_EXTRA_FLAGS="$xf" python3 "$sc/regress/selfmutant.py" \
        diff_fbpending_bound.c src/devices/dev_footbridge.c \
        "$sc/regress/selfmutants/fbpending_bound.old" "$sc/regress/selfmutants/fbpending_bound.new" \
        "R4 every case bounded" ) > "$OUT/$tag.txt" 2>&1
    rc=$?
    echo "$tag rc=$rc token=$(grep -oE 'SELFMUTANT_(OK|FAIL|SETUP)' "$OUT/$tag.txt" | tail -1)" | tee -a "$OUT/SUMMARY.txt"
    grep -E '^       ' "$OUT/$tag.txt" | sed 's/^/    /' | tee -a "$OUT/SUMMARY.txt"
}

#  L0 -- the REAL tree's helper and harness, exactly as gate_offline.sh's selfmutant_one calls it.
lane L0_postfix "$SEC" "$XF_REL"

#  L1 -- pre-fix: HEAD's harness in a scratch copy.
git -C "$SEC" show HEAD:regress/diff_fbpending_bound.c > "$S/harness.HEAD.c" 2>/dev/null \
    || cp "$ROOT/_scratchpad/t537/diff_fbpending_bound.HEAD.c" "$S/harness.HEAD.c"
grep -c 'FBBOUND_VERDICT=' "$S/harness.HEAD.c" | sed 's/^/HEAD harness FBBOUND_VERDICT lines: /' | tee -a "$OUT/SUMMARY.txt"
mkcopy "$S/pre" "$S/harness.HEAD.c"
lane L1_prefix "$S/pre/GXEMUL-SEC" "$XF_REL"

#  N1 -- the detector blinded: R3 accepts a trough of 0, so the 1 -> 0 mutant is no longer seen.
sed 's/worst_trough >= 1,/worst_trough >= 0,/' "$SEC/regress/diff_fbpending_bound.c" > "$S/harness.blind.c"
echo "N1 edit applied: $(diff "$SEC/regress/diff_fbpending_bound.c" "$S/harness.blind.c" | grep -c '^>') line(s)" | tee -a "$OUT/SUMMARY.txt"
mkcopy "$S/blind" "$S/harness.blind.c"
lane N1_blind "$S/blind/GXEMUL-SEC" "$XF_REL"

#  N2 -- an ABSOLUTE -I to the real tree's src/devices: both arms compile the pristine subject.
XF_ABS="-std=gnu99 -I$SEC/src/include -I$SEC/src/include/thirdparty -I$SEC/src/devices $OBJS -L/usr/X11R6/lib -lX11"
lane N2_absolute "$SEC" "$XF_ABS"

#  D0 -- the harness directly, as gate 2's main lane builds it.
( cd "$SEC/regress" && gcc -O2 -std=gnu99 -I"$SEC/src/include" -I"$SEC/src/include/thirdparty" \
    -I"$SEC/src/devices" -o "$S/fbbound" diff_fbpending_bound.c $OBJS -lm -L/usr/X11R6/lib -lX11 ) > "$OUT/D0_build.txt" 2>&1
echo "D0 build rc=$?" | tee -a "$OUT/SUMMARY.txt"
"$S/fbbound" 2147487744 > "$OUT/D0_deep.txt" 2>&1; echo "D0 deep rc=$?  $(grep -E '^FBBOUND_(PASS|FAIL)$|IDENTITY' "$OUT/D0_deep.txt" | tr '\n' ' ')" | tee -a "$OUT/SUMMARY.txt"
"$S/fbbound" > "$OUT/D0_shallow.txt" 2>&1; echo "D0 shallow rc=$?  $(grep -E '^FBBOUND_(PASS|FAIL)$|IDENTITY' "$OUT/D0_shallow.txt" | tr '\n' ' ')" | tee -a "$OUT/SUMMARY.txt"
echo "D0 deep: FBBOUND_VERDICT lines $(grep -c 'FBBOUND_VERDICT' "$OUT/D0_deep.txt"), ^FBBOUND_PASS\$ lines $(grep -c '^FBBOUND_PASS$' "$OUT/D0_deep.txt")" | tee -a "$OUT/SUMMARY.txt"

rm -rf "$S"
echo "RUN537_DONE" | tee -a "$OUT/SUMMARY.txt"
