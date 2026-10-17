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
# [#556, 2026-10-02 -- a records correction; the text above is kept as it was written] fadd toward
# +Inf/+Inf-opposite at m88k_rounding_probe.py:68-69 and flt toward +Inf at :96 also fail a missing 2-for-3 swap.
# (regress21:F9: regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md)
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
# [#556, 2026-10-02 -- a records correction; the text above is kept as it was written] Seven truncation rows (three
# SS and four SD). 25+7+8+6=46.  (regress21:F10:
# regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md)
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

#  ---------------------------------------------------------------------------
#  m88kexcdeliver (2026-09-05): the exception-DELIVERY detector, wired here for the same
#  reason as the #438 probe above -- this gate already owns the m88k binary.  The probe is
#  BOTH a rung-3 WITNESS (0/9 -> 0/10 -> 3/22 -> 2/23 -> 2/29 -> 3/30 -> 3/35 -> 4/36 -> 7/41 -> 7/46 (probe_v14_head.out) on HEAD 83df95c as the instrument
#  grew: every trap-like class stopped the machine.  With the final instrument the 7 are resid50, resid127,
#  resid11, resid50ind, resid50c and usfu1, whose CORRECT answer is HALT, and the pre-existing user vector 128 (usertb); sfu1h reads STOP
#  on HEAD because the FIRST divu halts on vector 0x008, not its own 0x072 -- probe10_head.out /
#  probe_v3_head.out .. probe_v11_head.out) and the DETECTOR (84 fault rows -- 59 until v22, 63 in v22, 73 in v23, 2026-10-16 -- + 2
#  controls; kill tables killtable/, killtable2/, killtable3/, killtable4/ + killtable4b/
#  (M_TAILRETURN), killtable5/ (the {class} x {MODE} and {SFRZ set, non-trap} x {class} closures), killtable6/ (the fallback far bound, resid127), killtable7/ (the frozen-TRAP rows per class), killtable8/ (the fallback in user mode, usfu1), killtable10/ (the frozen ERROR trap, the near bound, the fallback PSR-bit cells, the frozen user trap, the refatal channel; table 9 was folded into it), killtable11/ (the frozen traps naming the 0x1c2, MVMEPROM and 511 labels; the ERROR-arm-frozen and MISALIGNED-C representatives; the re-route x {IND, C} cells, errind/errc), killtable12/ (the re-route TRAP side x {IND, C}: both swept 46/46 before the rows existed), killtable13/ (the six previously-sweeping mutants, all killed), killtable14/ (grok's three predicted SER sweeps -- each 54/54 on the frozen v16 instrument and killed on v17 by its own row)
#  under regress/artifacts/m88kexcdeliver/).  Only the detector half runs here.
#
#  The pins are NAMED so that deleting a row is visible: `M88KEXC_RESULT=84/84' pins the
#  denominator (a row that stops running shrinks it); resid50 and sfu1h are the two rows
#  whose CORRECT answer is HALT -- they separate the shipped fix from a form that delivers
#  every vector (the rejected D4) or SFU1 (row m88kexcsfu1); vbrtb is the one ANCHORED row
#  (VBR relocated to 0x2000: it alone reds if the vector base stops being read).
#  [#556, 2026-10-02 -- a records correction; the text above is kept as it was written] Eight expected-HALT rows:
#  resid50, resid127, resid11, resid50ind, resid50c, resid50ser, sfu1h, usfu1.  (regress21:F11:
#  regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md)
EXCLOG=$LOGDIR/m88k_exc.log
python3 m88k_exc_probe.py "$PMAX" > "$EXCLOG" 2>&1 || true
grep -E "^M88KEXC_(ROW|RESULT|SELFTEST|CONTROLS)" "$EXCLOG" | cut -c1-110 | sed 's/^/       /'

if ! grep -q "M88KEXC_DONE" "$EXCLOG"; then
    note "m88k exception-delivery probe produced no completion sentinel; last lines follow"
    tail -5 "$EXCLOG" | sed 's/^/       /'
    check "m88k exc: probe completed" "no" "yes"
else
    check "m88k exc: CR parse self-test (PSR at reset == 0x80000002)" \
          "$(grep -c 'M88KEXC_SELFTEST=OK' "$EXCLOG")" "1"
    check "m88k exc: 84 fault rows, all as expected (the denominator is the pin)" \
          "$(grep -c 'M88KEXC_RESULT=84/84' "$EXCLOG")" "1"
    #  v22, repair 13 (2026-10-16): {class} x {delay slot}.  Before it only DIV0 faulted in a delay slot, and the
    #  form implemented = !cpu->delay_slot at MISALIGNED/UNIMPL/PRIV/OVF swept the 59-row probe clean at all four arms
    #  (artifacts/m88kexcdeliver/delayslot_20261016/).  BOUNDS and ERROR in a slot need a trap instruction there,
    #  which the manual does not settle -- disclosed in the probe's contract (repair13_20261016/, table 16).
    #  v23, repair 14: the delay-slot GRID, {7 labels} x {SFRZ} x {delay_slot} (table 19).  Unfrozen, all seven labels:
    check "m88k exc: a fault or a TRAP in a delay slot is delivered at all seven labels (the seven dslot<L> fault rows and, v24, the five dslot<L>tb trap rows)" \
          "$(grep -cE '^M88KEXC_ROW=(dslot +RESULT=DELIVER +pc=0x00000040|dslotmisalign +RESULT=DELIVER +pc=0x00000020|dslotunimpl +RESULT=DELIVER +pc=0x00000028|dslotpriv +RESULT=DELIVER +pc=0x00000030|dslotovf +RESULT=DELIVER +pc=0x00000048|dslotbounds +RESULT=DELIVER +pc=0x00000038|dsloterror +RESULT=DELIVER +pc=0x00000050|dslotmisaligntb +RESULT=DELIVER +pc=0x00000020|dslotunimpltb +RESULT=DELIVER +pc=0x00000028|dslotprivtb +RESULT=DELIVER +pc=0x00000030|dslotdiv0tb +RESULT=DELIVER +pc=0x00000040|dslotovftb +RESULT=DELIVER +pc=0x00000048) ' "$EXCLOG")" "12"
    #  ... and FROZEN, all seven labels, plus the fallback row:
    check "m88k exc: with SFRZ set, a slot fault is still re-routed (errdslot* at 0x50) and a slot trap still exempt at all seven labels (trapfrozen<L>dslot); SFU1 in a slot still halts, frozen or not (usfu1dslot, sfu1hdslot)" \
          "$(grep -cE '^M88KEXC_ROW=(errdslot(misalign|ovf|div0|priv|unimpl) +RESULT=DELIVER +pc=0x00000050|trapfrozen7dslot +RESULT=DELIVER +pc=0x00000038|trapfrozen10dslot +RESULT=DELIVER +pc=0x00000050|usfu1dslot +RESULT=HALT|trapfrozen4dslot +RESULT=DELIVER +pc=0x00000020|trapfrozen5dslot +RESULT=DELIVER +pc=0x00000028|trapfrozen6dslot +RESULT=DELIVER +pc=0x00000030|trapfrozen8dslot +RESULT=DELIVER +pc=0x00000040|trapfrozen9dslot +RESULT=DELIVER +pc=0x00000048|sfu1hdslot +RESULT=HALT) ' "$EXCLOG")" "14"
    check "m88k exc: IND set by the exception path from a pre-fault PSR with IND clear (indclr)" \
          "$(grep -cE '^M88KEXC_ROW=indclr +RESULT=DELIVER .*psr=0x8000000b .*epsr=0x80000000' "$EXCLOG")" "1"
    check "m88k exc: user-mode MISALIGNED and OVERFLOW deliver (umisalign 0x20, uovf 0x48 -- the {class} x {MODE} closure)" \
          "$(grep -cE '^M88KEXC_ROW=(umisalign +RESULT=DELIVER +pc=0x00000020|uovf +RESULT=DELIVER +pc=0x00000048) .*psr=0x8000000b .*epsr=0x00000002' "$EXCLOG")" "2"
    check "m88k exc: a frozen handler's non-trap fault of every class re-routes to ERROR (errovf errdiv0 errpriv errunimpl at 0x50)" \
          "$(grep -cE '^M88KEXC_ROW=err(ovf|div0|priv|unimpl|ind|c|ser) +RESULT=DELIVER +pc=0x00000050' "$EXCLOG")" "7"
    check "m88k exc: the two liveness/attribution controls computed their quotients" \
          "$(grep -cE '^M88KEXC_ROW=(live|attrib) +RESULT=DONE' "$EXCLOG")" "2"
    check "m88k exc: a residual vector (50) still HALTS at the fallback (negative control vs D4)" \
          "$(grep -cE '^M88KEXC_ROW=resid50 +RESULT=HALT' "$EXCLOG")" "1"
    check "m88k exc: resid127 (tb1 naming 127, the fallback window's FAR bound) still HALTs -- a shrunk bound delivers it instead" \
          "$(grep -cE '^M88KEXC_ROW=resid127 +RESULT=HALT' "$EXCLOG")" "1"
    check "m88k exc: a user-mode SFU1 still reaches the fallback (usfu1 HALT naming 0x072 -- the fallback predicate in user mode)" \
          "$(grep -cE '^M88KEXC_ROW=usfu1 +RESULT=HALT' "$EXCLOG")" "1"
    check "m88k exc: a frozen TRAP naming any class is delivered to its OWN vector, shadows frozen: every switch-1 label a trap can name -- and, since v16, with the TRAP side of the re-route varied by PSR bit as well (ind, c, ser), because eleven labels in ONE status state cover eleven labels and not the axis" \
          "$(grep -cE '^M88KEXC_ROW=trapfrozen(4|5|6|8|9|10|128|450|496|511|ind|c|ser|user|sfd1)? +RESULT=DELIVER ' "$EXCLOG")" "16"
    check "m88k exc: the {switch-1 arm} x {C, IND, SER} closure -- SIX unfrozen traps with C and SER set and IND clear are DELIVERED, not swept.  v16 rowed C/IND at five arms and closed SER at ONE (grok, pass 9: an axis claimed from a single cell); v17 ORs SER into the value those five share and adds ovftbser for the sixth arm" \
          "$(grep -cE '^M88KEXC_ROW=(unimpltbc|privtbc|boundstbc|div0tbc|errortbc|ovftbser) +RESULT=DELIVER +pc=0x000000(28|30|38|40|48|50) ' "$EXCLOG")" "6"
    check "m88k exc: and each of those six keeps BOTH the carry and the serial-mode bit through exception entry (psr=0xb000000b) -- the pin that reds if PSR_SUPCNOIND ever loses SER again" \
          "$(grep -cE '^M88KEXC_ROW=(unimpltbc|privtbc|boundstbc|div0tbc|errortbc|ovftbser) .*psr=0xb000000b ' "$EXCLOG")" "6"
    check "m88k exc: the SER axis at its two NON-arm sites -- the fallback predicate (resid50ser HALT) and the non-trap re-route (errser at 0x50).  Each swept the whole v16 instrument 54/54 before its row existed (killtable14/)" \
          "$(grep -cE '^M88KEXC_ROW=(resid50ser +RESULT=HALT|errser +RESULT=DELIVER +pc=0x00000050)' "$EXCLOG")" "2"
    check "m88k exc: the fallback window's NEAR bound and its PSR-bit cells still HALT (resid11; resid50 with IND clear; with C set; with SER set -- SIX settable bits vary at the fallback, and resid50ser is what made that claim true)" \
          "$(grep -cE '^M88KEXC_ROW=(resid11|resid50ind|resid50c|resid50ser) +RESULT=HALT' "$EXCLOG")" "4"
    check "m88k exc: no row carried the re-route's diagnostic where the trap exemption should hold, or lacked it where the re-route fired (bad=refatal)" \
          "$(grep -c 'bad=.*refatal' "$EXCLOG")" "0"
    check "m88k exc: SFU1 inside a handler still HALTS (the m88kexcsfu1 boundary)" \
          "$(grep -cE '^M88KEXC_ROW=sfu1h +RESULT=HALT' "$EXCLOG")" "1"
    check "m88k exc: the anchored row (VBR relocated) delivered at 0x2038" \
          "$(grep -cE '^M88KEXC_ROW=vbrtb +RESULT=DELIVER +pc=0x00002038' "$EXCLOG")" "1"
    check "m88k exc: a trap while frozen delivers to its own vector, not ERROR" \
          "$(grep -cE '^M88KEXC_ROW=trapfrozen +RESULT=DELIVER +pc=0x00000038' "$EXCLOG")" "1"
    check "m88k exc: carry survives the exception path (PSR 0x9000000b)" \
          "$(grep -cE '^M88KEXC_ROW=ovfc +RESULT=DELIVER .*psr=0x9000000b' "$EXCLOG")" "1"
    check "m88k exc: no row carried the pre-fix ERROR-level line (bad=level)" \
          "$(grep -c 'bad=.*level' "$EXCLOG")" "0"
fi

#  ---- #503 lunaabsentcpu: the LUNA-88K interrupt controller's per-CPU walk.
#
#  reassert_interrupts() walked all MAX_CPUS and called the NULL interrupt_assert of a slot DEVINIT never
#  connected, so on the DEFAULT one-cpu machine a guest store to an interrupt mask followed by a store to a
#  soft-interrupt register followed a null function pointer and ended the process.  This probe is BOTH the
#  rung-3 WITNESS (it shows the symptom on the pre-fix build and goes green after, same script) and the
#  DETECTOR.  Kill tables under regress/artifacts/lunaabsentcpu/: killtable/ .. killtable5/, the last on
#  this 37-row instrument -- BASE 37/37, all twenty-six distinct mutants killed, and M_NULLAB EQUIVALENT
#  (the empty-name stub path it edits is dead code, warrant recorded with the row).
#
#  THE PINS ARE STRUCTURAL ON PURPOSE.  The 37 rows reuse names across sessions -- `slot0' three times,
#  `cpu1' four -- so a per-name `grep -c' would count a population nobody intended.  The denominator, the
#  witness verdict and the two mandated controls are each unambiguous, and the denominator is what reds if
#  a row stops running.
LUNALOG=$LOGDIR/luna_absentcpu.log
python3 luna_absentcpu_probe.py "$PMAX" "$IMAGES" > "$LUNALOG" 2>&1 || true
grep -E "^(LUNAABS_|LUNA_ABSENTCPU_)" "$LUNALOG" | cut -c1-110 | sed 's/^/       /'

if ! grep -q "LUNAABS_DONE" "$LUNALOG"; then
    note "luna88k absent-cpu probe produced no completion sentinel; last lines follow"
    tail -5 "$LUNALOG" | sed 's/^/       /'
    check "luna absentcpu: probe completed" "no" "yes"
else
    check "luna absentcpu: 37 rows, all OK (the denominator is the pin -- a row that stops running shrinks it)" \
          "$(grep -c 'LUNAABS_RESULT=37/37' "$LUNALOG")" "1"
    check "luna absentcpu: the rung-3 witness verdict is PASS (PRE_FIX_SYMPTOM means the fix is gone; FAIL means a row broke)" \
          "$(grep -c '^LUNA_ABSENTCPU_WITNESS=PASS' "$LUNALOG")" "1"
    check "luna absentcpu: both mandated controls green -- liveness (a known value returns through the same decode) and device signature (the value could only have come from this device)" \
          "$(grep -cE '^LUNAABS_ROW=(live|devsig) +RESULT=OK' "$LUNALOG")" "2"
    check "luna absentcpu: no row reported a halted machine (the pre-fix symptom is the process ending mid-row)" \
          "$(grep -cE '^LUNAABS_ROW=[^ ]+ +RESULT=(HALT|NOSTART)' "$LUNALOG")" "0"
fi

gate_end
