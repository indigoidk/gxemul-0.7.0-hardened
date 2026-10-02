#!/bin/bash
# #529 F2 Opus seat kill table.  Phase 1: build every mutant in the scratch clone (clone-local sentinel), copy the
# binaries out, restore the clone from GXEMUL-SEC, rebuild, verify cmp clean + binary -nt source + restored == base,
# remove the sentinel.  Phase 2: run the FROZEN 71-row detector and the FROZEN obs probe on each binary, ONE AT A TIME.
# Phase 3: the TIME rows' margin, 10 repeats of the `time lb' session on base.  Every log copied to the durable
# artifacts dir as soon as it ends with its sentinel.  Launched from a frozen copy of this script.
set -u
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
ART=$SEC/regress/artifacts/crimewidthkill/opus_f2_20260913/logs
C=/tmp/gxopus529f2
F=src/devices/dev_sgi_ip32.c
L=/tmp/f2logs
B=/tmp/f2bins
MUTS="${MUTS:-a_lo10 a_imask h_imask h_lbl lt_len lt_addr lt_wset l_brace sft wst_mc}"
mkdir -p $ART $L $B
cd $C || exit 9
[ -e .MUTANT ] && { echo "SENTINEL PRESENT at start -- abort"; cat .MUTANT; exit 8; }
cmp -s $F $SEC/$F && echo "BASELINE_CMP CLEAN" | tee $L/table.out || { echo "BASELINE_CMP DIFFERS -- abort" | tee $L/table.out; exit 8; }
[ -x $B/base ] || { echo "no base binary -- abort"; exit 8; }
cp $SEC/$F /tmp/f2_orig_dev_sgi_ip32.c
echo "$F -- #529 F2 Opus seat mutant table; restore from GXEMUL-SEC" > .MUTANT
for m in $MUTS; do
  python3 /tmp/mutants_f2.FROZEN.py $m /tmp/f2_orig_dev_sgi_ip32.c $F > $L/$m.apply 2>&1 || { echo "$m APPLY_FAILED $(cat $L/$m.apply)" | tee -a $L/table.out; continue; }
  diff -u /tmp/f2_orig_dev_sgi_ip32.c $F > $L/$m.diff
  rm -f src/devices/dev_sgi_ip32.o gxemul
  make -j4 > $L/$m.build 2>&1; rc=$?
  if [ $rc -ne 0 ] || [ ! -e gxemul ] || ! [ gxemul -nt $F ] || ! [ src/devices/dev_sgi_ip32.o -nt $F ]; then
    echo "$m BUILD_FAILED rc=$rc" | tee -a $L/table.out; tail -5 $L/$m.build; continue; fi
  cp gxemul $B/$m
  cmp -s $B/$m $B/base && echo "$m NOTE binary byte-identical to base" | tee -a $L/table.out
  echo "$m BUILD_OK" | tee -a $L/table.out
done
echo "== restore" | tee -a $L/table.out
cp $SEC/$F $F
rm -f src/devices/dev_sgi_ip32.o gxemul
make -j4 > $L/restore.build 2>&1
if cmp -s $F $SEC/$F && [ gxemul -nt $F ] && [ src/devices/dev_sgi_ip32.o -nt $F ]; then
  cmp -s gxemul $B/base && echo "RESTORED: cmp clean, binary -nt source, restored == base byte-identical" | tee -a $L/table.out
  rm -f .MUTANT && echo "SENTINEL REMOVED" | tee -a $L/table.out
else
  echo "RESTORE NOT VERIFIED -- sentinel kept" | tee -a $L/table.out
fi
cp $L/*.diff $L/table.out $ART/ 2>/dev/null
for m in base $MUTS; do
  [ -x $B/$m ] || continue
  python3 -u /tmp/crime_f2.FROZEN.py $B/$m $m > $L/probe_$m.raw 2>&1
  [ "$(tail -1 $L/probe_$m.raw)" = CRIMEP_DONE ] && cp $L/probe_$m.raw $ART/
  python3 -u /tmp/crime_f2_obs.FROZEN.py $B/$m $m > $L/obs_$m.raw 2>&1
  [ "$(tail -1 $L/obs_$m.raw)" = F2OBS_DONE ] && cp $L/obs_$m.raw $ART/
  r=$(grep -o 'CRIMEP_RESULT=[0-9/]*' $L/probe_$m.raw); ct=$(grep -o 'CRIMEP_CONTROL=[A-Z]*' $L/probe_$m.raw)
  fl=$(grep '^FAILING:' $L/probe_$m.raw); s1=$(tail -1 $L/probe_$m.raw)
  e=$(grep -o 'F2OBS_RESULT=[0-9/]*' $L/obs_$m.raw); ed=$(grep '^DIFFS:' $L/obs_$m.raw); s2=$(tail -1 $L/obs_$m.raw)
  echo "$m  $r $ct [$s1] | $fl || $e [$s2] | $ed" | tee -a $L/table.out
  cp $L/table.out $ART/
done
python3 -u /tmp/crime_f2_obs.FROZEN.py $B/base base timing10 > $L/timing_base.raw 2>&1
[ "$(tail -1 $L/timing_base.raw)" = F2OBS_DONE ] && cp $L/timing_base.raw $ART/
grep '^TIMING' $L/timing_base.raw | tee -a $L/table.out
echo F2TABLE_DONE | tee -a $L/table.out
cp $L/table.out $ART/
