#!/bin/sh
#  #516 kill table D -- the SHIPPED 11-row instrument, re-measured after the main loop changed
#  `kbc attrib' following the measuring seat's caution.  The seat measured probe5; what ships is
#  probe5 PLUS that widening, so the seat's table no longer describes the deliverable.  A changed
#  instrument owes its own table: that is the whole reason this run exists.
#
#  Runs ENTIRELY in the scratch clone /tmp/gxopus516.  Touches no project tree.
set -u
S=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
C=/tmp/gxopus516
OUT=/tmp/kill516g
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad
FROZEN=$OUT/frozen_lca_irqstub_probe.py
MUT=$OUT/frozen_mut516d.py

mkdir -p $OUT

#  *** FREEZE BOTH THE INSTRUMENT AND THE MUTATOR. ***  A multi-run driver re-reads its python
#  between runs (the interpreter loads the whole file at startup, so run N+1 gets whatever the
#  file says THEN) -- so an edit mid-table lands inside the very comparison being made.
cp $S/regress/lca_irqstub_probe.py $FROZEN
cp $SP/mut516d.py                  $MUT

#  ---- NAME THE BASELINE, and cmp before mutant 1.  A clone inherits whatever it last held. ----
BASE=$S/src/devices/dev_lca.c
cp $BASE $OUT/dev_lca.c.FIXED
echo "=== BASELINE: GXEMUL-SEC working tree (the round's post-fix set) ==="
if cmp -s $C/src/devices/dev_lca.c $BASE; then
    echo "  clone dev_lca.c cmp CLEAN against the baseline before mutant 1"
else
    echo "  clone DIVERGED from baseline -- restoring from SEC before starting"
    cp $BASE $C/src/devices/dev_lca.c
fi

echo "$C/.MUTANT: src/devices/dev_lca.c  #516 KILL TABLE G in progress" > $C/.MUTANT

run () {
    lbl=$1
    cd $C || return
    rm -f src/devices/dev_lca.o
    if ! make -j4 > $OUT/build_$lbl.log 2>&1; then
        echo "$lbl BUILD_FAILED"; return
    fi
    #  MAKE_RC has been observed reporting 0 on a failed build, so freshness is checked, not
    #  assumed.  A stale binary is the trap this project has paid for twice.
    if [ ! gxemul -nt src/devices/dev_lca.c ]; then
        echo "$lbl STALE_BINARY"; return
    fi
    python3 -u $FROZEN $C/gxemul $lbl > $OUT/probe_$lbl.raw 2>&1
    r=$(grep -o 'LCAIRQ_RESULT=[0-9]*/[0-9]*' $OUT/probe_$lbl.raw | tail -1)
    a=$(grep -c 'ISA interrupt assert not implemented'   $OUT/probe_$lbl.raw)
    d=$(grep -c 'ISA interrupt deassert not implemented' $OUT/probe_$lbl.raw)
    t=$(tail -1 $OUT/probe_$lbl.raw)
    printf '%-22s %-10s ann_a=%s ann_d=%s  sentinel=%s\n' \
        "$lbl" "${r#LCAIRQ_RESULT=}" "$a" "$d" "$t"
}

mutate () {
    cp $OUT/dev_lca.c.FIXED $C/src/devices/dev_lca.c
    python3 $MUT $C/src/devices/dev_lca.c "$1" || echo "  *** MUTANT $1 FAILED TO APPLY ***"
}

echo ""
echo "=== #516 KILL TABLE G -- shipped 12-row instrument ==="
echo ""

cp $OUT/dev_lca.c.FIXED $C/src/devices/dev_lca.c
run base

for m in M2_both M2d_deassert M2a_assert M3_deassertoff M3a_assertoff M4_sharedlatch \
         M5_assertdishonest M6_deassertdishonest M7_deassert_assign M8_assert_assign \
         M9_deassert_nolatch M10_assert_nolatch M12_assertguard_swap M13_deassertguard_swap \
         M_nonull M11_null ; do
    mutate $m
    run $m
done

#  ---- RESTORE, verified against SEC (never against this script's own backup) -------------------
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
echo "KILL516G_DONE"
