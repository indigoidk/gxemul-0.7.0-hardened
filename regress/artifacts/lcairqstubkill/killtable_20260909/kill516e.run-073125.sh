#!/bin/sh
#  #516 TABLE E -- the ADDENDUM the pass-2 panel bought.
#
#  minimax named a mutant nobody had built: "swap ASSERT_BIT <-> DEASSERT_BIT in the *assert*
#  if-guard only -- the assignment unchanged".  That is the MIRROR of M4_sharedlatch, which swapped
#  guard AND assignment on the DEASSERT side.  It sits inside the clause-(d) DEPENDS-ON enumeration
#  (an operand swap drawn from a field the guarded body reads), so if it sweeps the table it is a
#  FLOOR BREACH and L2 -- fix in-round, however late.
#
#  M13 is its own mirror, added because building one half of a symmetric pair and not the other is
#  exactly the #499 shape this project keeps paying for.
set -u
S=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
C=/tmp/gxopus516
OUT=/tmp/kill516e
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad
FROZEN=$OUT/frozen_lca_irqstub_probe.py
MUT=$OUT/frozen_mut516e.py

mkdir -p $OUT
cp $S/regress/lca_irqstub_probe.py $FROZEN
cp $SP/mut516d.py                  $MUT
cp $S/src/devices/dev_lca.c        $OUT/dev_lca.c.FIXED

echo "=== BASELINE: GXEMUL-SEC working tree ==="
if cmp -s $C/src/devices/dev_lca.c $OUT/dev_lca.c.FIXED; then
    echo "  clone dev_lca.c cmp CLEAN against baseline before mutant 1"
else
    echo "  clone DIVERGED -- restoring from SEC first"
    cp $OUT/dev_lca.c.FIXED $C/src/devices/dev_lca.c
fi
echo "$C/.MUTANT: src/devices/dev_lca.c  #516 TABLE E in progress" > $C/.MUTANT

run () {
    lbl=$1
    cd $C || return
    rm -f src/devices/dev_lca.o
    if ! make -j4 > $OUT/build_$lbl.log 2>&1; then echo "$lbl BUILD_FAILED"; return; fi
    if [ ! gxemul -nt src/devices/dev_lca.c ]; then echo "$lbl STALE_BINARY"; return; fi
    python3 -u $FROZEN $C/gxemul $lbl > $OUT/probe_$lbl.raw 2>&1
    r=$(grep -o 'LCAIRQ_RESULT=[0-9]*/[0-9]*' $OUT/probe_$lbl.raw | tail -1)
    #  the LOAD-BEARING counts, read from the rows the probe itself computes (not from a grep over
    #  the raw -- table D shipped a column that could not fail because it grepped the wrong text)
    ao=$(grep -E '^assert once'   $OUT/probe_$lbl.raw | awk '{print $3}')
    do_=$(grep -E '^deassert once' $OUT/probe_$lbl.raw | awk '{print $3}')
    t=$(tail -1 $OUT/probe_$lbl.raw)
    printf '%-24s %-8s assert_once=%-6s deassert_once=%-6s sentinel=%s\n' \
        "$lbl" "${r#LCAIRQ_RESULT=}" "$ao" "$do_" "$t"
}

echo ""
echo "=== #516 TABLE E -- the panel's guard-swap mirrors, shipped 11-row instrument ==="
echo ""
cp $OUT/dev_lca.c.FIXED $C/src/devices/dev_lca.c
run base

for m in M12_assertguard_swap M13_deassertguard_swap ; do
    cp $OUT/dev_lca.c.FIXED $C/src/devices/dev_lca.c
    python3 $MUT $C/src/devices/dev_lca.c "$m" || echo "  *** MUTANT $m FAILED TO APPLY ***"
    run $m
done

cp $S/src/devices/dev_lca.c $C/src/devices/dev_lca.c
cd $C || exit 1
echo ""
if cmp -s src/devices/dev_lca.c $S/src/devices/dev_lca.c; then
    rm -f src/devices/dev_lca.o
    if make -j4 > $OUT/build_restore.log 2>&1 && [ gxemul -nt src/devices/dev_lca.c ]; then
        rm -f $C/.MUTANT
        echo "RESTORE: source cmp-clean vs SEC AND binary rebuilt fresh -- sentinel cleared"
    else
        echo "*** RESTORE REBUILD FAILED -- SENTINEL KEPT ***"
    fi
else
    echo "*** RESTORE cmp FAILED -- SENTINEL KEPT ***"
fi
echo "KILL516E_DONE"
