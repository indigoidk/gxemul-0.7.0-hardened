#!/bin/bash
S=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
P=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/prefixtree
O=/tmp/gxprefix; mkdir -p "$O"
gcc -O2 -std=c99 -I"$S/src/include" -I"$S/src/include/thirdparty" \
    -ffunction-sections -fdata-sections -Wl,--gc-sections \
    -o "$O/prefix" "$P/regress/diff_wdc_identify.c" 2> "$O/prefix.cc"
if [ $? -ne 0 ]; then echo COMPILEFAIL; head -6 "$O/prefix.cc"; exit 1; fi
"$O/prefix" > "$O/PREFIX_committed_device.out" 2>&1
grep '^  FAIL' "$O/PREFIX_committed_device.out"
tail -2 "$O/PREFIX_committed_device.out"
