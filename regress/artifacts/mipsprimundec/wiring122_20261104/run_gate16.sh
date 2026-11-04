#!/bin/bash
# run_gate16.sh -- gate 16 (gate_mips_folds.sh) with the mips_primundec block, alone, on the fixed build
R=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress
A=$R/artifacts/mipsprimundec/wiring122_20261104
rm -rf /tmp/gxr16mpu122; mkdir -p /tmp/gxr16mpu122
LOGDIR=/tmp/gxr16mpu122 bash "$R/gate_mips_folds.sh" > "$A/gate16.out" 2>&1
echo "gate rc=$?"
tail -n 2 "$A/gate16.out"
cp /tmp/gxr16mpu122/mips_primundec_probe.log "$A/gate16_mips_primundec.log" 2>/dev/null
grep -c "mips_primundec" "$A/gate16.out"
grep -E "FAIL|SKIP" "$A/gate16.out" | head -5
echo RUN_GATE16_DONE
