#!/bin/bash
T=/tmp/gxopus_p5
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
cd "$T" || exit 9
cmp -s src/devices/dev_pcc2.c "$SEC/src/devices/dev_pcc2.c" && echo "PART1 BASELINE CMP CLEAN" || { echo "PART1 FAIL"; exit 9; }
rm -f src/devices/dev_pcc2.o
make -j4 > "$T/base_build.log" 2>&1
echo "MAKE_RC=$?"
ls -la "$T/gxemul" "$T/src/devices/dev_pcc2.c"
if [ "$T/gxemul" -nt "$T/src/devices/dev_pcc2.c" ]; then echo "PART2 FRESH"; else echo "PART2 STALE"; fi
tail -3 "$T/base_build.log"
