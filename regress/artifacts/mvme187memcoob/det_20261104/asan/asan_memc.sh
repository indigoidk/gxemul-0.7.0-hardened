#!/bin/bash
# asan_memc.sh -- the mvme187memcoob sanitizer legs (the reconciliation's R1 and R2): the 56-row probe on the fix, on HEAD's
# dev_mvme187.c and on B3 (the indexed read before the switch reinstated, memc_variants.py), each built once with build-asan's flags
# (-O3, address + undefined: R1) and once with the device object at -O0, address only (R2).  The probe's `asan reports` row counts
# AddressSanitizer / "runtime error:" lines over every session.  Mutates ONLY the WSL scratch clone /tmp/gxmemcasan (a cp -a of
# build-asan/) under a clone-local .MUTANT sentinel, cleared only after the source and the Makefile are restored, cmp'd against
# GXEMUL-SEC / build-asan, and the binary rebuilt fresh.
set -u
# Run 2: the repo's ASAN gate options (regress/gate_asan_sweep.sh) -- run 1 counted LeakSanitizer's exit report (run1_leaks/).
export ASAN_OPTIONS=detect_leaks=0:abort_on_error=0:print_summary=1:verify_asan_link_order=0
export UBSAN_OPTIONS=print_stacktrace=0
G=/mnt/c/DocumentNoSnc/cc/GXEMUL
C=/tmp/gxmemcasan
IN=$G/GXEMUL-SEC/regress/artifacts/mvme187memcoob/det_20261104
OUT=$IN/asan
P=$IN/legs56/probe56_frozen.py
V=$IN/memc_variants.py
FIX=$IN/dev_mvme187.c.fix
HEADF=$IN/dev_mvme187.c.HEAD
S1=src/devices/dev_mvme187.c
O1=src/devices/dev_mvme187.o
MK=src/devices/Makefile
rm -rf $C && cp -a $G/build-asan $C || { echo "CLONE FAILED"; exit 3; }
cd $C || exit 3
echo "$S1 + $MK: mvme187memcoob sanitizer legs; baseline $FIX" > .MUTANT
cmp -s $S1 $FIX || { echo "clone source = baseline: NO"; exit 4; }
cp $MK $OUT/Makefile.devices.orig
build() {
    rm -f $O1
    make -j4 > $OUT/build_$1.log 2>&1
    rc=$?
    if [ $rc = 0 ] && [ $O1 -nt $S1 ] && [ gxemul -nt $O1 ]; then echo fresh; else echo "STALE_rc$rc"; fi
}
run() {   # label
    python3 -u $P $C/gxemul $1 $OUT/sessions_$1 > $OUT/probe_$1.out 2>&1
    r=$(grep '^MVME187_MEMC_RESULT=' $OUT/probe_$1.out | cut -d= -f2)
    red=$(grep '^MVME187_MEMC_RED=' $OUT/probe_$1.out | cut -d= -f2)
    a=$(grep -E '^asan reports ' $OUT/probe_$1.out | awk '{print $3}')
    echo "$1 $r asan=$a $(tail -n 1 $OUT/probe_$1.out) RED=$red" >> $OUT/SCORES.txt
    echo "$1 $r asan=$a"
}
leg() {   # optlabel
    cp $FIX $S1; f=$(build $1_fix); [ "$f" = fresh ] && run $1_fix || echo "$1_fix BUILD-$f" >> $OUT/SCORES.txt
    cp $HEADF $S1; f=$(build $1_HEAD); [ "$f" = fresh ] && run $1_HEAD || echo "$1_HEAD BUILD-$f" >> $OUT/SCORES.txt
    if python3 $V apply B3_idx_read $FIX $S1 > $OUT/apply_$1_B3.err 2>&1; then
        f=$(build $1_B3); [ "$f" = fresh ] && run $1_B3 || echo "$1_B3 BUILD-$f" >> $OUT/SCORES.txt
    else echo "$1_B3 MUTANT-TEXT-NOT-FOUND" >> $OUT/SCORES.txt; fi
}
: > $OUT/SCORES.txt
grep -m1 '^COPTIM=' $MK > $OUT/COPTIM_O3.txt
leg O3
sed -i 's/ -O3 -DNDEBUG -fsanitize=address,undefined / -O0 -DNDEBUG -fsanitize=address /' $MK
grep -m1 '^COPTIM=' $MK > $OUT/COPTIM_O0.txt
grep -q -- '-O0 -DNDEBUG -fsanitize=address ' $MK && leg O0 || echo "O0 MAKEFILE-EDIT-FAILED" >> $OUT/SCORES.txt
cp $OUT/Makefile.devices.orig $MK
cp $FIX $S1
echo "restore build: $(build restore)"
if cmp -s $S1 $G/GXEMUL-SEC/$S1 && cmp -s $MK $G/build-asan/$MK && [ gxemul -nt $S1 ]; then rm -f .MUTANT; echo "clone restored and rebuilt; sentinel cleared"; else echo "RESTORE NOT VERIFIED -- sentinel kept"; fi
md5sum $P $V $FIX $HEADF > $OUT/MD5.txt
echo ASAN_MEMC_DONE
