#!/bin/bash
# Opus seat, #545 repair-3d pass (q2g): scratch tree + BASELINE of the frozen 864-row 3d harness (6c92d7e5).
set -u
X=/tmp/opusr3d
P=/mnt/c/DocumentNoSnc/cc/GXEMUL
F=$P/_scratchpad/fbd5/q2g/frozen
O=$P/_scratchpad/fbd5/q2g/opus
rm -rf "$X"
mkdir -p "$X/regress"
cp -a "$P/GXEMUL-SEC/src" "$X/src"
cp "$P/build/config.h" "$X/config.h"
cp "$F/diff_footbridge.c" "$X/regress/diff_footbridge.c"
cp "$F/dev_footbridge.c" "$X/src/devices/dev_footbridge.c"
cmp "$X/src/devices/dev_footbridge.c" "$F/dev_footbridge.c" && echo "scratch device == frozen (cmp clean)"
cmp "$X/src/devices/dev_footbridge.c" "$P/GXEMUL-SEC/src/devices/dev_footbridge.c" && echo "frozen device == SEC device (cmp clean)"
cmp "$X/regress/diff_footbridge.c" "$F/diff_footbridge.c" && echo "scratch harness == frozen (cmp clean)"
cmp "$F/diff_footbridge.c" "$P/GXEMUL-SEC/regress/diff_footbridge.c" && echo "frozen harness == SEC harness (cmp clean)" || echo "frozen harness != SEC harness (SEC working copy differs)"
md5sum "$X/src/devices/dev_footbridge.c" "$X/regress/diff_footbridge.c" "$X/config.h" "$P/GXEMUL-SEC/regress/diff_footbridge.c" "$P/GXEMUL-SEC/regress/gate_offline.sh"
cd "$X/regress" || exit 9
gcc -O2 -std=c99 -Wall -D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE -ffunction-sections -fdata-sections -Wl,--gc-sections -I"$X/src" -I"$X/src/include" -I"$X/src/include/thirdparty" -o d diff_footbridge.c -lm 2> "$O/baseline_build.err"
echo "gcc rc=$? warnings=$(grep -c 'warning:' "$O/baseline_build.err")"
[ d -nt ../src/devices/dev_footbridge.c ] && echo "binary newer than device source"
./d > "$O/baseline.log" 2>&1
echo "run rc=$?"
tail -3 "$O/baseline.log"
echo "ok lines: $(grep -c '^  ok' "$O/baseline.log")  FAIL lines excl. selfcheck: $(grep '^  FAIL' "$O/baseline.log" | grep -vc '@@SELFCHECK@@')"
cmp "$O/baseline.log" "$P/GXEMUL-SEC/regress/artifacts/fbd5/q2_20260923/r3d_20260923/diff_FIX.log" && echo "baseline == the main loop r3d diff_FIX.log (byte-identical)"
md5sum d
echo SETUP_DONE
