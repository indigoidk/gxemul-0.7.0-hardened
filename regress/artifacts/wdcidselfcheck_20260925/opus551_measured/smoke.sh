#!/bin/bash
set -u
W=/tmp/opus551p1
d=$W/dev/pristine/regress
cp $W/sec/regress/diff_wdc_identify.c $d/smoke.c
t0=$(date +%s.%N)
cc -O2 -std=c99 -I$W/sec/src/include -I$W/sec/src/include/thirdparty -ffunction-sections -fdata-sections -Wl,--gc-sections -o $d/smoke $d/smoke.c > $d/smoke.cc 2>&1; echo "cc rc=$? in $(echo "$(date +%s.%N) - $t0" | bc) s"
wc -l < $d/smoke.cc
t0=$(date +%s.%N); $d/smoke > $d/smoke.log 2>&1; echo "run rc=$? in $(echo "$(date +%s.%N) - $t0" | bc) s"
tail -4 $d/smoke.log; grep -c '^  ok' $d/smoke.log; grep -c '^  FAIL' $d/smoke.log; wc -l < $d/smoke.log
