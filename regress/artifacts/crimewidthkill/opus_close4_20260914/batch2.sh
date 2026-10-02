#!/bin/bash
# #529 closing pass 4, Opus seat, BATCH 2 (class siblings): reuse the clone, sentinel per mutant, restore with the
# two-part clearance, then the frozen 131-row probe in 3 lanes, then discriminators on every 131/131, then durable copies.
set -u
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
C=/tmp/gxopuscrime4
F=src/devices/dev_sgi_ip32.c
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/oc4
ART=$SEC/regress/artifacts/crimewidthkill/opus_close4_20260914
OUT=/tmp/oc4
P=/tmp/cwp_close4.py
MUTS="d1_rearm_dog0200 d2_pre_dog0200 d3_rearm_wtime d4_pre_wistat d6_chan_len2 d7_rearm_wrev"
cp $SP/mutants_c4.py $OUT/mutants_c4b.FROZEN.py
cp $SP/disc_c4.py $OUT/disc_c4b.FROZEN.py
ls --full-time $SP/PRETABLE2.out | tee -a $OUT/logs/ORDER.txt
echo "batch2 build start $(date '+%F %T')" | tee -a $OUT/logs/ORDER.txt
md5sum $P | tee -a $OUT/logs/INSTRUMENT.md5
cd $C || exit 2
[ -e $C/.MUTANT ] && { echo "SENTINEL PRESENT at batch-2 start -- ABORT"; exit 2; }
cmp -s $F $SEC/$F || { echo "clone source differs from SEC -- ABORT"; exit 3; }

for m in $MUTS; do
    echo "mutant $m $(date '+%T')" > $C/.MUTANT
    cp $SEC/$F $F
    if ! python3 $OUT/mutants_c4b.FROZEN.py $m $F; then echo "TXTFAIL $m"; continue; fi
    diff -u $SEC/$F $F > $OUT/logs/$m.diff
    rm -f src/devices/dev_sgi_ip32.o
    make -j2 > $OUT/builds/$m.log 2>&1; rc=$?
    if [ $rc -ne 0 ] || ! [ gxemul -nt $F ] || ! [ src/devices/dev_sgi_ip32.o -nt $F ]; then
        echo "BUILD_FAIL $m rc=$rc"; grep -E 'error' $OUT/builds/$m.log | head -5; continue
    fi
    cp gxemul $OUT/builds/gx_$m
    same=""; cmp -s gxemul $OUT/builds/gx_base && same=" *** BYTE-IDENTICAL TO BASE ***"
    echo "BUILT $m rc=0 $(md5sum < gxemul | cut -c1-8) difflines=$(grep -c '^[+-][^+-]' $OUT/logs/$m.diff)$same"
done
cp $SEC/$F $F
rm -f src/devices/dev_sgi_ip32.o
make -j2 > $OUT/builds/restore2.log 2>&1; rc=$?
if [ $rc -eq 0 ] && cmp -s $F $SEC/$F && [ gxemul -nt $F ]; then
    cmp -s gxemul $OUT/builds/gx_base && echo "RESTORED binary == baseline (byte-identical)" || echo "RESTORED binary differs from baseline"
    rm -f $C/.MUTANT; echo "RESTORE_OK cmp clean vs SEC, gxemul -nt source, sentinel removed"
else
    echo "RESTORE_FAILED rc=$rc -- sentinel LEFT in place"
fi
echo "batch2 probes start $(date '+%F %T')" | tee -a $OUT/logs/ORDER.txt

lane() {
    for m in "$@"; do
        B=$OUT/builds/gx_$m
        [ -x "$B" ] || { echo "NOBIN $m"; continue; }
        t0=$(date +%s)
        python3 -u $P "$B" "$m" > $OUT/logs/probe_$m.raw 2>&1
        t1=$(date +%s)
        echo "RUN $m $(grep -o 'CRIMEP_RESULT=[0-9/]*' $OUT/logs/probe_$m.raw) $(grep -o 'CRIMEP_CONTROL=[A-Z]*' $OUT/logs/probe_$m.raw) last=$(tail -1 $OUT/logs/probe_$m.raw) secs=$((t1-t0)) | $(grep '^FAILING:' $OUT/logs/probe_$m.raw)"
    done
}
lane d1_rearm_dog0200 d2_pre_dog0200 > $OUT/logs/lane2a.out 2>&1 &
sleep 20
lane d3_rearm_wtime d4_pre_wistat > $OUT/logs/lane2b.out 2>&1 &
sleep 20
lane d6_chan_len2 d7_rearm_wrev > $OUT/logs/lane2c.out 2>&1 &
wait
cat $OUT/logs/lane2?.out | sort -k2 > $OUT/table_c4b.out
echo "batch2 probes end $(date '+%F %T')" | tee -a $OUT/logs/ORDER.txt
cat $OUT/table_c4b.out

for m in $MUTS; do
    grep -q "RUN $m CRIMEP_RESULT=131/131" $OUT/table_c4b.out || continue
    python3 -u $OUT/disc_c4b.FROZEN.py $OUT/builds/gx_base $OUT/builds/gx_$m $m >> $OUT/logs/disc_c4.out 2>&1
done
cat $OUT/logs/disc_c4.out

mkdir -p $ART/logs
cp $OUT/logs/* $ART/logs/ 2>/dev/null
cp $OUT/table_c4.out $OUT/table_c4b.out $ART/ 2>/dev/null
cp $SP/PRETABLE2.out $SP/mutants_c4.py $SP/disc_c4.py $SP/build_c4.sh $SP/probe_c4.sh $SP/batch2.sh $ART/
md5sum $OUT/builds/gx_* > $ART/logs/BINARIES.md5
echo "clone: sentinel=$([ -e $C/.MUTANT ] && echo PRESENT || echo absent) cmp=$(cmp -s $C/$F $SEC/$F && echo CLEAN || echo DIFFERS) fresh=$([ $C/gxemul -nt $C/$F ] && echo yes || echo NO)"
echo BATCH2_DONE
