# looptest0.sh -- quick standalone run of the prototype loop row on my r4 clone's RESTORED fix binary
# (fix4 == fix5 byte-identical product code).  Verifies that binary first: 4 sources cmp-clean vs
# SEC and the binary newer than each.  Writes only under /tmp/gxopus562r5 and the scratchpad.
S=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/msr/opus5
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
T=/tmp/gxopus562r4/LANE1/tree
FILES="src/cpus/cpu_arm.c src/cpus/cpu_arm_instr.c src/cpus/cpu_arm_instr_dpi.c src/include/cpu_arm.h"
ok=1
for f in $FILES; do
  cmp -s $T/$f $SEC/$f || { echo "SRC DIFFERS vs SEC: $f"; ok=0; }
  [ $T/gxemul -nt $T/$f ] || { echo "BINARY NOT NEWER than $f"; ok=0; }
done
[ -e $T/.MUTANT ] && { echo "SENTINEL PRESENT"; ok=0; }
echo "r4 LANE1 fix binary verified: $ok"
[ $ok = 1 ] || exit 4
mkdir -p /tmp/gxopus562r5/looptest && cd /tmp/gxopus562r5/looptest
cp $S/probe_frozen.py ./probe_frozen.py; cp $S/loop_row.py ./loop_row.py; cp $S/loop_standalone.py ./ls.py
python3 -u ls.py ./probe_frozen.py ./loop_row.py $T/gxemul r4fix 2>&1 | tee $S/looptest0.out
