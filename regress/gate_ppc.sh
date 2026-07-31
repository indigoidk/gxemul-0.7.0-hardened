#!/bin/bash
# GATE 13 -- PowerPC single-precision conversion fidelity, on real guest instructions.
#
# What this protects
# -----------------
# #304 gave `frsp` the rounding mode it never read (the narrowing was a host C cast,
# nearest-always, so the three directed modes were unreachable) and taught `stfs` the
# ISA's denormalization band, which it had been flushing to signed zero. #305 stopped
# `lfs`/`stfs` from destroying a NaN's sign and payload: the value-domain transport
# (interpret -> host double -> store) structurally cannot carry them, so the NaN classes
# are handled by bit surgery on the pattern instead.
#
# Why this gate had to exist BEFORE the fixes
# ------------------------------------------
# There is no PowerPC OS rig -- no guest boots on this path -- so the defects were found
# by a cold-debugger spike and every one of them could only be believed once an
# instrument measured it. The rows below were run against the COMMITTED build first and
# their committed bytes recorded; the fix then had to flip exactly the DISC rows and
# leave every PIN untouched. That baseline sweep is what makes "the fix worked" a
# measurement rather than a claim, and it caught three of the author's own wrong
# predictions before any code changed (frsp's RN overflow to Infinity is ISA-correct,
# and the negative band row keeps its sign through the flush).
#
# Three row classes, and why PINs are not decoration
# -------------------------------------------------
#   PIN  -- correct today, must stay. Includes two POLICY pins: for finite values at
#           and above ~2^129 the letter of Book I would splice-WRAP the exponent, and
#           this fork deliberately keeps #287's +/-Inf instead (the letter turns a
#           finite overflow into a NaN pattern: 1.5*2^128 -> 0x7FC00000). A policy pin
#           failing means someone changed a known divergence without updating the
#           record -- worth knowing either way.
#   DISC -- discriminator: committed byte is the defect, want flips with the fix.
#   DIV  -- known divergence left to a later round, pinned so it cannot drift.
#
# #310's thirteen rows cover the eight float UPDATE forms, every one of which
# stopped the emulator before this round -- neither the primary opcodes
# 0x31/0x33/0x35/0x37 nor the indexed 567/631/695/759 were defined or decoded.
# Each asserts BOTH halves of the contract: the value transferred and rA
# receiving the effective address. Two non-update rows assert the mirror image,
# that rA is unchanged, so an implementation that updated everything would fail
# as loudly as one that updated nothing.
#
# The control row is load-bearing: `msr=0x2000` must take or every FP instruction
# raises FPU-unavailable and the probe measures nothing. A dead probe SKIPs; it never
# passes quietly. The mode rows additionally read FPSCR back, because `mtfsf`'s FM-mask
# decode is scrambled (its own filed defect) and a mode that silently failed to take
# would turn every directed-mode row into a second copy of the RN row.
set -u
cd "$(dirname "$0")"
. ./lib.sh

gate_begin "gate 13: PowerPC single conversion (#304/#305)"

PMAX=${PMAX:-$ROOT/build/gxemul}
LOG=$LOGDIR/gate_ppc.log

need_exec "$PMAX"
need_file "$IMAGES/netbsd401-macppc-GENERIC"
command -v python3 >/dev/null || gate_skip "python3 not available"

note "binary : $PMAX"
note "machine: macppc/G4, NetBSD kernel loaded so the machine constructs; never executed"
note "cold debugger; big-endian (dump renders value order); msr=0x2000 required for FP"

python3 ppc_rounding_probe.py "$PMAX" "$IMAGES" > "$LOG" 2>&1 || true

if ! grep -q "PPC_CONV_RESULT=" "$LOG"; then
    note "probe produced no result line; last lines follow"
    tail -5 "$LOG" | sed 's/^/       /'
    gate_skip "probe did not complete"
fi

grep -E " ok$| FAIL$" "$LOG" | sed 's/^/       /'

# A probe whose control row failed has measured NOTHING, and no other row may be
# believed -- this harness has been bitten by a probe that reported a defect off
# sentinel reads while its guest code had never run.
ctrl=$(grep -o "PPC_CONV_CONTROL=[A-Z]*" "$LOG" | tail -1 | cut -d= -f2)
check "control rows prove the probe measures" "${ctrl:-missing}" "OK"

# The rounding-mode WRITE channel is proven once per mode, in its own sessions, by
# reading FPSCR back through the guest's own mffs. Both numbers are asserted, because
# "0 bad" is also what a probe reports when it never read FPSCR at all: the first
# version parsed the debugger's plain `reg`, which does not print FPSCR on this CPU,
# so the check passed vacuously on every run until a diff-review seat predicted the
# hole and the rewrite measured it (43 rows of "unparsed").
modebad=$(grep -o "PPC_CONV_MODEWRITES_BAD=[0-9]*" "$LOG" | tail -1 | cut -d= -f2)
modereads=$(grep -o "PPC_CONV_MODEREADS=[0-9]*" "$LOG" | tail -1 | cut -d= -f2)
check "every rounding-mode write took"    "${modebad:-missing}"   "0"
check "all four modes read back by guest" "${modereads:-0}"       "4"

res=$(grep -o "PPC_CONV_RESULT=[0-9]*/[0-9]*" "$LOG" | tail -1 | cut -d= -f2)
got=${res%/*}; want=${res#*/}
check "rows run"     "$want" 67
check "rows correct" "$got"  "$want"

# The table must keep enough of each class to be worth running: a gate whose rows are
# all pins cannot detect a reverted fix, and one with no pins cannot detect collateral
# damage. Both counts are asserted rather than trusted.
disc=$(grep -c " DISC " "$LOG")
pins=$(grep -c " PIN " "$LOG")
check_min "discriminating rows present" "$disc" 38
check_min "pinned rows present"         "$pins" 25

# The one row that records a divergence this round deliberately does NOT fix.
div=$(grep -c " DIV " "$LOG")
check "divergence rows recorded" "$div" 1

# Named rows, one per contract, so a single site reverting cannot hide behind a total.
#
# The pattern demands TWO spaces after the name, not one: the probe pads names to a
# fixed column, so a name that is a PREFIX of another ("frsp qNaN" of "frsp qNaN
# payload") matched both rows and the check counted 2 where it wanted 1. A check that
# counts the wrong rows is the same species as a check that cannot fail -- it was
# passing for the wrong reason the moment the table grew a longer name.
for v in "frsp qNaN" "frsp sNaN" "frsp 1+3ulp/2 RZ" "frsp band RP" "frsp band- RM" \
         "frsp tiny RP" "frsp 2^128 RZ" "frsp carry-up RZ" \
         "stfs 2^-127" "stfs band tail" "stfs band-" "stfsx 2^-127" \
         "stfs qNaN payload" "stfs sNaN passthrough" "stfsx qNaN payload" \
         "lfs qNaN-" "composed frsp->stfs NaN" "lfsx qNaN-" "VXSNAN sticky" \
         "fctiwz qNaN div" \
         "lfsu value" "lfsu updates r3" "lfs leaves r3" \
         "lfdu value" "lfdu updates r3" "stfsu updates r3" \
         "stfdu updates r3" "lfsux value" "lfsux updates r3" \
         "lfsx leaves r3" "lfdux updates r3" "stfsux updates r3" \
         "stfdux updates r3"; do
    n=$(count "$LOG" "^$v  .*ok$")
    check "  row: $v" "$n" 1
done

# The pins that record a DELIBERATE divergence from the letter of the ISA.
for v in "stfs 2^129 policy" "stfs 3\*2^128 policy" "frsp 2^128 RN"; do
    n=$(count "$LOG" "^$v .*ok$")
    check "  policy pin: $v" "$n" 1
done

gate_end
