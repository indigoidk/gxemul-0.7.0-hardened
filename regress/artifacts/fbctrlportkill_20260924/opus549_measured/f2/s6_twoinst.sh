#!/bin/bash
# Question 2: run the two-instance probe (frozen copy) in three modes against the fix, M_static and T_D9c_serial1.
set -u
CL=/tmp/gxo549f2m
F2=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/fbctrlportkill_20260924/opus549_measured/f2
cp "$F2/twoinst_probe.py" "$CL/probe/twoinst.frozen.py"
mkdir -p "$F2/twoinst"
S="$F2/TABLE_twoinst.out"
echo "# $(date +%T) twoinst probe md5=$(md5sum < "$CL/probe/twoinst.frozen.py" | cut -c1-8)" > "$S"
cd "$CL/probe" || exit 2
for b in fix M_static T_D9c_serial1; do
  for mode in stagger lockstepP serial2; do
    o="$F2/twoinst/${b}_${mode}.out"
    timeout 300 python3 -u twoinst.frozen.py "$CL/bins/gx_$b" "$mode" > "$o" 2>&1
    rc=$?
    red=$(grep -E '^  FAIL ' "$o" | sed -E 's/^  FAIL +//; s/  +got=/ got=/; s/ +want=/ want=/' | tr '\n' ';')
    printf '%-14s %-9s rc=%s md5=%s %s | %s\n' "$b" "$mode" "$rc" "$(md5sum < "$CL/bins/gx_$b" | cut -c1-8)" "$(grep -E '_RESULT=' "$o")" "$red" >> "$S"
  done
done
cmp -s "$CL/probe/twoinst.frozen.py" "$F2/twoinst_probe.py" && echo "# probe unchanged during the run" >> "$S"
echo "# $(date +%T) done" >> "$S"
cat "$S"
