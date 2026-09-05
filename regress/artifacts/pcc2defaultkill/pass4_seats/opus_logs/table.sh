#!/bin/bash
#  #501 pass-4 Opus seat kill table.  Sentinel discipline; restore VERIFIED by cmp against SEC
#  and by a REBUILT binary at the end.  Nothing is written to any project tree.
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/devices/dev_pcc2.c
C=/tmp/gxopus501p4
M=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/panel_501p4_agents/opus/mutate.py
echo "opus501p4 kill table -- mutating $C/src/devices/dev_pcc2.c" > $C/.MUTANT
for m in "$@"; do
  echo "===== $m ====="
  python3 "$M" "$m" || { echo "SKIP $m"; continue; }
  ( cd $C && rm -f src/devices/dev_pcc2.o && make -j4 > /tmp/build_$m.log 2>&1 ; echo "MAKE_RC=$?" )
  if [ ! $C/gxemul -nt $C/src/devices/dev_pcc2.c ]; then echo "BINARY_STALE_FAIL $m"; tail -5 /tmp/build_$m.log; continue; fi
  echo "BINARY_NEWER_OK"
  ( cd /tmp/gxinst501p4 && python3 -u ./pcc2_default_probe.py $C/gxemul "$m" > /tmp/gxopus501p4_$m.out 2>&1 )
  grep -E "PCC2D_RESULT|PCC2D_RED" /tmp/gxopus501p4_$m.out
done
echo "===== RESTORE ====="
python3 "$M" RESTORE
( cd $C && rm -f src/devices/dev_pcc2.o && make -j4 > /tmp/build_restore.log 2>&1 ; echo "MAKE_RC=$?" )
cmp -s $C/src/devices/dev_pcc2.c $SEC && echo "RESTORE_CMP_CLEAN_VS_SEC" || echo "RESTORE_CMP_FAIL"
if [ $C/gxemul -nt $C/src/devices/dev_pcc2.c ]; then echo "RESTORE_BINARY_NEWER_OK"; rm -f $C/.MUTANT; echo "SENTINEL_CLEARED"; else echo "RESTORE_BINARY_STALE -- SENTINEL KEPT"; fi
