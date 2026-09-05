#!/bin/sh
#  $1 = label
P=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/pcc2p11_opus
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
cp $SEC/regress/pcc2_width_probe.py /tmp/frozen_probe_p11.py
echo "FROZEN_MD5=$(md5sum /tmp/frozen_probe_p11.py | cut -c1-8)"
cd $SEC/regress || exit 9
date +'START %H:%M:%S'
python3 -u /tmp/frozen_probe_p11.py /tmp/gxopus_p11/gxemul "$1" > $P/$1.out 2>&1
echo "PROBE_RC=$?"
date +'END   %H:%M:%S'
tail -3 $P/$1.out
grep -c "FAIL$" $P/$1.out
