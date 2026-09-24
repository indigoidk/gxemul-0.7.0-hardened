#!/bin/bash
cd /mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2g/opus || exit 9
{ echo "ADDENDUM PREDICTIONS (q2g), written $(date '+%F %T %Z') BEFORE these two were built.  On the 864 rows: GREEN."
  echo "On the 872-row scratch extension (diff_ext.c 0f99ca50): GREEN as well -- W5 sets running, byte_order, is_32bit,"
  echo "ninstrs, mem, ncpus and the machine type, but NOT pc or cpsr."
  python3 gen_r3d_opus_b.py pred; echo PRED_B_DONE; } > PREDICTIONS_q2g_b.txt 2>&1
ls -la --time-style=full-iso PREDICTIONS_q2g_b.txt; cat PREDICTIONS_q2g_b.txt
