#!/bin/bash
S=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
Q=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/q4
O=/tmp/gxq4; mkdir -p "$O"
for m in D1_renumber D2_rowsplusplus E1_pkt; do
    gcc -O2 -std=c99 -I"$S/src/include" -I"$S/src/include/thirdparty" \
        -ffunction-sections -fdata-sections -Wl,--gc-sections \
        -o "$O/b_$m" "$Q/$m/regress/diff_wdc_identify.c" 2> "$O/$m.cc"
    if [ $? -ne 0 ]; then printf "  %-18s COMPILEFAIL\n" "$m"; head -3 "$O/$m.cc"; continue; fi
    "$O/b_$m" > "$O/$m.out" 2>&1
    printf "  %-18s %s   verdict=%s\n" "$m" \
        "$(grep -oE '^[0-9]+ rows, [0-9]+ failures' "$O/$m.out")" \
        "$(grep -oE 'WDC_IDENTIFY_(PASS|FAIL)' "$O/$m.out")"
done
