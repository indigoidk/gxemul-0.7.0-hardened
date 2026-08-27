#!/bin/bash
S=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
C=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/r480b
O=/tmp/gx480b; mkdir -p "$O"
build_run () {
    gcc -O2 -std=c99 -I"$S/src/include" -I"$S/src/include/thirdparty" \
        -ffunction-sections -fdata-sections -Wl,--gc-sections \
        -o "$O/$2" "$1/regress/diff_wdc_identify.c" 2> "$O/$2.cc"
    if [ $? -ne 0 ]; then echo COMPILEFAIL; return; fi
    "$O/$2" > "$O/$2.out" 2>&1
    grep -c '^  FAIL' "$O/$2.out"
}
echo "=== BASELINE ==="
b=$(build_run "$C" base)
echo "  failures: $b"
tail -2 "$O/base.out"
grep -E 'absent-drive command|every opcode clears' "$O/base.out"
echo
printf "  %-18s %-6s %s\n" MUTANT FAILS "carried by"
for m in M11_sameop M4_afterguard M23_exemptfill Mb_revert \
         Mq_identify Mq_read Mq_readmulti Mq_atapiid Mq_writemulti \
         Mq_idp Mq_setfeat Mq_softreset Mq_pktretry p1_belowguard1; do
    n=$(build_run "$O/$m" "bin_$m")
    printf "  %-18s %-6s " "$m" "$n"
    if [ "$n" = "COMPILEFAIL" ]; then echo "(does not compile)"
    elif [ "$n" = "0" ]; then echo "*** ESCAPED ***"
    else grep '^  FAIL' "$O/bin_$m.out" | sed 's/^  FAIL //' | cut -c1-36 | tr '\n' ';'; echo; fi
done
