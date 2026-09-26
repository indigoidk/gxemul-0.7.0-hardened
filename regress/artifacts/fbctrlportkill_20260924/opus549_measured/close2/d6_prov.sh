#!/bin/bash
CL=/tmp/gxo549cf2
C=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/fbctrlportkill_20260924/opus549_measured/close2
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
{
echo "# #549 closing F2 pass, Opus measuring seat -- inputs (end of run) and binaries; clone $CL (volatile)"
md5sum "$SEC/src/devices/dev_fbctrl.c" "$SEC/regress/fbctrl_port_probe.py" "$SEC/regress/gate_mips_folds.sh" /mnt/c/DocumentNoSnc/cc/GXEMUL/build/gxemul
md5sum "$C/gen_close2.py" "$C/kill_witness2.py" "$C/mk_probe_vkeeps.py"
cmp -s "$CL/src/devices/dev_fbctrl.c" "$SEC/src/devices/dev_fbctrl.c" && echo "clone dev_fbctrl.c == SEC"
[ -e "$CL/.MUTANT" ] && echo "SENTINEL PRESENT" || echo "no .MUTANT sentinel in the clone"
cd "$CL/bins" && md5sum gx_*
} > "$C/INPUTS_close2.md5"
ls /tmp/gx_fbctrl549* 2>/dev/null && echo LEFTOVERS || echo "no leftover /tmp stub files"
head -9 "$C/INPUTS_close2.md5"
