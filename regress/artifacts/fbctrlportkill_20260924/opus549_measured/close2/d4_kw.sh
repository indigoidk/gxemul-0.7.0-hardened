#!/bin/bash
CL=/tmp/gxo549cf2
C=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/fbctrlportkill_20260924/opus549_measured/close2
cp /mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/fbctrl_port_probe.py "$CL/probe/frozen_kw2.py"
cp "$C/kill_witness2.py" "$CL/probe/kw2.frozen.py"
cd "$CL/probe" || exit 2
for b in fix F_ref_c7; do echo "== $b"; python3 -u kw2.frozen.py "$CL/bins/gx_$b" "$CL/probe/frozen_kw2.py" 2>&1 | grep -E 'KW2|session'; done
