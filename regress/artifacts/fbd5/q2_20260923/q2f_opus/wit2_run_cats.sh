#!/bin/bash
# Build and run the in-process differential (wit2_main.c + two wit2_tu.c units) for each variant id given.
# Uses ONLY its own directory $W (its own base/ and var/ copies), plus read-only headers from /tmp/opusq2f/src.
# Special id: BASE (var = the frozen copy -- the negative control).  Output: $O/wit2/<vid>.txt, ending WIT2_DONE.
set -u
X=/tmp/opusq2f
W=${W:-/tmp/opusq2f_wit}
O=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2f/opus
FROZEN=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2f/frozen/dev_footbridge.c
MAXL=${MAXL:-3}
NRAND=${NRAND:-1000000}
mkdir -p "$W/base" "$W/var" "$O/wit2_cats"
cp "$O/wit2_tu.c" "$O/wit2_main.c" "$W/"
cp "$FROZEN" "$W/base/dev_footbridge.c"
cmp "$W/base/dev_footbridge.c" "$FROZEN" || { echo "base copy differs from frozen"; exit 9; }
CF="-O2 -std=c99 -Wall -D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE -ffunction-sections -fdata-sections -I$X/src -I$X/src/include -I$X/src/include/thirdparty"
cd "$W" || exit 9
gcc $CF -DPFX=base_ '-DDEVFILE="base/dev_footbridge.c"' -c wit2_tu.c -o tu_base.o || exit 9
gcc $CF -c wit2_main.c -o wit2_main.o || exit 9
for vid in "$@"; do
	rm -f "$W/var/dev_footbridge.c" tu_var.o wit2
	python3 "$O/mkvar.py" "$vid" "$W/var/dev_footbridge.c" > /dev/null || { echo "$vid: mkvar failed"; continue; }
	gcc $CF -DPFX=var_ '-DDEVFILE="var/dev_footbridge.c"' -c wit2_tu.c -o tu_var.o 2> "$W/var_build.err" \
	    || { echo "$vid: build failed"; cat "$W/var_build.err"; continue; }
	gcc -Wl,--gc-sections -o wit2 wit2_main.o tu_base.o tu_var.o -lm || { echo "$vid: link failed"; continue; }
	{
		echo "VARIANT $vid"
		diff "$W/base/dev_footbridge.c" "$W/var/dev_footbridge.c" | grep -E '^[<>]'
		md5sum var/dev_footbridge.c
		timeout 3000 ./wit2 "$MAXL" "$NRAND"
		echo "rc=$?"
	} > "$O/wit2_cats/$vid.txt" 2>&1
	echo "$vid: $(grep -E '^(START|RANDOM)' "$O/wit2_cats/$vid.txt" | sed -E 's/first appearance of a divergence: //' | tr '\n' ' ' | cut -c1-600)"
done
echo WIT2_RUN_DONE
