#!/bin/bash
set -u
T=/tmp/gxopusfbd5
D=/mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/fbd5/opus_p1_20260919
cd "$T" || exit 9
echo "=== binary under test ==="
ls -la gxemul; stat -c '%y' gxemul src/devices/dev_footbridge.c
echo "=== sentinel check ==="; ls -la .MUTANT 2>/dev/null || echo "  no .MUTANT (clean baseline)"
python3 -u "$D/opus_w.py" ./gxemul out/arm_stub.bin accept
