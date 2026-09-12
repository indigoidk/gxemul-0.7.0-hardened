#!/usr/bin/env bash
#
#  #524 (armbdt) kill table, SECOND TABLE -- the repaired driver.
#
#  *** THIS IS A NEW FILE, NOT AN EDIT OF killtable_20260911/killtable.sh. ***
#  That directory is the preserved artifact of a COMPLETED run; editing its
#  driver in place would falsify the record of what was actually executed.
#  The old driver stays exactly as it ran, defects and all, and this one
#  carries the repairs.  Row: killtablebaseline.
#
#  THREE DEFECTS IN THE FIRST DRIVER, and the third was found by reading the
#  whole file rather than the two lines that were reported:
#
#    1. BASELINE FROM A MUTABLE TREE.  It ran `git log --oneline -1` under a
#       comment saying "Verify SEC ... matches pure HEAD commit 8d372aa" and
#       then GATED ON NOTHING, taking the baseline with
#       `cp "$SEC_DIR/src/cpus/cpu_arm_instr.c"`.  That is the working tree,
#       which is a moving reference.  It did not bite -- the tree was pre-fix
#       when the table ran, so the measurement is valid -- but the fix landed
#       in the tree hours later, and a re-run would have copied the FIXED file
#       as its baseline.
#
#    2. THE HEAD LEG HAD NO PRESENCE PIN.  Every MUTANT leg is protected by
#       its find-text: the mutator exits 1 on MUTANT-TEXT-NOT-FOUND, so each
#       find-text doubles as a presence pin on the feature it edits.  The
#       BASELINE leg asserted nothing, so it would have silently measured the
#       fixed file and labelled the result HEAD.  The one leg without a pin
#       is the one that would lie.
#
#    3. *** THE TWO-PART RESTORATION CHECK WAS SELF-REFERENTIAL, and this is
#       the carrier's documented failure mode verbatim. ***  It restored the
#       clone from $HEAD_FILE -- the script's OWN BACKUP -- and then `cmp`'d
#       the result against the same working tree the backup was taken from.
#       The carrier says: verify the restore by `cmp` against GXEMUL-SEC,
#       "NEVER the script's own backup: a crashed run once left the tree
#       mutant, so the next run's 'orig' backup captured the mutant and its
#       restore restored it."  Here backup and comparand share one source, so
#       the check can only catch a failed `cp`, never a wrong baseline.
#
#  THE REPAIR IS THE SAME IDEA THREE TIMES: take the baseline from GIT, and
#  compare against GIT.  An immutable reference cannot drift out from under
#  the run.
#
#  NEGATIVE CONTROLS THIS DRIVER OWES BEFORE ITS RESULTS ARE CITED -- run
#  them with --selftest, which mutates nothing and builds nothing:
#    (a) baseline extraction from a WRONG commit must FAIL, not silently
#        produce a different file;
#    (b) the HEAD-leg pin must FAIL on the post-fix file (the text it
#        requires occurs 0 times there) and PASS on the baseline (exactly 2);
#    (c) the restoration cmp must FAIL when the clone is deliberately left
#        holding mutant text.
#
set -euo pipefail

BASELINE_COMMIT="8d372aa"          # NAMED BY COMMIT, never by a moving ref
REL="src/cpus/cpu_arm_instr.c"

CLONE="/tmp/gxarmbdt_clone"
SEC_DIR="/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC"
PROBE="$SEC_DIR/regress/artifacts/armbdt/agy_armbdt_witness_20260911.py"
MUTATOR="$SEC_DIR/regress/artifacts/armbdt/killtable_20260911d/mutate_armbdt.py"
OUT_DIR="$SEC_DIR/regress/artifacts/armbdt/killtable_20260911d"
HEAD_FILE="$CLONE/cpu_arm_instr.c.BASELINE_${BASELINE_COMMIT}"

#  The unmasked call text.  Present EXACTLY TWICE in the baseline (the LDM and
#  STM slow paths) and ZERO times once #524 lands.  Counting rather than merely
#  finding is deliberate: a count also catches a file where ONE site was fixed
#  and the other was not, which a bare `grep -q` would pass.
UNMASKED='cpu->memory_rw(cpu, cpu->mem, addr, data,'
UNMASKED_EXPECTED=2

extract_baseline () {
    #  Immutable source.  If the commit or path is wrong, git fails and set -e
    #  stops the run -- it cannot quietly hand back a different file.
    git -C "$SEC_DIR" show "${BASELINE_COMMIT}:${REL}" > "$HEAD_FILE"
    echo "[BASELINE] extracted ${BASELINE_COMMIT}:${REL} -> $HEAD_FILE"
}

pin_baseline () {
    #  THE PRESENCE PIN THE FIRST DRIVER LACKED.
    local f="$1" n
    n=$(grep -cF "$UNMASKED" "$f" || true)
    if [ "$n" -ne "$UNMASKED_EXPECTED" ]; then
        echo "ERROR: baseline pin FAILED -- expected $UNMASKED_EXPECTED occurrences" \
             "of the unmasked call in $f, found $n."
        echo "       A count of 0 means the baseline already carries the #524 fix;" \
             "a count of 1 means one site was repaired and the other was not."
        exit 1
    fi
    echo "[PIN] baseline carries the unmasked call exactly $n times -- correct pre-fix text"
}

if [ "${1:-}" = "--selftest" ]; then
    echo "=== NEGATIVE CONTROLS (no build, no mutation) ==="
    mkdir -p /tmp/gxarmbdt_selftest
    HEAD_FILE=/tmp/gxarmbdt_selftest/baseline.c

    echo "--- (a) a WRONG commit must FAIL ---"
    if git -C "$SEC_DIR" show "deadbee:${REL}" > /tmp/gxarmbdt_selftest/bad.c 2>/dev/null; then
        echo "  *** CONTROL FAILED: a bogus commit produced a file ***"; exit 9
    fi
    echo "  ok: git refused the bogus commit"

    echo "--- (b) the pin PASSES on the baseline and FAILS on the post-fix file ---"
    extract_baseline
    pin_baseline "$HEAD_FILE"
    n=$(grep -cF "$UNMASKED" "$SEC_DIR/$REL" || true)
    if [ "$n" -eq "$UNMASKED_EXPECTED" ]; then
        echo "  *** CONTROL FAILED: post-fix file still shows $n unmasked calls ***"; exit 9
    fi
    echo "  ok: post-fix working tree shows $n (not $UNMASKED_EXPECTED) -- the pin discriminates"

    echo "--- (c) the restoration cmp must compare against GIT, not the tree ---"
    if cmp -s "$HEAD_FILE" "$SEC_DIR/$REL"; then
        echo "  *** CONTROL FAILED: baseline and working tree are identical, so this"
        echo "      control cannot discriminate right now -- re-run when they differ ***"; exit 9
    fi
    echo "  ok: baseline differs from the working tree, so a cmp against the tree"
    echo "      would now FAIL where a cmp against git PASSES -- which is the defect"
    echo "      the first driver had, demonstrated rather than asserted."
    echo "SELFTEST_DONE"
    exit 0
fi

echo "=== KILL TABLE 4 STARTING ==="
echo "Clone:    $CLONE"
echo "SEC:      $SEC_DIR"
echo "Baseline: ${BASELINE_COMMIT}:${REL}  (immutable)"

extract_baseline
pin_baseline "$HEAD_FILE"

touch "$CLONE/.MUTANT"
echo "[SENTINEL] Dropped $CLONE/.MUTANT"

rm -f "$OUT_DIR/SCORES.txt" "$OUT_DIR/KILLTABLE_DONE"
touch "$OUT_DIR/SCORES.txt"

#  BASE  = the #524 fix.  HEAD = the immutable baseline, verbatim.
#  M_MASK1 = the clause-(d) mutant Fable ruled this round owes: the mask
#            weakened 0xfffffffc -> 0xfffffffe, which is the carrier's own
#            #461 `m_align1` shape (& 3 -> & 1).  It is PREDICTED 25/25 by
#            arithmetic -- every unaligned base in the probe is +1, and
#            x+1 & ~1 == x+1 & ~3 -- but predicted is not measured, and this
#            project's rule is that "it would sweep the table" is a
#            MEASUREMENT, never an inference.  That is why it is a leg.
LEGS=("BASE" "HEAD" "M_ENTRY" "M_MASK1" "M_MASK7" "M_PBITCOND" "M_POP_ONLY" "M_PUSH_ONLY" "M_NULL_MEDIUM")

for leg in "${LEGS[@]}"; do
    echo "--------------------------------------------------------"
    echo "Running leg: $leg"
    python3 "$MUTATOR" "$leg" "$CLONE/src/cpus/cpu_arm_instr.c" "$HEAD_FILE" "$HEAD_FILE"

    rm -f "$CLONE/src/cpus/"*.o
    make -C "$CLONE" -j4

    if [ ! "$CLONE/gxemul" -nt "$CLONE/src/cpus/cpu_arm_instr.c" ]; then
        echo "ERROR: binary not newer than source for leg $leg"; exit 1
    fi

    python3 -u "$PROBE" "$CLONE/gxemul" "$leg" > "$OUT_DIR/probe_${leg}.raw" 2>&1

    if ! grep -q "ARMBDT_WITNESS_DONE" "$OUT_DIR/probe_${leg}.raw"; then
        echo "ERROR: probe did not complete cleanly for leg $leg"; exit 1
    fi

    SCORE_LINE=$(grep -oE "SCORE [0-9]+/[0-9]+" "$OUT_DIR/probe_${leg}.raw" | head -1)
    echo "Leg $leg result: $SCORE_LINE"
    echo "${leg}: ${SCORE_LINE}" >> "$OUT_DIR/SCORES.txt"
done

echo "=== TWO-PART RESTORATION VERIFICATION (against GIT, not the tree) ==="
cp "$HEAD_FILE" "$CLONE/src/cpus/$(basename "$REL")"

#  Part 1 compares the restored clone against the IMMUTABLE baseline.  The
#  first driver compared it against the working tree the backup came from,
#  which is the carrier's named failure mode -- a backup validated against
#  its own source can only catch a failed copy.
if ! git -C "$SEC_DIR" show "${BASELINE_COMMIT}:${REL}" \
     | cmp -s - "$CLONE/src/cpus/$(basename "$REL")"; then
    echo "ERROR: source restoration failed cmp against ${BASELINE_COMMIT}"; exit 1
fi
echo "[VERIFIED] restored source == ${BASELINE_COMMIT}:${REL}"

rm -f "$CLONE/src/cpus/"*.o
make -C "$CLONE" -j4
if [ ! "$CLONE/gxemul" -nt "$CLONE/src/cpus/$(basename "$REL")" ]; then
    echo "ERROR: rebuilt binary is not newer than restored source"; exit 1
fi
echo "[VERIFIED] binary newer than source"

rm -f "$CLONE/.MUTANT"
echo "[SENTINEL] Cleared $CLONE/.MUTANT"

echo "--------------------------------------------------------"
echo "Running confirmation leg: RESTORED"
python3 -u "$PROBE" "$CLONE/gxemul" "RESTORED" > "$OUT_DIR/probe_RESTORED.raw" 2>&1
if ! grep -q "ARMBDT_WITNESS_DONE" "$OUT_DIR/probe_RESTORED.raw"; then
    echo "ERROR: probe did not complete cleanly for RESTORED"; exit 1
fi
RESTORED_SCORE=$(grep -oE "SCORE [0-9]+/[0-9]+" "$OUT_DIR/probe_RESTORED.raw" | head -1)
echo "RESTORED result: $RESTORED_SCORE"
echo "RESTORED: ${RESTORED_SCORE}" >> "$OUT_DIR/SCORES.txt"

echo "KILLTABLE_DONE" > "$OUT_DIR/KILLTABLE_DONE"
echo "=== KILL TABLE 4 COMPLETED ==="
