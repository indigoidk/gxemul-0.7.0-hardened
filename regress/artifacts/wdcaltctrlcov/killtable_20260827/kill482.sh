#!/bin/bash
S=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
C=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/r482
O=/tmp/gx482k; mkdir -p "$O"
build_run () {
    gcc -O2 -std=c99 -I"$S/src/include" -I"$S/src/include/thirdparty" \
        -ffunction-sections -fdata-sections -Wl,--gc-sections \
        -o "$O/$2" "$1/regress/diff_wdc_identify.c" 2> "$O/$2.cc"
    if [ $? -ne 0 ]; then echo COMPILEFAIL; return; fi
    "$O/$2" > "$O/$2.out" 2>&1
    grep -c '^  FAIL' "$O/$2.out"
}
echo "=== BASELINE (the #482 candidate) ==="
b=$(build_run "$C" b482base); echo "  failures: $b"; tail -2 "$O/b482base.out"
echo
printf "  %-16s %-6s %s\n" MUTANT FAILS "carried by"
for m in Mo_abt_atapi Mo_abt_wip Mo_abt_ring Mo_hob Mb_revert; do
    n=$(build_run "$O/$m" "bin_$m")
    printf "  %-16s %-6s " "$m" "$n"
    if [ "$n" = "COMPILEFAIL" ]; then echo "(does not compile)"
    elif [ "$n" = "0" ]; then echo "*** STILL ESCAPES -- the row is decoration ***"
    else grep '^  FAIL' "$O/bin_$m.out" | sed 's/^  FAIL //' | cut -c1-36 | tr '\n' ';'; echo; fi
done
