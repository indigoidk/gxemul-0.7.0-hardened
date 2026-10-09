#!/bin/bash
# fable5 late review of #473: the REPAIR-ROW pass only (the ship pass is in out/ship.txt).
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/fableq
W=/tmp/fable473
MUTS="ctrl_rearm32767 M1_opswap_received M2_rearm_relax65536 M2b_arm_relax65536 M3_rearm_lower16384"
python3 "$SP/addrows473.py" "$W/regress/diff_wdc_identify.c" "$W/regress/diff_wdc_identify.fb.c" || exit 9
echo "added lines: $(diff "$W/regress/diff_wdc_identify.c" "$W/regress/diff_wdc_identify.fb.c" | grep -cE '^>')"
grep -n 'printf("  SETUP fb inbuf failed' "$W/regress/diff_wdc_identify.fb.c" | head -2
bash "$SP/run473.sh" "$W/regress/diff_wdc_identify.fb.c" fb $MUTS 2>&1 | tee "$W/out/fb.txt"
# durable copies: /tmp evaporates
mkdir -p "$SP/measured_20261009"
cp "$W/out/ship.txt" "$W/out/fb.txt" "$W/out/base.log" "$SP/measured_20261009/" 2>/dev/null
cp "$W/regress/diff_wdc_identify.fb.c" "$SP/measured_20261009/diff_wdc_identify.fb.c"
for M in $MUTS; do cp "$W/m_ship_$M/run.log" "$SP/measured_20261009/ship_$M.log" 2>/dev/null; cp "$W/m_fb_$M/run.log" "$SP/measured_20261009/fb_$M.log" 2>/dev/null; done
md5sum "$W/src/devices/dev_wdc.c" > "$SP/measured_20261009/BASELINE_dev_wdc.md5"
ls -la "$SP/measured_20261009/" | head -30
echo DRIVE473B_DONE
