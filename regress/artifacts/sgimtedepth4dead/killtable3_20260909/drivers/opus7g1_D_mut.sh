#!/bin/bash
CL=/tmp/gxopus7g1
OUT=$CL/logs
echo "=== STAGE D  $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "binary: $(md5sum $CL/gxemul | cut -c1-32)"
echo "source line 1519: $(sed -n '1519p' $CL/src/devices/dev_sgi_re.c)"
cd "$CL/probe" || exit 9
echo "PROBE_MD5 (must equal the base run's): $(md5sum ./sgi_mte_fill_probe.py | cut -c1-32)"
python3 -u ./sgi_mte_fill_probe.py "$CL/gxemul" M_tlbA > "$OUT/M_tlbA.raw" 2>&1
PRC=$?
echo "PROBE_RC=$PRC"
echo "-- SENTINEL --"; tail -1 "$OUT/M_tlbA.raw"
echo "-- SCORE --"; grep -E '^MTEFILL_RESULT=' "$OUT/M_tlbA.raw"
echo "-- RED ROWS --"; grep -c 'FAIL$' "$OUT/M_tlbA.raw"; grep 'FAIL$' "$OUT/M_tlbA.raw"
echo "-- DIFF vs BASE (row-by-row) --"
diff "$OUT/BASE.raw" "$OUT/M_tlbA.raw" && echo "IDENTICAL_TO_BASE: every row scored the same"
echo "STAGE_D_DONE"
