#!/bin/bash
# killtable.sh -- ppcrldimimask kill table run in scratch clone /tmp/gxrldimi_clone

CLONE=/tmp/gxrldimi_clone
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
SRCREL=src/cpus/cpu_ppc_instr.c
TGT=$CLONE/$SRCREL
BASELINE=$SEC/$SRCREL
OUT=$SEC/regress/artifacts/ppcrldimimask/killtable_20260911
PROBE=$SEC/regress/artifacts/ppcrldimimask/opus_ppc_rldimi_witness_20260911.py
HEADFILE=/tmp/cpu_ppc_instr.c.HEAD
MUTATOR=$OUT/mutate_rldimi.py

mkdir -p "$OUT"
SCORES=$OUT/SCORES.txt
: > "$SCORES"

say() { echo "$@" | tee -a "$SCORES"; }

say "ppcrldimimask KILL TABLE   $(date -u +%Y-%m-%dT%H:%M:%SZ)"
say "clone=$CLONE  baseline=$BASELINE (GXEMUL-SEC, the repo source)"
say "probe=$PROBE  (frozen copy -- one instrument for every leg)"
say ""

# Extract HEAD file
git -C "$SEC" show HEAD:src/cpus/cpu_ppc_instr.c > "$HEADFILE"

# Drop sentinel before any edit
echo "$SRCREL kill-table mutation in progress (ppcrldimimask)" > "$CLONE/.MUTANT"
say "SENTINEL DROPPED: $CLONE/.MUTANT"
say ""

LEGS="BASE M_ORIG M_MUT63 M_NOWRAP M_NOKEEP_SH M_NOCIRC M_NO_MERGE HEAD"

for leg in $LEGS; do
    say "=== LEG $leg ==="
    echo "$SRCREL mutant=$leg (ppcrldimimask)" > "$CLONE/.MUTANT"

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

    python3 -u "$PROBE" "$CLONE/gxemul" "$leg" > "$OUT/probe_$leg.raw" 2>&1
    prc=$?
    sentinel=$(tail -1 "$OUT/probe_$leg.raw")
    score=$(grep -o 'SCORE [0-9]*/[0-9]*' "$OUT/probe_$leg.raw" | head -1)
    failing=$(grep '^FAILING:' "$OUT/probe_$leg.raw" | head -1)
    say "  probe rc=$prc  $score  sentinel=[$sentinel]"
    if [ -n "$failing" ]; then say "  $failing"; fi
    if [ "$sentinel" != "PPC_RLDIMI_WITNESS_DONE" ]; then
        say "  WARNING: log does NOT end in PPC_RLDIMI_WITNESS_DONE -- truncated, do not cite"
    fi
    say ""
done

# ---- restore from GXEMUL-SEC, rebuild, verify, then clear sentinel --------
say "=== RESTORE ==="
cp "$BASELINE" "$TGT"
rm -f "$CLONE"/src/cpus/cpu_ppc*.o
( cd "$CLONE" && make -j4 ) > "$OUT/build_RESTORE.log" 2>&1
rrc=$?
if cmp -s "$TGT" "$BASELINE"; then cmpok=CLEAN; else cmpok=DIFFERS; fi
if [ "$CLONE/gxemul" -nt "$TGT" ]; then rfresh=FRESH; else rfresh=STALE; fi
say "  restore build rc=$rrc  cmp-vs-SEC=$cmpok  binary=$rfresh"

if [ "$cmpok" = "CLEAN" ] && [ "$rfresh" = "FRESH" ]; then
    rm -f "$CLONE/.MUTANT"
    say "  SENTINEL CLEARED (both parts verified: source cmp CLEAN, binary FRESH)"
else
    say "  SENTINEL KEPT -- restore NOT verified; clone is still mutant"
fi

# Final confirmation leg: the restored tree must reproduce BASE.
python3 -u "$PROBE" "$CLONE/gxemul" RESTORED > "$OUT/probe_RESTORED.raw" 2>&1
say "  restored-tree probe: $(grep -o 'SCORE [0-9]*/[0-9]*' "$OUT/probe_RESTORED.raw" | head -1)  sentinel=[$(tail -1 "$OUT/probe_RESTORED.raw")]"
say ""
say "=== SUMMARY ==="
for leg in $LEGS RESTORED; do
    s=$(grep -o 'SCORE [0-9]*/[0-9]*' "$OUT/probe_$leg.raw" 2>/dev/null | head -1)
    f=$(grep '^FAILING:' "$OUT/probe_$leg.raw" 2>/dev/null | head -1)
    printf '%-12s %-16s %s\n' "$leg" "${s:-NOT MEASURED}" "$f" | tee -a "$SCORES"
done
say "KILLTABLE_DONE"
