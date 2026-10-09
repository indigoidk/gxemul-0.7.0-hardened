# finalcheck.sh -- after both waves: no sentinel left in any of MY clones, every clone cmp-clean vs SEC
# with a binary newer than its sources, and every preserved log ends in its completion sentinel.
S=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/msr/opus5
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
FILES="src/cpus/cpu_arm.c src/cpus/cpu_arm_instr.c src/cpus/cpu_arm_instr_dpi.c src/include/cpu_arm.h"
for l in LANE1 LANE2 LANE3 LANE4 LANE5; do
  T=/tmp/gxopus562r5/$l/tree; st="clean"
  [ -e $T/.MUTANT ] && st="SENTINEL($(cat $T/.MUTANT))"
  for f in $FILES; do cmp -s $T/$f $SEC/$f || st="$st DIFF:$f"; [ $T/gxemul -nt $T/$f ] || st="$st STALE:$f"; done
  echo "$l: $st"
done
n=0; bad=0
for f in $S/logs_LANE*/*.out $S/logs2_LANE*/*.out; do
  n=$((n+1)); t=$(tail -1 $f)
  case "$t" in ARMMSRMODE_DONE|LOOPSTANDALONE_DONE) ;; *) bad=$((bad+1)); echo "NO SENTINEL: $f [$t]";; esac
done
echo "preserved logs: $n, without a completion sentinel: $bad"
