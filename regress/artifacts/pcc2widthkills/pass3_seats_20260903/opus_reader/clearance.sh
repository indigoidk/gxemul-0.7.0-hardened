#!/bin/bash
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
T=/tmp/gxsec-build
F=src/devices/dev_pcc2.c
if [ -d "$T" ]; then
  if cmp -s "$T/$F" "$SEC/$F"; then P1=CLEAN; else P1=DIVERGENT; fi
  if [ -f "$T/gxemul" ]; then
    if [ "$T/gxemul" -nt "$T/$F" ]; then P2=FRESH; else P2="*** STALE ***"; fi
  else P2="no binary"; fi
  echo "gxsec-build/$F  part1=$P1  part2=$P2"
  ls -la --time-style=+%m-%d_%H:%M:%S "$T/gxemul" "$T/$F" 2>/dev/null | awk '{print "   ", $6, $7}'
else
  echo "gxsec-build ABSENT"
fi
