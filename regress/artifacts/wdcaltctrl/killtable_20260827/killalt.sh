#!/bin/bash
S=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
O=/tmp/gxaltk; mkdir -p "$O"
build_run () {
    gcc -O2 -std=c99 -I"$S/src/include" -I"$S/src/include/thirdparty" \
        -ffunction-sections -fdata-sections -Wl,--gc-sections \
        -o "$O/$2" "$1/regress/diff_wdc_identify.c" 2> "$O/$2.cc"
    if [ $? -ne 0 ]; then echo COMPILEFAIL; return; fi
    "$O/$2" > "$O/$2.out" 2>&1
    grep -c '^  FAIL' "$O/$2.out"
}
echo "=== BASELINE (repo tree, fix applied) ==="
b=$(build_run "$S" base)
echo "  failures: $b"
tail -2 "$O/base.out"
echo
printf "  %-16s %-6s %s\n" MUTANT FAILS "carried by"
for m in Mb_revert Md_nohelper Md_nolatch Md_widemask Md_bitswap Md_qualcmd Mo_nienzero Mo_nien4bit Mo_sigalways Mc_null; do
    n=$(build_run "$O/$m" "bin_$m")
    printf "  %-16s %-6s " "$m" "$n"
    if [ "$n" = "COMPILEFAIL" ]; then echo "(does not compile -- clause (c) kill)"
    elif [ "$n" = "0" ]; then echo "*** ESCAPED ***"
    else grep '^  FAIL' "$O/bin_$m.out" | sed 's/^  FAIL //' | cut -c1-34 | tr '\n' ';'; echo; fi
done
