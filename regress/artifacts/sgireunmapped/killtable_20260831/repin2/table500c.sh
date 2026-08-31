#!/bin/bash
#
#  PASS 3 -- the RE-PINNED PROBE IN SITU.  No rebuilds: pass 2's five binaries are
#  reused, so this measures the detector, not the compiler.  What it answers is the
#  denominator question directly -- rows emitted / green / red, MEASURED, for the
#  three literals gate_arm.sh pins at 35 / 35 / 0.
set -u
H=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/o500r
CLONE=/tmp/gx500r
OUT=$H/outc
mkdir -p $OUT
echo "TABLE500C start $(date +%H:%M:%S)"
echo "  probe under test: probe_new.run.py  md5 $(md5sum $H/probe_new.run.py | cut -d' ' -f1)"
echo "  (= regress/sgi_re_width_probe.py with repin.patch applied)"
echo ""
printf '  %-10s %-8s %-8s %-6s %-6s %-5s %s\n' variant result emitted green red rowok "the re-pinned row"
for V in base fix mexit0 mret0 mrdexit0; do
  B=$CLONE/gxb.$V
  [ -f $B ] || { echo "  $V: NO BINARY -- ABORT"; exit 1; }
  python3 -u $H/probe_new.run.py $B $V > $OUT/n_$V.txt 2>&1
  RC=$?; ND=$(grep -c '^OPUS497T_DONE$' $OUT/n_$V.txt); NR=$(grep -c '^OPUS497T_RESULT=' $OUT/n_$V.txt)
  if [ "$RC" -ne 0 ] || [ "$ND" -ne 1 ] || [ "$NR" -ne 1 ]; then
    echo "  $V: RUN DID NOT COMPLETE (rc=$RC sentinels=$ND) -- NOT SCORED, ABORT"
    tail -10 $OUT/n_$V.txt | sed 's/^/     /'; exit 1
  fi
  RES=$(grep -h '^OPUS497T_RESULT=' $OUT/n_$V.txt | cut -d= -f2)
  G=$(grep -c ' ok$' $OUT/n_$V.txt); R=$(grep -c ' FAIL$' $OUT/n_$V.txt); E=$((G+R))
  RK=$(grep -c '^other decl  .*ok$' $OUT/n_$V.txt)
  printf '  %-10s %-8s %-8s %-6s %-6s %-5s %s\n' "$V" "$RES" "$E" "$G" "$R" "$RK" \
    "$(grep -h '^other decl' $OUT/n_$V.txt | sed 's/  */ /g')"
done
echo ""
echo "=== every RED row, per variant (so a red is attributable, not just counted) ==="
for V in base fix mexit0 mret0 mrdexit0; do
  echo "  --- $V ---"
  grep -E ' FAIL$' $OUT/n_$V.txt | sed 's/^/     /' || echo "     (none)"
done
echo ""
echo "=== the gate's own three checks, evaluated against the fix log ==="
L=$OUT/n_fix.txt
echo "  sgi_re rows emitted : got=$(( $(grep -c ' ok$' $L) + $(grep -c ' FAIL$' $L) ))  gate pins 35"
echo "  sgi_re rows green   : got=$(grep -c ' ok$' $L)  gate pins 35"
echo "  sgi_re rows red     : got=$(grep -c ' FAIL$' $L)  gate pins 0"
echo "  row-list name check : 'other kill' present? $(grep -c '^other kill' $L)   'other decl' present? $(grep -c '^other decl' $L)"
echo "TABLE500C_DONE $(date +%H:%M:%S)"
