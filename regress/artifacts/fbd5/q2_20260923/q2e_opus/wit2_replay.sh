#!/bin/bash
# Build the differential for ONE variant and replay one sequence: wit2_replay.sh <vid> <devinit|calloc> <op>...
# Output: $O/wit2/REPLAY_<vid>_<n>.txt (n = next free number), ending WIT2_DONE.
set -u
X=/tmp/opusq2e
W=/tmp/opusq2e_witr
O=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2e/opus
FROZEN=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2e/frozen/dev_footbridge.c
vid=$1; shift
mkdir -p "$W/base" "$W/var"
cp "$O/wit2_tu.c" "$O/wit2_main.c" "$W/"
cp "$FROZEN" "$W/base/dev_footbridge.c"
CF="-O2 -std=c99 -Wall -D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE -ffunction-sections -fdata-sections -I$X/src -I$X/src/include -I$X/src/include/thirdparty"
cd "$W" || exit 9
python3 "$O/mkvar.py" "$vid" "$W/var/dev_footbridge.c" > /dev/null || exit 9
gcc $CF -DPFX=base_ '-DDEVFILE="base/dev_footbridge.c"' -c wit2_tu.c -o tu_base.o || exit 9
gcc $CF -DPFX=var_ '-DDEVFILE="var/dev_footbridge.c"' -c wit2_tu.c -o tu_var.o || exit 9
gcc $CF -c wit2_main.c -o wit2_main.o || exit 9
gcc -Wl,--gc-sections -o wit2r wit2_main.o tu_base.o tu_var.o -lm || exit 9
n=1; while [ -e "$O/wit2/REPLAY_${vid}_$n.txt" ]; do n=$((n + 1)); done
{ echo "VARIANT $vid"; diff "$W/base/dev_footbridge.c" "$W/var/dev_footbridge.c" | grep -E '^[<>]'; ./wit2r replay "$@"; echo "rc=$?"; } > "$O/wit2/REPLAY_${vid}_$n.txt" 2>&1
cat "$O/wit2/REPLAY_${vid}_$n.txt"
