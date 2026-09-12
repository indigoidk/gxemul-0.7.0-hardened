#!/usr/bin/env bash
set -euo pipefail

CLONE="/tmp/gxarmbdt_clone"
SEC_DIR="/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC"
PROBE="$SEC_DIR/regress/artifacts/armbdt/agy_armbdt_witness_20260911.py"
MUTATOR="$SEC_DIR/regress/artifacts/armbdt/killtable_20260911/mutate_armbdt.py"
OUT_DIR="$SEC_DIR/regress/artifacts/armbdt/killtable_20260911"
HEAD_FILE="$CLONE/cpu_arm_instr.c.HEAD_8d372aa"

echo "=== KILL TABLE RUN STARTING ==="
echo "Target clone: $CLONE"
echo "SEC dir: $SEC_DIR"

# Verify SEC cpu_arm_instr.c matches pure HEAD commit 8d372aa
git -C "$SEC_DIR" log --oneline -1
# Save head file
cp "$SEC_DIR/src/cpus/cpu_arm_instr.c" "$HEAD_FILE"

# Drop clone-local .MUTANT sentinel BEFORE first mutation
touch "$CLONE/.MUTANT"
echo "[SENTINEL] Dropped $CLONE/.MUTANT"

# Clear prior score file
rm -f "$OUT_DIR/SCORES.txt" "$OUT_DIR/KILLTABLE_DONE"
touch "$OUT_DIR/SCORES.txt"

LEGS=("BASE" "HEAD" "M_ENTRY" "M_POP_ONLY" "M_PUSH_ONLY" "M_NULL_MEDIUM")

for leg in "${LEGS[@]}"; do
    echo "--------------------------------------------------------"
    echo "Running leg: $leg"
    python3 "$MUTATOR" "$leg" "$CLONE/src/cpus/cpu_arm_instr.c" "$HEAD_FILE" "$HEAD_FILE"
    
    # Recompile
    rm -f "$CLONE/src/cpus/"*.o
    make -C "$CLONE" -j4
    
    # Verify binary is newer than source
    if [ ! "$CLONE/gxemul" -nt "$CLONE/src/cpus/cpu_arm_instr.c" ]; then
        echo "ERROR: gxemul binary is not newer than cpu_arm_instr.c for leg $leg"
        exit 1
    fi
    
    # Run probe
    python3 -u "$PROBE" "$CLONE/gxemul" "$leg" > "$OUT_DIR/probe_${leg}.raw" 2>&1
    
    # Verify sentinel
    if ! grep -q "ARMBDT_WITNESS_DONE" "$OUT_DIR/probe_${leg}.raw"; then
        echo "ERROR: probe did not complete cleanly for leg $leg"
        exit 1
    fi
    
    SCORE_LINE=$(grep -oE "SCORE [0-9]+/[0-9]+" "$OUT_DIR/probe_${leg}.raw" | head -1)
    echo "Leg $leg result: $SCORE_LINE"
    echo "${leg}: ${SCORE_LINE}" >> "$OUT_DIR/SCORES.txt"
done

# Copy candidate fix output to witness_fix.out
cp "$OUT_DIR/probe_BASE.raw" "$SEC_DIR/regress/artifacts/armbdt/witness_fix.out"
echo "Copied probe_BASE.raw to witness_fix.out"

# Two-part restoration verification
echo "=== TWO-PART RESTORATION VERIFICATION ==="
cp "$HEAD_FILE" "$CLONE/src/cpus/cpu_arm_instr.c"

# Part 1: cmp clean against SEC
if ! cmp -s "$CLONE/src/cpus/cpu_arm_instr.c" "$SEC_DIR/src/cpus/cpu_arm_instr.c"; then
    echo "ERROR: source restoration failed cmp against SEC"
    exit 1
fi
echo "[VERIFIED] cmp clean against SEC"

# Part 2: Rebuild binary and verify fresher than source
rm -f "$CLONE/src/cpus/"*.o
make -C "$CLONE" -j4
if [ ! "$CLONE/gxemul" -nt "$CLONE/src/cpus/cpu_arm_instr.c" ]; then
    echo "ERROR: rebuilt gxemul is not newer than restored source"
    exit 1
fi
echo "[VERIFIED] binary newer than source"

# Only after both parts verified, clear .MUTANT sentinel
rm -f "$CLONE/.MUTANT"
echo "[SENTINEL] Cleared $CLONE/.MUTANT"

# Run confirmation leg on restored tree
echo "--------------------------------------------------------"
echo "Running confirmation leg: RESTORED"
python3 -u "$PROBE" "$CLONE/gxemul" "RESTORED" > "$OUT_DIR/probe_RESTORED.raw" 2>&1
if ! grep -q "ARMBDT_WITNESS_DONE" "$OUT_DIR/probe_RESTORED.raw"; then
    echo "ERROR: probe did not complete cleanly for RESTORED"
    exit 1
fi
RESTORED_SCORE=$(grep -oE "SCORE [0-9]+/[0-9]+" "$OUT_DIR/probe_RESTORED.raw" | head -1)
echo "RESTORED result: $RESTORED_SCORE"
echo "RESTORED: ${RESTORED_SCORE}" >> "$OUT_DIR/SCORES.txt"

echo "KILLTABLE_DONE" > "$OUT_DIR/KILLTABLE_DONE"
echo "=== KILL TABLE COMPLETED SUCCESSFULLY ==="
