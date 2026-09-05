#!/bin/bash
T=/tmp/gxopus_p5
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
cp "$SEC/src/devices/dev_pcc2.c" "$T/src/devices/dev_pcc2.c" || exit 9
cmp -s "$T/src/devices/dev_pcc2.c" "$SEC/src/devices/dev_pcc2.c" && echo "RESTORE CMP CLEAN vs SEC" || { echo "RESTORE CMP FAILED"; exit 9; }
cd "$T" || exit 9
rm -f src/devices/dev_pcc2.o
make -j4 > "$T/restore_build.log" 2>&1
echo "MAKE_RC=$?"
if [ "$T/gxemul" -nt "$T/src/devices/dev_pcc2.c" ]; then
    echo "PART2 FRESH -- clearing sentinel"
    cp "$T/gxemul" /tmp/gxopus_p5_BASE_bin
    rm -f "$T/.MUTANT"
    ls /tmp/gxopus_p5/.MUTANT 2>/dev/null || echo "SENTINEL CLEARED"
else
    echo "PART2 STALE -- SENTINEL KEPT"
fi
