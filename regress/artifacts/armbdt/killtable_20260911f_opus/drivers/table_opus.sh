#!/usr/bin/env bash
#  opus524 PASS C kill table -- scratch clone, no project tree is written.
set -euo pipefail
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
REL=src/cpus/cpu_arm_instr.c
CLONE=/tmp/gxopus524c
BASEFILE=/tmp/opus524_baseline.c
OUT=/tmp/opus524_out
MUT=/tmp/opus524_frozen/mutate_opus.py     # FROZEN COPY, per the frozen-copy rule
PROBE=/tmp/opus524_frozen/arm_bdt_probe.py # FROZEN COPY of the 32-row detector
mkdir -p "$OUT"

git -C "$SEC" show 8d372aa:"$REL" > "$BASEFILE"
printf '[BASELINE] 8d372aa:%s  %s bytes\n' "$REL" "$(wc -c < "$BASEFILE")"
n=$(grep -cF 'cpu->memory_rw(cpu, cpu->mem, addr, data,' "$BASEFILE" || true)
[ "$n" -eq 2 ] || { echo "ERROR: baseline pin failed ($n != 2)"; exit 1; }
echo "[PIN] baseline carries the unmasked call exactly 2 times"

touch "$CLONE/.MUTANT"
echo "[SENTINEL] dropped $CLONE/.MUTANT"
: > "$OUT/SCORES.txt"

for leg in BASE M_MASK1 M_MASK15 M_POPP_NONE M_POPP_WEAK M_POPW_WEAK M_SBIT_NONE M_NPMASK; do
    echo "------------------------------------------------ leg $leg"
    python3 "$MUT" "$leg" "$CLONE/$REL" "$BASEFILE"
    echo "[MUTANT TEXT AS BUILT]"
    grep -n 'memory_rw(cpu, cpu->mem' "$CLONE/$REL" | sed 's/^/    /'
    rm -f "$CLONE/src/cpus/"*.o
    make -C "$CLONE" -j4 > "$OUT/build_${leg}.log" 2>&1 || { echo "BUILD FAILED $leg"; tail -20 "$OUT/build_${leg}.log"; exit 1; }
    [ "$CLONE/gxemul" -nt "$CLONE/$REL" ] || { echo "ERROR: binary not newer than source for $leg"; exit 1; }
    echo "[FRESH] binary newer than source"
    python3 -u "$PROBE" "$CLONE/gxemul" "$leg" > "$OUT/probe_${leg}.raw" 2>&1
    grep -q ARMBDT_WITNESS_DONE "$OUT/probe_${leg}.raw" || { echo "ERROR: probe incomplete for $leg"; exit 1; }
    s=$(grep -oE 'SCORE [0-9]+/[0-9]+' "$OUT/probe_${leg}.raw" | head -1)
    f=$(grep -E '^FAILING:' "$OUT/probe_${leg}.raw" | head -1)
    echo "RESULT $leg: $s   $f"
    printf '%-14s %s   %s\n' "$leg" "$s" "$f" >> "$OUT/SCORES.txt"
done

echo "=== RESTORE (against GIT, not my own backup) ==="
git -C "$SEC" show 8d372aa:"$REL" > "$CLONE/$REL"
git -C "$SEC" show 8d372aa:"$REL" | cmp -s - "$CLONE/$REL" || { echo "ERROR: restore cmp failed"; exit 1; }
echo "[VERIFIED] restored source == 8d372aa"
rm -f "$CLONE/src/cpus/"*.o
make -C "$CLONE" -j4 > "$OUT/build_RESTORE.log" 2>&1
[ "$CLONE/gxemul" -nt "$CLONE/$REL" ] || { echo "ERROR: restored binary not newer"; exit 1; }
echo "[VERIFIED] binary newer than restored source"
rm -f "$CLONE/.MUTANT"
echo "[SENTINEL] cleared"
echo "=== TABLE ==="
cat "$OUT/SCORES.txt"
echo "OPUS524_TABLE_DONE"
