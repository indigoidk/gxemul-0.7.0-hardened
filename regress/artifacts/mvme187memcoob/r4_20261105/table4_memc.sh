#!/bin/bash
# table2_memc.sh -- mvme187memcoob TEST-VARIANT TABLE 2 (adj_20261104/ADJ_MYTHOS.md M20/X7: table 1's nineteen rerun on the 74-row
# instrument, plus the ten the adjudication added; every SCORES line names the row count).  Legs first, in the same clone: base (the
# final candidate, dev_mvme187.c.fix2), the HEAD leg (dev_mvme187.c.HEAD) and three null media.  PRETABLE_2.out must exist first.
# Mutates ONLY the WSL scratch clone /tmp/gxmemc2 (a cp -a of build/) under a clone-local .MUTANT sentinel, cleared only after the
# restore cmp's against GXEMUL-SEC and rebuilds fresh.  Rebuild: rm the device object, make; require dev_mvme187.o -nt the source and
# gxemul -nt the object.
set -u
G=/mnt/c/DocumentNoSnc/cc/GXEMUL
C=/tmp/gxmemc5
IN=$G/GXEMUL-SEC/regress/artifacts/mvme187memcoob/det_20261104
OUT=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/mvme187memcoob/r4_20261105/table4
P=$OUT/probe148_frozen.py
N=148
V=$OUT/../memc_variants_4.py
FIX=$IN/dev_mvme187.c.fix2
S1=src/devices/dev_mvme187.c
O1=src/devices/dev_mvme187.o
[ -f $OUT/../PRETABLE_4.out ] || { echo "NO PRETABLE_2.out -- refusing"; exit 2; }
[ -f $P ] || { echo "NO frozen probe $P -- refusing"; exit 2; }
rm -rf $C && cp -a $G/build $C || { echo "CLONE FAILED"; exit 3; }
cd $C || exit 3
echo "$S1: mvme187memcoob table 2; baseline $FIX" > .MUTANT
cmp -s $S1 $FIX || { echo "clone source = baseline: NO"; exit 4; }
build() {
    rm -f $O1
    make -j4 > $OUT/build_$1.log 2>&1
    rc=$?
    if [ $rc = 0 ] && [ $O1 -nt $S1 ] && [ gxemul -nt $O1 ]; then echo fresh; else echo "STALE_rc$rc"; fi
}
run() {   # label binary
    python3 -u $P $2 $1 $OUT/sessions_$1 > $OUT/probe_$1.out 2>&1
    r=$(grep '^MVME187_MEMC_RESULT=' $OUT/probe_$1.out | cut -d= -f2)
    ctl=$(grep '^MVME187_MEMC_CONTROL=' $OUT/probe_$1.out | cut -d= -f2)
    sym=$(grep '^MVME187_MEMC_SYMPTOM=' $OUT/probe_$1.out | cut -d= -f2)
    asan=$(grep '^MVME187_MEMC_ASAN=' $OUT/probe_$1.out | cut -d= -f2)
    red=$(grep '^MVME187_MEMC_RED=' $OUT/probe_$1.out | cut -d= -f2)
    echo "$1 [$N rows] ${r:-none} CONTROL=${ctl:-none} SYMPTOM=${sym:-none} ASAN=${asan:-none} $(tail -n 1 $OUT/probe_$1.out) RED=${red:-none}" >> $OUT/SCORES.txt
    echo "$1 ${r:-none}"
}
: > $OUT/SCORES.txt
echo "base build: $(build base)"; run base $C/gxemul
cp $IN/dev_mvme187.c.HEAD $S1
f=$(build HEAD)
if [ "$f" = fresh ]; then run HEAD $C/gxemul; else echo "HEAD [$N rows] BUILD-$f" >> $OUT/SCORES.txt; fi
run null_true /bin/true; run null_absent $C/no_such_gxemul; run null_false /bin/false
for v in $(python3 $V list); do
    if python3 $V apply $v $FIX $S1 > $OUT/apply_$v.err 2>&1; then
        f=$(build $v)
        if [ "$f" = fresh ]; then run $v $C/gxemul; else echo "$v [$N rows] BUILD-$f" >> $OUT/SCORES.txt; fi
    else
        echo "$v [$N rows] MUTANT-TEXT-NOT-FOUND" >> $OUT/SCORES.txt
    fi
done
cp $FIX $S1
echo "restore build: $(build restore)"
if cmp -s $S1 $G/GXEMUL-SEC/$S1 && [ gxemul -nt $S1 ]; then
    rm -f .MUTANT; echo "clone restored to GXEMUL-SEC and rebuilt; sentinel cleared"
else
    echo "RESTORE NOT VERIFIED -- sentinel kept"
fi
md5sum $P $V $FIX $IN/dev_mvme187.c.HEAD $OUT/../PRETABLE_4.out > $OUT/MD5.txt
echo TABLE4_MEMC_DONE
