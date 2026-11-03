#!/bin/bash
# land577_prep.sh -- #577 landing, part 1 (WSL): apply the fix to SEC and est (shared file: byte-identical), copy the shipped probe,
# propagate cpu_sh.c into the three build trees and REBUILD each (rm src/cpus/*.o first), then the two-part clearance per tree.
# Run only while no gate, hook or table is running.  The gate run and the commit are parts 2 and 3.
set -u
P=/mnt/c/DocumentNoSnc/CC/GXEMUL; W=$P/_scratchpad/w577; SEC=$P/GXEMUL-SEC; EST=$P/est
echo "land577 prep start $(date '+%F %T')"
md5sum $SEC/src/cpus/cpu_sh.c $EST/src/cpus/cpu_sh.c | cut -c1-12 | uniq -c
python3 $W/apply_fix577.py $SEC/src/cpus/cpu_sh.c && python3 $W/apply_fix577.py $EST/src/cpus/cpu_sh.c || { echo "APPLY FAILED"; exit 1; }
cmp $SEC/src/cpus/cpu_sh.c $EST/src/cpus/cpu_sh.c && echo "SEC/est cpu_sh.c byte-identical"
cp -p $W/sh_tlbmulti_probe.NEW.py $SEC/regress/sh_tlbmulti_probe.py && echo "probe copied to regress/"
for T in $P/build $P/build-asan /tmp/gxsec-build; do
    echo "=== $T"; [ -d $T/src/cpus ] || { echo "no tree at $T"; continue; }
    cp -p $SEC/src/cpus/cpu_sh.c $T/src/cpus/cpu_sh.c
    ( cd $T && rm -f src/cpus/*.o && make -j4 > $W/make_land577_$(basename $T).log 2>&1 ); rc=$?
    echo "make rc=$rc"; cmp -s $T/src/cpus/cpu_sh.c $SEC/src/cpus/cpu_sh.c && echo "part 1 cmp CLEAN" || echo "part 1 cmp DIFFERS"
    [ $T/gxemul -nt $T/src/cpus/cpu_sh.c ] && echo "part 2 binary newer: yes $(ls -la --time-style=+%T $T/gxemul | awk '{print $6}')" || echo "part 2 binary newer: NO -- STALE"
done
echo "est/: source tree, part 2 N/A"
echo "LAND577_PREP_DONE $(date '+%F %T')"
