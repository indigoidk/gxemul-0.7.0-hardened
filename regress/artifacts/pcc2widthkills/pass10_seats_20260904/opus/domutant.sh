#!/bin/sh
W=$1
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
CLONE=/tmp/gxopus_p10
OUT=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/pcc2p10_opus
echo "=== SENTINEL FIRST ==="
echo "$W src/devices/dev_pcc2.c TxICR guard conjunct (opus pass10)" > $CLONE/.MUTANT
cat $CLONE/.MUTANT
echo "=== restore from SEC (never from my own backup) then mutate ==="
cp $SEC/src/devices/dev_pcc2.c $CLONE/src/devices/dev_pcc2.c
cmp $CLONE/src/devices/dev_pcc2.c $SEC/src/devices/dev_pcc2.c && echo "PRE_CMP_CLEAN"
python3 $OUT/mutate.py $W || exit 9
echo "=== DIFF COUNT vs SEC (proof of the mutant) ==="
diff $SEC/src/devices/dev_pcc2.c $CLONE/src/devices/dev_pcc2.c > $OUT/$W.diff
echo "DIFF_LINES=$(grep -c '^[<>]' $OUT/$W.diff)"
cat $OUT/$W.diff
echo "=== rebuild ==="
cd $CLONE && rm -f src/devices/dev_pcc2.o && make -j4 > $OUT/${W}_build.log 2>&1
echo "MAKE_RC=$?"
tail -2 $OUT/${W}_build.log
ls -la --time-style=full-iso $CLONE/gxemul $CLONE/src/devices/dev_pcc2.c
if [ $CLONE/gxemul -nt $CLONE/src/devices/dev_pcc2.c ]; then echo "BINARY_NEWER=YES"; else echo "BINARY_NEWER=NO -- ABORT"; exit 8; fi
echo "=== mutant present in the BINARY? (string proof is not available; object mtime + diff is) ==="
echo "OK"
