#!/bin/bash
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad
ART=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/opus_pass2_20260913
cp $SP/crime_p2_dbg.py /tmp/crime_p2_dbg.FROZEN.py
for b in base a_lo10; do python3 -u /tmp/crime_p2_dbg.FROZEN.py /tmp/p2bins/$b $b; done > /tmp/p2logs/dbg_probe.out 2>&1
cat /tmp/p2logs/dbg_probe.out
cp /tmp/p2logs/dbg_probe.out $ART/logs/
cp /tmp/crime_p2_dbg.FROZEN.py $ART/scripts/crime_p2_dbg.py
cp $SP/p2_dbg.sh $ART/scripts/
md5sum $ART/scripts/*.py $ART/scripts/*.sh > $ART/scripts/MD5SUMS
