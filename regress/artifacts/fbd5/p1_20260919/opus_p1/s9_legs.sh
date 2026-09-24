#!/bin/bash
set -u
T=/tmp/gxopusfbd5
SECG=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
D=/mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/fbd5/opus_p1_20260919
cd "$T" || exit 9
echo "=== rebuild the FIXED clone for the legs run ==="
git -C "$SECG" show HEAD:src/devices/dev_footbridge.c > src/devices/dev_footbridge.c || exit 9
python3 out/frozen/mkfix3.py src/devices/dev_footbridge.c fix >/dev/null || exit 9
rm -f src/devices/dev_footbridge.o gxemul
make -j6 > out/table/legs_build.log 2>&1
[ -x gxemul ] && [ gxemul -nt src/devices/dev_footbridge.c ] || { echo "BUILD FAIL"; exit 9; }
echo "binary: $(stat -c %y gxemul)"
cp "$D/legs.py" out/frozen/legs.py
python3 -u out/frozen/legs.py ./gxemul out/arm_stub.bin
echo "S9_DONE"
