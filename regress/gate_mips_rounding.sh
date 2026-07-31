#!/bin/bash
# GATE 12 -- MIPS cvt.d.l AND cvt.s.l rounding (arc), and #303 subnormal-operand
# decode on BOTH MIPS rigs.
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
PMAX_KERNEL=$ROOT/gxemul_pmax_rig/bsd
LOG=$LOGDIR/gate_mips_rounding.log
SLOG=$LOGDIR/gate_mips_subnorm.log

# ALL required inputs preflighted here, before either probe runs: a gate_skip fired
# after the first section has recorded checks would return SKIP and DISCARD any
# failures already found (a diff-review seat's finding).
need_exec "$PMAX"
need_file "$KERNEL"
need_file "$PMAX_KERNEL"
command -v python3 >/dev/null || gate_skip "python3 not available"

note "binary : $PMAX"
note "kernel : $KERNEL (loaded so the machine constructs; never executed)"
note "cold debugger; guest sets FCSR via ctc1 and loads its operand via ldc1"

python3 mips_rounding_probe.py "$PMAX" "$KERNEL" > "$LOG" 2>&1 || true

if ! grep -q "MIPS_CVT_RESULT=" "$LOG"; then
    note "probe produced no result line; last lines follow"
    tail -5 "$LOG" | sed 's/^/       /'
    check "cvt probe completed" "no" "yes"
    gate_end; exit $?
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

# ---- #303: subnormal-operand decode, both rigs -----------------------------------
# pmax/R3000 CONSUMES the decode (#246's gate cannot deliver on EXC3K -- the R3010's
# interrupt pin is unwired -- so fpu_unimpl_trap returns 0 and execution falls
# through; two panel seats refuted "MIPS is fully masked" and the rig agreed). The
# pmax rows are #303 discriminators, including the pinned KNOWN-CHANGE flip row on
# the NEGATIVE operand (true -2^-148 takes the deliberate #287/#292 store flush to
# MINUS zero -- the sign #287 preserves -- so the row trips a #287 revert too, which
# a positive row cannot; a diff-review seat's finding). arc/R4000 keeps the trap: its
# row proves the sentinel survives AND carries an integer-store execution witness so
# a dead session cannot false-pass. See mips_subnorm_probe.py.
#
# The last five rows are #309's. An unimplemented REGIMM sub-opcode used to reach
# `goto bad`, which sets cpu->running = 0 -- a legal-to-attempt encoding stopping the
# emulator instead of raising the Reserved Instruction exception real silicon raises.
# These rows assert the OUTCOME rather than a register: "RI" for the unimplemented rt
# values, "ran-no-exception" for BGEZ, which must still branch. Both rigs run them,
# because a fix reaching only one dyntrans mode would pass a single-rig gate.
python3 mips_subnorm_probe.py "$PMAX" "$PMAX_KERNEL" "$KERNEL" > "$SLOG" 2>&1 || true

if ! grep -q "MIPS_SUBN_RESULT=" "$SLOG"; then
    note "subnormal probe produced no result line; last lines follow"
    tail -5 "$SLOG" | sed 's/^/       /'
    #  a CHECK, not a gate_skip: the cvt section above has already recorded its
    #  results, and a skip here would discard them (diff-review seat's finding).
    check "subnormal probe completed" "no" "yes"
    gate_end; exit $?
fi

grep -E " ok$| FAIL" "$SLOG" | sed 's/^/       /'

sres=$(grep -o "MIPS_SUBN_RESULT=[0-9]*/[0-9]*" "$SLOG" | tail -1 | cut -d= -f2)
sgot=${sres%/*}; swant=${sres#*/}
check "subnorm rows run"     "$swant" 9
check "subnorm rows correct" "$sgot"  "$swant"
for v in "pmax mul.s subn" "pmax cvt.d.s subn" "pmax add.s flip" "arc mul.s trap" \
         "pmax regimm rt=0x15" "arc regimm rt=0x15" "pmax regimm rt=0x1e" \
         "pmax BGEZ control" "arc BGEZ control"; do
    n=$(count "$SLOG" "^$v .*ok$")
    check "  subnorm: $v" "$n" 1
done

gate_end
