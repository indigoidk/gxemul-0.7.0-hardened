#!/bin/bash
#  killtable_564.sh -- #564's kill table, in a SCRATCH CLONE (never a project build tree).  Run it from a frozen copy.
#  1. Baseline NAMED: the post-fix working set -- the clone's dev_sgi_re.c must cmp equal to GXEMUL-SEC's working tree
#     file before mutant 1, and the clone's binary must be newer than it.
#  2. Every mutant built into its own binary (clone-local .MUTANT sentinel while the tree is mutated); the tree is
#     restored and the baseline REBUILT afterwards, the sentinel removed only after cmp + freshness both pass.
#  3. The detector, from a FROZEN copy (its md5 in every log), run 2 at a time against: base, the null medium
#     (/bin/true), and each mutant.  Logs land under raw/ here, each with its completion sentinel checked.
set -u
K=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/sgirekills/killtable_564_20261017
WT=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/src/devices/dev_sgi_re.c
PROBE=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/sgi_mte_decline_probe.py
MUTSRC=$1                       # dir of <name>.c from mutants_564.py (table 1) or mutants_564b.py (table 2)
RAW=${2:-raw}                   # the log subdir: raw (table 1), raw2 (table 2)
C=/tmp/gxsk_564kt; BINS=/tmp/gxsk_564bins; FROZEN=/tmp/sgi_mte_decline_probe.kt564.py
mkdir -p "$K/$RAW"; rm -rf "$BINS"; mkdir -p "$BINS"
[ -e "$C/.MUTANT" ] && { echo "REFUSE: $C carries a .MUTANT sentinel from an earlier run"; cat "$C/.MUTANT"; exit 9; }
rm -rf "$C"; cp -a /tmp/gxsk_564fix "$C" || exit 9
cmp -s "$C/src/devices/dev_sgi_re.c" "$WT" || { echo "REFUSE: the clone's dev_sgi_re.c is not the working tree's"; exit 9; }
[ "$C/gxemul" -nt "$C/src/devices/dev_sgi_re.c" ] || { echo "REFUSE: the clone's binary is not fresh"; exit 9; }
cp "$PROBE" "$FROZEN"; PM=$(md5sum < "$FROZEN" | cut -c1-32)
echo "# kill table #564, $(date '+%Y-%m-%d %H:%M:%S'); baseline dev_sgi_re.c $(md5sum < "$WT" | cut -c1-32); probe md5 $PM"
cp "$C/gxemul" "$BINS/base"
NAMES=$(ls "$MUTSRC" | sed -n 's/\.c$//p')
echo "$(echo "$NAMES" | wc -w) mutants"
cd "$C"
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
    { echo "# probe md5 $PM; binary $2 ($1)"; python3 -u "$FROZEN" "$2" "$1"; } > "$K/$RAW/$1.out" 2>&1
}
cp /bin/true "$BINS/null"
LIST="base null $NAMES"
set -- $LIST
while [ $# -gt 0 ]; do
    a=$1; shift; b=${1:-}; [ -n "$b" ] && shift
    run1 "$a" "$BINS/$a" & pa=$!
    if [ -n "$b" ]; then run1 "$b" "$BINS/$b" & pb=$!; wait $pb; fi
    wait $pa
    for x in $a $b; do
        [ "$(tail -1 "$K/$RAW/$x.out")" = "MTEDECL_DONE" ] || echo "WARNING: $x has no completion sentinel"
        printf '%-10s %s\n' "$x" "$(grep -o 'MTEDECL_RESULT=[0-9]*/[0-9]*' "$K/$RAW/$x.out")"
    done
done
rm -f "$FROZEN"
echo KILLTABLE_564_DONE
