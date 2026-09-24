#!/bin/bash
# two-part clearance for #545's one product file across the four trees (read-only)
R=/mnt/c/DocumentNoSnc/CC/GXEMUL; F=src/devices/dev_footbridge.c
echo "clearance $(date '+%F %T')  SEC md5 $(md5sum $R/GXEMUL-SEC/$F | cut -c1-8)"
for t in build build-asan; do
  s=$R/$t/$F; b=$R/$t/gxemul
  p1=$(cmp -s $s $R/GXEMUL-SEC/$F && echo CLEAN || echo DIFFERS)
  p2=$([ $b -nt $s ] && echo FRESH || echo STALE); echo "  $t: part1 $p1  part2 $p2 (binary $(stat -c %y $b 2>/dev/null | cut -c1-19), source $(stat -c %y $s | cut -c1-19))"
done
s=/tmp/gxsec-build/$F; b=/tmp/gxsec-build/gxemul
p1=$(cmp -s $s $R/GXEMUL-SEC/$F && echo CLEAN || echo DIFFERS); p2=$([ $b -nt $s ] && echo FRESH || echo STALE)
echo "  /tmp/gxsec-build: part1 $p1  part2 $p2 (binary $(stat -c %y $b 2>/dev/null | cut -c1-19), source $(stat -c %y $s 2>/dev/null | cut -c1-19))"
echo "  est: part1 $(cmp -s $R/est/$F $R/GXEMUL-SEC/$F && echo CLEAN || echo DIFFERS)  part2 N/A (source tree, no binary)"
