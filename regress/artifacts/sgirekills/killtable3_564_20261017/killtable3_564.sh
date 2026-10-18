#!/bin/bash
#  killtable3_564.sh <mutant .c dir> -- #564's kill table 3, for the pass-2 REPAIR, in a SCRATCH CLONE (never a project
#  build tree).  Run it from a frozen copy.
#  1. Baseline NAMED: the post-repair working set.  The clone is a copy of the round's fix build with GXEMUL-SEC's
#     working-tree dev_sgi_re.c copied in and REBUILT before mutant 1; it must cmp equal and its binary be newer.
#  2. Every mutant built into its own binary under a clone-local .MUTANT sentinel; the tree is restored and the
#     baseline rebuilt afterwards, the sentinel removed only after cmp + freshness both pass.
#  3. The detector, from a FROZEN copy (its md5 in every log), THREE at a time against: base, the null medium
#     (/bin/true), HEAD 2951694f's build (clause (a) for the repaired instrument) and each mutant.  Logs under raw3/,
#     each with its completion sentinel checked.
set -u
K=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/sgirekills/killtable3_564_20261017
WT=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/src/devices/dev_sgi_re.c
PROBE=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/sgi_mte_decline_probe.py
HEADBIN=/tmp/gxsk_2951694f/gxemul
MUTSRC=$1
C=/tmp/gxsk_564kt3; BINS=/tmp/gxsk_564bins3; FROZEN=/tmp/sgi_mte_decline_probe.kt3.py
mkdir -p "$K/raw3"; rm -rf "$BINS"; mkdir -p "$BINS"
[ -e "$C/.MUTANT" ] && { echo "REFUSE: $C carries a .MUTANT sentinel from an earlier run"; cat "$C/.MUTANT"; exit 9; }
[ -x "$HEADBIN" ] || { echo "REFUSE: no HEAD build at $HEADBIN"; exit 9; }
rm -rf "$C"; cp -a /tmp/gxsk_564fix "$C" || exit 9
cd "$C"
cp "$WT" src/devices/dev_sgi_re.c; rm -f src/devices/dev_sgi_re.o
make -j4 > make_baseline.log 2>&1
cmp -s src/devices/dev_sgi_re.c "$WT" || { echo "REFUSE: the clone's dev_sgi_re.c is not the working tree's"; exit 9; }
[ gxemul -nt src/devices/dev_sgi_re.c ] || { echo "REFUSE: the clone's baseline binary is not fresh"; exit 9; }
cp "$PROBE" "$FROZEN"; PM=$(md5sum < "$FROZEN" | cut -c1-32)
echo "# kill table 3 #564, $(date '+%Y-%m-%d %H:%M:%S'); baseline dev_sgi_re.c $(md5sum < "$WT" | cut -c1-32); probe md5 $PM"
cp gxemul "$BINS/base"; cp /bin/true "$BINS/null"; cp "$HEADBIN" "$BINS/head"
NAMES=$(ls "$MUTSRC" | sed -n 's/\.c$//p')
echo "$(echo "$NAMES" | wc -w) mutants"
for n in $NAMES; do
    echo "mutant $n" > "$C/.MUTANT"
    cp "$MUTSRC/$n.c" src/devices/dev_sgi_re.c
    rm -f src/devices/dev_sgi_re.o
    if make -j4 > "make_$n.log" 2>&1 && [ gxemul -nt src/devices/dev_sgi_re.c ]; then
        cp gxemul "$BINS/$n"; echo "built $n"
    else
        echo "BUILD FAIL $n"; tail -5 "make_$n.log"
    fi
done
cp "$WT" src/devices/dev_sgi_re.c; rm -f src/devices/dev_sgi_re.o
make -j4 > make_restore.log 2>&1
if cmp -s src/devices/dev_sgi_re.c "$WT" && [ gxemul -nt src/devices/dev_sgi_re.c ]; then
    rm -f "$C/.MUTANT"; echo "RESTORED: clone source cmp-equal to the working tree and its binary fresh"
else
    echo "RESTORE NOT VERIFIED -- sentinel kept"; fi
run1() {  # run1 <name> <binary>
    { echo "# probe md5 $PM; binary $2 ($1)"; python3 -u "$FROZEN" "$2" "$1"; } > "$K/raw3/$1.out" 2>&1
}
set -- base null head $NAMES
while [ $# -gt 0 ]; do
    batch=""
    for i in 1 2 3; do [ $# -gt 0 ] && { batch="$batch $1"; shift; }; done
    pids=""
    for x in $batch; do run1 "$x" "$BINS/$x" & pids="$pids $!"; done
    for p in $pids; do wait $p; done
    for x in $batch; do
        [ "$(tail -1 "$K/raw3/$x.out")" = "MTEDECL_DONE" ] || echo "WARNING: $x has no completion sentinel"
        printf '%-10s %s\n' "$x" "$(grep -o 'MTEDECL_RESULT=[0-9]*/[0-9]*' "$K/raw3/$x.out")"
    done
done
rm -f "$FROZEN"
echo KILLTABLE3_564_DONE
