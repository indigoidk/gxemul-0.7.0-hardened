# ktr5w2.sh LANEn -- Opus pass-2R5 WAVE 2, in MY clone /tmp/gxopus562r5/<lane> only, started only
# after that lane's wave-1 run has printed KTR5_DONE (its tree restored, cmp-clean, binary fresh).
# Measures the PROTOTYPE zero-observation reorder (probe47r.py) against the latch-clear restore
# mutants, and glm's C1 (M_pop_retafter) against the SHIPPED probe.
# Never writes GXEMUL-SEC, est, build, build-asan or /tmp/gxsec-build.
LANE=$1
S=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/msr/opus5
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
R=/tmp/gxopus562r5; L=$R/$LANE; T=$L/tree; KT=$L/kt2
FILES="src/cpus/cpu_arm.c src/cpus/cpu_arm_instr.c src/cpus/cpu_arm_instr_dpi.c src/include/cpu_arm.h"
OUT=$S/KTR5W2_$LANE.out
case $LANE in
  LANE1) JOBS="r:BASE r:N_pop_forceN_first" ;;
  LANE2) JOBS="r:N_dpi_forceN_first r:N_pop_clrN_first" ;;
  LANE3) JOBS="r:N_pop_orold_first r:N_dpi_orold_first" ;;
  LANE4) JOBS="r:E_pop_forceN_clracc" ;;
  LANE5) JOBS="s:M_pop_retafter" ;;
esac
until grep -q KTR5_DONE $S/KTR5_$LANE.out 2>/dev/null; do sleep 20; done
rm -rf $KT; mkdir -p $KT/run
cp $S/probe47r.py $L/probe47r.py; cp $S/probe_frozen.py $L/probe47.py; cp $S/mutr5.py $L/mutr_w2.py
echo "--- OPUS KTR5 WAVE2 $LANE $(date) probe47r $(md5sum < $L/probe47r.py | cut -c1-8) (REORDERED grid, prototype); probe47 $(md5sum < $L/probe47.py | cut -c1-8) (shipped); mutr5 $(md5sum < $L/mutr_w2.py | cut -c1-8)" | tee $OUT
ok=1
[ -e $T/.MUTANT ] && { echo "SENTINEL PRESENT: $(cat $T/.MUTANT)" | tee -a $OUT; ok=0; }
for f in $FILES; do cmp -s $T/$f $SEC/$f || { echo "TREE NOT CLEAN vs SEC: $f" | tee -a $OUT; ok=0; }
  [ $T/gxemul -nt $T/$f ] || { echo "BINARY NOT FRESH vs $f" | tee -a $OUT; ok=0; }; done
[ $ok = 1 ] || { echo "WAVE2 ABORTED: tree not clean" | tee -a $OUT; exit 7; }
echo "wave-1 restore verified: 4 sources cmp-clean vs SEC, binary fresh, no sentinel" | tee -a $OUT
restore() { for f in $FILES; do cp $R/base/$f $T/$f; done
  for f in $FILES; do cmp -s $T/$f $SEC/$f || { echo "RESTORE CMP FAIL vs SEC $f" | tee -a $OUT; exit 9; }; done; }
build() { ( cd $T && rm -f src/cpus/*.o gxemul && make -j2 > $KT/make_$1.log 2>&1 ); local ok=1
  [ -x $T/gxemul ] || ok=0
  for f in $FILES; do [ $T/gxemul -nt $T/$f ] || ok=0; done; echo $ok; }
line() { local r=$(grep '^ARMMSRMODE_RESULT=' $KT/$1.out); local d=$(grep '^ARMMSRMODE_REDS=' $KT/$1.out)
  printf '%-30s %-14s %s  tail=%s\n' "$1" "${r#ARMMSRMODE_}" "${d#ARMMSRMODE_}" "$(tail -1 $KT/$1.out)" | tee -a $OUT
  grep ' FAIL ' $KT/$1.out | grep ' want=' | sed 's/  */ /g' | cut -c1-190 | sed 's/^/      /' | tee -a $OUT; }
dirty=0
for j in $JOBS; do
  p=${j%%:*}; m=${j#*:}
  if [ $p = r ]; then PR=$L/probe47r.py; tag=r47_$m; else PR=$L/probe47.py; tag=s47_$m; fi
  if [ $m != BASE ]; then
    echo "$T/.MUTANT: $m" > $T/.MUTANT; dirty=1
    restore
    python3 $L/mutr_w2.py $T $m >> $OUT 2>&1 || { echo "$m MUTANT-TEXT-NOT-FOUND -> FAIL" | tee -a $OUT; continue; }
    if [ "$(build $m)" != 1 ]; then echo "$m BUILD FAILED/STALE" | tee -a $OUT; grep -m3 -i error $KT/make_$m.log | tee -a $OUT; continue; fi
  fi
  ( cd $KT/run && python3 -u $PR $T/gxemul "$tag" > $KT/$tag.out 2>&1 ); line $tag
done
if [ $dirty = 1 ]; then
  restore
  if [ "$(build RESTORE)" = 1 ]; then rm -f $T/.MUTANT; echo "RESTORED: 4 sources cmp-clean vs SEC, binary fresh, sentinel cleared" | tee -a $OUT
  else echo "RESTORE REBUILD STALE -- sentinel kept" | tee -a $OUT; fi
fi
mkdir -p $S/logs2_$LANE; cp $KT/*.out $S/logs2_$LANE/
echo KTR5W2_DONE | tee -a $OUT
