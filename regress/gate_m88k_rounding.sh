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

# ---- #380: the idle fold vs bcnd.n's delay slot ------------------------------
# COMBINE(idle)'s .n arm installed the handler written for the PLAIN-bcnd
# sequence, so the delay slot -- which the architecture executes once per
# branch, taken or not -- ran ZERO times per taken iteration. On loop exit it
# ran once, which is exactly why no post-loop witness can see this: the probe's
# slot is a STORE and the stored word is read DURING the idle. Rows: `taken`
# (fold path; pre-fix deadbeef, fixed 11111111), `takenj` (-J reference: the
# faithful path stores on every build), `untaken` (the exit path stores on
# every build -- and then execution falls into zeroes and aborts, expected).
# The counter predicate is the reachability half: installs[2]>=1 proves the .n
# arm matched, n_taken_n>=1 proves the NEW handler's taken path ran (a distinct
# counter from the plain handler's, so the mutation self-test -- which reverts
# the install to the plain handler -- reads ntp>=1,ntn==0 instead of blinding
# itself), slot_runs>=1 proves the delay slot was dispatched, in_delayslot==0
# proves the by-construction guard never fired on this rig. Absent counters
# parse as DEAD, never zero.
ILOG=$LOGDIR/gate_m88k_idle.log
python3 m88k_idle_probe.py "$PMAX" > "$ILOG" 2>&1 || true

if ! grep -q "M380_RESULT=" "$ILOG"; then
    note "idle probe produced no result line; last lines follow"
    tail -5 "$ILOG" | sed 's/^/       /'
    check "idle probe completed" "no" "yes"
    gate_end; exit $?
fi

grep -E "M380_ROW=|M380_COUNTERS=" "$ILOG" | sed 's/^/       /'

for v in taken takenj untaken; do
    n=$(grep -cF "M380_ROW=$v RESULT=PASS got=11111111" "$ILOG")
    check "  idle row: $v" "$n" 1
done

#  #381: the predicate requires the EQUALITY slot == ntn, not merely both
#  >= 1 -- in the taken-row session every fold entry is taken, so the two
#  counters are equal there by the handler's construction (one slot dispatch
#  per entry), and a handler that dispatched the slot twice per entry (or a
#  counters line reading slot:12344) satisfied the old >=1 predicate while
#  every value row stayed green (the witness store is idempotent). ntp == 0
#  pins EXCLUSIVE use of the new handler in the same session (the plain
#  handler's counter was parsed and then ignored -- a pass-2 seat's finding).
ctrs=$(grep -o "M380_COUNTERS=[A-Za-z0-9:,/]*" "$ILOG" | tail -1 | cut -d= -f2)
case "$ctrs" in
    installs:*)
        i2=${ctrs#installs:*/*/}; i2=${i2%%,*}
        ntp=${ctrs#*ntp:}; ntp=${ntp%%,*}
        ntn=${ctrs#*ntn:}; ntn=${ntn%%,*}
        slt=${ctrs#*slot:}; slt=${slt%%,*}
        ds=${ctrs#*ds:}
        [ "${i2:-0}" -ge 1 ] && [ "${ntn:-0}" -ge 1 ] && \
            [ "${slt:-0}" -eq "${ntn:-1}" ] && [ "${ntp:-1}" -eq 0 ] && \
            [ "${ds:-1}" -eq 0 ] \
            && cver="OK" || cver="BAD($ctrs)"
        ;;
    *)  cver="DEAD" ;;
esac
check "  idle counters: arm3 fired, slot==ntn, ntp=0, guard quiet" "$cver" "OK"

ires=$(grep -o "M380_RESULT=[0-9]*/[0-9]*" "$ILOG" | tail -1 | cut -d= -f2)
check "idle rows run"     "${ires#*/}" 3
check "idle rows correct" "${ires%/*}" "${ires#*/}"

# ---------------------------------------------------------------------------
#  #433: the M8820x CMMU's five former exit(1) sites, each driven by ONE REAL GUEST
#  INSTRUCTION on the real memory path.  Before that round, 1007 of 1024 word offsets in
#  the device's window terminated the HOST process on a plain read.
#
#  WHY THIS IS HERE AND NOT ONLY IN GATE 2.  regress/diff_m8820x.c calls the access
#  function DIRECTLY, so it proves behaviour but cannot prove the site is REACHABLE -- it
#  would stay green under a change that unmapped the device.  This probe goes through the
#  real address decode and memory_rw plumbing, and it is structurally immune to the harness
#  artifact that corrupted this round's first offline reproduction: a harness fault emits no
#  `m8820x:` diagnostic at all, so a real detection and a broken probe are distinguishable
#  by construction.
#
#  COST: measured 3.6 s for 9 rows on a COLD DEBUGGER -- no boot.  A full luna88k rig drive
#  is 182-233 s.  A booting-rig row was deliberately NOT added: the fix is measured
#  boot-neutral, so it could only re-assert what gate_ab already asserts, at ~200 s of
#  load-sensitive wall clock in a battery already carrying ~37 such oracles.
SLOG=$LOGDIR/m8820x_sites.log
python3 m8820x_sites_probe.py "$PMAX" "$IMAGES" > "$SLOG" 2>&1 || true
grep -E "^(VALUE|CONTROL|site)" "$SLOG" | sed 's/^/       /'

if ! grep -q "M8820X_SITES_" "$SLOG"; then
    note "m8820x site probe produced no verdict; last lines follow"
    tail -5 "$SLOG" | sed 's/^/       /'
    check "m8820x site probe completed" "no" "yes"
else
    check "m8820x: every site survives a real guest instruction" \
          "$(grep -c 'M8820X_SITES_PASS' "$SLOG")" "1"
    #  A FLOOR, not an exact count, so adding a row later is not a red gate.
    check_min "m8820x: rows actually driven" \
          "$(grep -oE 'SURVIVED=[0-9]+' "$SLOG" | grep -oE '[0-9]+' | head -1)" 9
    #  VALUES, NOT SURVIVAL (rounds 79/80): the seeded 88200 rev-9 id can only have come
    #  back through this device, so a "fix" that stopped faulting without writing the
    #  result back is red here and green under any survival-only row.
    check "m8820x: CMMU_IDR still reads 0x00a90000 through a guest load" \
          "$(grep -c 'VALUE ld CMMU_IDR.*r4=0x00a90000' "$SLOG")" "1"
    #  EVERY planted word was disassembled and matched before being stepped -- the defence
    #  against the hand-assembled-encoding trap this project has been bitten by.
    check "m8820x: no planted word failed its disassembly check" \
          "$(grep -c 'dis_ok=False' "$SLOG")" "0"
    #  The fold, end to end: command 0x34 is HANDLED now, so it must survive WITHOUT a
    #  complaint, while 0x24 (a real PROBE) still complains once.
    check "m8820x: the folded command 0x34 survives silently" \
          "$(grep -A1 'st SCR cmd 0x34' "$SLOG" | grep -c 'emulator said')" "0"
    check "m8820x: an unimplemented command still complains once" \
          "$(grep -c 'unimplemented command 0x24; ignored (reported once)' "$SLOG")" "1"
fi

#  ---------------------------------------------------------------------------
#  #438: the INT_ST_MASK witness, wired here because this gate already depends on the
#  luna88k binary and images -- a new gate script would move GATE_MANIFEST, a bigger claim
#  than one probe is worth.
#
#  *** IT SHIPPED UNWIRED IN cf4b083, AND THAT IS WHY gate 6 WENT LATENTLY RED. *** With no
#  gate invoking it, nothing forced a gate run, so its three #392 constructs never moved
#  EXPECT_CONVERTED and the failure sat unseen until a review seat recomputed the census by
#  hand.  A probe wired in the same commit cannot hide that way.
#
#  The probe is BOTH halves of the ladder: a rung-3 WITNESS (it shows the pre-fix symptom on
#  a committed unmodified machine description) and a DETECTOR (D1-D4 separate store-as-is
#  from masked from not-storing, kill a narrowed guard, and pin the SECOND case label because
#  the site has four).  Only the detector half runs here -- the witness half needs a pre-fix
#  binary, which a gate cannot build.
LUNALOG=$LOGDIR/luna_intmask.log
python3 luna_intmask_probe.py "$PMAX" "$IMAGES" > "$LUNALOG" 2>&1 || true
grep -E "^  (C[0-9]|D[0-9]|E[0-9])" "$LUNALOG" | sed 's/^/       /'

if ! grep -q "LUNA_INTMASK_WITNESS=" "$LUNALOG"; then
    note "luna88k INT_ST_MASK probe produced no verdict; last lines follow"
    tail -5 "$LUNALOG" | sed 's/^/       /'
    check "luna88k INT_ST_MASK probe completed" "no" "yes"
else
    #  THE CONTROLS FIRST AND SEPARATELY.  C2 is the device-signature control: 0xfc000000
    #  reads back 0x00fc0000 because the handler shifts by 8, and RAM cannot produce that.
    #  A liveness row alone cannot substitute -- the footbridge probe's first draft returned
    #  0x0 everywhere WITH ITS RAM CONTROL GREEN, which is why the ladder demands two.
    check "luna88k intmask: device-signature control (the handler's own >>8)" \
          "$(grep -c 'C2 read INT_ST_MASK0 after legal write' "$LUNALOG")" "1"
    check "luna88k intmask: post-fix verdict" \
          "$(grep -c 'LUNA_INTMASK_WITNESS=PASS' "$LUNALOG")" "1"
    #  Named individually so deleting any one is visible rather than silent.  D2 is the row
    #  that kills latch-once-then-exit-on-the-next; D4 uses the SECOND case label, because a
    #  fix applied to cpunr 0 alone passes without it.
    check "luna88k intmask: the second-write row is present (kills latch-then-exit)" \
          "$(grep -c 'D2 readback' "$LUNALOG")" "1"
    check "luna88k intmask: the second case label is exercised" \
          "$(grep -c 'D4 readback from INT_ST_MASK1' "$LUNALOG")" "1"
    check "luna88k intmask: row failures" \
          "$(grep -cE '^  (C|D|E)[0-9].* (FAIL|MISMATCH)' "$LUNALOG")" "0"
fi

gate_end
