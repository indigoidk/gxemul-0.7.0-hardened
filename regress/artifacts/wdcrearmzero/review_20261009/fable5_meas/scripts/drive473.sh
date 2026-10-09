#!/bin/bash
# fable5 late review of #473: the whole measurement, in my own scratch (/tmp/fable473).
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/fableq
W=/tmp/fable473
MUTS="ctrl_rearm32767 M1_opswap_received M2_rearm_relax65536 M2b_arm_relax65536 M3_rearm_lower16384"
command -v python3 || { echo "NO python3 in WSL"; exit 7; }
echo "=============== SHIPPED DETECTOR (unmodified copy) ==============="
bash "$SP/run473.sh" "$W/regress/diff_wdc_identify.c" ship $MUTS 2>&1 | tee "$W/out/ship.txt"
echo "=============== REPAIR ROWS (scratch copy of the detector) ==============="
python3 "$SP/addrows473.py" "$W/regress/diff_wdc_identify.c" "$W/regress/diff_wdc_identify.fb.c" || exit 9
diff "$W/regress/diff_wdc_identify.c" "$W/regress/diff_wdc_identify.fb.c" | grep -cE '^[<>]'
bash "$SP/run473.sh" "$W/regress/diff_wdc_identify.fb.c" fb $MUTS 2>&1 | tee "$W/out/fb.txt"
echo DRIVE473_DONE
