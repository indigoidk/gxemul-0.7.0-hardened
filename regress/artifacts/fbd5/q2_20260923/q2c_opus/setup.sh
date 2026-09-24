#!/bin/bash
# Opus seat, #545 q2c (closing pass): build the scratch tree and the BASELINE 707-row harness binary.
# Writes nothing outside /tmp/opusq2c and the opus/ output dir.
set -u
X=/tmp/opusq2c
P=/mnt/c/DocumentNoSnc/cc/GXEMUL
F=$P/_scratchpad/fbd5/q2c/frozen
O=$P/_scratchpad/fbd5/q2c/opus
rm -rf "$X"
mkdir -p "$X/regress"
cp -a "$P/GXEMUL-SEC/src" "$X/src"
cp "$P/build/config.h" "$X/config.h"
cp "$F/diff_footbridge.c" "$X/regress/diff_footbridge.c"
cp "$F/dev_footbridge.c" "$X/src/devices/dev_footbridge.c"
cmp "$X/src/devices/dev_footbridge.c" "$F/dev_footbridge.c" && echo "scratch device == frozen (cmp clean)"
cmp "$X/regress/diff_footbridge.c" "$F/diff_footbridge.c" && echo "scratch harness == frozen (cmp clean)"
md5sum "$X/src/devices/dev_footbridge.c" "$X/regress/diff_footbridge.c" "$X/config.h"
cd "$X/regress" || exit 9
gcc --version | head -1
gcc -O2 -std=c99 -Wall -D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE -ffunction-sections -fdata-sections -Wl,--gc-sections -I"$X/src" -I"$X/src/include" -I"$X/src/include/thirdparty" -o d diff_footbridge.c -lm
echo "gcc rc=$?"
[ d -nt ../src/devices/dev_footbridge.c ] && echo "binary newer than device source"
./d > "$O/baseline.log" 2>&1
echo "run rc=$?"
tail -3 "$O/baseline.log"
echo "ok lines: $(grep -c '^  ok' "$O/baseline.log")"
echo "FAIL lines (all, incl selfcheck):"
grep '^  FAIL' "$O/baseline.log"
md5sum d
echo SETUP_DONE
