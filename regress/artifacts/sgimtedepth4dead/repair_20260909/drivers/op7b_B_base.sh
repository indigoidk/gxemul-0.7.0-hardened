#!/bin/bash
# Stage B: run the FROZEN 16-row probe against the BASELINE binary.  No `set -e'.
CL=/tmp/gxopus7g1b
OUT=$CL/logs
P=sgi_mte_fill_probe.REPAIRED.py
echo "=== STAGE B  $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "binary md5: $(md5sum $CL/gxemul | cut -c1-32)"
echo "source line 1519: $(sed -n '1519p' $CL/src/devices/dev_sgi_re.c)"
cd "$CL/probe" || exit 9
echo "FROZEN_PROBE_MD5: $(md5sum $P | cut -c1-32)"
T0=$(date +%s)
python3 -u ./$P "$CL/gxemul" BASE > "$OUT/BASE.raw" 2>&1
PRC=$?
T1=$(date +%s)
echo "PROBE_RC=$PRC  (0 = all green, 1 = at least one red; both are RESULTS)"
echo "ELAPSED=$((T1-T0))s   (per-run cost, for scheduling the rest of the table)"
echo "-- COMPLETION SENTINEL (a log is verified by its sentinel, not by its existence) --"
tail -1 "$OUT/BASE.raw"
echo "-- SCORE --"
grep -E '^MTEFILL_RESULT=' "$OUT/BASE.raw"
echo "-- RED ROWS: $(grep -c 'FAIL$' "$OUT/BASE.raw") --"
grep 'FAIL$' "$OUT/BASE.raw"
echo "-- FULL LOG --"
cat "$OUT/BASE.raw"
echo "STAGE_B_DONE"
