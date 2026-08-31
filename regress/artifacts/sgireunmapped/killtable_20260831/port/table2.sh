#!/bin/bash
#
#  #499 pass-2 kill table -- the SHIPPED probe, not the artifact detector.
#
#  *** THE SENTINEL GATE IS THE POINT OF THIS DRIVER. ***
#  `killdrivercrash': a driver that scores `grep -c FAIL' without reading the
#  run's exit status or the probe's completion sentinel will score a mutant
#  that died partway through as KILLED or ESCAPED purely by how far it got.
#  table499.sh HAD that defect -- careful about the build, blind to the run.
#  Here every variant must satisfy ALL of:
#      probe process exit status 0
#      exactly one OPUS499T_DONE
#      exactly one OPUS499T_RESULT=
#  and a variant that does not is ABORTED, never scored.
#
#  No `set -e`, and this script does NOT end in a comparison.
set -u
H=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/o499
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
PRISTINE=$SEC/src/devices/dev_sgi_re.c
CLONE=/tmp/gx499
OUT=$H/t2out
mkdir -p $OUT
cd $CLONE

echo "TABLE2 (#499 shipped probe) start $(date +%H:%M:%S)"
echo "baseline: HEAD $(cd $SEC && git rev-parse --short HEAD)  md5 $(md5sum $PRISTINE | cut -d' ' -f1)"
echo "probe   : $H/sgi_re_unmapped_probe.run.py (frozen copy taken before launch)"
echo ""

for V in base fix fix6 m1_tlba m4_bitcollide m5_lina_near mret0 m6_idxshift m7_wintrans; do
  echo "==================================================================="
  echo "VARIANT: $V   $(date +%H:%M:%S)"

  if [ ! -f $CLONE/gxemul.$V ]; then
    echo "$V applied to $CLONE/src/devices/dev_sgi_re.c" > $CLONE/.MUTANT
    python3 $H/mkvariant499.run.py $V $PRISTINE $CLONE/src/devices/dev_sgi_re.c
    if [ $? -ne 0 ]; then echo "  VARIANT GEN FAILED -- ABORT"; exit 1; fi
    rm -f $CLONE/src/devices/dev_sgi_re.o
    make > /tmp/gx499_b2_$V.log 2>&1
    if [ ! -f $CLONE/gxemul ]; then echo "  NO BINARY -- ABORT"; exit 1; fi
    if [ $CLONE/gxemul -nt $CLONE/src/devices/dev_sgi_re.c ]; then
      echo "  build: FRESH ([ binary -nt source ] = YES)"
    else
      echo "  build: STALE -- ABORT"; tail -20 /tmp/gx499_b2_$V.log; exit 1
    fi
    cp $CLONE/gxemul $CLONE/gxemul.$V
  else
    echo "  build: reused from the pass-1 table (md5 $(md5sum $CLONE/gxemul.$V | cut -d' ' -f1))"
  fi

  #  NOT piped: a pipe would report the FILTER's exit status, not the probe's.
  python3 -u $H/sgi_re_unmapped_probe.run.py $CLONE/gxemul.$V $V > $OUT/$V.txt 2>&1
  PRC=$?
  NDONE=$(grep -c '^OPUS499T_DONE$' $OUT/$V.txt)
  NRES=$(grep -c '^OPUS499T_RESULT=' $OUT/$V.txt)
  echo "  PROBE_RC=$PRC  SENTINELS=$NDONE  RESULT_LINES=$NRES"
  if [ "$PRC" -ne 0 ] || [ "$NDONE" -ne 1 ] || [ "$NRES" -ne 1 ]; then
    echo "  *** RUN DID NOT COMPLETE -- NOT SCORED, ABORTING THE TABLE ***"
    echo "  (killdrivercrash: a partial run must never be scored as a result)"
    tail -12 $OUT/$V.txt | sed 's/^/    /'
    exit 1
  fi
  grep -E 'FAIL$' $OUT/$V.txt | sed 's/^/  /'
  grep -E '^OPUS499T_(CONTROL|RESULT)' $OUT/$V.txt | sed 's/^/  /'
done

echo "==================================================================="
echo "=== RESTORE the clone to baseline, REBUILD, and VERIFY ==="
python3 $H/mkvariant499.run.py base $PRISTINE $CLONE/src/devices/dev_sgi_re.c
rm -f $CLONE/src/devices/dev_sgi_re.o
make > /tmp/gx499_b2_restore.log 2>&1
cmp -s $CLONE/src/devices/dev_sgi_re.c $PRISTINE && echo "RESTORE part1 cmp vs SEC: CLEAN" || echo "RESTORE part1: DIFFERS"
if [ $CLONE/gxemul -nt $CLONE/src/devices/dev_sgi_re.c ]; then
  echo "RESTORE part2 binary -nt source: YES"; rm -f $CLONE/.MUTANT
else
  echo "RESTORE part2: NO -- SENTINEL KEPT ON PURPOSE"
fi
echo ""
echo "md5 of every variant binary (any two identical would be a mis-build):"
md5sum $CLONE/gxemul.* | sort | sed 's/^/  /'
echo ""
echo "SENTINEL LEDGER -- score lines against completion sentinels, per variant:"
for V in base fix fix6 m1_tlba m4_bitcollide m5_lina_near mret0 m6_idxshift m7_wintrans; do
  if [ -f $OUT/$V.txt ]; then
    printf '  %-16s scores=%s sentinels=%s  %s\n' "$V" \
      "$(grep -c '^OPUS499T_RESULT=' $OUT/$V.txt)" \
      "$(grep -c '^OPUS499T_DONE$' $OUT/$V.txt)" \
      "$(grep -h '^OPUS499T_RESULT=' $OUT/$V.txt)"
  fi
done
echo "TABLE2_DONE $(date +%H:%M:%S)"
