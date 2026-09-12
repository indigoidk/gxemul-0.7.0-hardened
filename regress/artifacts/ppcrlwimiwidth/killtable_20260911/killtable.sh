#!/bin/bash
# killtable.sh -- ppcrlwimiwidth kill table run in scratch clone /tmp/gxrlwimi_clone

CLONE=/tmp/gxrlwimi_clone
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
SRCREL=src/cpus/cpu_ppc_instr.c
TGT=$CLONE/$SRCREL
BASELINE=$SEC/$SRCREL
OUT=$SEC/regress/artifacts/ppcrlwimiwidth/killtable_20260911
PROBE=$SEC/regress/artifacts/ppcrlwimiwidth/agy_ppc_rlwimi_witness_20260911.py
HEADFILE=/tmp/cpu_ppc_instr.c.HEAD
MUTATOR=$OUT/mutate_rlwimi.py

mkdir -p "$OUT"
SCORES=$OUT/SCORES.txt
: > "$SCORES"

say() { echo "$@" | tee -a "$SCORES"; }

say "ppcrlwimiwidth KILL TABLE   $(date -u +%Y-%m-%dT%H:%M:%SZ)"
say "clone=$CLONE  baseline=$BASELINE (GXEMUL-SEC, the repo source)"
say "probe=$PROBE  (frozen copy -- one instrument for every leg)"
say ""

# Extract HEAD file
git -C "$SEC" show HEAD:src/cpus/cpu_ppc_instr.c > "$HEADFILE"

# Drop sentinel before any edit
echo "$SRCREL kill-table mutation in progress (ppcrlwimiwidth)" > "$CLONE/.MUTANT"
say "SENTINEL DROPPED: $CLONE/.MUTANT"
say ""

LEGS="BASE M_REV_COND M_ONLY_CAST M_ONLY_HIGH M_POST_LOOP M_ORIG HEAD NULL_MEDIUM RESTORED"

for leg in $LEGS; do
    say "=== LEG $leg ==="
    echo "$SRCREL mutant=$leg (ppcrlwimiwidth)" > "$CLONE/.MUTANT"

    python3 "$MUTATOR" "$leg" "$TGT" "$BASELINE" "$HEADFILE" > "$OUT/mutate_$leg.txt" 2>&1
    mrc=$?
    say "  mutate rc=$mrc : $(head -1 "$OUT/mutate_$leg.txt")"
    if [ $mrc -ne 0 ]; then
        say "  LEG $leg ABORTED -- mutator refused (see mutate_$leg.txt)"
        say ""
        continue
    fi

    rm -f "$CLONE"/src/cpus/cpu_ppc*.o
    ( cd "$CLONE" && make -j4 ) > "$OUT/build_$leg.log" 2>&1
    brc=$?

    if [ "$CLONE/gxemul" -nt "$TGT" ]; then
        fresh=FRESH
    else
        fresh=STALE
    fi
    say "  build rc=$brc  binary=$fresh"
    if [ "$fresh" != "FRESH" ]; then
        say "  LEG $leg ABORTED -- binary not newer than source; NOT measured"
        say ""
        continue
    fi

    python3 "$PROBE" "$CLONE/gxemul" "$leg" > "$OUT/probe_$leg.raw" 2>&1
    prc=$?
    score_line=$(grep "^SCORE " "$OUT/probe_$leg.raw" || echo "NO SCORE LINE")
    failing_line=$(grep "^FAILING:" "$OUT/probe_$leg.raw" || echo "NO FAILING LINE")
    sentinel_found=$(grep -c "PPC_RLWIMI_WITNESS_DONE" "$OUT/probe_$leg.raw" || echo 0)

    say "  probe rc=$prc  sentinel=$sentinel_found"
    say "  $score_line"
    say "  $failing_line"
    say ""
done

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

say "KILLTABLE_DONE"
