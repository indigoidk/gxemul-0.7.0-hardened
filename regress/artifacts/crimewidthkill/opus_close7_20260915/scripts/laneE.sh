#!/bin/bash
L=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/opus_close7_20260915
until grep -q LANE_C_DONE $L/logs/lane_C.out 2>/dev/null; do sleep 10; done
bash $L/scripts/lane7.sh E E3b_byp_revout_acc
