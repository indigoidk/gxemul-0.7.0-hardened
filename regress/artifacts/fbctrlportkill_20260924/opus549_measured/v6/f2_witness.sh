#!/bin/bash
set -u
CL=/tmp/gxo549v6
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
C=$SEC/regress/artifacts/fbctrlportkill_20260924/opus549_measured/v6
FZ=$CL/probe/frozen_v6.py
cp "$C/unset_witness.py" "$CL/probe/uw.frozen.py"
cd "$CL/probe" || exit 2
for b in fix LB_unset16; do echo "== $b"; python3 -u uw.frozen.py "$CL/bins/gx_$b" "$FZ" 2>&1 | grep -E '^U '; done | tee "$C/unset_witness.out"
rm -f /tmp/gx_fbctrl549p_*.bin
