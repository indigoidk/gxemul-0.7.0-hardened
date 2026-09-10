#!/bin/bash
#  #519 TABLE 2c -- after table 2b: the 19-row instrument (all-bits class closure) on the final source.
#  BASE_19, M15_texrd (re-measured: expected KILLED now by `allbits announce'), M18_sharedbit_tlba.
set -u
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad
T2=$SEC/regress/artifacts/sgirandomcolour/killtable_20260910/t2
C=/tmp/gx519
n=0
while [ ! -f $T2/SCORES2.txt ] || ! grep -q TABLE519_2B_DONE $T2/SCORES2.txt || [ -f $C/.MUTANT ]; do
    sleep 60; n=$((n+1)); [ $n -gt 150 ] && { echo "TABLE519_2C: table 2b not finished after 150 min -- not starting"; exit 7; }
done
FROZEN=$T2/sgi_re_colourdefault_probe.REPAIRED19.asrun.py
cp $SEC/regress/sgi_re_colourdefault_probe.py $FROZEN
cp $SEC/src/devices/dev_sgi_re.c $T2/BASELINE_FIX519_final.c
cp $SP/mut519x.py $T2/mut519x.py
echo "=== TABLE 2c start $(date) after $n min wait; instrument md5 $(md5sum $FROZEN | cut -c1-8), $(grep -c 'row(' $FROZEN) row( sites; baseline = SEC dev_sgi_re.c md5 $(md5sum $T2/BASELINE_FIX519_final.c | cut -c1-8) ===" | tee -a $T2/SCORES2.txt
echo "$C/.MUTANT: src/devices/dev_sgi_re.c  #519 TABLE 2c (main loop) in progress" > $C/.MUTANT
run () {
    local lbl=$1 m=$2
    cd $C || return 1
    cp $T2/BASELINE_FIX519_final.c src/devices/dev_sgi_re.c
    if [ "$m" != "BASE" ]; then
        python3 $T2/mut519x.py src/devices/dev_sgi_re.c "$m" > $T2/mutate_$lbl.log 2>&1 || { echo "$lbl MUTANT_DID_NOT_APPLY (rc=$?)" | tee -a $T2/SCORES2.txt; tail -2 $T2/mutate_$lbl.log; return 1; }
    fi
    rm -f src/devices/dev_sgi_re.o
    if ! make -j4 > $T2/build_$lbl.log 2>&1; then echo "$lbl BUILD_FAILED" | tee -a $T2/SCORES2.txt; return 1; fi
    if [ ! gxemul -nt src/devices/dev_sgi_re.c ]; then echo "$lbl STALE_BINARY" | tee -a $T2/SCORES2.txt; return 1; fi
    python3 -u $FROZEN $C/gxemul $lbl > $T2/$lbl.raw 2>&1
    local r; r=$(grep -o 'SGICOLOUR_RESULT=[0-9]*/[0-9]*' $T2/$lbl.raw | tail -1)
    local reds; reds=$(grep -E ' FAIL$' $T2/$lbl.raw | awk '{print $1" "$2}' | tr '\n' ',' | cut -c1-120)
    printf '%-20s %-8s sentinel=%-16s reds=%s\n' "$lbl" "${r#SGICOLOUR_RESULT=}" "$(tail -1 $T2/$lbl.raw)" "$reds" | tee -a $T2/SCORES2.txt
}
run BASE_19 BASE
for m in M15_texrd M18_sharedbit_tlba; do run "${m}_19" "$m"; done
echo "=== RESTORE from SEC (2c) ===" | tee -a $T2/SCORES2.txt
cp $SEC/src/devices/dev_sgi_re.c $C/src/devices/dev_sgi_re.c; cd $C && rm -f src/devices/dev_sgi_re.o && make -j4 > $T2/build_restore2c.log 2>&1
if cmp -s $C/src/devices/dev_sgi_re.c $SEC/src/devices/dev_sgi_re.c && [ $C/gxemul -nt $C/src/devices/dev_sgi_re.c ]; then rm -f $C/.MUTANT; echo "$C restored cmp-clean vs SEC, rebuilt fresh, sentinel cleared" | tee -a $T2/SCORES2.txt; else echo "*** RESTORE INCOMPLETE -- SENTINEL KEPT ***" | tee -a $T2/SCORES2.txt; fi
echo "TABLE519_2C_DONE $(date)" | tee -a $T2/SCORES2.txt
