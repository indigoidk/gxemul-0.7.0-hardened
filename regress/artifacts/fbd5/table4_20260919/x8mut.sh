#!/bin/bash
R=/mnt/c/DocumentNoSnc/CC/GXEMUL; X=/tmp/fbd5x8
rm -rf $X; mkdir -p $X/regress; cp -a $R/GXEMUL-SEC/src $X/src; cp $R/build/config.h $X/config.h; cp $R/GXEMUL-SEC/regress/diff_footbridge.c $X/regress/
for M in FIX T1 T2; do
  cp $R/GXEMUL-SEC/src/devices/dev_footbridge.c $X/src/devices/dev_footbridge.c
  case $M in
    T1) sed -i 's/\t\t\todata = d->irq_status;$/\t\t\todata = d->irq_status \& 0xff;/' $X/src/devices/dev_footbridge.c ;;
    T2) sed -i 's/odata = d->fiq_status \& d->fiq_enable;/odata = (d->fiq_status \& d->fiq_enable) \& 0xff;/' $X/src/devices/dev_footbridge.c ;;
  esac
  echo "$M edits: $(diff $R/GXEMUL-SEC/src/devices/dev_footbridge.c $X/src/devices/dev_footbridge.c | grep -c '^>')"
  ( cd $X/regress && gcc -O2 -std=c99 -D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE -ffunction-sections -fdata-sections -Wl,--gc-sections -I$X/src -I$X/src/include -I$X/src/include/thirdparty -o $X/d diff_footbridge.c -lm ) || echo COMPILE_FAIL
  $X/d > $X/$M.log 2>&1; echo "$M rc=$? $(grep 'rows, ' $X/$M.log) red: $(grep -E '^  FAIL  [^@]' $X/$M.log | cut -c9-60 | tr '\n' '|')"
done
cp $X/*.log $R/_scratchpad/fbd5/impl/table4/ 2>/dev/null; for f in $X/FIX.log $X/T1.log $X/T2.log; do cp $f $R/_scratchpad/fbd5/impl/table4/x8_$(basename $f); done
