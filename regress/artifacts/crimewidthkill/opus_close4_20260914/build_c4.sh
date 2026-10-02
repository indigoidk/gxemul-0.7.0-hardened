#!/bin/bash
# #529 closing pass 4, Opus seat: scratch clone from build/, baseline identity + rebuild, 5 mutants + base, RESTORE
# with two-part clearance.  Writes only under /tmp/gxopuscrime4, /tmp/oc4 and the session scratchpad.
set -u
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
SRCTREE=/mnt/c/DocumentNoSnc/CC/GXEMUL/build
C=/tmp/gxopuscrime4
F=src/devices/dev_sgi_ip32.c
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/oc4
OUT=/tmp/oc4
MUTS="base c1_deepseek c2_kimik3 c3_codex_dbg c4_kimicli c5_codex_b1"
rm -rf $OUT; mkdir -p $OUT/builds $OUT/logs
cp $SP/mutants_c4.py $OUT/mutants_c4.FROZEN.py
cp $SEC/regress/crime_width_probe.py /tmp/cwp_close4.py
md5sum /tmp/cwp_close4.py $SEC/regress/crime_width_probe.py | tee $OUT/logs/INSTRUMENT.md5
echo "build start $(date '+%F %T')" | tee $OUT/logs/ORDER.txt

[ -e $C ] && { echo "CLONE EXISTS -- ABORT"; exit 2; }
cp -a $SRCTREE $C
cd $C || exit 2
[ -e $C/.MUTANT ] && { echo "clone inherited a sentinel -- ABORT"; exit 2; }
echo "BASELINE_CMP:"; cmp $F $SEC/$F && echo "  CMP CLEAN vs SEC" || { echo "  CMP DIFFERS -- ABORT"; exit 3; }

restore_and_exit() {
    cp $SEC/$F $F; rm -f src/devices/dev_sgi_ip32.o
    make -j2 > $OUT/builds/restore.log 2>&1
    if cmp -s $F $SEC/$F && [ gxemul -nt $F ]; then rm -f $C/.MUTANT; echo "RESTORE_OK on abort"; else echo "RESTORE_FAILED on abort -- sentinel LEFT"; fi
    exit ${1:-9}
}

for m in $MUTS; do
    echo "mutant $m $(date '+%T')" > $C/.MUTANT
    cp $SEC/$F $F
    if [ "$m" != "base" ]; then
        if ! python3 $OUT/mutants_c4.FROZEN.py $m $F; then echo "TXTFAIL $m"; restore_and_exit 5; fi
    fi
    diff -u $SEC/$F $F > $OUT/logs/$m.diff
    rm -f src/devices/dev_sgi_ip32.o
    make -j2 > $OUT/builds/$m.log 2>&1; rc=$?
    if [ $rc -ne 0 ] || ! [ gxemul -nt $F ] || ! [ src/devices/dev_sgi_ip32.o -nt $F ]; then
        echo "BUILD_FAIL $m rc=$rc"; grep -E 'error' $OUT/builds/$m.log | head -5; restore_and_exit 4
    fi
    cp gxemul $OUT/builds/gx_$m
    same=""; [ "$m" != "base" ] && cmp -s gxemul $OUT/builds/gx_base && same=" *** BYTE-IDENTICAL TO BASE ***"
    echo "BUILT $m rc=0 $(md5sum < gxemul | cut -c1-8) difflines=$(grep -c '^[+-][^+-]' $OUT/logs/$m.diff)$same"
    rm -f $C/.MUTANT
done

# ---- RESTORE ----
cp $SEC/$F $F
rm -f src/devices/dev_sgi_ip32.o
make -j2 > $OUT/builds/restore.log 2>&1; rc=$?
if [ $rc -eq 0 ] && cmp -s $F $SEC/$F && [ gxemul -nt $F ]; then
    cmp -s gxemul $OUT/builds/gx_base && echo "RESTORED binary == baseline (byte-identical)" || echo "RESTORED binary differs from baseline"
    rm -f $C/.MUTANT; echo "RESTORE_OK cmp clean vs SEC, gxemul -nt source, sentinel removed"
else
    echo "RESTORE_FAILED rc=$rc -- sentinel LEFT in place"
fi
md5sum $OUT/builds/gx_* > $OUT/logs/BINARIES.md5
echo "build end $(date '+%F %T')" | tee -a $OUT/logs/ORDER.txt
echo BUILD_C4_DONE
