#!/bin/bash
# Stage F: copy every log, the instrument, the drivers and the diffs to the DURABLE artifacts
# path.  /tmp evaporates, and copying anything a durable record will cite comes BEFORE the
# record is written.  Every preserved log is verified by its COMPLETION SENTINEL, not by its
# existence -- and only AFTER the job that wrote it has finished, or the copy preserves a
# truncation that looks complete.
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
CL=/tmp/gxopus7g1b
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad
DST=$SEC/regress/artifacts/sgimtedepth4dead/repair_20260909
echo "=== STAGE F (ARCHIVE)  $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
mkdir -p "$DST/drivers" "$DST/logs" || exit 9

echo "-- BOTH instruments: the one the table RAN, and the deliverable --"
#  They differ by a comment-only correction found after the table started.  Archiving only the
#  deliverable would leave the record citing a table produced by a file that is not in the
#  record; archiving only the measured one would ship a comment this seat knows is wrong.
cp "$CL/probe/sgi_mte_fill_probe.AS_MEASURED.py" "$DST/" || exit 9
cp "$CL/probe/sgi_mte_fill_probe.REPAIRED.py"    "$DST/" || exit 9
echo "AS_MEASURED (ran the table)   clone $(md5sum "$CL/probe/sgi_mte_fill_probe.AS_MEASURED.py" | cut -c1-32)"
echo "                            archive $(md5sum "$DST/sgi_mte_fill_probe.AS_MEASURED.py" | cut -c1-32)"
echo "REPAIRED    (the deliverable) clone $(md5sum "$CL/probe/sgi_mte_fill_probe.REPAIRED.py" | cut -c1-32)"
echo "                            archive $(md5sum "$DST/sgi_mte_fill_probe.REPAIRED.py" | cut -c1-32)"
echo "                            scratch $(md5sum "$SP/out/sgi_mte_fill_probe.REPAIRED.py" | cut -c1-32)"
echo "row() calls: AS_MEASURED=$(grep -c '^row(' "$DST/sgi_mte_fill_probe.AS_MEASURED.py")  REPAIRED=$(grep -c '^row(' "$DST/sgi_mte_fill_probe.REPAIRED.py")"
echo "-- the delta between them must be comment-only --"
diff "$DST/sgi_mte_fill_probe.AS_MEASURED.py" "$DST/sgi_mte_fill_probe.REPAIRED.py" > "$DST/drivers/probe_commentfix.diff"
NC=$(grep -cE '^[<>]' "$DST/drivers/probe_commentfix.diff")
NK=$(grep -E '^[<>]' "$DST/drivers/probe_commentfix.diff" | grep -cE '^[<>] *#')
echo "changed lines=$NC  comment lines=$NK  $([ "$NC" = "$NK" ] && echo 'COMMENT-ONLY CONFIRMED' || echo '*** NOT COMMENT-ONLY ***')"

echo "-- every probe log --"
cp "$CL"/logs/*.raw "$DST/logs/" || exit 9

echo "-- the one-line mutant diffs --"
cp /tmp/op7b_M*.diff "$DST/logs/" 2>/dev/null

echo "-- the drivers, and the build-log tails --"
cp "$SP"/op7b_*.sh "$SP"/op7b_mutate.py "$SP"/mk_repaired_probe.py "$DST/drivers/" || exit 9
cp "$SP/out/probe_repair.diff" "$DST/drivers/" 2>/dev/null
cp "$SP/out/TABLE_run.log" "$DST/logs/" 2>/dev/null
for b in A E; do tail -4 /tmp/op7b_build$b.log > "$DST/drivers/build_$b.tail" 2>/dev/null; done
for f in /tmp/op7b_build_M*.log; do
    n=$(basename "$f" .log); tail -3 "$f" > "$DST/drivers/${n}.tail" 2>/dev/null
done

echo
echo "-- COMPLETION SENTINEL OF EVERY PRESERVED LOG --"
for f in "$DST"/logs/*.raw; do
    printf '%-26s %6s bytes   score=%-16s last line: %s\n' "$(basename $f)" "$(stat -c %s $f)" \
        "$(grep -hoE 'MTEFILL_RESULT=[0-9]+/[0-9]+' $f | tail -1)" "$(tail -1 $f)"
done
echo
echo "-- ALL SCORES --"
grep -hE '^MTEFILL_RESULT=' "$DST"/logs/*.raw > /dev/null
for f in "$DST"/logs/*.raw; do
    printf '%-24s %s\n' "$(basename $f .raw)" "$(grep -E '^MTEFILL_RESULT=' $f)"
done
echo
ls -la "$DST" "$DST/logs" "$DST/drivers"
echo "STAGE_F_DONE"
