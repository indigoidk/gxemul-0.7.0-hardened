#!/bin/bash
#  Copy scripts + outputs to the artifacts dir the coordinator named (the ONLY write under the project).
set -u
C5=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus551p1/c
W=/tmp/opus551c
A=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/wdcidselfcheck_20260925/opus551_measured_c
mkdir -p "$A/logs" "$A/harness_variants"
for f in xform5.py analyze5.py pin.py; do cp "$C5/$f" "$A/$f.txt"; done
for f in run5.sh pin.sh save5.sh analyze5.out pin.out; do cp "$C5/$f" "$A/$f"; done
cp "$W/gatewdc.inc" "$A/gate2_wdc_block_extracted.inc.txt"
for h in "$W"/h/*.c; do cp "$h" "$A/harness_variants/$(basename "$h").txt"; done
for pair in "C pristine" "C_recon_ge_sub pristine" "C_recon_ge_sub dropold" "C_recon_ge_sub drqring" "C_recon_ge_sub w57hi" \
            "C_sub_after pristine" "C_sub_after dropold" "C_sub_after drqring" "C_sub_after w57hi" \
            "C_reset1 drqring" "C_reset2 drqring" "C_nocmpinc_reset1 dropold" "Cfix pristine" \
            "Cfix_recon_ge_sub dropold" "Cfix_sub_after w57hi" "Cpin pristine" "Cpin_nocmpinc_reset1 dropold"; do
    set -- $pair; cp "$W/dev/$2/regress/$1.log" "$A/logs/$1.$2.log"; done
bad=0; for l in "$A"/logs/*.log; do tail -1 "$l" | grep -qE '^WDC_IDENTIFY_(PASS|FAIL)$' || { echo "NO SENTINEL: $l"; bad=1; }; done
echo "logs: $(ls "$A"/logs | wc -l), sentinel-less: $bad"; ls "$A"
