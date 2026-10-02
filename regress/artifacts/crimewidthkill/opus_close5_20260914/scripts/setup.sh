#!/bin/bash
set -e
CLONE=/tmp/gxopuscrimec5
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
WD=/tmp/opuscrimec5
mkdir -p "$WD"
rm -rf "$CLONE"
cp -r /mnt/c/DocumentNoSnc/CC/GXEMUL/build "$CLONE"
cp "$SEC/src/devices/dev_sgi_ip32.c" "$CLONE/src/devices/dev_sgi_ip32.c"
cp "$SEC/src/devices/dev_sgi_ip32.c" "$WD/dev_sgi_ip32.c.orig"
cp "$SEC/regress/crime_width_probe.py" "$WD/probe.py"
if cmp -s "$CLONE/src/devices/dev_sgi_ip32.c" "$SEC/src/devices/dev_sgi_ip32.c"; then echo "CMP CLEAN vs SEC"; else echo "CMP DIFFERS"; exit 1; fi
cd "$CLONE"
find . -name "*.o" -exec touch {} +
sleep 1
rm -f src/cpus/*.o src/devices/dev_sgi_ip32.o gxemul
echo "BUILDING BASE..."
make >"$WD/build_base.log" 2>&1; RC=$?
echo "MAKE_RC=$RC"
if [ -f gxemul ] && [ gxemul -nt src/devices/dev_sgi_ip32.c ]; then echo "BINARY FRESH"; else echo "BINARY STALE/MISSING"; tail -8 "$WD/build_base.log"; exit 1; fi
cp gxemul "$WD/gxemul_base"
ls -la "$WD/gxemul_base"
echo "SETUP_DONE"
