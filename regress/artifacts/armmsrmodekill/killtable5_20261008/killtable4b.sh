# killtable4.sh <lane> <tool:mutant>... -- #562 repair-3 kill table, one LANE (own clone /tmp/gxmsr6/mut<lane>).
# Baseline = msr6/src_v6; probe frozen at /tmp/gxmsr6/probe_frozen.py (copied once by the launcher).
S=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/msr6
R=/tmp/gxmsr6; L=$1; shift; M=$R/mutb$L; KT=$R/kt${L}b
FILES="src/cpus/cpu_arm.c src/cpus/cpu_arm_instr.c src/cpus/cpu_arm_instr_dpi.c src/include/cpu_arm.h"
rm -rf $M $KT; cp -a $R/fix $M; mkdir -p $KT; OUT=$KT/LANE${L}b.out
restore() { for f in $FILES; do cp $S/src_v6/${f#src/} $M/$f; done
  for f in $FILES; do cmp -s $M/$f $S/src_v6/${f#src/} || { echo "RESTORE CMP FAIL $f" | tee -a $OUT; exit 9; }; done; }
build() { ( cd $M && rm -f src/cpus/*.o gxemul && make -j2 > make.log 2>&1 ); local ok=1
  for f in $FILES; do [ $M/gxemul -nt $M/$f ] || ok=0; done; echo $ok; }
probe() { ( mkdir -p $KT/run && cd $KT/run && cp $R/probe_frozen.py p.py && python3 -u p.py $M/gxemul "$1" > $KT/$1.out 2>&1 ); }
line() { local r=$(grep '^ARMMSRMODE_RESULT=' $KT/$1.out); local d=$(grep '^ARMMSRMODE_REDS=' $KT/$1.out)
  local t=$(tail -1 $KT/$1.out)
  printf '%-20s %-14s %s  tail=%s\n' "$1" "${r#ARMMSRMODE_}" "${d#ARMMSRMODE_}" "$t" | tee -a $OUT
  for nm in $(grep '^ARMMSRMODE_REDS=' $KT/$1.out | sed 's/^ARMMSRMODE_REDS=//; s/ /_/g; s/,/ /g' | cut -d' ' -f1-3); do
    [ "$nm" = none ] && continue
    grep "^  ${nm//_/ } " $KT/$1.out | head -1 | sed 's/  */ /g' | cut -c1-120 | sed 's/^/      /' | tee -a $OUT
  done; }
echo "LANE $L -- $(date) -- baseline = HEAD $(cat $R/HEAD.sha) + msr6/src_v6; probe frozen (grid probe)" > $OUT
echo "$M/.MUTANT: baseline rebuild" > $M/.MUTANT
restore; [ "$(build)" = 1 ] || { echo "BASE BUILD STALE" | tee -a $OUT; exit 8; }
probe BASE_L$L; line BASE_L$L
for tm in "$@"; do
  tool=${tm%%:*}; m=${tm#*:}
  echo "$M/.MUTANT: $m" > $M/.MUTANT
  restore
  python3 $R/$tool $M $m >> $OUT 2>&1 || { echo "$m MUTANT-TEXT-NOT-FOUND -> FAIL" | tee -a $OUT; continue; }
  if [ "$(build)" != 1 ]; then echo "$m BUILD FAILED/STALE" | tee -a $OUT; grep -m3 error $M/make.log | tee -a $OUT; continue; fi
  probe $m; line $m
done
restore
if [ "$(build)" = 1 ]; then rm -f $M/.MUTANT; echo "RESTORED lane $L: sources cmp-clean vs msr6/src_v6, binary fresh, sentinel cleared" | tee -a $OUT
else echo "RESTORE REBUILD STALE -- sentinel kept" | tee -a $OUT; fi
probe BASE_AFTER_L$L; line BASE_AFTER_L$L
mkdir -p $S/killtable5b; cp $KT/*.out $S/killtable5b/
echo LANE${L}b_DONE | tee -a $OUT
