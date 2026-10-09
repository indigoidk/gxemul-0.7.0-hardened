# killtable2.sh -- #562 pass-2 kill table in /tmp/gxmsr3/mut (clone-local; never touches project trees)
S=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/msr3
R=/tmp/gxmsr3; M=$R/mut; KT=$R/kt
FILES="src/cpus/cpu_arm.c src/cpus/cpu_arm_instr.c src/cpus/cpu_arm_instr_dpi.c src/include/cpu_arm.h"
rm -rf $M $KT; cp -a $R/fix $M; mkdir -p $KT
cp $S/arm_msrmode_probe.py $R/probe_frozen.py; cp $S/mutate2.py $R/mutate_frozen.py
OUT=$KT/KILLTABLE2.out
restore() { for f in $FILES; do cp $S/src/${f#src/} $M/$f; done
  for f in $FILES; do cmp -s $M/$f $S/src/${f#src/} || { echo "RESTORE CMP FAIL $f" | tee -a $OUT; exit 9; }; done; }
build() { ( cd $M && rm -f src/cpus/*.o gxemul && make -j4 > make.log 2>&1 ); local ok=1
  for f in $FILES; do [ $M/gxemul -nt $M/$f ] || ok=0; done; echo $ok; }
probe() { ( mkdir -p $KT/run && cd $KT/run && cp $R/probe_frozen.py p.py && python3 -u p.py $M/gxemul "$1" > $KT/$1.out 2>&1 ); }
line() { local r=$(grep '^ARMMSRMODE_RESULT=' $KT/$1.out); local d=$(grep '^ARMMSRMODE_REDS=' $KT/$1.out)
  local t=$(tail -1 $KT/$1.out)
  printf '%-20s %-14s %s  tail=%s\n' "$1" "${r#ARMMSRMODE_}" "${d#ARMMSRMODE_}" "$t" | tee -a $OUT
  for nm in $(grep '^ARMMSRMODE_REDS=' $KT/$1.out | sed 's/^ARMMSRMODE_REDS=//; s/ /_/g; s/,/ /g'); do
    [ "$nm" = none ] && continue
    grep "^  ${nm//_/ } " $KT/$1.out | head -1 | sed 's/  */ /g' | cut -c1-110 | sed 's/^/      /' | tee -a $OUT
  done; }
echo "KILLTABLE2 #562 pass 2 -- $(date) -- baseline = HEAD $(cat $R/HEAD.sha) + msr3/src (SEC working tree + comment edits); probe frozen (37 rows); N_* = pass-2 mutants, M_* = table-1 set re-run" > $OUT
echo "$M/.MUTANT: baseline rebuild" > $M/.MUTANT
restore; [ "$(build)" = 1 ] || { echo "BASE BUILD STALE" | tee -a $OUT; exit 8; }
probe BASE; line BASE
for m in $(python3 $R/mutate_frozen.py x LIST); do
  echo "$M/.MUTANT: $m" > $M/.MUTANT
  restore
  python3 $R/mutate_frozen.py $M $m >> $OUT 2>&1 || { echo "$m MUTANT-TEXT-NOT-FOUND -> FAIL" | tee -a $OUT; continue; }
  if [ "$(build)" != 1 ]; then echo "$m BUILD FAILED/STALE" | tee -a $OUT; grep -m3 error $M/make.log | tee -a $OUT; continue; fi
  probe $m; line $m
  mkdir -p $S/killtable2; cp $KT/$m.out $S/killtable2/; cp $OUT $S/KILLTABLE2.out
done
restore
if [ "$(build)" = 1 ]; then rm -f $M/.MUTANT; echo "RESTORED: sources cmp-clean vs msr3/src, binary fresh, sentinel cleared" | tee -a $OUT
else echo "RESTORE REBUILD STALE -- sentinel kept" | tee -a $OUT; fi
probe BASE_AFTER; line BASE_AFTER
mkdir -p $S/killtable2; cp $KT/*.out $S/killtable2/
echo KILLTABLE2_DONE | tee -a $OUT; cp $OUT $S/KILLTABLE2.out
