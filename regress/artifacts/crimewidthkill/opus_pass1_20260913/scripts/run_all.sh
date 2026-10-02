#!/bin/bash
set -u
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad
[ -d /tmp/gxopuscrime_out_run1 ] || mv /tmp/gxopuscrime_out /tmp/gxopuscrime_out_run1
bash "$SP/run_rows.sh" base fault decline delete return1 fallsw nolatch len1only readonly
