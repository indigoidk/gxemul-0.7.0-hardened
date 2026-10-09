S=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/msr6
R=/tmp/gxmsr6
until [ -s $S/KILLTABLE5_lanes.out ] && grep -q LANE4_DONE $S/KILLTABLE5_lanes.out; do sleep 30; done
sleep 5
cp $S/mutr4.py $R/mutr4.py
L1=""; L2=""; L3=""; L4=""; i=0
for m in $(python3 $R/mutr4.py x LIST); do x="mutr4.py:$m"; case $((i % 4)) in 0) L1="$L1 $x";; 1) L2="$L2 $x";; 2) L3="$L3 $x";; 3) L4="$L4 $x";; esac; i=$((i+1)); done
echo "TABLE2 TOTAL $i"
bash $S/killtable4b.sh 1 $L1 > $R/lane1b.log 2>&1 &
bash $S/killtable4b.sh 2 $L2 > $R/lane2b.log 2>&1 &
bash $S/killtable4b.sh 3 $L3 > $R/lane3b.log 2>&1 &
bash $S/killtable4b.sh 4 $L4 > $R/lane4b.log 2>&1 &
wait
cat $R/kt1b/LANE1b.out $R/kt2b/LANE2b.out $R/kt3b/LANE3b.out $R/kt4b/LANE4b.out > $S/KILLTABLE5_lanes_opus.out
echo LAUNCH7_DONE
