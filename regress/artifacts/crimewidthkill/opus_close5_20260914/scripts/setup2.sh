#!/bin/bash
set -e
CLONE=/tmp/gxopuscrimec5b
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
WD=/tmp/opuscrimec5
mkdir -p "$WD"
rm -rf "$CLONE"
cp -r /mnt/c/DocumentNoSnc/CC/GXEMUL/build "$CLONE"
cp "$SEC/src/devices/dev_sgi_ip32.c" "$CLONE/src/devices/dev_sgi_ip32.c"
if cmp -s "$CLONE/src/devices/dev_sgi_ip32.c" "$SEC/src/devices/dev_sgi_ip32.c"; then echo "CMP CLEAN vs SEC"; else echo "CMP DIFFERS"; exit 1; fi
cd "$CLONE"
find . -name "*.o" -exec touch {} +
sleep 1
rm -f src/cpus/*.o src/devices/dev_sgi_ip32.o gxemul
echo "BUILDING BASE (clone2)..."
make >"$WD/build_base2.log" 2>&1; RC=$?
echo "MAKE_RC=$RC"
if [ -f gxemul ] && [ gxemul -nt src/devices/dev_sgi_ip32.c ]; then echo "BINARY FRESH"; else echo "BINARY STALE/MISSING"; tail -8 "$WD/build_base2.log"; exit 1; fi
echo "SETUP2_DONE"
