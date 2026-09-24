#!/bin/bash
set -u
T=/tmp/gxopusfbd5
SECG=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
D=/mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/fbd5/opus_p1_20260919
cd "$T" || exit 9
cp "$D/opus_w.py" out/frozen/opus_w3.py
cp "$D/mkfix.py"  out/frozen/mkfix3.py
for V in fix m_sharebit m_onebit; do
  echo ""
  echo "########## $V"
  git -C "$SECG" show HEAD:src/devices/dev_footbridge.c > src/devices/dev_footbridge.c || exit 9
  python3 out/frozen/mkfix3.py src/devices/dev_footbridge.c "$V" >/dev/null || exit 9
  rm -f src/devices/dev_footbridge.o gxemul
  make -j6 > "out/table/abuild_$V.log" 2>&1
  [ -x gxemul ] && [ gxemul -nt src/devices/dev_footbridge.c ] || { echo "BUILD FAIL"; tail -5 "out/table/abuild_$V.log"; exit 9; }
  for s in all5 decline; do
    python3 -u out/frozen/opus_w3.py ./gxemul out/arm_stub.bin "$s" > "out/table/${V}_$s.raw" 2>&1
    echo "--- $s : $(grep -E '^OPUS_W_ROWS|^OPUS_W_RED' "out/table/${V}_$s.raw" | tr '\n' ' ')"
  done
  grep -E '^Z1|COMPLAINTS' "out/table/${V}_all5.raw"
done
echo "S8_DONE"
