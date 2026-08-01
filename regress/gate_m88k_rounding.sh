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

# 73 = 46 as of #303 (25 rounding-mode rows + #302's six trnc and eight int/nint rows,
# which the decoder used to HALT on + #303's six subnormal-operand rows) + #306's
# eighteen mixed-format rows + #307's seven tcnd trap rows + #308's two round-to-nearest witnesses.
#
# #306 closed a FAMILY, not the two encodings that happened to get reported: the size
# field is a format TRIPLE, so each of fadd/fsub/fmul/fdiv has eight legal forms, and
# this tree implemented whichever ones its guests happened to execute -- fsub had .sds
# while fadd did not. Twelve were missing and every one stopped the emulator on a legal
# instruction; six were measured halting on this rig before the fix.
#
# The fmul/fdiv mode rows earned their place twice over, because the fix took two
# tries and a seat's witness caught each one.
#
# Draft one copied fmul_sss's "compute in host double, round at the store", which is
# safe ONLY because two SINGLE sources make the product exact in a double. A double
# source voids that and the two roundings compound: 3.0f times the nearest double to
# 1/3 has an exact product just BELOW 1.0, the host product ties to exactly 1.0, and
# the toward-zero store answers 0x3f800000 where one correct rounding owes 0x3f7fffff.
# The "fmul.ssd RZ" and "RM" rows are that failure.
#
# Draft two moved to #300's _rm helpers -- and those return the host result UNCHANGED
# under nearest, because for a DOUBLE destination the host's nearest result already is
# correct. Narrowed to single it is a double rounding again, in the mode OpenBSD/m88k
# userland actually runs. The two "odd ..." rows are that failure: 1.5f times
# 0x3FF555556AAAAAAB gave 0x40000000 for 0x40000001, and a quotient landing exactly on
# the 1+2^-24 midpoint gave 0x3f800000 for 0x3f800001.
#
# #308's round-to-odd helpers fix every mode at once (53 >= 2*24 + 2, so an odd
# intermediate can never sit on a destination midpoint), verified offline against a
# single correct rounding over 960,000 operand pairs in all four modes.
#
# #307's rows measure a TRAP, so their witness is the PC after one step rather than a
# register: taken lands at VBR + 8*vector, not-taken advances by four, and either way
# the emulator is still running -- which is the point, since every one of these
# encodings stopped it before. The vector is 128 or above on purpose: vectors 0..127
# are the hardware ones and vector 0 is RESET, which really does stop the machine.
check "rows run"       "$want" 80
check "rows correct"   "$got"  "$want"

# The four swap-tripwire rows asserted by name: these are the rows a 2<->3 decode
# mistake fails while everything symmetric stays green.
for v in "fadd-neg toward+Inf" "fadd-neg toward-Inf" \
         "flt-neg toward-Inf" "flt-neg toward+Inf"; do
    n=$(count "$LOG" "^$v .*ok$")
    check "  asymmetric: $v" "$n" 1
done

# One row per wired site, so a single site silently reverting cannot hide. The last
# four are #299's: the flipped band row, the exact-zero sign pair, and the Inf
# pass-through witness on the double-operand sds arm.
for v in "fadd-pos RN" "fsub.sss RN" "fsub.sds RN" "fmul RN tie" "fdiv RN" "flt-pos RN tie" \
         "fadd band toward+Inf" "fadd zero toward-Inf" "fadd zero RN" "fsub.sds inf" "fdiv.ddd 1/10 RZ" \
         "trncSS +Inf" "trncSS qNaN-" "trncSD 2^31" "trncSD qNaN+" "trncSD qNaN-" \
         "intSS 5.2 +Inf" "intSS -5.2 -Inf" "nintSS 2.5 tie" "nintSS 3.5 tie" "nintSD 2.5 tie" \
         "subn fmul +" "subn fmul -" "subn fmul.dss" "subn fmul.ddd" "subn fcmp.ssd" \
         "subn flip x2.0" \
         "fmul.ssd RZ" "fmul.ssd RN" "fmul.ssd RM" "fadd.ssd RN" "fadd.sds RN" \
         "fadd.sdd RN" "fsub.ssd RN" "fsub.sdd RN" "fmul.sds RN" "fmul.sdd RN" \
         "fdiv.ssd RN" "fdiv.ssd RZ" "fdiv.sds RN" "fdiv.sdd RN" \
         "fdiv.dds RN hi" "fdiv.dds RN lo" "fdiv.dds RP lo" \
         "tcnd eq0,r0 taken" "tcnd ne0,r0 fallthru" "tcnd lt0,r2=-1 taken" \
         "tcnd gt0,r2=-1 fall" "tcnd maxneg taken" "tcnd maxneg vs 2^31-1" \
         "tcnd mask 0x1d ~ ne0" "odd fmul.sds RN" "odd fdiv.ssd RN"; do
    n=$(count "$LOG" "^$v .*ok$")
    check "  site: $v" "$n" 1
done

# ---- #323: bcnd, tcnd's twin ------------------------------------------------
# The handler table was generated only for the nine mask values the assembler
# has mnemonics for; the other twenty-three stayed NULL and the decoder answers
# a NULL entry with `goto bad`, stopping the emulator. Measured: nine named
# masks ran, eight unnamed ones halted.
#
# These rows assert the BRANCH DECISION rather than survival -- rounds 79 and 80
# both showed a survival-only row cannot tell a repaired instruction from one
# that merely stopped faulting, and here it would also miss a mask decoded with
# the wrong condition.
#
# The load-bearing pair is m5=4 against m5=c. Both mean "negative" and they
# differ only on the most negative value, which the manual makes its own class:
# an implementation that collapsed those two classes passes every other row and
# fails "m5=4 MIN fall".
for v in "bcnd m5=4 -1 taken" "bcnd m5=4 MIN fall" "bcnd m5=c MIN taken" \
         "bcnd m5=f all taken" "bcnd m5=0 none fall"; do
    n=$(count "$LOG" "^$v .*ok$")
    check "  #323: $v" "$n" 1
done
# Two of the nine that always worked: the rewrite replaced their named
# comparisons with the mask, so a regression there shows up here.
for v in "bcnd m5=1 gt0 taken" "bcnd m5=2 eq0 taken"; do
    n=$(count "$LOG" "^$v .*ok$")
    check "  #323 pin: $v" "$n" 1
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
