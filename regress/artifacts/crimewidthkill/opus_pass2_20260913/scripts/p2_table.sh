#!/bin/bash
# #529 pass-2 Opus seat kill table: build each mutant in the scratch clone, run the FROZEN detector and the
# FROZEN escape probe against it.  Clone-local sentinel; restore verified by cmp against GXEMUL-SEC + rebuild.
set -u
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
C=/tmp/gxopus529p2
F=src/devices/dev_sgi_ip32.c
L=/tmp/p2logs
MUTS="${MUTS:-$(python3 $SP/mutants_p2.py list x y)}"
mkdir -p $L /tmp/p2bins
cp $SP/mutants_p2.py /tmp/mutants_p2.FROZEN.py
md5sum /tmp/crime_p2.FROZEN.py /tmp/crime_p2_escape.FROZEN.py /tmp/mutants_p2.FROZEN.py > $L/INSTRUMENT.md5
cd $C || exit 9
cmp -s $F $SEC/$F && echo "BASELINE_CMP CLEAN" | tee $L/table.out || { echo "BASELINE_CMP DIFFERS -- abort" | tee $L/table.out; exit 8; }
cp $SEC/$F /tmp/p2_orig_dev_sgi_ip32.c
for m in $MUTS; do
  echo "$F mutant $m (opus pass2)" > $C/.MUTANT
  python3 /tmp/mutants_p2.FROZEN.py $m /tmp/p2_orig_dev_sgi_ip32.c $F > $L/$m.apply 2>&1 || { echo "$m APPLY_FAILED $(cat $L/$m.apply)" | tee -a $L/table.out; continue; }
  diff -u /tmp/p2_orig_dev_sgi_ip32.c $F > $L/$m.diff
  rm -f src/devices/dev_sgi_ip32.o gxemul
  make -j4 > $L/$m.build 2>&1; rc=$?
  if [ $rc -ne 0 ] || [ ! -e gxemul ] || ! [ gxemul -nt $F ]; then echo "$m BUILD_FAILED rc=$rc" | tee -a $L/table.out; continue; fi
  cp gxemul /tmp/p2bins/$m
  cmp -s /tmp/p2bins/$m /tmp/p2bins/base && echo "$m NOTE binary byte-identical to base" | tee -a $L/table.out
  python3 -u /tmp/crime_p2.FROZEN.py /tmp/p2bins/$m $m > $L/probe_$m.raw 2>&1
  python3 -u /tmp/crime_p2_escape.FROZEN.py /tmp/p2bins/$m $m > $L/esc_$m.raw 2>&1
  r=$(grep -o 'CRIMEP_RESULT=[0-9/]*' $L/probe_$m.raw); ct=$(grep -o 'CRIMEP_CONTROL=[A-Z]*' $L/probe_$m.raw)
  fl=$(grep '^FAILING:' $L/probe_$m.raw); s1=$(tail -1 $L/probe_$m.raw)
  e=$(grep -o 'P2ESC_RESULT=[0-9/]*' $L/esc_$m.raw); ed=$(grep '^DIFFS:' $L/esc_$m.raw); s2=$(tail -1 $L/esc_$m.raw)
  echo "$m  $r $ct [$s1] | $fl || $e [$s2] | $ed" | tee -a $L/table.out
done
echo "== restore"
cp $SEC/$F $F
cmp -s $F $SEC/$F && echo "RESTORE_CMP CLEAN" | tee -a $L/table.out
rm -f src/devices/dev_sgi_ip32.o gxemul
make -j4 > $L/restore.build 2>&1
if [ gxemul -nt $F ] && cmp -s $F $SEC/$F; then
  cmp -s gxemul /tmp/p2bins/base && echo "RESTORED_BINARY == base byte-identical" | tee -a $L/table.out
  rm -f $C/.MUTANT; echo "SENTINEL REMOVED" | tee -a $L/table.out
else
  echo "RESTORE NOT VERIFIED -- sentinel kept" | tee -a $L/table.out
fi
echo P2TABLE_DONE | tee -a $L/table.out
