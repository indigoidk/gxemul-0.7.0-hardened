#!/bin/bash
#  run_boots.sh -- rung-4 boot comparison: ONE frozen instrument, both trees, quiet and -v.
D=/mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/opus_landiskaux_20260918
FROZEN=/tmp/boot_cmp.frozen.py
cp "$D/boot_cmp.py" "$FROZEN"
echo "INSTRUMENT $(md5sum < "$FROZEN" | cut -c1-12)"
for V in 0 1; do
  for T in base fix; do
    python3 -u "$FROZEN" "$T" "$V" "/tmp/lax_boot_${T}_v$V.log" > "$D/boot_${T}_v$V.out" 2>&1
    cat "$D/boot_${T}_v$V.out"
    echo
  done
done
echo RUN_BOOTS_DONE
