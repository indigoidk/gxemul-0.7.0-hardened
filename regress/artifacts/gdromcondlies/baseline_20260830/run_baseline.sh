#!/bin/bash
R=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
BIN=/mnt/c/DocumentNoSnc/cc/GXEMUL/build/gxemul
KERNEL=/mnt/c/DocumentNoSnc/CC/GXEMUL/_images/openbsd76-landisk-bsd.rd
cmp -s /mnt/c/DocumentNoSnc/cc/GXEMUL/build/src/devices/dev_dreamcast_gdrom.c \
       $R/src/devices/dev_dreamcast_gdrom.c && echo "SRC_CMP_CLEAN" || echo "SRC_CMP_DIRTY"
[ "$BIN" -nt /mnt/c/DocumentNoSnc/cc/GXEMUL/build/src/devices/dev_dreamcast_gdrom.c ] \
  && echo "BINARY_NEWER yes" || echo "BINARY_NEWER NO"
cd /tmp || exit 9
python3 -u "$R/regress/gdrom_cond_probe.py" "$BIN" "$KERNEL" 2>&1
echo "RC=$?"
