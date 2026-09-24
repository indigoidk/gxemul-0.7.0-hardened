#!/bin/bash
# Write the PREDICTIONS for gen_r3d_opus.py's variants BEFORE any of them is built (its mtime is the order proof).
cd /mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2g/opus || exit 9
{
	echo "PREDICTIONS (q2g, the 864-row 3d instrument 6c92d7e5 on the frozen device 783c0c7f), written $(date '+%F %T %Z') BEFORE any of these variants was built."
	echo "Classes: RED (target = the row(s) it is aimed at; CONTROLS); EQ (equivalent); GREEN-DISC (real, named by the 3d contract's NOT COVERED);"
	echo "GREEN-REAL (real, NOT named there -- a finding if measured so)."
	python3 gen_r3d_opus.py pred
	echo PRED_DONE
} > PREDICTIONS_q2g.txt 2>&1
ls -la --time-style=full-iso PREDICTIONS_q2g.txt
sed -n 4p PREDICTIONS_q2g.txt
awk 'NR>4 && $1 !~ /^PRED_DONE/ {print $4}' PREDICTIONS_q2g.txt | sort | uniq -c
