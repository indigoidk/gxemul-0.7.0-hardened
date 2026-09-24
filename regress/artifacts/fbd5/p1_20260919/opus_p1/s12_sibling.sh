#!/bin/bash
set -u
T=/tmp/gxopusfbd5
D=/mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/fbd5/opus_p1_20260919
cd "$T" || exit 9
echo "=== on the RESTORED (HEAD) binary -- no source edit, no sentinel ==="
cat .MUTANT 2>/dev/null || echo "  .MUTANT absent (clean)"
md5sum gxemul
cp "$D/opus_w.py" out/frozen/opus_w4.py
python3 -u out/frozen/opus_w4.py ./gxemul out/arm_stub.bin sibling
echo "S12_DONE"
