#!/bin/bash
# #545 pass-2 repair, re-measured by the main loop: the SHIPPED differential (HEAD + P-rows + X-rows, IDENTITY 134, the
# exact file now in GXEMUL-SEC) against the FIX and every mutant that escaped the pre-repair detector (Opus pass 2:
# A1-A4, B1-B3, G1, G2; M11 from table 2), plus the pre-repair table's mutants M1-M10 so no earlier kill is lost.
# Offline only: one gcc + one run per mutant, in /tmp/fbd5x (a copy of GXEMUL-SEC/src); no project tree written.
set -u
R=/mnt/c/DocumentNoSnc/CC/GXEMUL
SEC=$R/GXEMUL-SEC
X=/tmp/fbd5x
OUT=$R/_scratchpad/fbd5/impl/xtable
mkdir -p "$OUT"; : > "$OUT/XTABLE.log"
rm -rf "$X"; mkdir -p "$X/regress"; cp -a "$SEC/src" "$X/src"; cp "$R/build/config.h" "$X/config.h"
cp "$SEC/regress/diff_footbridge.c" "$X/regress/diff_footbridge.c"
cp "$SEC/src/devices/dev_footbridge.c" "$X/FIX.c"
echo "#545 xtable -- $X/src/devices/dev_footbridge.c mutated; restore = FIX.c" > "$X/.MUTANT"
grep -c '"134"' "$X/regress/diff_footbridge.c" | sed 's/^/identity pin 134 present: /' | tee -a "$OUT/XTABLE.log"
for M in FIX M1 M2 M3 M4 M5 M6 M7 M8 M9 M10 M11 A1 A2 A3 A4 B1 B2 B3 G1 G2; do
    cp "$X/FIX.c" "$X/src/devices/dev_footbridge.c"
    case $M in
        FIX) ;;
        M*)  python3 "$R/_scratchpad/fbd5/impl/mkmut_fbd5.py" "$X" "$M" > /dev/null || { echo "$M DID NOT APPLY" | tee -a "$OUT/XTABLE.log"; continue; } ;;
        A4)  sed -i 's/else if (!d->warned_fiq_status_w) {/else if (len == 4 \&\& !d->warned_fiq_status_w) {/' "$X/src/devices/dev_footbridge.c"
             [ "$(grep -c 'len == 4 && !d->warned_fiq_status_w' "$X/src/devices/dev_footbridge.c")" = 1 ] || { echo "A4 DID NOT APPLY" | tee -a "$OUT/XTABLE.log"; continue; } ;;
        *)   python3 "$R/_scratchpad/fbd5/opus_p2_20260919/mkmut_p2.py" "$X" "$M" > /dev/null || { echo "$M DID NOT APPLY" | tee -a "$OUT/XTABLE.log"; continue; } ;;
    esac
    ( cd "$X/regress" && gcc -O2 -std=c99 -D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE -ffunction-sections -fdata-sections -Wl,--gc-sections \
        -I"$X/src" -I"$X/src/include" -I"$X/src/include/thirdparty" -o "$X/d_$M" ./diff_footbridge.c -lm > "$OUT/cc_$M.log" 2>&1 ) || { echo "$M COMPILE FAILED" | tee -a "$OUT/XTABLE.log"; continue; }
    "$X/d_$M" > "$OUT/diff_$M.log" 2>&1; rc=$?
    printf '%-4s rc=%s %s  red: %s\n' "$M" "$rc" "$(grep -E 'rows, ' "$OUT/diff_$M.log" | tr -d '\n')" \
        "$(grep -E '^  FAIL  [^@]' "$OUT/diff_$M.log" | cut -c9-40 | cut -d: -f1 | sort -u | tr '\n' ',' | cut -c1-150)" | tee -a "$OUT/XTABLE.log"
done
cp "$X/FIX.c" "$X/src/devices/dev_footbridge.c"
cmp -s "$X/src/devices/dev_footbridge.c" "$SEC/src/devices/dev_footbridge.c" && rm -f "$X/.MUTANT" && echo "RESTORED, sentinel cleared" | tee -a "$OUT/XTABLE.log"
echo XTABLE_DONE | tee -a "$OUT/XTABLE.log"
