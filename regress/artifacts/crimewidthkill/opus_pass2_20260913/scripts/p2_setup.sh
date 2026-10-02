#!/bin/bash
# pass-2 Opus seat: create scratch clone, verify baseline, freeze probe, rebuild baseline
set -u
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
SRC=/tmp/gxopuscrime
C=/tmp/gxopus529p2
ART=$SEC/regress/artifacts/crimewidthkill/opus_pass2_20260913
echo "== source tree state"
ls -la $SRC/gxemul $SRC/src/devices/dev_sgi_ip32.c $SRC/.MUTANT 2>&1
if [ -e $C ]; then echo "CLONE EXISTS ALREADY"; ls -la $C | head; exit 3; fi
cp -a $SRC $C || exit 4
echo "== baseline cmp vs SEC"
cmp $C/src/devices/dev_sgi_ip32.c $SEC/src/devices/dev_sgi_ip32.c && echo BASELINE_CMP_CLEAN || echo BASELINE_CMP_DIFFERS
md5sum $C/src/devices/dev_sgi_ip32.c $SEC/src/devices/dev_sgi_ip32.c
cp $SEC/regress/crime_width_probe.py /tmp/crime_p2.FROZEN.py
md5sum /tmp/crime_p2.FROZEN.py $SEC/regress/crime_width_probe.py
mkdir -p $ART
echo "== rebuild baseline in clone"
cd $C && rm -f src/devices/dev_sgi_ip32.o && make -j4 > /tmp/p2_build_base.log 2>&1; echo MAKE_RC=$?
tail -3 /tmp/p2_build_base.log
if [ gxemul -nt src/devices/dev_sgi_ip32.c ] && [ -e src/devices/dev_sgi_ip32.o ]; then echo FRESH_BINARY; else echo STALE_BINARY; fi
mkdir -p /tmp/p2bins && cp gxemul /tmp/p2bins/base && ls -la /tmp/p2bins
echo SETUP_DONE
