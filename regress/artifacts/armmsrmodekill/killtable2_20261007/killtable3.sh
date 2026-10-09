# killtable3.sh -- #562 table 3 (Opus pass-2 additions); runs AFTER killtable2.sh. Appends to KILLTABLE2.out.
S=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/msr3
R=/tmp/gxmsr3; M=$R/mut; KT=$R/kt3; F=$R/fix
FILES="src/cpus/cpu_arm.c src/cpus/cpu_arm_instr.c src/cpus/cpu_arm_instr_dpi.c src/include/cpu_arm.h"
grep -q KILLTABLE2_DONE $R/kt/KILLTABLE2.out || { echo "TABLE 2 NOT DONE -- refusing"; exit 7; }
[ -e $M/.MUTANT ] && echo "NOTE: mut sentinel present at start: $(cat $M/.MUTANT) -- restoring from src_v3"
rm -rf $KT; mkdir -p $KT; OUT=$R/kt/KILLTABLE2.out
cp $S/arm_msrmode_probe.py $R/probe_frozen3.py; cp $S/mutate3.py $R/mutate_frozen3.py
restore() { for f in $FILES; do cp $S/src_v3/${f#src/} $1/$f; done
  for f in $FILES; do cmp -s $1/$f $S/src_v3/${f#src/} || { echo "RESTORE CMP FAIL $1 $f" | tee -a $OUT; exit 9; }; done; }
build() { ( cd $1 && rm -f src/cpus/*.o gxemul && make -j4 > make.log 2>&1 ); local ok=1
  for f in $FILES; do [ $1/gxemul -nt $1/$f ] || ok=0; done; echo $ok; }
probe() { ( mkdir -p $KT/run && cd $KT/run && cp $1 p.py && python3 -u p.py $3 "$2" > $KT/$2.out 2>&1 ); }
line() { local r=$(grep '^ARMMSRMODE_RESULT=' $KT/$1.out); local d=$(grep '^ARMMSRMODE_REDS=' $KT/$1.out)
  local t=$(tail -1 $KT/$1.out)
  printf '%-22s %-14s %s  tail=%s\n' "$1" "${r#ARMMSRMODE_}" "${d#ARMMSRMODE_}" "$t" | tee -a $OUT
  for nm in $(grep '^ARMMSRMODE_REDS=' $KT/$1.out | sed 's/^ARMMSRMODE_REDS=//; s/ /_/g; s/,/ /g'); do
    [ "$nm" = none ] && continue
    grep "^  ${nm//_/ } " $KT/$1.out | head -1 | sed 's/  */ /g' | cut -c1-110 | sed 's/^/      /' | tee -a $OUT
  done; }
echo "--- TABLE 3 ($(date)): Opus pass-2 additions. baseline = HEAD + msr3/src_v3 (table-2 src + backstop comment rewording, comments only); probe3 = 38 rows (+ kill 03 + records fixes); probe2 = table-2 frozen 37-row probe" | tee -a $OUT
# the FIX tree, rebuilt on src_v3 -> run_fixed.out; HEAD -> run_head.out
restore $F; [ "$(build $F)" = 1 ] || { echo "FIX BUILD STALE" | tee -a $OUT; exit 8; }
probe $R/probe_frozen3.py FIXED_probe3 $F/gxemul; line FIXED_probe3
probe $R/probe_frozen3.py HEAD_probe3 $R/head/gxemul; line HEAD_probe3
echo "$M/.MUTANT: table-3 baseline rebuild" > $M/.MUTANT
restore $M; [ "$(build $M)" = 1 ] || { echo "BASE BUILD STALE" | tee -a $OUT; exit 8; }
probe $R/probe_frozen3.py BASE_probe3 $M/gxemul; line BASE_probe3
for m in $(python3 $R/mutate_frozen3.py x LIST); do
  echo "$M/.MUTANT: $m" > $M/.MUTANT
  restore $M
  python3 $R/mutate_frozen3.py $M $m >> $OUT 2>&1 || { echo "$m MUTANT-TEXT-NOT-FOUND -> FAIL" | tee -a $OUT; continue; }
  if [ "$(build $M)" != 1 ]; then echo "$m BUILD FAILED/STALE" | tee -a $OUT; continue; fi
  [ $m = O_mask_nibble ] && { probe $R/probe_frozen.py ${m}_probe2 $M/gxemul; line ${m}_probe2; }
  probe $R/probe_frozen3.py ${m}_probe3 $M/gxemul; line ${m}_probe3
done
restore $M
if [ "$(build $M)" = 1 ]; then rm -f $M/.MUTANT; echo "RESTORED (table 3): sources cmp-clean vs msr3/src_v3, binary fresh, sentinel cleared" | tee -a $OUT
else echo "RESTORE REBUILD STALE -- sentinel kept" | tee -a $OUT; fi
probe $R/probe_frozen3.py BASE_AFTER_probe3 $M/gxemul; line BASE_AFTER_probe3
cp $KT/FIXED_probe3.out $S/run_fixed.out; cp $KT/HEAD_probe3.out $S/run_head.out
mkdir -p $S/killtable3; cp $KT/*.out $S/killtable3/
echo KILLTABLE3_DONE | tee -a $OUT; cp $OUT $S/KILLTABLE2.out
