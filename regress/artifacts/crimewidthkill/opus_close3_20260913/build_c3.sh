#!/bin/bash
# #529 closing pass 3, Opus seat: scratch clone from build/, baseline identity + rebuild, 12 mutants, RESTORE with the
# two-part clearance.  Writes nothing outside /tmp/gxopus529c3, /tmp/oc3 and the session scratchpad.
set -u
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
SRCTREE=/mnt/c/DocumentNoSnc/CC/GXEMUL/build
C=/tmp/gxopus529c3
F=src/devices/dev_sgi_ip32.c
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_close3
OUT=/tmp/oc3
MUTS="rearm_ctlrd rearm_dogclr rearm_ctl0 pre_istat pre_revbr pre_dogbr byp_rev byp_time ans_hi32_b5 land_b4clr ans_ctl_lb pre_ctlrd"
rm -rf $OUT; mkdir -p $OUT/builds $OUT/logs
cp $SP/mutants_c3.py $OUT/mutants_c3.FROZEN.py
cp $SP/disc_c3.py $OUT/disc_c3.FROZEN.py
# freeze the shipped probe ONCE
cp $SEC/regress/crime_width_probe.py /tmp/cwp_close3.py
md5sum /tmp/cwp_close3.py $SEC/regress/crime_width_probe.py | tee $OUT/logs/INSTRUMENT.md5
ls --full-time $SP/PRETABLE.out | tee $OUT/logs/ORDER.txt
echo "build start $(date '+%F %T')" | tee -a $OUT/logs/ORDER.txt

[ -e $C ] && { echo "CLONE EXISTS -- ABORT"; exit 2; }
cp -a $SRCTREE $C
cd $C || exit 2
[ -e $C/.MUTANT ] && { echo "clone inherited a sentinel -- ABORT"; exit 2; }
echo "BASELINE_CMP:"; cmp $F $SEC/$F && echo "  CMP CLEAN vs SEC" || { echo "  CMP DIFFERS -- ABORT"; exit 3; }
md5sum $F $SEC/$F
rm -f src/devices/dev_sgi_ip32.o
make -j4 > $OUT/builds/base.log 2>&1; rc=$?
if [ $rc -ne 0 ] || ! [ gxemul -nt $F ]; then echo "BASE_BUILD_FAIL rc=$rc"; tail -5 $OUT/builds/base.log; exit 4; fi
cp gxemul $OUT/builds/gx_base
echo "BASE built rc=0 gxemul -nt source $(md5sum < gxemul | cut -c1-8)"

for m in $MUTS; do
    echo "mutant $m $(date '+%T')" > $C/.MUTANT
    cp $SEC/$F $F
    if ! python3 $OUT/mutants_c3.FROZEN.py $m $F; then echo "TXTFAIL $m"; continue; fi
    diff -u $SEC/$F $F > $OUT/logs/$m.diff
    rm -f src/devices/dev_sgi_ip32.o
    make -j4 > $OUT/builds/$m.log 2>&1; rc=$?
    if [ $rc -ne 0 ] || ! [ gxemul -nt $F ] || ! [ src/devices/dev_sgi_ip32.o -nt $F ]; then
        echo "BUILD_FAIL $m rc=$rc"; grep -E 'error' $OUT/builds/$m.log | head -5; continue
    fi
    cp gxemul $OUT/builds/gx_$m
    same=""; cmp -s gxemul $OUT/builds/gx_base && same=" *** BYTE-IDENTICAL TO BASE ***"
    echo "BUILT $m rc=0 $(md5sum < gxemul | cut -c1-8) difflines=$(grep -c '^[+-][^+-]' $OUT/logs/$m.diff)$same"
done

# ---- RESTORE: source from SEC, rebuild, then BOTH parts of the clearance ----
cp $SEC/$F $F
rm -f src/devices/dev_sgi_ip32.o
make -j4 > $OUT/builds/restore.log 2>&1; rc=$?
if [ $rc -eq 0 ] && cmp -s $F $SEC/$F && [ gxemul -nt $F ]; then
    cmp -s gxemul $OUT/builds/gx_base && echo "RESTORED binary == baseline (byte-identical)" || echo "RESTORED binary differs from baseline"
    rm -f $C/.MUTANT; echo "RESTORE_OK cmp clean vs SEC, gxemul -nt source, sentinel removed"
else
    echo "RESTORE_FAILED rc=$rc -- sentinel LEFT in place"
fi
md5sum $OUT/builds/gx_* > $OUT/logs/BINARIES.md5
echo "build end $(date '+%F %T')" | tee -a $OUT/logs/ORDER.txt
echo BUILD_DONE
