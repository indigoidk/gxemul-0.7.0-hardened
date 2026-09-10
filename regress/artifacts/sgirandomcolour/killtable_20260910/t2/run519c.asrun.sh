#!/bin/bash
#  #519 pass-2 repair, cut 2: run the 16-row instrument on the fix clone and on HEAD, then TABLE 2 in the
#  fix clone (/tmp/gx519): BASE, M13_okorx, M14_okory, M15_texrd (expected escape, disclosed).
set -u
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad
ART=$SEC/regress/artifacts/sgirandomcolour
K1=$ART/killtable_20260910
T2=$K1/t2
C=/tmp/gx519
cd $SEC || exit 9
D=$ART/fix_20260910
echo "=== run519c $(date) ==="
echo "instrument vs the seat's frozen 14-row copy (only setup_put's vertex branch, the header sentence and the new block may differ):"
diff $K1/sgi_re_colourdefault_probe.FROZEN.py regress/sgi_re_colourdefault_probe.py | grep -cE '^[<>]' | sed 's/^/  changed lines: /'
echo "fix clone source vs SEC: $(cmp -s $C/src/devices/dev_sgi_re.c src/devices/dev_sgi_re.c && echo CLEAN || echo DIVERGENT); binary fresh: $([ $C/gxemul -nt $C/src/devices/dev_sgi_re.c ] && echo FRESH || echo STALE); sentinel: $([ -f $C/.MUTANT ] && cat $C/.MUTANT || echo none)"
git show HEAD:src/devices/dev_sgi_re.c > /tmp/head_sgi_re.c
echo "build/ dev_sgi_re.c vs HEAD: $(cmp -s /mnt/c/DocumentNoSnc/CC/GXEMUL/build/src/devices/dev_sgi_re.c /tmp/head_sgi_re.c && echo HEAD || echo NOT-HEAD); build/gxemul fresh: $([ /mnt/c/DocumentNoSnc/CC/GXEMUL/build/gxemul -nt /mnt/c/DocumentNoSnc/CC/GXEMUL/build/src/devices/dev_sgi_re.c ] && echo FRESH || echo STALE)"
python3 -u regress/sgi_re_colourdefault_probe.py $C/gxemul FIX519c > $D/FIX519_detector_run3.out 2>&1
echo "FIX rc=$? $(grep -o 'SGICOLOUR_RESULT=[0-9]*/[0-9]*' $D/FIX519_detector_run3.out) $(tail -1 $D/FIX519_detector_run3.out)"; grep -E ' FAIL$' $D/FIX519_detector_run3.out | cut -c1-140
python3 -u regress/sgi_re_colourdefault_probe.py /mnt/c/DocumentNoSnc/CC/GXEMUL/build/gxemul HEAD1ce8296 > $D/HEAD_detector_run2.out 2>&1
echo "HEAD rc=$? $(grep -o 'SGICOLOUR_RESULT=[0-9]*/[0-9]*' $D/HEAD_detector_run2.out) $(tail -1 $D/HEAD_detector_run2.out)"; grep -E ' FAIL$' $D/HEAD_detector_run2.out | awk '{print "  red: "$1" "$2}' | head -20
#  ---------------------------------------------------------------- TABLE 2 in the fix clone
mkdir -p $T2
FROZEN=$T2/sgi_re_colourdefault_probe.REPAIRED16.asrun.py
cp regress/sgi_re_colourdefault_probe.py $FROZEN
cp src/devices/dev_sgi_re.c $T2/BASELINE_FIX519.c
cp $SP/mut519x.py $T2/mut519x.py
echo "=== TABLE 2 start $(date); instrument md5 $(md5sum $FROZEN | cut -c1-8), $(grep -c 'row(' $FROZEN) row( sites; baseline = SEC dev_sgi_re.c md5 $(md5sum $T2/BASELINE_FIX519.c | cut -c1-8), identical to table 1's: $(cmp -s $T2/BASELINE_FIX519.c $K1/BASELINE_FIX519.c && echo YES || echo NO) ===" | tee $T2/SCORES2.txt
echo "$C/.MUTANT: src/devices/dev_sgi_re.c  #519 TABLE 2 (main loop) in progress" > $C/.MUTANT
run () {   # label mutant
    local lbl=$1 m=$2
    cd $C || return 1
    cp $T2/BASELINE_FIX519.c src/devices/dev_sgi_re.c
    if [ "$m" != "BASE" ]; then
        python3 $T2/mut519x.py src/devices/dev_sgi_re.c "$m" > $T2/mutate_$lbl.log 2>&1 || { echo "$lbl MUTANT_DID_NOT_APPLY (rc=$?)" | tee -a $T2/SCORES2.txt; tail -2 $T2/mutate_$lbl.log; return 1; }
    fi
    rm -f src/devices/dev_sgi_re.o
    if ! make -j4 > $T2/build_$lbl.log 2>&1; then echo "$lbl BUILD_FAILED" | tee -a $T2/SCORES2.txt; return 1; fi
    if [ ! gxemul -nt src/devices/dev_sgi_re.c ]; then echo "$lbl STALE_BINARY" | tee -a $T2/SCORES2.txt; return 1; fi
    python3 -u $FROZEN $C/gxemul $lbl > $T2/$lbl.raw 2>&1
    local r; r=$(grep -o 'SGICOLOUR_RESULT=[0-9]*/[0-9]*' $T2/$lbl.raw | tail -1)
    local reds; reds=$(grep -E ' FAIL$' $T2/$lbl.raw | awk '{print $1" "$2}' | tr '\n' ',' | cut -c1-120)
    printf '%-14s %-8s sentinel=%-16s reds=%s\n' "$lbl" "${r#SGICOLOUR_RESULT=}" "$(tail -1 $T2/$lbl.raw)" "$reds" | tee -a $T2/SCORES2.txt
}
run BASE BASE
for m in M13_okorx M14_okory M15_texrd; do run "$m" "$m"; done
echo "=== RESTORE from SEC ===" | tee -a $T2/SCORES2.txt
cp $SEC/src/devices/dev_sgi_re.c $C/src/devices/dev_sgi_re.c; cd $C && rm -f src/devices/dev_sgi_re.o && make -j4 > $T2/build_restore.log 2>&1
if cmp -s $C/src/devices/dev_sgi_re.c $SEC/src/devices/dev_sgi_re.c && [ $C/gxemul -nt $C/src/devices/dev_sgi_re.c ]; then rm -f $C/.MUTANT; echo "$C restored cmp-clean vs SEC, rebuilt fresh, sentinel cleared" | tee -a $T2/SCORES2.txt; else echo "*** RESTORE INCOMPLETE -- SENTINEL KEPT ***" | tee -a $T2/SCORES2.txt; fi
echo "TABLE519_2_DONE $(date)" | tee -a $T2/SCORES2.txt
