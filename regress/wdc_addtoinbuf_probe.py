"""wdcaddtoinbufbound -- RUNG-3 WITNESS.  Real guest instructions, real address
decode, real memory_rw, on an UNMODIFIED in-tree machine description
(`evbmips -e malta`).  No device is added and no machine description is edited.

THE DEFECT.  The guest WRITE arm of the wdc data port pushes bytes into the
shared inbuf ring with NO phase guard.  During an ATAPI DATA-IN transfer the
one diagnostic that could announce a stray write is suppressed, because its
condition requires !atapi_cmd_in_progress and that flag is 1 for the whole of
DATAIN.  Injected bytes grow `head` WITHOUT touching `atapi_len`, so they sit
in the ring ahead of the next chunk and the guest's whole next chunk arrives
SHIFTED.

THE ORACLE IS ABSOLUTE, NOT RELATIVE.  Chunk 2's bytes are poisoned at known
image offsets, so the fixed leg's expected values are tied to DISK CONTENT
through a channel outside the ring -- not merely "different from the shipped
leg".

THE PATH (all references GXEMUL-SEC/src/devices/dev_wdc.c at HEAD c125450):
  wd_command(7) <- 0xa0   wdc_command() ATAPI_PKT_CMD arm: sets
                          atapi_cmd_in_progress=1, atapi_phase=PHASE_CMDOUT.
  wd_data(0)   <- 12 CDB bytes (READ(10), LBA 0, 128 blocks -- see READ_BLOCKS
                          below for why 128 and not 32).  On the 12th,
                          inbuf_len==12 and the dispatch
                          fires (guarded by atapi_cmd_in_progress && !badlen_this
                          && atapi_phase==PHASE_CMDOUT && inbuf_len==12).
                          diskimage_scsicommand() READ(10) -> res==1,
                          data_in_len=65536; atapi_len clamped to 32768 and
                          32768 bytes pushed; atapi_phase=PHASE_DATAIN.
  wd_data(0)   -> 32767 byte reads.  Each pops one byte and decrements
                          atapi_len (consumed = len==4?4:(len>=2?2:1), clamped
                          to what remains).  atapi_len -> 1, ring holds 1.
  wd_data(0)   <- ONE 2-byte store.  The write arm's `case 2:` pushes
                          idata&0xff then (idata>>8)&0xff -- 0xa5 then 0x5a for
                          0x5aa5 little-endian.  atapi_len is UNTOUCHED.
  wd_data(0)   -> one byte read.  Pops the last chunk-1 byte, atapi_len -> 0,
                          and the re-arm fires: atapi_received(32768) <
                          data_in_len(65536), so atapi_len = 32768 and
                          data_in[32768+j] is pushed ONTO THE DIRTY RING.
  wd_data(0)   -> the next reads.  *** SHIPPED: the guest is handed its own
                          injected bytes back as disk data.  FIXED: chunk 2. ***

STATUS ORACLE, PINNED FROM SOURCE AND NOT FROM A MEASUREMENT.  status_byte()
ORs DRDY|DSC (0x50, diskimage_exist true), DRQ (0x08) when head != tail, DRQ
again when atapi_cmd_in_progress && (atapi_phase & WDCS_DRQ) -- PHASE_DATAIN is
WDCS_DRQ|WDCI_IN so that arm is set too -- and ERR (0x01) only when d->error.
wdc_command() assigns `d->error = 0` at its top, so after ATAPI_PKT_CMD the ERR
bit is CLEAR.  Expected: 0x58.  (The wdcringambig probe sees 0x59 because it
issues no command at all and the power-on d->error = 1 stands.)

WHY FREE-RUNNING AND NOT `step`:  DEVINIT sets d->data_debug = 1, so every
data-port access calls debug().  debug() adds 1 to `verbose` when single_step is
set and subtracts 1 when emul_executing, so a STEPPED run prints a line per
access while a FREE-RUNNING run at default verbosity has v == -1 and prints
nothing.  The probe therefore breakpoints and continues.

CONTROLS CARRIED (both mandated for an access witness):
  A  RAM LIVENESS      a known value round-trips through plain RAM using the
                       IDENTICAL sb/lbu instruction shapes.
  B  DEVICE SIGNATURE  two reads of the SAME data-port address return PUSH
                       ORDER (0x5a then 0xa5).  A memory cell cannot do this;
                       RAM would return a5,a5.
  D  DISK CONTENT      the first DATA-IN byte is the poisoned image byte 0xC0,
                       so the ring demonstrably holds real disk data.
  CONTROL 0            every hand-assembled word is checked against the
                       emulator's OWN disassembler.  A wrong register field
                       silently yields 0, which several rows would accept.

NOTHING IN THE REPO IS WRITTEN.  Both trees under measurement are copies under
/tmp, and the CD image is generated under /tmp.
CONTRACT -- vacuity-floor clause (e).

  WHY THIS EXISTS AT ALL, and it is not a preference: the shipped 128-row offline
  detector (regress/diff_wdc_identify.c) scores ZERO failures with this defect LIVE.
  It cannot see the defect, so floor clause (a) is unsatisfiable from any existing
  row.  This probe is the only instrument that observes it.

  CATCHES: edits to the write-arm phase guard that let host stores reach the ring
    during DATA-IN.
      * dropping the phase conjunct, or re-aiming it at another phase -- measured,
        17 of 20, via the post-re-arm readback returning injected bytes;
      * qualifying the guard by access WIDTH -- measured, 17 of 20; note this also
        escapes any witness that injects with single-byte stores, which is why the
        injection here is a 2-byte store;
      * dropping the FLAG conjunct so the guard over-refuses -- measured, 18 of 20,
        caught by the DEVICE-SIGNATURE control rather than by a defect row, because
        an over-reaching guard suppresses the pre-command pushes too and the FIFO
        then reads back ff.
      * edits that leave the guard REFUSING after a non-packet command has cleared
        the ATAPI state -- the ACCEPT side, rows M and N.  The measured instance is the
        operand swap `atapi_cmd_in_progress` -> `atapi_st != NULL`, which escaped
        all 22 rows before those four existed and refuses every ordinary data-port
        write for the life of the device once a packet command has run.
        *** STATE WHAT THIS BUYS NARROWLY: it is NOT "the accept side is pinned",
        and a measuring seat showed that claim is FALSE. ***  Rows B and M differ
        in exactly ONE dimension a mutant can read -- whether a packet command has
        ever run (`atapi_st`, `atapi_received`, `cur_command`, the latches).  That
        is why the flag-conjunct deletion reds FOUR rows, B and M redundantly, and
        why **the swap above is these arms' only UNIQUE kill**: at row B `atapi_st`
        is still NULL, so the swapped guard is false there and B stays green.
        A SECOND operand replacement -- `cur_command == ATAPI_PKT_CMD` -- was measured
        sweeping all 30 and is NOT caught here: it replaces the flag operand rather
        than exempting an opcode, so BOTH vehicles leave it green.  Filed as
        `wdcflagswap2`.  (This pointer used to read 'two further accept-side mutants
        -- see BLIND-TO' and dangled: one referent was repaired in this same round
        and the other was never listed there at all.)

  BLIND to: everything the offline detector covers (ring occupancy, the CDB dispatch,
    the sector drain) -- the two are COMPLEMENTARY and neither subsumes the other, so
    both ship.  Also blind to injections during the LAST chunk, which have no
    following re-arm; and it walks ONE chunk boundary, not several (wdcrearmwalk).
    *** ONE MORE IS FILED.  A SECOND WAS FILED AND THEN CLOSED IN THIS SAME ROUND, AND
    THIS BLOCK SAID "FILED" ABOUT IT UNTIL A PANEL SEAT CAUGHT THE CONTRADICTION FROM
    THE PACKET ALONE. ***
      * THE INEQUALITY WIDTH QUALIFIER -- `&& len != 4` -- IS CLOSED, NOT FILED.
        It was derived by one seat, filed as above-floor coverage debt, then MEASURED
        by another sweeping the whole detector.  *** CITE THAT EVIDENCE PRECISELY:
        the a5/5a/00 readback the finding is usually quoted with came from a probe
        whose DATA-IN injection had been WIDENED to 4 bytes to demonstrate the
        hazard -- it is not what E4 scores against THIS instrument. ***  Against the
        repaired probe E4 leaves G/H/I green and dies on row L (`want 50 got 58`),
        because the K2 store is admitted and the ring gains bytes.  Same conclusion,
        different row, and the first draft of this comment named the wrong one.
        It is clause (d)'s canonical form on the predicate #495 added,
        so it is a FLOOR BREACH and was repaired here by the 4-byte store in the K2
        arm.  Measured after the repair: 29/30, 1 red.  `wdcwidth4` records the
        history; the escape itself is closed.
        **The sentence that stood here said "Filed as `wdcwidth4`" while the repair
        was already in the same diff** -- a wrong record shipped alongside its own
        refutation, and the deepseek seat found it by noticing the packet contradicted
        itself.  A disposition written before a measurement outlives the measurement
        unless someone goes back for it.
      * deleting the ring reset from wdc_new_command_reset().  *** THE FIGURE THIS
        ENTRY CARRIED -- 'escapes all 26' -- WAS INVALIDATED BY THIS ROUND'S OWN
        REPAIR AND WAS NOT RE-RUN. ***  26 is 13 rows x 2, the instrument BEFORE the
        N arm and the 4-byte store; the shipped one is 15/30.  And the stated reason
        -- the guard keeps the ring empty at every command boundary -- holds only on
        the FIXED leg; the bug-file version of the same sentence carries that
        qualifier and this one dropped it.  On the BASE leg K and K2 both LAND, so
        the ring holds bytes at the RECAL boundary and deleting the reset is
        predicted to red row M/t7.  **DERIVED, NOT MEASURED** -- said plainly rather
        than carried as a number.  Filed as `wdcringresetblind` with the re-run owed.
        *This is the round's own LEG-0 discipline -- re-measure an inherited figure
        rather than transcribe it -- left unapplied to a figure the round itself
        invalidated.*

  ONE CONTROL IS WEAKER THAN IT LOOKS, named rather than hidden: the status-byte row.
    status_byte() ORs DRQ from three independent conditions, two of which are true
    here at once, so it cannot distinguish `ring non-empty` from `packet command
    active`.  It is a LIVENESS row and pins nothing about the defect.  The
    device-signature row is the one carrying weight -- and it earned it, by being
    what caught the over-refusing mutant.

  NOT WIRED INTO A GATE: two-leg differential, dated-exempt with its siblings.
"""
import os
import pty
import re
import select
import sys
import time

#  PARAMETERISED on promotion.  The seat built this for its own scratch run and
#  hardcoded five paths; a committed detector cannot.  The defaults are the
#  seat's, so a bare invocation still reproduces its run exactly.
#
#      wdc_addtoinbuf_probe.py <base_bin> <fix_bin> <cd_image> <outdir>
#
#  *** THE SENTENCE THAT SAT HERE WAS A WRONG RECORD ABOUT THIS INSTRUMENT, INSIDE
#  THIS INSTRUMENT, AND IT WAS ALREADY FALSE ON THE DAY IT WAS COMMITTED. ***  It read
#  "THE PROGRAM AND THE ROWS BELOW ARE UNTOUCHED.  They are what measured 20 of 20
#  across both legs."  #495 had added the J/K/L arm in that same round -- its own
#  comment says "Added after mutant M5 escaped at 20/20" -- which took the instrument
#  to 11 rows and 22 predictions before the file was ever committed.
#
#  THE REVISION HISTORY, which is what that sentence was reaching for:
#      10 rows / 20 predictions   the promoted witness, as the measuring seat built it
#      11 rows / 22 predictions   #495 added J/K/L after M5 escaped at 20/20
#      15 rows / 30 predictions   wdcatapistswap added the M and N accept arms and a
#                                 third access width
#
#  (this line read '13 rows / 26' until a seat noticed the round had GROWN PAST ITS
#  OWN REVISION ENTRY -- the N arm and the 4-byte store landed after it was written.)
#
#  A frozen-instrument claim is worth making, but it must name the revision it is
#  frozen AT.  An unqualified "untouched" goes false the first time anyone touches the
#  file, and nothing re-reads a comment to check.  Found by the fable5 seat, which also
#  noticed the 17-of-20 and 18-of-20 figures in the CATCHES block below are the
#  10-row-era numbers and are kept as DATED measurements, not as current scores.
SHIPPED_BIN = sys.argv[1] if len(sys.argv) > 1 else "/tmp/gxadd/base/gxemul"
FIXED_BIN = (sys.argv[2] if len(sys.argv) > 2
             else os.environ.get("FIXBIN", "/tmp/gxadd/fixA/gxemul"))
FIXTAG = os.environ.get("FIXTAG", "fixA")
CD = sys.argv[3] if len(sys.argv) > 3 else "/tmp/gxadd/cd.iso"
BASE = 0xffffffff80100000          # KSEG0, physical 0x00100000, inside malta's 128 MB
LOGDIR = sys.argv[4] if len(sys.argv) > 4 else "/tmp/gxadd/probe"
RAWBIN = os.path.join(LOGDIR, "addtoinbuf.bin")

DATA_HI, DATA_LO = 0xb800, 0x01f0  # wdc data port, KSEG1 (physical 0x180001f0)
CMD_OFF = 7                        # wd_command (W) / wd_status (R)
RAM_HI = 0x8020                    # KSEG0 scratch for the RAM liveness control

DRDY, DSC, DRQ, ERR = 0x40, 0x10, 0x08, 0x01
ST_DATAIN = DRDY | DSC | DRQ       # 0x58 -- ERR cleared by wdc_command()
#  0x50.  In PHASE_COMPLETED the phase carries no WDCS_DRQ, so DRQ here reflects
#  ring occupancy alone: this is the byte an EMPTY ring produces.
ST_IDLE = DRDY | DSC               # 0x50 -- DRQ clear, nothing queued

ATAPI_PKT_CMD = 0xa0
#  WDCC_RECAL: the M arm's clearing command.  Chosen because its whole case body is
#  `d->int_assert = 1; break;` -- it pushes nothing into the ring, so the arm starts
#  from a known-empty ring rather than from a drain.
#
#  *** NOT WDCC_IDENTIFY, AND THE REASON IS NOT OBVIOUS FROM THE COMMAND TABLE. ***
#  wdc_command() takes an early return, BEFORE its switch, when the drive is a CDROM
#  and the command is WDCC_IDENTIFY.  This probe attaches a CD image (`-d ciR:`), so
#  IDENTIFY would never reach its case here.  The flag would still clear -- the early
#  returns sit after wdc_new_command_reset() -- but for a reason no reader of the
#  switch would see.  Found by a packet-fed panel seat that noticed the brief had
#  inlined the switch without the function's two early returns.
WDCC_RECAL = 0x10
#  The SECOND no-fill vehicle, and it is not redundancy -- see the N arm.  Same case
#  shape as RECAL (`debug(); d->int_assert = 1; break;`), different opcode.
ATAPI_SOFT_RESET = 0x08
# READ(10): opcode, flags, LBA[4] big-endian, reserved, len[2] big-endian, control
#
# *** THE BLOCK COUNT IS 128, NOT THE 32 THE ROUND'S SKETCH ASSUMED, AND THE
#     DIFFERENCE IS THE WHOLE WITNESS.  MEASURED, then explained: ***
# The sketch said "32 blocks on a CD-ROM", which reads as 32 x 2048 = 65536.
# In THIS tree a CD-ROM's logical_block_size is 512, not 2048 --
# diskimage.c:1984-1990 wraps the pmax/2048 choice in `#if 0` and assigns 512
# unconditionally, with a comment recording that OpenBSD/arc requires 512.
# diskimage_scsicmd.c:766 then computes size = retlen * logical_block_size.
# So 32 blocks is 16384 bytes -- BELOW the 32768 chunk clamp, so the whole
# transfer fits in chunk 1, atapi_received reaches data_in_len exactly, the
# re-arm takes its `else` branch to PHASE_COMPLETED, and NO SECOND CHUNK IS
# EVER FETCHED.  The defect cannot be exhibited at 32 blocks.
# MEASURED at 32 blocks: row F returned a5 (the injected byte) with the ring
# holding only the injection, and the over-read latch fired -- the signature of
# a transfer that ended early, not of the defect.
# 128 blocks x 512 = 65536 -> chunk 1 = 32768, chunk 2 = 32768, which is the
# two-chunk shape the defect needs.  ofs = LBA * 512 = 0, so data_in[j] is
# still image[j] and the poisoned offsets are unchanged.
READ_BLOCKS = 128
CDB = [0x28, 0, 0, 0, 0, 0, 0,
       (READ_BLOCKS >> 8) & 0xff, READ_BLOCKS & 0xff, 0, 0, 0]

DRAIN_AFTER_FIRST = 32766          # 1 (row D) + 32766 = 32767 pops -> atapi_len == 1
#  Rows G/H/I take three bytes of chunk 2; this drains the rest so the transfer
#  COMPLETES and atapi_phase leaves DATA-IN.  32768 - 3 = 32765.
DRAIN_CHUNK2 = 32765
INJECT = 0x5aa5                    # -> pushes 0xa5 then 0x5a

zero, t0, t1, t2, t3, t4, t5, t6 = 0, 8, 9, 10, 11, 12, 13, 14
s0, s1, s2, s3, s4, s5, s6, s7 = 16, 17, 18, 19, 20, 21, 22, 23
t8, t9 = 24, 25
#  t7/v0 carry the M arm's readbacks and v1/a0 the N arm's.  Each arm deliberately
#  uses its OWN output registers for its scratch stores too, so neither touches a
#  register any other arm uses -- see the note above the M arm.
t7, v0, v1, a0 = 15, 2, 3, 4


def R(op, rs, rt, rd, sa, fn):
    return (op << 26) | (rs << 21) | (rt << 16) | (rd << 11) | (sa << 6) | fn


def I(op, rs, rt, imm):
    return (op << 26) | (rs << 21) | (rt << 16) | (imm & 0xffff)


def lui(rt, imm):
    return I(0x0F, 0, rt, imm)


def ori(rt, rs, imm):
    return I(0x0D, rs, rt, imm)


def addiu(rt, rs, imm):
    return I(0x09, rs, rt, imm)


def sb(rt, off, base):
    return I(0x28, base, rt, off)


def sh(rt, off, base):
    return I(0x29, base, rt, off)


def sw(rt, off, base):
    #  Added by `wdcatapistswap` after a measuring seat found the probe had NO 4-byte
    #  access emitter at all -- no `sw`, no `lw` -- so `case 4:` on both endian arms,
    #  were unexercised on every leg of every run this detector had ever made.
    #
    #  *** THIS SENTENCE ALSO CLAIMED THE `sw` EXERCISES `consumed = len == 4 ? 4 :
    #  ...`.  IT CANNOT, AND A SEAT CHECKED THE SCOPE RATHER THAN THE NAME. ***
    #  `consumed` lives inside `if (writeflag == MEM_READ)`, so no STORE reaches it;
    #  it needs a 4-byte LOAD, and this probe's only load emitter is `lbu`.  So
    #  `consumed` has only ever taken its `: 1` branch, before this round and after.
    #  The BE push arms are likewise unexecuted -- the guest is little-endian -- and
    #  `-e maltabe` is a registered in-tree subtype, so a BE leg is a one-word argv
    #  change rather than a machine edit (`wdcprobeendian`).
    return I(0x2b, base, rt, off)


def lbu(rt, off, base):
    return I(0x24, base, rt, off)


def bne(rs, rt, off):
    return I(0x05, rs, rt, off)


def beq(rs, rt, off):
    return I(0x04, rs, rt, off)


def or_(rd, rs, rt):
    return R(0, rs, rt, rd, 0, 0x25)


NOP = 0
prog = []


def emit(word, want_mnemonic):
    prog.append((word, want_mnemonic))


emit(lui(t0, DATA_HI), "lui t0,0xb800")
emit(ori(t0, t0, DATA_LO), "ori t0,t0,0x01f0")
emit(lui(t4, RAM_HI), "lui t4,0x8020")

# A -- RAM LIVENESS, identical instruction shapes, plain RAM.
emit(addiu(t3, zero, 0x55), "addiu t3,zr,85")
emit(sb(t3, 0, t4), "sb t3,0(t4)")
emit(lbu(t8, 0, t4), "lbu t8,0(t4)")

# B -- DEVICE SIGNATURE.  Two pushes, then two reads of the SAME address.
emit(addiu(t3, zero, 0x5a), "addiu t3,zr,90")
emit(sb(t3, 0, t0), "sb t3,0(t0)")
emit(addiu(t3, zero, 0xa5), "addiu t3,zr,165")
emit(sb(t3, 0, t0), "sb t3,0(t0)")
emit(lbu(s0, 0, t0), "lbu s0,0(t0)")
emit(lbu(s1, 0, t0), "lbu s1,0(t0)")
# ring is empty again here: head == tail == 2.

# ARM the packet command.
emit(addiu(t3, zero, ATAPI_PKT_CMD), "addiu t3,zr,160")
emit(sb(t3, CMD_OFF, t0), "sb t3,7(t0)")

# Send the 12-byte CDB.  t3 is reloaded only when the value changes.
last = None
for b in CDB:
    if b != last:
        emit(addiu(t3, zero, b), "addiu t3,zr,%d" % b)
        last = b
    emit(sb(t3, 0, t0), "sb t3,0(t0)")
# On the 12th byte the dispatch fires and 32768 bytes are pushed.

# C -- status with the DATA-IN chunk queued.
emit(lbu(s2, CMD_OFF, t0), "lbu s2,7(t0)")

# D -- first DATA-IN byte: the poisoned image byte 0xC0 (disk-content control).
emit(lbu(s3, 0, t0), "lbu s3,0(t0)")

# drain the rest of chunk 1 but ONE byte.
emit(ori(t2, zero, DRAIN_AFTER_FIRST), "ori t2,zr,0x7ffe")
emit(lbu(t5, 0, t0), "lbu t5,0(t0)")
emit(addiu(t2, t2, -1), "addiu t2,t2,-1")
emit(bne(t2, zero, -3), "bne zr,t2,")
emit(NOP, "nop")

# E -- THE INJECTION.  One 2-byte store while atapi_phase == PHASE_DATAIN.
emit(ori(t6, zero, INJECT), "ori t6,zr,0x5aa5")
emit(sh(t6, 0, t0), "sh t6,0(t0)")

# F -- the last chunk-1 byte.  THIS read takes atapi_len to 0 and fires the
#      re-arm, which refills chunk 2 onto a ring still holding the injected bytes.
emit(lbu(s4, 0, t0), "lbu s4,0(t0)")

# G/H/I -- what the guest is handed as "chunk 2".
emit(lbu(s5, 0, t0), "lbu s5,0(t0)")
emit(lbu(s6, 0, t0), "lbu s6,0(t0)")
emit(lbu(s7, 0, t0), "lbu s7,0(t0)")

#  ---- J/K/L: THE PHASE-COMPLETED ARM.  Added after mutant M5 escaped at 20/20. ----
#
#  M5 narrows the guard from `!= PHASE_CMDOUT` to `== PHASE_DATAIN`.  Every row above
#  injects during DATA-IN, where BOTH forms refuse, so M5 passed all twenty.  It lets
#  stores through in PHASE_COMPLETED, which the shipped guard refuses.
#
#  J -- drain the rest of chunk 2 so the transfer completes and the phase moves on.
emit(ori(t2, zero, DRAIN_CHUNK2), "ori t2,zr,0x7ffd")
emit(lbu(t5, 0, t0), "lbu t5,0(t0)")
emit(addiu(t2, t2, -1), "addiu t2,t2,-1")
emit(bne(t2, zero, -3), "bne zr,t2,")
emit(NOP, "nop")

#  K -- THE SECOND INJECTION: a different PHASE *and* a different WIDTH.
#
#  *** THE WIDTH IS LOAD-BEARING AND WAS NOT, WHICH COST A FLOOR BREACH. ***  Both
#  injections used to be 2-byte stores, so a guard qualified `&& len == 2` refused
#  BOTH and swept all 22 rows clean -- MEASURED escaping, the mirror of the
#  `&& len == 1` mutant the round DID build.  The table had measured the inert
#  member of the family and concluded the family was covered.
#
#  A SINGLE-BYTE store here closes the EQUALITY family with one instruction: `len == 1`
#  now lets the 2-byte DATA-IN injection through (rows G/H/I red), and `len == 2` lets
#  this one through (row L red).
#
#  *** THE SENTENCE THAT ENDED THIS PARAGRAPH WAS A FALSE UNIVERSAL, AND IT SAT TWO
#  LINES BELOW ITS OWN REFUTATION. ***  It read "No single width qualifier can refuse
#  both."  True of EQUALITY qualifiers, FALSE of the inequality: `&& len != 4` refuses
#  a 1-byte store AND a 2-byte store, so it left every row green while re-opening the
#  defect BYTE-FOR-BYTE.  Measured by a seat at 30/30 -- rows G/H/I returned the
#  injected a5/5a/00, which is what the PRE-FIX build returns, against the fix's real
#  disk content c2/c3/c4.
#
#  THE CLOSURE CONDITION, and it needs TWO clauses rather than one -- the first draft
#  of this comment ran them together and a seat took the sentence apart:
#
#    a qualifier `&& P(len)` ESCAPES THE DETECTOR    iff P is TRUE on every width
#                                                        this probe INJECTS;
#    it escapes AND RE-OPENS THE DEFECT              iff ADDITIONALLY P is FALSE
#                                                        on some width that PUSHES.
#
#  The widths that push are exactly 1, 2 and 4.  The 3- and 8-byte cases fall to
#  `default:` and push NOTHING, so a qualifier that stops refusing there changes no
#  observable: it is an EQUIVALENT MUTANT.  Injecting all three pushing widths means
#  no P can be true on every injected width and false on a pushing one, so **the
#  family of HARMFUL escapes is closed** -- {1,2} left `!= 4` open, {2,4} leaves
#  `!= 1`, {1,4} leaves `!= 2`, and only {1,2,4} closes it.
#
#  *** EQUIVALENT MUTANTS SURVIVE AND ALWAYS WILL: `&& len != 8`, `&& len != 3`,
#  `&& len <= 4` all leave every row green. ***  That is not a coverage hole -- none
#  of them lets a byte reach the ring -- and no row can or should kill them.  Two
#  seats disagreed about this and BOTH were partly right: one showed the survivors
#  exist, the other that they are inert.  The sentence, not the substance, was wrong.
emit(ori(t6, zero, INJECT), "ori t6,zr,0x5aa5")
emit(sb(t6, 0, t0), "sb t6,0(t0)")

#  K2 -- THE 4-BYTE INJECTION.  The third width, and the third leg of the proof above.
#
#  One instruction, NO new row and NO re-pinning: on the fixed leg it is refused like
#  its neighbours, so the ring stays empty and row L still reads ST_IDLE; on the base
#  leg it lands like its neighbours, so DRQ is set and row L still reads ST_DATAIN.
#  It kills the `len != 4` escape and it kills M3 and M6 at the same time.
#
#  It is also the ONLY access in this probe that reaches the device's `case 4:` WRITE
#  arm, which no leg of any run had executed before.
#
#  *** SAY `case 4:` WRITE ARM AND NOTHING MORE.  An earlier draft added "and the
#  whole `consumed = ...` accounting" -- FALSE: `consumed` is in the MEM_READ arm and
#  a store cannot reach it.  Closing a WRITE-side gap buys nothing on the READ side,
#  and a claim that reaches across is the CLAIM->ROW check's own quarry. ***
emit(sw(t6, 0, t0), "sw t6,0(t0)")

#  L -- the status byte, and here it is a SHARP control rather than a weak one.
#  status_byte() ORs DRQ from three conditions: ring occupancy, write_in_progress,
#  and `atapi_cmd_in_progress && (atapi_phase & WDCS_DRQ)`.  During DATA-IN the third
#  is true, which is why row C pins nothing about the ring.  PHASE_COMPLETED is
#  (WDCI_IN | WDCI_CMD) and carries NO WDCS_DRQ, so here DRQ comes from ring
#  occupancy alone: DRQ set means the injected bytes landed.
emit(lbu(t1, CMD_OFF, t0), "lbu t1,7(t0)")

emit(or_(t9, t2, zero), "or t9,t2,zr")

#  ---- M: THE ACCEPT ROW.  Added by `wdcatapistswap` after an operand swap escaped
#  ---- all 22 rows of the table above.
#
#  The swap is `d->atapi_cmd_in_progress` -> `d->atapi_st != NULL` in the #495 guard.
#  It is not a contrived edit: dev_wdc.c's own comment records that the flag
#  CONFLATES TWO ROLES and files exactly this refactor, so a future round separating
#  them could write the swap believing it a simplification.
#
#  *** WHY A COMMAND MUST BE ISSUED FIRST, WHICH IS THE WHOLE DESIGN. ***  The obvious
#  form -- push and pop straight after the packet transfer completes -- is VACUOUS, and
#  a panel seat proved it from the source rather than by running it.  atapi_cmd_in_progress
#  has exactly TWO write sites: cleared in wdc_new_command_reset(), set at the packet
#  dispatch.  NO COMPLETION PATH CLEARS IT.  So post-transfer the flag is still 1, the
#  shipped guard refuses too, both legs read ff, and the row pins nothing.
#
#  The states where shipped and swapped DIFFER are exactly `flag == 0 && atapi_st != NULL`,
#  and only a command can produce them: wdc_new_command_reset() is the sole writer of
#  flag = 0, while atapi_st has ONE write site (the alloc) and NO clear site anywhere,
#  so once allocated the disagreement is permanent.  The RECAL is therefore load-bearing,
#  not scene-setting.
#
#  A second seat objected that RECAL leaves phase == 0 whereas "the real hole" would
#  leave PHASE_COMPLETED, so a mutant keying on the phase would tell them apart.  That
#  state does not exist: wdc_new_command_reset() zeroes flag and phase in the same three
#  lines, and every site that sets a nonzero phase lies on a path where the flag is 1.
#  **flag == 0 implies phase == 0**, so RECAL reaches the hole itself, not a stand-in.
#
#  *** POSITION IS LOAD-BEARING: THIS ARM MUST STAY AFTER THE PACKET ARMS. ***  Its
#  E2 kill exists only because a packet command has already allocated atapi_st.  Before
#  that, atapi_st is NULL -- devinit does `memset(d, 0, sizeof(struct wdc_data))` -- so
#  the swapped guard is FALSE, the pushes land, and both rows go green.  A future tidy-up
#  that groups the accept rows with the controls at the top would leave them permanently
#  green under E2 **with no visible change to the file**: same rows, same values, same
#  count, zero kill.  Named by the fable5 seat; the arm stated the disagreement state it
#  needs but never stated the ordering as a constraint.
#
#  REGISTER DISCIPLINE: this arm uses t7 and v0 for its scratch stores as well as for
#  its two readbacks, so it touches no register any earlier arm uses.  An earlier draft
#  used t3; a seat pointed out it could not tell from the packet whether t3 was read
#  back, and the sidestep costs the same eight instructions.
emit(addiu(t7, zero, WDCC_RECAL), "addiu t7,zr,16")
emit(sb(t7, CMD_OFF, t0), "sb t7,7(t0)")
emit(addiu(t7, zero, 0x5a), "addiu t7,zr,90")
emit(sb(t7, 0, t0), "sb t7,0(t0)")
emit(addiu(v0, zero, 0xa5), "addiu v0,zr,165")
emit(sb(v0, 0, t0), "sb v0,0(t0)")

#  The two readbacks.  Under the swap both pushes were refused, so these pop an EMPTY
#  ring and wdc_get_inbuf() returns its -1 sentinel: 5a,a5 -> ff,ff.
#
#  CROSS-DEPENDENCY, named here because neither file says it otherwise: the SECOND
#  readback's oracle rests on that `return` sitting OUTSIDE the overread latch.  That
#  is #464's finding and it is pinned by the `overread -1` row in another probe -- move
#  the return inside the latch and this row's second value changes meaning.  A latch
#  already burned by an earlier arm does not weaken either oracle, because the latch
#  gates the MESSAGE and not the return value.
emit(lbu(t7, 0, t0), "lbu t7,0(t0)")
emit(lbu(v0, 0, t0), "lbu v0,0(t0)")

#  ---- N: THE SECOND VEHICLE.  A DIFFERENT no-fill opcode, and it closes an axis the
#  ---- M arm holds fixed.
#
#  *** THIS IS THE M5/M6 LESSON ON A NEW AXIS, AND A SEAT FOUND IT BEFORE THE TABLE RAN
#  RATHER THAN AFTER. ***  With only the M arm, the smallest edit that re-opens the hole
#  and still sweeps every row is ONE conjunct naming this arm's own opcode:
#
#      if (d->atapi_st != NULL &&
#          d->atapi_phase != PHASE_CMDOUT &&
#          d->cur_command != WDCC_RECAL) {
#
#  After RECAL `cur_command` is 0x10, so the M pushes land and row M stays GREEN.  During
#  DATA-IN and PHASE_COMPLETED `cur_command` is still ATAPI_PKT_CMD, so G/H/I and L match
#  the fix.  **And after any OTHER no-fill command the ordinary writes are refused again**
#  -- the hole is fully re-opened, and a detector with one vehicle cannot see it.
#
#  A detector built from one scenario is blind along the axis that scenario holds fixed.
#  #495 learned this twice in one round -- M5 on the PHASE axis, M6 on the WIDTH axis --
#  and the axis here is WHICH no-fill opcode cleared the flag.
#
#  ONE CONJUNCT CANNOT EXEMPT TWO OPCODES.  RECAL is 0x10, ATAPI_SOFT_RESET is 0x08, and
#  both reach their case bodies on this CD-backed drive (neither is IDENTIFY, so neither
#  takes wdc_command()'s CDROM early return).  Exempting one leaves the other red.
emit(addiu(v1, zero, ATAPI_SOFT_RESET), "addiu v1,zr,8")
emit(sb(v1, CMD_OFF, t0), "sb v1,7(t0)")
emit(addiu(v1, zero, 0x5a), "addiu v1,zr,90")
emit(sb(v1, 0, t0), "sb v1,0(t0)")
emit(addiu(a0, zero, 0xa5), "addiu a0,zr,165")
emit(sb(a0, 0, t0), "sb a0,0(t0)")
emit(lbu(v1, 0, t0), "lbu v1,0(t0)")
emit(lbu(a0, 0, t0), "lbu a0,0(t0)")

HALT = len(prog)
emit(beq(zero, zero, -1), "b 0x")
emit(NOP, "nop")

HALT_ADDR = BASE + HALT * 4
REGS = ("t8", "s0", "s1", "s2", "s3", "s4", "s5", "s6", "s7", "t9", "t1",
        "t7", "v0", "v1", "a0")

# label, register, want SHIPPED, want FIXED, kind
ROWS = [
    ("A  RAM LIVENESS     RAM readback, same sb/lbu shapes", "t8", 0x55, 0x55, "control"),
    ("B  DEVICE SIGNATURE 1st read of the data port", "s0", 0x5a, 0x5a, "control"),
    ("B  DEVICE SIGNATURE 2nd read -- a FIFO, not a cell", "s1", 0xa5, 0xa5, "control"),
    ("C  LIVENESS         status with chunk 1 queued", "s2", ST_DATAIN, ST_DATAIN, "control"),
    ("D  DISK CONTENT     chunk 1 byte 0 (image[0])", "s3", 0xC0, 0xC0, "control"),
    ("F  DISK CONTENT     chunk 1 LAST byte (image[32767])", "s4", 0xC1, 0xC1, "control"),
    ("G  *** DEFECT ***   1st byte after re-arm", "s5", 0xa5, 0xC2, "defect"),
    ("H  *** DEFECT ***   2nd byte after re-arm", "s6", 0x5a, 0xC3, "defect"),
    ("I  *** DEFECT ***   3rd byte after re-arm", "s7", 0xC2, 0xC4, "defect"),
    ("   drain loop counter reached zero", "t9", 0x00, 0x00, "control"),
    #  THE M5 ROW.  Its want-SHIPPED value is RECORDED FROM THE FIRST RUN, not
    #  predicted: on the pre-fix build the FIRST injection also landed, so the
    #  ring state at this point is a consequence of two injections rather than
    #  one, and predicting it would have been a guess dressed as an oracle.  The
    #  FIXED value IS predicted: both injections refused, chunk 2 drains exactly,
    #  ring empty, so DRQ clear.
    ("L  *** DEFECT ***   status after a store in PHASE_COMPLETED",
     "t1", ST_DATAIN, ST_IDLE, "defect"),

    #  M -- THE ACCEPT SIDE.  Both legs want the SAME value, which is the point: a
    #  LEGAL write must be unaffected by the fix.  These rows are green on every
    #  shipped binary and redden only under a mutant that over-refuses -- the swap
    #  `atapi_st != NULL` (which is permanently true once a packet command has run)
    #  and the flag-conjunct deletion (which leaves `phase != PHASE_CMDOUT`, and
    #  PHASE_CMDOUT is nonzero while the post-RECAL phase is 0).
    ("M  ACCEPT           ordinary write after RECAL, 1st byte",
     "t7", 0x5a, 0x5a, "accept"),
    ("M  ACCEPT           ordinary write after RECAL, 2nd byte",
     "v0", 0xa5, 0xa5, "accept"),

    #  N -- the SAME assertion through a DIFFERENT no-fill opcode.  Not redundancy:
    #  with only the M rows, `&& d->cur_command != WDCC_RECAL` re-opens the hole for
    #  every other command while sweeping every row.  One conjunct cannot exempt two
    #  opcodes.
    ("N  ACCEPT           ordinary write after SOFT_RESET, 1st byte",
     "v1", 0x5a, 0x5a, "accept"),
    ("N  ACCEPT           ordinary write after SOFT_RESET, 2nd byte",
     "a0", 0xa5, 0xa5, "accept"),
]


class Emu(object):
    def __init__(self, argv, boot_wait=5.0):
        self.buf = bytearray()
        self.pid, self.fd = pty.fork()
        if self.pid == 0:
            try:
                os.execvp(argv[0], argv)
            finally:
                os._exit(127)
        self.drain(boot_wait)

    def drain(self, seconds):
        end = time.time() + seconds
        while time.time() < end:
            r, _, _ = select.select([self.fd], [], [], 0.05)
            if self.fd in r:
                try:
                    d = os.read(self.fd, 65536)
                except OSError:
                    return
                if not d:
                    return
                self.buf.extend(d)

    def send(self, cmd, wait=0.4):
        start = len(self.buf)
        data = (cmd + "\n").encode()
        view = memoryview(data)
        while len(view):
            n = os.write(self.fd, view)
            view = view[n:]
            if len(view):
                self.drain(0.05)
        self.drain(wait)
        return bytes(self.buf[start:]).decode("latin1", "replace")

    def close(self, log):
        try:
            os.write(self.fd, b"quit\n")
            self.drain(0.4)
        except OSError:
            pass
        for fn in (lambda: os.close(self.fd),
                   lambda: os.kill(self.pid, 9),
                   lambda: os.waitpid(self.pid, 0)):
            try:
                fn()
            except OSError:
                pass
        with open(log, "w") as f:
            f.write(bytes(self.buf).decode("latin1", "replace"))


def reg(emu, name):
    for _ in range(5):
        out = emu.send("print %s" % name, wait=0.35)
        m = re.findall(r"0x[0-9a-fA-F]+", out)
        if m:
            return int(m[-1], 16)
        emu.drain(0.25)
    return None


def run_one(binary, tag):
    argv = [binary, "-V", "-E", "evbmips", "-e", "malta",
            "-d", "ciR:" + CD, "0x%x:%s" % (BASE, RAWBIN)]
    print("  command   " + " ".join(argv))
    emu = Emu(argv)

    # CONTROL 0 -- hand-assembled words checked against the emulator's own
    # disassembler.  Addresses print WITHOUT an 0x prefix.
    dis = emu.send("unassemble 0x%x 0x%x" % (BASE, BASE + len(prog) * 4), wait=2.5)
    seen = {}
    for line in dis.splitlines():
        m = re.match(r"^\s*([0-9a-f]{8,16}):\s+([0-9a-f]{8})\s+(?:<-)?\s*(.*)$", line)
        if m:
            seen[int(m.group(1), 16) & 0xffffffff] = (m.group(2), m.group(3).strip())

    word_ok = word_bad = mn_ok = mn_bad = 0
    bad_lines = []
    for i, (w, want_mn) in enumerate(prog):
        addr = (BASE + i * 4) & 0xffffffff
        hit = seen.get(addr)
        if hit is None:
            word_bad += 1
            mn_bad += 1
            bad_lines.append("  BAD  0x%08x  no disassembly line" % addr)
            continue
        gotw, gotmn = hit
        norm = " ".join(gotmn.replace("\t", " ").split())
        want_norm = " ".join(want_mn.split())
        if gotw == "%08x" % w:
            word_ok += 1
        else:
            word_bad += 1
            bad_lines.append("  BADWORD 0x%08x  %s vs %08x" % (addr, gotw, w))
        if norm.startswith(want_norm):
            mn_ok += 1
        else:
            mn_bad += 1
            bad_lines.append("  MNEMONIC 0x%08x  %r vs want %r" % (addr, norm, want_norm))
    print("  CONTROL 0  words %d of %d ; mnemonics %d of %d agree with the"
          " emulator's disassembler" % (word_ok, len(prog), mn_ok, len(prog)))
    for l in bad_lines[:14]:
        print(l)

    pc0 = reg(emu, "pc")
    print("  pc at entry = %s (want 0x%016x)"
          % (("0x%016x" % pc0) if pc0 is not None else "UNREADABLE", BASE))

    emu.send("breakpoint add 0x%x" % HALT_ADDR, wait=0.5)
    t = time.time()
    emu.send("continue", wait=1.0)
    deadline = time.time() + 300
    hit = False
    while time.time() < deadline:
        emu.drain(0.5)
        tail = bytes(emu.buf[-4000:]).decode("latin1", "replace")
        #  *** MATCH THE HIT LINE, NOT THE BARE WORD. ***  This read
        #  `if "BREAKPOINT" in <tail>.upper():` until 2026-08-30, and the
        #  transcript contains the probe's OWN echoed setup command,
        #  `breakpoint add 0x...`.  The check matched its own input and could
        #  never return False.  It was right by accident in every run where the
        #  guest parked, and silently wrong in the first run where it did not:
        #  a mutant returning 0 from the device handler raises EXCEPTION_DBE, the
        #  guest re-executes the faulting store forever, and the probe still
        #  reported `breakpoint reached: True` with every register reading ??.
        #  That was scored as a KILL -- a failed run counted as a table result.
        #  The emulator prints `BREAKPOINT: pc = 0x...` on a real hit.
        if "BREAKPOINT: PC" in tail.upper():
            hit = True
            break
    elapsed = time.time() - t
    if not hit:
        print("  *** BREAKPOINT NOT REACHED within 300 s"
              " -- rows below are NOT a measurement")

    got = {}
    for nm in REGS:
        v = reg(emu, nm)
        got[nm] = None if v is None else (v & 0xff)

    whole = bytes(emu.buf).decode("latin1", "replace")
    diags = {n: whole.count(n) for n in
             ("wdc inbuf overrun", "write to DATA, but not", "reading too much",
              "ATAPI command rejected", "DATA OUT")}
    emu.close(os.path.join(LOGDIR, "transcript_%s.log" % tag))
    return got, elapsed, hit, diags


def main():
    os.makedirs(LOGDIR, exist_ok=True)
    with open(RAWBIN, "wb") as f:
        for w, _ in prog:
            f.write(bytes([w & 0xff, (w >> 8) & 0xff,
                           (w >> 16) & 0xff, (w >> 24) & 0xff]))

    print("=" * 94)
    print("wdcaddtoinbufbound -- RUNG-3 WITNESS on unmodified `evbmips -e malta`")
    print("=" * 94)
    print("machine   evbmips -e malta  5Kc, little endian, 128 MB (machine desc UNMODIFIED)")
    print("wdc       physical 0x180001f0 via bus_pci piix4_ide; KSEG1 0xffffffffb80001f0")
    print("media     -d ciR:%s  (CD-ROM, IDE, read-only)" % CD)
    print("program   %d guest instructions at 0x%016x, parks at 0x%016x"
          % (len(prog), BASE, HALT_ADDR))
    print("transfer  READ(10) LBA 0 x %d blocks of 512 = %d B; chunk 1 = 32768"
          % (READ_BLOCKS, READ_BLOCKS * 512))
    print("inject    ONE 2-byte store of 0x%04x while atapi_phase == PHASE_DATAIN" % INJECT)
    print()

    print("-" * 94)
    print("LEG 1 -- SHIPPED build (source-identical to GXEMUL-SEC at HEAD c125450)")
    print("-" * 94)
    ship, t_ship, hit_s, dg_s = run_one(SHIPPED_BIN, "shipped")
    print("  elapsed %.2f s   breakpoint reached: %s" % (t_ship, hit_s))
    print("  diagnostics seen: %s" % dg_s)
    print()

    print("-" * 94)
    print("LEG 2 -- %s build, SAME guest program, SAME image" % FIXTAG)
    print("-" * 94)
    fix, t_fix, hit_f, dg_f = run_one(FIXED_BIN, FIXTAG)
    print("  elapsed %.2f s   breakpoint reached: %s" % (t_fix, hit_f))
    print("  diagnostics seen: %s" % dg_f)
    print()

    print("-" * 94)
    print("RESULTS -- every value below was produced by a GUEST LOAD through real decode")
    print("-" * 94)
    print("  %-52s %-4s %-16s %-16s" % ("", "reg", "SHIPPED", FIXTAG.upper()))
    npass = nfail = 0
    changed = []
    for label, rn, wship, wfix, kind in ROWS:
        gs, gf = ship.get(rn), fix.get(rn)
        oks, okf = (gs == wship), (gf == wfix)
        npass += oks + okf
        nfail += (not oks) + (not okf)
        if wship != wfix:
            changed.append((label, rn, wship, wfix, gs, gf))
        print("  %-52s %-4s want %02x got %-4s want %02x got %-4s  %s"
              % (label, rn, wship, ("%02x" % gs) if gs is not None else "??",
                 wfix, ("%02x" % gf) if gf is not None else "??",
                 ("ok" if (oks and okf) else "FAIL")))
    print()
    print("  %d of %d predictions correct across both legs" % (npass, npass + nfail))
    print()

    print("-" * 94)
    print("THE DIFFERENTIAL -- the rows the defect owns, same script, opposite colour")
    print("-" * 94)
    for label, rn, wship, wfix, gs, gf in changed:
        print("  %-52s %-4s  %02x -> %02x   %s"
              % (label, rn, gs if gs is not None else 0, gf if gf is not None else 0,
                 "AS PREDICTED" if (gs == wship and gf == wfix) else "MISMATCH"))
    print()
    print("-" * 94)
    print("WHY THIS IS THE DEVICE AND NOT RAM  (device-signature control)")
    print("-" * 94)
    print("  s0/s1 read the SAME address twice and returned 0x%02x then 0x%02x."
          % (ship.get("s0") or 0, ship.get("s1") or 0))
    print("  A memory cell returns the last value written to BOTH reads (a5,a5).")
    print("  Push order (5a,a5) can only come from a FIFO -- the wdc inbuf ring.")
    print("  And row D returned 0x%02x, the poisoned CD image byte at offset 0,"
          % (ship.get("s3") or 0))
    print("  so the ring demonstrably holds real DISK data, not device scratch.")
    print()
    print("ADDTOINBUF_RUNG3_DONE")


main()
