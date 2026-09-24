#!/bin/bash
# Opus seat, #545 q2r: build the scratch tree and the BASELINE harness binary.
# Writes nothing outside /tmp/opusq2r and the opus/ output dir.
set -u
X=/tmp/opusq2r
P=/mnt/c/DocumentNoSnc/cc/GXEMUL
F=$P/_scratchpad/fbd5/q2r/frozen
O=$P/_scratchpad/fbd5/q2r/opus
rm -rf "$X"
mkdir -p "$X/regress"
cp -a "$P/GXEMUL-SEC/src" "$X/src"
cp "$P/build/config.h" "$X/config.h"
cp "$F/diff_footbridge.c" "$X/regress/diff_footbridge.c"
cp "$F/dev_footbridge.c" "$X/src/devices/dev_footbridge.c"
cp "$F/dev_footbridge.c" "$X/dev_footbridge.frozen.c"
md5sum "$X/src/devices/dev_footbridge.c" "$X/regress/diff_footbridge.c" "$X/dev_footbridge.frozen.c" "$X/config.h"
cd "$X/regress" || exit 9
T0=$(date +%s.%N)
gcc -O2 -std=c99 -D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE -ffunction-sections -fdata-sections -Wl,--gc-sections -I"$X/src" -I"$X/src/include" -I"$X/src/include/thirdparty" -o d diff_footbridge.c -lm
echo "gcc rc=$?"
T1=$(date +%s.%N)
echo "build seconds: $(echo "$T1 - $T0" | bc 2>/dev/null || echo n/a)"
ls -la --time-style=full-iso d ../src/devices/dev_footbridge.c diff_footbridge.c
./d > "$O/baseline.log" 2>&1
echo "run rc=$?"
tail -3 "$O/baseline.log"
echo "ok lines: $(grep -c '^  ok' "$O/baseline.log")"
echo "FAIL lines (all, incl selfcheck):"
grep '^  FAIL' "$O/baseline.log"
echo "SETUP_DONE"
