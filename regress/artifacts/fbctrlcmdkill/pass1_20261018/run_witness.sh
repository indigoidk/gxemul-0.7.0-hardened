#!/bin/bash
#  run_witness.sh -- fbctrlcmdkill's test-first witness on the HEAD binary in the scratch clone /tmp/gx566.
#  Both clearance parts are checked first: the clone's dev_fbctrl.c is HEAD's blob, and the binary is newer than it.
set -u
S=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/fbcmd
C=/tmp/gx566
echo "WITNESS start $(date '+%F %T')"
[ -e "$C/.MUTANT" ] && { echo "clone carries a sentinel -- stop"; exit 9; }
cmp -s "$S/head_dev_fbctrl.c" "$C/src/devices/dev_fbctrl.c" && echo "part 1: dev_fbctrl.c == HEAD" || { echo "part 1 FAILED"; exit 9; }
[ "$C/gxemul" -nt "$C/src/devices/dev_fbctrl.c" ] && echo "part 2: binary newer than dev_fbctrl.c" || { echo "part 2 FAILED"; exit 9; }
echo "binary md5 $(md5sum < "$C/gxemul" | cut -c1-32)"
python3 -u "$S/fbctrl_cmd_witness.py" "$C/gxemul" > "$S/WITNESS_headbin.out" 2>&1
echo "witness rc=$?"
cat "$S/WITNESS_headbin.out"
echo "WITNESS end $(date '+%F %T')"
