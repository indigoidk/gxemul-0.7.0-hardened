#!/bin/bash
CL=/tmp/gxo549v6
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
C=$SEC/regress/artifacts/fbctrlportkill_20260924/opus549_measured/v6
{
echo "# #549 v6 pass, Opus measuring seat -- inputs (end of run); clone $CL (volatile)"
md5sum "$SEC/src/devices/dev_fbctrl.c" "$SEC/regress/fbctrl_port_probe.py" "$SEC/regress/gate_mips_folds.sh" /mnt/c/DocumentNoSnc/cc/GXEMUL/build/gxemul
cmp -s "$CL/src/devices/dev_fbctrl.c" "$SEC/src/devices/dev_fbctrl.c" && echo "clone dev_fbctrl.c == SEC (end of run)"
[ -e "$CL/.MUTANT" ] && echo "SENTINEL PRESENT" || echo "no .MUTANT sentinel"
echo "# built binaries:"; cd "$CL/bins" && md5sum gx_* 2>/dev/null
} > "$C/INPUTS_v6.md5"
ls /tmp/gx_fbctrl549p_*.bin 2>/dev/null && echo LEFTOVERS || echo "no leftover /tmp stubs"
head -8 "$C/INPUTS_v6.md5"
