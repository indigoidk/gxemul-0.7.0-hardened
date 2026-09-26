#!/bin/bash
CL=/tmp/gxo549f2m
F2=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/fbctrlportkill_20260924/opus549_measured/f2
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
{
echo "# opus F2 measuring seat (fresh start 2026-09-25) -- inputs and binaries; the clone is $CL (volatile)"
echo "# (INPUTS.md5 in this directory is the EARLIER F2 seat's, which stopped before measuring; not used here)"
md5sum "$SEC/src/devices/dev_fbctrl.c" "$SEC/regress/fbctrl_port_probe.py" "$SEC/regress/gate_mips_folds.sh" "$SEC/regress/lib.sh"
md5sum "$F2/fbctrl_port_probe.f2proto.py" "$F2/twoinst_probe.py" "$F2/gen_variants_f2.py"
cmp -s "$CL/src/devices/dev_fbctrl.c" "$SEC/src/devices/dev_fbctrl.c" && echo "clone dev_fbctrl.c == SEC (end of run)"
[ "$CL/gxemul" -nt "$CL/src/devices/dev_fbctrl.c" ] && echo "clone gxemul newer than its dev_fbctrl.c; md5 $(md5sum < $CL/gxemul | cut -c1-8)"
[ -e "$CL/.MUTANT" ] && echo "SENTINEL PRESENT" || echo "no .MUTANT sentinel in the clone"
echo "# binaries"
cd "$CL/bins" && md5sum gx_* 
} > "$F2/INPUTS_opusf2m.md5"
ls /tmp/gx_fbctrl549* 2>/dev/null && echo "LEFTOVER TMP FILES" || echo "no leftover /tmp stub/cfg files"
cat "$F2/INPUTS_opusf2m.md5" | head -12
