#!/bin/bash
# GATE 12 -- MIPS cvt.d.l AND cvt.s.l rounding, on real guest instructions (arc, R4400).
#
# What this protects
# -----------------
# #301 redoes cvt.d.l's int64 -> double conversion from the raw source register, in
# exact integer arithmetic, under the FCSR mode. Before it, the conversion happened as a
# host cast inside ieee_interpret_float_value -- under the HOST's nearest mode -- and
# the D store is a pure re-encode, so the mode never got a say for integers with more
# than 53 significant bits.
#
# Why this gate exists SEPARATELY from gate 2's #301 vectors: the offline vectors pin
# the pure helper, but the CVT-case WIRING in cpu_mips_coproc.c could revert silently
# while the helper stayed perfect -- the same helper-vs-wiring hole a #299 panel seat
# named for build flags. These rows run the real decode -> fpu_op -> store path with the
# guest setting FCSR itself via ctc1.
#
# Scope: arc only. cvt.d.l is MIPS-III+ and the pmax R3000 raises RI on the ldc1
# (measured; the trace is in the round-66 CHANGELOG block).
set -u
cd "$(dirname "$0")"
. ./lib.sh

gate_begin "gate 12: MIPS cvt.d.l/cvt.s.l rounding (#301)"

PMAX=${PMAX:-$ROOT/build/gxemul}
KERNEL=$ROOT/gxemul_arc_rig/bsd
LOG=$LOGDIR/gate_mips_rounding.log

need_exec "$PMAX"
need_file "$KERNEL"
command -v python3 >/dev/null || gate_skip "python3 not available"

note "binary : $PMAX"
note "kernel : $KERNEL (loaded so the machine constructs; never executed)"
note "cold debugger; guest sets FCSR via ctc1 and loads its operand via ldc1"

python3 mips_rounding_probe.py "$PMAX" "$KERNEL" > "$LOG" 2>&1 || true

if ! grep -q "MIPS_CVT_RESULT=" "$LOG"; then
    note "probe produced no result line; last lines follow"
    tail -5 "$LOG" | sed 's/^/       /'
    gate_skip "probe did not complete"
fi

grep -E " ok$| FAIL" "$LOG" | sed 's/^/       /'

# The control row is load-bearing: a dead probe must be a SKIP-shaped failure, never a
# quiet pass of zero rows or a false REPRODUCED. The probe's first version reported a
# defect off six sentinel reads while its guest code had never run.
ctrl=$(grep -o "MIPS_CVT_CONTROL=[A-Z]*" "$LOG" | tail -1 | cut -d= -f2)
check "control row proves the probe measures" "${ctrl:-missing}" "OK"

res=$(grep -o "MIPS_CVT_RESULT=[0-9]*/[0-9]*" "$LOG" | tail -1 | cut -d= -f2)
got=${res%/*}; want=${res#*/}
check "rows run"     "$want" 11
check "rows correct" "$got"  "$want"

# The directed rows by name: these are the rows a reverted #301 fails (they read the
# host-nearest answer) while every RN row and the control stay green.
for v in "2^53+1 RP" "2^54+7 RZ" "2^54+7 RP" "-(2^54+7) RZ" "-(2^54+7) RM" "SL dbltie RN" "FR0 2^53+1 RP"; do
    n=$(count "$LOG" "^$v .*ok$")
    check "  directed: $v" "$n" 1
done

gate_end
