#!/bin/bash
#  killtable567f.sh -- #567's kill table 3 (PRETABLE_ADDENDUM_t3.out, written before this runs): EVERY mutant built
#  (tables 1, 1b, 2a, 3a: 32) and both null media, on probe v3 (106 rows), in the scratch clone /tmp/gx567.  BASELINE:
#  the fix.  A clone-local sentinel is dropped before the first mutant and cleared only after the restore passes both
#  clearance parts.  Run from a frozen copy of THIS script.  The mutant list is a bash ARRAY, one group per line, so no
#  line continuation is needed.
set -u
S=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/fbcmd
C=/tmp/gx567
F=src/devices/dev_fbctrl.c
OUT=$S/killtable3
mkdir -p "$OUT"
PROBE=$OUT/probe.v3.frozen.py
cp "$S/fbctrl_cmd_probe.v3.py" "$PROBE"
MUTANTS=(mutants/B_gateoff mutants/D1_u32 mutants/D2_gt1 mutants/D3_gt0 mutants/D4_ge0 mutants/D5_len4)
MUTANTS+=(mutants/D6_shared mutants/D7_debug mutants/D8_store mutants/D9_anyport mutants/D10_nolatch)
MUTANTS+=(mutants_b/E1_gt3 mutants_b/E2_nopref mutants_b/E3_setref mutants_b/E4_hoist mutants_b/E5_signed)
MUTANTS+=(mutants_c/E6_readdisp mutants_c/E7_anyport mutants_c/E8_latchpre mutants_c/E9_argtrunc mutants_c/E10_operand)
MUTANTS+=(mutants_c/E11_intcast mutants_c/E12_elseif mutants_c/E13_lenne4 mutants_c/E14_latchwide)
MUTANTS+=(mutants_d/E15_sdnodisp mutants_d/E16_sdbound0 mutants_d/E17_shbound1 mutants_d/E18_sdbound3)
MUTANTS+=(mutants_d/E19_shbound3 mutants_d/E20_latchacc mutants_d/E21_latchread)
echo "TABLE3 start $(date '+%F %T')" | tee "$OUT/SCORES.txt"
[ "${#MUTANTS[@]}" = 32 ] || { echo "mutant list holds ${#MUTANTS[@]}, not 32 -- stop" | tee -a "$OUT/SCORES.txt"; exit 9; }
for spec in "${MUTANTS[@]}"; do [ -f "$S/$spec.c" ] || { echo "no source for $spec -- stop" | tee -a "$OUT/SCORES.txt"; exit 9; }; done
[ -e "$C/.MUTANT" ] && { echo "clone already carries a sentinel -- stop" | tee -a "$OUT/SCORES.txt"; exit 9; }
cmp -s "$S/dev_fbctrl.fix567.c" "$C/$F" || { echo "clone's $F is not the fix -- stop" | tee -a "$OUT/SCORES.txt"; exit 9; }
[ "$C/gxemul" -nt "$C/$F" ] || { echo "clone's binary is older than $F -- stop" | tee -a "$OUT/SCORES.txt"; exit 9; }
echo "probe v3 md5 $(md5sum < "$PROBE" | cut -c1-32); 32 mutant sources present" | tee -a "$OUT/SCORES.txt"
run_probe() {   # $1 label, $2 binary
    python3 -u "$PROBE" "$2" > "$OUT/$1.raw" 2>&1
    local rc=$?
    printf '%-14s rc=%s %s %s last=%s\n' "$1" "$rc" "$(grep -a '^FBCMD_RESULT' "$OUT/$1.raw")" \
        "$(grep -a '^FBCMD_CONTROL' "$OUT/$1.raw")" "$(tail -n 1 "$OUT/$1.raw")" | tee -a "$OUT/SCORES.txt"
    grep -aE '^  [^ ].* got=[^ ]* +want=[^ ]* +FAIL  ' "$OUT/$1.raw" | sed -E 's/ +FAIL  .*//; s/^  */      red: /' >> "$OUT/SCORES.txt"
}
build() {       # $1 label
    (cd "$C" && rm -f src/cpus/*.o src/devices/dev_fbctrl.o && make -j4 > "$OUT/build_$1.log" 2>&1)
    local rc=$?
    [ "$C/gxemul" -nt "$C/$F" ] || { echo "$1: BINARY NOT FRESH (make rc=$rc) -- stop, sentinel kept" | tee -a "$OUT/SCORES.txt"; exit 9; }
}
echo "base: the fix" | tee -a "$OUT/SCORES.txt"
run_probe base "$C/gxemul"
echo "SCRATCH CLONE (#567 kill table 3): $F carries a mutant" > "$C/.MUTANT"
for spec in "${MUTANTS[@]}"; do
    m=$(basename "$spec")
    cp "$S/$spec.c" "$C/$F"
    build "$m"
    run_probe "$m" "$C/gxemul"
done
echo "null media (c):" | tee -a "$OUT/SCORES.txt"
run_probe C_absent /nonexistent/gxemul
run_probe C_bintrue /bin/true
echo "--- restore" | tee -a "$OUT/SCORES.txt"
cp "$S/dev_fbctrl.fix567.c" "$C/$F"
build restore
cmp -s "$S/dev_fbctrl.fix567.c" "$C/$F" && echo "part 1: $F == the fix" | tee -a "$OUT/SCORES.txt" \
    || { echo "part 1 FAILED -- sentinel kept" | tee -a "$OUT/SCORES.txt"; exit 9; }
[ "$C/gxemul" -nt "$C/$F" ] && echo "part 2: binary newer than $F" | tee -a "$OUT/SCORES.txt" \
    || { echo "part 2 FAILED -- sentinel kept" | tee -a "$OUT/SCORES.txt"; exit 9; }
echo "restored binary md5 $(md5sum < "$C/gxemul" | cut -c1-32)" | tee -a "$OUT/SCORES.txt"
rm -f "$C/.MUTANT"; echo "sentinel cleared" | tee -a "$OUT/SCORES.txt"
echo "TABLE3 end $(date '+%F %T')" | tee -a "$OUT/SCORES.txt"
echo TABLE3_DONE | tee -a "$OUT/SCORES.txt"
