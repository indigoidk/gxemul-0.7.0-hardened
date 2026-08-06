#!/bin/bash
# GATE 14 -- ARM subtract-family carry flags (#311) and undefined routing (#312).
#
# What this protects
# -----------------
# #311: the subtract family computed its carry-out as `a >= b`. That is
# NOT-BORROW for SUB/CMP/RSB, which have no borrow-in, and WRONG for SBC/RSC,
# whose result is `a - b - NOT(C)`. The two disagree exactly when `a == b` with
# carry-in clear: `a - a - 1` borrows, so carry must be CLEAR, and `a >= b`
# reported it SET. The fix takes the flag from the full 64-bit result the file
# already computes (`c32 == c64`), which is the same answer as `a >= b` for the
# three instructions that were already right.
#
# #312: ARM's permanently-undefined encodings reached `goto bad`, which sets
# cpu->running = 0 (cpu_dyntrans.c) -- a legal-to-attempt instruction stopping
# the whole emulator, the same halt class as #264/#309/#310. They now raise the
# Undefined Instruction exception the silicon raises.
#
# This gate is known to be able to FAIL
# ------------------------------------
# It was run against the committed pre-fix build and scored 39 of the 56 rows it
# had at that moment, failing in exactly the 17 places the three fixes were
# predicted to flip and nowhere else. The two `subs rn=pc` pins were added after
# that sweep and pass either way, so the same build on today's table would read
# 41/58 -- stated exactly rather than restated as 39/58, because the count is
# evidence and evidence does not get rounded to the number that sounds better.
# That measurement is what shows these rows discriminate; gate 3's mutant
# machinery does not reach here, because it operates on float_emul.c and this
# gate measures the real emulator instead of a pure function.
#
# Swept again for #346 against a binary built from the parent commit: 162 of
# 165, failing the three cache-clean rows the fix flips and nowhere else. The
# two cache-clean CONTROL rows pass on both builds, which is what they are for.
#
# Why most of this gate is PINs
# ----------------------------
# #311 rewrites ONE line that five instructions share, and two of them were
# already correct. The pins are the point: they assert that SUB, RSB and CMP --
# and the ADD/ADC arm of the same #if, which keeps its own `c32 != c64` test --
# were not disturbed. A gate for this fix that checked only SBC and RSC would
# not detect the regression that matters most.
#
# The decode-time row
# ------------------
# `udf cond-failed nop` is the strongest reachability statement here: a
# conditional UDF whose condition is FALSE also stopped the committed
# emulator, because `goto bad` fires during DECODE, before any condition is
# evaluated. The guest never had to execute the instruction at all. That row
# asserts execution continued AND no exception was raised as a SINGLE value,
# because checking "no exception" alone would score a point on a build that
# halted before reaching anything.
set -u
cd "$(dirname "$0")"
. ./lib.sh

gate_begin "gate 14: ARM/Thumb flags (#311/#312/#319-#322/#328/#329)"

PMAX=${PMAX:-$ROOT/build/gxemul}
LOG=$LOGDIR/gate_arm.log
STUB=$LOGDIR/arm_stub.bin

need_exec "$PMAX"
command -v python3 >/dev/null || gate_skip "python3 not available"

# `testarm` prints usage and exits without a file argument, so a four-byte raw
# stub is loaded purely to make the machine construct. Every row overwrites it
# before anything executes; it is scaffolding, not code under test.
python3 -c "
import struct, sys
open(sys.argv[1], 'wb').write(struct.pack('<I', 0xe1a00000))
" "$STUB" || gate_skip "could not write the load stub"

note "binary : $PMAX"
note "machine: testarm/SA1110, cold debugger, RAM at 0"
note "little-endian; every word read is byte-swapped back by the probe"
note "flags read by the guest's own mrs r3,cpsr -- not a debugger register print"

python3 arm_flags_probe.py "$PMAX" "$STUB" > "$LOG" 2>&1 || true

if ! grep -q "ARM_FLAGS_RESULT=" "$LOG"; then
    note "probe produced no result line; last lines follow"
    tail -5 "$LOG" | sed 's/^/       /'
    gate_skip "probe did not complete"
fi

grep -E " ok$| FAIL$" "$LOG" | sed 's/^/       /'

# A probe whose control row failed has measured NOTHING and no other row may be
# believed. This harness has been bitten by a probe that reported a defect off
# sentinel reads while its guest code had never run.
ctrl=$(grep -o "ARM_FLAGS_CONTROL=[A-Z]*" "$LOG" | tail -1 | cut -d= -f2)
check "control row proves the probe measures" "${ctrl:-missing}" "OK"

res=$(grep -o "ARM_FLAGS_RESULT=[0-9]*/[0-9]*" "$LOG" | tail -1 | cut -d= -f2)
got=${res%/*}; want=${res#*/}
check "rows run"     "$want" 165
check "rows correct" "$got"  "$want"

# Both classes must stay populated: a gate that is all pins cannot detect a
# reverted fix, and one with no pins cannot detect collateral damage.
disc=$(grep -c " DISC " "$LOG")
pins=$(grep -c " PIN " "$LOG")
check_min "discriminating rows present" "$disc" 44
check_min "pinned rows present"         "$pins" 55

# Named rows, one contract each, so a single site reverting cannot hide behind
# a total. Two spaces after the name: the probe pads names to a fixed column,
# and a name that is a PREFIX of another would otherwise match both rows (the
# trap that made three of gate 13's checks count the wrong rows).
#
# The SBC/RSC discriminators -- three different equal-operand values, because a
# fix that special-cased one constant would pass a single row.
# #340: the combiner rows. The two "combined" rows carry the defect; the two
# "standalone" rows are the control that attributes it to the COMBINER rather
# than to the instruction -- same encoding, same operands, no following branch;
# and "flat C preserved" catches a fix that starts clobbering C on an
# unrotated immediate, where the ISA preserves it. Named individually so one
# reverting site cannot hide behind the total.
for v in "A teq rot C combined" "A tst rot C combined" \
         "A teq rot C standalone" "A tst rot C standalone" \
         "A teq flat C preserved"; do
    n=$(count "$LOG" "^$v  .*ok$")
    check "  row: $v" "$n" 1
done

# #342: the XOR-swap fold. The DISC row is its own proof that the fold
# happened -- three standalone `eor rX,rX,rX` cannot leave a nonzero value, so
# only X(xchg) could have produced the 0x5a the committed build returned.
#
# The swap rows are PINs in the shape the matcher actually accepts, Rm == Rd
# (`eor X,Y,X`). The first version of them used Rn == Rd and so never matched
# the combiner at all -- it was measuring three standalone EORs while claiming
# to exercise the fold, which a review seat caught. They now run the FOLDED
# handler on pass 2 and pin that its swap is correct, so a broken X(xchg) fails
# here; they still cannot distinguish folded-and-correct from
# not-folded-and-correct, which is why they are pins and not discriminators.
for v in "A xchg same-reg zeroes" "A xchg same-reg r1 pin" \
         "A xchg swap r0" "A xchg swap r1"; do
    n=$(count "$LOG" "^$v  .*ok$")
    check "  row: $v" "$n" 1
done

# #345/#346: the cache-clean fold. Four loops, each one field off the genuine
# `ldr r2,[r0],#32 / subs r1,r1,#0x20 / bne / mcr`, so no row can be satisfied
# by the wrong guard.
#
#   r0/r1 intact  -- #345: base r5, counter r6. Its stride is 32 deliberately,
#       so that #346's immediate check cannot block this fold and stand in for
#       the register check the row exists to protect.
#   imm4 r0/r2    -- #346: `ldr r2,[r0],#4` folded anyway and advanced r0 by 32,
#       reading 0x9120 where the architecture returns 0x9104. r2 is the second
#       half of that: the skipped load left it at its 0x77 seed.
#   wrong Rd      -- `ldr r6,[r0],#32` folded and stranded r6 at 0x66.
#
# The two control rows are what stop an over-tight guard from disabling the
# optimisation unnoticed -- no discriminator above can see that, since they all
# pass when nothing ever folds. "fold r0" pins the closed form's arithmetic;
# "still folds" is the only value that PROVES the fold fired for the genuine
# sequence, because r0 is 0x9120 whether it folds or not. It asserts a stale r2,
# which is a defect #346 does not fix -- when that is fixed its want becomes
# 0xa5a5a5a5 and it keeps working as the fold detector.
for v in "A cacheclean r0 intact" "A cacheclean r1 intact" \
         "A cacheclean still folds" "A cacheclean fold r0" \
         "A cacheclean imm4 r0" "A cacheclean imm4 r2" \
         "A cacheclean wrong Rd"; do
    n=$(count "$LOG" "^$v  .*ok$")
    check "  row: $v" "$n" 1
done

for v in "sbcs eq C=0 C" "sbcs eq0 C=0 C" "sbcs eqmax C=0 C" "rscs eq C=0 C"; do
    n=$(count "$LOG" "^$v  .*ok$")
    check "  disc: $v" "$n" 1
done

# The value rows on those same four: the arithmetic was ALWAYS right, and a
# "fix" that repaired the flag by breaking the result must not pass.
for v in "sbcs eq C=0 rd" "sbcs eq0 C=0 rd" "sbcs eqmax C=0 rd" "rscs eq C=0 rd"; do
    n=$(count "$LOG" "^$v  .*ok$")
    check "  value intact: $v" "$n" 1
done

# The instructions the fix must NOT disturb.
for v in "subs eq C" "subs lt C" "subs gt C" "subs zerominus C" \
         "rsbs gt C" "rsbs lt C" \
         "cmp eq NZCV" "cmp lt NZCV" "cmp gt NZCV" \
         "subs rn=pc rd" "subs rn=pc C" \
         "adds carry-out C" "adds no-carry C" \
         "adcs carry-out C" "adcs no-carry C" \
         "sbcs eq C=1 C" "sbcs gt C=0 C" "sbcs lt C=0 C" "sbcs lt C=1 C" \
         "rscs gt C=0 C" "rscs lt C=0 C"; do
    n=$(count "$LOG" "^$v  .*ok$")
    check "  pin: $v" "$n" 1
done

# #313: ADC was the ONE opcode listed in the outer V-update #if that matched
# neither inner formula, so ADCS could only ever clear V. The paired adds rows
# are what make these a statement about ADC rather than about V generally --
# the identical overflow through ADDS was already correct.
for v in "adcs V pos-ovf" "adcs V pos-ovf2" "adcs V neg-ovf"; do
    n=$(count "$LOG" "^$v  .*ok$")
    check "  disc: $v" "$n" 1
done
for v in "adcs V none" "adds V pos-ovf" "adds V none" "sbcs V ovf"; do
    n=$(count "$LOG" "^$v  .*ok$")
    check "  pin: $v" "$n" 1
done

# #312's rows. The handler-ran row is the witness that the exception was
# actually TAKEN; mode and lr prove it was entered as an exception rather than
# branched into.
#
# The page-end row is not redundant with the first: X(und) reconstructs the
# faulting PC with a hard-coded 4KB mask, and at page offset 0 both halves of
# that arithmetic are zero, so only a row at the last slot of a page can catch
# a wrong mask.
for v in "udf handler ran" "udf UND32 mode" "udf lr=pc+4" \
         "udf gdb-form handler ran" "udf gdb-form UND32 mode" \
         "udf gdb-form lr=pc+4" \
         "udf page-end handler ran" "udf page-end UND32 mode" \
         "udf page-end lr=pc+4" "udf cond-failed nop"; do
    n=$(count "$LOG" "^$v  .*ok$")
    check "  undefined: $v" "$n" 1
done

# ---- #319/#320/#321: rotations the decoder rejected, and MVNS's carry -------
# Every row asserts a VALUE. `uxtah ROR 24` is the discriminating one of the
# first group: a byte extract is the same under a rotate as under a shift at
# every encodable amount, so the uxtab rows cannot tell those apart, while the
# halfword form at 24 wraps rm's low byte into bits 15:8.
#
# `rotc zero C` is the row that never halted -- the old guard exempted an imm8
# of zero, so that case shipped with the wrong carry rather than stopping, which
# is why this group is a wrong-answer fix and not only a halt fix.
#
# All four MVNS bands are present because two of them would pass by coincidence:
# the decoder rewrites `mvn #imm` to `mov #~imm`, and with S set the carry was
# then read off the COMPLEMENT.
for v in "uxtab ROR 8" "uxtab ROR 16" "uxtab ROR 24" \
         "uxtah ROR 8" "uxtah ROR 16" "uxtah ROR 24" \
         "rotc movs val" "rotc movs C" "rotc zero C" "rotc ands C" \
         "rotc orrs val" "rotc bics val" "rotc tst C" \
         "mvns rot0 C=0" "mvns rot0 C=1" "mvns b31=0 C" "mvns b31=1 C" \
         "mvns value"; do
    n=$(count "$LOG" "^$v  .*ok$")
    check "  round 78: $v" "$n" 1
done
for v in "rotc pc src C"; do
    n=$(count "$LOG" "^$v  .*ok$")
    check "  round 78: $v" "$n" 1
done
for v in "uxtab ROR 0" "rot0 movs C" "mvn S-clear" "rot0 pc src C" \
         "rotc pc gt255" "rotc bound 256"; do
    n=$(count "$LOG" "^$v  .*ok$")
    check "  round 78 pin: $v" "$n" 1
done

# #328: the THUMB rows. Everything above is ARM-mode; the Thumb interpreter is a
# separate implementation that #311 never touched, and it had THREE flag defects in
# four near-identical blocks -- Z read off a 64-bit value, C derived from the carry
# out of a negation (so subtracting zero reported a borrow), and V read from the sign
# of the negated subtrahend (which breaks at 0x80000000, the one value that is its
# own negation). Each row asserts the flags AND rd, because the value was already
# right and a flags-only row could not tell a fixed flag from a broken result.
for v in "T ctrl ADDS 2+3" "T ctrl SUBS 5-3" "T ctrl SUBS borrow"          "T Z subs equal" "T Z cmp imm equal" "T Z subs imm equal"          "T Z cmp reg equal" "T Z adds wrap"          "T C subs zero" "T C cmp imm 0" "T C subs imm 0" "T C cmp reg zero"          "T V 0-INT_MIN" "T V -1-INT_MIN" "T V INT_MIN-same"          "T alias subs rd==rm" \
         "T Z adds imm8 wrap" "T Z adds imm3 wrap" "T C subs imm3 zero" \
         "T V subs INT_MIN" "T V adds overflow" "T C subs 0-0" \
         "T V adds INT_MIN x2"; do
    n=$(count "$LOG" "^$v  .*ok$")
    check "  thumb: $v" "$n" 1
    n=$(count "$LOG" "^$v rd  .*ok$")
    check "  thumb: $v rd" "$n" 1
done


# #329: the Thumb SHIFT rows. ASR-immediate took Z and N from a register chosen by the
# shift amount; RORS never cleared Z/N; and LSR #0 / ASR #0 encode shift-by-32 rather
# than shift-by-zero. The two LSL #0 rows are the control -- that encoding IS a genuine
# no-op and its C must survive untouched, which is why they run at both carry-in values.
# The positive-operand shift-32 rows only became measurable once the rig could preset
# carry: against a build that never writes C they would pass on a cold machine anyway.
for v in "T LSL #0 keeps C1" "T LSL #0 keeps C0" "T ASR #12 flags reg"          "T RORS clears Z" "T RORS clears N"          "T LSR #0 neg" "T LSR #0 pos" "T ASR #0 neg" "T ASR #0 pos"          "T LSR rd!=0"; do
    n=$(count "$LOG" "^$v  .*ok$")
    check "  shift: $v" "$n" 1
    n=$(count "$LOG" "^$v rd  .*ok$")
    check "  shift: $v rd" "$n" 1
done

gate_end
