# launch5.sh -- run the five Opus pass-2R5 lanes concurrently and wait for all of them.
S=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/msr/opus5
R=/tmp/gxopus562r5
[ -d $R/HEADL ] && [ ! -d $R/LANE5 ] && mv $R/HEADL $R/LANE5
cp $S/ktr5.sh $R/ktr5.run.sh
echo "LAUNCH5 $(date)"
for l in LANE1 LANE2 LANE3 LANE4 LANE5; do
  bash $R/ktr5.run.sh $l > $R/$l.launch.log 2>&1 &
done
wait
for l in LANE1 LANE2 LANE3 LANE4 LANE5; do cp $R/$l.launch.log $S/$l.launch.log; done
echo "LAUNCH5_DONE $(date)"
