#!/bin/bash
# GATE 10 -- SuperH floating-point rounding mode, measured on real guest instructions.
#
# What this protects
# -----------------
# #296 wired FPSCR.RM into thirteen of the sixteen single-precision store sites in
# cpu_sh_instr.c. Before it, the field was guest-writable and decoded NOWHERE: every store
# truncated. Truncation is round-toward-zero, which is the mode the SH-4 resets into, so
# there was no visible defect until you look at a guest that CHANGES the mode -- and
# OpenBSD/landisk installs round-to-nearest at every exec.
#
# Why the vectors look the way they do
# -----------------------------------
# Each one runs under BOTH modes and expects DIFFERENT answers, so reverting #296 turns the
# gate red. Two vectors are deliberately mode-INDEPENDENT and named PIN: they record limits
# that are real and are NOT fixed (double precision cannot be fixed at the store, and the
# host-double double-rounding is shared by every CPU core). A pin failing means someone
# changed a known limitation without updating the record -- which is worth knowing either
# way, and is the opposite of a check that cannot fail.
#
# The gate asserts on the number of discriminating vectors as well as on the results,
# because a table where every vector wants the same answer in both modes would pass
# vacuously. That is the failure mode this harness has now been bitten by five times.
set -u
cd "$(dirname "$0")"
. ./lib.sh

gate_begin "gate 10: SuperH rounding mode (#296)"

PMAX=${PMAX:-$ROOT/build/gxemul}
KERNEL=$IMAGES/openbsd76-landisk-bsd.rd
LOG=$LOGDIR/gate_sh_rounding.log

need_exec "$PMAX"
need_file "$KERNEL"
command -v python3 >/dev/null || gate_skip "python3 not available"

note "binary : $PMAX"
note "kernel : $KERNEL (loaded so the machine constructs; never executed)"
note "cold debugger, no media, no console -- the SCIF drops host->guest writes (#293)"

python3 sh_rounding_probe.py "$PMAX" "$KERNEL" > "$LOG" 2>&1 || true

if ! grep -q "SH_ROUND_RESULT=" "$LOG"; then
    note "probe produced no result line; last lines follow"
    tail -5 "$LOG" | sed 's/^/       /'
    gate_skip "probe did not complete"
fi

sed -n '1,/SH_ROUND_DISCRIMINATING/p' "$LOG" | grep -E "ok$|FAIL" | sed 's/^/       /'

res=$(grep -o "SH_ROUND_RESULT=[0-9]*/[0-9]*" "$LOG" | tail -1 | cut -d= -f2)
got=${res%/*}; want=${res#*/}
disc=$(grep -o "SH_ROUND_DISCRIMINATING=[0-9]*" "$LOG" | tail -1 | cut -d= -f2)

# 30 vector-mode pairs: 15 vectors x 2 modes (9 from #296, 6 ftrc rows from #297).
check     "vector-mode pairs run"                  "$want" 30
check     "vector-mode pairs correct"              "$got"  "$want"
# EXACTLY 7 of the 15 vectors discriminate between the two modes. If this number drops,
# someone weakened the #296 table and the gate stopped being able to fail; if it RISES,
# someone made a mode-independent row (a PIN, or an ftrc row -- ftrc is truncation by
# architecture) depend on FPSCR.RM, which is drift in the other direction.
check     "vectors that discriminate the two modes" "$disc" 7

# Per-instruction closure: naming them individually means a single site silently reverting
# cannot hide behind an aggregate count. The ftrc rows are #297's regression checks: on
# the pre-#297 build the +Inf and +2^40 rows measured 0x80000000 (the raw-cast UB answer)
# where the SH-4 manual owes +MAX.
for v in "fdiv" "float" "fadd" "fmac" "fipr" "ftrv" "fmul" \
         "ftrcS-inf" "ftrcS-ovf" "ftrcS-nan" "ftrcS-edge" \
         "ftrcD-2p31" "ftrcD-neghalf"; do
    n=$(grep -c "^$v .*ok$" "$LOG")
    check "  $v: both modes correct" "$n" 2
done

gate_end
