#!/bin/bash
X=/tmp/opusq2r
W=/tmp/opusq2r_x9
O=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2r/opus
F=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2r/frozen
mkdir -p "$W/base"
cp "$F/dev_footbridge.c" "$W/base/dev_footbridge.c"
cp "$O/x9check.c" "$W/"
cd "$W" || exit 9
gcc -O2 -std=c99 -D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE -ffunction-sections -fdata-sections -Wl,--gc-sections \
  -I"$X/src" -I"$X/src/include" -I"$X/src/include/thirdparty" -o x9check x9check.c -lm || exit 9
./x9check | tee "$O/x9check.out"
