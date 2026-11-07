#!/bin/bash
#  Every witness, run twice -- HEAD's driver and the FIXED copy -- into its own log.  WSL:
#     bash /mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/wkdc/controls/run_controls.sh
#  Then compare.py reads the logs.  Nothing outside wkdc/ is written.
set -u
W=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/wkdc
H=$W/headsrc/regress
F=$W/fix
export KILLSCORE=$F/killscore.sh
exec > "$W/controls/run_controls.log" 2>&1
echo "run_controls start $(date '+%F %T')"
#  frozen copies of every driver under test: one instrument per comparison
mkdir -p "$W/controls/frozen"
cp "$H/artifacts/wdccmdreset/killtable_20260827/kill479.sh" "$W/controls/frozen/kill479.HEAD.sh"
cp "$F/kill479.sh"                                      "$W/controls/frozen/kill479.FIX.sh"
cp "$H/selftest_mutation.sh"                            "$W/controls/frozen/selftest_mutation.HEAD.sh"
cp "$F/selftest_mutation.sh"                            "$W/controls/frozen/selftest_mutation.FIX.sh"
cp "$H/artifacts/batteryreds/row5_20260829/killrow5c.sh" "$W/controls/frozen/killrow5c.HEAD.sh"
cp "$F/killrow5c.sh"                                    "$W/controls/frozen/killrow5c.FIX.sh"
cp "$F/killscore.sh"                                    "$W/controls/frozen/killscore.sh"
export KILLSCORE=$W/controls/frozen/killscore.sh
md5sum "$W"/controls/frozen/* | sed "s#$W/##"
Z=$W/controls/frozen
bash "$W/witness/w1_kill479.sh"       "$Z/kill479.HEAD.sh" HEAD;          echo "w1 HEAD rc=$?"
bash "$W/witness/w1_kill479.sh"       "$Z/kill479.FIX.sh"  FIX;           echo "w1 FIX rc=$?"
bash "$W/witness/w1r_kill479_real.sh" "$Z/kill479.HEAD.sh" HEAD;          echo "w1r HEAD rc=$?"
bash "$W/witness/w1r_kill479_real.sh" "$Z/kill479.FIX.sh"  FIX;           echo "w1r FIX rc=$?"
for st in mixed allcrash allkill real; do
	bash "$W/witness/w2_gate3.sh" "$Z/selftest_mutation.HEAD.sh" HEAD "$st"; echo "w2 HEAD $st rc=$?"
	bash "$W/witness/w2_gate3.sh" "$Z/selftest_mutation.FIX.sh"  FIX  "$st"; echo "w2 FIX $st rc=$?"
done
bash "$W/witness/w3_killrow5c.sh"     "$Z/killrow5c.HEAD.sh" HEAD;        echo "w3 HEAD rc=$?"
bash "$W/witness/w3_killrow5c.sh"     "$Z/killrow5c.FIX.sh"  FIX;         echo "w3 FIX rc=$?"
echo "RUN_CONTROLS_DONE $(date '+%F %T')"
