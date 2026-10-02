#!/bin/bash
L=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/opus_close7_20260915
until grep -q LANE_B_DONE $L/logs/lane_B.out 2>/dev/null; do sleep 10; done
bash $L/scripts/lane7.sh D F4a_byp_imask4r F4b_byp_istat4r
bash $L/scripts/discall7b.sh > $L/logs/discall7b.out 2>&1
