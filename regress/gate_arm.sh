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
# whole gate still green at 261 checks.
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
# There is no LDRD/STRD row on purpose: A2.8 makes an unaligned doubleword
# access UNPREDICTABLE prior to ARMv6, so every base that would exercise the
# ~7 mask makes the instruction unspecified -- covered by the fix, not honestly
# assertable.
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
check "endian rows run"     "${ewant:-missing}" 70
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
         "swp le un2 b2" "swp le un2 b3" "swp le un2 sent"; do
    n=$(count "$ENDLOG" "^$v  *DISC .*ok$")
    check "  endian row: $v" "$n" 1
done

gate_end
