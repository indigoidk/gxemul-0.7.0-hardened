#!/bin/bash
#  gate14_full.sh -- the full gate 14 (regress/gate_arm.sh, with the #568 block wired) on build/gxemul, ALONE.
set -u
R=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress
L=/tmp/gx568gate
rm -rf "$L"; mkdir -p "$L"
echo "start $(date '+%F %T') binary $(md5sum < /mnt/c/DocumentNoSnc/cc/GXEMUL/build/gxemul | cut -c1-32) gate_arm.sh $(md5sum < $R/gate_arm.sh | cut -c1-32)"
cd "$R" && LOGDIR=$L bash gate_arm.sh
rc=$?
echo "end $(date '+%F %T') rc=$rc"
cp "$L/vme_default.log" /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/vme/apply/gate14_vme_default.log 2>/dev/null
echo "GATE14_FULL_DONE rc=$rc"
