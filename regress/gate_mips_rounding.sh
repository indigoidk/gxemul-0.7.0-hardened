#!/bin/bash
# GATE 12 -- MIPS cvt.d.l AND cvt.s.l rounding (arc), #303 subnormal-operand
# decode on BOTH MIPS rigs, and #295 forced rounding modes on BOTH rigs.
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
FLOG=$LOGDIR/gate_mips_fixedmode.log

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
# values. The BGEZ controls prove an IMPLEMENTED sub-opcode still BRANCHES, through a
# memory witness -- the guest stores one marker on the fall-through path and another at
# the branch target, so taken, not-taken and nothing-ran are three distinguishable
# answers. An earlier version asserted only "did not fault", which a nop would have
# satisfied, and then a PC readback, which parses on arc but not reliably on pmax; the
# dump channel works on both. Both rigs run every row, because a fix reaching only one
# dyntrans mode would pass a single-rig gate.
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

# ---- #295: forced rounding modes, both rigs ---------------------------------
# round.w/ceil.w/floor.w force their architectural modes; the likeliest revert
# (cvt.w's FPU_RM_FROM_FCSR copy-pasted back) EQUALS correct code under the
# default FCSR.RM=0, so every discriminating row sets a NON-ZERO mode via guest
# ctc1. Both rigs as TRANSPORT breadth only -- the constants sit in shared C
# below the rigs' convergence point (cop1_slow -> coproc_function ->
# fpu_function), so either rig kills the constant mutant; what differs per rig
# is operand transport (FR=0 lwc1-pair vs FR=1 ldc1) and the dyntrans
# instantiation. Source-format scope: D rows only -- the .s spellings reach the
# SAME call sites with the SAME constants (the fmt field is masked out of the
# decode switch), and .l is queue item #57. Row names are asserted as FIXED
# strings with embedded delimiters (M295_ROW=rig:name RESULT=PASS): this gate's
# own padded-column `^name .*ok$` pattern has already produced both a
# double-match and an unsatisfiable row elsewhere in the battery.
# selftest_mutation_295.sh (manual lane, full rebuild per mutant) proves each
# row flips under its op's mutant; the trunc/NaN/cvt/cfc1 rows are CONTROLS and
# cannot flip by construction.
python3 mips_fixedmode_probe.py "$PMAX" "$PMAX_KERNEL" "$KERNEL" both > "$FLOG" 2>&1 || true

if ! grep -q "M295_RESULT=" "$FLOG"; then
    note "fixedmode probe produced no result line; last lines follow"
    tail -5 "$FLOG" | sed 's/^/       /'
    check "fixedmode probe completed" "no" "yes"
    gate_end; exit $?
fi

grep "M295_ROW=" "$FLOG" | sed 's/^/       /'

# The ctc1 witness pair is LOAD-BEARING per rig: on the fixed binary every
# discriminating row is FCSR-independent, so only the cvt.w row (which consumes
# FCSR) and the cfc1 readback prove the guest's mode write landed. A trunc row
# cannot -- trunc is mode-immune in every state.
for rig in pmax arc; do
    c=$(grep -o "M295_CONTROL=$rig:[A-Z]*" "$FLOG" | tail -1 | cut -d: -f2)
    check "  fixedmode ctc1 witness ($rig)" "${c:-missing}" "OK"
done

fres=$(grep -o "M295_RESULT=[0-9]*/[0-9]*" "$FLOG" | tail -1 | cut -d= -f2)
fgot=${fres%/*}; fwant=${fres#*/}
check "fixedmode rows run"     "$fwant" 28
check "fixedmode rows correct" "$fgot"  "$fwant"

for rig in pmax arc; do
    for n in r25rp r35rm r27rm rn25rm rbnd c21rm cn225rm f29rp fn225rp \
             cvt27rm cfc1 t35rp tn35rm nan; do
        c=$(grep -cF "M295_ROW=$rig:$n RESULT=PASS" "$FLOG")
        check "  fixedmode: $rig:$n" "$c" 1
    done
done

gate_end
