#!/bin/bash
# opus5 late seat, wdcrearmzero: extract three revisions into a PRIVATE WSL scratch
# (/tmp/gxopuswdc) and build each revision's offline detector unmodified (the baseline).
# Writes nothing under any project tree.
set -u
S=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opuswdc
mkdir -p /tmp/gxopuswdc && cd /tmp/gxopuswdc || exit 9
for r in HEAD 1f1a02b d894e35d; do tar -xf "$S/t_$r.tar"; cp "$S/config.h" "t_$r/config.h"; done
ls
for r in HEAD 1f1a02b d894e35d; do
  cd /tmp/gxopuswdc/t_$r/regress || exit 8
  if gcc -O2 -std=c99 -I../src/include -I../src/include/thirdparty \
       -ffunction-sections -fdata-sections -Wl,--gc-sections \
       -o base diff_wdc_identify.c > build.log 2>&1; then
     ./base > base.out 2>base.err
     rc=$?
     echo "$r rc=$rc :: $(grep -E '^[0-9]+ rows' base.out) :: $(grep -c WDC_IDENTIFY_PASS base.out) pass"
  else
     echo "$r BUILD FAILED"; head -20 build.log
  fi
done
echo SETUP_BASE_DONE
