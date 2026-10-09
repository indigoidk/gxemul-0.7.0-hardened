#!/bin/bash
# fable5 late review of #473: third pass -- just-BELOW rows added to the scratch copy.
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/fableq
W=/tmp/fable473
MUTS="ctrl_rearm32767 M2_rearm_relax65536 M2b_arm_relax65536 M3_rearm_lower16384"
python3 "$SP/addrows473c.py" "$W/regress/diff_wdc_identify.fb.c" "$W/regress/diff_wdc_identify.fb2.c" || exit 9
bash "$SP/run473.sh" "$W/regress/diff_wdc_identify.fb2.c" fb2 $MUTS 2>&1 | tee "$W/out/fb2.txt"
cp "$W/out/fb2.txt" "$SP/measured_20261009/"
cp "$W/regress/diff_wdc_identify.fb2.c" "$SP/measured_20261009/diff_wdc_identify.fb2.c"
for M in $MUTS; do cp "$W/m_fb2_$M/run.log" "$SP/measured_20261009/fb2_$M.log" 2>/dev/null; done
echo DRIVE473C_DONE
