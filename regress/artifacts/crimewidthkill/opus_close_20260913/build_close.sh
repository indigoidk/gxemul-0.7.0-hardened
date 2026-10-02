#!/bin/bash
# build every mutant binary in the scratch clone, then restore the clone to the SEC working set (two-part clearance)
set -u
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
C=/tmp/gxopus529close
F=src/devices/dev_sgi_ip32.c
MUT=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/mutants_close.py
OUT=/tmp/close529
mkdir -p $OUT/builds $OUT/diffs
cp "$MUT" $OUT/mutants_close.FROZEN.py
cd "$C" || exit 2
for m in lt_len c_dog rearm4 pre4 rearm_time ctl_collide wst_mc2 lt_blk rd_hi lt_wl wnz_lbl acc4_210; do
    echo "mutant $m" > "$C/.MUTANT"
    cp "$SEC/$F" "$F"
    if ! python3 $OUT/mutants_close.FROZEN.py $m "$F"; then echo "BUILD_FAIL $m (mutant text)"; continue; fi
    diff -u "$SEC/$F" "$F" > $OUT/diffs/$m.diff
    rm -f src/devices/dev_sgi_ip32.o
    make -j4 > $OUT/builds/$m.log 2>&1; rc=$?
    if [ $rc -ne 0 ] || ! [ gxemul -nt "$F" ] || ! [ src/devices/dev_sgi_ip32.o -nt "$F" ]; then
        echo "BUILD_FAIL $m rc=$rc"; grep -E 'error|warning' $OUT/builds/$m.log | head -5; continue
    fi
    cp gxemul $OUT/builds/gx_$m
    echo "BUILT $m rc=0 fresh $(md5sum < gxemul | cut -c1-8) diff_lines=$(grep -c '^[+-][^+-]' $OUT/diffs/$m.diff)"
    grep -E 'warning' $OUT/builds/$m.log | head -3
done
# ---- restore: source from SEC, rebuild, then BOTH parts of the clearance before the sentinel goes ----
cp "$SEC/$F" "$F"
rm -f src/devices/dev_sgi_ip32.o
make -j4 > $OUT/builds/restore.log 2>&1; rc=$?
if cmp -s "$F" "$SEC/$F" && [ gxemul -nt "$F" ] && [ $rc -eq 0 ]; then
    cmp -s gxemul /tmp/gx529close_base && echo "RESTORED binary == baseline binary (byte-identical)" || echo "RESTORED binary differs from baseline copy (timestamps in build?)"
    rm -f "$C/.MUTANT"; echo "RESTORE_OK cmp clean, gxemul -nt source, sentinel removed"
else
    echo "RESTORE_FAILED -- sentinel left in place"
fi
ls $OUT/builds/
echo BUILD_DONE
