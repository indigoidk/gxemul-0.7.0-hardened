#!/bin/bash
cd /tmp
python3 /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/mk_table46.py > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/mk_table46.out 2>&1; echo "MKTABLE RC=$?"
echo "--- table 16's clone, READ-ONLY for me: still clean?"
ls /tmp/gxopus_r14/.MUTANT 2>&1 | head -1
cmp /tmp/gxopus_r14/src/devices/dev_sgi_ip32.c /mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/src/devices/dev_sgi_ip32.c && echo "gxopus_r14 source CLEAN"
md5sum /tmp/gxopus_r14_bins16/base /tmp/gxopus_acc46_bins/base | cut -c1-8
echo "--- my clone after the runs"
ls /tmp/gxopus_acc46/.MUTANT 2>&1 | head -1
cmp /tmp/gxopus_acc46/src/devices/dev_sgi_ip32.c /mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/src/devices/dev_sgi_ip32.c && echo "gxopus_acc46 source CLEAN"
[ /tmp/gxopus_acc46/gxemul -nt /tmp/gxopus_acc46/src/devices/dev_sgi_ip32.c ] && echo "gxopus_acc46 binary FRESH"
ps -eo pid,args | grep -E '[g]xemul|[r]eplay46' | head -3; echo "stray processes listed above (none expected)"
