#!/bin/bash
# Build and run the in-process differential (wit_main.c + two wit_tu.c units) for each variant id given.
# Uses ONLY /tmp/opusq2r_wit (its own base/ and var/ copies) plus read-only headers from /tmp/opusq2r/src.
# Variant sources are rebuilt from the driver's saved one-hunk diffs against the FROZEN copy.
# Special ids: BASE (var = frozen copy, the negative control).
set -u
X=/tmp/opusq2r
W=/tmp/opusq2r_wit
O=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2r/opus
FROZEN=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2r/frozen/dev_footbridge.c
MAXL=${MAXL:-3}
NRAND=${NRAND:-2000000}
mkdir -p "$W/base" "$W/var" "$O/wit"
cp "$O/wit_tu.c" "$O/wit_main.c" "$W/"
cp "$FROZEN" "$W/base/dev_footbridge.c"
cmp "$W/base/dev_footbridge.c" "$FROZEN" || { echo "base copy differs from frozen"; exit 9; }
CF="-O2 -std=c99 -D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE -ffunction-sections -fdata-sections -I$X/src -I$X/src/include -I$X/src/include/thirdparty"
cd "$W" || exit 9
gcc $CF -DPFX=base_ '-DDEVFILE="base/dev_footbridge.c"' -c wit_tu.c -o tu_base.o || exit 9
gcc $CF -c wit_main.c -o wit_main.o || exit 9
for vid in "$@"; do
	if [ "$vid" = BASE ]; then
		cp "$FROZEN" "$W/var/dev_footbridge.c"
	else
		rm -f "$W/var/dev_footbridge.c"
		patch -s -o "$W/var/dev_footbridge.c" "$W/base/dev_footbridge.c" < "$X/diffs/$vid.diff" || { echo "$vid: patch failed"; continue; }
	fi
	rm -f tu_var.o wit
	gcc $CF -DPFX=var_ '-DDEVFILE="var/dev_footbridge.c"' -c wit_tu.c -o tu_var.o || { echo "$vid: build failed"; continue; }
	gcc -Wl,--gc-sections -o wit wit_main.o tu_base.o tu_var.o -lm || { echo "$vid: link failed"; continue; }
	{
		echo "VARIANT $vid"
		if [ "$vid" != BASE ]; then grep -E '^[-+]	' "$X/diffs/$vid.diff"; fi
		md5sum var/dev_footbridge.c
		timeout 1200 ./wit "$MAXL" "$NRAND"
		echo "rc=$?"
	} > "$O/wit/$vid.txt" 2>&1
	echo "$vid: $(grep -E '^(START|RANDOM)' "$O/wit/$vid.txt" | tr '\n' ' ' | cut -c1-400)"
done
echo WIT_RUN_DONE
