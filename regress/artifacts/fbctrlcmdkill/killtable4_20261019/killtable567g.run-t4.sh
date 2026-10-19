#!/bin/bash
#  killtable567g.sh -- #567's kill table 4 (PRETABLE_ADDENDUM_t4.out, written before this runs): probe v4's two legs (the
#  fix, HEAD's binary), then EVERY mutant built -- tables 1, 1b, 2a and 3a: 32; table 4's new ones: 12 -- on probe v4, the
#  twelve new ones also on probe v3 (where each should escape), and both null media, in the scratch clone /tmp/gx567.
#  BASELINE: the fix.  A clone-local sentinel is dropped before the first mutant and cleared only after the restore passes
#  both clearance parts.  Run from a frozen copy of THIS script.  Mutant lists are bash ARRAYS, one group per line.
set -u
S=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/fbcmd
C=/tmp/gx567
H=/tmp/gx566
F=src/devices/dev_fbctrl.c
OUT=$S/killtable4
mkdir -p "$OUT"
P4=$OUT/probe.v4.frozen.py
P3=$OUT/probe.v3.frozen.py
cp "$S/fbctrl_cmd_probe.v4.py" "$P4"
cp "$S/fbctrl_cmd_probe.v3.py" "$P3"
OLD=(mutants/B_gateoff mutants/D1_u32 mutants/D2_gt1 mutants/D3_gt0 mutants/D4_ge0 mutants/D5_len4)
OLD+=(mutants/D6_shared mutants/D7_debug mutants/D8_store mutants/D9_anyport mutants/D10_nolatch)
OLD+=(mutants_b/E1_gt3 mutants_b/E2_nopref mutants_b/E3_setref mutants_b/E4_hoist mutants_b/E5_signed)
OLD+=(mutants_c/E6_readdisp mutants_c/E7_anyport mutants_c/E8_latchpre mutants_c/E9_argtrunc mutants_c/E10_operand)
OLD+=(mutants_c/E11_intcast mutants_c/E12_elseif mutants_c/E13_lenne4 mutants_c/E14_latchwide)
OLD+=(mutants_d/E15_sdnodisp mutants_d/E16_sdbound0 mutants_d/E17_shbound1 mutants_d/E18_sdbound3)
OLD+=(mutants_d/E19_shbound3 mutants_d/E20_latchacc mutants_d/E21_latchread)
NEW=(mutants_e/E22_sdclear3 mutants_e/E23_sbset3 mutants_e/E24_shset3 mutants_e/E25_swset3 mutants_e/E26_setnarrow)
NEW+=(mutants_e/E27_sdnoset mutants_e/E28_sbnoset mutants_e/E29_testnarrow mutants_e/E30_portwidth)
NEW+=(mutants_e/E31_ldreaddisp mutants_e/E32_lbreadstore mutants_e/E33_lbreadpred)
echo "TABLE4 start $(date '+%F %T')" | tee "$OUT/SCORES.txt"
[ "${#OLD[@]}" = 32 ] || { echo "old list holds ${#OLD[@]}, not 32 -- stop" | tee -a "$OUT/SCORES.txt"; exit 9; }
[ "${#NEW[@]}" = 12 ] || { echo "new list holds ${#NEW[@]}, not 12 -- stop" | tee -a "$OUT/SCORES.txt"; exit 9; }
for spec in "${OLD[@]}" "${NEW[@]}"; do [ -f "$S/$spec.c" ] || { echo "no source for $spec -- stop" | tee -a "$OUT/SCORES.txt"; exit 9; }; done
[ -e "$C/.MUTANT" ] && { echo "clone already carries a sentinel -- stop" | tee -a "$OUT/SCORES.txt"; exit 9; }
cmp -s "$S/dev_fbctrl.fix567.c" "$C/$F" || { echo "clone's $F is not the fix -- stop" | tee -a "$OUT/SCORES.txt"; exit 9; }
[ "$C/gxemul" -nt "$C/$F" ] || { echo "clone's binary is older than $F -- stop" | tee -a "$OUT/SCORES.txt"; exit 9; }
cmp -s "$S/dev_fbctrl.head.c" "$H/$F" || { echo "$H's $F is not HEAD's -- stop" | tee -a "$OUT/SCORES.txt"; exit 9; }
[ "$H/gxemul" -nt "$H/$F" ] || { echo "$H's binary is older than $F -- stop" | tee -a "$OUT/SCORES.txt"; exit 9; }
echo "probe v4 md5 $(md5sum < "$P4" | cut -c1-32); probe v3 md5 $(md5sum < "$P3" | cut -c1-32); 44 mutant sources present" | tee -a "$OUT/SCORES.txt"
run_probe() {   # $1 label, $2 binary, $3 probe
    python3 -u "$3" "$2" > "$OUT/$1.raw" 2>&1
    local rc=$?
    printf '%-20s rc=%s %s %s last=%s\n' "$1" "$rc" "$(grep -a '^FBCMD_RESULT' "$OUT/$1.raw")" \
        "$(grep -a '^FBCMD_CONTROL' "$OUT/$1.raw")" "$(tail -n 1 "$OUT/$1.raw")" | tee -a "$OUT/SCORES.txt"
    grep -aE '^  [^ ].* got=[^ ]* +want=[^ ]* +FAIL  ' "$OUT/$1.raw" | sed -E 's/ +FAIL  .*//; s/^  */      red: /' >> "$OUT/SCORES.txt"
}
build() {       # $1 label
    (cd "$C" && rm -f src/cpus/*.o src/devices/dev_fbctrl.o && make -j4 > "$OUT/build_$1.log" 2>&1)
    local rc=$?
    [ "$C/gxemul" -nt "$C/$F" ] || { echo "$1: BINARY NOT FRESH (make rc=$rc) -- stop, sentinel kept" | tee -a "$OUT/SCORES.txt"; exit 9; }
}
echo "legs (v4): the fix, then HEAD's binary" | tee -a "$OUT/SCORES.txt"
run_probe leg_FIX "$C/gxemul" "$P4"
run_probe leg_HEAD "$H/gxemul" "$P4"
echo "SCRATCH CLONE (#567 kill table 4): $F carries a mutant" > "$C/.MUTANT"
echo "the 32 earlier mutants, on v4:" | tee -a "$OUT/SCORES.txt"
for spec in "${OLD[@]}"; do
    m=$(basename "$spec")
    cp "$S/$spec.c" "$C/$F"
    build "$m"
    run_probe "$m" "$C/gxemul" "$P4"
done
echo "the 12 new mutants, on v3 (each should escape) and on v4:" | tee -a "$OUT/SCORES.txt"
for spec in "${NEW[@]}"; do
    m=$(basename "$spec")
    cp "$S/$spec.c" "$C/$F"
    build "$m"
    run_probe "${m}_v3" "$C/gxemul" "$P3"
    run_probe "$m" "$C/gxemul" "$P4"
done
echo "null media (c), on v4:" | tee -a "$OUT/SCORES.txt"
run_probe C_absent /nonexistent/gxemul "$P4"
run_probe C_bintrue /bin/true "$P4"
echo "--- restore" | tee -a "$OUT/SCORES.txt"
cp "$S/dev_fbctrl.fix567.c" "$C/$F"
build restore
cmp -s "$S/dev_fbctrl.fix567.c" "$C/$F" && echo "part 1: $F == the fix" | tee -a "$OUT/SCORES.txt" \
    || { echo "part 1 FAILED -- sentinel kept" | tee -a "$OUT/SCORES.txt"; exit 9; }
[ "$C/gxemul" -nt "$C/$F" ] && echo "part 2: binary newer than $F" | tee -a "$OUT/SCORES.txt" \
    || { echo "part 2 FAILED -- sentinel kept" | tee -a "$OUT/SCORES.txt"; exit 9; }
echo "restored binary md5 $(md5sum < "$C/gxemul" | cut -c1-32)" | tee -a "$OUT/SCORES.txt"
rm -f "$C/.MUTANT"; echo "sentinel cleared" | tee -a "$OUT/SCORES.txt"
echo "TABLE4 end $(date '+%F %T')" | tee -a "$OUT/SCORES.txt"
echo TABLE4_DONE | tee -a "$OUT/SCORES.txt"
