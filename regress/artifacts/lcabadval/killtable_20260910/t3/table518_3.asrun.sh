#!/bin/bash
#  #518 TABLE 3 -- the main loop finishing the two walled Opus seats' tables on the 64-row instrument.
#  Runs in the seats' SCRATCH CLONES with their own mutators and FROZEN baselines; writes only under
#  /tmp and regress/artifacts/lcabadval/killtable_20260910/t3/.  No project tree is touched.
set -u
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
K=$SEC/regress/artifacts/lcabadval/killtable_20260910
T3=$K/t3
mkdir -p $T3
FROZEN=$T3/lca_badval_probe.REPAIRED64.asrun.py
cp $SEC/regress/lca_badval_probe.py $FROZEN
echo "=== TABLE 3 start $(date) ; instrument md5 $(md5sum $FROZEN | cut -c1-8), $(grep -c 'row(' $FROZEN) row( sites ==="
echo "=== BASELINE IDENTITY (frozen copies vs live SEC) ==="
if cmp -s $K/t2/BASELINE_t2.c $SEC/src/devices/dev_lca.c; then echo "t2/BASELINE_t2.c == SEC dev_lca.c"; else echo "*** t2/BASELINE_t2.c DIFFERS from SEC -- the seat's frozen baseline predates a fix change; STOP"; exit 7; fi
if cmp -s $K/BASELINE_FIX518c.c $SEC/src/devices/dev_lca.c; then echo "BASELINE_FIX518c.c == SEC dev_lca.c"; else echo "*** BASELINE_FIX518c.c DIFFERS from SEC -- STOP"; exit 7; fi

run_in () {   # clone label mutator-script mutant
    local C=$1 lbl=$2 MUT=$3 m=$4
    cd $C || return 1
    echo "$C/.MUTANT: src/devices/dev_lca.c  #518 TABLE 3 (main loop) $m in progress" > $C/.MUTANT
    python3 $MUT --restore > /dev/null 2>&1 || { echo "$lbl RESTORE_FAILED"; return 1; }
    if [ "$m" != "BASE" ]; then
        python3 $MUT "$m" > $T3/mutate_$lbl.log 2>&1 || { echo "$lbl MUTANT_DID_NOT_APPLY (rc=$?)"; cat $T3/mutate_$lbl.log | tail -3; return 1; }
    fi
    rm -f src/devices/dev_lca.o
    if ! make -j4 > $T3/build_$lbl.log 2>&1; then echo "$lbl BUILD_FAILED"; return 1; fi
    if [ ! gxemul -nt src/devices/dev_lca.c ]; then echo "$lbl STALE_BINARY"; return 1; fi
    python3 -u $FROZEN $C/gxemul $lbl > $T3/$lbl.raw 2>&1
    local r; r=$(grep -o 'LCABADVAL_RESULT=[0-9]*/[0-9]*' $T3/$lbl.raw | tail -1)
    local s; s=$(tail -1 $T3/$lbl.raw)
    local reds; reds=$(grep -E ' FAIL$' $T3/$lbl.raw | awk '{print $1" "$2}' | tr '\n' ',' | cut -c1-120)
    printf '%-26s %-8s sentinel=%-14s reds=%s\n' "$lbl" "${r#LCABADVAL_RESULT=}" "$s" "$reds" | tee -a $T3/SCORES3.txt
}

C2=/tmp/gxopus518b; M2=$K/t2/mutate518_t2.py
C1=/tmp/gxopus518;  M1=$K/mutate518.py
echo "=== clone t2 ($C2): BASE + M20 (equivalence check) + M25..M47 ===" | tee -a $T3/SCORES3.txt
run_in $C2 BASE $M2 BASE
for m in M20_def_echo M25_conf_widen M26_base_widen M27_mask_widen M28_field_idata M29_tbena_nostore M30_nolatch_mask1 M31_nolatch_defr M32_shared_conf_wen M33_shared_m0_defw M34_conf_dropbit0 M35_tbena_dropten M36_nolatch_defw M37_base0_nonzero M38_wen_base1_off M39_wen_base0_off M40_conf_ann_bit0 M41_mask_raw_store M42_def_allones M43_mask1_widen M44_mask1_field_idata M45_base1_nosg M46_conf_ann_wide M47_base1_widen; do
    run_in $C2 "$m" $M2 "$m"
done
echo "=== clone t1 ($C1): the table-1 seat's own mutants that swept the 58-row instrument ===" | tee -a $T3/SCORES3.txt
for m in M26_mask_field_wide M27_tbena_mask_wide M32_wen_ann_or M33_conf_ann_or M35_field_from_idata M37_conf_ann_eq; do
    run_in $C1 "t1_$m" $M1 "$m"
done
echo "=== RESTORE both clones from SEC ===" | tee -a $T3/SCORES3.txt
for C in $C2 $C1; do
    cp $SEC/src/devices/dev_lca.c $C/src/devices/dev_lca.c
    cd $C && rm -f src/devices/dev_lca.o && make -j4 > $T3/build_restore_$(basename $C).log 2>&1
    if cmp -s $C/src/devices/dev_lca.c $SEC/src/devices/dev_lca.c && [ $C/gxemul -nt $C/src/devices/dev_lca.c ]; then
        rm -f $C/.MUTANT; echo "$C: restored cmp-clean vs SEC, rebuilt fresh, sentinel cleared" | tee -a $T3/SCORES3.txt
    else
        echo "*** $C: RESTORE INCOMPLETE -- SENTINEL KEPT ***" | tee -a $T3/SCORES3.txt
    fi
done
echo "=== project trees untouched? ===" | tee -a $T3/SCORES3.txt
for t in /mnt/c/DocumentNoSnc/CC/GXEMUL/build /mnt/c/DocumentNoSnc/CC/GXEMUL/build-asan /tmp/gxsec-build; do
    echo "$t: part1=$(cmp -s $t/src/devices/dev_lca.c $SEC/src/devices/dev_lca.c && echo CLEAN || echo DIVERGENT) part2=$([ $t/gxemul -nt $t/src/devices/dev_lca.c ] && echo FRESH || echo STALE) sentinel=$(ls $t/.MUTANT 2>/dev/null | wc -l)" | tee -a $T3/SCORES3.txt
done
echo "TABLE518_3_DONE $(date)" | tee -a $T3/SCORES3.txt
