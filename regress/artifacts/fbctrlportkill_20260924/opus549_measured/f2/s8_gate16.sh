#!/bin/bash
# Question 3: run gate 16's fbctrl block (extracted from the WORKING-TREE gate_mips_folds.sh, lines 53-74) on the p2
# fixture logs, as shipped and with each candidate reconciliation line inserted before the block's closing `fi`.
# The probe is replaced by a stand-in that prints the fixture verbatim and exits 0; LOGDIR is clone-local.
set -u
CL=/tmp/gxo549f2m
F2=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/fbctrlportkill_20260924/opus549_measured/f2
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
FIX=$F2/../p2/gate16_fixtures
W=$CL/g16
rm -rf "$W"; mkdir -p "$W/log"
cp "$SEC/regress/lib.sh" "$W/lib.sh"
cmp "$W/lib.sh" "$SEC/regress/lib.sh" && echo "lib.sh copy CMP clean ($(md5sum < "$W/lib.sh" | cut -c1-8))"
G=$SEC/regress/gate_mips_folds.sh
[ "$(sed -n 53p "$G")" = 'FBCLOG=$LOGDIR/fbctrl_port_probe.log' ] && [ "$(sed -n 74p "$G")" = 'fi' ] || { echo "BLOCK ANCHORS MOVED"; exit 3; }
sed -n 53,73p "$G" > "$W/block_head.sh"
echo "gate_mips_folds.sh md5 $(md5sum < "$G" | cut -c1-8); block = lines 53-74"
cat > "$W/fbctrl_port_probe.py" <<'PYEOF'
import os, sys
sys.stdout.write(open(os.environ["G16_FIXTURE"]).read())
PYEOF
# candidates (each ONE line, inserted before the closing fi)
cat > "$W/cand_none.sh" <<'EOF'
EOF
cat > "$W/cand_rows.sh" <<'EOF'
    check "fbctrl_port rows emitted" "$(grep -cE '^  (ok|FAIL) ' "$FBCLOG")" "${fbres#*/}"
EOF
cat > "$W/cand_ok.sh" <<'EOF'
    check "fbctrl_port ok rows emitted" "$(grep -c '^  ok ' "$FBCLOG")" "${fbres%/*}"
EOF
for c in none rows ok; do
    { cat "$W/block_head.sh"; cat "$W/cand_$c.sh"; echo "fi"; } > "$W/block_$c.sh"
done
diff <(sed -n 53,74p "$G") "$W/block_none.sh" > /dev/null && echo "block_none == gate lines 53-74 (verbatim)"
cp "$W/block_rows.sh" "$F2/g16_block_plus_rows.sh"; cp "$W/block_ok.sh" "$F2/g16_block_plus_ok.sh"
OUT=$F2/TABLE_gate16.out
echo "# $(date +%T)  fixture x candidate -> gate verdict (fixtures: p2/gate16_fixtures, unmodified)" > "$OUT"
printf '%-26s %-34s %-34s %-34s\n' fixture "as shipped" "+ rows emitted == denominator" "+ ok rows == numerator" >> "$OUT"
cd "$W" || exit 2
for fx in good row_deleted row_failed_result_intact empty dup trunc_nodone no_result no_control trunc_mid dup_done result_trailing dup_result; do
    line=$(printf '%-26s' "$fx")
    for c in none rows ok; do
        res=$(G16_FIXTURE="$FIX/fixture_$fx.log" LOGDIR="$W/log" PMAX=/bin/true bash -c '
            . ./lib.sh
            gate_begin "g16 block on fixture '"$fx"' ('"$c"')"
            . ./block_'"$c"'.sh
            gate_end' 2>&1)
        echo "$res" > "$F2/g16/${fx}_${c}.out" 2>/dev/null || { mkdir -p "$F2/g16"; echo "$res" > "$F2/g16/${fx}_${c}.out"; }
        v=$(echo "$res" | tail -1 | sed -E 's/^g16 block on fixture [a-z_]+ \([a-z]+\): //')
        line="$line $(printf '%-34s' "$v")"
    done
    echo "$line" >> "$OUT"
done
echo "# $(date +%T) done" >> "$OUT"
cat "$OUT"
