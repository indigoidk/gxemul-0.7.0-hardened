#!/bin/bash
CL=/tmp/gxo549c3
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
C=$SEC/regress/artifacts/fbctrlportkill_20260924/opus549_measured/c3
{
echo "# #549 verifying pass, Opus measuring seat -- inputs (end of run); clone $CL (volatile)"
md5sum "$SEC/src/devices/dev_fbctrl.c" "$SEC/regress/fbctrl_port_probe.py" /mnt/c/DocumentNoSnc/cc/GXEMUL/build/gxemul
cmp -s "$CL/src/devices/dev_fbctrl.c" "$SEC/src/devices/dev_fbctrl.c" && echo "clone dev_fbctrl.c == SEC (end of run)"
[ -e "$CL/.MUTANT" ] && echo "SENTINEL PRESENT" || echo "no .MUTANT sentinel in the clone"
echo "# built binaries:"; cd "$CL/bins" && md5sum gx_* 2>/dev/null | head -40
} > "$C/INPUTS_c3.md5"
ls /tmp/gx_fbctrl549* 2>/dev/null && echo LEFTOVERS || echo "no leftover /tmp stub files"
head -6 "$C/INPUTS_c3.md5"
