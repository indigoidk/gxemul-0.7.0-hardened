#!/bin/bash
# NOTE: no `set -e' and this script does NOT end in a comparison.
set -u
H=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/o499
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
PRISTINE=$SEC/src/devices/dev_sgi_re.c
CLONE=/tmp/gx499
cd $CLONE

echo "TABLE499 start $(date +%H:%M:%S)"
echo "baseline named: HEAD $(cd $SEC && git rev-parse --short HEAD), md5 $(md5sum $PRISTINE | cut -d' ' -f1)"
echo "driver + generator + detector are FROZEN COPIES (*.run.py) taken before launch"
echo

for V in fix fix6 m1_tlba m2_tlbb m3_tlbc m4_bitcollide; do
  echo "==================================================================="
  echo "VARIANT: $V   $(date +%H:%M:%S)"
  echo "$V applied to $CLONE/src/devices/dev_sgi_re.c" > $CLONE/.MUTANT
  python3 $H/mkvariant499.run.py $V $PRISTINE $CLONE/src/devices/dev_sgi_re.c
  RC=$?
  if [ $RC -ne 0 ]; then echo "  VARIANT GEN FAILED rc=$RC -- ABORT"; exit 1; fi
  echo "  changed lines vs HEAD: $(diff -u $PRISTINE $CLONE/src/devices/dev_sgi_re.c | grep -cE '^[+-][^+-]')"
  rm -f $CLONE/src/devices/dev_sgi_re.o
  make > /tmp/gx499_build_$V.log 2>&1
  if [ ! -f $CLONE/gxemul ]; then echo "  NO BINARY -- ABORT"; exit 1; fi
  if [ $CLONE/gxemul -nt $CLONE/src/devices/dev_sgi_re.c ]; then
      echo "  build: FRESH ([ binary -nt source ] = YES)"
  else
      echo "  build: STALE -- ABORT"; tail -20 /tmp/gx499_build_$V.log; exit 1
  fi
  cp $CLONE/gxemul $CLONE/gxemul.$V
  python3 -u $H/detector.run.py $CLONE/gxemul.$V $V 2>&1
done

echo "==================================================================="
echo "=== RESTORE the clone to baseline, REBUILD, and VERIFY ==="
python3 $H/mkvariant499.run.py base $PRISTINE $CLONE/src/devices/dev_sgi_re.c
rm -f $CLONE/src/devices/dev_sgi_re.o
make > /tmp/gx499_build_restore.log 2>&1
cmp -s $CLONE/src/devices/dev_sgi_re.c $PRISTINE && echo "RESTORE part1 cmp vs SEC: CLEAN" || echo "RESTORE part1: DIFFERS"
if [ $CLONE/gxemul -nt $CLONE/src/devices/dev_sgi_re.c ]; then echo "RESTORE part2 binary -nt source: YES"; else echo "RESTORE part2: NO -- SENTINEL KEPT"; fi
rm -f $CLONE/.MUTANT
echo "md5 of every variant binary (any two identical is a mis-build):"
md5sum $CLONE/gxemul.* | sort
echo "TABLE499_DONE $(date +%H:%M:%S)"
