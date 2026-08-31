#!/bin/bash
#
#  #499 pass-2, table 3 -- the mutants that discharge the PORTED probe's own
#  new rows, plus the oracle-correction order proof.
#
#  Same sentinel gate as table2.sh: a run that does not emit exactly one
#  OPUS499T_DONE with exit status 0 is ABORTED, never scored.
set -u
H=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/o499
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
PRISTINE=$SEC/src/devices/dev_sgi_re.c
CLONE=/tmp/gx499
OUT=$H/t2out
mkdir -p $OUT
cd $CLONE

echo "TABLE3 start $(date +%H:%M:%S)"
echo "baseline: HEAD $(cd $SEC && git rev-parse --short HEAD)  md5 $(md5sum $PRISTINE | cut -d' ' -f1)"
echo ""

for V in mnolatch mbothsame mrdcollide; do
  echo "==================================================================="
  echo "VARIANT: $V   $(date +%H:%M:%S)"
  echo "$V applied to $CLONE/src/devices/dev_sgi_re.c" > $CLONE/.MUTANT
  python3 $H/mkvariant499.run.py $V $PRISTINE $CLONE/src/devices/dev_sgi_re.c
  if [ $? -ne 0 ]; then echo "  VARIANT GEN FAILED -- ABORT"; exit 1; fi
  echo "  edit vs the fix:"
  python3 $H/mkvariant499.run.py fix $PRISTINE /tmp/gx499dry/fix.c 2>/dev/null
  diff -u /tmp/gx499dry/fix.c $CLONE/src/devices/dev_sgi_re.c | grep -E '^[+-][^+-]' | sed 's/^/    /'
  rm -f $CLONE/src/devices/dev_sgi_re.o
  make > /tmp/gx499_b3_$V.log 2>&1
  if [ ! -f $CLONE/gxemul ]; then echo "  NO BINARY -- ABORT"; exit 1; fi
  if [ $CLONE/gxemul -nt $CLONE/src/devices/dev_sgi_re.c ]; then
    echo "  build: FRESH ([ binary -nt source ] = YES)"
  else
    echo "  build: STALE -- ABORT"; tail -20 /tmp/gx499_b3_$V.log; exit 1
  fi
  cp $CLONE/gxemul $CLONE/gxemul.$V

  python3 -u $H/sgi_re_unmapped_probe.run.py $CLONE/gxemul.$V $V > $OUT/$V.txt 2>&1
  PRC=$?
  NDONE=$(grep -c '^OPUS499T_DONE$' $OUT/$V.txt)
  NRES=$(grep -c '^OPUS499T_RESULT=' $OUT/$V.txt)
  echo "  PROBE_RC=$PRC  SENTINELS=$NDONE  RESULT_LINES=$NRES"
  if [ "$PRC" -ne 0 ] || [ "$NDONE" -ne 1 ] || [ "$NRES" -ne 1 ]; then
    echo "  *** RUN DID NOT COMPLETE -- NOT SCORED, ABORTING ***"
    tail -12 $OUT/$V.txt | sed 's/^/    /'
    exit 1
  fi
  grep -E 'FAIL$' $OUT/$V.txt | sed 's/^/  /'
  grep -E '^OPUS499T_(CONTROL|RESULT)' $OUT/$V.txt | sed 's/^/  /'
done

echo "==================================================================="
echo "=== ORACLE-CORRECTION ORDER PROOF for sgi_re_width_probe.py's other kill ==="
echo "The re-pin must be measured RED on the COMMITTED build under the NEW"
echo "expectation BEFORE the code changes, or it is indistinguishable from"
echo "fitting the test to the binary."
for V in base fix; do
  echo "--- $V ---"
  python3 -u $H/repin.run.py $CLONE/gxemul.$V $V 2>&1
done

echo "==================================================================="
echo "=== RESTORE ==="
python3 $H/mkvariant499.run.py base $PRISTINE $CLONE/src/devices/dev_sgi_re.c
rm -f $CLONE/src/devices/dev_sgi_re.o
make > /tmp/gx499_b3_restore.log 2>&1
cmp -s $CLONE/src/devices/dev_sgi_re.c $PRISTINE && echo "RESTORE part1 cmp vs SEC: CLEAN" || echo "RESTORE part1: DIFFERS"
if [ $CLONE/gxemul -nt $CLONE/src/devices/dev_sgi_re.c ]; then
  echo "RESTORE part2 binary -nt source: YES"; rm -f $CLONE/.MUTANT
else
  echo "RESTORE part2: NO -- SENTINEL KEPT ON PURPOSE"
fi
echo ""
echo "SENTINEL LEDGER -- scores against completion sentinels, ALL twelve variants:"
for V in base fix fix6 m1_tlba m4_bitcollide m5_lina_near mret0 m6_idxshift m7_wintrans mnolatch mbothsame mrdcollide; do
  if [ -f $OUT/$V.txt ]; then
    printf '  %-16s scores=%s sentinels=%s  %s\n' "$V" \
      "$(grep -c '^OPUS499T_RESULT=' $OUT/$V.txt)" \
      "$(grep -c '^OPUS499T_DONE$' $OUT/$V.txt)" \
      "$(grep -h '^OPUS499T_RESULT=' $OUT/$V.txt)"
  else
    printf '  %-16s NO LOG\n' "$V"
  fi
done
echo "md5 of every variant binary:"
md5sum $CLONE/gxemul.* | sort | sed 's/^/  /'
echo "TABLE3_DONE $(date +%H:%M:%S)"
