#!/bin/bash
# batch 2: build (with sentinel + two-part restore), probe each, then discriminators for every survivor candidate
set -u
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_close2
OUT=/tmp/close2
ps aux | grep -E '[g]xemul|[c]wp_close2|[m]ake -j' | head && echo "(above: stray processes, if any)"
bash $SP/build_muts2.sh
bash $SP/run_probes.sh "istat_leak dog_leak istat_lane"
cp $SP/disc_c2.py $OUT/disc_c2.FROZEN.py
: > $OUT/disc_c2.out
for m in rd_hi_lh istat_leak dog_leak istat_lane; do
    python3 -u $OUT/disc_c2.FROZEN.py /tmp/gx529c2_base $OUT/builds/gx_$m $m 2>&1 | tee -a $OUT/disc_c2.out
done
echo BATCH2_DONE
