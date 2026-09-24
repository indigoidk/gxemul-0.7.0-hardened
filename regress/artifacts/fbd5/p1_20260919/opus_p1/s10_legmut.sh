#!/bin/bash
set -u
T=/tmp/gxopusfbd5
SECG=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
D=/mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/fbd5/opus_p1_20260919
cd "$T" || exit 9
echo "=== build a PRE-FIX (HEAD) binary and keep it aside ==="
git -C "$SECG" show HEAD:src/devices/dev_footbridge.c > src/devices/dev_footbridge.c || exit 9
cmp -s out/fb_head.c src/devices/dev_footbridge.c && echo "  source at HEAD" || exit 9
rm -f src/devices/dev_footbridge.o gxemul
make -j6 > out/table/head_build.log 2>&1
[ -x gxemul ] && [ gxemul -nt src/devices/dev_footbridge.c ] || { echo "BUILD FAIL"; exit 9; }
cp gxemul out/gxemul_HEAD
echo "  out/gxemul_HEAD: $(md5sum out/gxemul_HEAD)"
echo "=== rebuild the FIXED binary ==="
python3 out/frozen/mkfix3.py src/devices/dev_footbridge.c fix >/dev/null || exit 9
rm -f src/devices/dev_footbridge.o gxemul
make -j6 > out/table/fix_build2.log 2>&1
[ -x gxemul ] && [ gxemul -nt src/devices/dev_footbridge.c ] || { echo "BUILD FAIL"; exit 9; }
cp "$D/legmut.py" out/frozen/legmut.py
python3 -u out/frozen/legmut.py ./gxemul ./out/gxemul_HEAD out/arm_stub.bin
echo "S10_DONE"
