# ktr.sh -- Opus pass-2R kill table for #562, in MY clone /tmp/gxopus562r only.
S=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/msr/opus2r
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
R=/tmp/gxopus562r2; T=$R/tree; KT=$R/kt
FILES="src/cpus/cpu_arm.c src/cpus/cpu_arm_instr.c src/cpus/cpu_arm_instr_dpi.c src/include/cpu_arm.h"
OUT=$S/KTR2.out
mkdir -p $R
if [ ! -d $T ]; then cp -a /tmp/gxopus562/tree $T || exit 5; fi
# baseline snapshot = the SEC working-tree copies NOW (frozen for the whole table)
rm -rf $R/base; mkdir -p $R/base
for f in $FILES; do mkdir -p $R/base/$(dirname $f); cp $SEC/$f $R/base/$f; done
cp $SEC/regress/arm_msrmode_probe.py $R/probe_frozen.py; cp $S/mutr2.py $R/mutr_frozen.py
rm -rf $KT; mkdir -p $KT/run
echo "--- OPUS KTR2 $(date) baseline=SEC working tree (4 files), probe=frozen SEC arm_msrmode_probe.py ($(md5sum < $R/probe_frozen.py | cut -c1-8))" | tee $OUT
restore() { for f in $FILES; do cp $R/base/$f $T/$f; done
  for f in $FILES; do cmp -s $T/$f $SEC/$f || { echo "RESTORE CMP FAIL vs SEC $f" | tee -a $OUT; exit 9; }; done; }
build() { ( cd $T && rm -f src/cpus/*.o gxemul && make -j4 > $KT/make_$1.log 2>&1 ); local ok=1
  for f in $FILES; do [ $T/gxemul -nt $T/$f ] || ok=0; done; echo $ok; }
probe() { ( cd $KT/run && python3 -u $R/probe_frozen.py $T/gxemul "$1" > $KT/$1.out 2>&1 ); }
line() { local r=$(grep '^ARMMSRMODE_RESULT=' $KT/$1.out); local d=$(grep '^ARMMSRMODE_REDS=' $KT/$1.out)
  printf '%-20s %-14s %s  tail=%s\n' "$1" "${r#ARMMSRMODE_}" "${d#ARMMSRMODE_}" "$(tail -1 $KT/$1.out)" | tee -a $OUT
  grep 'FAIL' $KT/$1.out | sed 's/  */ /g' | cut -c1-120 | sed 's/^/      /' | tee -a $OUT; }
echo "$T/.MUTANT: baseline build" > $T/.MUTANT
restore $T; echo "baseline cmp vs SEC: clean (4 files)" | tee -a $OUT
[ "$(build BASE)" = 1 ] || { echo "BASE BUILD STALE" | tee -a $OUT; exit 8; }
probe BASE; line BASE
for m in $(python3 $R/mutr_frozen.py x LIST); do
  echo "$T/.MUTANT: $m" > $T/.MUTANT
  restore
  python3 $R/mutr_frozen.py $T $m >> $OUT 2>&1 || { echo "$m MUTANT-TEXT-NOT-FOUND -> FAIL" | tee -a $OUT; continue; }
  if [ "$(build $m)" != 1 ]; then echo "$m BUILD FAILED/STALE" | tee -a $OUT; continue; fi
  probe $m; line $m
done
restore
if [ "$(build RESTORE)" = 1 ]; then rm -f $T/.MUTANT; echo "RESTORED: 4 sources cmp-clean vs SEC, binary fresh, sentinel cleared" | tee -a $OUT
else echo "RESTORE REBUILD STALE -- sentinel kept" | tee -a $OUT; fi
probe BASE_AFTER; line BASE_AFTER
mkdir -p $S/logs2; cp $KT/*.out $S/logs2/
echo KTR2_DONE | tee -a $OUT
