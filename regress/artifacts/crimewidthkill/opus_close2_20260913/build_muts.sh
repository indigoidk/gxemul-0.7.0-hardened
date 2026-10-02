#!/bin/bash
# build each mutant in the clone, then RESTORE with two-part clearance
set -u
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
C=/tmp/gxopus529c2
F=src/devices/dev_sgi_ip32.c
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_close2
OUT=/tmp/close2
mkdir -p $OUT/builds $OUT/diffs
cp "$SP/mutants_c2.py" $OUT/mutants_c2.FROZEN.py
cd "$C" || exit 2
for m in rd_hi_lh soft_gate rd_hi_lb rd_lh_all; do
    echo "mutant $m" > "$C/.MUTANT"
    cp "$SEC/$F" "$F"
    if ! python3 $OUT/mutants_c2.FROZEN.py $m "$F"; then echo "TXTFAIL $m"; continue; fi
    diff -u "$SEC/$F" "$F" > $OUT/diffs/$m.diff
    rm -f src/devices/dev_sgi_ip32.o
    make -j4 > $OUT/builds/$m.log 2>&1; rc=$?
    if [ $rc -ne 0 ] || ! [ gxemul -nt "$F" ] || ! [ src/devices/dev_sgi_ip32.o -nt "$F" ]; then
        echo "BUILD_FAIL $m rc=$rc"; grep -E 'error' $OUT/builds/$m.log | head -5; continue
    fi
    cp gxemul $OUT/builds/gx_$m
    echo "BUILT $m rc=0 $(md5sum < gxemul | cut -c1-8) difflines=$(grep -c '^[+-][^+-]' $OUT/diffs/$m.diff)"
done
# ---- RESTORE ----
cp "$SEC/$F" "$F"
rm -f src/devices/dev_sgi_ip32.o
make -j4 > $OUT/builds/restore.log 2>&1; rc=$?
if cmp -s "$F" "$SEC/$F" && [ gxemul -nt "$F" ] && [ $rc -eq 0 ]; then
    cmp -s gxemul /tmp/gx529c2_base && echo "RESTORED binary == baseline (byte-identical)" || echo "RESTORED binary differs (timestamp only?)"
    rm -f "$C/.MUTANT"; echo "RESTORE_OK cmp clean, gxemul -nt source, sentinel removed"
else
    echo "RESTORE_FAILED -- sentinel left in place"
fi
ls $OUT/builds/
echo BUILD_DONE
