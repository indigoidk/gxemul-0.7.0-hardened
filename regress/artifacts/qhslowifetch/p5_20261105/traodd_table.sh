#!/bin/bash
# traodd_table.sh -- qhslowifetch pass 5, Mythos breach 2, MEASURED before its repair: `T ra` from 0xfec00004 (aligned) and 0xfec00005
# (unaligned) on the fix and on two variants of arm (a)'s guard -- A1 `&& cpu->pc == addr`, A2 `&& !(cpu->pc & 3)` -- plus the 79-row
# probe on each variant.  Mutates ONLY /tmp/gxqhs10 (a cp -a of build/) under a clone-local .MUTANT sentinel; cleared only after the
# restore cmp's against GXEMUL-SEC and rebuilds fresh.
set -u
G=/mnt/c/DocumentNoSnc/cc/GXEMUL
C=/tmp/gxqhs10
OUT=$G/GXEMUL-SEC/regress/artifacts/qhslowifetch/p5_20261105/traodd_table
FIX=$G/GXEMUL-SEC/regress/artifacts/qhslowifetch/r5_20261105/cpu_ppc_instr.c.fix5
W=$G/GXEMUL-SEC/regress/artifacts/qhslowifetch/p5_20261105/traodd_witness.py
P=$G/GXEMUL-SEC/regress/artifacts/qhslowifetch/r5_20261105/table5/probe79_frozen.py
VP=$G/GXEMUL-SEC/regress/artifacts/qhslowifetch/p5_20261105/traodd_variant.py
S1=src/cpus/cpu_ppc_instr.c
mkdir -p $OUT
rm -rf $C && cp -a $G/build $C || { echo "CLONE FAILED"; exit 3; }
cd $C || exit 3
echo "$S1: qhslowifetch traodd table; baseline $FIX (with #575's two lines, as GXEMUL-SEC)" > .MUTANT
cmp -s $S1 $G/GXEMUL-SEC/$S1 || { echo "clone source = GXEMUL-SEC: NO"; exit 4; }
cp $S1 $OUT/cpu_ppc_instr.c.base
build() {
    rm -f src/cpus/cpu_ppc*.o
    make -j4 > $OUT/build_$1.log 2>&1
    rc=$?
    if [ $rc = 0 ] && [ src/cpus/cpu_ppc.o -nt $S1 ] && [ gxemul -nt src/cpus/cpu_ppc.o ]; then echo fresh; else echo "STALE_rc$rc"; fi
}
wit() {
    for a in 0xfec00004 0xfec00005; do
        (cd $OUT && timeout 120 python3 $W $C/gxemul $1 $a | grep '^TRAODD ')
    done
}
echo "base build: $(build base)"; wit base
for V in A1 A2; do
    python3 $VP $OUT/cpu_ppc_instr.c.base $S1 $V || { echo "VARIANT $V NOT APPLIED"; continue; }
    echo "$V build: $(build $V)"; wit $V
    python3 -u $P $C/gxemul $V > $OUT/probe79_$V.out 2>&1
    grep -E '^PPC_IFETCH_(RESULT|CONTROL|SYMPTOM|RED)=' $OUT/probe79_$V.out
done
cp $OUT/cpu_ppc_instr.c.base $S1
echo "restore build: $(build restore)"
if cmp -s $S1 $G/GXEMUL-SEC/$S1 && [ gxemul -nt $S1 ]; then rm -f .MUTANT; echo "clone restored and rebuilt; sentinel cleared"; else echo "RESTORE NOT VERIFIED -- sentinel kept"; fi
echo TRAODD_TABLE_DONE
