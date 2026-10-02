#!/bin/bash
L=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/opus_close7_20260915
until grep -q LANE_A_DONE $L/logs/lane_A.out 2>/dev/null; do sleep 10; done
bash $L/scripts/lane7.sh C F1_byp_ctl8w_0201 F1b_byp_ctl4w_0201 F3_byp_sw04
