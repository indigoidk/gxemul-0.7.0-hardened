#!/bin/bash
#  #519 TABLE 2b -- after run519c.sh's table 2 has restored /tmp/gx519: BASE on the FINAL source (the announce's
#  bracket edit landed after table 2's baseline copy if this file says so), M16_dropcase_rgb, M17_dropcase_rgba.
set -u
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad
T2=$SEC/regress/artifacts/sgirandomcolour/killtable_20260910/t2
C=/tmp/gx519
n=0
while [ ! -f $T2/SCORES2.txt ] || ! grep -q TABLE519_2_DONE $T2/SCORES2.txt || [ -f $C/.MUTANT ]; do
    sleep 60; n=$((n+1)); [ $n -gt 120 ] && { echo "TABLE519_2B: table 2 not finished after 120 min -- not starting"; exit 7; }
done
echo "=== TABLE 2b start $(date) after $n min wait; baseline = SEC dev_sgi_re.c md5 $(md5sum $SEC/src/devices/dev_sgi_re.c | cut -c1-8); table 2's baseline: $(cmp -s $SEC/src/devices/dev_sgi_re.c $T2/BASELINE_FIX519.c && echo IDENTICAL || echo 'DIFFERS (the announce bracket edit; recorded in PRETABLE 6.h)') ===" | tee -a $T2/SCORES2.txt
cp $SEC/src/devices/dev_sgi_re.c $T2/BASELINE_FIX519_final.c
FROZEN=$T2/sgi_re_colourdefault_probe.REPAIRED16.asrun.py
echo "instrument: frozen table-2 copy vs working file: $(cmp -s $FROZEN $SEC/regress/sgi_re_colourdefault_probe.py && echo IDENTICAL || echo 'DIFFERS (see PRETABLE 6.h; re-frozen as REPAIRED16b)')" | tee -a $T2/SCORES2.txt
cp $SEC/regress/sgi_re_colourdefault_probe.py $T2/sgi_re_colourdefault_probe.REPAIRED16b.asrun.py; FROZEN=$T2/sgi_re_colourdefault_probe.REPAIRED16b.asrun.py
cp $SP/mut519x.py $T2/mut519x.py
echo "$C/.MUTANT: src/devices/dev_sgi_re.c  #519 TABLE 2b (main loop) in progress" > $C/.MUTANT
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
    printf '%-18s %-8s sentinel=%-16s reds=%s\n' "$lbl" "${r#SGICOLOUR_RESULT=}" "$(tail -1 $T2/$lbl.raw)" "$reds" | tee -a $T2/SCORES2.txt
}
run BASE_final BASE
for m in M16_dropcase_rgb M17_dropcase_rgba; do run "$m" "$m"; done
echo "=== RESTORE from SEC (2b) ===" | tee -a $T2/SCORES2.txt
cp $SEC/src/devices/dev_sgi_re.c $C/src/devices/dev_sgi_re.c; cd $C && rm -f src/devices/dev_sgi_re.o && make -j4 > $T2/build_restore2b.log 2>&1
if cmp -s $C/src/devices/dev_sgi_re.c $SEC/src/devices/dev_sgi_re.c && [ $C/gxemul -nt $C/src/devices/dev_sgi_re.c ]; then rm -f $C/.MUTANT; echo "$C restored cmp-clean vs SEC, rebuilt fresh, sentinel cleared" | tee -a $T2/SCORES2.txt; else echo "*** RESTORE INCOMPLETE -- SENTINEL KEPT ***" | tee -a $T2/SCORES2.txt; fi
echo "TABLE519_2B_DONE $(date)" | tee -a $T2/SCORES2.txt
