# launch5w2.sh -- wave 2: each lane waits for its own wave-1 KTR5_DONE, then runs ktr5w2 (frozen copy).
S=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/msr/opus5
R=/tmp/gxopus562r5
cp $S/ktr5w2.sh $R/ktr5w2.run.sh
echo "LAUNCH5W2 $(date)"
for l in LANE1 LANE2 LANE3 LANE4 LANE5; do
  bash $R/ktr5w2.run.sh $l > $R/$l.w2.launch.log 2>&1 &
done
wait
for l in LANE1 LANE2 LANE3 LANE4 LANE5; do cp $R/$l.w2.launch.log $S/$l.w2.launch.log; done
echo "LAUNCH5W2_DONE $(date)"
