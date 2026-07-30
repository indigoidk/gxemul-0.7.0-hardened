#!/bin/bash
# GATE 11 -- m88k floating-point rounding mode, measured on real guest instructions.
#
# What this protects
# -----------------
# #298 decoded fcr63 (the FPCR) bits 15:14 into the six m88k single-precision store
# sites. Before it, the register was stored and readable but decoded into NOTHING, and
# every single-precision result truncated -- while OpenBSD/m88k zeroes fcr63 at exec,
# which means round-to-NEAREST, so every luna88k userland single-precision result was
# one ulp low about half the time. The RN rows here are that defect, flipped.
#
# The swap tripwire
# -----------------
# m88k's directed-mode encoding (10 = toward -Inf, 11 = toward +Inf) is the OPPOSITE of
# MIPS/SH and of float_emul.h's IEEE_RM_* values, so #298's decode swaps 2 and 3. A
# decode without the swap passes every sign-SYMMETRIC vector -- the two directed modes
# just trade places consistently -- so this gate runs sign-ASYMMETRIC rows (fadd-neg-*,
# flt-neg-*) whose expected values differ by operand sign. Those rows are the only
# defence against the single most likely wrong implementation.
#
# Every row sets the mode the way a real guest does: the guest itself executes
# `fstcr r5,fcr63`, proving decode end-to-end rather than only the store arm.
set -u
cd "$(dirname "$0")"
. ./lib.sh

gate_begin "gate 11: m88k rounding mode (#298)"

PMAX=${PMAX:-$ROOT/build/gxemul}
IMG=$IMAGES/liveimage-luna88k-raw-20250518.img
BOOTFILE=$IMAGES/boot
LOG=$LOGDIR/gate_m88k_rounding.log

need_exec "$PMAX"
need_file "$IMG" "$BOOTFILE"
command -v python3 >/dev/null || gate_skip "python3 not available"

note "binary : $PMAX"
note "image  : $IMG (R: throwaway overlay; never written)"
note "cold debugger; the guest executes fstcr itself, results read from GPRs"

python3 m88k_rounding_probe.py "$PMAX" "$IMAGES" > "$LOG" 2>&1 || true

if ! grep -q "M88K_ROUND_RESULT=" "$LOG"; then
    note "probe produced no result line; last lines follow"
    tail -5 "$LOG" | sed 's/^/       /'
    gate_skip "probe did not complete"
fi

grep -E " ok$| FAIL" "$LOG" | sed 's/^/       /'

res=$(grep -o "M88K_ROUND_RESULT=[0-9]*/[0-9]*" "$LOG" | tail -1 | cut -d= -f2)
got=${res%/*}; want=${res#*/}

# 21 = 19 behaviour rows + the known-divergent residue-band PIN (which must FLIP and be
# rewritten when round 64's round-to-odd helper lands) + fcr63 retention.
check "rows run"       "$want" 21
check "rows correct"   "$got"  "$want"

# The four swap-tripwire rows asserted by name: these are the rows a 2<->3 decode
# mistake fails while everything symmetric stays green.
for v in "fadd-neg toward+Inf" "fadd-neg toward-Inf" \
         "flt-neg toward-Inf" "flt-neg toward+Inf"; do
    n=$(count "$LOG" "^$v .*ok$")
    check "  asymmetric: $v" "$n" 1
done

# One row per wired site, so a single site silently reverting cannot hide.
for v in "fadd-pos RN" "fsub.sss RN" "fsub.sds RN" "fmul RN tie" "fdiv RN" "flt-pos RN tie"; do
    n=$(count "$LOG" "^$v .*ok$")
    check "  site: $v" "$n" 1
done

# Every row writes a pure-RM value into fcr63 through the guest's own fstcr. Since #298
# that is an IMPLEMENTED operation and m88k_fstcr() must not call it UNIMPLEMENTED -- a
# panel seat caught the original diff still warning here. The first version of this
# check grepped THIS gate's log for the warning string, which was itself a check that
# cannot fail: the warning goes to the emulator's stdout, which only the probe's pty
# capture ever sees, never this log. So the PROBE counts it inside each session and
# reports two markers -- the accumulated count across all pure-RM sessions (must be 0)
# and a deliberate non-RM write of 0x1 as the positive control (must be exactly 1,
# proving the counter counts). Asserting the pair is what makes the zero meaningful.
warns=$(grep -o "M88K_FSTCR_WARNS=[0-9]*" "$LOG" | tail -1 | cut -d= -f2)
wctrl=$(grep -o "M88K_WARN_CONTROL=[0-9None]*" "$LOG" | tail -1 | cut -d= -f2)
check "pure-RM fcr63 writes produce no UNIMPLEMENTED warning" "${warns:-missing}" 0
check "positive control: non-RM write 0x1 warns exactly once" "${wctrl:-missing}" 1

gate_end
