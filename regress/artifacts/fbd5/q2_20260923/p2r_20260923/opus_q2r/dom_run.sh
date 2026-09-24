#!/bin/bash
# Targeted differential for the four dom_* variants, in its own dir (never /tmp/opusq2r/src).
X=/tmp/opusq2r
W=/tmp/opusq2r_dom
O=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2r/opus
FROZEN=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2r/frozen/dev_footbridge.c
mkdir -p "$W/base" "$W/var"
cp "$O/wit_tu.c" "$O/dom_main.c" "$W/"
cp "$FROZEN" "$W/base/dev_footbridge.c"
CF="-O2 -std=c99 -D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE -ffunction-sections -fdata-sections -I$X/src -I$X/src/include -I$X/src/include/thirdparty"
cd "$W" || exit 9
gcc $CF -DPFX=base_ '-DDEVFILE="base/dev_footbridge.c"' -c wit_tu.c -o tu_base.o || exit 9
gcc $CF -c dom_main.c -o dom_main.o || exit 9
: > "$O/dom_witness.txt"
for vid in ${VIDS:-BASE dom_idata_len4 dom_idata_lenne1 dom_fold_from180 dom_fold_from100 c_dir_A2_len4 idata_A2_ne20}; do
	if [ "$vid" = BASE ]; then cp "$FROZEN" var/dev_footbridge.c
	else rm -f var/dev_footbridge.c; patch -s -o var/dev_footbridge.c base/dev_footbridge.c < "$X/diffs/$vid.diff" || continue; fi
	gcc $CF -DPFX=var_ '-DDEVFILE="var/dev_footbridge.c"' -c wit_tu.c -o tu_var.o || continue
	gcc -Wl,--gc-sections -o dom dom_main.o tu_base.o tu_var.o -lm || continue
	{ echo "VARIANT $vid"; ./dom; echo "rc=$?"; } >> "$O/dom_witness.txt" 2>&1
done
cat "$O/dom_witness.txt"
