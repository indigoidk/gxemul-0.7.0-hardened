#!/bin/bash
# #549 F2 measuring seat (fresh start 2026-09-25): clone build/ into WSL /tmp, name the baseline, rebuild it there.
# Baseline = the GXEMUL-SEC WORKING TREE's dev_fbctrl.c (the uncommitted #549 fix), cmp-verified below.
set -u
ROOT=/mnt/c/DocumentNoSnc/cc/GXEMUL
SEC=$ROOT/GXEMUL-SEC
F2=$SEC/regress/artifacts/fbctrlportkill_20260924/opus549_measured/f2
CL=/tmp/gxo549f2m
echo "START $(date +%T)"
if [ -e "$CL" ]; then echo "REFUSED: $CL exists"; exit 2; fi
cp -a "$ROOT/build" "$CL" || { echo "CP FAILED"; exit 2; }
mkdir -p "$CL/bins" "$CL/probe" "$CL/var"
cp "$SEC/regress/fbctrl_port_probe.py" "$CL/probe/fbctrl_port_probe.py"
if cmp "$CL/src/devices/dev_fbctrl.c" "$SEC/src/devices/dev_fbctrl.c"; then echo "CMP dev_fbctrl.c clone vs SEC working tree: CLEAN"; else echo "CMP dev_fbctrl.c: DIFFERS"; exit 3; fi
if cmp "$CL/probe/fbctrl_port_probe.py" "$SEC/regress/fbctrl_port_probe.py"; then echo "CMP fbctrl_port_probe.py clone vs SEC working tree: CLEAN"; else echo "CMP probe: DIFFERS"; exit 3; fi
cp "$CL/src/devices/dev_fbctrl.c" "$CL/var/fix.c"
md5sum "$SEC/src/devices/dev_fbctrl.c" "$SEC/regress/fbctrl_port_probe.py" "$CL/src/devices/dev_fbctrl.c" "$CL/probe/fbctrl_port_probe.py"
cd "$CL" || exit 2
rm -f src/cpus/*.o
make -j8 > "$CL/make_base.log" 2>&1
MRC=$?
echo "MAKE_RC=$MRC"
if [ gxemul -nt src/devices/dev_fbctrl.c ] && [ gxemul -nt src/cpus/cpu_mips.o ]; then echo "FRESH=yes"; else echo "FRESH=NO"; fi
ls -la --time-style=full-iso gxemul src/devices/dev_fbctrl.c src/devices/dev_fbctrl.o src/cpus/cpu_mips.o
grep -ci ' error' "$CL/make_base.log"
cp gxemul bins/gx_fix
md5sum gxemul bins/gx_fix
cp "$CL/make_base.log" "$F2/make_base.log"
echo "END $(date +%T)"
