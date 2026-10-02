#!/bin/bash
# #529 F2 Opus seat: scratch clone, baseline cmp vs SEC, freeze the probe + obs probe, rebuild baseline in the clone,
# then run the obs probe once on base (apparatus check).
set -u
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
SRC=/tmp/gxopuscrime
C=/tmp/gxopus529f2
F=src/devices/dev_sgi_ip32.c
L=/tmp/f2logs
if [ -e $C ]; then echo "CLONE EXISTS ALREADY -- abort"; exit 3; fi
[ -e $SRC/.MUTANT ] && { echo "SOURCE CLONE HAS A SENTINEL -- abort"; exit 3; }
cp -a $SRC $C || exit 4
mkdir -p $L /tmp/f2bins
cmp $C/$F $SEC/$F && echo BASELINE_CMP_CLEAN || { echo BASELINE_CMP_DIFFERS; exit 5; }
md5sum $C/$F $SEC/$F
cp $SEC/regress/crime_width_probe.py /tmp/crime_f2.FROZEN.py
cp $SP/crime_f2_obs.py /tmp/crime_f2_obs.FROZEN.py
cp $SP/mutants_f2.py /tmp/mutants_f2.FROZEN.py
md5sum /tmp/crime_f2.FROZEN.py $SEC/regress/crime_width_probe.py /tmp/crime_f2_obs.FROZEN.py /tmp/mutants_f2.FROZEN.py | tee $L/INSTRUMENT.md5
cd $C || exit 6
rm -f src/devices/dev_sgi_ip32.o
make -j4 > $L/build_base.log 2>&1; echo MAKE_RC=$?
if [ gxemul -nt $F ] && [ src/devices/dev_sgi_ip32.o -nt $F ]; then echo FRESH_BINARY; else echo STALE_BINARY; exit 7; fi
cp gxemul /tmp/f2bins/base
cmp -s /tmp/f2bins/base $SRC/gxemul && echo "base == /tmp/gxopuscrime/gxemul (byte-identical)" || echo "base differs from /tmp/gxopuscrime/gxemul"
python3 -u /tmp/crime_f2_obs.FROZEN.py /tmp/f2bins/base base > $L/obs_base.raw 2>&1
tail -3 $L/obs_base.raw
echo SETUP_DONE
