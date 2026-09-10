#!/bin/bash
# Stage E: RESTORE FROM SEC (never from a local backup), REBUILD, verify BOTH parts, clear
# the sentinel.  The sentinel protects the SOURCE; the thing measured is the BINARY, so the
# restore is not finished until the binary is rebuilt.
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
CL=/tmp/gxopus7g1b
F=src/devices/dev_sgi_re.c
OUT=$CL/logs
SP_OUT=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/out
P=sgi_mte_fill_probe.AS_MEASURED.py
echo "=== STAGE E (RESTORE)  $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "-- sentinel present before the restore? --"; cat "$CL/.MUTANT" 2>&1 | head -c 200; echo

#  The table and the null medium are finished, so the frozen instrument can now be renamed to
#  say what it is.  Renaming BEFORE they finished would have pulled the file out from under a
#  running comparison, which is the hazard the freeze exists to prevent.
echo "-- name the frozen instrument for what it is, and verify it is the file the table used --"
mv "$CL/probe/sgi_mte_fill_probe.REPAIRED.py" "$CL/probe/$P" || { echo "E-FAIL mv"; exit 9; }
echo "clone   AS_MEASURED md5: $(md5sum "$CL/probe/$P" | cut -c1-32)"
echo "scratch AS_MEASURED md5: $(md5sum "$SP_OUT/sgi_mte_fill_probe.AS_MEASURED.py" | cut -c1-32)"
cmp -s "$CL/probe/$P" "$SP_OUT/sgi_mte_fill_probe.AS_MEASURED.py" \
  && echo "FROZEN INSTRUMENT CONFIRMED: the file that ran the table is byte-identical to the archived copy" \
  || { echo "E-FAIL: the frozen instrument is not the archived copy"; exit 9; }

cp "$SEC/$F" "$CL/$F" || { echo "E-FAIL cp"; exit 9; }

echo "-- PART 1: source cmp vs SEC (the REPO, never a local backup) --"
if cmp -s "$CL/$F" "$SEC/$F"; then echo "PART1=CLEAN"; else echo "E-FAIL part1"; exit 9; fi
echo "SEC_MD5   $(md5sum $SEC/$F | cut -c1-32)"
echo "CLONE_MD5 $(md5sum $CL/$F | cut -c1-32)"
echo "line 1519: $(sed -n '1519p' $CL/$F)"

echo "-- PART 2: REBUILD, then [ binary -nt source ] --"
cd "$CL" || exit 9
rm -f src/devices/dev_sgi_re.o
make -j4 > /tmp/op7b_buildE.log 2>&1; echo "MAKE_RC=$? (not trusted alone)"
if [ -x "$CL/gxemul" ] && [ "$CL/gxemul" -nt "$CL/$F" ]; then
  echo "PART2=OK   [ gxemul -nt $F ]"
else
  echo "E-FAIL part2 -- LEAVING THE SENTINEL IN PLACE"
  ls -la --time-style=full-iso "$CL/gxemul" "$CL/$F"; exit 9
fi
ls -la --time-style=full-iso "$CL/gxemul" "$CL/$F"
echo "RESTORED_BIN_MD5: $(md5sum $CL/gxemul | cut -c1-32)"
echo "   (must equal stage A/B's e113ca7193a91b8953c4c10f37417ab2 -- the restore confirmed"
echo "    by the ARTIFACT, not only by the file compare)"

echo "-- RE-RUN THE FROZEN PROBE ON THE RESTORED BINARY: the restore's own regression test --"
cd "$CL/probe" || exit 9
python3 -u ./$P "$CL/gxemul" BASE_after_restore > "$OUT/BASE_after_restore.raw" 2>&1
echo "PROBE_RC=$?"
echo "SENTINEL: $(tail -1 "$OUT/BASE_after_restore.raw")"
grep -E '^MTEFILL_RESULT=' "$OUT/BASE_after_restore.raw"
echo "-- row-for-row against the ORIGINAL base run (line 1 carries the label, so skip it) --"
diff <(tail -n +2 "$OUT/BASE.raw") <(tail -n +2 "$OUT/BASE_after_restore.raw") \
  && echo "IDENTICAL_TO_BASE: the clone is back to the baseline, measured not asserted"

echo
echo "-- THE COMMENT-ONLY CORRECTION, MEASURED RATHER THAN ASSERTED. --"
#  A records error was found in the frozen probe's CONTRACT block AFTER the table started: it
#  said briefs "asserted" the `fill b top' row existed from 2026-09-07, when on that date the
#  round's own brief PROPOSED it and the round then dropped it.  The correction is comment-only
#  -- proved statically (30 changed lines, all comments; 278 non-comment lines byte-identical) --
#  but this project's rule is RUN IT, DO NOT ASSERT IT, so it is also proved empirically here:
#  the corrected file is run against the SAME restored baseline binary and must be row-for-row
#  identical to the frozen file's run above.
cp "$SP_OUT/sgi_mte_fill_probe.REPAIRED.py" "$CL/probe/" || { echo "E-FAIL: corrected probe cp"; exit 9; }
cd "$CL/probe" || exit 9
echo "AS_MEASURED md5: $(md5sum $P | cut -c1-32)"
echo "CORRECTED   md5: $(md5sum sgi_mte_fill_probe.REPAIRED.py | cut -c1-32)"
python3 -u ./sgi_mte_fill_probe.REPAIRED.py "$CL/gxemul" BASE_corrected > "$OUT/BASE_corrected.raw" 2>&1
echo "PROBE_RC=$?"
echo "SENTINEL: $(tail -1 "$OUT/BASE_corrected.raw")"
grep -E '^MTEFILL_RESULT=' "$OUT/BASE_corrected.raw"
echo "-- row-for-row, corrected probe vs the frozen probe, same binary (line 1 carries the label) --"
diff <(tail -n +2 "$OUT/BASE_after_restore.raw") <(tail -n +2 "$OUT/BASE_corrected.raw") \
  && echo "COMMENT_ONLY_CONFIRMED: identical row for row, so the correction changed no behaviour"

echo "-- BOTH PARTS PASSED -> clearing the sentinel --"
rm -f "$CL/.MUTANT"
ls -la "$CL/.MUTANT" 2>&1 | head -1

echo "-- PROJECT TREES UNTOUCHED? --"
for T in /mnt/c/DocumentNoSnc/CC/GXEMUL/build /mnt/c/DocumentNoSnc/CC/GXEMUL/build-asan; do
  if [ -d "$T" ]; then
    cmp -s "$T/$F" "$SEC/$F" && echo "$T  $F CMP CLEAN vs SEC" || echo "*** $T $F DIFFERS ***"
    ls -la "$T/.MUTANT" 2>&1 | head -1
  fi
done
echo "-- and the tracked probe: still the SHIPPED 14-row file, untouched by this seat --"
echo "SEC probe md5: $(md5sum $SEC/regress/sgi_mte_fill_probe.py | cut -c1-32)  (was dcada99957a733e283efbcaf391d4409 at stage A)"
echo "SEC probe row count: $(grep -c '^row(' $SEC/regress/sgi_mte_fill_probe.py)"
echo "STAGE_E_DONE"
