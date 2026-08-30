#!/bin/bash
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad
BIN=/tmp/gxopus_cond/gxemul
KERNEL=/mnt/c/DocumentNoSnc/CC/GXEMUL/_images/openbsd76-landisk-bsd.rd

echo "=== PRE-RUN FRESHNESS (two-part clearance, run not asserted) ==="
cmp -s /tmp/gxopus_cond/src/devices/dev_dreamcast_gdrom.c \
       /mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/devices/dev_dreamcast_gdrom.c \
  && echo "SRC_CMP_CLEAN" || echo "SRC_CMP_DIRTY"
if [ "$BIN" -nt /tmp/gxopus_cond/src/devices/dev_dreamcast_gdrom.c ]; then
    echo "BINARY_NEWER_THAN_SOURCE yes"
else
    echo "BINARY_NEWER_THAN_SOURCE NO"
fi
ls -la "$BIN"
ls -la "$KERNEL"
echo ""

cd /tmp/gxopus_cond || exit 9
python3 -u "$SP/gdrom_cond_witness.py" "$BIN" "$KERNEL" 2>&1
echo "RUNNER_RC=$?"
