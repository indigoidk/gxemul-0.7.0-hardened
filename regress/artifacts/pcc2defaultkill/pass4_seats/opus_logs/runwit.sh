#!/bin/bash
cp /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/panel_501p4_agents/opus/len4_witness.py /tmp/gxinst501p4/
cd /tmp/gxinst501p4 || exit 9
python3 -u ./len4_witness.py /tmp/gxopus501p4/gxemul BASE 2>&1 | tee /tmp/len4wit_BASE.out
