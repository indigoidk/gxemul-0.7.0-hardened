#!/bin/bash
#  #496 KILL TABLE -- gdromcondlies.
#
#  *** RUNS IN A SCRATCH CLONE BY DEFAULT (owner decision 2026-08-28, on measured practice).
#  It writes to NO project tree and leaves the clone cmp-clean. ***
#
#  THE RECIPE THAT MAKES THE DEFAULT SAFE, and each step is a recorded line below:
#    1. NAME THE BASELINE and cmp the file-to-be-mutated against it BEFORE mutant 1 --
#       a clone inherits whatever build/ held mid-round.
#    2. REBUILD THE BASELINE BINARY IN THE CLONE and check [ binary -nt source ].  The
#       base-table run doubles as that freshness proof.
#    3. Clone-local sentinel, plus the FROZEN-COPY driver rule.
#    4. The volatile-path rule with extra force: /tmp evaporates, so any number a durable
#       record will cite is copied into regress/artifacts/ BEFORE the record is written.
#
#  *** RUN THE FROZEN COPY, NOT THIS FILE. ***
#      cp kill496.sh kill496.run-$(date +%H%M%S).sh && bash kill496.run-*.sh
#  Bash reads a script INCREMENTALLY by byte offset, so editing this file while it runs
#  shifts every offset after the insertion point and the shell resumes mid-token.  The
#  signature is a syntax error at run time that `bash -n` afterwards cannot reproduce.
#  Measured on killwdc.sh: an eight-mutant table died on its first mutant.
#
#  *** AND THE PROBE IS FROZEN TOO. ***  Python reads the whole file at startup, so the
#  RUNNING invocation is immune -- but a multi-run driver re-reads it BETWEEN runs, and an
#  edit to a row's NOTE text lands in the very output being diffed.  A comparison run owes
#  ONE instrument.
set -u

STAMP=$(date +%Y%m%d_%H%M%S)
CLONE=${CLONE:-/tmp/gx496}
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
OUT=${OUT:-$SEC/regress/artifacts/gdromcondlies/killtable_20260830}
DEV=src/devices/dev_dreamcast_gdrom.c
KERNEL=/mnt/c/DocumentNoSnc/CC/GXEMUL/_images/openbsd76-landisk-bsd.rd

#  TABLETAG refuses an untagged partial run: a kill log that overwrites its predecessor
#  turns a durable citation into a pointer at something ELSE.  Measured twice this week --
#  a record did not become unverifiable, it became CONTRADICTED BY ITS OWN EVIDENCE.
TABLETAG=${TABLETAG:-}
if [ -z "$TABLETAG" ]; then
    echo "REFUSED: set TABLETAG (e.g. TABLETAG=base, TABLETAG=M5) so kill logs are"
    echo "         tagged and a partial re-run cannot clobber a cited log."
    exit 2
fi

PROBE_SRC=$SEC/regress/gdrom_cond_probe.py
FROZEN=$OUT/probe.frozen_$STAMP.py

echo "=== #496 KILL TABLE  tag=$TABLETAG  stamp=$STAMP ==="
echo "clone : $CLONE"
echo "out   : $OUT"

# ---------------------------------------------------------------- 1. NAME THE BASELINE
#  The baseline is the round's POST-FIX WORKING SET -- not HEAD.  HEAD does not yet carry
#  the fix, so a clone of HEAD would measure the wrong thing.  Stating which, and checking
#  it, is step 1 of the recipe rather than a comment about it.
echo ""
echo "--- baseline: the round's post-fix working set in GXEMUL-SEC ---"
if [ ! -d "$CLONE" ]; then
    echo "cloning build/ -> $CLONE (relocatable cp -a)"
    cp -a /mnt/c/DocumentNoSnc/cc/GXEMUL/build "$CLONE" || exit 9
fi
cp "$SEC/$DEV" "$CLONE/$DEV" || exit 9
cp "$SEC/$DEV" "$CLONE/BASELINE.c" || exit 9
if cmp -s "$CLONE/$DEV" "$SEC/$DEV"; then
    echo "BASELINE_CMP_CLEAN"
else
    echo "BASELINE_CMP_DIRTY -- refusing to measure"; exit 9
fi

#  freeze the instrument
cp "$PROBE_SRC" "$FROZEN" || exit 9
echo "frozen instrument: $(basename "$FROZEN")"

# ------------------------------------------------------------------- helpers
build_it () {
    ( cd "$CLONE" && rm -f src/devices/dev_dreamcast_gdrom.o && make ) > "$CLONE/build.log" 2>&1
    local rc=$?
    #  MAKE_RC has been observed reporting 0 on a FAILED build, so the freshness pair is
    #  the real test and the exit status is only a hint.
    if [ ! "$CLONE/gxemul" -nt "$CLONE/$DEV" ]; then
        echo "  BUILD_STALE (rc=$rc) -- binary not newer than source"
        return 1
    fi
    echo "  BUILD_OK (rc=$rc, binary newer than source)"
    return 0
}

score_it () {
    local tag=$1
    local log=$OUT/kill_${tag}.out
    python3 -u "$FROZEN" "$CLONE/gxemul" "$KERNEL" > "$log" 2>&1
    #  A PRESERVED LOG IS VERIFIED BY ITS COMPLETION SENTINEL, NOT BY ITS EXISTENCE.
    if ! grep -q "GDROMCOND_PROBE_DONE" "$log"; then
        echo "  $tag: NO SENTINEL -- run truncated or died; log NOT citable"
        return 1
    fi
    local r
    r=$(grep -o "GDROMCOND_PROBE_RESULT=[0-9]*/[0-9]*" "$log" | tail -1 | cut -d= -f2)
    echo "  $tag: $r   ($(basename "$log"))"
    return 0
}

restore () {
    cp "$CLONE/BASELINE.c" "$CLONE/$DEV"
    #  cmp against SEC -- the REPO SOURCE, never the script's own backup.  A crashed run
    #  once left a tree mutant, so the next run's "orig" backup captured the mutant and
    #  its restore restored it.
    if cmp -s "$CLONE/$DEV" "$SEC/$DEV"; then
        echo "  restored, cmp-clean vs SEC"
        return 0
    fi
    echo "  RESTORE FAILED -- sentinel stays"
    return 1
}

# ------------------------------------------------- 2. REBUILD THE BASELINE IN THE CLONE
echo ""
echo "--- base leg (doubles as the freshness proof) ---"
echo "$DEV baseline rebuild" > "$CLONE/.MUTANT"
build_it || exit 9
score_it "L0_base_${TABLETAG}" || exit 9
rm -f "$CLONE/.MUTANT"

echo ""
echo "KILL496_BASE_DONE"
echo ""
echo "Mutants are applied by kill496_mut.py, one at a time, each with the sentinel"
echo "dropped BEFORE the edit and cleared only after restore is verified by cmp"
echo "against SEC and the binary is rebuilt.  THE RESTORE IS NOT FINISHED UNTIL THE"
echo "BINARY IS REBUILT: the sentinel protects the source; the thing measured is the"
echo "binary, and a mutant binary over clean sources has been caught twice here."
echo ""
echo "KILL496_DONE"
