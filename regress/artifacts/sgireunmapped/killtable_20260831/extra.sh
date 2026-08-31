#!/bin/bash
set -u
H=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/o499
CLONE=/tmp/gx499
cp $H/extra_rows.py $H/extra_rows.run.py
echo "EXTRA ROWS -- four rows the shipped detector does not contain."
echo "start $(date +%H:%M:%S)"
for V in base fix fix6 m4_bitcollide; do
  echo "==================================================================="
  echo "VARIANT: $V"
  if [ ! -f $CLONE/gxemul.$V ]; then echo "  MISSING BINARY $CLONE/gxemul.$V -- skip"; continue; fi
  python3 -u $H/extra_rows.run.py $CLONE/gxemul.$V $V 2>&1
done
echo "EXTRA_TABLE_DONE $(date +%H:%M:%S)"
