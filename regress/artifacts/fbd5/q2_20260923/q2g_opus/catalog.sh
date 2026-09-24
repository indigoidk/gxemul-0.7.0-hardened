#!/bin/bash
# Catalogue the main loop's 739 r3d variants: one diff -U0 per variant against FIX.c (the SEC device).
V=/tmp/fbd5r3d_var
O=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2g/opus
cmp $V/FIX.c /mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2g/frozen/dev_footbridge.c && echo "FIX.c == frozen device"
: > $O/existing_edits.txt
n=0
for f in $V/*.c; do
  b=$(basename $f .c)
  [ "$b" = FIX ] && continue
  n=$((n+1))
  echo "=== $b" >> $O/existing_edits.txt
  diff -U0 $V/FIX.c $f | grep -E '^[-+][^-+]|^[-+]$' >> $O/existing_edits.txt
done
echo "variants catalogued: $n"
grep -c '^===' $O/existing_edits.txt
