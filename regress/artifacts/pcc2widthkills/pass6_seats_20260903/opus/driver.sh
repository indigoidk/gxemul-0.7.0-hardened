#!/bin/bash
#  pcc2widthkills PASS 6, Opus seat.  Scratch clone /tmp/gxopus_p6 ONLY.
#  BASELINE: GXEMUL-SEC working tree (uncommitted repair on b78bb0f), md5 294222357ca13dfe632edbcfeb421ad6
T=/tmp/gxopus_p6
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
OUT=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/pcc2p6_opus/table
PROBE=$OUT/frozen_probe.py
MUT=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/pcc2p6_opus/mutate.py
cd $T || exit 9

run () {   # $1 = label
  rm -f src/devices/dev_pcc2.o
  make -j4 > $OUT/build_$1.log 2>&1
  rc=$?
  echo "[$1] MAKE_RC=$rc" >> $OUT/driver.log
  if ! [ gxemul -nt src/devices/dev_pcc2.c ]; then echo "[$1] STALE BINARY -- ABORT" >> $OUT/driver.log; return 1; fi
  echo "[$1] binary $(date -r gxemul +%H:%M:%S) source $(date -r src/devices/dev_pcc2.c +%H:%M:%S)" >> $OUT/driver.log
  python3 -u $PROBE $T/gxemul $1 > $OUT/probe_$1.out 2>&1
  g=$(grep -c ' ok$' $OUT/probe_$1.out)
  f=$(grep -c ' FAIL$' $OUT/probe_$1.out)
  echo "[$1] $g/$((g+f))  reds: $(grep ' FAIL$' $OUT/probe_$1.out | cut -c1-16 | tr -s ' ' | tr '\n' ',')" >> $OUT/driver.log
  tail -1 $OUT/probe_$1.out >> $OUT/driver.log
}

restore () {
  cp -p /tmp/gxopus_p6_pcc2_ORIG.c src/devices/dev_pcc2.c
  if cmp -s src/devices/dev_pcc2.c $SEC/src/devices/dev_pcc2.c; then
     echo "RESTORE: cmp vs SEC CLEAN" >> $OUT/driver.log
  else
     echo "RESTORE: cmp vs SEC DIFFERS -- SENTINEL KEPT" >> $OUT/driver.log; return 1
  fi
}

: > $OUT/driver.log
echo "clone $T  baseline md5 $(md5sum src/devices/dev_pcc2.c | cut -d' ' -f1)" >> $OUT/driver.log
echo "probe frozen md5 $(md5sum $PROBE | cut -d' ' -f1)" >> $OUT/driver.log

run BASE

for M in M1_W4FALL_ALL M2_PENDT_TXICR M3_DELGUARD_GENCTL; do
  echo "$M in progress" > $T/.MUTANT
  restore
  code=${M%%_*}
  python3 $MUT $code >> $OUT/driver.log 2>&1 || { echo "$M MUTATE FAILED" >> $OUT/driver.log; continue; }
  grep -c 'if (len < 4) break;' src/devices/dev_pcc2.c >> $OUT/driver.log
  grep -c 'pending_timer1_interrupts == 0' src/devices/dev_pcc2.c >> $OUT/driver.log
  grep -c 'PCC2_W_GENCTL_LEN' src/devices/dev_pcc2.c >> $OUT/driver.log
  run $M
done

restore
rm -f src/devices/dev_pcc2.o
make -j4 > $OUT/build_RESTORE.log 2>&1
echo "RESTORE MAKE_RC=$?" >> $OUT/driver.log
if cmp -s src/devices/dev_pcc2.c $SEC/src/devices/dev_pcc2.c; then rm -f $T/.MUTANT; echo "SENTINEL CLEARED" >> $OUT/driver.log; fi
echo "TABLE_DONE" >> $OUT/driver.log
