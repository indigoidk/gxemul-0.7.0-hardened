#!/bin/sh
P=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/pcc2p11_opus
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
cd $SEC/regress || exit 9
python3 -u $P/control_iclr.py /tmp/gxopus_p11/gxemul "$1" 2>&1 | tail -12
