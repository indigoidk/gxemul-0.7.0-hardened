#!/bin/bash
set -u
H=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/o499
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
PRISTINE=$SEC/src/devices/dev_sgi_re.c
CLONE=/tmp/gx499
cd $CLONE
V=m5_lina_near
echo "M5 -- the ACCEPT-SIDE BLIND SPOT, measured rather than argued."
echo "PREDICTION written before the build: 14/14 CLEAN SWEEP (total escape)."
echo "$V applied to $CLONE/src/devices/dev_sgi_re.c" > $CLONE/.MUTANT
python3 $H/mkvariant499.run.py $V $PRISTINE $CLONE/src/devices/dev_sgi_re.c || exit 1
python3 $H/mkvariant499.run.py fix $PRISTINE /tmp/gx499dry/fix.c
echo "--- the edit (fix -> $V) ---"
diff -u /tmp/gx499dry/fix.c $CLONE/src/devices/dev_sgi_re.c | grep -E '^[+-][^+-]'
rm -f $CLONE/src/devices/dev_sgi_re.o
make > /tmp/gx499_build_$V.log 2>&1
if [ $CLONE/gxemul -nt $CLONE/src/devices/dev_sgi_re.c ]; then echo "  build: FRESH"; else echo "  build STALE -- ABORT"; exit 1; fi
cp $CLONE/gxemul $CLONE/gxemul.$V
python3 -u $H/detector.run.py $CLONE/gxemul.$V $V 2>&1
echo "--- and the CONTROL: is the defect real?  probe 0x1700, the window BASE ---"
python3 -u $H/base_slot_probe.py $CLONE/gxemul.$V $V 2>&1
python3 -u $H/base_slot_probe.py $CLONE/gxemul.fix fix 2>&1
echo "=== RESTORE ==="
python3 $H/mkvariant499.run.py base $PRISTINE $CLONE/src/devices/dev_sgi_re.c
rm -f $CLONE/src/devices/dev_sgi_re.o
make > /tmp/gx499_build_restore2.log 2>&1
cmp -s $CLONE/src/devices/dev_sgi_re.c $PRISTINE && echo "RESTORE part1: CLEAN" || echo "RESTORE part1: DIFFERS"
[ $CLONE/gxemul -nt $CLONE/src/devices/dev_sgi_re.c ] && echo "RESTORE part2: YES" || echo "RESTORE part2: NO -- SENTINEL KEPT"
rm -f $CLONE/.MUTANT
echo "M5_DONE $(date +%H:%M:%S)"
