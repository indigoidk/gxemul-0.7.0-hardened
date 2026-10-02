#!/bin/bash
S=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/opus_close7_20260915/scripts
bash $S/discall7.sh > $S/../logs/discall7.out 2>&1
bash $S/lane7.sh B E1_byp_ctl4r E2_byp_time4 E3_byp_revout
