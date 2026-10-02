#!/bin/bash
# #529 F2 Opus seat, phase 2: build c_dog (clone-local sentinel, restore verified), run the FROZEN 71-row detector and
# the obs probe on it, then the REPAIR ROWS script on base and on every mutant that scored 71/71.  One run at a time.
set -u
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
ART=$SEC/regress/artifacts/crimewidthkill/opus_f2_20260913/logs
C=/tmp/gxopus529f2
F=src/devices/dev_sgi_ip32.c
L=/tmp/f2logs
B=/tmp/f2bins
cp $SP/mutants_f2.py /tmp/mutants_f2b.FROZEN.py
cp $SP/crime_f2_repairrows.py /tmp/crime_f2_rep.FROZEN.py
md5sum /tmp/crime_f2.FROZEN.py /tmp/crime_f2_obs.FROZEN.py /tmp/mutants_f2b.FROZEN.py /tmp/crime_f2_rep.FROZEN.py | tee $L/INSTRUMENT2.md5
cd $C || exit 9
[ -e .MUTANT ] && { echo "SENTINEL PRESENT at start -- abort"; exit 8; }
cmp -s $F $SEC/$F && echo "P2 BASELINE_CMP CLEAN" | tee $L/phase2.out || { echo "P2 BASELINE_CMP DIFFERS -- abort"; exit 8; }
echo "$F -- #529 F2 Opus seat phase 2 (c_dog); restore from GXEMUL-SEC" > .MUTANT
for m in c_dog; do
  python3 /tmp/mutants_f2b.FROZEN.py $m $SEC/$F $F > $L/$m.apply 2>&1 || { echo "$m APPLY_FAILED"; cat $L/$m.apply; }
  diff -u $SEC/$F $F > $L/$m.diff
  rm -f src/devices/dev_sgi_ip32.o gxemul
  make -j4 > $L/$m.build 2>&1; rc=$?
  if [ $rc -eq 0 ] && [ gxemul -nt $F ] && [ src/devices/dev_sgi_ip32.o -nt $F ]; then cp gxemul $B/$m; echo "$m BUILD_OK" | tee -a $L/phase2.out
  else echo "$m BUILD_FAILED rc=$rc" | tee -a $L/phase2.out; fi
done
cp $SEC/$F $F
rm -f src/devices/dev_sgi_ip32.o gxemul
make -j4 > $L/restore2.build 2>&1
if cmp -s $F $SEC/$F && [ gxemul -nt $F ] && [ src/devices/dev_sgi_ip32.o -nt $F ] && cmp -s gxemul $B/base; then
  rm -f .MUTANT; echo "P2 RESTORED: cmp clean, binary -nt source, == base; SENTINEL REMOVED" | tee -a $L/phase2.out
else echo "P2 RESTORE NOT VERIFIED -- sentinel kept" | tee -a $L/phase2.out; fi
cp $L/c_dog.diff $ART/ 2>/dev/null
m=c_dog
python3 -u /tmp/crime_f2.FROZEN.py $B/$m $m > $L/probe_$m.raw 2>&1
[ "$(tail -1 $L/probe_$m.raw)" = CRIMEP_DONE ] && cp $L/probe_$m.raw $ART/
echo "$m $(grep -o 'CRIMEP_RESULT=[0-9/]*' $L/probe_$m.raw) $(grep -o 'CRIMEP_CONTROL=[A-Z]*' $L/probe_$m.raw) [$(tail -1 $L/probe_$m.raw)] | $(grep '^FAILING:' $L/probe_$m.raw)" | tee -a $L/phase2.out
for m in base h_imask h_lbl lt_len lt_addr lt_wset wst_mc c_dog sft; do
  [ -x $B/$m ] || continue
  python3 -u /tmp/crime_f2_rep.FROZEN.py $B/$m $m > $L/rep_$m.raw 2>&1
  [ "$(tail -1 $L/rep_$m.raw)" = F2REP_DONE ] && cp $L/rep_$m.raw $ART/
  echo "REP $m $(grep -o 'F2REP_RESULT=[0-9/]*' $L/rep_$m.raw) [$(tail -1 $L/rep_$m.raw)] | $(grep '^FAILING:' $L/rep_$m.raw)" | tee -a $L/phase2.out
done
echo F2PHASE2_DONE | tee -a $L/phase2.out
cp $L/phase2.out $L/INSTRUMENT2.md5 $ART/
