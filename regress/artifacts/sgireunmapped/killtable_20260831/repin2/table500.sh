#!/bin/bash
#
#  #499 re-pin measurement.  Three variants, two oracles, one shipped probe.
#  Same sentinel gate as the round's earlier tables: a run that does not emit
#  exactly one completion sentinel with rc 0 is ABORTED, never scored.
set -u
H=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/o500r
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
PRISTINE=$SEC/src/devices/dev_sgi_re.c
CLONE=/tmp/gx500r
OUT=$H/out
mkdir -p $OUT $CLONE/dry
cd $CLONE

echo "TABLE500 start $(date +%H:%M:%S)"
echo "BASELINE NAMED: HEAD $(cd $SEC && git rev-parse --short HEAD)"
echo "  dev_sgi_re.c md5 $(md5sum $PRISTINE | cut -d' ' -f1)"
echo "  sgi_re_width_probe.py md5 $(md5sum $SEC/regress/sgi_re_width_probe.py | cut -d' ' -f1)"
echo "  clone source cmp vs SEC before mutant 1: $(cmp -s $CLONE/src/devices/dev_sgi_re.c $PRISTINE && echo CLEAN || echo DIFFERS)"
echo ""

python3 $H/mk500.run.py base $PRISTINE $CLONE/dry/base.c >/dev/null 2>&1

for V in base fix mexit0; do
  echo "==================================================================="
  echo "VARIANT: $V   $(date +%H:%M:%S)"
  echo "$V applied to $CLONE/src/devices/dev_sgi_re.c" > $CLONE/.MUTANT
  python3 $H/mk500.run.py $V $PRISTINE $CLONE/src/devices/dev_sgi_re.c
  if [ $? -ne 0 ]; then echo "  VARIANT GEN FAILED -- ABORT"; exit 1; fi
  echo "  source md5: $(md5sum $CLONE/src/devices/dev_sgi_re.c | cut -d' ' -f1)"
  echo "  edit vs base:"
  diff -u $CLONE/dry/base.c $CLONE/src/devices/dev_sgi_re.c | grep -E '^[+-][^+-]' | sed 's/^/    /' | head -40
  echo "    (changed lines: $(diff -u $CLONE/dry/base.c $CLONE/src/devices/dev_sgi_re.c | grep -cE '^[+-][^+-]'))"
  rm -f $CLONE/src/devices/dev_sgi_re.o
  make -j8 > /tmp/gx500r_b_$V.log 2>&1
  if [ ! -f $CLONE/gxemul ]; then echo "  NO BINARY -- ABORT"; tail -20 /tmp/gx500r_b_$V.log; exit 1; fi
  if [ $CLONE/gxemul -nt $CLONE/src/devices/dev_sgi_re.c ]; then
    echo "  build: FRESH ([ binary -nt source ] = YES)"
  else
    echo "  build: STALE -- ABORT"; tail -20 /tmp/gx500r_b_$V.log; exit 1
  fi
  cp $CLONE/gxemul $CLONE/gxemul.$V

  echo "  --- the two oracles ---"
  python3 -u $H/score500.run.py $CLONE/gxemul.$V $V > $OUT/oracle_$V.txt 2>&1
  ORC=$?
  ND=$(grep -c '^SCORE500_DONE$' $OUT/oracle_$V.txt)
  echo "  ORACLE_RC=$ORC  SENTINELS=$ND"
  if [ "$ORC" -ne 0 ] || [ "$ND" -ne 1 ]; then
    echo "  *** ORACLE RUN DID NOT COMPLETE -- NOT SCORED, ABORTING ***"
    tail -15 $OUT/oracle_$V.txt | sed 's/^/    /'; exit 1
  fi
  sed -n '3,$p' $OUT/oracle_$V.txt | sed 's/^/  /'

  echo "  --- the SHIPPED 35-row probe, unmodified ---"
  python3 -u $H/sgi_re_width_probe.run.py $CLONE/gxemul.$V $V > $OUT/probe_$V.txt 2>&1
  PRC=$?
  NDONE=$(grep -c '^OPUS497T_DONE$' $OUT/probe_$V.txt)
  NRES=$(grep -c '^OPUS497T_RESULT=' $OUT/probe_$V.txt)
  echo "  PROBE_RC=$PRC  SENTINELS=$NDONE  RESULT_LINES=$NRES"
  if [ "$PRC" -ne 0 ] || [ "$NDONE" -ne 1 ] || [ "$NRES" -ne 1 ]; then
    echo "  *** PROBE RUN DID NOT COMPLETE -- NOT SCORED, ABORTING ***"
    tail -12 $OUT/probe_$V.txt | sed 's/^/    /'; exit 1
  fi
  grep -E 'FAIL$' $OUT/probe_$V.txt | sed 's/^/    /'
  grep -E '^OPUS497T_(CONTROL|RESULT)' $OUT/probe_$V.txt | sed 's/^/    /'
  echo "    rows emitted = $(( $(grep -c ' ok$' $OUT/probe_$V.txt) + $(grep -c ' FAIL$' $OUT/probe_$V.txt) ))  green = $(grep -c ' ok$' $OUT/probe_$V.txt)  red = $(grep -c ' FAIL$' $OUT/probe_$V.txt)"
  echo ""
done

echo "==================================================================="
echo "=== RESTORE (two-part clearance) ==="
python3 $H/mk500.run.py base $PRISTINE $CLONE/src/devices/dev_sgi_re.c
rm -f $CLONE/src/devices/dev_sgi_re.o
make -j8 > /tmp/gx500r_restore.log 2>&1
if cmp -s $CLONE/src/devices/dev_sgi_re.c $PRISTINE; then
  echo "RESTORE part1 cmp vs SEC (never vs my own backup): CLEAN"
  P1=ok
else
  echo "RESTORE part1: DIFFERS"; P1=bad
fi
if [ $CLONE/gxemul -nt $CLONE/src/devices/dev_sgi_re.c ]; then
  echo "RESTORE part2 [ binary -nt source ]: YES"
  P2=ok
else
  echo "RESTORE part2: NO"; P2=bad
fi
if [ "$P1" = ok ] && [ "$P2" = ok ]; then
  rm -f $CLONE/.MUTANT; echo "SENTINEL CLEARED (both parts passed)"
else
  echo "SENTINEL KEPT ON PURPOSE (clearance incomplete)"
fi
echo ""
echo "SENTINEL LEDGER:"
for V in base fix mexit0; do
  printf '  %-8s oracle_sentinels=%s  probe_sentinels=%s  %s\n' "$V" \
    "$(grep -c '^SCORE500_DONE$' $OUT/oracle_$V.txt 2>/dev/null)" \
    "$(grep -c '^OPUS497T_DONE$' $OUT/probe_$V.txt 2>/dev/null)" \
    "$(grep -h '^OPUS497T_RESULT=' $OUT/probe_$V.txt 2>/dev/null)"
done
echo "md5 of every variant binary:"
md5sum $CLONE/gxemul.* | sort | sed 's/^/  /'
echo "TABLE500_DONE $(date +%H:%M:%S)"
