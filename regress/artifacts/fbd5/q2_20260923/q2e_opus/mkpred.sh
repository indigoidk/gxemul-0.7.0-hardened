#!/bin/bash
cd /mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2e/opus || exit 9
{
	echo "PREDICTIONS (q2e, the 862-row instrument 0263974b), written $(date '+%F %T %Z') BEFORE any of these variants was built."
	echo "Classes: RED (target = the row(s) it is aimed at); EQ; GREEN-DISC (real, named by the 862 contract's NOT COVERED);"
	echo "GREEN-REAL (real, NOT named -- a finding if measured so)."
	python3 gen_q2e.py pred
	echo PRED_DONE
} > PREDICTIONS_q2e.txt 2>&1
ls -la --time-style=full-iso PREDICTIONS_q2e.txt
head -1 PREDICTIONS_q2e.txt; sed -n 4p PREDICTIONS_q2e.txt
awk '$1 ~ /^(B_|IA|TD|PR|J0|W0)/ {print $4}' PREDICTIONS_q2e.txt | sort | uniq -c
