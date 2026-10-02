#!/bin/bash
# make the scratch clone from build/ (fixed source), verify identity vs SEC, build baseline
set -u
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
SRCTREE=/mnt/c/DocumentNoSnc/CC/GXEMUL/build
C=/tmp/gxopus529c2
F=src/devices/dev_sgi_ip32.c
OUT=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_close2

rm -rf "$C"
cp -a "$SRCTREE" "$C"
cd "$C" || exit 2
echo "BASELINE_CMP:"; cmp "$C/$F" "$SEC/$F" && echo "  CMP CLEAN vs SEC" || { echo "  CMP DIFFERS -- ABORT"; exit 3; }
md5sum "$C/$F" "$SEC/$F"
# fresh baseline build
rm -f src/devices/dev_sgi_ip32.o
make -j4 > "$OUT/logs/base_build.log" 2>&1; rc=$?
echo "make rc=$rc"
if [ $rc -ne 0 ]; then tail -20 "$OUT/logs/base_build.log"; echo BUILD_FAIL; exit 4; fi
[ gxemul -nt "$F" ] && echo "gxemul -nt source OK" || echo "gxemul NOT newer -- WARN"
[ src/devices/dev_sgi_ip32.o -nt "$F" ] && echo "obj -nt source OK" || echo "obj NOT newer -- WARN"
cp gxemul /tmp/gx529c2_base
md5sum gxemul
echo SETUP_DONE
