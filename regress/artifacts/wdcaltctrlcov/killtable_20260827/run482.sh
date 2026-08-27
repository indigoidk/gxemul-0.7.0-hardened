#!/bin/bash
S=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
C=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/r482
O=/tmp/gx482; mkdir -p "$O"
gcc -O2 -std=c99 -I"$S/src/include" -I"$S/src/include/thirdparty" \
    -ffunction-sections -fdata-sections -Wl,--gc-sections \
    -o "$O/b482" "$C/regress/diff_wdc_identify.c" 2> "$O/b482.cc"
if [ $? -ne 0 ]; then echo COMPILEFAIL; head -8 "$O/b482.cc"; exit 1; fi
"$O/b482" > "$O/BASE482.out" 2>&1
grep -E 'ATA write alone|packet alone|0x88 control' "$O/BASE482.out"
tail -2 "$O/BASE482.out"
