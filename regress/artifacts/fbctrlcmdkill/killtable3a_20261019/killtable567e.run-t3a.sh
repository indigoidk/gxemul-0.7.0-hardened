#!/bin/bash
#  killtable567c.sh -- #567's kill table 3a (PRETABLE_ADDENDUM_t3a.out, written before this runs), in the scratch clone
#  /tmp/gx567, on probe v2 (kill table 2's frozen copy).  BASELINE: the fix (dev_fbctrl.fix567.c), left in the
#  clone by table 1b's restore (both parts).  A clone-local sentinel is dropped before the first mutant and cleared only
#  after the restore passes both clearance parts.  Run from a frozen copy of THIS script.
set -u
S=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/fbcmd
C=/tmp/gx567
F=src/devices/dev_fbctrl.c
OUT=$S/killtable3a
PROBE=$S/killtable2/probe.v2.frozen.py
mkdir -p "$OUT"
echo "TABLE3A start $(date '+%F %T')" | tee "$OUT/SCORES.txt"
[ -e "$C/.MUTANT" ] && { echo "clone already carries a sentinel -- stop" | tee -a "$OUT/SCORES.txt"; exit 9; }
cmp -s "$S/dev_fbctrl.fix567.c" "$C/$F" || { echo "clone's $F is not the fix -- stop" | tee -a "$OUT/SCORES.txt"; exit 9; }
[ "$C/gxemul" -nt "$C/$F" ] || { echo "clone's binary is older than $F -- stop" | tee -a "$OUT/SCORES.txt"; exit 9; }
echo "probe md5 $(md5sum < "$PROBE" | cut -c1-32) (kill table 2's frozen v2)" | tee -a "$OUT/SCORES.txt"
run_probe() {   # $1 label, $2 binary
    python3 -u "$PROBE" "$2" > "$OUT/$1.raw" 2>&1
    local rc=$?
    printf '%-14s rc=%s %s %s last=%s\n' "$1" "$rc" "$(grep -a '^FBCMD_RESULT' "$OUT/$1.raw")" \
        "$(grep -a '^FBCMD_CONTROL' "$OUT/$1.raw")" "$(tail -1 "$OUT/$1.raw")" | tee -a "$OUT/SCORES.txt"
    grep -aE '^  [^ ].* got=[^ ]* +want=[^ ]* +FAIL  ' "$OUT/$1.raw" | sed -E 's/ +FAIL  .*//; s/^  */      red: /' >> "$OUT/SCORES.txt"
}
build() {       # $1 label
    (cd "$C" && rm -f src/cpus/*.o src/devices/dev_fbctrl.o && make -j4 > "$OUT/build_$1.log" 2>&1)
    local rc=$?
    [ "$C/gxemul" -nt "$C/$F" ] || { echo "$1: BINARY NOT FRESH (make rc=$rc) -- stop, sentinel kept" | tee -a "$OUT/SCORES.txt"; exit 9; }
}
echo "base: the fix, as left by table 1b's restore" | tee -a "$OUT/SCORES.txt"
run_probe base "$C/gxemul"
echo "SCRATCH CLONE (#567 kill table 3a): $F carries a mutant" > "$C/.MUTANT"
for m in E15_sdnodisp E16_sdbound0 E17_shbound1 E18_sdbound3 E19_shbound3 E20_latchacc E21_latchread; do
    cp "$S/mutants_d/$m.c" "$C/$F"
    build "$m"
    run_probe "$m" "$C/gxemul"
done
echo "--- restore" | tee -a "$OUT/SCORES.txt"
cp "$S/dev_fbctrl.fix567.c" "$C/$F"
build restore
cmp -s "$S/dev_fbctrl.fix567.c" "$C/$F" && echo "part 1: $F == the fix" | tee -a "$OUT/SCORES.txt" \
    || { echo "part 1 FAILED -- sentinel kept" | tee -a "$OUT/SCORES.txt"; exit 9; }
[ "$C/gxemul" -nt "$C/$F" ] && echo "part 2: binary newer than $F" | tee -a "$OUT/SCORES.txt" \
    || { echo "part 2 FAILED -- sentinel kept" | tee -a "$OUT/SCORES.txt"; exit 9; }
echo "restored binary md5 $(md5sum < "$C/gxemul" | cut -c1-32)" | tee -a "$OUT/SCORES.txt"
rm -f "$C/.MUTANT"; echo "sentinel cleared" | tee -a "$OUT/SCORES.txt"
echo "TABLE3A end $(date '+%F %T')" | tee -a "$OUT/SCORES.txt"
echo TABLE3A_DONE | tee -a "$OUT/SCORES.txt"
