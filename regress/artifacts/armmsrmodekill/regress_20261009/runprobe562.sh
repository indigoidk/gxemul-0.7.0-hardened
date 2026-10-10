#!/bin/bash
# fable5 REGRESS seat for #562: run the COMMITTED probe (one instrument, from the commit's own regress dir)
# against the PARENT and the COMMIT binaries, sequentially, in the private scratch clone.
set -u
D=/tmp/gxfable562
S=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/c562/fable/work
cd "$D/commit/regress" || { echo "NO REGRESS DIR"; exit 9; }
echo "probe md5: $(md5sum arm_msrmode_probe.py)"
echo "python3: $(python3 --version 2>&1)"
for pair in "parent PARENT_04f3e7c0" "commit COMMIT_4f908ad5"; do
  set -- $pair
  echo "=== run $1 ($2) start $(date +%T)"
  python3 -u arm_msrmode_probe.py "$D/$1/gxemul" "$2" > "$S/probe_$1.out" 2>&1; echo "PROBE_RC=$? end $(date +%T)"
  grep -E '^ARMMSRMODE_(CONTROL|RESULT|SESSIONS|REDS|TALLY|DONE)' "$S/probe_$1.out"
done
echo "PROBERUNS_DONE $(date +%T)"
