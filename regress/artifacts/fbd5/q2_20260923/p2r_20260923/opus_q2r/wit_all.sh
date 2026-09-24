#!/bin/bash
# Differential on every GREEN variant of results.tsv, plus the two controls (BASE must show nothing;
# a_pos_A0_irq_enable = the brief's Q1 must show an announce divergence).
O=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2r/opus
GREENS=$(awk -F'\t' 'NR > 1 && $5 == "ok" && $7 == "0" { print $1 }' "$O/results.tsv")
echo "greens: $(echo $GREENS | wc -w)" > "$O/wit_all.out"
MAXL=3 NRAND=2000000 bash "$O/wit_run.sh" BASE a_pos_A0_irq_enable $GREENS >> "$O/wit_all.out" 2>&1
echo "WIT_ALL_DONE rc=$?" >> "$O/wit_all.out"
