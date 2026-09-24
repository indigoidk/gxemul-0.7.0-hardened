#!/bin/bash
# #545 TABLE 4 (offline only; derived from run_table3.sh) -- the repaired detector (after pass 2) against EVERY mutant built so far, in scratch trees only.
#   A offline: the SHIPPED regress/diff_footbridge.c (149 rows) vs FIX + 34 mutants  (/tmp/fbd5x, a copy of SEC src)
#   B guest:   the SHIPPED footbridge_sites_probe.py (37 rows) + the two pending probes, in a clone of build/
#              (/tmp/gxfbd5c): FIX, Z9 (text swap, guest-only), M1b-M1e (exit reinstated per site)
# Frozen instruments, a sentinel per scratch tree, restore + cmp against GXEMUL-SEC, every build freshness-checked.
set -u
R=/mnt/c/DocumentNoSnc/CC/GXEMUL
SEC=$R/GXEMUL-SEC
I=$R/_scratchpad/fbd5/impl
OUT=$I/table4
mkdir -p "$OUT"; : > "$OUT/TABLE4.log"
log() { echo "$*" | tee -a "$OUT/TABLE4.log"; }
log "TABLE4_START (offline: 327-row differential vs every mutant) $(date '+%F %T')  SEC dev_footbridge.c md5 $(md5sum $SEC/src/devices/dev_footbridge.c | cut -c1-8)"

# ---------------------------------------------------------------- A offline
X=/tmp/fbd5x4
rm -rf "$X"; mkdir -p "$X/regress" "$X/frozen"; cp -a "$SEC/src" "$X/src"; cp "$R/build/config.h" "$X/config.h"
cp "$SEC/regress/diff_footbridge.c" "$X/regress/diff_footbridge.c"; cp "$SEC/regress/diff_footbridge.c" "$X/frozen/"
cp "$SEC/src/devices/dev_footbridge.c" "$X/FIX.c"
echo "#545 table3 A -- restore from FIX.c" > "$X/.MUTANT"
for M in FIX M1 M2 M3 M4 M5 M6 M7 M8 M9 M10 M11 A1 A2 A3 A4 B1 B2 B3 G1 G2 Z1 Z1b Z2 Z3 Z4 Z5 Z6 Z7 Z7b Z8 Z9 M1b M1c M1d M1e F1 F1b F1c F2 F2b F3 F3b F4 F4b F4c F5 F5b F7 F7b; do
    cp "$X/FIX.c" "$X/src/devices/dev_footbridge.c"
    case $M in
        FIX) ;;
        F*)  python3 "$R/_scratchpad/fbd5/opus_f2_20260919/mkmut_f2.py" "$X" "$M" > /dev/null || { log "$M DID NOT APPLY"; continue; } ;;
        M1b|M1c|M1d|M1e|Z*) python3 "$I/mkmut_p2b.py" "$X" "$M" > /dev/null || { log "$M DID NOT APPLY"; continue; } ;;
        M*)  python3 "$I/mkmut_fbd5.py" "$X" "$M" > /dev/null || { log "$M DID NOT APPLY"; continue; } ;;
        A4)  sed -i 's/else if (!d->warned_fiq_status_w) {/else if (len == 4 \&\& !d->warned_fiq_status_w) {/' "$X/src/devices/dev_footbridge.c" ;;
        *)   python3 "$R/_scratchpad/fbd5/opus_p2_20260919/mkmut_p2.py" "$X" "$M" > /dev/null || { log "$M DID NOT APPLY"; continue; } ;;
    esac
    ( cd "$X/regress" && gcc -O2 -std=c99 -D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE -ffunction-sections -fdata-sections -Wl,--gc-sections \
        -I"$X/src" -I"$X/src/include" -I"$X/src/include/thirdparty" -o "$X/d_$M" "$X/frozen/diff_footbridge.c" -lm > "$OUT/cc_$M.log" 2>&1 ) || { log "OFF $M COMPILE FAILED"; continue; }
    "$X/d_$M" > "$OUT/diff_$M.log" 2>&1; rc=$?
    log "$(printf 'OFF %-4s rc=%s %-24s red: %s' "$M" "$rc" "$(grep -E 'rows, ' "$OUT/diff_$M.log" | tr -d '\n')" "$(grep -E '^  FAIL  [^@]' "$OUT/diff_$M.log" | cut -c9-24 | sort -u | tr '\n' ',' | cut -c1-120)")"
done
cp "$X/FIX.c" "$X/src/devices/dev_footbridge.c"
cmp -s "$X/src/devices/dev_footbridge.c" "$SEC/src/devices/dev_footbridge.c" && rm -f "$X/.MUTANT" && log "A RESTORED (cmp == SEC), sentinel cleared"

log "TABLE4_DONE $(date '+%F %T')"
