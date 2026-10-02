#!/bin/bash
# batch 3: fresh clone, baseline rebuild, 2 mutants, restore; then the REPAIRED (121-row) probe, frozen, one lane
set -u
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
C=/tmp/gxopus529c2
F=src/devices/dev_sgi_ip32.c
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_close2
ART=$SEC/regress/artifacts/crimewidthkill/opus_close2_20260913/batch3
OUT=/tmp/close2c
mkdir -p $OUT/builds $OUT/logs $ART
P=/tmp/cwp_close2_121.py
cp $SEC/regress/crime_width_probe.py $P
md5sum $P | tee $OUT/logs/INSTRUMENT.md5
cp $SP/mutants_c2.py $OUT/mutants_c2.FROZEN3.py
rm -rf $C; cp -a /mnt/c/DocumentNoSnc/CC/GXEMUL/build $C; cd $C || exit 2
cmp -s $F $SEC/$F && echo "BASELINE_CMP CLEAN" || { echo "BASELINE_CMP DIFFERS -- ABORT"; exit 3; }
rm -f src/devices/dev_sgi_ip32.o; make -j4 > $OUT/builds/base.log 2>&1; rc=$?
[ $rc -eq 0 ] && [ gxemul -nt $F ] && cp gxemul $OUT/builds/gx_base && echo "BASE built rc=0 -nt $(md5sum < gxemul | cut -c1-8)" || { echo BASE_BUILD_FAIL; exit 4; }
for m in istat_lane istat_leak; do
    echo "mutant $m" > $C/.MUTANT
    cp $SEC/$F $F
    python3 $OUT/mutants_c2.FROZEN3.py $m $F || { echo "TXTFAIL $m"; continue; }
    diff -u $SEC/$F $F > $OUT/logs/$m.diff
    rm -f src/devices/dev_sgi_ip32.o; make -j4 > $OUT/builds/$m.log 2>&1; rc=$?
    if [ $rc -ne 0 ] || ! [ gxemul -nt $F ]; then echo "BUILD_FAIL $m"; continue; fi
    cp gxemul $OUT/builds/gx_$m; echo "BUILT $m $(md5sum < gxemul | cut -c1-8)"
done
cp $SEC/$F $F; rm -f src/devices/dev_sgi_ip32.o; make -j4 > $OUT/builds/restore.log 2>&1; rc=$?
if cmp -s $F $SEC/$F && [ gxemul -nt $F ] && [ $rc -eq 0 ] && cmp -s gxemul $OUT/builds/gx_base; then
    rm -f $C/.MUTANT; echo "RESTORE_OK cmp clean, -nt, binary == base, sentinel removed"
else echo "RESTORE_FAILED -- sentinel left"; fi
md5sum $OUT/builds/gx_* > $OUT/logs/BINARIES.md5
for m in base istat_lane istat_leak; do
    python3 -u $P $OUT/builds/gx_$m $m > $OUT/logs/probe121_$m.raw 2>&1
    echo "NEW121 $m $(grep -o 'CRIMEP_RESULT=[0-9/]*' $OUT/logs/probe121_$m.raw) $(grep -o 'CRIMEP_CONTROL=[A-Z]*' $OUT/logs/probe121_$m.raw) last=$(tail -1 $OUT/logs/probe121_$m.raw) | $(grep '^FAILING:' $OUT/logs/probe121_$m.raw)" | tee -a $OUT/table121.out
    grep -E '^istat lb v0|^istat lh v0' $OUT/logs/probe121_$m.raw
done
cp $OUT/logs/* $OUT/table121.out $OUT/mutants_c2.FROZEN3.py $SP/PRETABLE3.out $SP/batch3.sh $ART/
cd /tmp && rm -rf $C $OUT $P
ls -d $C 2>/dev/null || echo "clone deleted"
echo BATCH3_DONE
