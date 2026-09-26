#!/bin/bash
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus551p1
W=/tmp/opus551p1
R=$SP/results; rm -rf $R; mkdir -p $R/logs $R/harness
python3 $SP/xform.py census $W/sec/regress/diff_wdc_identify.c > $R/census.txt
python3 $SP/analyze.py > $R/analyze.txt 2>&1
cp $W/h/A.c $W/h/Ahard.c $W/h/ORIGF.c $W/h/AF.c $R/harness/
for dev in pristine selfmut rev255 cyl13 srstbit; do
  for h in ORIG.O2 A.O2 Ahard.O2 E_eq1.O2 E_uchar.O2 E_rows_h.O2 E_noret.O2 E_after3.O2 E_eq1c.O2; do
    [ -f $W/dev/$dev/regress/$h.log ] && cp $W/dev/$dev/regress/$h.log $R/logs/$dev.$h.log
  done
done
cp $W/dev/pristine/regress/Abad.O2.cc $R/logs/Abad.O2.cc
cp $W/dev/pristine/regress/../../../dev/pristine/regress/ORIG.O0.cc $R/logs/ORIG.O0.cc 2>/dev/null
cp /tmp/opus551p1/dev/pristine/regress/smoke_O0.cc $R/logs/gateflags_O0_link.cc 2>/dev/null
tar -C $W -czf $R/force_logs.tgz force
ls -la $R $R/logs | head -60; du -sh $R
