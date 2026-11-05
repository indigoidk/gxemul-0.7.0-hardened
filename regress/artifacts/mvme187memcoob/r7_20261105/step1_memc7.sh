#!/bin/bash
# step1_memc7.sh -- mvme187memcoob repair 6, STEP 1 (regress_20261105/REG_MYTHOS_local.md section 2(d); DISPOSITION.md):
# measure the eight own-latch variants on the CURRENT 206-row probe before any probe edit.  The eight scored 206/206 in table 5
# (r5_20261105/table5/SCORES.txt:2916-2919, :2931, :2936-2937, :2990); this re-measures them in a fresh scratch clone, and its base
# leg doubles as the clone's freshness proof.
# BASELINE (named): GXEMUL-SEC/src/devices/dev_mvme187.c (the working tree's fix) and step1/probe206_frozen.py (a copy of
# regress/mvme187_memc_probe.py taken before repair 6 touched it; md5 recorded below).
# Mutates ONLY the WSL scratch clone /tmp/gxmemc7 (a cp -a of build/) under a clone-local .MUTANT sentinel, cleared only after the
# restored source cmp's against GXEMUL-SEC AND the rebuilt binary is newer than it.  Baseline build: rm src/cpus/*.o and the device
# object, make; variant builds: rm the device object, make (dev_mvme187.c is #included by nothing); every build must leave
# dev_mvme187.o -nt the source and gxemul -nt the object.  Run from a frozen copy (step1_memc7.run.sh).
set -u
G=/mnt/c/DocumentNoSnc/cc/GXEMUL
SEC=$G/GXEMUL-SEC
MD=$SEC/regress/artifacts/mvme187memcoob
R7=$MD/r7_20261105
OUT=$R7/step1
C=/tmp/gxmemc7
P=$OUT/probe206_frozen.py
V=$MD/r5_20261105/memc_variants_5.py
FIX=$SEC/src/devices/dev_mvme187.c
S1=src/devices/dev_mvme187.c
O1=src/devices/dev_mvme187.o
N=206
EIGHT="L_MB_M_xori_any L_ME_M_xori_any L_DB_D_xori_any L_DA_D_xori_any L_MT_M_xori_M L_MW_M_xori_M L_DT_D_xori_D L_DT_D_idat_W.D"
[ -f $P ] || { echo "NO frozen probe $P -- refusing"; exit 2; }
[ -f $V ] || { echo "NO variant script $V -- refusing"; exit 2; }
[ -f $FIX ] || { echo "NO baseline $FIX -- refusing"; exit 2; }
[ -e $C ] && { echo "$C exists -- refusing to overwrite a clone this script did not make"; exit 2; }
echo "step 1 start $(date -u +%FT%TZ)"
cp -a $G/build $C || { echo "CLONE FAILED"; exit 3; }
cd $C || exit 3
echo "$S1: mvme187memcoob repair 6 step 1 (the eight own-latch variants on 206 rows); baseline $FIX" > .MUTANT
mkdir -p $C/logs $C/sessions
if cmp -s $S1 $FIX; then echo "clone source = baseline: yes"; else echo "clone source = baseline: NO -- refusing"; exit 4; fi
build() {   # label [full]
    if [ "${2:-}" = full ]; then rm -f src/cpus/*.o; fi
    rm -f $O1
    make -j4 > $C/logs/build_$1.log 2>&1
    rc=$?
    if [ $rc = 0 ] && [ $O1 -nt $S1 ] && [ gxemul -nt $O1 ]; then echo fresh; else cp $C/logs/build_$1.log $OUT/build_$1.log; echo "STALE_rc$rc"; fi
}
run() {   # label binary
    local sess=$C/sessions/$1
    rm -rf $sess
    python3 -u $P $2 $1 $sess > $OUT/probe_$1.out 2>&1
    r=$(grep '^MVME187_MEMC_RESULT=' $OUT/probe_$1.out | cut -d= -f2)
    ctl=$(grep '^MVME187_MEMC_CONTROL=' $OUT/probe_$1.out | cut -d= -f2)
    sym=$(grep '^MVME187_MEMC_SYMPTOM=' $OUT/probe_$1.out | cut -d= -f2)
    red=$(grep '^MVME187_MEMC_RED=' $OUT/probe_$1.out | cut -d= -f2)
    echo "$1 [$N rows] ${r:-none} CONTROL=${ctl:-none} SYMPTOM=${sym:-none} $(tail -n 1 $OUT/probe_$1.out) RED=${red:-none}" >> $OUT/SCORES.txt
    rm -rf $OUT/sessions_$1; cp -r $sess $OUT/sessions_$1
    echo "$1 ${r:-none}"
}
: > $OUT/SCORES.txt
f=$(build base full); echo "base build: $f"
if [ "$f" != fresh ] || ! [ gxemul -nt $S1 ]; then echo "BASE BUILD NOT FRESH -- refusing"; exit 5; fi
ls -l --time-style=full-iso gxemul $S1 $O1 > $OUT/FRESHNESS.txt
echo "gxemul -nt $S1: yes; $O1 -nt $S1: yes; gxemul -nt $O1: yes" >> $OUT/FRESHNESS.txt
run base $C/gxemul
for v in $EIGHT; do
    if python3 $V apply $v $FIX $S1 > $C/logs/apply_$v.err 2>&1; then
        diff $FIX $S1 > $OUT/diff_$v.txt
        f=$(build $v)
        if [ "$f" = fresh ]; then run $v $C/gxemul; else echo "$v [$N rows] BUILD-$f" >> $OUT/SCORES.txt; fi
    else
        cp $C/logs/apply_$v.err $OUT/apply_$v.err
        echo "$v [$N rows] MUTANT-TEXT-NOT-FOUND" >> $OUT/SCORES.txt
    fi
done
cp $FIX $S1
f=$(build restore); echo "restore build: $f"
if [ "$f" = fresh ] && cmp -s $S1 $SEC/$S1 && [ gxemul -nt $S1 ]; then
    rm -f .MUTANT; echo "clone restored to GXEMUL-SEC and rebuilt; sentinel cleared"
else
    echo "RESTORE NOT VERIFIED -- sentinel kept"
fi
md5sum $P $V $FIX $SEC/regress/mvme187_memc_probe.py > $OUT/MD5.txt
echo "step 1 end $(date -u +%FT%TZ)"
echo STEP1_MEMC7_DONE
