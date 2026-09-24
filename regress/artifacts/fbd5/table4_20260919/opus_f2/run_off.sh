#!/bin/bash
# Opus f2: OFFLINE half -- the shipped diff_footbridge.c vs FIX + the f2 mutants, in /tmp/gxopusf2x (copy of SEC src).
set -u
R=/mnt/c/DocumentNoSnc/CC/GXEMUL; SEC=$R/GXEMUL-SEC; D=$R/_scratchpad/fbd5/opus_f2_20260919; OUT=$D/off
mkdir -p "$OUT"; : > "$D/OFF.log"
log() { echo "$*" | tee -a "$D/OFF.log"; }
X=/tmp/gxopusf2x
rm -rf "$X"; mkdir -p "$X/frozen"; cp -a "$SEC/src" "$X/src"; cp "$R/build/config.h" "$X/config.h"
cp "$SEC/regress/diff_footbridge.c" "$X/frozen/"; cp "$SEC/src/devices/dev_footbridge.c" "$X/FIX.c"
cp "$D/mkmut_f2.py" "$X/frozen/"
echo "opus f2 offline -- restore dev_footbridge.c from SEC" > "$X/.MUTANT"
log "OFF_START $(date '+%F %T') SEC md5 $(md5sum $SEC/src/devices/dev_footbridge.c | cut -c1-8) diff md5 $(md5sum $X/frozen/diff_footbridge.c | cut -c1-8)"
for M in FIX "$@"; do
    cp "$X/FIX.c" "$X/src/devices/dev_footbridge.c"
    [ $M = FIX ] || python3 "$X/frozen/mkmut_f2.py" "$X" "$M" > /dev/null || { log "$M DID NOT APPLY"; continue; }
    ( cd "$X" && gcc -O2 -std=c99 -D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE -ffunction-sections -fdata-sections -Wl,--gc-sections \
        -I"$X/src" -I"$X/src/include" -I"$X/src/include/thirdparty" -o "$X/d_$M" "$X/frozen/diff_footbridge.c" -lm > "$OUT/cc_$M.log" 2>&1 ) || { log "OFF $M COMPILE FAILED"; continue; }
    "$X/d_$M" > "$OUT/diff_$M.log" 2>&1; rc=$?
    log "$(printf 'OFF %-4s rc=%s %-24s red: %s' "$M" "$rc" "$(grep -E 'rows, ' "$OUT/diff_$M.log" | tr -d '\n')" "$(grep -E '^  FAIL  [^@]' "$OUT/diff_$M.log" | cut -c9-75 | tr '\n' '|' | cut -c1-300)")"
done
cp "$X/FIX.c" "$X/src/devices/dev_footbridge.c"
cmp -s "$X/src/devices/dev_footbridge.c" "$SEC/src/devices/dev_footbridge.c" && rm -f "$X/.MUTANT" && log "OFF RESTORED (cmp == SEC), sentinel cleared"
log "OFF_DONE $(date '+%F %T')"
