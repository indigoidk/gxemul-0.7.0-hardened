#!/bin/bash
# table6_memc.sh -- mvme187memcoob TEST-VARIANT TABLE 6 (repair 6: session R18, 213 rows; regress_20261105/REG_MYTHOS_local.md
# section 2(d), regress_20261105/DISPOSITION.md).  Legs first, in ONE fresh clone: base (GXEMUL-SEC's dev_mvme187.c, which repair 6
# does not change), HEAD (det_20261104/dev_mvme187.c.HEAD), three null media, B1-B3 (table 4's verbatim reinstatements, applied by
# memc_variants_5.py); then the eight own-latch variants; then the other 657 of table 5's 665 green representatives
# (table6/VARS_6.txt = memc_pretable_6.py vars).  PRETABLE_6.out is written first; every SCORES line names the row count, the
# measured red set and PRED= (match / MISS / none) against table6/PRED_MAP_6.txt, PRETABLE_6's machine-readable form.
# Mutates ONLY the WSL scratch clone /tmp/gxmemc8 (a cp -a of build/) under a clone-local .MUTANT sentinel, cleared only after the
# restored source cmp's against GXEMUL-SEC and the rebuilt binary is newer than it.  Baseline build: rm src/cpus/*.o and the device
# object, make; variant builds: rm the device object, make (dev_mvme187.c is #included by nothing); every build must leave
# dev_mvme187.o -nt the source and gxemul -nt the object.  Session transcripts are copied out for the legs, the eight and any MISS.
# Run from a frozen copy (table6_memc.run.sh).
set -u
G=/mnt/c/DocumentNoSnc/cc/GXEMUL
SEC=$G/GXEMUL-SEC
MD=$SEC/regress/artifacts/mvme187memcoob
R7=$MD/r7_20261105
OUT=$R7/table6
C=/tmp/gxmemc8
P=$OUT/probe213_frozen.py
N=213
V=$MD/r5_20261105/memc_variants_5.py
FIX=$SEC/src/devices/dev_mvme187.c
HEAD=$MD/det_20261104/dev_mvme187.c.HEAD
S1=src/devices/dev_mvme187.c
O1=src/devices/dev_mvme187.o
PM=$OUT/PRED_MAP_6.txt
EIGHT=" L_MB_M_xori_any L_ME_M_xori_any L_DB_D_xori_any L_DA_D_xori_any L_MT_M_xori_M L_MW_M_xori_M L_DT_D_xori_D L_DT_D_idat_W.D "
[ -f $R7/PRETABLE_6.out ] || { echo "NO PRETABLE_6.out -- refusing"; exit 2; }
for f in $P $V $FIX $HEAD $PM $OUT/VARS_6.txt; do [ -f $f ] || { echo "NO $f -- refusing"; exit 2; }; done
[ "$(md5sum < $P | cut -c1-32)" = 1d69cc4e6cb1499894fdf1fcbe3049bd ] || { echo "frozen probe is not PRETABLE_6's instrument -- refusing"; exit 2; }
[ -e $C ] && { echo "$C exists -- refusing to overwrite a clone this script did not make"; exit 2; }
[ -e $OUT/SCORES.txt ] && { echo "$OUT/SCORES.txt exists -- refusing to overwrite a measurement"; exit 2; }
cmp -s $P $SEC/regress/mvme187_memc_probe.py || echo "note: the frozen probe differs from the in-tree probe; the frozen one is the instrument"
echo "table 6 start $(date -u +%FT%TZ); PRETABLE_6.out mtime $(date -u -r $R7/PRETABLE_6.out +%FT%TZ)"
cp -a $G/build $C || { echo "CLONE FAILED"; exit 3; }
cd $C || exit 3
echo "$S1: mvme187memcoob repair 6 table 6 (213 rows); baseline $FIX" > .MUTANT
mkdir -p $C/logs $C/sessions
if cmp -s $S1 $FIX; then echo "clone source = baseline: yes"; else echo "clone source = baseline: NO -- refusing"; exit 4; fi
norm() {   # a comma list -> sorted comma list ("none" for empty)
    local s
    s=$(echo "$1" | tr ',' '\n' | grep -v '^$' | grep -v '^none$' | sort | tr '\n' ',' | sed 's/,$//')
    echo "${s:-none}"
}
build() {   # label [full]
    if [ "${2:-}" = full ]; then rm -f src/cpus/*.o; fi
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
    pline=$(awk -F'\t' -v n="$1" '$1 == n' $PM | head -n 1)
    verdict=none
    if [ -n "$pline" ]; then
        pset=$(echo "$pline" | cut -f3)
        if [ "$(norm "$red")" = "$(norm "$pset")" ]; then verdict=match; else verdict=MISS; fi
    fi
    echo "$1 [$N rows] ${r:-none} CONTROL=${ctl:-none} SYMPTOM=${sym:-none} ASAN=${asan:-none} $(tail -n 1 $OUT/probe_$1.out) RED=$red PRED=$verdict" >> $OUT/SCORES.txt
    if [ "$3" = 1 ] || [ "$verdict" = MISS ]; then rm -rf $OUT/sessions_$1; cp -r $sess $OUT/sessions_$1; fi
    echo "$1 ${r:-none} PRED=$verdict"
}
variant() {   # name keep-sessions
    if python3 $V apply $1 $FIX $S1 > $C/logs/apply_$1.err 2>&1; then
        f=$(build $1)
        if [ "$f" = fresh ]; then run $1 $C/gxemul $2; else echo "$1 [$N rows] BUILD-$f" >> $OUT/SCORES.txt; fi
    else
        cp $C/logs/apply_$1.err $OUT/apply_$1.err
        echo "$1 [$N rows] MUTANT-TEXT-NOT-FOUND" >> $OUT/SCORES.txt
    fi
}
: > $OUT/SCORES.txt
f=$(build base full); echo "base build: $f"
if [ "$f" != fresh ] || ! [ gxemul -nt $S1 ]; then echo "BASE BUILD NOT FRESH -- refusing"; exit 5; fi
ls -l --time-style=full-iso gxemul $S1 $O1 > $OUT/FRESHNESS.txt
run base $C/gxemul 1
cp $HEAD $S1
f=$(build HEAD)
if [ "$f" = fresh ]; then run HEAD $C/gxemul 1; else echo "HEAD [$N rows] BUILD-$f" >> $OUT/SCORES.txt; fi
cp $FIX $S1
run null_true /bin/true 1; run null_absent $C/no_such_gxemul 1; run null_false /bin/false 1
for v in B1_cnf_exit B2_def_exit B3_idx_read; do variant $v 1; done
VARS=$(cat $OUT/VARS_6.txt)
nv=$(echo $VARS | wc -w)
echo "variants: $nv (PRED_MAP lines: $(wc -l < $PM))"
for v in $VARS; do
    case "$EIGHT" in *" $v "*) variant $v 1 ;; *) variant $v 0 ;; esac
done
cp $FIX $S1
f=$(build restore); echo "restore build: $f"
if [ "$f" = fresh ] && cmp -s $S1 $SEC/$S1 && [ gxemul -nt $S1 ]; then
    rm -f .MUTANT; echo "clone restored to GXEMUL-SEC and rebuilt; sentinel cleared"
else
    echo "RESTORE NOT VERIFIED -- sentinel kept"
fi
{
    echo "lines in SCORES.txt: $(wc -l < $OUT/SCORES.txt) (8 legs + $nv variants)"
    echo "PRED=match:      $(grep -c 'PRED=match' $OUT/SCORES.txt)"
    echo "PRED=MISS:       $(grep -c 'PRED=MISS' $OUT/SCORES.txt)"
    echo "PRED=none:       $(grep -c 'PRED=none' $OUT/SCORES.txt)"
    echo "BUILD failures:  $(grep -c 'BUILD-' $OUT/SCORES.txt)"
    echo "text not found:  $(grep -c 'MUTANT-TEXT-NOT-FOUND' $OUT/SCORES.txt)"
    echo "variants scoring $N/$N (survivors; legs excluded): $(grep -vE '^(base|HEAD|null_true|null_absent|null_false|B1_cnf_exit|B2_def_exit|B3_idx_read) ' $OUT/SCORES.txt | grep -c " $N/$N ")"
    echo "MISS lines:"; grep 'PRED=MISS' $OUT/SCORES.txt | cut -d' ' -f1
} > $OUT/TALLY.txt
cat $OUT/TALLY.txt
md5sum $P $V $FIX $HEAD $R7/PRETABLE_6.out $PM $OUT/VARS_6.txt $R7/memc_pretable_6.py > $OUT/MD5.txt
echo "table 6 end $(date -u +%FT%TZ)"
echo TABLE6_MEMC_DONE
