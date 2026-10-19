#!/bin/bash
#  killtable567.sh -- #567's kill table 1, in the scratch clone /tmp/gx567 (a cp -a of /tmp/gx566, whose sources are HEAD's).
#  BASELINE NAMED: the draft fix, dev_fbctrl.fix567.c (the round's post-fix working set); its 95/95 is PROBE95_postfix.out.
#  PRETABLE.out (section 4) predicted every mutant before this file existed.  The probe is FROZEN (copied) once; every
#  leg runs that copy.  A clone-local sentinel is dropped before the first mutant and cleared only after the restore
#  passes both clearance parts against the draft.  build/ is not touched.  Run from a frozen copy of THIS script.
set -u
S=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/fbcmd
C=/tmp/gx567
F=src/devices/dev_fbctrl.c
OUT=$S/killtable1
mkdir -p "$OUT"
echo "TABLE1 start $(date '+%F %T')" | tee "$OUT/SCORES.txt"
[ -e "$C/.MUTANT" ] && { echo "clone already carries a sentinel -- stop" | tee -a "$OUT/SCORES.txt"; exit 9; }
cmp -s "$S/dev_fbctrl.fix567.c" "$C/$F" || { echo "clone's $F is not the draft fix -- stop" | tee -a "$OUT/SCORES.txt"; exit 9; }
[ "$C/gxemul" -nt "$C/$F" ] || { echo "clone's binary is older than $F -- stop" | tee -a "$OUT/SCORES.txt"; exit 9; }
cp "$S/fbctrl_cmd_probe.py" "$OUT/probe.frozen.py"
echo "probe md5 $(md5sum < "$OUT/probe.frozen.py" | cut -c1-32)" | tee -a "$OUT/SCORES.txt"
run_probe() {   # $1 label, $2 binary
    python3 -u "$OUT/probe.frozen.py" "$2" > "$OUT/$1.raw" 2>&1
    local rc=$?
    printf '%-12s rc=%s %s %s last=%s\n' "$1" "$rc" "$(grep -a '^FBCMD_RESULT' "$OUT/$1.raw")" \
        "$(grep -a '^FBCMD_CONTROL' "$OUT/$1.raw")" "$(tail -1 "$OUT/$1.raw")" | tee -a "$OUT/SCORES.txt"
    grep -a ' FAIL ' "$OUT/$1.raw" | sed 's/^  */      red: /' | cut -c1-70 >> "$OUT/SCORES.txt"
}
build() {       # $1 label
    (cd "$C" && rm -f src/cpus/*.o src/devices/dev_fbctrl.o && make -j4 > "$OUT/build_$1.log" 2>&1)
    local rc=$?
    [ "$C/gxemul" -nt "$C/$F" ] || { echo "$1: BINARY NOT FRESH (make rc=$rc) -- stop, sentinel kept" | tee -a "$OUT/SCORES.txt"; exit 9; }
}
echo "base: the draft fix, as built" | tee -a "$OUT/SCORES.txt"
run_probe base "$C/gxemul"
echo "SCRATCH CLONE (#567 kill table 1): $F carries a mutant" > "$C/.MUTANT"
for m in B_gateoff D1_u32 D2_gt1 D3_gt0 D4_ge0 D5_len4 D6_shared D7_debug D8_store D9_anyport D10_nolatch; do
    cp "$S/mutants/$m.c" "$C/$F"
    build "$m"
    run_probe "$m" "$C/gxemul"
done
echo "null media (c):" | tee -a "$OUT/SCORES.txt"
run_probe C_absent /nonexistent/gxemul
run_probe C_bintrue /bin/true
echo "--- restore" | tee -a "$OUT/SCORES.txt"
cp "$S/dev_fbctrl.fix567.c" "$C/$F"
build restore
cmp -s "$S/dev_fbctrl.fix567.c" "$C/$F" && echo "part 1: $F == the draft fix" | tee -a "$OUT/SCORES.txt" \
    || { echo "part 1 FAILED -- sentinel kept" | tee -a "$OUT/SCORES.txt"; exit 9; }
[ "$C/gxemul" -nt "$C/$F" ] && echo "part 2: binary newer than $F" | tee -a "$OUT/SCORES.txt" \
    || { echo "part 2 FAILED -- sentinel kept" | tee -a "$OUT/SCORES.txt"; exit 9; }
echo "restored binary md5 $(md5sum < "$C/gxemul" | cut -c1-32)" | tee -a "$OUT/SCORES.txt"
rm -f "$C/.MUTANT"; echo "sentinel cleared" | tee -a "$OUT/SCORES.txt"
echo "TABLE1 end $(date '+%F %T')" | tee -a "$OUT/SCORES.txt"
echo TABLE1_DONE | tee -a "$OUT/SCORES.txt"
