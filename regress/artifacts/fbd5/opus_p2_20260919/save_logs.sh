#!/bin/bash
D=/mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/fbd5/opus_p2_20260919/logs
mkdir -p "$D"; cd /tmp/gxopusfbd5p2/out || exit 1
cp sites_*.log diff_*.log mut_*.diff sites_M13*.py sites_R0.py "$D"/
ls "$D" | wc -l
