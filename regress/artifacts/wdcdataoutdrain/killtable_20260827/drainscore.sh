#!/bin/bash
#  Score each candidate drain fix against the FOUR measured entrances AND against
#  the 45 pre-existing rows, so a fix that closes the defect by breaking something
#  else is not scored as a win.
#
#    empty     occupancy 0,   3-byte store          (first=0xdd)
#    empty8    occupancy 0,   8-byte store          (first=0xdd)
#    leftover  occupancy 512 UNREAD, 8-byte store   (first=0xbe)   <- grok
#    wr+pkt    WRITE live + a legal CDB dispatch    (first=0x5a)   <- fable
S=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
V=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/dvar
O=/tmp/gxdvar
mkdir -p "$O"

lbl () { if [ "$1" = "0" ]; then echo CLOSED; else echo OPEN; fi; }

printf "  %-10s %-7s %-7s %-9s %-8s %s\n" VARIANT empty empty8 leftover wr+pkt "other rows"
printf "  %-10s %-7s %-7s %-9s %-8s %s\n" ------- ----- ------ -------- ------ ----------
for d in "$V"/*/; do
    n=$(basename "$d")
    gcc -O2 -std=c99 -I"$S/src/include" -I"$S/src/include/thirdparty" \
        -ffunction-sections -fdata-sections -Wl,--gc-sections \
        -o "$O/$n" "$d/regress/diff_wdc_identify.c" 2> "$O/$n.cc"
    if [ $? -ne 0 ]; then
        printf "  %-10s %s\n" "$n" "DOES NOT COMPILE"
        head -4 "$O/$n.cc" | sed 's/^/       /'
        continue
    fi
    "$O/$n" > "$O/$n.out" 2>&1
    e1=$(grep -c '^  FAIL an empty ring writes'   "$O/$n.out")
    e2=$(grep -c '^  FAIL an 8-byte write drains' "$O/$n.out")
    e3=$(grep -c '^  FAIL leftover payload'       "$O/$n.out")
    e4=$(grep -c '^  FAIL a CDB dispatch'         "$O/$n.out")
    e5=$(grep -c '^  FAIL a legal write after'      "$O/$n.out")
    tot=$(grep -c '^  FAIL' "$O/$n.out")
    oth=$(( tot - e1 - e2 - e3 - e4 - e5 ))
    if [ "$oth" -eq 0 ]; then othtxt="all green"; else othtxt="*** $oth BROKEN ***"; fi
    printf "  %-10s %-7s %-7s %-9s %-8s %s\n" \
        "$n" "$(lbl $e1)" "$(lbl $e2)" "$(lbl $e3)" "$(lbl $e4)" "$(lbl $e5)" "$othtxt"
    if [ "$oth" -ne 0 ]; then
        grep '^  FAIL' "$O/$n.out" \
          | grep -vE 'empty ring writes|8-byte write drains|leftover payload|a CDB dispatch|a legal write after' \
          | sed 's/^/       /'
    fi
done
