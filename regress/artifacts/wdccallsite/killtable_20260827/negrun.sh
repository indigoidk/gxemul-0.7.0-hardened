#!/bin/bash
S=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
N=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/negctl
gcc -O2 -std=c99 -I"$S/src/include" -I"$S/src/include/thirdparty" \
    -ffunction-sections -fdata-sections -Wl,--gc-sections \
    -o /tmp/negb "$N/regress/diff_wdc_identify.c" 2>/tmp/neg.cc
rc=$?
if [ $rc -ne 0 ]; then echo "COMPILEFAIL rc=$rc"; head -6 /tmp/neg.cc; exit 1; fi
/tmp/negb > /tmp/neg.out 2>&1
echo "  detector says : $(grep -oE '^[0-9]+ rows, [0-9]+ failures' /tmp/neg.out)  $(grep -oE 'WDC_IDENTIFY_(PASS|FAIL)' /tmp/neg.out)"
echo "  -- so the COUNT PIN and the failure count both pass this mutation --"
echo "  new gate check : got $(grep -c 'a rejected command still resets' /tmp/neg.out)  want 1"
