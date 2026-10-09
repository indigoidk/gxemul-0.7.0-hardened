# ktr3b.sh LANE3|LANE4 MODE(both|closure) -- Opus pass-2R3 kill table for #562 repair 3, in MY clones /tmp/gxopus562r3/<lane> only.
LANE=$1; MODE=$2
S=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/msr/opus3
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
R=/tmp/gxopus562r3/$LANE; T=$R/tree; KT=$R/kt
FILES="src/cpus/cpu_arm.c src/cpus/cpu_arm_instr.c src/cpus/cpu_arm_instr_dpi.c src/include/cpu_arm.h"
OUT=$S/KTR3_$LANE.out
mkdir -p $R
if [ ! -d $T ]; then cp -a /tmp/gxopus562r2/tree $T || exit 5; fi
rm -rf $R/base; mkdir -p $R/base
for f in $FILES; do mkdir -p $R/base/$(dirname $f); cp $SEC/$f $R/base/$f; done
cp $S/probe_frozen.py $R/probe_frozen.py; cp $S/mutr3b.py $R/mutr_frozen.py; cp $S/probe_closure2.py $R/probe_closure.py
rm -rf $KT; mkdir -p $KT/run
echo "--- OPUS KTR3 $LANE $(date) baseline=SEC working tree (4 files), probe=frozen ($(md5sum < $R/probe_frozen.py | cut -c1-8)) closure ($(md5sum < $R/probe_closure.py | cut -c1-8)) mode=$MODE" | tee $OUT
restore() { for f in $FILES; do cp $R/base/$f $T/$f; done
  for f in $FILES; do cmp -s $T/$f $SEC/$f || { echo "RESTORE CMP FAIL vs SEC $f" | tee -a $OUT; exit 9; }; done; }
build() { ( cd $T && rm -f src/cpus/*.o gxemul && make -j4 > $KT/make_$1.log 2>&1 ); local ok=1
  [ -x $T/gxemul ] || ok=0
  for f in $FILES; do [ $T/gxemul -nt $T/$f ] || ok=0; done; echo $ok; }
probe() { if [ "$MODE" = both ]; then ( cd $KT/run && python3 -u $R/probe_frozen.py $T/gxemul "$1" > $KT/$1.out 2>&1 ); line $1; fi
  ( cd $KT/run && python3 -u $R/probe_closure.py $T/gxemul "$1" > $KT/$1.CL.out 2>&1 ); line $1.CL; }
line() { local r=$(grep '^ARMMSRMODE_RESULT=' $KT/$1.out); local d=$(grep '^ARMMSRMODE_REDS=' $KT/$1.out)
  printf '%-20s %-14s %s  tail=%s\n' "$1" "${r#ARMMSRMODE_}" "${d#ARMMSRMODE_}" "$(tail -1 $KT/$1.out)" | tee -a $OUT
  grep 'FAIL' $KT/$1.out | sed 's/  */ /g' | cut -c1-160 | sed 's/^/      /' | tee -a $OUT; }
echo "$T/.MUTANT: baseline build" > $T/.MUTANT
restore; echo "baseline cmp vs SEC: clean (4 files)" | tee -a $OUT
[ "$(build BASE)" = 1 ] || { echo "BASE BUILD STALE" | tee -a $OUT; exit 8; }
probe BASE
for m in $(python3 $R/mutr_frozen.py x $LANE); do
  echo "$T/.MUTANT: $m" > $T/.MUTANT
  restore
  python3 $R/mutr_frozen.py $T $m >> $OUT 2>&1 || { echo "$m MUTANT-TEXT-NOT-FOUND -> FAIL" | tee -a $OUT; continue; }
  if [ "$(build $m)" != 1 ]; then echo "$m BUILD FAILED/STALE" | tee -a $OUT; tail -5 $KT/make_$m.log | tee -a $OUT; continue; fi
  probe $m
done
restore
if [ "$(build RESTORE)" = 1 ]; then rm -f $T/.MUTANT; echo "RESTORED: 4 sources cmp-clean vs SEC, binary fresh, sentinel cleared" | tee -a $OUT
else echo "RESTORE REBUILD STALE -- sentinel kept" | tee -a $OUT; fi
probe BASE_AFTER
mkdir -p $S/logs_$LANE; cp $KT/*.out $S/logs_$LANE/
echo KTR3_DONE | tee -a $OUT
