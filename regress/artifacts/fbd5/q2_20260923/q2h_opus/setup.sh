#!/bin/bash
# Opus seat, #545 repair-3e pass (q2h): scratch tree + BASELINE of BOTH the frozen 3d harness (6c92d7e5)
# and the frozen 3e harness (15a1c2a2, under review), on the frozen device (783c0c7f).
set -u
X=/tmp/opusr3e
P=/mnt/c/DocumentNoSnc/cc/GXEMUL
F=$P/_scratchpad/fbd5/q2h/frozen
O=$P/_scratchpad/fbd5/q2h/opus
rm -rf "$X"
mkdir -p "$X/regress"
cp -a "$P/GXEMUL-SEC/src" "$X/src"
cp "$P/build/config.h" "$X/config.h"
cp "$F/diff_footbridge.c"     "$X/regress/diff_footbridge.3e.c"
cp "$F/diff_footbridge.r3d.c" "$X/regress/diff_footbridge.3d.c"
cp "$F/dev_footbridge.c"      "$X/src/devices/dev_footbridge.c"
echo "=== integrity ==="
cmp "$X/src/devices/dev_footbridge.c" "$F/dev_footbridge.c" && echo "scratch device == frozen"
cmp "$X/src/devices/dev_footbridge.c" "$P/GXEMUL-SEC/src/devices/dev_footbridge.c" && echo "frozen device == SEC device"
cmp "$F/diff_footbridge.c" "$P/GXEMUL-SEC/regress/diff_footbridge.c" && echo "frozen 3e harness == SEC harness"
md5sum "$X/src/devices/dev_footbridge.c" "$X/regress/diff_footbridge.3e.c" "$X/regress/diff_footbridge.3d.c" "$X/config.h"
CF() { gcc -O2 -std=c99 -Wall -D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE -ffunction-sections -fdata-sections \
    -Wl,--gc-sections -I"$X/src" -I"$X/src/include" -I"$X/src/include/thirdparty" -o "$2" "$1" -lm ; }
cd "$X/regress" || exit 9
echo "=== build 3e ==="
CF diff_footbridge.3e.c d3e 2> "$O/build_3e.err"
echo "gcc 3e rc=$? warnings=$(grep -c 'warning:' "$O/build_3e.err")"
[ d3e -nt ../src/devices/dev_footbridge.c ] && echo "3e binary newer than device"
./d3e > "$O/baseline_3e.log" 2>&1 ; echo "3e run rc=$?"
tail -2 "$O/baseline_3e.log"
echo "=== build 3d ==="
CF diff_footbridge.3d.c d3d 2> "$O/build_3d.err"
echo "gcc 3d rc=$? warnings=$(grep -c 'warning:' "$O/build_3d.err")"
./d3d > "$O/baseline_3d.log" 2>&1 ; echo "3d run rc=$?"
tail -2 "$O/baseline_3d.log"
echo "=== cross-checks ==="
cmp "$O/baseline_3e.log" "$P/GXEMUL-SEC/regress/artifacts/fbd5/q2_20260923/r3e_20260923/diff_FIX.log" \
    && echo "3e baseline == main-loop r3e diff_FIX.log (byte-identical)" || echo "3e baseline != main-loop r3e diff_FIX.log"
cmp "$O/baseline_3d.log" "$P/GXEMUL-SEC/regress/artifacts/fbd5/q2_20260923/r3d_20260923/diff_FIX.log" \
    && echo "3d baseline == main-loop r3d diff_FIX.log (byte-identical)" || echo "3d baseline != main-loop r3d diff_FIX.log"
md5sum d3e d3d
echo SETUP_DONE
