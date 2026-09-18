#!/bin/bash
SPW=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus535
CL=/tmp/gxopus535; cd "$CL" || exit 9
echo "sentinel: dev_pcc2.c mutants r2 (opus535)" > .MUTANT
rm -f src/cpus/*.o
for P in "BASE BASE" "A_latch_bypass_mien A" "F_latchset_mienclear F" "BASE BASE_restore"; do
  set -- $P; M=$1; L=$2
  echo "===== $M"
  python3 "$SPW/mutate.py" "$M" || exit 9
  rm -f src/devices/dev_pcc2.o
  make -j4 > "$SPW/build_r2_$L.log" 2>&1; echo "MAKE_RC=$?"
  [ gxemul -nt src/devices/dev_pcc2.c ] && echo FRESH=OK || { echo FRESH=STALE; exit 9; }
  [ "$L" = BASE_restore ] && continue
  python3 -u "$SPW/probe.r2.py" "$CL/gxemul" "$M" > "$SPW/r2_$L.raw" 2>&1
  grep -E "RESULT|WITNESS" "$SPW/r2_$L.raw"; grep " FAIL$" "$SPW/r2_$L.raw"; echo "TAIL: $(tail -1 "$SPW/r2_$L.raw")"
done
cmp src/devices/dev_pcc2.c "$SPW/pcc2_HEAD.c" && [ gxemul -nt src/devices/dev_pcc2.c ] && rm -f .MUTANT && echo CLEARED
