#!/bin/bash
SPW=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_pcc2k
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
CL=/tmp/gxopus_pcc2k; cd "$CL" || exit 9
echo sentinel > .MUTANT
for M in BASE M_announce_notmien BASE; do
  echo "===== $M (repaired probe)"
  python3 "$SPW/mutate.py" "$M" || exit 9
  rm -f src/devices/dev_pcc2.o; make -j4 > "$SPW/build2_$M.log" 2>&1; echo MAKE_RC=$?
  [ gxemul -nt src/devices/dev_pcc2.c ] && echo FRESH=OK || { echo STALE; exit 9; }
  python3 -u "$SPW/probe.repaired.py" "$CL/gxemul" "$M" > "$SPW/rep_$M.raw" 2>&1
  grep -E "RESULT|DONE|FAIL|says mien" "$SPW/rep_$M.raw"
done
cmp src/devices/dev_pcc2.c "$SEC/src/devices/dev_pcc2.c" && [ gxemul -nt src/devices/dev_pcc2.c ] && rm -f .MUTANT && echo CLEARED
