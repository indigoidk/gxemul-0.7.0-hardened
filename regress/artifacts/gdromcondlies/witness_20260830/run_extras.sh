#!/bin/bash
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad
cd /tmp/gxopus_cond || exit 9
python3 -u "$SP/gdrom_cond_extras.py" /tmp/gxopus_cond/gxemul \
    /mnt/c/DocumentNoSnc/CC/GXEMUL/_images/openbsd76-landisk-bsd.rd 2>&1
