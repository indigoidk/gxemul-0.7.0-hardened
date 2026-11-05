#!/bin/bash
# table1_qhs.sh -- test-variant table 1 for the qhslowifetch detector (legs50/probe50_frozen.py, 50 rows).  For each variant of
# qhs_variants.py: apply it to the frozen post-fix source (cpu_ppc_instr.c.fix), rebuild, run the probe.  PRETABLE.out (the
# predictions) was written before this script.  Mutates ONLY the WSL scratch clone /tmp/gxqhstab (a cp -a of build/) under a
# clone-local .MUTANT sentinel, cleared only after the restore cmp's against GXEMUL-SEC and rebuilds fresh.  Rebuild per variant:
# rm src/cpus/cpu_ppc*.o, make; require cpu_ppc.o -nt the source and gxemul -nt cpu_ppc.o.  Runs from a frozen copy.
set -u
G=/mnt/c/DocumentNoSnc/cc/GXEMUL
C=/tmp/gxqhstab
IN=$G/GXEMUL-SEC/regress/artifacts/qhslowifetch/det_20261104
OUT=$IN/table1
P=$IN/legs50/probe50_frozen.py
V=$IN/qhs_variants.py
FIX=$IN/cpu_ppc_instr.c.fix
S1=src/cpus/cpu_ppc_instr.c
S2=src/include/cpu_ppc.h
rm -rf $C && cp -a $G/build $C || { echo "CLONE FAILED"; exit 3; }
cd $C || exit 3
echo "$S1: qhslowifetch test-variant table 1; baseline $FIX" > .MUTANT
if cmp -s $S1 $FIX && cmp -s $S2 $IN/cpu_ppc.h.fix; then echo "clone source = baseline: yes"; else echo "clone source = baseline: NO"; exit 4; fi
build() {
    rm -f src/cpus/cpu_ppc*.o
    make -j4 > $OUT/build_$1.log 2>&1
    rc=$?
    if [ $rc = 0 ] && [ src/cpus/cpu_ppc.o -nt $S1 ] && [ gxemul -nt src/cpus/cpu_ppc.o ]; then echo fresh; else echo "STALE_rc$rc"; fi
}
run() {   # label binary
    python3 -u $P $2 $1 > $OUT/probe_$1.out 2>&1
    r=$(grep '^PPC_IFETCH_RESULT=' $OUT/probe_$1.out | cut -d= -f2)
    ctl=$(grep '^PPC_IFETCH_CONTROL=' $OUT/probe_$1.out | cut -d= -f2)
    red=$(grep '^PPC_IFETCH_RED=' $OUT/probe_$1.out | cut -d= -f2)
    last=$(tail -n 1 $OUT/probe_$1.out)
    echo "$1 $r CONTROL=$ctl $last RED=$red" >> $OUT/SCORES.txt
    echo "$1 $r"
}
: > $OUT/SCORES.txt
echo "base build: $(build base)"
run base $C/gxemul
for v in $(python3 $V list); do
    if python3 $V apply $v $FIX $S1 > $OUT/apply_$v.err 2>&1; then
        f=$(build $v)
        if [ "$f" = fresh ]; then run $v $C/gxemul; else echo "$v BUILD-$f" >> $OUT/SCORES.txt; echo "$v BUILD-$f"; fi
    else
        echo "$v MUTANT-TEXT-NOT-FOUND" >> $OUT/SCORES.txt; echo "$v MUTANT-TEXT-NOT-FOUND"
    fi
done
cp $FIX $S1
echo "restore build: $(build restore)"
if cmp -s $S1 $G/GXEMUL-SEC/$S1 && cmp -s $S2 $G/GXEMUL-SEC/$S2 && [ gxemul -nt $S1 ]; then rm -f .MUTANT; echo "clone restored to GXEMUL-SEC and rebuilt; sentinel cleared"; else echo "RESTORE NOT VERIFIED -- sentinel kept"; fi
md5sum $P $V $FIX $IN/cpu_ppc.h.fix $IN/PRETABLE.out > $OUT/MD5.txt
echo TABLE1_QHS_DONE
