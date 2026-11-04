#!/bin/bash
# killtable_mpu.sh -- the test-variant table for the mipsprimundec fix's detector (2026-11-04).  Runs from a FROZEN copy
# (killtable_mpu.run.sh); every input it reads is a frozen copy beside it: mpu_variants.py, probe_frozen.py, cpu_mips_instr.c.base
# (the round's post-fix working set) and cpu_mips_instr.c.HEAD.  Mutates ONLY the WSL scratch clone /tmp/gxmpukt (a cp -a of
# build/), under a clone-local .MUTANT sentinel cleared only after the restore is cmp'd against GXEMUL-SEC and rebuilt fresh.
# Rebuild per variant: rm src/cpus/cpu_mips*.o (the one object that #includes cpu_mips_instr.c, and its siblings), make, and require
# cpu_mips.o -nt the source AND gxemul -nt cpu_mips.o -- a narrowed form of the carrier's `rm src/cpus/*.o`, with a per-variant
# freshness proof instead.
set -u
G=/mnt/c/DocumentNoSnc/cc/GXEMUL
C=/tmp/gxmpukt
OUT=$G/GXEMUL-SEC/regress/artifacts/mipsprimundec/killtable_20261104
V=$OUT/mpu_variants.py
P=$OUT/probe_frozen.py
SRC=src/cpus/cpu_mips_instr.c
BASE=$OUT/cpu_mips_instr.c.base
rm -rf $C && cp -a $G/build $C || { echo "CLONE FAILED"; exit 3; }
cd $C || exit 3
echo "$SRC: test variants of the mipsprimundec fix; baseline $BASE" > .MUTANT
cmp -s $SRC $BASE && echo "clone source = baseline: yes" || { echo "clone source = baseline: NO"; exit 4; }
build() {
    rm -f src/cpus/cpu_mips*.o
    make -j4 > $OUT/build_$1.log 2>&1
    rc=$?
    if [ $rc = 0 ] && [ src/cpus/cpu_mips.o -nt $SRC ] && [ gxemul -nt src/cpus/cpu_mips.o ]; then echo fresh; else echo "STALE_rc$rc"; fi
}
run() {
    python3 -u $P $C/gxemul $1 > $OUT/probe_$1.out 2>&1
    r=$(grep '^MIPS_PRIMUNDEC_RESULT=' $OUT/probe_$1.out | cut -d= -f2)
    red=$(grep '^MIPS_PRIMUNDEC_RED=' $OUT/probe_$1.out | cut -d= -f2)
    last=$(tail -n 1 $OUT/probe_$1.out)
    echo "$1 $r $last RED=$red" >> $OUT/SCORES.txt
    echo "$1 $r"
}
: > $OUT/SCORES.txt
echo "base build: $(build base)"
run base
for m in $(python3 $V list); do
    cp $BASE $SRC
    if ! python3 $V apply $m $BASE $SRC > $OUT/apply_$m.err 2>&1; then
        echo "$m MUTANT-TEXT-NOT-FOUND" >> $OUT/SCORES.txt; echo "$m MUTANT-TEXT-NOT-FOUND"; continue
    fi
    f=$(build $m)
    if [ "$f" != fresh ]; then echo "$m BUILD-$f" >> $OUT/SCORES.txt; echo "$m BUILD-$f"; continue; fi
    run $m
done
cp $BASE $SRC
echo "restore build: $(build restore)"
if cmp -s $SRC $G/GXEMUL-SEC/$SRC && [ gxemul -nt $SRC ]; then rm -f .MUTANT; echo "clone restored to GXEMUL-SEC and rebuilt; sentinel cleared"; else echo "RESTORE NOT VERIFIED -- sentinel kept"; fi
echo KILLTABLE_MPU_DONE
