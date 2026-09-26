#!/bin/bash
#  Copy scripts + outputs to the durable artifacts dir the coordinator named (the ONLY write under the project).
set -u
P2=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus551p1/p2
W=/tmp/opus551p2
A=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/wdcidselfcheck_20260925/opus551_measured_p2
mkdir -p "$A/logs" "$A/harness_variants"
for f in xform3.py analyze3.py wide.py; do cp "$P2/$f" "$A/$f.txt"; done
for f in run3.sh wide.sh save.sh analyze3.out wide.out; do cp "$P2/$f" "$A/$f"; done
cp "$W/gatewdc.inc" "$A/gate2_wdc_block_extracted.inc.txt"
for h in F F_fc F_fc_scnoforce_chkstub F_name F_postinc F_scnoforce_chkstub F_sect4 F_u16 F_want165 F_wrap F_wide F_wide_u16 F_wide_sect4; do
    cp "$W/h/$h.c" "$A/harness_variants/$h.c.txt"; done
for pair in "F pristine" "F dropold" "F w57hi" "F w58lo" "F drqring" "F_want165 dropold" "F_sect4 w57hi" "F_wrap w57hi" \
            "F_u16 w58lo" "F_postinc drqring" "F_name drqring" "F_scnoforce_chkstub pristine" \
            "F_fc_scnoforce_chkstub pristine" "F_fc pristine" "F_wide pristine" "F_wide_u16 pristine" "F_wide_sect4 pristine"; do
    set -- $pair; cp "$W/dev/$2/regress/$1.log" "$A/logs/$1.$2.log"; done
bad=0; for l in "$A"/logs/*.log; do tail -1 "$l" | grep -qE '^WDC_IDENTIFY_(PASS|FAIL)$' || { echo "NO SENTINEL: $l"; bad=1; }; done
echo "logs saved: $(ls "$A"/logs | wc -l), sentinel-less: $bad"; ls "$A"
