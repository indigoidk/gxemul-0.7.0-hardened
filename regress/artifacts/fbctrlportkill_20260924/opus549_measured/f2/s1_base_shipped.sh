#!/bin/bash
# Run the SHIPPED probe (frozen copy, cmp-verified) against the clone's fix binary.
set -u
CL=/tmp/gxo549f2m
F2=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/fbctrlportkill_20260924/opus549_measured/f2
cd "$CL/probe" || exit 2
cmp fbctrl_port_probe.py /mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/fbctrl_port_probe.py && echo "PROBE CMP CLEAN"
md5sum "$CL/bins/gx_fix"
S=$(date +%s)
python3 -u fbctrl_port_probe.py "$CL/bins/gx_fix" > "$F2/base_shipped_fix.out" 2>&1
echo "probe rc=$? secs=$(( $(date +%s) - S ))"
tail -3 "$F2/base_shipped_fix.out"
