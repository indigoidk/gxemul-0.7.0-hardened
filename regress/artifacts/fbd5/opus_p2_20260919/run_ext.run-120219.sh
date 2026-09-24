#!/bin/bash
# Candidate repair rows measured against the fix and the escapes -- compile-only, in /tmp/gxopusfbd5p2/ext (the clone's src is NOT mutated).
set -u
ROOT=/mnt/c/DocumentNoSnc/CC/GXEMUL
SEC=$ROOT/GXEMUL-SEC
ME=$ROOT/_scratchpad/fbd5/opus_p2_20260919
CLONE=/tmp/gxopusfbd5p2
EXT=$CLONE/ext
rm -rf "$EXT"; mkdir -p "$EXT/x" "$EXT/src/devices" "$EXT/out"
python3 - "$SEC/regress/diff_footbridge.c" "$ME/ext_block.c" "$EXT/x/diff_ext.c" <<'PY'
import io, sys
s = io.open(sys.argv[1], encoding='utf-8', newline='').read()
blk = io.open(sys.argv[2], encoding='utf-8', newline='').read()
anchor = '\t/*  IDENTITY, as every differential here carries.'
assert s.count(anchor) == 1
s = s.replace(anchor, blk + anchor)
io.open(sys.argv[3], 'w', encoding='utf-8', newline='').write(s)
PY
cp "$SEC/src/devices/dev_footbridge.c" "$EXT/FIX.c"
for M in FIX A1 A2 A3 B1 B2 B3 G1 G2 M11 A4; do
    mkdir -p "$EXT/t_$M/src/devices" "$EXT/t_$M/x"
    cp "$EXT/FIX.c" "$EXT/t_$M/src/devices/dev_footbridge.c"
    cp "$EXT/x/diff_ext.c" "$EXT/t_$M/x/"
    if [ $M = M11 ]; then python3 "$ROOT/_scratchpad/fbd5/impl/mkmut_fbd5.py" "$EXT/t_$M" M11 >/dev/null || echo "$M NOAPPLY"
    elif [ $M = A4 ]; then sed -i 's/else if (!d->warned_fiq_status_w) {/else if (len == 4 \&\& !d->warned_fiq_status_w) {/' "$EXT/t_$M/src/devices/dev_footbridge.c"; grep -c 'len == 4 && !d->warned_fiq_status_w' "$EXT/t_$M/src/devices/dev_footbridge.c"
    elif [ $M != FIX ]; then python3 "$ME/mkmut_p2.py" "$EXT/t_$M" $M >/dev/null || echo "$M NOAPPLY"; fi
    ( cd "$EXT/t_$M/x" && gcc -O2 -std=c99 -D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE -ffunction-sections -fdata-sections -Wl,--gc-sections \
        -I"$CLONE/src" -I"$CLONE/src/include" -I"$CLONE/src/include/thirdparty" -I"$CLONE/regress" \
        -o "$EXT/out/d_$M" ./diff_ext.c -lm > "$EXT/out/c_$M.log" 2>&1 ) || { echo "EXT_$M COMPILE FAIL"; tail -5 "$EXT/out/c_$M.log"; continue; }
    "$EXT/out/d_$M" > "$EXT/out/r_$M.log" 2>&1; rc=$?
    echo "EXT_$M rc=$rc $(grep -E 'rows, ' "$EXT/out/r_$M.log") red: $(grep -E '^  FAIL ' "$EXT/out/r_$M.log" | grep -v SELFCHECK | cut -c9-80 | tr '\n' '|')"
done
mkdir -p "$ME/ext_logs"; cp "$EXT/out/"r_*.log "$ME/ext_logs/"
echo EXT_DONE
