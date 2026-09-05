#!/bin/bash
cd /tmp/gxopus501p4 || exit 9
rm -f src/devices/dev_pcc2.o
make -j4 > /tmp/gxopus501p4_base_build.log 2>&1
echo "MAKE_RC=$?"
ls -la --time-style=+%H:%M:%S gxemul src/devices/dev_pcc2.c
if [ gxemul -nt src/devices/dev_pcc2.c ]; then echo BINARY_NEWER_OK; else echo BINARY_STALE_FAIL; fi
cmp -s src/devices/dev_pcc2.c /mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/devices/dev_pcc2.c && echo SRC_CMP_CLEAN_VS_SEC || echo SRC_DIFFERS
