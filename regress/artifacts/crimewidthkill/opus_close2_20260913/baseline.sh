#!/bin/bash
set -u
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
C=/tmp/gxopus529c2
F=src/devices/dev_sgi_ip32.c
cd "$C" || exit 2
cmp -s "$C/$F" "$SEC/$F" && echo "CMP CLEAN vs SEC" || { echo "CMP DIFF -- ABORT"; exit 3; }
rm -f src/devices/dev_sgi_ip32.o
make -j4 > /tmp/c2_base_build.log 2>&1
echo "make rc=$?"
[ gxemul -nt "$F" ] && echo "gxemul -nt source OK" || echo "gxemul NOT newer WARN"
[ src/devices/dev_sgi_ip32.o -nt "$F" ] && echo "obj -nt source OK" || echo "obj NOT newer WARN"
cp gxemul /tmp/gx529c2_base
md5sum gxemul
# freeze the shipped probe ONCE
cp "$SEC/regress/crime_width_probe.py" /tmp/cwp_close2.py
md5sum /tmp/cwp_close2.py "$SEC/regress/crime_width_probe.py"
echo BASELINE_DONE
