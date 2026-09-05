#!/bin/bash
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/pcc2p5_opus
cp "$SP/discriminator.py" /tmp/gxopus_p5_disc.py
md5sum /tmp/gxopus_p5_disc.py
cd /tmp/gxopus_p5 || exit 9
for b in BASE M1; do
    timeout 300 python3 -u /tmp/gxopus_p5_disc.py "/tmp/gxopus_p5_${b}_bin" "$b"
done
