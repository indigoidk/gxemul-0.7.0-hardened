#!/bin/bash
cd /tmp/gxopus539p1 || exit 9
echo "=== binary vs EVERY restored source (part 2 of the two-part clearance) ==="
for f in src/cpus/cpu_alpha_palcode.c src/devices/dev_lca.c src/devices/dev_pcc2.c \
         src/devices/dev_sgi_ip32.c src/devices/dev_sh4.c src/devices/dev_footbridge.c; do
  if [ gxemul -nt "$f" ]; then R=FRESH; else R="*** STALE ***"; fi
  printf '  %-40s %s   (src %s)\n' "$f" "$R" "$(stat -c %y "$f" | cut -c1-19)"
done
echo "binary: $(stat -c %y gxemul | cut -c1-19)  size $(stat -c %s gxemul)"
echo "=== md5 vs the project build/ binary (expect DIFFERENT: I reverted 6 files) ==="
md5sum gxemul /mnt/c/DocumentNoSnc/CC/GXEMUL/build/gxemul
echo "=== version banner ==="
./gxemul -V 2>&1 | head -3
