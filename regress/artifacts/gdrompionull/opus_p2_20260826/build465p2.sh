#!/bin/bash
# OPUS 465 PASS-2 SEAT: build a SCRATCH COPY.  NEVER writes to GXEMUL-SEC.
set -u
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
T=/tmp/gx465p2
LOG=/mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/p465

rm -rf "$T"
mkdir -p "$T"
cp -a "$SEC"/. "$T"/ 2>/dev/null
echo "opus5 pass-2 seat scratch copy of GXEMUL-SEC @ $(date)" > "$T/.SCRATCH_COPY"
cd "$T" || exit 9
rm -rf .git
./configure > "$LOG/conf.log" 2>&1
rm -f src/cpus/*.o
make -j8 > "$LOG/make_base.log" 2>&1
RC=$?
echo "MAKE_RC=$RC"
ls -la "$T/gxemul" 2>/dev/null
if [ -f "$T/gxemul" ] && [ "$T/gxemul" -nt "$T/src/devices/dev_dreamcast_gdrom.c" ]; then
    echo "BINARY_FRESH=yes"
else
    echo "BINARY_FRESH=NO"
fi
