#!/bin/bash
# b3repeat_memc7.sh -- mvme187memcoob repair 6: characterise table 6's one PRED=MISS.  B3 (the indexed read reinstated) reddened
# R17 f3 r2 in table 6 (0xd8; table 5 read 0x0 there).  This builds ONE B3 binary in a fresh scratch clone and runs the frozen
# 213-row probe on it three times, so the record can say whether the value is stable for one binary or varies run to run.
# Baseline: GXEMUL-SEC/src/devices/dev_mvme187.c; base built first (rm src/cpus/*.o and the device object) and run once.
# Mutates ONLY /tmp/gxmemc9 (a cp -a of build/) under a clone-local .MUTANT sentinel, cleared only after the restored source cmp's
# against GXEMUL-SEC and the rebuilt binary is newer than it.  Run from a frozen copy (b3repeat_memc7.run.sh).
set -u
G=/mnt/c/DocumentNoSnc/cc/GXEMUL
SEC=$G/GXEMUL-SEC
MD=$SEC/regress/artifacts/mvme187memcoob
OUT=$MD/r7_20261105/b3repeat
C=/tmp/gxmemc9
P=$MD/r7_20261105/table6/probe213_frozen.py
V=$MD/r5_20261105/memc_variants_5.py
FIX=$SEC/src/devices/dev_mvme187.c
S1=src/devices/dev_mvme187.c
O1=src/devices/dev_mvme187.o
[ -e $C ] && { echo "$C exists -- refusing"; exit 2; }
mkdir -p $OUT
echo "b3 repeat start $(date -u +%FT%TZ)"
cp -a $G/build $C || { echo "CLONE FAILED"; exit 3; }
cd $C || exit 3
echo "$S1: mvme187memcoob repair 6, B3 repeat; baseline $FIX" > .MUTANT
mkdir -p logs
cmp -s $S1 $FIX && echo "clone source = baseline: yes" || { echo "clone source = baseline: NO"; exit 4; }
build() {   # label [full]
    if [ "${2:-}" = full ]; then rm -f src/cpus/*.o; fi
    rm -f $O1
    make -j4 > logs/build_$1.log 2>&1
    rc=$?
    if [ $rc = 0 ] && [ $O1 -nt $S1 ] && [ gxemul -nt $O1 ]; then echo fresh; else cp logs/build_$1.log $OUT/build_$1.log; echo "STALE_rc$rc"; fi
}
f=$(build base full); echo "base build: $f"; [ "$f" = fresh ] || exit 5
python3 -u $P $C/gxemul base $C/s_base > $OUT/probe_base.out 2>&1
echo "base: $(grep '^MVME187_MEMC_RESULT=' $OUT/probe_base.out) $(grep '^R17 f3 r2' $OUT/probe_base.out | cut -c1-40) $(tail -n 1 $OUT/probe_base.out)"
python3 $V apply B3_idx_read $FIX $S1 > logs/apply_B3.err 2>&1 || { echo "APPLY FAILED"; cat logs/apply_B3.err; exit 6; }
f=$(build B3); echo "B3 build: $f"; [ "$f" = fresh ] || exit 5
md5sum gxemul > $OUT/MD5_B3_binary.txt
for i in 1 2 3; do
    python3 -u $P $C/gxemul B3run$i $C/s_b3_$i > $OUT/probe_B3run$i.out 2>&1
    echo "B3 run $i: $(grep '^MVME187_MEMC_RESULT=' $OUT/probe_B3run$i.out) $(grep '^MVME187_MEMC_RED=' $OUT/probe_B3run$i.out) [R17 f3 r2: $(grep '^R17 f3 r2' $OUT/probe_B3run$i.out | awk '{print $4}')] $(tail -n 1 $OUT/probe_B3run$i.out)"
done
cp $FIX $S1
f=$(build restore); echo "restore build: $f"
if [ "$f" = fresh ] && cmp -s $S1 $SEC/$S1 && [ gxemul -nt $S1 ]; then
    rm -f .MUTANT; echo "clone restored to GXEMUL-SEC and rebuilt; sentinel cleared"
else
    echo "RESTORE NOT VERIFIED -- sentinel kept"
fi
echo "b3 repeat end $(date -u +%FT%TZ)"
echo B3REPEAT_MEMC7_DONE
