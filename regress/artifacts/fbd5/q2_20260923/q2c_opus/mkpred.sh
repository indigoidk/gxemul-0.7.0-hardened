#!/bin/bash
cd /mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2c/opus || exit 9
{
	echo "PREDICTIONS for the new one-line shapes, written $(date '+%F %T %Z') BEFORE any variant was built or run."
	echo "Classes: RED; EQ (green, equivalent); GREEN-DISC (green, real, named by NOT COVERED); GREEN-REAL (green, real,"
	echo "NOT named -- a finding if measured so); GREEN-MACH (green, equivalent only because nothing drives the bit)."
	python3 gen_variants.py pred
	echo PRED_DONE
} > PREDICTIONS_q2c.txt 2>&1
ls -la --time-style=full-iso PREDICTIONS_q2c.txt
head -1 PREDICTIONS_q2c.txt
