#!/bin/bash
#  Copy scripts + outputs to the artifacts dir the coordinator named (the ONLY write under the project).
set -u
F2B=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus551p1/f2b
W=/tmp/opus551f2b
A=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/wdcidselfcheck_20260925/opus551_measured_f2b
mkdir -p "$A/logs" "$A/harness_variants"
for f in xform4.py analyze4.py cnt.py; do cp "$F2B/$f" "$A/$f.txt"; done
for f in run4.sh cnt.sh save4.sh analyze4.out cnt.out; do cp "$F2B/$f" "$A/$f"; done
cp "$W/gatewdc.inc" "$A/gate2_wdc_block_extracted.inc.txt"
echo "cmp_fails occurrences in B_cnt.c: $(grep -c cmp_fails "$W/h/B_cnt.c")" > "$A/B_cnt_check.txt"
for h in "$W"/h/*.c; do cp "$h" "$A/harness_variants/$(basename "$h").txt"; done
for pair in "B pristine" "B_want165 dropold" "B_sect4 w57hi" "B_wrap w57hi" "B_u16 w58lo" "B_postinc drqring" \
            "B_name drqring" "B_scnoforce_chkstub pristine" "B_tally pristine" "B_tally dropold" "B_tally drqring" \
            "B_tally w57hi" "B_andsect pristine" "B_nosc_full pristine" "B_nosc_keepdecl pristine" \
            "B_cnt pristine" "B_cnt_tally dropold" "B_cnt_tally drqring" "B_cnt_tally w57hi"; do
    set -- $pair; cp "$W/dev/$2/regress/$1.log" "$A/logs/$1.$2.log"; done
cp "$W/dev/pristine/regress/B_nosc_nodecl.cc" "$A/logs/B_nosc_nodecl.pristine.cc.txt"
bad=0; for l in "$A"/logs/*.log; do tail -1 "$l" | grep -qE '^WDC_IDENTIFY_(PASS|FAIL)$' || { echo "NO SENTINEL: $l"; bad=1; }; done
echo "logs: $(ls "$A"/logs | wc -l), sentinel-less: $bad"; cat "$A/B_cnt_check.txt"; ls "$A"
