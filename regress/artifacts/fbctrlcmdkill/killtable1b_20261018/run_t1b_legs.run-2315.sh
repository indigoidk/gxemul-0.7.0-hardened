#!/bin/bash
#  run_t1b_legs.sh -- #567: kill table 1b (frozen driver), then the SHIPPED probe's two legs on one instrument.
#  The legs run the pass-2 frozen copy (pass2_20261018/frozen/fbctrl_cmd_probe.py.txt, the bytes the brief inlines):
#  HEAD's binary (/tmp/gx566, checked to hold HEAD's dev_fbctrl.c) and the fix's (/tmp/gx567, after 1b's restore).
set -u
S=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/fbcmd
P=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/fbctrlcmdkill/pass2_20261018
F=src/devices/dev_fbctrl.c
bash "$S/killtable567b.run-2315.sh"
tail -1 "$S/killtable1b/SCORES.txt" | grep -qx TABLE1B_DONE || { echo "TABLE 1B DID NOT FINISH -- legs not run"; exit 9; }
mkdir -p "$P/legs"
PROBE="$P/legs/probe.frozen.py"
cp "$P/frozen/fbctrl_cmd_probe.py.txt" "$PROBE"
{
echo "#567 in-tree legs, $(date '+%F %T'): the shipped probe (frozen copy, md5 $(md5sum < "$PROBE" | cut -c1-32))"
for leg in HEAD:/tmp/gx566:head_dev_fbctrl.c FIX:/tmp/gx567:dev_fbctrl.fix567.c; do
    IFS=: read -r name tree want <<< "$leg"
    if ! cmp -s "$S/$want" "$tree/$F"; then echo "$name: $tree/$F is not $want -- leg not run"; continue; fi
    if [ -e "$tree/.MUTANT" ]; then echo "$name: $tree carries a sentinel -- leg not run"; continue; fi
    if [ ! "$tree/gxemul" -nt "$tree/$F" ]; then echo "$name: binary older than $F -- leg not run"; continue; fi
    python3 -u "$PROBE" "$tree/gxemul" > "$P/legs/$name.out" 2>&1
    rc=$?
    echo "$name ($tree, $want; binary md5 $(md5sum < "$tree/gxemul" | cut -c1-12)): rc=$rc $(grep -a '^FBCMD_RESULT' "$P/legs/$name.out") $(grep -a '^FBCMD_CONTROL' "$P/legs/$name.out") last=$(tail -1 "$P/legs/$name.out")"
done
echo LEGS_DONE
} | tee "$P/legs/LEGS.out"
