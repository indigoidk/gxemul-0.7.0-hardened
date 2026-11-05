#!/bin/bash
# table9_qhs.sh <a|b> -- qhslowifetch TEST-VARIANT TABLE 9 (repair 8: 137 rows, 69 variants), derived from table8_qhs.sh.
# ONE instrument at the final row count (table9/probe137_frozen.py, cmp-identical to base137/probe137_run.py, 137/137 on build/),
# every SCORES line naming it.  Legs first, in the same clone: base (the fix), the HEAD leg (det_20261104's cpu_ppc_instr.c.HEAD +
# cpu_ppc.h.HEAD), three null media; then the variants of qhs_variants_9.py (run with python3 -B, so no bytecode cache lands in the
# earlier tables' directories).  PRETABLE_9.out must exist first (its mtime precedes every output here).  Two phases, because one
# pass is ~500 s against the Bash tool's 600 s cap:
#   a  fresh clone + sentinel + both sources cmp'd = baseline; legs; variants 1-35; the clone's source put back to the baseline,
#      the sentinel KEPT (its binary is the last variant's)
#   b  refuses unless the clone still carries the sentinel and the baseline source; variants 36-69; restore, cmp against
#      GXEMUL-SEC, rebuild, and only then clear the sentinel
# Mutates ONLY /tmp/gxqhs15 (a cp -a of build/).
set -u
G=/mnt/c/DocumentNoSnc/cc/GXEMUL
C=/tmp/gxqhs15
IN=$G/GXEMUL-SEC/regress/artifacts/qhslowifetch/det_20261104
R7=$G/GXEMUL-SEC/regress/artifacts/qhslowifetch/r7_20261105
OUT=$R7/table9
P=$OUT/probe137_frozen.py
N=137
V=$R7/qhs_variants_9.py
FIX=$R7/cpu_ppc_instr.c.fix7
S1=src/cpus/cpu_ppc_instr.c
S2=src/include/cpu_ppc.h
PH=${1:-none}
[ -f $R7/PRETABLE_9.out ] || { echo "NO PRETABLE_9.out -- refusing"; exit 2; }
[ -f $P ] || { echo "NO frozen probe $P -- refusing"; exit 2; }
cmp -s $P $R7/base137/probe137_run.py || { echo "frozen probe != base-run copy -- refusing"; exit 2; }
build() {
    rm -f src/cpus/cpu_ppc*.o
    make -j4 > $OUT/build_$1.log 2>&1
    rc=$?
    if [ $rc = 0 ] && [ src/cpus/cpu_ppc.o -nt $S1 ] && [ gxemul -nt src/cpus/cpu_ppc.o ]; then echo fresh; else echo "STALE_rc$rc"; fi
}
run() {   # label binary
    python3 -B -u $P $2 $1 $OUT/sessions_$1 > $OUT/probe_$1.out 2>&1
    r=$(grep '^PPC_IFETCH_RESULT=' $OUT/probe_$1.out | cut -d= -f2)
    c=$(grep '^PPC_IFETCH_CONTROL=' $OUT/probe_$1.out | cut -d= -f2)
    y=$(grep '^PPC_IFETCH_SYMPTOM=' $OUT/probe_$1.out | cut -d= -f2)
    red=$(grep '^PPC_IFETCH_RED=' $OUT/probe_$1.out | cut -d= -f2)
    echo "$1 [$N rows] ${r:-none} CONTROL=${c:-none} SYMPTOM=${y:-none} $(tail -n 1 $OUT/probe_$1.out) RED=${red:-none}" >> $OUT/SCORES.txt
    echo "$1 ${r:-none}"
}
variants() {   # first last (1-based, inclusive)
    for v in $(python3 -B $V list | tr ' ' '\n' | sed -n "$1,$2p"); do
        if python3 -B $V apply $v $FIX $S1 > $OUT/apply_$v.err 2>&1; then
            f=$(build $v)
            if [ "$f" = fresh ]; then run $v $C/gxemul; else echo "$v [$N rows] BUILD-$f" >> $OUT/SCORES.txt; echo "$v BUILD-$f"; fi
        else
            echo "$v [$N rows] MUTANT-TEXT-NOT-FOUND" >> $OUT/SCORES.txt; echo "$v MUTANT-TEXT-NOT-FOUND"
        fi
    done
}
NV=$(python3 -B $V list | wc -w)
case $PH in
a)
    [ -e $OUT/SCORES.txt ] && { echo "SCORES.txt exists -- phase a already ran; refusing to overwrite"; exit 2; }
    rm -rf $C && cp -a $G/build $C || { echo "CLONE FAILED"; exit 3; }
    cd $C || exit 3
    echo "$S1: qhslowifetch table 9; baseline $FIX" > .MUTANT
    cmp -s $S1 $FIX && cmp -s $S2 $IN/cpu_ppc.h.fix || { echo "clone source = baseline: NO"; exit 4; }
    echo "clone source = baseline (fix7, cpu_ppc.h.fix): yes; $NV variants listed"
    : > $OUT/SCORES.txt
    f=$(build base); echo "base build: $f"
    [ "$f" = fresh ] || { echo "BASE BUILD NOT FRESH -- stopping; sentinel kept"; exit 5; }
    run base $C/gxemul
    cp $IN/cpu_ppc_instr.c.HEAD $S1; cp $IN/cpu_ppc.h.HEAD $S2
    echo "HEAD build: $(build HEAD)"; run HEAD $C/gxemul
    cp $IN/cpu_ppc.h.fix $S2
    run null_true /bin/true; run null_absent /nonexistent/gxemul; run null_false /bin/false
    variants 1 35
    cp $FIX $S1
    echo "phase a done: clone source put back to the baseline; its binary is the last variant's; sentinel KEPT"
    echo TABLE9_PHASE_A_DONE
    ;;
b)
    cd $C || { echo "no clone $C"; exit 3; }
    [ -f .MUTANT ] || { echo "no sentinel in $C -- phase a did not leave this clone; refusing"; exit 4; }
    cmp -s $S1 $FIX && cmp -s $S2 $IN/cpu_ppc.h.fix || { echo "clone source = baseline: NO"; exit 4; }
    variants 36 $NV
    cp $FIX $S1
    echo "restore build: $(build restore)"
    if cmp -s $S1 $G/GXEMUL-SEC/$S1 && cmp -s $S2 $G/GXEMUL-SEC/$S2 && [ gxemul -nt $S1 ] && [ gxemul -nt src/cpus/cpu_ppc.o ]; then
        rm -f .MUTANT; echo "clone restored to GXEMUL-SEC and rebuilt; sentinel cleared"
    else
        echo "RESTORE NOT VERIFIED -- sentinel kept"
    fi
    md5sum $P $V $FIX $IN/cpu_ppc.h.fix $IN/cpu_ppc_instr.c.HEAD $IN/cpu_ppc.h.HEAD $R7/PRETABLE_9.out $R7/b123_variant.py \
        $R7/g12_variant.py $R7/b7b_variant.py $R7/b8_variant.py > $OUT/MD5.txt
    echo TABLE9_QHS_DONE
    ;;
*)
    echo "usage: table9_qhs.sh a|b"; exit 2
    ;;
esac
