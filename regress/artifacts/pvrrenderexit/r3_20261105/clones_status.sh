#!/bin/bash
# clones_status.sh -- read-only: for each repair-3 scratch clone, sentinel present?, dev_pvr.c cmp vs GXEMUL-SEC, binary fresh?
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/src/devices/dev_pvr.c
for d in /tmp/gxpvr3 /tmp/gxpvr3b /tmp/gxpvr3c /tmp/gxpvr3d /tmp/gxpvr3e /tmp/gxpvr4; do
  if [ ! -e "$d" ]; then echo "$d absent"; continue; fi
  s=clean; [ -e "$d/.MUTANT" ] && s=SENTINEL
  c=DIVERGENT; cmp -s "$d/src/devices/dev_pvr.c" "$SEC" && c=CMP_CLEAN
  f=STALE; [ "$d/gxemul" -nt "$d/src/devices/dev_pvr.c" ] && f=BIN_FRESH
  echo "$d $s $c $f"
done
