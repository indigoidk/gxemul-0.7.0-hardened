#!/bin/bash
# Stage B: run the FROZEN probe against the BASELINE binary.  No `set -e' (probe exits 1 on a red row).
CL=/tmp/gxopus7g1
OUT=$CL/logs; mkdir -p "$OUT"
echo "=== STAGE B  $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "binary: $(md5sum $CL/gxemul | cut -c1-32)  $(ls -la --time-style=full-iso $CL/gxemul | awk '{print $6,$7}')"
cd "$CL/probe" || exit 9
python3 -u ./sgi_mte_fill_probe.py "$CL/gxemul" BASE > "$OUT/BASE.raw" 2>&1
PRC=$?
echo "PROBE_RC=$PRC  (0 means all rows green; 1 means at least one red -- both are RESULTS)"
echo "-- COMPLETION SENTINEL (a preserved log is verified by its sentinel, not by its existence) --"
tail -1 "$OUT/BASE.raw"
echo "-- SCORE --"
grep -E '^MTEFILL_RESULT=' "$OUT/BASE.raw"
echo "-- RED ROWS --"
grep -c 'FAIL$' "$OUT/BASE.raw"
grep 'FAIL$' "$OUT/BASE.raw"
echo "STAGE_B_DONE"
