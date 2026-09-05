#!/bin/bash
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
T=/tmp/gxopus501p3
rm -rf "$T"
cp -a /mnt/c/DocumentNoSnc/CC/GXEMUL/build "$T"
cd "$T" || exit 9
if cmp -s src/devices/dev_pcc2.c "$SEC/src/devices/dev_pcc2.c"; then
  echo "CLONE_SRC_CMP_CLEAN_VS_SEC"
else
  echo "CLONE_SRC_DIFFERS_FROM_SEC -- STOP"; exit 8
fi
cp src/devices/dev_pcc2.c /tmp/pcc2.baseline.c
rm -f src/devices/dev_pcc2.o gxemul
make -j4 > /tmp/base_build.log 2>&1
echo "MAKE_RC=$?"
ls -la --time-style=full-iso gxemul src/devices/dev_pcc2.c
if [ gxemul -nt src/devices/dev_pcc2.c ]; then echo "BINARY_NEWER_OK"; else echo "BINARY_STALE -- STOP"; fi
md5sum "$SEC/regress/pcc2_default_probe.py"
