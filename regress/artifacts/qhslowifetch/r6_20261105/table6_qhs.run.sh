#!/bin/bash
# table3_qhs.sh -- qhslowifetch TEST-VARIANT TABLE 3 (repair 3: 60 rows, 30 variants) (FINAL_FABLE.md F8: ONE instrument at the final row count, every SCORES line naming
# it).  Legs first, in the same clone: base (the final candidate), the HEAD leg (cpu_ppc_instr.c.HEAD + cpu_ppc.h.HEAD), three null
# media; then the 27 variants of qhs_variants_2.py.  PRETABLE_2.out must exist first (its mtime precedes table2/'s files).  Mutates
# ONLY /tmp/gxqhs2 (a cp -a of build/) under a clone-local .MUTANT sentinel, cleared only after the restore cmp's against GXEMUL-SEC
# and rebuilds fresh.
set -u
G=/mnt/c/DocumentNoSnc/cc/GXEMUL
C=/tmp/gxqhs11
IN=$G/GXEMUL-SEC/regress/artifacts/qhslowifetch/det_20261104
OUT=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/qhslowifetch/r6_20261105/table6
P=$OUT/probe82_frozen.py
N=82
V=$OUT/../qhs_variants_6.py
FIX=$OUT/../cpu_ppc_instr.c.fix6
S1=src/cpus/cpu_ppc_instr.c
S2=src/include/cpu_ppc.h
[ -f $OUT/../PRETABLE_6.out ] || { echo "NO PRETABLE_2.out -- refusing"; exit 2; }
[ -f $P ] || { echo "NO frozen probe $P -- refusing"; exit 2; }
rm -rf $C && cp -a $G/build $C || { echo "CLONE FAILED"; exit 3; }
cd $C || exit 3
echo "$S1: qhslowifetch table 6; baseline $FIX" > .MUTANT
cmp -s $S1 $FIX && cmp -s $S2 $IN/cpu_ppc.h.fix || { echo "clone source = baseline: NO"; exit 4; }
build() {
    rm -f src/cpus/cpu_ppc*.o
    make -j4 > $OUT/build_$1.log 2>&1
    rc=$?
    if [ $rc = 0 ] && [ src/cpus/cpu_ppc.o -nt $S1 ] && [ gxemul -nt src/cpus/cpu_ppc.o ]; then echo fresh; else echo "STALE_rc$rc"; fi
}
run() {   # label binary
    python3 -u $P $2 $1 $OUT/sessions_$1 > $OUT/probe_$1.out 2>&1
    r=$(grep '^PPC_IFETCH_RESULT=' $OUT/probe_$1.out | cut -d= -f2)
    c=$(grep '^PPC_IFETCH_CONTROL=' $OUT/probe_$1.out | cut -d= -f2)
    y=$(grep '^PPC_IFETCH_SYMPTOM=' $OUT/probe_$1.out | cut -d= -f2)
    red=$(grep '^PPC_IFETCH_RED=' $OUT/probe_$1.out | cut -d= -f2)
    echo "$1 [$N rows] ${r:-none} CONTROL=${c:-none} SYMPTOM=${y:-none} $(tail -n 1 $OUT/probe_$1.out) RED=${red:-none}" >> $OUT/SCORES.txt
    echo "$1 ${r:-none}"
}
: > $OUT/SCORES.txt
echo "base build: $(build base)"; run base $C/gxemul
cp $IN/cpu_ppc_instr.c.HEAD $S1; cp $IN/cpu_ppc.h.HEAD $S2
echo "HEAD build: $(build HEAD)"; run HEAD $C/gxemul
cp $IN/cpu_ppc.h.fix $S2
run null_true /bin/true; run null_absent /nonexistent/gxemul; run null_false /bin/false
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
if cmp -s $S1 $G/GXEMUL-SEC/$S1 && cmp -s $S2 $G/GXEMUL-SEC/$S2 && [ gxemul -nt $S1 ]; then
    rm -f .MUTANT; echo "clone restored to GXEMUL-SEC and rebuilt; sentinel cleared"
else
    echo "RESTORE NOT VERIFIED -- sentinel kept"
fi
md5sum $P $V $FIX $IN/cpu_ppc.h.fix $IN/cpu_ppc_instr.c.HEAD $IN/cpu_ppc.h.HEAD $OUT/../PRETABLE_6.out > $OUT/MD5.txt
echo TABLE6_QHS_DONE
