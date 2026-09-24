#!/bin/bash
cd /mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2c/opus || exit 9
{
	echo "PREDICTIONS for the SECOND table (N_SB drive-test bit masks, N_X attribution probes), written $(date '+%F %T %Z')"
	echo "BEFORE any of these variants was built or run.  Same classes as PREDICTIONS_q2c.txt.  N_X1: held by X10W only;"
	echo "N_X2: held by X6W only; N_X3: held by X7W only."
	python3 gen_variants.py pred | grep -E '^(variants|N_SB|N_X)'
	echo PRED2_DONE
} > PREDICTIONS_q2c_table2.txt 2>&1
ls -la --time-style=full-iso PREDICTIONS_q2c_table2.txt
head -4 PREDICTIONS_q2c_table2.txt
awk '/^N_/{print $4}' PREDICTIONS_q2c_table2.txt | sort | uniq -c
