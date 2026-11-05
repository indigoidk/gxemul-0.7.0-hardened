#!/bin/bash
# table1b_qhs.sh -- qhslowifetch table 1b: base, D14_c_meset and D15_dom_ok, each built once in a scratch clone and measured by BOTH the
# 50-row probe sent to pass 2 and the 52-row candidate (two noT rows).  PRETABLE_1b.out was written first.  Baseline: the
# post-fix source WITH the D8 comment rewording (cpu_ppc_instr.c.fix2, comment-only different from .fix).  Mutates ONLY /tmp/gxqhs1b
# (a cp -a of build/) under a clone-local .MUTANT sentinel, cleared only after the restore cmp's against GXEMUL-SEC and rebuilds fresh.
set -u
G=/mnt/c/DocumentNoSnc/cc/GXEMUL
C=/tmp/gxqhs1b
IN=$G/GXEMUL-SEC/regress/artifacts/qhslowifetch/det_20261104
OUT=$IN/table1b
P50=$IN/legs50/probe50_frozen.py
P52=$OUT/probe52c.py
V=$IN/qhs_variants_1b.py
FIX=$IN/cpu_ppc_instr.c.fix2
S1=src/cpus/cpu_ppc_instr.c
rm -rf $C && cp -a $G/build $C || { echo "CLONE FAILED"; exit 3; }
cd $C || exit 3
echo "$S1: qhslowifetch table 1b; baseline $FIX" > .MUTANT
cmp -s $S1 $FIX && cmp -s src/include/cpu_ppc.h $IN/cpu_ppc.h.fix || { echo "clone source = baseline: NO"; exit 4; }
build() {
    rm -f src/cpus/cpu_ppc*.o
    make -j4 > $OUT/build_$1.log 2>&1
    rc=$?
    if [ $rc = 0 ] && [ src/cpus/cpu_ppc.o -nt $S1 ] && [ gxemul -nt src/cpus/cpu_ppc.o ]; then echo fresh; else echo "STALE_rc$rc"; fi
}
run() {   # label probe tag
    python3 -u $2 $C/gxemul $1 > $OUT/probe_$1_$3.out 2>&1
    r=$(grep '^PPC_IFETCH_RESULT=' $OUT/probe_$1_$3.out | cut -d= -f2)
    red=$(grep '^PPC_IFETCH_RED=' $OUT/probe_$1_$3.out | cut -d= -f2)
    echo "$1 [$3] $r $(tail -n 1 $OUT/probe_$1_$3.out) RED=$red" >> $OUT/SCORES.txt
    echo "$1 [$3] $r"
}
: > $OUT/SCORES.txt
echo "base build: $(build base)"
run base $P50 p50; run base $P52 p52
for v in $(python3 $V list); do
    if python3 $V apply $v $FIX $S1 > $OUT/apply_$v.err 2>&1; then
        f=$(build $v)
        if [ "$f" = fresh ]; then run $v $P50 p50; run $v $P52 p52; else echo "$v BUILD-$f" >> $OUT/SCORES.txt; fi
    else
        echo "$v MUTANT-TEXT-NOT-FOUND" >> $OUT/SCORES.txt
    fi
done
cp $FIX $S1
echo "restore build: $(build restore)"
if cmp -s $S1 $G/GXEMUL-SEC/$S1 && [ gxemul -nt $S1 ]; then rm -f .MUTANT; echo "clone restored to GXEMUL-SEC and rebuilt; sentinel cleared"; else echo "RESTORE NOT VERIFIED -- sentinel kept"; fi
md5sum $P50 $P52 $V $FIX $IN/PRETABLE_1b.out > $OUT/MD5.txt
echo TABLE1B_QHS_DONE
