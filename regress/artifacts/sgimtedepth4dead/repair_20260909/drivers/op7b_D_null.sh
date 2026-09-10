#!/bin/bash
# Stage D: the NULL MEDIUM.  No build, no mutation -- the frozen probe is pointed at a binary
# that is not gxemul at all.  Clause (c) asks whether the instrument carries identity rows;
# this is the cheapest demonstration that it does.  *** NO null medium was defined in
# killtable_20260907 or killtable2_20260907; this one is added here. ***
CL=/tmp/gxopus7g1b
OUT=$CL/logs
P=sgi_mte_fill_probe.REPAIRED.py
echo "=== STAGE D (NULL MEDIUM)  $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "-- no mutation is in flight: --"
ls -la "$CL/.MUTANT" 2>&1 | head -1
cd "$CL/probe" || exit 9
echo "FROZEN_PROBE_MD5: $(md5sum $P | cut -c1-32)   (must equal every other run's)"
echo "NULL MEDIUM = /bin/true  ($(md5sum /bin/true | cut -c1-32))"
python3 -u ./$P /bin/true NULL_dead > "$OUT/NULL_dead.raw" 2>&1
echo "PROBE_RC=$?"
echo "SENTINEL: $(tail -1 "$OUT/NULL_dead.raw")"
grep -E '^MTEFILL_RESULT=' "$OUT/NULL_dead.raw"
echo "-- FULL LOG --"
cat "$OUT/NULL_dead.raw"
echo "STAGE_D_DONE"
