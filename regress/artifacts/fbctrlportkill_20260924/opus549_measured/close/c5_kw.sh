#!/bin/bash
CL=/tmp/gxo549close
C=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/fbctrlportkill_20260924/opus549_measured/close
cp "$C/kill_witness.py" "$CL/probe/kw.frozen.py"
cd "$CL/probe" || exit 2
for b in fix E_ref_cmd E_ref_p2; do echo "== $b"; python3 -u kw.frozen.py "$CL/bins/gx_$b" "$CL/probe/frozen_x.py" 2>&1 | grep -E 'KW|session'; done
