#!/bin/bash
O=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2g/opus
RUN=/tmp/opusr3d_brun_$(date +%H%M%S); mkdir -p "$RUN"
cp "$O/run_b.py" "$O/gen_r3d_opus_b.py" "$O/gen_r3d_opus.py" "$RUN/"
python3 -u "$RUN/run_b.py"
[ -e /tmp/opusr3d_b/.MUTANT ] && echo "SENTINEL PRESENT" || echo "no sentinel"
cmp /tmp/opusr3d_b/src/devices/dev_footbridge.c $O/../frozen/dev_footbridge.c && echo "b device == frozen"
