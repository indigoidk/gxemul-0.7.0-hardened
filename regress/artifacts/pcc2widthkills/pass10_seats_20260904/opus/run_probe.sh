#!/bin/sh
# $1 = label
OUT=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/pcc2p10_opus
cd /mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress || exit 9
echo "START $1 $(date '+%H:%M:%S')"
python3 -u /tmp/frozen_probe_p10.py /tmp/gxopus_p10/gxemul "$1" > $OUT/$1.out 2>&1
echo "RC=$?  END $1 $(date '+%H:%M:%S')"
tail -3 $OUT/$1.out
grep -c RED $OUT/$1.out
