#!/bin/bash
# Stage H: copy every log, instrument and driver to the DURABLE artifacts path (/tmp evaporates).
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
CL=/tmp/gxopus7g1
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad
DST=$SEC/regress/artifacts/sgimtedepth4dead/killtable3_20260909
echo "=== STAGE H  $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
mkdir -p "$DST/drivers" || exit 9

cp "$CL/logs/BASE.raw" "$CL/logs/M_tlbA.raw" "$CL/logs/M_tlbAB.raw" "$DST/" || exit 9
cp "$CL/logs/reach_BASE.raw" "$CL/logs/reach_M_tlbA.raw" "$CL/logs/reach_M_tlbAB.raw" "$DST/" || exit 9
cp "$CL/probe/tlb_reach_control.py" "$DST/" || exit 9
cp /tmp/gxopus7g1_M_tlbA.diff /tmp/gxopus7g1_M_tlbAB.diff "$DST/" || exit 9
cp "$SP"/opus7g1_*.sh "$DST/drivers/" || exit 9
for b in A C E F; do tail -4 /tmp/gxopus7g1_build$b.log > "$DST/drivers/build_$b.tail" 2>/dev/null; done

echo "-- COMPLETION SENTINELS OF EVERY PRESERVED LOG (verified by sentinel, not by existence) --"
for f in "$DST"/*.raw; do printf '%-22s %8s bytes   last line: %s\n' "$(basename $f)" "$(stat -c %s $f)" "$(tail -1 $f)"; done
echo
echo "-- SCORES --"
grep -H 'MTEFILL_RESULT=' "$DST"/BASE.raw "$DST"/M_tlbA.raw "$DST"/M_tlbAB.raw | sed 's#.*/##'
grep -H 'TLBREACH_RESULT=' "$DST"/reach_*.raw | sed 's#.*/##'
echo
ls -la "$DST" "$DST/drivers"
echo "STAGE_H_DONE"
