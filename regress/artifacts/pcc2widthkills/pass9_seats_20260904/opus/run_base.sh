#!/bin/sh
cd /tmp/gxopus_p9 || exit 9
date +%H:%M:%S
python3 -u /tmp/frozen_probe_p9.py /tmp/gxopus_p9/gxemul OPUS_BASE > /tmp/gxopus_p9_BASE.out 2>&1
echo "PROBE_RC=$?"
date +%H:%M:%S
tail -6 /tmp/gxopus_p9_BASE.out
cp /tmp/gxopus_p9_BASE.out /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/pcc2p9_opus/BASE.out
