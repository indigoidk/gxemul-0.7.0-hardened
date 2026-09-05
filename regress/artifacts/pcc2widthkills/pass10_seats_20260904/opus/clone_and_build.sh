#!/bin/sh
set -x
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
CLONE=/tmp/gxopus_p10
OUT=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/pcc2p10_opus

echo "=== STEP 0: pre-existing clone check ==="
ls -la $CLONE 2>/dev/null | head -3
rm -rf $CLONE
echo "=== STEP 1: cp -a build -> clone ==="
cp -a /mnt/c/DocumentNoSnc/CC/GXEMUL/build $CLONE
echo "cp rc=$?"
echo "=== STEP 2: cmp dev_pcc2.c clone vs SEC ==="
cmp $CLONE/src/devices/dev_pcc2.c $SEC/src/devices/dev_pcc2.c
echo "CMP_PCC2_RC=$?"
md5sum $CLONE/src/devices/dev_pcc2.c $SEC/src/devices/dev_pcc2.c
echo "=== STEP 2b: any .MUTANT sentinel in the source build tree? ==="
ls -la /mnt/c/DocumentNoSnc/CC/GXEMUL/build/.MUTANT 2>&1
ls -la $CLONE/.MUTANT 2>&1
echo "=== STEP 3: rm object, rebuild ==="
cd $CLONE
rm -f src/devices/dev_pcc2.o
make -j4 > $OUT/base_build.log 2>&1
echo "MAKE_RC=$?"
tail -5 $OUT/base_build.log
echo "=== STEP 4: freshness ==="
ls -la --time-style=full-iso $CLONE/gxemul $CLONE/src/devices/dev_pcc2.c
if [ $CLONE/gxemul -nt $CLONE/src/devices/dev_pcc2.c ]; then echo "BINARY_NEWER=YES"; else echo "BINARY_NEWER=NO"; fi
$CLONE/gxemul -V 2>&1 | head -2
echo "=== DONE ==="
