#!/bin/bash
set -u
H=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/o499/sib
C=/tmp/gx499
echo "SIBLING-PROBE INTERACTION -- do the two SHIPPED, GATE-WIRED probes change"
echo "score under #499's fix and under M4?  Frozen copies, run from $H."
echo "start $(date +%H:%M:%S)"
cd $H
for V in base fix m4_bitcollide; do
  echo "==================================================================="
  echo "###### sgi_re_width_probe.py (#497, gate_arm.sh:1131)  on  $V"
  python3 -u $H/sgi_re_width_probe.frozen.py $C/gxemul.$V $V 2>&1 | grep -E 'FAIL|OPUS497T_'
done
for V in base fix; do
  echo "==================================================================="
  echo "###### sgi_de_width_probe.py (#498, gate_arm.sh:1072)  on  $V"
  python3 -u $H/sgi_de_width_probe.frozen.py $C/gxemul.$V $V 2>&1 | grep -E 'FAIL|OPUS498T_'
done
echo "SIB_DONE $(date +%H:%M:%S)"
