#!/bin/bash
set -u
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
SRC=$SEC/src/devices/dev_sgi_re.c
OLD=/tmp/gxopus_sgire
CLONE=/tmp/gx499

echo "=== 1. NAME THE BASELINE ==="
echo "  HEAD          : $(cd $SEC && git rev-parse --short HEAD)"
echo "  md5 SEC  file : $(md5sum $SRC | cut -d' ' -f1)"
echo "  md5 OLD clone : $(md5sum $OLD/src/devices/dev_sgi_re.c | cut -d' ' -f1)"

echo
echo "=== 2. cp -a old clone -> $CLONE ==="
rm -rf $CLONE
time cp -a $OLD $CLONE
echo "CLONE created, baseline copy, no mutant applied yet" > $CLONE/.MUTANT
rm -f $CLONE/.STALE $CLONE/gxemul.*

echo
echo "=== 3. install HEAD's dev_sgi_re.c and PROVE the src tree == HEAD ==="
cp $SRC $CLONE/src/devices/dev_sgi_re.c
cmp $CLONE/src/devices/dev_sgi_re.c $SRC && echo "  file under test == HEAD : CLEAN" || echo "  DIFFERS -- STOP"
echo "  full src/ divergence vs SEC (excluding *.o and the crash dumps):"
diff -rq --exclude='*.o' --exclude='grep.exe.stackdump' $CLONE/src $SEC/src 2>&1 | sed 's/^/    /'
echo "  ^^ EXPECT exactly the six declared est-divergence paths from tools/est_divergence.txt"
echo "     (.index Makefile Makefile.skel autodev.c dev_jazz.c dev_ne2000.c machine_arc.c)"
echo "     none of which is reachable from -E sgi -e ip32."

echo
echo "=== 4. BASELINE BUILD in the clone (rm cpus/*.o, conservative) ==="
cd $CLONE
rm -f src/cpus/*.o src/devices/dev_sgi_re.o
time make > /tmp/gx499_build_base.log 2>&1
MAKE_RC=$?
echo "  MAKE_RC=$MAKE_RC   (NOT TRUSTED -- see part 2 below)"
tail -3 /tmp/gx499_build_base.log | sed 's/^/    /'

echo
echo "=== 5. TWO-PART CLEARANCE ==="
cmp -s $CLONE/src/devices/dev_sgi_re.c $SRC && echo "  PART1 source cmp vs SEC : CLEAN" || echo "  PART1 : DIFFERS"
if [ -f $CLONE/gxemul ] && [ $CLONE/gxemul -nt $CLONE/src/devices/dev_sgi_re.c ]; then
  echo "  PART2 [ binary -nt source ] : YES"
else
  echo "  PART2 : NO -- STALE OR MISSING BINARY, ABORT"
fi
ls -la --time-style=+%H:%M:%S $CLONE/gxemul $CLONE/src/devices/dev_sgi_re.c | sed 's/^/    /'
rm -f $CLONE/.MUTANT
echo "SETUP499_DONE"
