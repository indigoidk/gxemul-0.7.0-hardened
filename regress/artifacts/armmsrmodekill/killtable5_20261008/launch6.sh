S=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/msr6
R=/tmp/gxmsr6
cp $S/arm_msrmode_probe.py $R/probe_frozen.py
TOOLS="${TOOLS:-mutr.py mutr2.py mutate2.py mutate3.py mutr3b.py mutate5.py mutate6.py}"
for t in $TOOLS; do cp $S/$t $R/$t; done
ALL=""; SEEN=" "
for t in $TOOLS; do for m in $(python3 $R/$t x LIST); do
  case "$SEEN" in *" $m "*) continue;; esac; SEEN="$SEEN$m "; ALL="$ALL $t:$m"; done; done
L1=""; L2=""; L3=""; L4=""; i=0
for x in $ALL; do case $((i % 4)) in 0) L1="$L1 $x";; 1) L2="$L2 $x";; 2) L3="$L3 $x";; 3) L4="$L4 $x";; esac; i=$((i+1)); done
echo "TOTAL $i distinct mutants"
bash $S/killtable4.sh 1 $L1 > $R/lane1.log 2>&1 &
bash $S/killtable4.sh 2 $L2 > $R/lane2.log 2>&1 &
bash $S/killtable4.sh 3 $L3 > $R/lane3.log 2>&1 &
bash $S/killtable4.sh 4 $L4 > $R/lane4.log 2>&1 &
wait
cat $R/kt1/LANE1.out $R/kt2/LANE2.out $R/kt3/LANE3.out $R/kt4/LANE4.out > $S/KILLTABLE5_lanes${TAG}.out
echo LAUNCH6_DONE
