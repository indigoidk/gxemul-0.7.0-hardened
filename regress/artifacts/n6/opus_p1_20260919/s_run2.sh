#!/bin/bash
set -u
T=/tmp/gxopus539p1
D=/mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/n6/opus_p1_20260919
SECR=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress
cd "$T" || exit 9

echo "########## M3b: raw reg text ##########"
python3 -u "$D/opus_m3b.py" "$T/gxemul" "$T/out/arm_stub.bin" > "$T/out/opus_m3b.raw" 2>&1
echo "rc=$?  sentinel=$(tail -1 "$T/out/opus_m3b.raw")"
cp "$T/out/opus_m3b.raw" "$D/opus_m3b.raw"

echo
echo "########## M4: the real footbridge_sites_probe.py on the COMMITTED baseline ##########"
cp "$SECR/footbridge_sites_probe.py" "$T/out/footbridge_sites_probe.frozen.py"
cd "$T/out" || exit 9
timeout 600 python3 -u "$T/out/footbridge_sites_probe.frozen.py" "$T/gxemul" "$T/out/arm_stub.bin" > "$T/out/sites.raw" 2>&1
echo "rc=$?"
cp "$T/out/sites.raw" "$D/sites.raw"
cat "$T/out/sites.raw"

echo
echo "########## single-step interrupt suppression, in THIS fork ##########"
grep -n "Do not cause interrupts while single-stepping" -A 3 \
     /mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/cpus/cpu_dyntrans.c
