#!/bin/bash
set -u
CL=/tmp/gxo549f2m
F2=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/fbctrlportkill_20260924/opus549_measured/f2
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
python3 "$F2/mk_shipped_cfg2.py" "$SEC/regress/fbctrl_port_probe.py" "$CL/probe/shipped_cfg2.py" || exit 2
diff "$SEC/regress/fbctrl_port_probe.py" "$CL/probe/shipped_cfg2.py" > "$F2/shipped_cfg2.diff"
mkdir -p "$F2/shipped_cfg2"
cd "$CL/probe" || exit 2
for b in fix M_static T_D9c_serial1; do
  python3 -u shipped_cfg2.py "$CL/bins/gx_$b" > "$F2/shipped_cfg2/$b.out" 2>&1
  echo "$b rc=$? $(grep -E '^FBCTRLP_(RESULT|CONTROL)=' "$F2/shipped_cfg2/$b.out" | tr '\n' ' ') | $(grep -E '^  session' "$F2/shipped_cfg2/$b.out" | tr -s ' ' | tr '\n' ';')"
done
rm -f /tmp/gx_fbctrl549p_*.bin.cfg
