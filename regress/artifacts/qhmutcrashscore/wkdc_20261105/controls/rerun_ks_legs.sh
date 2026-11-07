#!/bin/bash
#  Re-run the legs that SOURCE killscore.sh, with the FINAL helper (last NON-BLANK line), so every FIX leg in
#  CONTROLS.txt was measured with the helper as recorded in fix/.  HEAD legs do not source it and are not re-run.
set -u
W=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/wkdc
Z=$W/controls/frozen
exec > "$W/controls/rerun_ks_legs.log" 2>&1
cp "$W/fix/killscore.sh" "$Z/killscore.sh"
cp "$W/fix/kill479.sh"   "$Z/kill479.FIX.sh"
md5sum "$Z/killscore.sh" "$Z/kill479.FIX.sh" | sed "s#$W/##"
export KILLSCORE=$Z/killscore.sh
bash "$W/witness/w1_kill479.sh"       "$Z/kill479.FIX.sh" FIX;                 echo "w1 FIX rc=$?"
bash "$W/witness/w1r_kill479_real.sh" "$Z/kill479.FIX.sh" FIX "$W/r479src";    echo "w1r479 FIX rc=$?"
bash "$W/controls/ks_unit.sh" "$Z/killscore.sh" > "$W/controls/ks_unit.frozen.out" 2>&1; echo "ks_unit (frozen copy) rc=$?"
echo RERUN_KS_LEGS_DONE
