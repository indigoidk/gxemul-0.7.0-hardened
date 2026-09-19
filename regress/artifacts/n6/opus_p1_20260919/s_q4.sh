#!/bin/bash
set -u
T=/tmp/gxopus539p1
D=/mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/n6/opus_p1_20260919
cd "$T" || exit 9
echo "baseline in place?  cmp vs HEAD:"
cmp -s src/devices/dev_footbridge.c out/fb_head.c && echo "  CLEAN" || { echo "  DIRTY"; exit 9; }
python3 -u "$D/opus_q4.py" "$T/gxemul" "$T/out/arm_stub.bin" > out/q4.raw 2>&1
echo "rc=$?  sentinel=$(tail -1 out/q4.raw)"
cp out/q4.raw "$D/q4.raw"
cat out/q4.raw
