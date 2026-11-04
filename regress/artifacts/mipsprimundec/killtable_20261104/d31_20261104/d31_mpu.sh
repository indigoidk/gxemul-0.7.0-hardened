#!/bin/bash
# d31_mpu.sh -- cloud Fable 5.1's D31 follow-up (adj_20261104/ADJ2_D31_FABLE.md: D31 ROW-OWED, HOLD until measured).  Measures the
# 122-row probe (the R5900 row `r59 mdmx notRI` added) on: the round's post-fix working set WITH the adjudicated comments (base122),
# test variant D31 (the MDMX arm's R5900 test made false, mpu_variants2.py), HEAD's cpu_mips_instr.c, and the two dead-binary legs.
# Runs from a FROZEN copy (d31_mpu.run.sh); every input is a frozen copy beside it: probe122_frozen.py, cpu_mips_instr.c.base122,
# cpu_mips_instr.c.HEAD, mpu_variants.py, mpu_variants2.py.  Mutates ONLY the WSL scratch clone /tmp/gxmpud31 (a cp -a of build/),
# under a clone-local .MUTANT sentinel cleared only after the restore is cmp'd against GXEMUL-SEC and rebuilt fresh.  Rebuild per
# variant: rm src/cpus/cpu_mips*.o, make, and require cpu_mips.o -nt the source AND gxemul -nt cpu_mips.o (table 1's recipe).
set -u
G=/mnt/c/DocumentNoSnc/cc/GXEMUL
C=/tmp/gxmpud31
OUT=$G/GXEMUL-SEC/regress/artifacts/mipsprimundec/killtable_20261104/d31_20261104
V=$OUT/mpu_variants2.py
P=$OUT/probe122_frozen.py
SRC=src/cpus/cpu_mips_instr.c
BASE=$OUT/cpu_mips_instr.c.base122
HEADF=$OUT/cpu_mips_instr.c.HEAD
rm -rf $C && cp -a $G/build $C || { echo "CLONE FAILED"; exit 3; }
cd $C || exit 3
echo "$SRC: the D31 measurement for mipsprimundec; baseline $BASE" > .MUTANT
cmp -s $SRC $BASE && echo "clone source = baseline (base122): yes" || { echo "clone source = baseline: NO"; exit 4; }
build() {
    rm -f src/cpus/cpu_mips*.o
    make -j4 > $OUT/build_$1.log 2>&1
    rc=$?
    if [ $rc = 0 ] && [ src/cpus/cpu_mips.o -nt $SRC ] && [ gxemul -nt src/cpus/cpu_mips.o ]; then echo fresh; else echo "STALE_rc$rc"; fi
}
run() {   # label binary
    python3 -u $P $2 $1 > $OUT/probe_$1.out 2>&1
    r=$(grep '^MIPS_PRIMUNDEC_RESULT=' $OUT/probe_$1.out | cut -d= -f2)
    ctl=$(grep '^MIPS_PRIMUNDEC_CONTROL=' $OUT/probe_$1.out | cut -d= -f2)
    red=$(grep '^MIPS_PRIMUNDEC_RED=' $OUT/probe_$1.out | cut -d= -f2)
    last=$(tail -n 1 $OUT/probe_$1.out)
    echo "$1 $r CONTROL=$ctl $last RED=$red" >> $OUT/SCORES_D31.txt
    echo "$1 $r"
}
: > $OUT/SCORES_D31.txt
echo "base122 build: $(build base122)"
run base122 $C/gxemul
cp $BASE $SRC
if python3 $V apply D31_r5900_false $BASE $SRC > $OUT/apply_D31.err 2>&1; then
    f=$(build D31)
    if [ "$f" = fresh ]; then run D31 $C/gxemul; else echo "D31 BUILD-$f" >> $OUT/SCORES_D31.txt; echo "D31 BUILD-$f"; fi
else
    echo "D31 MUTANT-TEXT-NOT-FOUND" >> $OUT/SCORES_D31.txt; echo "D31 MUTANT-TEXT-NOT-FOUND"
fi
cp $HEADF $SRC
f=$(build HEAD)
if [ "$f" = fresh ]; then run HEAD $C/gxemul; else echo "HEAD BUILD-$f" >> $OUT/SCORES_D31.txt; echo "HEAD BUILD-$f"; fi
run deadtrue /bin/true
run deadabsent $C/no_such_gxemul
cp $BASE $SRC
echo "restore build: $(build restore)"
if cmp -s $SRC $G/GXEMUL-SEC/$SRC && [ gxemul -nt $SRC ]; then rm -f .MUTANT; echo "clone restored to GXEMUL-SEC and rebuilt; sentinel cleared"; else echo "RESTORE NOT VERIFIED -- sentinel kept"; fi
md5sum $P $BASE $HEADF $V $OUT/mpu_variants.py > $OUT/MD5.txt
echo D31_MPU_DONE
