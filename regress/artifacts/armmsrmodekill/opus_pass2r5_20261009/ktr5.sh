# ktr5.sh LANEn -- Opus pass-2R5 kill table for #562 repair 5, in MY clones /tmp/gxopus562r5/<lane> only.
# Never writes GXEMUL-SEC, est, build, build-asan or /tmp/gxsec-build.
# LANE1-4: the SHIPPED 47-row probe (frozen copy, md5 97555f3a).  LANE5: the PROTOTYPE 48-row probe
# (the 47 shipped rows + `msr loop'), the standalone loop row per binary, and a HEAD leg.
LANE=$1
S=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/msr/opus5
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
R=/tmp/gxopus562r5; L=$R/$LANE; T=$L/tree; KT=$L/kt
FILES="src/cpus/cpu_arm.c src/cpus/cpu_arm_instr.c src/cpus/cpu_arm_instr_dpi.c src/include/cpu_arm.h"
OUT=$S/KTR5_$LANE.out
if [ "$LANE" = LANE5 ]; then PROBE=probe48.py; else PROBE=probe_frozen.py; fi
[ -d $T ] || { echo "NO TREE $T" | tee $OUT; exit 5; }
rm -rf $KT; mkdir -p $KT/run
cp $S/$PROBE $L/probe.py; cp $S/mutr5.py $L/mutr.py
cp $S/probe_frozen.py $L/probe_frozen.py; cp $S/loop_row.py $L/loop_row.py; cp $S/loop_standalone.py $L/ls.py
echo "--- OPUS KTR5 $LANE $(date) baseline=SEC working tree (4 files) via $R/base; probe=$PROBE ($(md5sum < $L/probe.py | cut -c1-8)); mutr5 $(md5sum < $L/mutr.py | cut -c1-8)" | tee $OUT
restore() { for f in $FILES; do cp $R/base/$f $T/$f; done
  for f in $FILES; do cmp -s $T/$f $SEC/$f || { echo "RESTORE CMP FAIL vs SEC $f" | tee -a $OUT; exit 9; }; done; }
build() { ( cd $T && rm -f src/cpus/*.o gxemul && make -j2 > $KT/make_$1.log 2>&1 ); local ok=1
  [ -x $T/gxemul ] || ok=0
  for f in $FILES; do [ $T/gxemul -nt $T/$f ] || ok=0; done; echo $ok; }
line() { local r=$(grep '^ARMMSRMODE_RESULT=' $KT/$1.out); local d=$(grep '^ARMMSRMODE_REDS=' $KT/$1.out)
  printf '%-22s %-14s %s  tail=%s\n' "$1" "${r#ARMMSRMODE_}" "${d#ARMMSRMODE_}" "$(tail -1 $KT/$1.out)" | tee -a $OUT
  grep ' FAIL ' $KT/$1.out | grep ' want=' | sed 's/  */ /g' | cut -c1-190 | sed 's/^/      /' | tee -a $OUT; }
probe() { ( cd $KT/run && python3 -u $L/probe.py $T/gxemul "$1" > $KT/$1.out 2>&1 ); line $1; }
loopsa() { ( cd $KT/run && python3 -u $L/ls.py $L/probe_frozen.py $L/loop_row.py $T/gxemul "$1" > $KT/$1.loop.out 2>&1 )
  echo "  [standalone msr loop, $1] $(grep -A2 '^  msr loop' $KT/$1.loop.out | tr '\n' ' ' | sed 's/  */ /g')  tail=$(tail -1 $KT/$1.loop.out)" | tee -a $OUT; }
echo "$T/.MUTANT: baseline build" > $T/.MUTANT
restore; echo "baseline cmp vs SEC: clean (4 files)" | tee -a $OUT
[ "$(build BASE)" = 1 ] || { echo "BASE BUILD STALE" | tee -a $OUT; exit 8; }
rm -f $T/.MUTANT
[ "$LANE" = LANE5 ] && loopsa BASE
probe BASE
for m in $(python3 $L/mutr.py x $LANE); do
  echo "$T/.MUTANT: $m" > $T/.MUTANT
  restore
  python3 $L/mutr.py $T $m >> $OUT 2>&1 || { echo "$m MUTANT-TEXT-NOT-FOUND -> FAIL" | tee -a $OUT; continue; }
  if [ "$(build $m)" != 1 ]; then echo "$m BUILD FAILED/STALE" | tee -a $OUT; grep -m3 -i error $KT/make_$m.log | tee -a $OUT; continue; fi
  [ "$LANE" = LANE5 ] && loopsa $m
  probe $m
done
if [ "$LANE" = LANE5 ]; then
  echo "$T/.MUTANT: HEAD ef577140 sources" > $T/.MUTANT
  for f in $FILES; do cp $R/headsrc/$f $T/$f; done
  for f in $FILES; do cmp -s $T/$f $R/headsrc/$f || { echo "HEAD COPY CMP FAIL $f" | tee -a $OUT; exit 9; }; done
  echo "HEAD sources installed (git show HEAD, cmp-clean)" | tee -a $OUT
  if [ "$(build HEAD)" = 1 ]; then loopsa HEAD; probe HEAD; else echo "HEAD BUILD FAILED/STALE" | tee -a $OUT; fi
fi
restore
if [ "$(build RESTORE)" = 1 ]; then rm -f $T/.MUTANT; echo "RESTORED: 4 sources cmp-clean vs SEC, binary fresh, sentinel cleared" | tee -a $OUT
else echo "RESTORE REBUILD STALE -- sentinel kept" | tee -a $OUT; fi
if [ "$LANE" = LANE5 ]; then loopsa BASE_AFTER; else probe BASE_AFTER; fi
mkdir -p $S/logs_$LANE; cp $KT/*.out $S/logs_$LANE/
echo KTR5_DONE | tee -a $OUT
