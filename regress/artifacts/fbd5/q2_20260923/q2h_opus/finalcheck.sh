#!/bin/bash
FZ=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2h/frozen/dev_footbridge.c
for d in /tmp/opusr3e /tmp/opusr3e_w0 /tmp/opusr3e_w1 /tmp/opusr3e_w2 /tmp/opusr3e_w3 /tmp/opusr3e_w4 /tmp/opusr3e_w5 /tmp/opusr3e_add /tmp/opusr3e_bs; do
  [ -d "$d" ] || continue
  if [ -e "$d/.MUTANT" ]; then echo "SENTINEL PRESENT: $d"
  elif cmp -s "$d/src/devices/dev_footbridge.c" "$FZ"; then echo "clean (device==frozen): $d"
  else echo "DEVICE DIFFERS: $d"; fi
done
echo FINALCHECK_DONE
