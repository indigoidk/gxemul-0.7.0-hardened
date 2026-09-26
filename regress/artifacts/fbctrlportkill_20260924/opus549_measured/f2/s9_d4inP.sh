#!/bin/bash
set -u
CL=/tmp/gxo549f2m
F2=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/fbctrlportkill_20260924/opus549_measured/f2
python3 "$F2/mk_proto_d4inP.py" "$F2/fbctrl_port_probe.f2proto.py" "$CL/probe/proto_d4inP.py" || exit 2
diff "$F2/fbctrl_port_probe.f2proto.py" "$CL/probe/proto_d4inP.py" > "$F2/proto_d4inP.diff"
mkdir -p "$F2/proto_d4inP"
cd "$CL/probe" || exit 2
for b in fix M_gt M_store N_datarearm T_D4b_cmdrearm; do
  o="$F2/proto_d4inP/$b.out"
  python3 -u proto_d4inP.py "$CL/bins/gx_$b" > "$o" 2>&1
  echo "$b rc=$? $(grep -E '^FBCTRLP_RESULT=' "$o") | $(grep -E '^  session P' "$o" | tr -s ' ') | P-rows red: $(grep -E '^  FAIL (refuse|announce|D10 P|D4-in-P)' "$o" | wc -l)"
done
