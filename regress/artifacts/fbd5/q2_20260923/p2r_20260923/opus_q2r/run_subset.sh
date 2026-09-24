#!/bin/bash
# Control subset: the brief's Q1..Q5 (must each go red on X9 all-zero rows: 3,3,3,3,2) plus two predicted greens.
cd /tmp/opusq2r || exit 9
python3 -u /mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2r/opus/driver.py \
  a_pos_A0_irq_enable a_pos_A1_irq_status a_pos_A3_fiq_enable a_pos_A4_fiq_status a_pos_A2_irq_enable \
  b_neg_A1_L1o fl_neg_A0_L1l c_dir_A2_len4 2>&1
ls -la /tmp/opusq2r/.MUTANT 2>&1
