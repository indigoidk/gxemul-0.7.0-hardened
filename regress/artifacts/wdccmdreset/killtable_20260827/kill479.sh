#!/bin/bash
S=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
M=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/m479
O=/tmp/gx479k; mkdir -p "$O"
build_run () {
    gcc -O2 -std=c99 -I"$S/src/include" -I"$S/src/include/thirdparty" \
        -ffunction-sections -fdata-sections -Wl,--gc-sections \
        -o "$O/$2" "$1/regress/diff_wdc_identify.c" 2> "$O/$2.cc"
    if [ $? -ne 0 ]; then echo COMPILEFAIL; return; fi
    "$O/$2" > "$O/$2.out" 2>&1
    grep -c '^  FAIL' "$O/$2.out"
}
echo "=== BASELINE ==="
b=$(build_run "$S" base)
nrows=$(grep -oE '^[0-9]+ rows' "$O/base.out" | head -1 | cut -d' ' -f1)
echo "  $nrows rows, $b failures"
[ "$b" != "0" ] && { echo "  *** BASELINE NOT GREEN ***"; grep '^  FAIL' "$O/base.out" | sed 's/^/    /'; exit 1; }
echo
printf "  %-14s %-9s %s\n" MUTANT VERDICT "rows that carried the kill"
printf "  %-14s %-9s %s\n" ------ ------- --------------------------
for d in "$M"/*/; do
    n=$(basename "$d")
    f=$(build_run "$d" "$n")
    if [ "$f" = "COMPILEFAIL" ]; then
        printf "  %-14s %-9s %s\n" "$n" "KILLED" "does not compile"
    elif [ "$f" = "0" ]; then
        printf "  %-14s %-9s %s\n" "$n" "*ESCAPED*" "(clean sweep of $nrows rows)"
    else
        why=$(grep '^  FAIL' "$O/$n.out" | sed 's/^  FAIL  *//' | cut -c1-37 \
              | sed 's/ *$//' | paste -sd';' - | cut -c1-90)
        printf "  %-14s %-9s %s\n" "$n" "KILLED" "$f red: $why"
    fi
done
