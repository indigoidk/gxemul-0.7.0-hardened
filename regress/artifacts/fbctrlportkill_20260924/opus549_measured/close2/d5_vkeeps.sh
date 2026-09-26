#!/bin/bash
set -u
CL=/tmp/gxo549cf2
C=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/fbctrlportkill_20260924/opus549_measured/close2
python3 "$C/mk_probe_vkeeps.py" /mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/fbctrl_port_probe.py "$CL/probe/vkeeps.py" || exit 2
diff /mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/fbctrl_port_probe.py "$CL/probe/vkeeps.py" > "$C/probe_vkeeps.diff"
mkdir -p "$C/vkeeps"
cd "$CL/probe" || exit 2
for b in fix F_ref_c7 F_ref_y1 F_ref_r55 F_ref_cmd1 F_rd_c7; do
  python3 -u vkeeps.py "$CL/bins/gx_$b" > "$C/vkeeps/$b.out" 2>&1
  echo "$b rc=$? $(grep -E '^FBCTRLP_RESULT=' "$C/vkeeps/$b.out") | $(grep -E '^  FAIL ' "$C/vkeeps/$b.out" | sed -E 's/^  FAIL +//; s/ +got=/ got=/; s/ +want=.*//' | tr '\n' ';')"
done
