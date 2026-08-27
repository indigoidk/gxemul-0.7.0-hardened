#!/bin/bash
#  #480 kill table.  The candidate detector (83 rows) against the three CALL-SITE
#  mutants that swept #479's 80 rows byte-identically, plus the clause-(b) control.
S=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
C=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/r480
O=/tmp/gx480; mkdir -p "$O"

build_run () {
    gcc -O2 -std=c99 -I"$S/src/include" -I"$S/src/include/thirdparty" \
        -ffunction-sections -fdata-sections -Wl,--gc-sections \
        -o "$O/$2" "$1/regress/diff_wdc_identify.c" 2> "$O/$2.cc"
    if [ $? -ne 0 ]; then echo COMPILEFAIL; return; fi
    "$O/$2" > "$O/$2.out" 2>&1
    grep -c '^  FAIL' "$O/$2.out"
}

echo "=== BASELINE (candidate detector, unmutated product code) ==="
b=$(build_run "$C" base)
echo "  failures: $b"
tail -2 "$O/base.out"
echo
echo "  the three new rows on the baseline:"
grep -E 'same-opcode reissue|rejected command still|refill command starts' "$O/base.out"
echo
echo "=== MUTANTS ==="
printf "  %-16s %-8s %s\n" MUTANT FAILURES "rows that carried the kill"
for m in M11_sameop M4_afterguard M23_exemptfill Mb_revert; do
    n=$(build_run "$O/$m" "bin_$m")
    printf "  %-16s %-8s " "$m" "$n"
    if [ "$n" = "COMPILEFAIL" ]; then
        echo "(does not compile)"
    elif [ "$n" = "0" ]; then
        echo "*** ESCAPED ***"
    else
        grep '^  FAIL' "$O/bin_$m.out" | sed 's/^  FAIL //' | cut -c1-40 | tr '\n' ';' | sed 's/;$//'
        echo
    fi
done
