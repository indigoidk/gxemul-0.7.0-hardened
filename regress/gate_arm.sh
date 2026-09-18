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
# And again for #347 against a binary built from ITS parent (be6ea08): 168 of
# 173, failing exactly the five `A cclean2 ... ` discriminators and nowhere
# else. All three of that round's control/anti-clobber pins pass on both builds.
#
# And for round 99 (#348/#349/#350) against a binary built from the pre-fix
# HEAD (dea2fef): 181 of 190, failing exactly the NINE new DISC rows -- the
# two flags rows, the tail/zero/tail-V flag rows, the two fires rows,
# `A cacheclean nonmult` reading "fold", and `A cacheclean zero n` reading
# "none" -- and nowhere else. On the fixed build: 190/190. The retired
# `A cclean2 still fold` control asserted the MISSING flags and was replaced
# in the same change by the #349 marker rows, exactly as its own comment
# required. The nonmult witness's first draft is itself a recorded lesson:
# it expected a data abort at the top of RAM (measured false -- non-existent
# reads log and continue) and compared a dump string unswapped, so it read
# its own sentinel's parity; see run_cc_nonmult's docstring. Its "live"
# verdict was then tightened in review to also demand load progress (r0
# moved off 0x9120), closing a false pass against a guard that returns
# without calling the load.
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
check "rows run"     "$want" 190
check "rows correct" "$got"  "$want"

# Both classes must stay populated: a gate that is all pins cannot detect a
# reverted fix, and one with no pins cannot detect collateral damage. The
# floors track the deltas each round adds; a review seat noted they are far
# below the actuals (112/78 after round 99) and so guard only against mass
# reclassification, with `rows run` guarding deletion.
disc=$(grep -c " DISC " "$LOG")
pins=$(grep -c " PIN " "$LOG")
check_min "discriminating rows present" "$disc" 58
check_min "pinned rows present"         "$pins" 66

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

# #345/#346/#348/#349/#350: the first cache-clean fold. Matcher probes, each
# one field off the genuine `ldr r2,[r0],#32 / subs r1,r1,#0x20 / bne / mcr`,
# so no row can be satisfied by the wrong guard:
#
#   r0/r1 intact  -- #345: base r5, counter r6. Its stride is 32 deliberately,
#       so that #346's immediate check cannot block this fold and stand in for
#       the register check the row exists to protect.
#   imm4 r0/r2    -- #346: `ldr r2,[r0],#4` folded anyway and advanced r0 by 32,
#       reading 0x9120 where the architecture returns 0x9104. r2 is the second
#       half of that: the skipped load left it at its 0x77 seed.
#   wrong Rd      -- `ldr r6,[r0],#32` folded and stranded r6 at 0x66.
#
# "fold r0" pins the closed form's arithmetic; "still folds" asserts the stale
# r2, a defect deliberately unfixed (OUTSTANDING_BUGS), which makes it a fold
# detector independent of #349's marker. The #348 rows ride a 0x40 counter --
# at 0x20, a fix that skipped the r1 preload would be invisible:
#
#   flags         -- #348: seeded N|V (cmp r9,#0x80000000), the loop's zero
#       exit owes Z|C = 0x6; the committed pre-fix build read the seed back.
#   fold r1       -- the genuine counter result, 0, unasserted before round 99.
#   nonmult       -- #350: a 0x21 counter re-entering the installed fold. The
#       unguarded fold consumed it (r0 went odd: += 0x21); the guard falls
#       back to the real loop, which never exits, and the session is forced
#       back with ^C. The verdict is read from the registers: "fold" on an
#       unaided exit with r0 odd, "live" only with the residue invariant
#       AND r0 advanced off its phase-A value (load progress).
#   quiet/fires   -- #349: the fold-fired marker, absent at default verbosity,
#       present under `verbosity cpu 3` on the genuine loop only. The fires
#       row is the channel's own positive control; ctrl proves selectivity.
#   zero n        -- #350's r1 == 0 arm: the honest iteration count (2^27) is
#       unassertable by any register or flag, so it is read off the marker
#       text itself. A formula reverted to `r1 >> 5` prints 0 and fails.
for v in "A cacheclean r0 intact" "A cacheclean r1 intact" \
         "A cacheclean still folds" "A cacheclean fold r0" \
         "A cacheclean imm4 r0" "A cacheclean imm4 r2" \
         "A cacheclean wrong Rd" "A cacheclean flags" \
         "A cacheclean fold r1" "A cacheclean nonmult" \
         "A cacheclean quiet" "A cacheclean fires" \
         "A cacheclean fires ctrl" "A cacheclean zero n"; do
    n=$(count "$LOG" "^$v  .*ok$")
    check "  row: $v" "$n" 1
done

# #347/#348/#349: the SECOND cache-clean fold, which had BOTH halves of the
# #347 defect -- `add rX,rX,#32 / subs rY,rY,#32` accepted for any X and Y,
# and a handler that wrote no guest register at all -- and then the flags
# defect #348 closed. Loops one field off the genuine
# `mcr / mcr / add r0,r0,#32 / subs r1,r1,#32 / bhi`, plus counters for both
# exits of the loop:
#
#   fold r0/r1    -- the genuine sequence. The committed #346-era handler
#       returned r0 = 0x9100 and r1 = 0x40 for a loop that owes 0x9140 and 0.
#   flags         -- #348: seeded N|V, the 0x40 counter's zero exit owes
#       Z|C = 0x6. The pre-fix build read the seed back.
#   base r5/r1    -- `add r5,r5,#32`: the fold fired anyway and stranded r5 at
#       0x9100 and r1 at 0x40.
#   cnt r6        -- `subs r6,r6,#32`: fired anyway, r6 left at 0x40.
#   base r0 / cnt r1 -- the anti-clobber pins. They pass on the pre-fix build
#       too, on purpose: they exist to catch the OPPOSITE error, a handler that
#       now writes r[0]/r[1] by name behind a matcher that still takes any
#       register. Without them the register guard could be dropped and only the
#       rows above, which already pass, would notice.
#   tail flags/r0/r1 -- the 0x30 counter exits on the subs BORROWING and owes
#       N alone (0x8); the registers pin #347's closed form on the borrow
#       path, which no earlier row covered. "tail V" repeats the run seeded
#       V=1: V must come back 0 on the borrow exit too (it is structurally 0
#       -- the final operand lies in [0, 0x20] for every uint32 counter).
#   zero flags/r0/r1 -- counter 0, the one input where #347's `(r1 == 0 ||`
#       disjunct is load-bearing: owes r0 += 0x20, r1 = 0xffffffe0, flags 0x8.
#   quiet/fires   -- #349: the marker channel. The old `still fold` control
#       asserted the MISSING flags (seeded N surviving) and was retired in the
#       same change that fixed them, as its own comment required; the marker
#       is its replacement as the only fold-fired detector, since post-#348
#       the genuine sequence is architecturally transparent.
for v in "A cclean2 fold r0" "A cclean2 fold r1" "A cclean2 flags" \
         "A cclean2 base r5" "A cclean2 base r1" "A cclean2 base r0" \
         "A cclean2 cnt r6" "A cclean2 cnt r1" "A cclean2 tail flags" \
         "A cclean2 tail r0" "A cclean2 tail r1" "A cclean2 tail V" \
         "A cclean2 zero flags" "A cclean2 zero r0" "A cclean2 zero r1" \
         "A cclean2 quiet" "A cclean2 fires" "A cclean2 fires ctrl"; do
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

# ---- #351/#352/#353: netbsd_idle, via the READ-AHEAD install path -----------
# A SEPARATE probe (arm_idle_probe.py), because every row here runs with NO
# breakpoint so translation read-ahead is ON -- the install path a real guest
# takes, and the one arm_flags_probe.py's breakpoint driver structurally cannot
# reach (cpu_dyntrans.c:1939 gates read-ahead on breakpoints.n == 0). The
# register-alias defect (c) and the forward-beq hang (d) are invisible under a
# breakpoint, so they could only be witnessed here.
#
# Swept against a binary built from the pre-fix HEAD (704036e): 2 of 9, failing
# exactly the seven DISC rows -- exit dest 0x77, exit flags 0x6, idle dest 0x77,
# idle flags 0x8, `alias exits` 0x55 (fold took the wrong exit), `target
# reached` deadbeef (the forward-beq HUNG the guest), and `fires` (no marker) --
# and passing the two PINs. On the fixed build: 9/9.
IDLELOG=$LOGDIR/gate_arm_idle.log
python3 arm_idle_probe.py "$PMAX" "$STUB" > "$IDLELOG" 2>&1 || true

if ! grep -q "IDLE_RESULT=" "$IDLELOG"; then
    note "idle probe produced no result line; last lines follow"
    tail -5 "$IDLELOG" | sed 's/^/       /'
    gate_skip "idle probe did not complete"
fi

grep -E " ok$| FAIL$" "$IDLELOG" | sed 's/^/       /'

ictrl=$(grep -o "IDLE_CONTROL=[A-Z]*" "$IDLELOG" | tail -1 | cut -d= -f2)
check "idle control proves the probe measures" "${ictrl:-missing}" "OK"

ires=$(grep -o "IDLE_RESULT=[0-9]*/[0-9]*" "$IDLELOG" | tail -1 | cut -d= -f2)
igot=${ires%/*}; iwant=${ires#*/}
check "idle rows run"     "$iwant" 9
check "idle rows correct" "$igot"  "$iwant"

# Named rows, one contract each. The two PINs pass on both builds by design:
# `quiet` asserts marker absence at default verbosity (boot-log hygiene), and
# `alias -J ref` pins that the alias program's architectural answer really is
# idle (so the DISC above attributes its 0x55 to the fold, not the program).
for v in "A idle exit dest" "A idle exit flags" "A idle path dest" \
         "A idle path flags" "A idle alias exits" "A idle target reached" \
         "A idle fires" "A idle quiet" "A idle alias -J ref"; do
    n=$(count "$IDLELOG" "^$v  .*ok$")
    check "  idle row: $v" "$n" 1
done

# ---- #354: netbsd_memcpy, via the READ-AHEAD install path -------------------
# The memcpy fold did memcpy(dst,src,32) + advanced r0/r1 but never wrote
# r3/r4/ip/lr, which the architecture leaves = the last 16 bytes loaded (the
# final iteration's second ldmia). Same SEPARATE-probe / read-ahead-ON reason
# as the idle rows. Owed words are full-width and distinct per register so a
# byteswap or wrong index is self-evident.
#
# Swept against a binary built from the committed HEAD (pre-#354): 4 of 12,
# failing exactly the eight DISC rows (r3/r4/ip/lr = seeds 0x33/0x44/0xcc/0xee
# on both the 1-iteration and 2-iteration loops) and passing the four r0/r1
# PINs (the advance was always correct). On the fixed build: 12/12.
MEMLOG=$LOGDIR/gate_arm_memcpy.log
python3 arm_memcpy_probe.py "$PMAX" "$STUB" > "$MEMLOG" 2>&1 || true

if ! grep -q "MEMCPY_RESULT=" "$MEMLOG"; then
    note "memcpy probe produced no result line; last lines follow"
    tail -5 "$MEMLOG" | sed 's/^/       /'
    gate_skip "memcpy probe did not complete"
fi

grep -E " ok$| FAIL$" "$MEMLOG" | sed 's/^/       /'

# The control proves the harness runs end-to-end (program assembled, guest
# executed, dump parsed, byteswap convention right) against the GENUINE
# instruction path under -J. It does NOT prove the measured sessions went
# through the FOLD: post-#354 the fold and the genuine path agree by
# construction, so nothing here would notice if a future change broke the
# combiner registration -- the rows would keep passing via the real
# instructions and the coverage would silently vanish. Only a #349/#352-style
# fold-fired marker closes that; it is recorded in OUTSTANDING_BUGS, and the
# historical pre-#354 sweep (4/12, the eight DISC rows red) is what establishes
# that these rows discriminate at all.
mctrl=$(grep -o "MEMCPY_CONTROL=[A-Z]*" "$MEMLOG" | tail -1 | cut -d= -f2)
check "memcpy control: harness measures (not fold-fired)" "${mctrl:-missing}" "OK"

mres=$(grep -o "MEMCPY_RESULT=[0-9]*/[0-9]*" "$MEMLOG" | tail -1 | cut -d= -f2)
mgot=${mres%/*}; mwant=${mres#*/}
check "memcpy rows run"     "$mwant" 17
check "memcpy rows correct" "$mgot"  "$mwant"

# The four r0/r1 PINs pass on both builds -- they guard against a fix that
# regresses the advance while writing the registers (Codex's clobber concern:
# r0/r1/r2 are outside the {r3,r4,ip,lr} reglist, so the exact-iword matcher
# already forbids aliasing; these pins make that guarantee visible).
#  #359: the five `dst` rows are the only assertions in this whole gate that
#  read the BYTES the fold moved. Everything else here reads registers, and
#  registers cannot see the copy size: r3/r4/ip/lr are published by a direct
#  page read that bypasses the fold's memcpy call, and r0/r1 advance
#  unconditionally. Measured, and this is why the rows exist: a build whose fold
#  called memcpy with 16 instead of 32 -- half the bytes moved, same iteration
#  count, same register advance -- passed this probe 12/12 and the whole of gate
#  14 at 243 checks. With the dst rows it reads 15/17, red at exactly
#  `1it dst w6` and `2it dst w14`, both showing the pre-fill sentinel where a
#  source word was owed. They are PIN, not DISC: the genuine ldmia/stmia moves
#  the same bytes, so the destination is identical folded or not -- what they
#  discriminate is a broken copy. Note `2it dst w9` deliberately PASSES on that
#  mutant (it lies in the first 16 bytes of the second iteration, which is still
#  copied); the discriminator for a later iteration is w14, and keeping both
#  makes the row set say which half of the copy failed.
for v in "A memcpy 1it r3" "A memcpy 1it r4" "A memcpy 1it ip" \
         "A memcpy 1it lr" "A memcpy 1it r0" "A memcpy 1it r1" \
         "A memcpy 1it dst w1" "A memcpy 1it dst w6" \
         "A memcpy 1it dst tail" \
         "A memcpy 2it r3" "A memcpy 2it r4" "A memcpy 2it ip" \
         "A memcpy 2it lr" "A memcpy 2it r0" "A memcpy 2it r1" \
         "A memcpy 2it dst w9" "A memcpy 2it dst w14"; do
    n=$(count "$MEMLOG" "^$v  .*ok$")
    check "  memcpy row: $v" "$n" 1
done

# ---- #355/#356: the strlen fold ---------------------------------------------
# #355: COMBINE(strlen) never required the load's base and destination to
# differ, so `ldrb r3,[r3,#1]!` folded. The genuine writeback overwrites the
# loaded byte, so the cmps compares an ADDRESS and the loop runs on; the fold's
# condition tests the byte and EXITS. The encoding is UNPREDICTABLE, so neither
# answer is "wrong" -- but the emulator was giving two answers for one program
# depending on whether the combination happened, and -J is this gate's own
# architectural oracle.
#
# #356: the walk had no budget bound and ran the whole string inside ONE
# dispatch -- host unresponsive for the duration, and n_translated_instrs (an
# int, reset per run_instr, with a REPLAYABLE walk) drivable into signed
# overflow with ~18-24 MB of non-NUL memory at the DEFAULT -M 64.
#
# The yield is witnessed WITHOUT a clock: the test machine's mp device exposes
# cpu->ninstrs at 0x110000d0, and ninstrs is committed only when run_instr
# returns, so a guest sampling it either side of a 16 KB walk reads ~0 if the
# walk never left one dispatch. All numeric rows assert BANDS, because the exact
# counts depend on N_SAFE_DYNTRANS_LIMIT (8191) and the 120-dispatch group
# boundary -- named so a change to either moves the bands deliberately.
#
# Swept against a binary built from the pre-fix HEAD: 3 of 7, failing exactly
# the four discriminators -- `yields` and `bill band` both read 0 (the walk
# never left the dispatch), `alias exits` read 0x55 (the fold took the wrong
# exit) and `alias moved` read "no" (it had exited after three bytes). The
# three PINs pass on both builds. On the fixed build: 7/7.
STRLOG=$LOGDIR/gate_arm_strlen.log
python3 arm_strlen_probe.py "$PMAX" > "$STRLOG" 2>&1 || true

if ! grep -q "STRLEN_RESULT=" "$STRLOG"; then
    note "strlen probe produced no result line; last lines follow"
    tail -5 "$STRLOG" | sed 's/^/       /'
    gate_skip "strlen probe did not complete"
fi

grep -E " ok$| FAIL$" "$STRLOG" | sed 's/^/       /'

sctrl=$(grep -o "STRLEN_CONTROL=[A-Z]*" "$STRLOG" | tail -1 | cut -d= -f2)
check "strlen control: -J reference walked and yielded" "${sctrl:-missing}" "OK"

sres=$(grep -o "STRLEN_RESULT=[0-9]*/[0-9]*" "$STRLOG" | tail -1 | cut -d= -f2)
sgot=${sres%/*}; swant=${sres#*/}
check "strlen rows run"     "$swant" 7
check "strlen rows correct" "$sgot"  "$swant"

for v in "A strlen -J ref" "A strlen -J end addr" "A strlen yields" \
         "A strlen bill band" "A strlen end addr" "A strlen alias exits" \
         "A strlen alias moved"; do
    n=$(count "$STRLOG" "^$v  .*ok$")
    check "  strlen row: $v" "$n" 1
done

# #357: the base writeback (cpu_arm_instr_loadstore.c)
# -------------------------------------------------------------------------
# The template computed one address, masked it for alignment, and wrote the
# base register back FROM THE MASKED VALUE. ARM ARM DDI 0100I computes the
# writeback from the unmasked Rn (A5.2.8 post-indexed, A5.2.5 pre-indexed;
# A2-43 puts the truncation inside Memory[]).
#
# The reachable symptom is a loop that cannot make progress, not a wrong
# value: with a word access and a post-index offset of 1 the masked writeback
# is a FIXED POINT -- base 0x10001 masks to 0x10000, plus 1 is 0x10001, the
# value it started from. Rows A/A2 run ten iterations and assert the exact
# architectural result; the count lives in r3, so nothing here depends on how
# far execution got or on host speed.
#
# WHICH ROW REACHES WHICH SITE -- #364 CORRECTED THIS TABLE, WHICH WAS INVERTED.
# It used to say the fast path "only runs once the page is in the translation
# array, so a single-execution row measures the GENERAL path and nothing else",
# and it referred forward to a "CORRECTION below" that was never written. Both
# are fixed here. MEASURED: no row in this probe reached the general path at
# all -- a marker at the top of A__NAME__general counted ZERO hits on all 17
# rows, including the x10 iterations and both re-seeded passes.
#
# The cause was the probe's own seeding. `put w` -> store_32bit_word ->
# memory_rw(CACHE_DATA), and insertion is gated on !no_exceptions, so a page
# seeded with `put w` is ALREADY warm before the guest runs. `put b` uses
# CACHE_NONE | NO_EXCEPTIONS and does not insert. The old note had the two
# backwards, and it was recorded as a verified mechanism, so two shipped rounds
# leaned on it: #357's general-path writeback and #362's general-path rotation
# were both unmeasured, and each was independently confirmed DELETABLE with this
# whole gate still green at 358 checks.  (This said 261 until 2026-08-26 -- the count
# grew when the gate took on `barearm` and `cats`, and commit 6014b7e's message records
# "PASS 358 checks (was 261)".  The carrier carried the same stale number; both were
# corrected together, because a number with two homes rots in both.)
#
# TWO AXES, kept apart. The first draft of this correction conflated them and
# claimed the new cold rows cover "general post-index writeback". They do NOT:
# their LDR is P=1/W=0, and the writeback is emitted only under (P and W) or
# (not P), so an offset form has no writeback statement at all. Caught in review.
#
#   -- the four WRITEBACK sites (the `reg(ic->arg[0]) =` statements) --
#   fast    post-index  every iteration of the x10 rows, plus the one-shot
#                       post-index rows and the PIN rows (11 in total)
#   fast    pre-index   "pre4 unal gen" AND "pre4 unal fast" (both passes)
#   general post-index  UNCOVERED
#   general pre-index   UNCOVERED
#
#   -- rows with NO writeback site (P=1/W=0 offset forms) --
#   "pre4 no wb" and the three "rot word unal" rows   (fast function)
#   the three "rot word cold" rows                    (general function)
#
#   -- which rows enter A__NAME__general AT ALL, the question this round answers --
#   the three "rot word cold" rows, and nothing else: they exercise the
#   load-and-rotate arm and the memory_rw slow path, which is a DATA site.
#
# So #357's general-path WRITEBACK fix still has no row reaching it. That is
# recorded in OUTSTANDING_BUGS rather than papered over here.
#
# No line numbers here on purpose: the ones this table used to carry (:213/:216,
# :338/:342) had gone stale by the round that corrected it -- the third time in
# this file, whose own #357 note already says a numeric cite here has gone stale
# twice before.
#
# "pre4 unal fast" still needs its two passes with the base re-seeded each pass:
# without the re-seed, pass 1 leaves an ALIGNED base and the row has nothing
# left to discriminate. Only its SITE attribution was wrong, not its design.
# Loads and stores are separate instantiations of the template, so a load-only
# set cannot see a store-side regression: hence the store row. Register-offset
# forms are a third family: hence the regofs row.
#
# The control is the loaded-data row rather than a pass count: r1 starts at 0,
# so a distinctive nonzero value proves the guest really executed and really
# loaded. A wrong register field reads 0, and a row that accepts 0 accepts that
# mistake by accident -- this harness has shipped exactly that defect before.
#
# DISC-M ("model") on the halfword row is deliberate: an unaligned halfword
# load's DATA is UNPREDICTABLE (A4.1.28) while its writeback stays defined
# (A5.3.6), so the row asserts the BASE only and pins the pseudocode model, not
# a silicon mandate. Every other DISC row is a word form, i.e. mandated space.
# There is no *unaligned* LDRD/STRD row on purpose: A2.8 makes an unaligned
# doubleword access UNPREDICTABLE prior to ARMv6, so every base that would
# exercise the ~7 mask makes the instruction unspecified -- covered by the
# fix, not honestly assertable. [#389: ALIGNED LDRD/STRD byte-order rows now
# live in the endian section below -- this note is scoped to the writeback/
# unaligned axis only.]
#
# #364: the sentence that used to stand here -- "no row pins the unaligned
# loaded DATA ... such a row would be inverted by the round that fixes
# rotation" -- was falsified by #362, which added exactly three such rows, and
# by #364, which added three more from a cold page. It is removed rather than
# annotated. The ALIGNED data row remains, and remains correct for its own
# reason: no rotation applies at offset 0 in any architecture version.
#
# Swept against a snapshot of the pre-fix binary: 5 of 14, with all nine DISC
# rows failing at exactly the predicted masked values and all five PINs
# passing. On the fixed build: 14/14. Read that 5/14 with the corrected table
# above -- it is entirely a FAST-path result, since no row of that era entered
# the general path. #362 took the set to 17, #364 to 20.
WBLOG=$LOGDIR/gate_arm_writeback.log
python3 arm_writeback_probe.py "$PMAX" > "$WBLOG" 2>&1 || true

if ! grep -q "WRITEBACK_RESULT=" "$WBLOG"; then
    note "writeback probe produced no result line; last lines follow"
    tail -5 "$WBLOG" | sed 's/^/       /'
    gate_skip "writeback probe did not complete"
fi

grep -E " ok$| FAIL$" "$WBLOG" | sed 's/^/       /'

wctrl=$(grep -o "WRITEBACK_CONTROL=[A-Z]*" "$WBLOG" | tail -1 | cut -d= -f2)
check "writeback control: guest ran and loaded" "${wctrl:-missing}" "OK"

wres=$(grep -o "WRITEBACK_RESULT=[0-9]*/[0-9]*" "$WBLOG" | tail -1 | cut -d= -f2)
wgot=${wres%/*}; wwant=${wres#*/}
check "writeback rows run"     "$wwant" 22
check "writeback rows correct" "$wgot"  "$wwant"

# ---------------------------------------------------------------------------
# #524 (armbdt): block data transfer through a COLD host page.
#
# arm_pop()/arm_push() take a fast path when the host page is resident and a
# slow memory_rw() path when it is not.  The fast path truncates the low two
# address bits for free; the slow path passed the RAW address, whose transfer
# is a page-granular memcpy -- so an unaligned base SPLICED BYTES ACROSS A WORD
# BOUNDARY and the same instruction returned different bytes according to host
# page-cache warmth.  Fixed by masking AT THE TWO ACCESS SITES ONLY; the mask
# must never move to function entry, because writeback uses the unmasked
# running address.
#
# THE DENOMINATOR IS PINNED TO A LITERAL BELOW, DELIBERATELY.  The probe grew
# 25 -> 29 -> 32 -> 39 -> 43 rows across seven kill tables as clause-(d) mutants were
# closed, and a gate that trusts the probe's own denominator cannot tell a
# probe that lost rows from one that never had them.
#
# Five mutants are measured dead in regress/artifacts/armbdt/killtable_20260911e/:
#   M_ENTRY      mask hoisted to entry      27/32  ARM_LDM_WB_UNAL1/2, ARM_STM_WB_UNAL,
#                                                  THUMB_POP_WB_UNAL, THUMB_PUSH_WB_UNAL
#   M_MASK1      mask weakened to & ~1      29/32  ARM_LDM_COLD_DATA_P2, ARM_STM_COLD_DATA_P2,
#                                                  THUMB_PUSH_COLD_DATA_P2
#   M_MASK7      mask over-aligned to & ~7  30/32  ARM_LDM_COLD_DATA_BIT2, ARM_STM_COLD_DATA_BIT2
#   M_PBITCOND   mask conditional on p_bit  31/32  THUMB_PUSH_COLD_DATA_P2
#   M_NULL_MEDIUM both helpers return        8/32  24 rows red; the 8 that SURVIVE are the six
#                                                  PATH_* rows and the two *_COLD_CLOBBER rows
#
# THE KILLING ROWS ARE NAMED, NOT DESCRIBED, FOR TWO REASONS.  A name is checkable against
# killtable_20260911e/probe_<mutant>.raw; a description is not.  And the earlier wording said
# M_ENTRY was "killed by the writeback rows" -- which collided with the arm_writeback_probe.py
# stem and made check_score_claims read 27/32 as a stale claim about THAT probe (its pin is 22).
# A comment that makes a checker wrong is the defanging rule's own lesson: before writing a word
# a tool matches on, ask what the tool will do with it.
#
# *** THE 8 SURVIVORS UNDER THE NULL MEDIUM ARE A DISCLOSED LIMIT, NOT A PASS. ***  With both
# helpers replaced by `return;' nothing is written at all, so a row asserting a NEIGHBOUR was not
# clobbered is satisfied trivially, and the PATH_* rows observe which host-page path was taken
# rather than what landed.  Clause (c) is met by the 24 that do red; these 8 say why 8/32 is not 0.
BDTLOG=$LOGDIR/gate_arm_bdt.log
python3 arm_bdt_probe.py "$PMAX" > "$BDTLOG" 2>&1 || true

if ! grep -q "ARMBDT_RESULT=" "$BDTLOG"; then
    note "bdt probe produced no result line; last lines follow"
    tail -5 "$BDTLOG" | sed 's/^/       /'
    gate_skip "bdt probe did not complete"
fi

grep -E " ok$| FAIL$" "$BDTLOG" | sed 's/^/       /'

bctrl=$(grep -o "ARMBDT_CONTROL=[A-Z]*" "$BDTLOG" | tail -1 | cut -d= -f2)
check "bdt control: liveness and attribution" "${bctrl:-missing}" "OK"

bres=$(grep -o "ARMBDT_RESULT=[0-9]*/[0-9]*" "$BDTLOG" | tail -1 | cut -d= -f2)
bgot=${bres%/*}; bwant=${bres#*/}
#  *** PIN MOVED 32 -> 39 ON 2026-09-11, DELIBERATELY, FOR THE CLASS CLOSURE. ***
#  Pass C measured FIVE clause-(d) mutants at 32/32 -- a TOTAL ESCAPE each -- all
#  one class: every p/u/s/w partition was discharged on the STORE side and
#  undischarged on the LOAD side, because the only leg varying those bits was
#  Thumb PUSH, which calls arm_push().  Seven rows close the load side; all SIX
#  built mutants now die (killtable_20260911g_closure/SCORES.txt):
#    BASE        39/39                     M_SBIT_NONE 38/39 -- S_P2
#    M_POPP_NONE 37/39 -- IB_P2, DB_P2     M_POPP_WEAK 37/39 -- IB_P2, DB_P2
#    M_NPMASK    37/39 -- IB_P2, DB_P2     M_POPW_WEAK 37/39 -- DB_P2, MULTI_P2_R1
#    M_POPU_WEAK 37/39 -- DA_P2, DB_P2
#  A pin that follows the probe cannot tell a probe that GAINED rows from one
#  that LOST them, so the literal moves by hand and says why.
#  *** PIN 39 -> 43 ON 2026-09-12: THE TEN-CELL FLOOR. ***  Table 7
#  (killtable_20260911h_floor) is the first table in this round whose rows are
#  enumerated from the HELPERS OWN INPUTS rather than from the mutant list --
#  which is what the class-closure rule always said, and what pass C invoked but
#  did not do.  Every earlier repair rowed at the residue of the mutant it had
#  just found, so each pass discovered the next strength.
#
#  EVERY NEW ROW SITS AT AN ACCESS ADDRESS = 7 (mod 8): bits 0, 1 and 2 are all
#  set, so ONE access discriminates ~1, ~2, ~3 AND ~7.  No future strength needs
#  a new residue.
#
#    BASE 43/43.  All ten floor cells kill:
#      M_PUSHS_NONE   42/43 ARM_STM_S_R7        M_POPP_MASK2  41/43 IB_P2, DB_P2
#      M_PUSH_IB_WEAK 42/43 ARM_STM_IB_R7       M_PUSH_DA_WEAK 42/43 ARM_STM_DA_R7
#      M_PUSHPC_NONE  42/43 ARM_STM_PC_DB_R7    M_PUSHP_OVER7 41/43 IB_R7, PC_DB_R7
#      plus the six table-g mutants, all still dead.
#    The ONE escape is DISCLOSED: D_PUW_WEAK 43/43, named in the contract.
check "bdt rows run"     "$bwant" 43
check "bdt rows correct" "$bgot"  "$bwant"

# #367: PATH ATTRIBUTION IS NOW A CHECKED QUANTITY, not a comment.
#
# Which of the two load/store paths a row takes was asserted in prose and was
# wrong three rounds running: #364 found the `put w` / `put b` warming note
# INVERTED and recorded as verified, with two shipped rounds leaning on it;
# #364's own draft then mis-attributed a writeback site to an offset form that
# compiles no writeback statement at all; and #365 found the general writeback
# sites reached but UNDISCRIMINATED, since `ldrb` has datalen 1 so the alignment
# mask is the identity for it. Each was rediscovered with a throwaway marker and
# a scratch build, three times, because the instrument did not survive the round.
#
# The emulator now counts entries into A__NAME__general (cpu_arm.h ls_general),
# and `tlbdump` -- previously an EMPTY stub on ARM while it printed on other
# architectures -- reads it out. PULL-ONLY: nothing prints unless a session asks,
# so the rows elsewhere in this gate that assert an ABSENCE of output are
# untouched, and a free-running guest cannot be flooded.
#
# The aggregate carries the seventeen ZEROS -- exactly the claim #364 found
# inverted -- so a warming assumption that silently changes turns this red even
# though no named row below covers those rows individually.
lsres=$(grep -o "LSGEN_RESULT=[0-9]*/[0-9]*" "$WBLOG" | tail -1 | cut -d= -f2)
lsgot=${lsres%/*}; lswant=${lsres#*/}
check "writeback path rows run"     "${lswant:-missing}" 22
check "writeback path rows correct" "${lsgot:-missing}"  "$lswant"

# The five rows that must ENTER the general path, named individually so one
# reverting cannot hide behind the total. The derivation, which matters more than
# the numbers: the general path's own memory_rw SELF-WARMS, so a cold row is 1
# and not N. The `ldrt` row is 1 despite its page being WARM, because the
# is_userpage test precedes the page test and a kernel `put w` insert never sets
# that bit -- which is what makes a T form general-path BY CONSTRUCTION and
# immune to any future seeding change.
for v in "A wb rot word cold plus1" "A wb rot word cold plus2" \
         "A wb rot word cold plus3" "A wb word ldrt post4 unal" \
         "A wb word cold pre4 unal"; do
    n=$(count "$WBLOG" "^$v path  .*ok\$")
    check "  writeback path: $v" "$n" 1
done

# #358: fold-fired markers (netbsd_copyin / netbsd_copyout)
# -------------------------------------------------------------------------
# Both folds replace six user-mode transfers with one C function whose
# registers, addresses and instruction billing are IDENTICAL to the
# instructions replaced, so a row asserting their result passes whether or not
# the fold fires. Until #357 one witness existed -- the template masked its base
# writeback while these folds did not, so an unaligned base read 0x10019 folded
# against 0x10018 genuine -- and #357 correctly removed it by fixing the
# template. These two folds also had NO rows at all before this.
#
# The rows are FREE-RUNNING by necessity, not by style. Measured: a two-pass
# program with a breakpoint one instruction before the folded window executes the
# GENUINE sequence on both the default and the -J build, while the same program
# with no breakpoint folds -- so a breakpoint suppresses the fold. A breakpoint ON
# a slot is worse: that path re-marks its own slot for retranslation and the
# matchers test ic[i].f, so a fold can never install there. Two passes are
# required because the folds gate on is_userpage, which only the user-access
# general handler sets -- the very handler the fold's bail-out delegates to.
#
# Each fold gets a pair so neither row can be vacuous in either direction. The
# `fires` row demands the marker AND the verbosity echo AND the six transferred
# values: without the echo a session whose verbosity raise silently failed would
# report zero markers and look exactly like a dead fold, and without the values
# the row would prove a line was printed rather than that work was done. The
# `quiet` row asserts silence at default verbosity and must never be rewritten to
# drive the guest with `step` -- single-step BYPASSES debugmsg's verbosity gate.
#
# Non-vacuity proven per fold on scratch trees built from this exact source.
# Disabling ONLY netbsd_copyin's arming (by making its iword test unsatisfiable,
# which keeps the statement structure intact) gives 3 of 4, with exactly
# `A fold copyin fires` red and copyout's rows still green. An earlier attempt
# replaced the arming assignment with a comment and left a dangling `if` that
# swallowed the copyout arming, killing both folds -- one real reason and one
# artifact, which is why the break is done by constant and not by deletion.
FOLDLOG=$LOGDIR/gate_arm_foldmark.log
python3 arm_fold_marker_probe.py "$PMAX" > "$FOLDLOG" 2>&1 || true

if ! grep -q "FOLDMARK_RESULT=" "$FOLDLOG"; then
    note "fold-marker probe produced no result line; last lines follow"
    tail -5 "$FOLDLOG" | sed 's/^/       /'
    gate_skip "fold-marker probe did not complete"
fi

grep -E " ok$| FAIL$" "$FOLDLOG" | sed 's/^/       /'

fres=$(grep -o "FOLDMARK_RESULT=[0-9]*/[0-9]*" "$FOLDLOG" | tail -1 | cut -d= -f2)
fgot=${fres%/*}; fwant=${fres#*/}
#  #360: the `warm`/`cold` pairs are the LIVE controls, and the difference from
#  the `quiet` rows is visible in one measurement. On a build with ONLY
#  netbsd_copyin's arming disabled, `A fold copyin quiet` still reads **ok** --
#  it asserts an absence, and an absence is exactly what a dead fold produces --
#  while `A fold copyin cold` goes red because it asserts a DECLINE occurred
#  (install 1, fire 0, decline 1). Measured 5 of 8 on that build, red at exactly
#  the three copyin rows, with copyout's four green.
#
#  The install count is what makes the diagnosis one-read: install 0 means the
#  matcher declined; install 1 with fire 0 and decline 1 means the fold was
#  reached and turned the operands down, and the decline text names the clause.
#  Every arm also asserts the verbosity echo and that r0/r1 advanced by the full
#  six transfers -- the latter holds folded or not, so it proves the program ran
#  without presuming the fold, which is what stops the cold arm's zero from
#  being meaningless. Measured: with verbosity off the guest ran perfectly and
#  reported zero fires AND zero installs, so counting absences alone cannot tell
#  a dead fold from a broken session.
#  #361 adds rows for the last two folds that had #358 markers but nothing
#  exercising them -- the scope debt #358 was criticised for. Two shapes, and
#  they are NOT interchangeable:
#    xchg  declines at the MATCHER (install 0), because #342's `a != b` term
#          rejects the shape before anything is installed.
#    scanc declines at a GUARD (install 1, decline 1), like copyin/copyout, and
#          has TWO decline sites -- the second reachable only after the first
#          passes, since the table address is computed from the byte just loaded.
#          Both are exercised, with distinct reason spellings so a row can say
#          which page missed.
#
#  `A fold xchg selective` is one row spanning BOTH xchg arms, and it exists
#  because a measuring seat showed the negative arm is VACUOUS ALONE: install 0 /
#  fire 0 reads identically on a healthy build and on one with xchg's arming
#  removed, so by itself it cannot tell "the matcher rejected the shape" from
#  "the matcher does not exist" -- the #360 defect again. Measured on an
#  arming-dead build: `A fold xchg samereg` reads **ok** while
#  `A fold xchg selective` goes red. The rejected alternative is recorded in the
#  probe: relocating #342's term into the matched shape so the arm self-diagnoses
#  works, but it edits a shipped correction's guard for instrumentation's sake.
#
#  scanc's r3 is a genuine three-way value witness -- 0x77 is table[4] when the
#  fold runs, 0x66 is table[0] because an unmapped string load yields zero, and
#  0x00 when the table page is the missing one -- plus an r5 sentinel proving the
#  program reached its end. Measured: on a scanc-arming-dead build all three arms
#  keep byte-identical register values and only the marker triple moves, so a
#  value-only row would be vacuous for this fold.
check "fold-marker rows run"     "$fwant" 21
check "fold-marker rows correct" "$fgot"  "$fwant"

# #383: the four BE rows put the copyin/copyout folds' byte-order handling on
# the test surface -- on barearm both folds install and fire (their matchers
# gate on HOST endianness, not guest), so the value rows discriminate the fix.
# The +1/+3 UNALIGNED copyin rows are the composition-order discriminators (a
# fix swapping AFTER #362's rotation passes +0 but fails these). FOLDMARK_
# CONTROL_BE is the fix-state-independent liveness pin (r1 ^ sl == the
# architectural word on every build), so a dead barearm session cannot
# false-green the BE group.
fctrlbe=$(grep -o "FOLDMARK_CONTROL_BE=[A-Z]*" "$FOLDLOG" | tail -1 | cut -d= -f2)
# #384: the control pins that the barearm rig ran, both passes executed, and
# the rig is genuinely big-endian (an LE rig fails it). It does NOT prove the
# fold fired -- that is the value rows' fire==1 -- so the name does not claim it.
check "fold-marker BE control: barearm ran, rig is BE" "${fctrlbe:-missing}" "OK"

for v in "A fold copyin fires" "A fold copyin quiet" \
         "A fold copyout fires" "A fold copyout quiet" \
         "A fold copyin warm" "A fold copyin cold" \
         "A fold copyout warm" "A fold copyout cold" \
         "A fold xchg fires" "A fold xchg samereg" \
         "A fold xchg selective" "A fold scanc fires" \
         "A fold scanc nostr" "A fold scanc notbl" \
         "A fold copyin rot plus1" "A fold copyin rot plus2" \
         "A fold copyin rot plus3" \
         "A fold copyin BE +0" "A fold copyin BE +1" \
         "A fold copyin BE +3" "A fold copyout BE"; do
    n=$(count "$FOLDLOG" "^$v  .*ok$")
    check "  fold-marker row: $v" "$n" 1
done

for v in "A wb word post1 unal x10" "A wb word post1 algn x10" \
         "A wb word post4 unal" "A wb word pre4 unal gen" \
         "A wb word pre4 unal fast" "A wb word postneg4 unal" \
         "A wb store post1 unal x10" "A wb regofs post1 unal x10" \
         "A wb halfword post1 unal" "A wb word post4 algn" \
         "A wb algn load data" "A wb byte post1 unal" \
         "A wb word pre4 no wb" "A wb wrap from zero" \
         "A wb rot word unal plus1" "A wb rot word unal plus2" \
         "A wb rot word unal plus3" \
         "A wb rot word cold plus1" "A wb rot word cold plus2" \
         "A wb rot word cold plus3" \
         "A wb word ldrt post4 unal" "A wb word cold pre4 unal"; do
    n=$(count "$WBLOG" "^$v  .*ok$")
    check "  writeback row: $v" "$n" 1
done

# #372: the general-path word STORE ignored cpu->byte_order.
# ----------------------------------------------------------------------------
# Its arm was UNCONDITIONALLY EMPTY -- guard `!A__B && !A__H && HOST_LE` with an
# `#ifdef A__STRD`-only body, and A__STRD implies A__H, which the guard excludes.
# So a plain word STR on an LE host emitted no bytes and memory_rw copied the
# register's HOST bytes; the FAST path was always order-aware, so one STR wrote
# guest order to a warm page and host order to a cold one, and every strt (always
# general on its first access per page) was reversed.
#
# This probe runs BOTH byte orders. The six `be *` rows use -E barearm (BE) and
# are the DISCriminators; the six `le *` rows use -E testarm (LE) and are
# INVARIANCE CONTROLS -- on LE the broken code was accidentally right (host order
# == guest order), so they pin nothing about #372 and exist only to catch a fix
# that repairs BE by breaking LE. The `ldrb` witnesses are the purest form: a
# byte load has no byte order, so it exposes the raw memory layout directly, and
# the buggy column is the exact reverse of the arch column.
#
# #372's original sweep (its SIX BE + six LE rows): pre-fix 7 of 12 -- the five
# cold BE rows red at the host-order values, the warm control and LE controls
# green. Fixed: 12/12. #378 grew the section to 34 rows (22 BE / 12 LE) with the
# INVERTED polarity -- its sweep numbers are in the named-row comment below; the
# 12-row narrative above this line is #372 history, scoped as such by #379.
# #386 grew it to 58: swp (the last word-sized ARM memory handler, LE-only on
# both sides + raw unmasked address) and its swpb/aligned-LE/by-construction
# controls; sweep numbers in the named-row comment below.
ENDLOG=$LOGDIR/gate_arm_endian.log
python3 arm_endian_probe.py "$PMAX" > "$ENDLOG" 2>&1 || true

if ! grep -q "ENDIAN_RESULT=" "$ENDLOG"; then
    note "endian probe produced no result line; last lines follow"
    tail -5 "$ENDLOG" | sed 's/^/       /'
    gate_skip "endian probe did not complete"
fi

grep -E " ok$| FAIL$" "$ENDLOG" | sed 's/^/       /'

# The control is the BE cold-word row's SIBLING warm row: it demands a
# distinctive nonzero word through the order-aware fast path, proving the BE rig
# (barearm) constructed and the program ran, before any DISC row is believed.
ectrl=$(grep -o "ENDIAN_CONTROL=[A-Z]*" "$ENDLOG" | tail -1 | cut -d= -f2)
check "endian control: BE rig ran and stored" "${ectrl:-missing}" "OK"

# #378's own liveness pin: the multi-transfer cold rows go through bdt_*, which
# swaps on EVERY build, so they read arch values on buggy and fixed builds
# alike -- a dead rig, wrong register field or non-firing LDM reads 0/sentinel
# instead. Distinct from ENDIAN_CONTROL so the two extensions fail separately.
ectrl378=$(grep -o "ENDIAN_CONTROL378=[A-Z]*" "$ENDLOG" | tail -1 | cut -d= -f2)
check "endian control: multi rows ran (378)" "${ectrl378:-missing}" "OK"

# #379: the warm DISC rows depend on `put w` having warmed the pages, and a
# silently failing put would flip them all to a FALSE GREEN on a buggy build
# (bdt_* is architecturally correct on both arms). The probe checks every
# put's echo for the debugger's FAILED marker.
eputs=$(grep -o "PUT_STATUS=[A-Z]*" "$ENDLOG" | tail -1 | cut -d= -f2)
check "endian puts all landed (379)" "${eputs:-missing}" "OK"

eres=$(grep -o "ENDIAN_RESULT=[0-9]*/[0-9]*" "$ENDLOG" | tail -1 | cut -d= -f2)
egot=${eres%/*}; ewant=${eres#*/}
#  #389's liveness pin: the LE LDRD/STRD rows are fix-state-independent (LE
#  was always correct) and read the sentinel 0 if the instructions are dead.
ectrld=$(grep -o "ENDIAN_CONTROL_D=[A-Z]*" "$ENDLOG" | tail -1 | cut -d= -f2)
#  #389 pass-2 (Opus seat): the name used to read "ldrd/strd ran", which
#  overclaimed -- BOTH pins behind ENDIAN_CONTROL_D are on the LE rig
#  (testarm), so nothing here pins that LDRD/STRD executed on barearm. That is
#  not a fixable omission: a liveness pin must be fix-state-INDEPENDENT, and on
#  BE every LDRD/STRD row changes value with the fix by construction. The BE
#  side is still fail-closed -- a dead BE rig reddens its ten DISC rows -- but
#  the NAME must say what it actually pins.
check "endian control: ldrd/strd ran on the LE rig (389)" "${ectrld:-missing}" "OK"

check "endian rows run"     "${ewant:-missing}" 102
check "endian rows correct" "${egot:-missing}"  "$ewant"

# The BE discriminators named individually, so one reverting cannot hide
# behind the total. #372's DISC rows are the COLD ones (general path was
# wrong); #378's DISC rows are the WARM ones (LDM/STM fast path was wrong) --
# the inverted polarity is the point, and the probe carries explicit per-row
# kinds for exactly that reason. Swept against the pre-#378 build: 24/34, the
# ten warm multi rows red at exactly the per-word-reversed values. Fixed: 34/34.
# #386 grew the section 34 -> 58 (swp/swpb; X(swp) was LE-only both sides and
# unrotated/unmasked). Swept against the pre-#386 build: 42/58, all 16 DISC
# rows red at exactly the predicted buggy values. Fixed: 58/58. The LE unal
# rows are DISC too (the manual's rotation is endian-independent, so the fix
# MOVES them); "swp be unal b2" is arch==buggy by construction (bits[15:8]
# lands at P+2 under both the buggy +1-shifted LE write and the fixed BE
# write) and is deliberately NOT in this list.
# #387 grew it 58 -> 70: the +2 offset groups, because three wrong forms
# AGREE with the shipped code at +1 and aligned -- `8*(addr&1)`, a raw-odd
# rotate guard, and an `addr &= ~1` mask -- and all three passed the 58-row
# set (the fold-marker probe's three-offsets rule). Every +2 row is DISC
# (the +1 b2 collision does not recur at +2). Measured: each hole-mutant
# reddens the +2 rows while the +1 rows stay green (68/68/58 of 70).
# The pattern below also pins each named row's KIND (DISC): re-typing a red
# discriminator as CTRL with arch=buggy would otherwise keep the name green
# -- the "shipped fix with no detector" vacuity mode, closed for free here.
for v in "be cold word" "be cold byte0" "be cold byte1" \
         "be cold byte2" "be cold byte3" \
         "be stm warm b0" "be stm warm b1" "be stm warm b2" "be stm warm b3" \
         "be stm warm b4" "be stm warm b5" "be stm warm b6" "be stm warm b7" \
         "be ldm warm r1" "be ldm warm r2" \
         "swp be word" "swp be b0" "swp be b1" "swp be b2" "swp be b3" \
         "swp be unal r2" "swp be unal b0" "swp be unal b1" \
         "swp be unal b3" "swp be unal sent" \
         "swp le unal r2" "swp le unal b0" "swp le unal b1" \
         "swp le unal b2" "swp le unal b3" "swp le unal sent" \
         "swp be un2 r2" "swp be un2 b0" "swp be un2 b1" \
         "swp be un2 b2" "swp be un2 b3" "swp be un2 sent" \
         "swp le un2 r2" "swp le un2 b0" "swp le un2 b1" \
         "swp le un2 b2" "swp le un2 b3" "swp le un2 sent" \
         "ldrd be r4" "ldrd be r5" \
         "strd be b0" "strd be b1" "strd be b2" "strd be b3" \
         "strd be b4" "strd be b5" "strd be b6" "strd be b7" \
         "390 be base +8" "390 be base +12" \
         "390 le base +8" "390 le base +12" \
         "390 be bothpc" "390 le bothpc"; do
    n=$(count "$ENDLOG" "^$v  *DISC .*ok$")
    check "  endian row: $v" "$n" 1
done

#  #390's CTRL rows, pinned by name so they cannot be quietly retyped or
#  dropped -- a DISC pattern would never match them.  Two different reasons:
#
#  the DATA-role rows must pass on the PRE-fix build too, because they do not
#  detect the defect; they detect a WRONG FIX that moves the stored R15 value
#  off +12, which A2-9 forbids doing for some R15 stores and not others.
#
#  the LDRD rows are CTRL because the round's original claim about them was
#  REFUTED by measurement: LDRD's base was never +12.  They began as DISC with
#  a `buggy` column that turned out to be fiction -- the mutant battery left
#  them green, and the actual pre-#390 parent reads the same values the fixed
#  build does.  They are kept as standing evidence that LDRD with Rn == PC is
#  unaffected, and they will redden if a future round drags it into that path.
for v in "390 be data +12" "390 le data +12" \
         "390 be ldrd r0" "390 be ldrd r1" \
         "390 le ldrd r0" "390 le ldrd r1"; do
    n=$(count "$ENDLOG" "^$v  *CTRL .*ok$")
    check "  endian row: $v" "$n" 1
done

# ---------------------------------------------------------------------------
#  #432: THE FOOTBRIDGE'S FIRST REACHABILITY WITNESS OF ANY KIND.
#
#  Recorded before this probe existed: R6 was the ONLY code round in this tree with no
#  reachability witness -- no rig boots a footbridge machine and there is no m8online analog.
#  regress/diff_footbridge.c calls the device functions DIRECTLY, so it proves BEHAVIOUR and
#  would stay green under a change that unmapped the device entirely.  This drives real guest
#  ldr/str through the real address decode and the real memory_rw plumbing on a COLD DEBUGGER:
#  measured 1.9 s for three arms, against a rig boot this tree does not have at all.
#
#  IT LIVES HERE, in the ARM gate, for the same reason m8820x_sites_probe.py lives in
#  gate_m88k_rounding.sh: `cats` is an ARM machine and this gate already writes the four-byte
#  raw stub that makes such a machine construct.  A new gate script would move GATE_MANIFEST,
#  which is a bigger claim than one probe is worth.
#
#  THE TRAP IT GUARDS, and it nearly produced a confident wrong answer.  machine_cats.c:131
#  maps only the low 256 MB and the footbridge is at PA 0x42000000, so under the boot-time MMU
#  every device row reads 0x0 WITH A RAM LIVENESS ROW STILL GREEN -- which is exactly what an
#  absent device looks like.  The probe's arm T runs the same program with the MMU-disable
#  instructions replaced by nops and requires that it CANNOT produce the device's answer; arm L
#  reads CP15 c1 back and requires bit 0 clear.  Negative-controlled in both directions.
FBLOG=$LOGDIR/footbridge_sites.log
python3 footbridge_sites_probe.py "$PMAX" "$STUB" > "$FBLOG" 2>&1 || true
grep -E "^(  arm |C[0-9]|A[0-9]|I1|K1|D1)" "$FBLOG" | sed 's/^/       /'

if ! grep -q "FOOTBRIDGE_SITES_" "$FBLOG"; then
    note "footbridge probe produced no verdict; last lines follow"
    tail -5 "$FBLOG" | sed 's/^/       /'
    check "footbridge probe completed" "no" "yes"
else
    #  THE CONTROL FIRST, and separately from the verdict.  A probe whose controls failed has
    #  measured NOTHING, and this one has a control that a liveness row cannot substitute for.
    check "footbridge: controls prove the probe measures" \
          "$(grep -c 'FOOTBRIDGE_SITES_CONTROL=OK' "$FBLOG")" "1"
    check "footbridge: every row green" \
          "$(grep -c 'FOOTBRIDGE_SITES_PASS' "$FBLOG")" "1"
    #  VALUES, NOT SURVIVAL.  0x1011 is DC21285_VENDOR_ID (dev_footbridge.c:423) and can only
    #  have come back through this device; an unmapped read survives too, it just returns 0.
    check "footbridge: VENDOR_ID 0x1011 through a real guest ldr" \
          "$(grep -cE '^A1 .*got=0x00001011 .*ok$' "$FBLOG")" "1"
    #  The vanishing top byte IS the handler's signature: :548 stores idata & TIMER_MAX_VAL.
    #  RAM, or any decode that merely absorbed the store, returns 0x12345678 unchanged.
    check "footbridge: TIMER_1_LOAD masked to 24 bits by the handler" \
          "$(grep -cE '^A2 .*got=0x00345678 .*ok$' "$FBLOG")" "1"
    #  THE PROBE'S OWN FAILABILITY CONTROL.  Arms L and K differ by ONE instruction; K reads
    #  IRQ_ENABLE_SET, an UNFIXED fatal()+exit(1) at :495-497.  Without it, "SURVIVED" on every
    #  row is satisfied by a probe whose guest code never reached the device at all.
    check "footbridge: the one-instruction kill arm still dies" \
          "$(grep -cE '^K1 .*ok$' "$FBLOG")" "1"
    #  The defence against the hand-assembled-encoding trap: every planted word is compared
    #  against the disassembly the emulator printed AS IT STEPPED IT.
    check "footbridge: no planted word failed its disassembly check" \
          "$(grep -c 'DISASSEMBLY MISMATCH' "$FBLOG")" "0"
fi

#  ---------------------------------------------------------------------------------------
#  #439/#440 PIT 8253 latch + LSB/MSB selector -- pitlatch / pitclobber.
#
#  WIRED HERE, ALONGSIDE footbridge_sites_probe.py, BECAUSE gate_hygiene.sh SAID SO.  Its
#  own 17 -> 18 bump note reads: "Wiring it into gate_arm.sh alongside
#  footbridge_sites_probe.py is the follow-up, and it wants an operator who can run that
#  gate."  The probe execs `-E cats` and hand-assembles ARM, so this is the only gate whose
#  machine it shares.
#
#  *** IT SHIPPED UNWIRED AND THE CARRIER SAID WHY THAT IS DANGEROUS: an unwired probe is
#  exactly what shipped latent in cf4b083. ***  It has been dated-exempt in
#  check_probe_wiring.py until 2026-09-20 (`wiringcliff`), and this discharges that debt --
#  the exemption line comes out in the same edit, which is what stops a stale exemption
#  outliving its cause.
#
#  CONTROLS FIRST AND SEPARATELY.  The probe's own header says it: "CONTROLS (if any is RED
#  every row below is meaningless)".  C1 is a RAM liveness through the same decode, C2 reads
#  CP15 c1 back to prove the MMU really went off, A1 is a device signature -- and arm T is
#  the negative control that runs the same program with the MMU-disable instructions
#  replaced by nops and requires it CANNOT produce the device's answer.  Under the boot-time
#  MMU the low 256 MB alone is mapped, so a device row reads 0x0 WITH A LIVENESS ROW STILL
#  GREEN, which is indistinguishable from an absent device.  That is why C2 and T exist and
#  why a liveness row cannot stand in for them.
#  ---------------------------------------------------------------- #497 widthkillclass
#  *** THIS PROBE IS FOR AN SGI/MIPS MACHINE AND IT IS WIRED INTO THE GATE NAMED `arm`.
#  That is following a precedent, not endorsing it. ***  This gate already runs
#  footbridge_sites_probe.py and pit8253_latch_probe.py -- neither of which is an ARM
#  instruction test either -- so it has become the tree's general DEVICE-probe gate by
#  accretion.  *** BUT THOSE TWO AT LEAST RUN THIS GATE'S OWN `-E cats` MACHINE, AND
#  THIS ONE DOES NOT: it is the FIRST probe here on a foreign machine AND CPU family.
#  The PIT wiring comment says outright that it was placed here BECAUSE this is the only
#  gate whose machine it shares. ***  So this is not a third instance of an existing
#  accretion; it is a new kind of one, and the sentence above is true while its
#  implication was generous to the decision it defends.  The architecture-named alternative, gate_mips.sh, is an 82-line RIG-BOOT
#  gate with no probe infrastructure at all; putting a 35-row detector there would change
#  what that gate is for.
#
#  Recorded rather than silently compounded: the right answer is a gate_devices.sh split,
#  which is a harness round of its own and owes its own controls.  FILED as
#  `gatedevicesplit`, with a forcing criterion: the NEXT device probe wired into
#  this gate converts it from filed to OWED.
#  *** #498 sgidewidth.  WIRING THIS PROBE FIRES A PRE-SPECIFIED TRIGGER, AND THE TRIGGER
#  IS HONOURED RATHER THAN QUIETLY PASSED. ***  The #497 block below filed `gatedevicesplit`
#  with a forcing criterion in its own words: "the NEXT device probe wired into this gate
#  converts it from filed to OWED."  This is that probe.  The row is moved to OWED in the
#  same commit -- a criterion that fires and is ignored is worse than one never written,
#  because the next reader trusts it.
#
#  It is wired HERE anyway, and deliberately: the split is a harness round owing its own
#  controls, and holding a HIGH device fix hostage to a gate refactor would be the tail
#  wagging the dog.  What is NOT acceptable is compounding it silently.
DEWLOG=$LOGDIR/sgi_de_width.log
python3 sgi_de_width_probe.py "$PMAX" gate > "$DEWLOG" 2>&1 || true

#  SENTINEL FIRST -- a preserved log is verified by its completion sentinel, never by its
#  existence.  A killed run loses every row and looks exactly like one that produced none.
if ! grep -q "OPUS498T_DONE" "$DEWLOG"; then
    note "sgi_de width probe did not reach its completion sentinel; last lines follow"
    tail -5 "$DEWLOG" | sed 's/^/       /'
    check "sgi_de width probe completed" "no" "yes"
else
    check "sgi_de width probe completed" "yes" "yes"

    #  CONTROLS BY NAME.  A detector whose liveness and device-signature rows are dead
    #  scores well on a corpse: every access row would read "no message" and pass.
    check "sgi_de controls live+devsig" \
          "$(grep -q 'OPUS498T_CONTROL=OK' "$DEWLOG" && echo yes || echo no)" "yes"

    #  PER-ROW PASS, one line, checked individually.  A row that silently stops being
    #  tested is the padded-column class -- a name as long as its column makes the check
    #  unsatisfiable and the row quietly stops being tested.
    #  *** `tail_acc_x' PINS A HOST DEATH ON PURPOSE AND WILL GO RED BY SUCCEEDING. ***
    #  It observes `sgideprimop' -- an accepted-width access with startFlag reaches
    #  draw_primitive(), whose default arm is fatal on 254 of 256 top-byte op classes,
    #  two of which (POINT 0x00, TRIANGLE 0x02) are DOCUMENTED primitives.
    #
    #  *** THE BLAST RADIUS HAS THREE TIERS, NOT ONE, AND THIS NOTE SAID `BOTH ROWS' UNTIL
    #  2026-08-31.  Corrected after the grok seat read the oracles against the code paths
    #  they exercise and found the overstatement. ***
    #
    #    tail_acc_x            CERTAIN red -- wants exit1, and the fix removes the death.
    #    tail_acc              CONDITIONAL -- it counts the DRAW message SUBSTRING and
    #                          wants 1.  A fix that LATCHES the text without REWORDING it
    #                          still prints the first occurrence, so the row stays GREEN.
    #                          It reds only if the message is reworded.
    #    hi_draw, hi_rd_draw   NEITHER red NOR safe.  Both want count(DRAW) == 0, so a
    #                          REWORD leaves them green because the string no longer
    #                          exists -- GREEN FOR THE WRONG REASON, i.e. VACUOUS BY
    #                          CONSTRUCTION.  A reword silently blinds them; it does not
    #                          fail them, and nothing would say so.
    #
    #  *** SO THE DESIGN CONSTRAINT IS: KEEP THE MESSAGE TEXT AND ADD `(once)'. ***  That
    #  costs ONE oracle re-pin (tail_acc_x).  Rewording costs two re-pins AND silently
    #  blinds two further rows -- which is the worse half and is invisible to any gate.
    #  *** AND THE OBVIOUS RE-PIN IS A TRAP.  DO NOT RE-PIN `tail_acc_x' ONTO `"exit0"'. ***
    #  Adjudicated 2026-08-31 by the flagship seat, which traced the channel rather than the
    #  intent.  The row wants `exit1' today; the natural correction is `exit0' ("the host now
    #  survives").  Trace what that oracle can see:
    #
    #    a future one-token death reinstatement -- `exit(0)' at the default arm instead of
    #    `exit(1)' -- prints the announce once and then DIES.  `how' is then "exit0", so a
    #    re-pinned tail_acc_x reads GREEN; `tail_acc' still counts its one message, GREEN;
    #    and no other session reaches draw_primitive() at all.  TOTAL ESCAPE, 29/29.
    #
    #  So the re-pin would MINT, at the exact site being fixed, the exact blindness the queue
    #  row `exit0oracle' was filed to describe: EXIT STATUS CANNOT VARY between `declined and
    #  then quit' and `died with status 0'.  That is knowable at WRITING time from the CHANNEL
    #  check -- name the mutant a row kills and the observable that differs under it -- and it
    #  is why that check is run before the table, not after.
    #
    #  RE-PIN ONTO A POSITIVE POST-DRAW OBSERVABLE INSTEAD: extend the session with a load
    #  through the device and assert the VALUE (`printed()' already exists in the probe and
    #  reads "died" when the host is gone).  An exit-status row may stay as a SECOND channel;
    #  the value row is the load-bearing one.  This is L1 -- a row under construction -- so
    #  there is no stopping-rule tension in fixing it in-round.
    #
    #  The fixing round therefore owes a FOURTH mutant beside the three already enumerated:
    #  death-by-`exit(0)' at the default arm, which the re-pinned row must kill.
    #
    #  Oracle-correction ordering applies -- re-pin FIRST, measure the committed build red,
    #  THEN edit.  Without this note the red reads as a regression in THIS device.
    for v in "live" "devsig" "lo_kill" "lo_decl" "lo_alive" "lo_sent" "lo_latch" "lo_kill2" "lo_decl2" "lo_alive2" "lo_sent2" "hi_draw" "hi_alive" "hi_rd_draw" "hi_rd_alive" "hi_rd_sent" "two_widths_n" "two_widths_1" "two_widths_2" "dec_switch" "hi_kill" "tail_acc" "tail_acc_x" "tail_acc_h" "acc4_last" "acc8_hi32" "acc8_lo32" "acc8_read" "re_first" "sharedlatch"; do
        check "sgi_de row: $v" "$(count "$DEWLOG" "^$v  .*ok$")" "1"
    done

    #  DENOMINATOR, SUMMED ARITHMETICALLY.  Two rows, not one: a single "22 ok" check
    #  cannot tell a LOST row from a FAILING one, and those need different responses.
    #  The sum is arithmetic rather than a string join -- concatenating two counts and
    #  comparing to "220" is satisfied by (22 ok, 0 FAIL) AND by (2 ok, 20 FAIL), which
    #  is a defect this gate has already shipped once.
    check "sgi_de rows emitted" \
          "$(( $(count "$DEWLOG" " ok$") + $(count "$DEWLOG" " FAIL$") ))" "30"
    check "sgi_de rows green" "$(count "$DEWLOG" " ok$")" "30"
fi

SGILOG=$LOGDIR/sgi_re_width.log
python3 sgi_re_width_probe.py "$PMAX" gate > "$SGILOG" 2>&1 || true

#  SENTINEL FIRST.  A preserved log is verified by its completion sentinel, never by its
#  existence: a killed run loses every row and looks exactly like a run that produced none.
if ! grep -q "OPUS497T_DONE" "$SGILOG"; then
    note "sgi_re width probe did not reach its completion sentinel; last lines follow"
    tail -5 "$SGILOG" | sed 's/^/       /'
    check "sgi_re width probe completed" "no" "yes"
else
    grep -E " ok$| FAIL$" "$SGILOG" | sed 's/^/       /'

    #  CONTROLS BY NAME, not by count.  A green-row total lets a control go red while the
    #  sum stays acceptable -- and a run whose controls died is an APPARATUS failure, which
    #  must not be read as a wall of product failures.
    for c in "live" "live64" "devsig stat"; do
        check "sgi_re control: $c" "$(count "$SGILOG" "^$c  .*ok$")" "1"
    done
    check "sgi_re controls live" \
          "$(grep -q 'OPUS497T_CONTROL=OK' "$SGILOG" && echo yes || echo no)" "yes"

    #  PER-ROW PASS.  Checked individually rather than by a total, because a row that
    #  silently stops being tested is the padded-column class: a name as long as its column
    #  makes a check UNSATISFIABLE and the row quietly stops being tested.
    #  The list is ONE LINE on purpose -- a backslash-continued list assembled through
    #  nested quoting once gained a bogus word `n` and shipped a RED gate.
    for v in "live" "devsig stat" "tlb_a sw surv" "tlb_a sw lat1" "tlb_a lw surv" "tlb_a accept" "tlb_b sw surv" "tlb_b sw lat1" "tlb_b lw surv" "tlb_b accept" "tlb_c sw surv" "tlb_c sw lat1" "tlb_c lw surv" "tlb_c accept" "tex sw surv" "tex sw lat1" "tex lw surv" "tex accept" "linear_a sw surv" "linear_a sw lat1" "linear_a lw surv" "linear_a accept" "linear_b sw surv" "linear_b sw lat1" "linear_b lw surv" "linear_b accept" "xsite 6msg" "xsite order" "other decl" "live64" "tlb_a ld lo" "tlb_a ld hi" "tlb_b ld lo" "tlb_b ld hi" "tlb_c ld lo" "tlb_c ld hi" "linear_a ld lo" "linear_a ld hi" "linear_b ld lo" "linear_b ld hi" "tex ld lo" "tex ld hi" "tex rd lat1" "tex xbit" "tex/unmap" "unmap/tex"; do
        check "sgi_re row: $v" "$(count "$SGILOG" "^$v  .*ok$")" "1"
    done

    #  DENOMINATOR PINNED TO A LITERAL.  A detector that loses rows must not be able to pass
    #  by shrinking, and the count is the only thing that says so.  Raise it DELIBERATELY.
    #  Both halves pinned: 46 rows emitted AND all 46 green.
    #  *** RAISED 44 -> 46 ON THIS ROUND'S OWN PASS 2. ***  The panel found a clause-(d)
    #  floor breach: giving the TEX read decline an already-used NON-LEN latch bit
    #  (1 << 8 = SGIRE_W_UNMAP_RD) escapes a 44/44 sweep, because the detector's four
    #  TEX-read scenarios and its unmapped-read scenario never share an emulator instance
    #  -- `tex xbit' set bits 0-5 only AT THAT TIME (it now fires 0-10).  Repaired by two
    #  SAME-INSTANCE rows asserting both
    #  announces fire, in BOTH orderings; one ordering would leave the mirror open.
    #  *** RAISED 35 -> 44 BY #513, DELIBERATELY, IN THE SAME COMMIT AS THE FIX. ***
    #  The six `<arm> ld kill' rows are GONE -- they asserted that a len == 8 READ still
    #  ends the host at each window, which was true until #513 removed those kills.  They
    #  are replaced by TWO anchored ACCEPT rows per accepting arm (window base AND last
    #  slot, because a row at the base tests the near bound twice and the far bound never),
    #  four CRIME_RE_TEX decline rows, and a 64-bit liveness control.  Arithmetic:
    #  35 - 6 + 14 + 1 = 44.  Two rows rather than one,
    #  because a single "35 ok" check cannot tell a LOST row from a FAILING one -- and
    #  those need different responses.
    #  *** THE FIRST DRAFT OF THIS BLOCK HAD TWO DEFECTS, BOTH FOUND BY THE PASS-2 SEAT.
    #  (1) It ended in `|| true`, which is INERT: check() in lib.sh has no `return`, so
    #  it exits 0 on BOTH branches and the row counts into _fails regardless.  The
    #  suppression never existed -- but a reader would conclude that row was advisory,
    #  which is worse than either behaviour on its own.
    #  (2) The denominator concatenated two counts and compared to "350" -- satisfied by
    #  (35 ok, 0 FAIL) AND by (3 ok, 50 FAIL).  A string join is not an arithmetic
    #  identity, and it was redundant with the two rows below it anyway. ***
    #  *** AND THE FIRST REPAIR OF (2) REPRODUCED THE VERY DEFECT THE PANEL HAD JUST FOUND
    #  IN THIS ROUND'S BRIEF.  I wrote `count "$SGILOG" " ok$| FAIL$"` -- but count() is
    #  `grep -ac`, PLAIN grep, so `|` is a LITERAL and the pattern matches NOTHING.
    #  Measured: 0 against a log holding 35 rows.  The seats had flagged `grep -i
    #  'sgi|width'` in the brief for exactly this, one hour earlier. ***
    #
    #  Summed ARITHMETICALLY instead, which needs no regex dialect at all -- and unlike the
    #  string-concatenation form it replaces, it cannot be satisfied by (3 ok, 50 FAIL).
    check "sgi_re rows emitted" \
          "$(( $(count "$SGILOG" " ok$") + $(count "$SGILOG" " FAIL$") ))" "46"
    check "sgi_re rows green"   "$(count "$SGILOG" " ok$")"   "46"
    check "sgi_re rows red"     "$(count "$SGILOG" " FAIL$")" "0"

fi

#  ---- *** MOVED OUT ONE NESTING LEVEL, 2026-08-31.  It was pasted INSIDE the
#  ---- sgi_re_width probe's success branch, so if THAT probe missed its sentinel this
#  ---- block was never invoked at all -- 28 rows, three denominators and its own
#  ---- sentinel check evaporating while the gate reported one red row about a
#  ---- different probe.  Silent coverage loss, and it defeated the very sentence
#  ---- that justified the block (a committed detector no gate runs is a wrong
#  ---- record).  Both sibling blocks sit at depth 0; the block's own zero
#  ---- indentation was the tell that it had been written top-level and pasted
#  ---- into a branch.  Found by the #499 pass-2 seat walking the brace depth. ***
#  ---- #499's detector for the unmatched-address catch-all.  Wired IN THE SAME COMMIT as
#  ---- the fix: a committed detector that no gate runs is a wrong record under the vacuity
#  ---- floor's contract clause, and this one measured 18/28 on the pre-fix build and 28/28
#  ---- on the fix, so it carries its own test-first evidence.
#  ---- the coordinator's file.  Modelled on the sgi_re_width_probe block -- find it
#  ---- with `grep -n 'sgi_re_width_probe.py "$PMAX"' gate_arm.sh`, NOT by line
#  ---- number: the original citation said :1131, which is inside the sgi_de comment,
#  ---- and this block has since moved once already.  A same-file line citation is
#  ---- invalidated by your own edits to that file.
UNMLOG=$LOGDIR/sgi_re_unmapped.log
python3 sgi_re_unmapped_probe.py "$PMAX" gate > "$UNMLOG" 2>&1 || true

#  SENTINEL FIRST.  A preserved log is verified by its completion sentinel, never by its
#  existence: a killed run loses every row and looks exactly like a run that produced none.
if ! grep -q "OPUS499T_DONE" "$UNMLOG"; then
    check "sgi_re unmapped probe completed" "no" "yes"
else
    check "sgi_re unmapped probe completed" "yes" "yes"
    check "sgi_re unmapped controls" "$(count "$UNMLOG" '^OPUS499T_CONTROL=OK$')" "1"
    for v in "live" "devsig" "wr surv" "wr kill" "wr decl" "rd surv" "rd kill" "rd decl" "rd sent" "rd nodbe" "wr lat1" "rd lat1" "wr rd 2msg" "xwin7 pre" "xwin wr" "xwin rd" "tlba acc lo" "tlba acc hi" "tlbb acc lo" "tlbb acc hi" "tlbc acc lo" "tlbc acc hi" "tex acc lo" "tex acc hi" "lina acc lo" "lina acc hi" "linb acc lo" "linb acc hi" "wr narrow surv" "wr narrow decl" "rd narrow surv" "rd narrow sent" "clip surv" "clip decl" "clip nar surv" "clip nar decl" "clip rd surv" "clip rd decl" "clip rd sent" "clip rdn surv" "clip rdn decl" "cliphi rd surv" "cliphi rd decl" "cliphi wr surv" "cliphi wr decl" "rd narrow decl" "wr zero surv" "wr zero decl" "wr then live" "clip wr live"; do
        check "sgi_re unmapped row: $v" "$(count "$UNMLOG" "^$v  .*ok$")" "1"
    done

    #  DENOMINATOR, SUMMED ARITHMETICALLY -- two rows, not one: a single "28 ok" check
    #  cannot tell a LOST row from a FAILING one, and those need different responses.
    check "sgi_re unmapped rows emitted" \
          "$(( $(count "$UNMLOG" " ok$") + $(count "$UNMLOG" " FAIL$") ))" "50"
    check "sgi_re unmapped rows green" "$(count "$UNMLOG" " ok$")"   "50"
    check "sgi_re unmapped rows red"   "$(count "$UNMLOG" " FAIL$")" "0"
fi

#  ---- sgirandompixel: horrible_getputpixel()'s unimplemented-mode arm.
#
#  WHAT THIS PROTECTS.  That arm used to do `*color = random()' with its exit(1) commented out, so a failed
#  pixel GET handed the CALLER a random value and draw_primitive() wrote it to the destination in the same
#  loop iteration.  DE_MODE_LIN_B (0x1400) is one of the FIVE modes crmfbreg.h documents and extracts to
#  tlb_mode 5, so it was reachable with a DOCUMENTED mode.  Now declined, with a latched announce.
#
#  The probe is BOTH the rung-3 WITNESS (7/8 red on the pre-fix build under the re-pinned oracle, preserved as
#  artifacts/sgirandompixel/witness_20260906/prefix_repinned_RED.out) and the DETECTOR (kill table in
#  artifacts/sgirandompixel/killtable/: five mutants, all killed, BASE 8/8 opening and closing).
#
#  `lin_b diag once' IS THE ROW THAT NEEDED THE MOST CARE and the reason the probe draws a 1x4 rectangle
#  rather than a single pixel: with one pixel an UNLATCHED announce also fires exactly once, the count channel
#  cannot vary, and M_NOLATCH escaped 8/8.  Height rather than width, because LIN_A addressing is
#  `ofs = x & 4095' -- y is ignored, so four rows rewrite one byte and the VALUE oracle survives.
RANDLOG=$LOGDIR/sgi_re_randompixel.log
python3 sgi_re_randompixel_probe.py "$PMAX" gate > "$RANDLOG" 2>&1 || true

if ! grep -q "SGIRAND_DONE" "$RANDLOG"; then
    check "sgi_re randompixel probe completed" "no" "yes"
else
    check "sgi_re randompixel probe completed" "yes" "yes"
    check "sgi_re randompixel witness verdict" "$(count "$RANDLOG" '^SGIRAND_WITNESS=PASS$')" "1"
    #  TWO SPACES AFTER $v, NOT ONE -- the sibling block above uses the same idiom and this block did not,
    #  which the gate caught on its first run: `lin_b diag' got=2, because `^lin_b diag .*ok$' also matches
    #  the row `lin_b diag once'.  That is the padded-column trap in its MATCHES-TWO-ROWS direction.
    #
    #  The probe prints names with "%-16s" followed by an explicit space, so a name of N chars is followed
    #  by (16-N)+1 spaces.  The longest name here is `lin_b diag once' at 15, leaving exactly two -- so this
    #  pattern has ONE CHARACTER of margin.  If a name must grow past 15, widen the probe's "%-16s"
    #  in the same diff.
    #
    #  *** CORRECTED 2026-09-07 (#505 pass 2, the kimi substitute).  This used to say a name of 16 or
    #  more makes the pattern "UNSATISFIABLE, which is the same trap in its other, SILENT direction:
    #  the check stops testing anything and stays green."  THE SILENT PART IS FALSE. ***  `count'
    #  returns 0, `check' compares 0 against the wanted "1", and 0 != 1 FAILS -- loudly.  Measured
    #  over rendered rows at lengths 15/16/17.  An unsatisfiable pattern is silent only where a check
    #  wants ZERO, which no row check here does.  The dangerous direction is the ONE-SPACE form,
    #  which matched `lin_b diag once' from `lin_b diag' and is what this block was written for.
    for v in "live" "devsig" "copy lin_a" "lin_b not src" "lin_b is fg" "lin_b alive" "lin_b diag" "lin_b diag once"; do
        check "sgi_re randompixel row: $v" "$(count "$RANDLOG" "^$v  .*ok$")" "1"
    done

    #  DENOMINATOR, SUMMED ARITHMETICALLY -- two rows, not one, for the sibling block's reason.
    check "sgi_re randompixel rows emitted" \
          "$(( $(count "$RANDLOG" " ok$") + $(count "$RANDLOG" " FAIL$") ))" "8"
    check "sgi_re randompixel rows green" "$(count "$RANDLOG" " ok$")"   "8"
    check "sgi_re randompixel rows red"   "$(count "$RANDLOG" " FAIL$")" "0"
fi

#  ---- #519 sgirandomcolour: the PUT-side twin of the block above.  The COLOUR-mode default arm
#  wrote four random() bytes into guest memory, reachable with the documented DE_MODE_TYPE_YCRCB; it
#  now declines the store with a latched announce.  The probe's controlling CONTRACT names its
#  projection -- {TLB_A, TLB_B, TLB_C, LIN_A} x {bufdepth 1,2,4,8} x {latch clear, set on entry}, all
#  32 cells occupied -- and kill table 5 (artifacts/sgirandomcolour/killtable5_20260912/SCORES.txt)
#  measured 15 legs, every one on its pre-registered prediction: BASE 89/89, HEAD 28/89, eleven
#  single-cell zero-store controls 88/89 each on its OWN row, NIB_OTHER 78/89, TAIL8 81/89.
#  PARSE BEFORE SCORE: the RESULT and DONE lines must each appear exactly once and be well formed.
#  The denominator is a LITERAL -- a pin that follows the probe cannot tell gained rows from lost ones.
COLLOG=$LOGDIR/sgi_re_colourdefault.log
python3 sgi_re_colourdefault_probe.py "$PMAX" gate > "$COLLOG" 2>&1 || true
colres=$(grep -c '^SGICOLOUR_RESULT=' "$COLLOG")
colresok=$(grep -cE '^SGICOLOUR_RESULT=[0-9]+/[0-9]+$' "$COLLOG")
coldone=$(grep -cx 'SGICOLOUR_DONE' "$COLLOG")
if [ "$colres" = 1 ] && [ "$colresok" = 1 ] && [ "$coldone" = 1 ]; then
    check "sgi_re colourdefault protocol parsed" "yes" "yes"
    #  `live' is the liveness control: a supported RGBA PUT lands its colour.  Two spaces after the
    #  name, the padded-column idiom above -- `live silent' must not match `live'.
    check "sgi_re colourdefault liveness row" "$(count "$COLLOG" "^live  .*ok$")" "1"
    col=$(grep '^SGICOLOUR_RESULT=' "$COLLOG" | cut -d= -f2)
    check "sgi_re colourdefault rows run"     "${col#*/}" 89
    check "sgi_re colourdefault rows correct" "${col%/*}" 89
else
    note "sgi_re colourdefault: protocol lines missing or duplicated (result=$colres/$colresok done=$coldone)"
    tail -5 "$COLLOG" | sed 's/^/       /'
    check "sgi_re colourdefault protocol parsed" "no" "yes"
fi

#  ------------------------------------------------------------ #505 sgirergbroundtrip
#  horrible_getputpixel()'s RGB GET read buf[1..3] while its RGB PUT writes the three channels at
#  buf[0..2] and an explicit pad at buf[3] -- so an RGB pixel did not survive its own round trip and
#  the red channel was dropped.  RGB was the ONLY 32-bit colour mode in the file failing this way.
#
#  THE ARM WAS CHOSEN ON EVIDENCE FROM A DIFFERENT DEVICE, which is what makes the warrant
#  non-circular: dev_sgi_gbe.c's scanout reads the same tile memory back as
#  (buf[0]<<24)+(buf[1]<<16)+(buf[2]<<8)+buf[3], and CRMFB_MODE_TYP_RGB8 takes R,G,B from bits
#  31..24 / 23..16 / 15..8 -- byte 0 is R and byte 3 is UNUSED.  The pad sits at buf[3] because the
#  CONSUMER ignores buf[3], not because PUT writes a zero there.
#
#  `rgb depth64' IS NOT DECORATION -- IT CLOSES A MEASURED CLAUSE-(d) FLOOR BREACH.  The first kill
#  table's M6_cond (guard kept, repair conditioned on `bufdepth == 4') scored a CLEAN SWEEP 6/6,
#  because every session then used BUFDEPTH_32 and the mutant's fix branch was the only one the
#  detector ever executed.  Its mirror M7_cond8 (exempting bufdepth 8 instead) also dies, so the
#  WIDTH AXIS is closed rather than the one cell the mutant happened to use.
#
#  `rgb samemode' reaches the RGB *PUT* arm, which no other row executes -- every other session is
#  RGB->RGBA.  Measured, not assumed: M8_put corrupts that arm alone and reds exactly this row.
RGBLOG=$LOGDIR/sgi_re_rgb.log
python3 sgi_re_rgb_probe.py "$PMAX" gate > "$RGBLOG" 2>&1 || true

if ! grep -q "SGIRGB_DONE" "$RGBLOG"; then
    check "sgi_re rgb probe completed" "no" "yes"
else
    check "sgi_re rgb probe completed" "yes" "yes"
    check "sgi_re rgb witness verdict" "$(count "$RGBLOG" '^SGIRGB_WITNESS=PASS$')" "1"
    #  TWO SPACES AFTER $v, NOT ONE -- the sibling blocks above were both bitten by the one-space
    #  form, in both of its directions.  Pre-flighted mechanically for this row set before the gate
    #  ever ran: no name is a prefix of another, and every pattern matches exactly one rendered row.
    #
    #  The probe prints names with "%-16s" plus an explicit space, so a name of N chars is followed
    #  by (16-N)+1 spaces.  The longest here is `rgb not corrupt' at 15, leaving exactly two -- ONE
    #  CHARACTER of margin.  If a name must grow past 15, widen the probe's "%-16s" in the same diff.
    #
    #  *** WHAT A TOO-LONG NAME ACTUALLY DOES: IT REDS, LOUDLY.  The sibling block above says it
    #  "silently stops testing anything while staying green", and an earlier draft of THIS block
    #  copied that sentence.  It is WRONG, and the pass-2 panel caught it. ***  `count' returns 0
    #  when the pattern matches nothing, `check' compares that 0 against a wanted "1", and 0 != 1
    #  FAILS.  Measured over rendered rows at lengths 15/16/17: 15 matches (ok), 16 and 17 match
    #  nothing (FAIL).  The UNSATISFIABLE direction of this trap is the SAFE one for a want-1 check;
    #  it is only silent where a check wants ZERO.  The genuinely dangerous direction remains the
    #  ONE-SPACE form, which matches a LONGER name's row as well and was measured on the sibling.
    for v in "live" "devsig" "copy lin_a" "rgb chan" "rgb not corrupt" "rgb alive" "rgb samemode" "rgb depth64" "rgb tiled" "rgb tiled64"; do
        check "sgi_re rgb row: $v" "$(count "$RGBLOG" "^$v  .*ok$")" "1"
    done

    #  DENOMINATOR, SUMMED ARITHMETICALLY: a row that stops being emitted at all is otherwise
    #  invisible -- its named check goes 0, but so does a check for a row that never existed.
    #  *** THE DENOMINATOR PINNED 8 WHILE THE PROBE EMITTED 9, AND THE ROW LIST NEVER NAMED
    #  `rgb tiled'.  A pass-3 seat found it by reading the gate against the probe rather than the
    #  probe against itself. ***  It would have failed LOUDLY -- emitted 9, wanted 8 -- which is the
    #  safe direction, but it would have shipped, and `rgb tiled' would have been unchecked BY NAME
    #  while appearing in the count.  Both new rows are named above and the pins are 10.
    check "sgi_re rgb rows emitted" \
          "$(( $(count "$RGBLOG" " ok$") + $(count "$RGBLOG" " FAIL$") ))" "10"
    check "sgi_re rgb rows green" "$(count "$RGBLOG" " ok$")"   "10"
    check "sgi_re rgb rows red"   "$(count "$RGBLOG" " FAIL$")" "0"
fi

#  ------------------------------------------------------------ #500 sgideprimop
#  draw_primitive()'s default arm ended the host on a guest-written drawing op.
#  Now a latched decline.  The detector is its OWN probe rather than rows bolted
#  onto sgi_de_width_probe.py, because that one is about WIDTH and owns the
#  `tail_acc*' rows that pin draw_primitive's REACHABILITY -- a different claim.
PRIMLOG=$LOGDIR/sgi_de_primop.log
python3 sgi_de_primop_probe.py "$PMAX" gate > "$PRIMLOG" 2>&1 || true

#  SENTINEL FIRST, for the reason the sibling block states: a preserved log is
#  verified by its completion sentinel, never by its existence.
if ! grep -q "OPUS500_DONE" "$PRIMLOG"; then
    check "sgi_de primop probe completed" "no" "yes"
else
    check "sgi_de primop probe completed" "yes" "yes"
    for v in "live" "devsig" "pt surv" "pt live" "pt decl" "tri surv" "tri live" "tri decl" "reset surv" "reset live" "reset decl" "two once" "two live" "rd surv" "rd decl" "xlatch decl" "xlatch live" "xlatch unm" "xlatch unliv" "xlatch all" "xlatch alliv" "xlatch pre" "acc rect" "acc live" "acc rect mod" "acc rect liv" "acc line mod" "acc line liv" "n25 nox" "n25 noxset" "dec b26" "dec b27" "dec b28" "dec b29" "dec b30" "dec b31" "dec hi liv" "dec low" "dec low liv" "dec ops" "dec ops liv" "dec flood" "dec flood liv" "dec regs" "dec regs liv" "dec regs set" "dec regs stip" "n25 rect" "n25 rectliv" "n25 rectset" "n25 line"; do
        check "sgi_de primop row: $v" "$(count "$PRIMLOG" "^$v  .*ok$")" "1"
    done

    #  DENOMINATOR, SUMMED -- a single "19 ok" check cannot tell a LOST row from a
    #  FAILING one, and those need different responses.
    check "sgi_de primop rows emitted"           "$(( $(count "$PRIMLOG" " ok$") + $(count "$PRIMLOG" " FAIL$") ))" "51"
    check "sgi_de primop rows green" "$(count "$PRIMLOG" " ok$")"   "51"
    check "sgi_de primop rows red"   "$(count "$PRIMLOG" " FAIL$")" "0"
fi



#  ------------------------------------------------------------ pcc2widthkills
#  Twelve width-guard blocks in DEVICE_ACCESS(pcc2) ended the host on a guest-chosen
#  access width.  Now a DIRECTION SPLIT: reads accept (the memcpy above the switch
#  already served them), writes decline with a per-instance latch.  The witness
#  (pcc2_width_witness.py, 4/10 on the committed build) is NOT run here -- its job was
#  to exist before the edit; this is the detector it grew into.
PCC2LOG=$LOGDIR/pcc2_width.log
python3 -u pcc2_width_probe.py "$PMAX" gate > "$PCC2LOG" 2>&1 || true

#  SENTINEL FIRST: a preserved log is verified by its completion sentinel, never by
#  its existence.
if ! grep -q "PCC2W_PROBE_DONE" "$PCC2LOG"; then
    check "pcc2 width probe completed" "no" "yes"
else
    check "pcc2 width probe completed" "yes" "yes"
    for v in "live" "devsig" "byte rd" "byte rd liv" "hrd genctl" "hrd genctl lv" "hrd genctl nod" "hwr genctl" "hwr genctl lv" "hrd t2ctl" "hrd t2ctl lv" "hrd t2ctl nod" "hwr t2ctl" "hwr t2ctl lv" "hrd t2icr" "hrd t2icr lv" "hrd t2icr nod" "hwr t2icr" "hwr t2icr lv" "hrd sccerr" "hrd sccerr lv" "hrd sccerr nod" "hwr sccerr" "hwr sccerr lv" "hrd scctx" "hrd scctx lv" "hrd scctx nod" "hwr scctx" "hwr scctx lv" "wrd sccerr" "wrd sccerr lv" "wrd sccerr nod" "wwr sccerr" "wwr sccerr lv" "wwr sccerr dcl" "val h genctl" "val w sccerr" "rb genctl" "rb genctl dcl" "rb vecbase" "rb t2ctl" "rb t2ctl dcl" "rb t2icr" "rb t2icr dcl" "rb scctx" "rb scctx dcl" "hwr sccerr dcl" "rb genctl lo" "latch same" "latch two" "latch aba" "latch same2" "rb2 genctl" "rb2 t2ctl" "rb2 t2icr" "rb2 scctx" "rb2 vecbase" "rb2 sccicr" "rb2 sccrx" "rb2 scsiicr" "rb2 mask" "pscale noig2" "ipl noig2" "hrd genctl rb" "hrd t2ctl rb" "hrd t2icr rb" "hrd scctx rb" "hrd ipl noro" "brd2 genctl" "brd2 vecbase" "brd2 t2ctl" "brd2 t2icr" "brd2 sccicr" "brd2 scctx" "brd2 sccrx" "brd2 scsiicr" "brd2 mask" "brd pscale noig" "brd ipl noro" "rb4 genctl" "rb8 genctl" "rb4 vecbase" "rbq vecbase" "rb8 vecbase" "rb4 t2ctl" "rb8 t2ctl" "rb4 t2icr" "rb8 t2icr" "rb4 sccicr" "rbq sccicr" "rb8 sccicr" "rb4 scctx" "rbq scctx" "rb8 scctx" "rb4 sccrx" "rbq sccrx" "rb8 sccrx" "rb4 scsiicr" "rbq scsiicr" "rb8 scsiicr" "rb4 mask" "rb8 mask" "pscale noig4" "pscale noig8" "ipl noig4" "ipl noig8" "latch samew" "latch samed" "latch all one" "pend2 arm" "pend2 decl" "pend2 rb" "pend2 rbi" "pend2 rb1" "pend2 rb1i" "pend2 rbc" "pend2 rbh" "pend2 rb1c" "pend2 rb1h" "pend2 huh" "pend2 zctl" "pend2 rbz" "pend1 arm" "pend1 decl" "pend1 rb" "pend1 rbi" "pend1 rb2" "pend1 rb2i" "pend1 rbc" "pend1 rbh" "pend1 rb2c" "pend1 rb2h" "pend1 huh" "pend1 zctl" "pend1 rbz" "ovf2 arm" "ovf2 decl" "ovf2 rb" "ovf2 rbv" "ovf2 rbx" "ovf2 rb1" "ovf2 rb1v" "ovf2 rb1x" "ovf2 huh" "ovf1 arm" "ovf1 decl" "ovf1 rb" "ovf1 rbv" "ovf1 rbx" "ovf1 rb2" "ovf1 rb2v" "ovf1 rb2x" "ovf1 huh" "ipl wset" "ovfhi2 arm" "ovfhi2 decl" "ovfhi2 rb" "ovfhi2 rbv" "ovfhi2 rbx" "ovfhi2 rb1" "ovfhi2 rb1v" "ovfhi2 rb1x" "ovfhi2 huh" "ovfhi1 arm" "ovfhi1 decl" "ovfhi1 rb" "ovfhi1 rbv" "ovfhi1 rbx" "ovfhi1 rb2" "ovfhi1 rb2v" "ovfhi1 rb2x" "ovfhi1 huh" "pendn2 arm" "pendn2 decl" "pendn2 rb" "pendn1 arm" "pendn1 decl" "pendn1 rb" "latch all zero" "rb t2icr il4" "rb t1icr il4" "ipl rset" "latch all rev" "pendboth arm" "pendboth arm1" "pendboth decl" "pendboth rb" "pendboth rbi" "pendboth rb1" "pendboth rb1i" "pendboth rbc" "pendboth rbh" "pendboth rb1c" "pendboth rb1h" "pendboth huh" "rb t2ctl b27" "rb t1ctl b27" "rb4 t1ctl" "rb8 t1ctl" "rb4 t1icr" "rb8 t1icr" "latch all" "latch all lv" "latch all fail" "acc genctl" "acc genctl nod" "acc t2ctl" "acc t2ctl nod" "acc t2icr" "acc t2icr nod" "acc scctx" "acc scctx nod" "acc sccerr" "acc sccerr nod" "op vecbase" "op vecbase dcl" "op pscale" "op pscale dcl" "op t1ctl" "op t1ctl dcl" "op t1icr" "op t1icr dcl" "op sccicr" "op sccicr dcl" "op sccrx" "op sccrx dcl" "op scsiicr" "op scsiicr dcl" "rb sccicr" "rb sccrx" "rb scsiicr" "op pscale noig" "rb vecbase own" "hwr ipl noig" "latch all w" "latch all d" "acc all" "acc all lv" "acc pscale ign" "acc ipl ro" "rb t1ctl" "rb t1icr" "hrd ipl" "hrd ipl lv" "hrd ipl nod" "hwr ipl" "hwr ipl lv" "hwr ipl dcl" "op mask" "op mask dcl" "rb mask"; do
        check "pcc2 width row: $v" "$(count "$PCC2LOG" "^$v  .*ok$")" "1"
    done

    #  DENOMINATOR, SUMMED -- a lost row and a failing row need different responses.
    check "pcc2 width rows emitted"           "$(( $(count "$PCC2LOG" " ok$") + $(count "$PCC2LOG" " FAIL$") ))" "251"
    check "pcc2 width rows green" "$(count "$PCC2LOG" " ok$")"   "251"
    check "pcc2 width rows red"   "$(count "$PCC2LOG" " FAIL$")" "0"
fi


#  ------------------------------------------------------------ pcc2defaultkill (#501)
#  The default: arm of DEVICE_ACCESS(pcc2) ended the host on any access to an uncased
#  offset, reads included.  Now: reads keep the served byte, writes are declined, one
#  latched announce per offset per instance.  The witness (regress/artifacts/pcc2defaultkill/
#  witness_20260905/, 7/13 on the committed build) is NOT run here; this is its detector.
PCC2DLOG=$LOGDIR/pcc2_default.log
python3 -u pcc2_default_probe.py "$PMAX" gate > "$PCC2DLOG" 2>&1 || true
if ! grep -q "PCC2D_PROBE_DONE" "$PCC2DLOG"; then
    check "pcc2 default probe completed" "no" "yes"
else
    check "pcc2 default probe completed" "yes" "yes"
    for v in "live" "devsig chipid" "named wr" "named wr msg" "named rd" "named rd msg" \
        "named rd srvd" "inword wr" "inword msg" "inword rdawr" "inword rd" "unnamed wr" \
        "unnamed msg" "unnamed rdawr" "unnamed rd" "ieicr rdawr" "ieerr rdawr" "sccerr rdawr" \
        "latch sameoff" "sameoff val" "latch twooff" "latch rw one" "latch rd rd" "latch rd wr" \
        "latch aba" "alias 0x6a" "alias msg" "dir wr text" "wr declined" "wr val text" \
        "dir rd text" "srvd val" "srvd val text" "srvd half text" "half wr rdawr" "srvd rd latch" \
        "srvd wr latch" "wide wr" "wide wr msg" "wide wr val" "wide rd" "wide rd srvd" \
        "genctl rt" "t1cmp word rt" "put b ctl" "put b ctl msg"; do
        check "pcc2 default row: $v" "$(count "$PCC2DLOG" "^$v  .*ok$")" "1"
    done
    check "pcc2 default rows emitted" "$(( $(count "$PCC2DLOG" " ok$") + $(count "$PCC2DLOG" " FAIL$") ))" "46"
    check "pcc2 default rows green"   "$(count "$PCC2DLOG" " ok$")"   "46"
    check "pcc2 default rows red"     "$(count "$PCC2DLOG" " FAIL$")" "0"
fi

#  ------------------------------------------------------------ pcc2c040kill (#512) + #535
#  One legal guest st.b of 0x04 to PCC2 GENCTL ran reassert_interrupts() and ended the host (#512,
#  9fa07fe).  This detector shipped in NO GATE (wiringcliff) -- so its 16 rows defended nothing --
#  and a late seat MEASURED an L2 in it: an announce gated on !MIEN scored 16/16 (#535 adds
#  `c040 says mien' and, after its pass 2 measured count x MIEN, `c040 once mien': 18 rows).  Needs only the binary: mvme88k/mvme187 constructs from the PROM.
C040LOG=$LOGDIR/pcc2_c040.log
python3 -u pcc2_c040_probe.py "$PMAX" gate > "$C040LOG" 2>&1 || true
if ! grep -q "PCC2C040_DONE" "$C040LOG"; then
    check "pcc2 c040 probe completed" "no" "yes"
else
    check "pcc2 c040 probe completed" "yes" "yes"
    for v in "genctl ctl" "genctl ctlq" "c040 kill" "c040 attrib" "c040 says" "c040 once" "c040 predirty" "irq pending" "irq live" "c040 noassert" "c040 noassert2" "c040 recover" "c040 says mien" "c040 once mien" "c040 genctl" "c040 pending" "c040x2 pending" "c040rec pending"; do
        check "pcc2 c040 row: $v" "$(count "$C040LOG" "^$v  .*ok$")" "1"
    done
    check "pcc2 c040 rows emitted" "$(( $(count "$C040LOG" " ok$") + $(count "$C040LOG" " FAIL$") ))" "18"
    check "pcc2 c040 rows green"   "$(count "$C040LOG" " ok$")"   "18"
    check "pcc2 c040 rows red"     "$(count "$C040LOG" " FAIL$")" "0"
fi


PITLOG=$LOGDIR/pit8253_latch.log
python3 pit8253_latch_probe.py "$PMAX" "$STUB" > "$PITLOG" 2>&1 || true

#  A PRESERVED LOG IS VERIFIED BY ITS COMPLETION SENTINEL, NOT BY ITS EXISTENCE.  The probe
#  gained PIT8253_LATCH_DONE specifically so this row could be written correctly the first
#  time -- before it, the last line was a bare "PASS", a word that occurs in dozens of other
#  contexts and cannot distinguish a COMPLETED run from a TRUNCATED one.
if ! grep -q "PIT8253_LATCH_DONE" "$PITLOG"; then
    note "pit8253 probe did not reach its completion sentinel; last lines follow"
    tail -5 "$PITLOG" | sed 's/^/       /'
    check "pit8253 probe completed" "no" "yes"
else
    grep -E "^  (ok|FAIL) " "$PITLOG" | sed 's/^/       /'

    #  THE THREE CONTROLS PLUS THE MMU-ON NEGATIVE CONTROL, each pinned by name.  A count of
    #  green rows would let a control go red while the total stayed acceptable.
    for c in "C1 liveness" "C2 MMU state" "A1 device signature" "T  MMU-ON control"; do
        check "pit8253 control: $c" \
              "$(grep -c "^  ok   $c" "$PITLOG")" "1"
    done

    #  Per-row presence.  A row that silently stops being tested is the padded-column class,
    #  so each is checked individually rather than by a total.  Eighteen rows: 4 controls +
    #  E/A2 apparatus + R0..R11.
    for v in "E  encodings" "A2 recompute stream" \
             "R0 the run produced data" "R1 latch preserves programming" \
             "R2 latch is not an error" "R3 latched read is not the reload" \
             "R4 16-bit readback is the reload" "R5 one recompute per write pair" \
             "R6 no transient count of zero" \
             "R7 read and write flip-flops are separate" \
             "R8 the latch is released by reading it" \
             "R9 a mid-pair latch completes the pair and lets go" \
             "R10 a Control Word rewinds the write flip-flop" \
             "R11 ...and it does so PER COUNTER, not just counter 0"; do
        check "pit8253 row green: $v" \
              "$(grep -c "^  ok   $v" "$PITLOG")" "1"
    done

    #  The denominator against a LITERAL: a probe that loses rows cannot pass by shrinking.
    check "pit8253 rows run" "$(grep -cE '^  (ok|FAIL) ' "$PITLOG")" "18"
fi

#  ---- xscaleinten: arm_coproc_i80321_6's read of the modelled inten register (CP6 crm 0 / crn 0)
#  ended the host with `fatal(); exit(1)' after computing the right value; it is now an ACCEPT.  The
#  promoted detector is 30 rows: the agy witness's 26, codex's two (D_OP1, INTEN_WRITE_PRESERVES_ISTEER),
#  D_CRM1_TMR0 (the crm-isolation row), and RD0_ALLONES, added on pass 2 after an exit keyed on
#  `rd == 0' measured 29/29 against the 29-row instrument.  Kill table 3
#  (artifacts/xscaleinten/killtable3_20260912/): twelve legs, all on prediction, BASE 30/30, HEAD 12/30;
#  each pass-2 row the SOLE killer of its own mutant (RD0_ALLONES kills M_RD0 and M_MAGICBIT).  Unreached rows report
#  BLOCKED and are not passes, so both FAIL and BLOCKED must be zero.  Section shape from the codex
#  promotion design (codex_promote_20260912b.txt), which said 28; pinned by hand at 30.
XSCALELOG=$LOGDIR/gate_xscale_inten.log
xrc=0
python3 -u xscale_inten_probe.py "$PMAX" gate "$STUB" > "$XSCALELOG" 2>&1 || xrc=$?

#  PARSE BEFORE SCORE: exactly one valid record of each kind.
if [ "$(grep -c '^XSCALE_RESULT=' "$XSCALELOG")" != "1" ] ||
   ! grep -Eq '^XSCALE_RESULT=(0|[1-9][0-9]*)/(0|[1-9][0-9]*)$' "$XSCALELOG" ||
   [ "$(grep -c '^XSCALE_CONTROL=' "$XSCALELOG")" != "1" ] ||
   ! grep -Eq '^XSCALE_CONTROL=(OK|FAIL)$' "$XSCALELOG" ||
   [ "$(grep -cx 'XSCALE_PROBE_DONE' "$XSCALELOG")" != "1" ]; then
    note "xscale probe produced no unique, valid completion record; last lines follow"
    tail -5 "$XSCALELOG" | sed 's/^/       /'
    check "xscale probe output parses" "no" "yes"
else
    check "xscale probe output parses" "yes" "yes"
    grep -E ' (ok|FAIL|BLOCKED)$' "$XSCALELOG" | sed 's/^/       /'
    check "xscale controls" "$(sed -n 's/^XSCALE_CONTROL=//p' "$XSCALELOG")" "OK"
    check "xscale probe exit status" "$xrc" "0"
    xres=$(sed -n 's/^XSCALE_RESULT=//p' "$XSCALELOG")
    #  Pinned by hand to a LITERAL: a pin that follows the probe cannot tell gained rows from lost ones.
    #  UNQUOTED on purpose: check_score_claims.py's PIN regex cannot see a quoted count, so `#526'
    #  shipped this as "30" and the score-claims check guarded nothing here (fixed in `#527').
    check "xscale rows run"     "${xres#*/}" 30
    check "xscale rows correct" "${xres%/*}" "30"
    check "xscale rows emitted" "$(grep -cE ' (ok|FAIL|BLOCKED)$' "$XSCALELOG")" "30"
    check "xscale rows failed"  "$(grep -c ' FAIL$' "$XSCALELOG")" "0"
    check "xscale rows blocked" "$(grep -c ' BLOCKED$' "$XSCALELOG")" "0"
fi

gate_end
