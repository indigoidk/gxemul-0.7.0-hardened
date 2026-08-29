#!/bin/bash
#  #491's REAL claim is not "the warning is gone".  It is that the warning was
#  costing an entire gate, and removing it restores that coverage.
#
#  THE CASCADE, from the 2026-08-29 battery:
#    gate_build FAILS (2 warnings)  ->  it withdraws $RIG/gxsec-gxemul at start
#    and republishes only on success  ->  gate_mips need_exec's that binary and
#    reports `SKIP -- missing or non-executable binary`.
#
#  A whole gate's coverage lost and scored as SKIP, not FAIL.  Identical to what
#  one stale allowlist line cost on 2026-08-23.
#
#  So the test is TWO gates in sequence, in the order the battery runs them.
set -u
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
OUT=$SEC/regress/artifacts/diskimagesign/cascade_20260829
mkdir -p "$OUT"
cd "$SEC/regress" || exit 1

echo "=== BEFORE: is the arc rig binary present? ==="
ls -la /mnt/c/DocumentNoSnc/CC/GXEMUL/gxemul_arc_rig/gxsec-gxemul 2>/dev/null || echo "  ABSENT (withdrawn by the failed battery run)"

echo
echo "=== gate 1: gate_build ==="
bash gate_build.sh > "$OUT/gate_build.log" 2>&1
echo "  exit=$?"
grep -E '^  FAIL|warnings|clean-build: (PASS|FAIL)' "$OUT/gate_build.log" | head -12 | sed 's/^/    /'

echo
echo "=== did it republish the shared arc binary? ==="
ls -la /mnt/c/DocumentNoSnc/CC/GXEMUL/gxemul_arc_rig/gxsec-gxemul 2>/dev/null | sed 's/^/  /' || echo "  STILL ABSENT"

echo
echo "=== gate 4: gate_mips -- SKIP or run? ==="
bash gate_mips.sh > "$OUT/gate_mips.log" 2>&1
echo "  exit=$?"
grep -E 'SKIP|mips-rigs: (PASS|FAIL)|^  FAIL' "$OUT/gate_mips.log" | head -8 | sed 's/^/    /'

echo
echo "CASCADE491_DONE"
