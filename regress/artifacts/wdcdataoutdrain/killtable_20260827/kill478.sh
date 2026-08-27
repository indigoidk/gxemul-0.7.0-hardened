#!/bin/bash
#  #478 kill table.  A mutant is KILLED if the 50-row detector reddens; the row that
#  carried the kill is named, because "killed" without a row is not a measurement.
S=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
M=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/m478
D=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/drain
O=/tmp/gx478
mkdir -p "$O"

build_run () {
    gcc -O2 -std=c99 -I"$S/src/include" -I"$S/src/include/thirdparty" \
        -ffunction-sections -fdata-sections -Wl,--gc-sections \
        -o "$O/$2" "$1/regress/diff_wdc_identify.c" 2> "$O/$2.cc"
    if [ $? -ne 0 ]; then echo COMPILEFAIL; return; fi
    "$O/$2" > "$O/$2.out" 2>&1
    grep -c '^  FAIL' "$O/$2.out"
}

echo "=== BASELINE: the shipped tree against the detector ==="
b=$(build_run "$D" base)
nrows=$(grep -oE '^[0-9]+ rows' "$O/base.out" | head -1 | cut -d' ' -f1)
echo "  baseline: $nrows rows, $b failures"
if [ "$b" != "0" ]; then
    echo "  *** BASELINE NOT GREEN -- the table below would be meaningless ***"
    grep '^  FAIL' "$O/base.out" | sed 's/^/    /'
    exit 1
fi
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
        why=$(grep '^  FAIL' "$O/$n.out" | sed 's/^  FAIL  *//' \
              | cut -c1-37 | sed 's/ *$//' | paste -sd';' - | cut -c1-92)
        printf "  %-14s %-9s %s\n" "$n" "KILLED" "$f red: $why"
    fi
done
