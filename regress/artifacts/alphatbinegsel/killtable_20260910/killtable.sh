#!/bin/bash
# killtable.sh -- #520 alphatbinegsel kill table, run in the SCRATCH CLONE /tmp/gx520.
#
# Never writes GXEMUL-SEC/src, build/, build-asan/ or /tmp/gxsec-build.  It reads
# GXEMUL-SEC only, and writes the clone plus an output dir.
#
# Discipline enforced here rather than remembered:
#   * .MUTANT sentinel dropped BEFORE the first edit, cleared only after a restore
#     that is verified by cmp against GXEMUL-SEC *and* by a fresh rebuild.
#   * baseline for every leg is GXEMUL-SEC's file, never a backup this script made.
#   * rm src/cpus/*.o before every build (conservative clean-build precaution).
#   * [ binary -nt source ] after every build -- make has been observed reporting
#     success on a failed build.
#   * every raw log is checked for the probe's completion sentinel ALPHATBI_DONE.
#   * ONE FROZEN PROBE for all legs, so the comparison uses one instrument.
#
# NOT run with set -e: a failing leg must be RECORDED, not abort the table.

CLONE=/tmp/gx520
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
SRCREL=src/cpus/cpu_alpha_palcode.c
TGT=$CLONE/$SRCREL
BASELINE=$SEC/$SRCREL
OUT=$1
PROBE=$2
HEADFILE=$3
MUTATOR=$4

if [ -z "$OUT" ] || [ -z "$PROBE" ] || [ -z "$HEADFILE" ] || [ -z "$MUTATOR" ]; then
    echo "usage: killtable.sh <outdir> <frozen-probe> <head-file> <mutator>"; exit 2
fi
mkdir -p "$OUT"
SCORES=$OUT/SCORES.txt
: > "$SCORES"

say() { echo "$@" | tee -a "$SCORES"; }

say "#520 alphatbinegsel KILL TABLE   $(date -u +%Y-%m-%dT%H:%M:%SZ)"
say "clone=$CLONE  baseline=$BASELINE (GXEMUL-SEC, the repo source)"
say "probe=$PROBE  (frozen copy -- one instrument for every leg)"
say ""

# ---- sentinel BEFORE any edit --------------------------------------------
echo "$SRCREL kill-table mutation in progress (#520 alphatbinegsel)" > "$CLONE/.MUTANT"
say "SENTINEL DROPPED: $CLONE/.MUTANT"
say ""

LEGS="BASE M_A M_B M_C M_D M_E M_F M_G M_H M_I HEAD"

for leg in $LEGS; do
    say "=== LEG $leg ==="
    echo "$SRCREL mutant=$leg (#520)" > "$CLONE/.MUTANT"

    python3 "$MUTATOR" "$leg" "$TGT" "$BASELINE" "$HEADFILE" > "$OUT/mutate_$leg.txt" 2>&1
    mrc=$?
    say "  mutate rc=$mrc : $(head -1 "$OUT/mutate_$leg.txt")"
    if [ $mrc -ne 0 ]; then
        say "  LEG $leg ABORTED -- mutator refused (see mutate_$leg.txt)"
        say ""
        continue
    fi

    rm -f "$CLONE"/src/cpus/*.o
    ( cd "$CLONE" && make -j4 ) > "$OUT/build_$leg.log" 2>&1
    brc=$?

    # make has reported success on a failed build; the binary timestamp is the test.
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
    score=$(grep -o 'ALPHATBI_RESULT=[0-9]*/[0-9]*' "$OUT/probe_$leg.raw" | head -1)
    failing=$(grep '^FAILING:' "$OUT/probe_$leg.raw" | head -1)
    say "  probe rc=$prc  $score  sentinel=[$sentinel]"
    if [ -n "$failing" ]; then say "  $failing"; fi
    if [ "$sentinel" != "ALPHATBI_DONE" ]; then
        say "  WARNING: log does NOT end in ALPHATBI_DONE -- truncated, do not cite"
    fi
    say ""
done

# ---- restore from GXEMUL-SEC, rebuild, verify, then clear sentinel --------
say "=== RESTORE ==="
cp "$BASELINE" "$TGT"
rm -f "$CLONE"/src/cpus/*.o
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
say "  restored-tree probe: $(grep -o 'ALPHATBI_RESULT=[0-9]*/[0-9]*' "$OUT/probe_RESTORED.raw" | head -1)  sentinel=[$(tail -1 "$OUT/probe_RESTORED.raw")]"
say ""
say "=== SUMMARY ==="
for leg in $LEGS RESTORED; do
    s=$(grep -o 'ALPHATBI_RESULT=[0-9]*/[0-9]*' "$OUT/probe_$leg.raw" 2>/dev/null | head -1)
    f=$(grep '^FAILING:' "$OUT/probe_$leg.raw" 2>/dev/null | head -1)
    printf '%-10s %-24s %s\n' "$leg" "${s:-NOT MEASURED}" "$f" | tee -a "$SCORES"
done
say "KILLTABLE_DONE"
