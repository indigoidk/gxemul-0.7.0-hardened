#!/bin/bash
set -u
T=/tmp/gxopusfbd5
D=/mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/fbd5/opus_p1_20260919
cd "$T" || exit 9
echo "=== binary: $(stat -c '%y' gxemul) ==="
for s in witness accept decline; do
  echo ""
  echo "########## SET=$s ##########"
  python3 -u "$D/opus_w.py" ./gxemul out/arm_stub.bin "$s"
done
echo ""
echo "########## SHIPPED SITES PROBE, unchanged ##########"
python3 -u /mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/footbridge_sites_probe.py ./gxemul out/arm_stub.bin
echo "S5_DONE"
