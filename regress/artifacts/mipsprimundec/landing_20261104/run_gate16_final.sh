#!/bin/bash
# run_gate16_final.sh -- gate 16 (gate_mips_folds.sh) alone, in situ, on the fixed build, with the probe's FINAL bytes (the regress
# review's two docstring corrections applied); the regress review's UNSETTLED 2 asked for a fresh in-situ count
R=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress
A=$R/artifacts/mipsprimundec/landing_20261104
md5sum $R/mips_primundec_probe.py $R/gate_mips_folds.sh > $A/MD5_gate16_final.txt
rm -rf /tmp/gxr16mpufinal; mkdir -p /tmp/gxr16mpufinal
date -u +start=%FT%TZ > $A/gate16_final.time
LOGDIR=/tmp/gxr16mpufinal bash "$R/gate_mips_folds.sh" > "$A/gate16_final.out" 2>&1
echo "gate rc=$?" >> $A/gate16_final.time
date -u +end=%FT%TZ >> $A/gate16_final.time
cp /tmp/gxr16mpufinal/mips_primundec_probe.log "$A/gate16_final_mips_primundec.log" 2>/dev/null
echo "total=$(grep -cE '^  (ok|FAIL) ' $A/gate16_final.out) block=$(grep -E '^  (ok|FAIL) ' $A/gate16_final.out | grep -c mips_primundec)" >> $A/gate16_final.time
tail -n 1 "$A/gate16_final.out"
echo RUN_GATE16_FINAL_DONE
