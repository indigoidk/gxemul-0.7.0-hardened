#!/bin/bash
#  #518 TABLE 4 -- the final 67-row instrument against the cells rounds 3/4 added: t2's M43..M47 (mask1
#  widen / field-from-idata, base1 nosg / widen, conf ann wide) via the seat's mutator, plus M48_wen_perreg
#  and M49_def_narrow via mut518x.py.  Runs AFTER table 3 has restored /tmp/gxopus518b.  The baseline is
#  the CURRENT SEC dev_lca.c (round 4 changed comments only); t2's frozen BASELINE_t2.c differs from it by
#  those comments, so this table restores from SEC (not from the seat's frozen copy) and says so.
set -u
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
K=$SEC/regress/artifacts/lcabadval/killtable_20260910
T4=$K/t4
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad
C=/tmp/gxopus518b
mkdir -p $T4
FROZEN=$T4/lca_badval_probe.REPAIRED67.asrun.py
cp $SEC/regress/lca_badval_probe.py $FROZEN
cp $SEC/src/devices/dev_lca.c $T4/BASELINE_round4.c
cp $SP/mut518x.py $T4/mut518x.py
echo "=== TABLE 4 start $(date); instrument md5 $(md5sum $FROZEN | cut -c1-8), $(grep -c 'row(' $FROZEN) row( sites; baseline = SEC round-4 dev_lca.c md5 $(md5sum $T4/BASELINE_round4.c | cut -c1-8) ===" | tee $T4/SCORES4.txt
if [ -f $C/.MUTANT ]; then echo "*** $C still carries a sentinel (table 3 not finished?) -- STOP" | tee -a $T4/SCORES4.txt; exit 7; fi
echo "baseline vs t2 frozen copy: $(cmp -s $T4/BASELINE_round4.c $K/t2/BASELINE_t2.c && echo IDENTICAL || echo 'DIFFERS (comment-only round-4 edits; diff below)')" | tee -a $T4/SCORES4.txt
diff $K/t2/BASELINE_t2.c $T4/BASELINE_round4.c | grep -cE '^[<>]' | sed 's/^/  changed lines: /' | tee -a $T4/SCORES4.txt
echo "$C/.MUTANT: src/devices/dev_lca.c  #518 TABLE 4 (main loop) in progress" > $C/.MUTANT
run () {   # label mutator mutant
    local lbl=$1 MUT=$2 m=$3
    cd $C || return 1
    cp $T4/BASELINE_round4.c src/devices/dev_lca.c
    if [ "$m" != "BASE" ]; then
        if [ "$MUT" = "t2" ]; then
            python3 $K/t2/mutate518_t2.py "$m" > $T4/mutate_$lbl.log 2>&1 || { echo "$lbl MUTANT_DID_NOT_APPLY (rc=$?)" | tee -a $T4/SCORES4.txt; tail -2 $T4/mutate_$lbl.log; return 1; }
        else
            python3 $T4/mut518x.py src/devices/dev_lca.c "$m" > $T4/mutate_$lbl.log 2>&1 || { echo "$lbl MUTANT_DID_NOT_APPLY (rc=$?)" | tee -a $T4/SCORES4.txt; tail -2 $T4/mutate_$lbl.log; return 1; }
        fi
    fi
    rm -f src/devices/dev_lca.o
    if ! make -j4 > $T4/build_$lbl.log 2>&1; then echo "$lbl BUILD_FAILED" | tee -a $T4/SCORES4.txt; return 1; fi
    if [ ! gxemul -nt src/devices/dev_lca.c ]; then echo "$lbl STALE_BINARY" | tee -a $T4/SCORES4.txt; return 1; fi
    python3 -u $FROZEN $C/gxemul $lbl > $T4/$lbl.raw 2>&1
    local r; r=$(grep -o 'LCABADVAL_RESULT=[0-9]*/[0-9]*' $T4/$lbl.raw | tail -1)
    local reds; reds=$(grep -E ' FAIL$' $T4/$lbl.raw | awk '{print $1" "$2}' | tr '\n' ',' | cut -c1-120)
    printf '%-24s %-8s sentinel=%-14s reds=%s\n' "$lbl" "${r#LCABADVAL_RESULT=}" "$(tail -1 $T4/$lbl.raw)" "$reds" | tee -a $T4/SCORES4.txt
}
run BASE none BASE
for m in M43_mask1_widen M44_mask1_field_idata M45_base1_nosg M46_conf_ann_wide M47_base1_widen; do run "$m" t2 "$m"; done
for m in M48_wen_perreg M49_def_narrow; do run "$m" x "$m"; done
echo "=== RESTORE from SEC ===" | tee -a $T4/SCORES4.txt
cp $SEC/src/devices/dev_lca.c $C/src/devices/dev_lca.c; cd $C && rm -f src/devices/dev_lca.o && make -j4 > $T4/build_restore.log 2>&1
if cmp -s $C/src/devices/dev_lca.c $SEC/src/devices/dev_lca.c && [ $C/gxemul -nt $C/src/devices/dev_lca.c ]; then rm -f $C/.MUTANT; echo "$C restored cmp-clean vs SEC, rebuilt fresh, sentinel cleared" | tee -a $T4/SCORES4.txt; else echo "*** RESTORE INCOMPLETE -- SENTINEL KEPT ***" | tee -a $T4/SCORES4.txt; fi
echo "TABLE518_4_DONE $(date)" | tee -a $T4/SCORES4.txt
