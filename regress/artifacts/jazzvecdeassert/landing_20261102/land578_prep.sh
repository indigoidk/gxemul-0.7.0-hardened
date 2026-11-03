#!/bin/bash
# land578_prep.sh -- #578 landing, part 1 (WSL): apply the fix to SEC and est (dev_jazz.c is a DIVERGENCE-SET file: the two copies differ
# elsewhere, the jazz_jazzio function is byte-identical, and apply_fix578c.py lands in both), copy the shipped probe and the gate, propagate
# each build tree's OWN source (build/ compiles est's dev_jazz.c; build-asan/ and /tmp/gxsec-build compile SEC's) and REBUILD each, then the
# two-part clearance per tree against the tree's reference copy -- est for build/, SEC for the other two.  Run only while no gate, hook or
# table is running.  The gate run (./run.sh 1 4) and the commit are parts 2 and 3.
set -u
P=/mnt/c/DocumentNoSnc/CC/GXEMUL; W=$P/_scratchpad/w578; SEC=$P/GXEMUL-SEC; EST=$P/est
echo "land578 prep start $(date '+%F %T')"
echo "before:"; md5sum $SEC/src/devices/dev_jazz.c $EST/src/devices/dev_jazz.c $P/build/src/devices/dev_jazz.c $P/build-asan/src/devices/dev_jazz.c /tmp/gxsec-build/src/devices/dev_jazz.c | cut -c1-12,34- | sed 's#/mnt/c/DocumentNoSnc/CC/GXEMUL/##'
python3 $W/apply_fix578c.py $SEC/src/devices/dev_jazz.c && python3 $W/apply_fix578c.py $EST/src/devices/dev_jazz.c || { echo "APPLY FAILED"; exit 1; }
grep -c '#578: no deassert here' $SEC/src/devices/dev_jazz.c $EST/src/devices/dev_jazz.c
cp -p $W/jazz_vector_probe.py $SEC/regress/jazz_vector_probe.py && echo "probe copied to regress/ (md5 $(md5sum $SEC/regress/jazz_vector_probe.py | cut -c1-12))"
cp -p $W/gate_mips.NEW2.sh $SEC/regress/gate_mips.sh && echo "gate_mips.sh staged from gate_mips.NEW2.sh"
for spec in "build:$EST" "build-asan:$SEC" "/tmp/gxsec-build:$SEC"; do
    T=${spec%%:*}; REF=${spec##*:}; case $T in /*) ;; *) T=$P/$T ;; esac
    echo "=== $T (reference: $(basename $REF))"; [ -d $T/src/devices ] || { echo "no tree at $T"; continue; }
    cp -p $REF/src/devices/dev_jazz.c $T/src/devices/dev_jazz.c
    ( cd $T && rm -f src/devices/dev_jazz.o && make -j4 > $W/landing/make_land578_$(basename $T).log 2>&1 ); rc=$?
    echo "make rc=$rc"; cmp -s $T/src/devices/dev_jazz.c $REF/src/devices/dev_jazz.c && echo "part 1 cmp CLEAN vs $(basename $REF)" || echo "part 1 cmp DIFFERS"
    [ $T/gxemul -nt $T/src/devices/dev_jazz.c ] && echo "part 2 binary newer: yes $(ls -la --time-style=+%T $T/gxemul | awk '{print $6}')" || echo "part 2 binary newer: NO -- STALE"
done
echo "est/: source tree, part 2 N/A"
echo "after:"; md5sum $SEC/src/devices/dev_jazz.c $EST/src/devices/dev_jazz.c $P/build/src/devices/dev_jazz.c $P/build-asan/src/devices/dev_jazz.c /tmp/gxsec-build/src/devices/dev_jazz.c | cut -c1-12,34- | sed 's#/mnt/c/DocumentNoSnc/CC/GXEMUL/##'
echo "LAND578_PREP_DONE $(date '+%F %T')"
