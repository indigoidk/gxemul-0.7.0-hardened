#!/bin/bash
set -u
ROOT=/mnt/c/DocumentNoSnc/cc/GXEMUL
SEC=$ROOT/GXEMUL-SEC
CL=/tmp/gxo549v6
C=$SEC/regress/artifacts/fbctrlportkill_20260924/opus549_measured/v6
echo "START $(date +%T)"
if [ -e "$CL" ]; then echo "REFUSED: $CL exists"; exit 2; fi
cp -a "$ROOT/build" "$CL" || { echo CPFAIL; exit 2; }
mkdir -p "$CL/bins" "$CL/probe" "$CL/var"
cp "$SEC/regress/fbctrl_port_probe.py" "$CL/probe/fbctrl_port_probe.py"
cmp "$CL/src/devices/dev_fbctrl.c" "$SEC/src/devices/dev_fbctrl.c" && echo "CMP dev_fbctrl.c: CLEAN" || { echo DIFF; exit 3; }
cmp "$CL/probe/fbctrl_port_probe.py" "$SEC/regress/fbctrl_port_probe.py" && echo "CMP probe(v6): CLEAN" || { echo DIFF; exit 3; }
md5sum "$SEC/src/devices/dev_fbctrl.c" "$SEC/regress/fbctrl_port_probe.py" "$CL/src/devices/dev_fbctrl.c" "$CL/probe/fbctrl_port_probe.py"
cp "$CL/src/devices/dev_fbctrl.c" "$CL/var/fix.c"
cd "$CL" || exit 2
rm -f src/cpus/*.o
make -j4 > "$CL/make_base.log" 2>&1
echo "MAKE_RC=$?"
[ gxemul -nt src/devices/dev_fbctrl.c ] && [ gxemul -nt src/cpus/cpu_mips.o ] && echo "FRESH=yes" || echo "FRESH=NO"
cp gxemul bins/gx_fix
echo "base md5 $(md5sum < gxemul | cut -d' ' -f1) (build/gxemul: $(md5sum < $ROOT/build/gxemul | cut -d' ' -f1))"
cd "$CL/probe" && python3 -u fbctrl_port_probe.py "$CL/bins/gx_fix" > "$C/base_fix.out" 2>&1
echo "probe rc=$? $(grep -E '^FBCTRLP_(RESULT|CONTROL)=' $C/base_fix.out | tr '\n' ' ')"
grep -E '^  session B' "$C/base_fix.out"
echo "END $(date +%T)"
