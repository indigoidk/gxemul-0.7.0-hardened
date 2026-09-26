#!/bin/bash
# #549 closing F2 pass, Opus measuring seat: clone build/ into WSL /tmp, cmp against the working tree, rebuild the base.
set -u
ROOT=/mnt/c/DocumentNoSnc/cc/GXEMUL
SEC=$ROOT/GXEMUL-SEC
CL=/tmp/gxo549cf2
echo "START $(date +%T)"
if [ -e "$CL" ]; then echo "REFUSED: $CL exists"; exit 2; fi
cp -a "$ROOT/build" "$CL" || { echo "CP FAILED"; exit 2; }
mkdir -p "$CL/bins" "$CL/probe" "$CL/var"
cp "$SEC/regress/fbctrl_port_probe.py" "$CL/probe/fbctrl_port_probe.py"
cmp "$CL/src/devices/dev_fbctrl.c" "$SEC/src/devices/dev_fbctrl.c" && echo "CMP dev_fbctrl.c clone vs SEC working tree: CLEAN" || { echo "CMP dev_fbctrl.c DIFFERS"; exit 3; }
cmp "$CL/probe/fbctrl_port_probe.py" "$SEC/regress/fbctrl_port_probe.py" && echo "CMP probe clone vs SEC working tree: CLEAN" || { echo "CMP probe DIFFERS"; exit 3; }
md5sum "$SEC/src/devices/dev_fbctrl.c" "$SEC/regress/fbctrl_port_probe.py" "$CL/src/devices/dev_fbctrl.c" "$CL/probe/fbctrl_port_probe.py"
cp "$CL/src/devices/dev_fbctrl.c" "$CL/var/fix.c"
cd "$CL" || exit 2
rm -f src/cpus/*.o
make -j8 > "$CL/make_base.log" 2>&1
echo "MAKE_RC=$?"
if [ gxemul -nt src/devices/dev_fbctrl.c ] && [ gxemul -nt src/cpus/cpu_mips.o ]; then echo "FRESH=yes"; else echo "FRESH=NO"; fi
cp gxemul bins/gx_fix
echo "base md5 $(md5sum < gxemul | cut -d' ' -f1) (build/gxemul: $(md5sum < $ROOT/build/gxemul | cut -d' ' -f1))"
cd "$CL/probe" && python3 -u fbctrl_port_probe.py "$CL/bins/gx_fix" > "$ROOT/GXEMUL-SEC/regress/artifacts/fbctrlportkill_20260924/opus549_measured/close2/base_fix.out" 2>&1
echo "probe rc=$? $(grep -E '^FBCTRLP_(RESULT|CONTROL)=' $ROOT/GXEMUL-SEC/regress/artifacts/fbctrlportkill_20260924/opus549_measured/close2/base_fix.out | tr '\n' ' ')"
echo "END $(date +%T)"
