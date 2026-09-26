#!/bin/bash
set -u
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus551p1
W=/tmp/opus551p1
F="-std=c99 -I$W/sec/src/include -I$W/sec/src/include/thirdparty -ffunction-sections -fdata-sections -Wl,--gc-sections"
python3 $SP/xform.py make $W/sec/regress/diff_wdc_identify.c $W/h/E_eq1c.c E_eq1c > /dev/null
for dev in pristine selfmut cyl13; do
    d=$W/dev/$dev/regress; cp $W/h/E_eq1c.c $d/
    rm -f $d/E_eq1c.O2
    cc -O2 $F -o $d/E_eq1c.O2 $d/E_eq1c.c > $d/E_eq1c.O2.cc 2>&1 && [ $d/E_eq1c.O2 -nt $d/E_eq1c.c ] || { echo "BUILD FAIL $dev"; continue; }
    $d/E_eq1c.O2 > $d/E_eq1c.O2.log 2>&1; rc=$?
    echo "$dev rc=$rc: $(grep -cE '^  FAIL' $d/E_eq1c.O2.log) FAIL lines | $(grep -E '^[0-9]+ rows' $d/E_eq1c.O2.log) | $(grep -oE 'WDC_IDENTIFY_(PASS|FAIL)' $d/E_eq1c.O2.log) | $(grep SELFCHECK $d/E_eq1c.O2.log | sed 's/^ *//')"
    grep -E '^  FAIL' $d/E_eq1c.O2.log | head -3
done
