#!/bin/bash
#  the valid-run control for kill479, against the detector it was written for (#479's tree, 23430365)
set -u
W=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/wkdc
export KILLSCORE=$W/controls/frozen/killscore.sh
Z=$W/controls/frozen
bash "$W/witness/w1r_kill479_real.sh" "$Z/kill479.HEAD.sh" HEAD "$W/r479src"; echo "w1r479 HEAD rc=$?"
bash "$W/witness/w1r_kill479_real.sh" "$Z/kill479.FIX.sh"  FIX  "$W/r479src"; echo "w1r479 FIX rc=$?"
echo RUN_W1R479_DONE
