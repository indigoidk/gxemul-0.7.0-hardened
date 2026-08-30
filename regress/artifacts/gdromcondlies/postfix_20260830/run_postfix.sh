#!/bin/bash
#  POST-FIX leg.  Same instrument as the pre-fix run: the probe is the COMMITTED
#  copy under regress/artifacts/, unedited since the 15/15 run.
R=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
P=$R/regress/artifacts/gdromcondlies/witness_20260830/gdrom_cond_witness.py
BIN=/mnt/c/DocumentNoSnc/cc/GXEMUL/build/gxemul
KERNEL=/mnt/c/DocumentNoSnc/CC/GXEMUL/_images/openbsd76-landisk-bsd.rd

echo "=== TWO-PART CLEARANCE ==="
cmp -s /mnt/c/DocumentNoSnc/cc/GXEMUL/build/src/devices/dev_dreamcast_gdrom.c \
       $R/src/devices/dev_dreamcast_gdrom.c && echo "SRC_CMP_CLEAN" || echo "SRC_CMP_DIRTY"
[ "$BIN" -nt /mnt/c/DocumentNoSnc/cc/GXEMUL/build/src/devices/dev_dreamcast_gdrom.c ] \
  && echo "BINARY_NEWER yes" || echo "BINARY_NEWER NO"
echo ""
cd /tmp || exit 9
python3 -u "$P" "$BIN" "$KERNEL" 2>&1
echo "RUNNER_RC=$?"
