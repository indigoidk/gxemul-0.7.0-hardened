#!/bin/bash
S=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
N=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/r482nh
O=/tmp/gxnh; mkdir -p "$O"
gcc -O2 -std=c99 -I"$S/src/include" -I"$S/src/include/thirdparty" \
    -ffunction-sections -fdata-sections -Wl,--gc-sections \
    -o "$O/bnh" "$N/regress/diff_wdc_identify.c" 2>"$O/bnh.cc" || { echo COMPILEFAIL; head -4 "$O/bnh.cc"; exit 1; }
"$O/bnh" > "$O/NOHELPER_100row.out" 2>&1
echo "  Md_nohelper vs the 100-row detector:"
grep '^  FAIL' "$O/NOHELPER_100row.out" | sed 's/^  FAIL //' | cut -c1-42 | sed 's/^/    /'
tail -2 "$O/NOHELPER_100row.out" | sed 's/^/  /'
