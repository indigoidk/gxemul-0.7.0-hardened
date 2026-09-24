#!/bin/bash
cd /mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2f/opus || exit 9
{
	echo "PREDICTIONS (q2f, the 864-row instrument 8309c5b7), written $(date '+%F %T %Z') BEFORE any of these variants was built."
	echo "Classes: RED (target = the row(s) it is aimed at); EQ; GREEN-DISC (real, named by the 864 contract's NOT COVERED);"
	echo "GREEN-REAL (real, NOT named -- a finding if measured so)."
	python3 gen_q2f.py pred
	echo PRED_DONE
} > PREDICTIONS_q2f.txt 2>&1
ls -la --time-style=full-iso PREDICTIONS_q2f.txt
head -1 PREDICTIONS_q2f.txt; sed -n 4p PREDICTIONS_q2f.txt
awk '$1 ~ /^(P_|FS|MC|TX)/ {print $4}' PREDICTIONS_q2f.txt | sort | uniq -c
