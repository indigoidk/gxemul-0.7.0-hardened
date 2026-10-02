#!/bin/bash
# second build batch (hi_gate, pa_gate), then restore with the two-part clearance; then probe them; then discriminators
set -u
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
C=/tmp/gxopus529close
F=src/devices/dev_sgi_ip32.c
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad
OUT=/tmp/close529
ART=$SEC/regress/artifacts/crimewidthkill/opus_close_20260913
cp $SP/mutants_close.py $OUT/mutants_close.FROZEN2.py
cp $SP/disc_close.py $OUT/disc_close.FROZEN.py
cd "$C" || exit 2
cmp -s "$F" "$SEC/$F" || { echo "CLONE NOT AT BASELINE before batch 2"; exit 3; }
for m in hi_gate pa_gate; do
    echo "mutant $m" > "$C/.MUTANT"
    cp "$SEC/$F" "$F"
    python3 $OUT/mutants_close.FROZEN2.py $m "$F" || { echo "BUILD_FAIL $m (text)"; continue; }
    diff -u "$SEC/$F" "$F" > $OUT/diffs/$m.diff
    rm -f src/devices/dev_sgi_ip32.o
    make -j4 > $OUT/builds/$m.log 2>&1; rc=$?
    if [ $rc -ne 0 ] || ! [ gxemul -nt "$F" ]; then echo "BUILD_FAIL $m rc=$rc"; continue; fi
    cp gxemul $OUT/builds/gx_$m; echo "BUILT $m fresh $(md5sum < gxemul | cut -c1-8)"
done
cp "$SEC/$F" "$F"; rm -f src/devices/dev_sgi_ip32.o
make -j4 > $OUT/builds/restore2.log 2>&1; rc=$?
if cmp -s "$F" "$SEC/$F" && [ gxemul -nt "$F" ] && [ $rc -eq 0 ] && cmp -s gxemul /tmp/gx529close_base; then
    rm -f "$C/.MUTANT"; echo "RESTORE2_OK cmp clean, gxemul -nt source, binary == baseline, sentinel removed"
else echo "RESTORE2_FAILED -- sentinel left"; fi
bash $SP/probe_close.run.sh "hi_gate pa_gate"
# discriminators: base vs each survivor/extra, same script
for m in rearm4 pre4 rearm_time ctl_collide wst_mc2 rd_hi lt_blk wnz_lbl acc4_210 pa_gate hi_gate; do
    [ -x $OUT/builds/gx_$m ] || { echo "NOBIN $m"; continue; }
    python3 -u $OUT/disc_close.FROZEN.py /tmp/gx529close_base $OUT/builds/gx_$m $m 2>&1 | tee -a $OUT/disc_close.out
done
cp $OUT/disc_close.out $OUT/diffs/*.diff "$ART/logs/" 2>/dev/null
cp $OUT/mutants_close.FROZEN2.py "$ART/mutants_close.py"; cp $OUT/disc_close.FROZEN.py "$ART/disc_close.py"
cp $SP/probe_close.sh $SP/build_close.sh $SP/build2_close.sh "$ART/" 2>/dev/null
echo BATCH2_DONE
