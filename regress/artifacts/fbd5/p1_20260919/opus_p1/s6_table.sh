#!/bin/bash
# The Q2 weakening table.  FROZEN COPIES of the probe and the patcher are used,
# so the originals stay editable while this runs.
set -u
T=/tmp/gxopusfbd5
SECG=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
D=/mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/fbd5/opus_p1_20260919
cd "$T" || exit 9
mkdir -p out/frozen out/table
cp "$D/opus_w.py" out/frozen/opus_w.py
cp "$D/mkfix.py"  out/frozen/mkfix.py
cp "$SECG/regress/footbridge_sites_probe.py" out/frozen/sites.py
echo "FROZEN: $(md5sum out/frozen/*.py)"
echo "$T/.MUTANT: dev_footbridge.c under a kill table (fbd5 opus p1)" > "$T/.MUTANT"

for V in fix m_keepexit m_unlatch m_sharebit m_leak18c m_store180 m_swallow m_misname m_latchrd m_fiqleak m_fiqraw; do
  echo ""
  echo "############################ VARIANT $V"
  git -C "$SECG" show HEAD:src/devices/dev_footbridge.c > src/devices/dev_footbridge.c || exit 9
  python3 out/frozen/mkfix.py src/devices/dev_footbridge.c "$V" || { echo "PATCH REFUSED $V"; continue; }
  rm -f src/devices/dev_footbridge.o gxemul
  make -j6 > "out/table/build_$V.log" 2>&1
  RC=$?
  if [ ! -x gxemul ] || [ ! gxemul -nt src/devices/dev_footbridge.c ]; then
    echo "$V BUILD FAILED rc=$RC"; tail -5 "out/table/build_$V.log"; continue
  fi
  echo "$V build rc=$RC binary=$(stat -c %y gxemul)"
  for s in accept decline; do
    python3 -u out/frozen/opus_w.py ./gxemul out/arm_stub.bin "$s" > "out/table/${V}_$s.raw" 2>&1
    echo "  $s : $(grep -E '^OPUS_W_ROWS|^OPUS_W_RED' "out/table/${V}_$s.raw" | tr '\n' ' ')"
  done
  python3 -u out/frozen/sites.py ./gxemul out/arm_stub.bin > "out/table/${V}_sites.raw" 2>&1
  echo "  sites: $(grep -E '^ROWS=|^FOOTBRIDGE_SITES_' "out/table/${V}_sites.raw" | tr '\n' ' ')  K1:$(grep -E '^K1 ' "out/table/${V}_sites.raw" | tail -c 40 | tr -d '\n')"
done
echo ""
echo "S6_DONE"
