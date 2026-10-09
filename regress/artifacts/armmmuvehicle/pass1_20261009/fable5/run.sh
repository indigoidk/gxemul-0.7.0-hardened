#!/bin/bash
cd /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/mmuv || exit 9
chmod +x gxemul
python3 -u exp.py ./gxemul > exp.out 2>&1
echo "rc=$?" >> exp.out
