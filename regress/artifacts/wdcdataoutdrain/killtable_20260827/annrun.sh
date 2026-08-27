#!/bin/bash
S=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
B=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad
O=/tmp/gxann; mkdir -p "$O"
for v in _base Mstatic Mnolatch; do
  gcc -O2 -std=c99 -I"$S/src/include" -I"$S/src/include/thirdparty" \
      -ffunction-sections -fdata-sections -Wl,--gc-sections \
      -o "$O/$v" "$B/$v/regress/diff_wdc_identify.c" 2> "$O/$v.cc" || { echo "  $v DOES NOT COMPILE"; head -5 "$O/$v.cc"; continue; }
  "$O/$v" > "$O/$v.out" 2>&1
  echo "  $v: $(tail -2 "$O/$v.out" | head -1)"
  grep '^  FAIL' "$O/$v.out" | sed 's/^/      /'
done
