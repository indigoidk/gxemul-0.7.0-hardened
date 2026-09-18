#!/bin/bash
SPW=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_pcc2k
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
CL=/tmp/gxopus_pcc2k
rm -rf "$CL"; cp -a /mnt/c/DocumentNoSnc/CC/GXEMUL/build "$CL" || exit 9
echo "sentinel" > "$CL/.MUTANT"
cd "$CL"
rm -f src/cpus/*.o
for M in BASE M_announce_notmien M_announce_onlyifsuppressing BASE; do
  echo "===== $M"
  python3 "$SPW/mutate.py" "$M" || exit 9
  diff "$SEC/src/devices/dev_pcc2.c" src/devices/dev_pcc2.c
  rm -f src/devices/dev_pcc2.o
  make -j4 > "$SPW/build_$M.log" 2>&1; echo "MAKE_RC=$?"
  if [ gxemul -nt src/devices/dev_pcc2.c ]; then echo FRESH=OK; else echo FRESH=STALE; exit 9; fi
  python3 -u "$SPW/probe.frozen.py" "$CL/gxemul" "$M" > "$SPW/$M.raw" 2>&1
  grep -E "RESULT|FAIL|DONE" "$SPW/$M.raw"; grep -E "^(c040|genctl|irq)" "$SPW/$M.raw" | grep -v " ok"
done
cmp src/devices/dev_pcc2.c "$SEC/src/devices/dev_pcc2.c" && [ gxemul -nt src/devices/dev_pcc2.c ] && rm -f .MUTANT && echo CLEARED
