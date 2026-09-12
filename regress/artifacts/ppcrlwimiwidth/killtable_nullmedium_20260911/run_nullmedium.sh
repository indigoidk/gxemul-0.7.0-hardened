#!/bin/bash
# run_nullmedium.sh -- ppcrlwimiwidth honest NULL_MEDIUM leg in scratch clone /tmp/gxrlwimi_clone

CLONE=/tmp/gxrlwimi_clone
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
SRCREL=src/cpus/cpu_ppc_instr.c
TGT=$CLONE/$SRCREL
BASELINE=$SEC/$SRCREL
OUT=$SEC/regress/artifacts/ppcrlwimiwidth/killtable_nullmedium_20260911
PROBE=$SEC/regress/artifacts/ppcrlwimiwidth/agy_ppc_rlwimi_witness_20260911.py
HEADFILE=/tmp/cpu_ppc_instr.c.HEAD
MUTATOR=$OUT/mutate_rlwimi.py

mkdir -p "$OUT"
SCORES=$OUT/SCORES.txt
: > "$SCORES"

say() { echo "$@" | tee -a "$SCORES"; }

say "ppcrlwimiwidth NULL_MEDIUM (IDENTITY) LEG   $(date -u +%Y-%m-%dT%H:%M:%SZ)"
say "clone=$CLONE  baseline=$BASELINE (GXEMUL-SEC, the repo source)"
say "probe=$PROBE  (frozen copy -- one instrument for every leg)"
say ""

# Extract HEAD file if not present
git -C "$SEC" show HEAD:src/cpus/cpu_ppc_instr.c > "$HEADFILE"

# Pre-check baseline matches clone before starting
if ! cmp -s "$BASELINE" "$TGT"; then
    say "ERROR: Clone is not clean vs BASELINE before start!"
    exit 1
fi

# Drop sentinel before mutation
echo "$SRCREL mutant=NULL_MEDIUM (ppcrlwimiwidth)" > "$CLONE/.MUTANT"
say "SENTINEL DROPPED: $CLONE/.MUTANT"
say ""

# === LEG NULL_MEDIUM ===
say "=== LEG NULL_MEDIUM ==="
echo "$SRCREL mutant=NULL_MEDIUM (ppcrlwimiwidth)" > "$CLONE/.MUTANT"

python3 "$MUTATOR" "NULL_MEDIUM" "$TGT" "$BASELINE" "$HEADFILE" > "$OUT/mutate_NULL_MEDIUM.txt" 2>&1
mrc=$?
say "  mutate rc=$mrc : $(head -1 "$OUT/mutate_NULL_MEDIUM.txt")"
if [ $mrc -ne 0 ]; then
    say "  LEG NULL_MEDIUM ABORTED -- mutator refused"
    exit 1
fi

rm -f "$CLONE"/src/cpus/cpu_ppc*.o
( cd "$CLONE" && make -j4 ) > "$OUT/build_NULL_MEDIUM.log" 2>&1
brc=$?

if [ "$CLONE/gxemul" -nt "$TGT" ]; then
    fresh=FRESH
else
    fresh=STALE
fi
say "  build rc=$brc  binary=$fresh"
if [ "$fresh" != "FRESH" ]; then
    say "  LEG NULL_MEDIUM ABORTED -- binary not newer than source; NOT measured"
    exit 1
fi

python3 "$PROBE" "$CLONE/gxemul" "NULL_MEDIUM" > "$OUT/probe_NULL_MEDIUM.raw" 2>&1
prc=$?
score_line=$(grep "^SCORE " "$OUT/probe_NULL_MEDIUM.raw" || echo "NO SCORE LINE")
failing_line=$(grep "^FAILING:" "$OUT/probe_NULL_MEDIUM.raw" || echo "NO FAILING LINE")
sentinel_found=$(grep -c "PPC_RLWIMI_WITNESS_DONE" "$OUT/probe_NULL_MEDIUM.raw" || echo 0)

say "  probe rc=$prc  sentinel=$sentinel_found"
say "  $score_line"
say "  $failing_line"
say ""

# === LEG RESTORED ===
say "=== LEG RESTORED ==="
echo "$SRCREL mutant=RESTORED (ppcrlwimiwidth)" > "$CLONE/.MUTANT"

python3 "$MUTATOR" "RESTORED" "$TGT" "$BASELINE" "$HEADFILE" > "$OUT/mutate_RESTORED.txt" 2>&1
mrc=$?
say "  mutate rc=$mrc : $(head -1 "$OUT/mutate_RESTORED.txt")"
if [ $mrc -ne 0 ]; then
    say "  LEG RESTORED ABORTED -- mutator refused"
    exit 1
fi

rm -f "$CLONE"/src/cpus/cpu_ppc*.o
( cd "$CLONE" && make -j4 ) > "$OUT/build_RESTORED.log" 2>&1
brc=$?

if [ "$CLONE/gxemul" -nt "$TGT" ]; then
    fresh=FRESH
else
    fresh=STALE
fi
say "  build rc=$brc  binary=$fresh"
if [ "$fresh" != "FRESH" ]; then
    say "  LEG RESTORED ABORTED -- binary not newer than source; NOT measured"
    exit 1
fi

python3 "$PROBE" "$CLONE/gxemul" "RESTORED" > "$OUT/probe_RESTORED.raw" 2>&1
prc=$?
score_line=$(grep "^SCORE " "$OUT/probe_RESTORED.raw" || echo "NO SCORE LINE")
failing_line=$(grep "^FAILING:" "$OUT/probe_RESTORED.raw" || echo "NO FAILING LINE")
sentinel_found=$(grep -c "PPC_RLWIMI_WITNESS_DONE" "$OUT/probe_RESTORED.raw" || echo 0)

say "  probe rc=$prc  sentinel=$sentinel_found"
say "  $score_line"
say "  $failing_line"
say ""

# Verification & Restoration
say "=== CLEARANCE & SENTINEL REMOVAL ==="
if cmp -s "$BASELINE" "$TGT"; then
    cmp_res="CLEAN"
else
    cmp_res="DIFF"
fi

if [ "$CLONE/gxemul" -nt "$TGT" ]; then
    bin_res="FRESH"
else
    bin_res="STALE"
fi

say "  Clearance: Part 1 (cmp vs SEC)=$cmp_res  Part 2 (binary -nt source)=$bin_res"

if [ "$cmp_res" = "CLEAN" ] && [ "$bin_res" = "FRESH" ]; then
    rm -f "$CLONE/.MUTANT"
    say "  SENTINEL CLEARED: $CLONE/.MUTANT removed"
else
    say "  WARNING: SENTINEL NOT CLEARED -- verification failed!"
fi

say "NULLMEDIUM_DONE"
