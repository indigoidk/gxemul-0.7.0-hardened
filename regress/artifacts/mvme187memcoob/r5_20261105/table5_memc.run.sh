#!/bin/bash
# table5_memc.sh -- mvme187memcoob TEST-VARIANT TABLE 5 (repair 5, 206 rows; p4_20261105/CONS_MYTHOS_local.md sections 3-4):
# table 4's 112 variants re-applied to the current fix plus the L-walk's built cells (memc_variants_5.py; PRETABLE_5.out written
# first, every prediction derived before this runs).  Legs first, in the same clone: base (GXEMUL-SEC's dev_mvme187.c, which repair
# 5 did not change), the HEAD leg (det_20261104/dev_mvme187.c.HEAD) and three null media.  Every SCORES line names the row count,
# the measured red set and PRED= (match / atleast-ok / MISS / none) against PRED_MAP.txt, the machine-readable form of PRETABLE_5.
# Mutates ONLY the WSL scratch clone /tmp/gxmemc6 (a cp -a of build/) under a clone-local .MUTANT sentinel, cleared only after the
# restore cmp's against GXEMUL-SEC and rebuilds fresh.  Rebuild: rm the device object, make; require dev_mvme187.o -nt the source
# and gxemul -nt the object.  Variant session transcripts stay in the clone (/mnt/c is slow) and are copied out only on a MISS;
# the legs' transcripts are copied out always.
set -u
G=/mnt/c/DocumentNoSnc/cc/GXEMUL
SEC=$G/GXEMUL-SEC
C=/tmp/gxmemc6
IN=$SEC/regress/artifacts/mvme187memcoob/det_20261104
R5=$SEC/regress/artifacts/mvme187memcoob/r5_20261105
OUT=$R5/table5
P=$OUT/probe206_frozen.py
N=206
V=$R5/memc_variants_5.py
FIX=$SEC/src/devices/dev_mvme187.c
HEAD=$IN/dev_mvme187.c.HEAD
S1=src/devices/dev_mvme187.c
O1=src/devices/dev_mvme187.o
[ -f $R5/PRETABLE_5.out ] || { echo "NO PRETABLE_5.out -- refusing"; exit 2; }
[ -f $P ] || { echo "NO frozen probe $P -- refusing"; exit 2; }
[ -f $V ] || { echo "NO variant script $V -- refusing"; exit 2; }
[ -f $HEAD ] || { echo "NO HEAD source $HEAD -- refusing"; exit 2; }
[ -f $FIX ] || { echo "NO baseline $FIX -- refusing"; exit 2; }
cmp -s $P $SEC/regress/mvme187_memc_probe.py || echo "note: the frozen probe differs from the in-tree probe; the frozen one is the instrument"
rm -rf $C && cp -a $G/build $C || { echo "CLONE FAILED"; exit 3; }
cd $C || exit 3
mkdir -p $C/logs $C/sessions
echo "$S1: mvme187memcoob table 5; baseline $FIX" > .MUTANT
cmp -s $S1 $FIX || { echo "clone source = baseline: NO"; exit 4; }
# the predictions in machine-readable form (name <TAB> EXACT|ATLEAST <TAB> rows), and the model's calibration record
python3 $V predmap > $OUT/PRED_MAP.txt 2> $OUT/predmap.err || { echo "predmap FAILED"; exit 5; }
python3 $V check4 > $OUT/check4.out 2>&1
norm() {   # a comma list -> sorted comma list ("none" for empty)
    local s
    s=$(echo "$1" | tr ',' '\n' | grep -v '^$' | grep -v '^none$' | sort | tr '\n' ',' | sed 's/,$//')
    echo "${s:-none}"
}
build() {
    rm -f $O1
    make -j4 > $C/logs/build_$1.log 2>&1
    rc=$?
    if [ $rc = 0 ] && [ $O1 -nt $S1 ] && [ gxemul -nt $O1 ]; then echo fresh; else cp $C/logs/build_$1.log $OUT/build_$1.log; echo "STALE_rc$rc"; fi
}
run() {   # label binary keep-sessions(1/0)
    local sess=$C/sessions/$1
    rm -rf $sess
    python3 -u $P $2 $1 $sess > $OUT/probe_$1.out 2>&1
    r=$(grep '^MVME187_MEMC_RESULT=' $OUT/probe_$1.out | cut -d= -f2)
    ctl=$(grep '^MVME187_MEMC_CONTROL=' $OUT/probe_$1.out | cut -d= -f2)
    sym=$(grep '^MVME187_MEMC_SYMPTOM=' $OUT/probe_$1.out | cut -d= -f2)
    asan=$(grep '^MVME187_MEMC_ASAN=' $OUT/probe_$1.out | cut -d= -f2)
    red=$(grep '^MVME187_MEMC_RED=' $OUT/probe_$1.out | cut -d= -f2)
    red=${red:-none}
    pline=$(awk -F'\t' -v n="$1" '$1 == n' $OUT/PRED_MAP.txt | head -n 1)
    verdict=none
    if [ -n "$pline" ]; then
        kind=$(echo "$pline" | cut -f2)
        pset=$(echo "$pline" | cut -f3)
        if [ "$kind" = EXACT ]; then
            if [ "$(norm "$red")" = "$(norm "$pset")" ]; then verdict=match; else verdict=MISS; fi
        else
            verdict=atleast-ok
            if [ "$pset" != none ]; then
                for row in $(echo "$pset" | tr ',' ' '); do
                    echo ",$red," | grep -q ",$row," || verdict=MISS
                done
            fi
        fi
    fi
    echo "$1 [$N rows] ${r:-none} CONTROL=${ctl:-none} SYMPTOM=${sym:-none} ASAN=${asan:-none} $(tail -n 1 $OUT/probe_$1.out) RED=$red PRED=$verdict" >> $OUT/SCORES.txt
    if [ "$3" = 1 ] || [ "$verdict" = MISS ]; then rm -rf $OUT/sessions_$1; cp -r $sess $OUT/sessions_$1; fi
    echo "$1 ${r:-none} PRED=$verdict"
}
: > $OUT/SCORES.txt
echo "base build: $(build base)"; run base $C/gxemul 1
cp $HEAD $S1
f=$(build HEAD)
if [ "$f" = fresh ]; then run HEAD $C/gxemul 1; else echo "HEAD [$N rows] BUILD-$f" >> $OUT/SCORES.txt; fi
cp $FIX $S1
run null_true /bin/true 1; run null_absent $C/no_such_gxemul 1; run null_false /bin/false 1
VARS=$(python3 $V list) || { echo "list FAILED"; exit 5; }
nv=$(echo $VARS | wc -w)
echo "variants: $nv (PRED_MAP lines: $(wc -l < $OUT/PRED_MAP.txt))"
for v in $VARS; do
    if python3 $V apply $v $FIX $S1 > $C/logs/apply_$v.err 2>&1; then
        f=$(build $v)
        if [ "$f" = fresh ]; then run $v $C/gxemul 0; else echo "$v [$N rows] BUILD-$f" >> $OUT/SCORES.txt; fi
    else
        cp $C/logs/apply_$v.err $OUT/apply_$v.err
        echo "$v [$N rows] MUTANT-TEXT-NOT-FOUND" >> $OUT/SCORES.txt
    fi
done
cp $FIX $S1
echo "restore build: $(build restore)"
if cmp -s $S1 $SEC/$S1 && [ gxemul -nt $S1 ]; then
    rm -f .MUTANT; echo "clone restored to GXEMUL-SEC and rebuilt; sentinel cleared"
else
    echo "RESTORE NOT VERIFIED -- sentinel kept"
fi
{
    echo "variants run: $nv"
    echo "PRED=match:      $(grep -c 'PRED=match' $OUT/SCORES.txt)"
    echo "PRED=atleast-ok: $(grep -c 'PRED=atleast-ok' $OUT/SCORES.txt)"
    echo "PRED=MISS:       $(grep -c 'PRED=MISS' $OUT/SCORES.txt)"
    echo "PRED=none:       $(grep -c 'PRED=none' $OUT/SCORES.txt)"
    echo "BUILD failures:  $(grep -c 'BUILD-' $OUT/SCORES.txt)"
    echo "text not found:  $(grep -c 'MUTANT-TEXT-NOT-FOUND' $OUT/SCORES.txt)"
    echo "variants scoring $N/$N (survivors, base excluded): $(grep -v '^base ' $OUT/SCORES.txt | grep -c " $N/$N ")"
    echo "MISS lines:"; grep 'PRED=MISS' $OUT/SCORES.txt | cut -d' ' -f1
} > $OUT/TALLY.txt
cat $OUT/TALLY.txt
md5sum $P $V $FIX $HEAD $R5/PRETABLE_5.out $OUT/PRED_MAP.txt > $OUT/MD5.txt
echo TABLE5_MEMC_DONE
