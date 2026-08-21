#!/usr/bin/env python3
"""Rung-3 cold-debugger witness for `pitlatch` / `pitclobber` (dev_8253.c).

Real guest ARM instructions, real address decode, real memory_rw, on an UNMODIFIED
in-tree `-E cats`.  No boot, no disk image, no guest OS, no device_add of our own.

REACHABILITY: machine_cats.c -> dev_footbridge.c:730 ("ali_m1543") -> bus_pci.c:459/476
sets isa_portbase 0x7c000000; bus_isa.c:241 registers "8253 ... addr=isa_portbase+0x40".
So the PIT lives at PA 0x7c000040..0x7c000043 (CNTR0..2, MODE).

THE MMU TRAP (footbridge_sites_probe.py's header documents it): machine_cats.c calls
arm_setup_initial_translation_table(), which maps only the low 256 MB, ignoring the top
VA nibble.  PA 0x7c000000 is outside that window, so under the boot MMU the device is
UNREACHABLE and a load returns 0 -- which is exactly what the pre-fix symptom looks like.
So arm T (the same program with the three MMU-disable words replaced by NOPs) MUST NOT
produce the device's answer.  Without arm T a "0" row proves nothing at all.

THREE ARMS.  D and F differ by EXACTLY TWO IMMEDIATES (the counter bytes), which is what
makes F a discriminator rather than a second opinion:

  D  counter <- 0x2e9c   TIMER_DIV(100), what OpenBSD clock.c:162-166 programs
  F  counter <- 0xffff   what findcpuspeed() (clock.c:333-335) programs, and it then
                         divides by (0xffff - gettick()) at clock.c:344.  If a design
                         makes the latched read return the reload value, that divisor
                         is ZERO.  F measures the divisor, so the hazard is a number
                         this probe prints, not an argument.
  T  MMU left on         negative control

#440 adds four more arms.  None of P/Z/I latches anything, so they measure the
LSB/MSB selector alone; L measures the latch and the selector where they meet.

  P  two 16-bit write pairs, count 0x2e9c   the selector was ONE-WAY, so it stuck
                                            at MSB and pair 2 put BOTH bytes in
                                            the high half: a third recompute the
                                            guest never asked for, and a readback
                                            of 0x2e2e instead of 0x2e9c
  Z  the same with count 0x2e00             low byte 0x00, so that intermediate
                                            counter is EXACTLY 0 -- the device is
                                            driven to 0 Hz by a guest that never
                                            programs count 0.  This is the door
                                            onto the separately-filed count-0
                                            defect, which is why it gets its own
                                            arm rather than a comment.
  I  the i8254 p. 8 interleave              "read LSB, write new LSB, read MSB,
                                            write new MSB", a documented-valid
                                            sequence.  It is the row that
                                            separates TWO flip-flops (correct)
                                            from ONE shared one -- the plausible
                                            smaller fix, which passes P and Z.
  L  latch, read, read, read, read          #439 set latched[] and cleared it only
                                            on a mode write, so one latch command
                                            made every later read return 0 for
                                            ever.  Reads 3 and 4 must return the
                                            counter again.  (Found by the #439
                                            pass-2 review.)

usage: pit8253_latch_probe.py <gxemul-binary> <four-byte-raw-stub> [--learn]
"""
import os, pty, re, select, sys, time

BIN   = sys.argv[1]
STUB  = sys.argv[2]
LEARN = "--learn" in sys.argv

CODE = 0x00008000
DATA = 0x00009000
NOP  = 0xE1A00000
NOPTXT = "mov r0,r0"

MMU_OFF = [
    (0x00, 0xEE110F10, "mrc 15,0,r0,cr1,cr0,0", "read CP15 c1"),
    (0x04, 0xE3C00001, "bic r0,r0,#1",          "clear the MMU enable bit"),
    (0x08, 0xEE010F10, "mcr 15,0,r0,cr1,cr0,0", "MMU OFF -> VA == PA"),
]
MMU_NOP = [
    (0x00, NOP, NOPTXT, "arm T: MMU LEFT ON -- the negative control"),
    (0x04, NOP, NOPTXT, ""),
    (0x08, NOP, NOPTXT, ""),
]

MOVR1 = lambda imm: (0xE3A01000 | imm)          # mov r1,#imm   (imm8, no rotate)
#  #440: the disassembler prints a zero immediate as "#0", NOT "#0x0" -- the
#  committed body() hardcoded that at 0x5c.  Arm Z writes a zero counter byte, so
#  the formatting has to be shared rather than rediscovered.  Row E would have
#  caught it, but as a DISASSEMBLY MISMATCH, i.e. as a probe bug wearing the
#  costume of a device bug.
MOVTXT = lambda imm: "mov r1,#0" if imm == 0 else "mov r1,#0x%x" % imm
STRB43 = (0xE5C01043, "strb r1,[r0,#67]")       # MODE  <- r1
STRB40 = (0xE5C01040, "strb r1,[r0,#64]")       # CNTR0 <- r1


#  #440: controls C1/C2 and the A1 device signature, lifted VERBATIM out of body()
#  so that every arm carries its own controls.  Arms D/F/T must go on measuring
#  exactly what they measured before this was extracted -- that is the check.
#
#  A1 survives the flip-flop fix on purpose: the MODE<-0x34 at 0x38 rewinds the
#  selector under BOTH the old one-way clear and the new flip-flop, so A1 stays a
#  control and never doubles as the thing under test.
PROLOGUE = [
    (0x0c, 0xEE113F10, "mrc 15,0,r3,cr1,cr0,0", "C2: read CP15 c1 BACK -- measures MMU state"),
    (0x10, 0xE3A0047C, "mov r0,#0x7c000000",    "ISA portbase (bus_pci.c:459/476)"),
    (0x14, 0xE3A04A09, "mov r4,#0x9000",        "scratch RAM"),
    (0x18, 0xE5945000, "ldr r5,[r4]",           "C1 liveness: plain RAM, expect 0x11223344"),

    #  ---- A1 device signature: a value RAM cannot produce -------------------
    #  MODE<-0x34 (16BIT), then two byte writes to the SAME address: 0xAA then 0x55.
    #  dev_8253.c:117-124 puts 0xAA in the LOW half and 0x55 in the HIGH half
    #  (counter=0x55AA); MODE<-0x34 again rewinds the LSB/MSB selector, so the read
    #  returns 0xAA -- the byte from TWO writes ago.  RAM would return 0x55, and an
    #  ABSENT device would return 0x00.  Nonzero and specific, deliberately.
    (0x1c, MOVR1(0x34), "mov r1,#0x34",         "TIMER_SEL0|16BIT|RATEGEN"),
    (0x20, STRB43[0],   STRB43[1],              "MODE <- 0x34"),
    (0x24, MOVR1(0xAA), "mov r1,#0xaa",         ""),
    (0x28, STRB40[0],   STRB40[1],              "CNTR0 LSB <- 0xAA"),
    (0x2c, MOVR1(0x55), "mov r1,#0x55",         ""),
    (0x30, STRB40[0],   STRB40[1],              "CNTR0 MSB <- 0x55  (counter=0x55AA)"),
    (0x34, MOVR1(0x34), "mov r1,#0x34",         ""),
    (0x38, STRB43[0],   STRB43[1],              "MODE <- 0x34 again (rewind selector)"),
    (0x3c, 0xE5D08040,  "ldrb r8,[r0,#64]",     "A1: expect 0xAA (device) not 0x55 (RAM)"),
]


def body(lo, hi):
    """The guest sequence.  `lo`/`hi` are the two counter bytes a driver writes."""
    return PROLOGUE + [
    #  ---- program counter 0 the way a real driver does ----------------------
    (0x40, MOVR1(0x34), "mov r1,#0x34",         ""),
    (0x44, STRB43[0],   STRB43[1],              "MODE <- 0x34"),
    (0x48, MOVR1(lo),   "mov r1,#0x%x" % lo,    "CNTR0 <- low byte"),
    (0x4c, STRB40[0],   STRB40[1],              ""),
    (0x50, MOVR1(hi),   "mov r1,#0x%x" % hi,    "CNTR0 <- high byte"),
    (0x54, STRB40[0],   STRB40[1],              ""),
    (0x58, 0xE5D09043,  "ldrb r9,[r0,#67]",     "M1: mode_byte after programming"),

    #  ---- THE SYMPTOM: the standard counter-latch command -------------------
    #  OpenBSD clock.c:206-210 gettick():  outb(TIMER_MODE, TIMER_SEL0|TIMER_LATCH)
    #  then lo=inb(TIMER_CNTR0); hi=inb(TIMER_CNTR0); return (hi<<8)|lo;
    #  TIMER_LATCH is 0x00 (i8253reg.h:95) -- a COMMAND, not an error.
    (0x5c, MOVR1(0x00), "mov r1,#0",            "TIMER_SEL0|TIMER_LATCH"),
    (0x60, STRB43[0],   STRB43[1],              "MODE <- 0x00  (LATCH counter 0)"),
    (0x64, 0xE5D02043,  "ldrb r2,[r0,#67]",     "M2 (pitclobber): mode_byte AFTER the latch"),
    (0x68, 0xE5D06040,  "ldrb r6,[r0,#64]",     "L1 (pitlatch): gettick() low byte"),
    (0x6c, 0xE5D07040,  "ldrb r7,[r0,#64]",     "L2 (pitlatch): gettick() high byte"),
    ]


def body_flip(lo, hi):
    """#440 `pitflip`: ONE mode write, then TWO full 16-bit write pairs, then a
    16-bit read pair.  Nothing latches, so #439's path is not involved at all and
    this measures the selector by itself.

    A real 8254's flip-flop ALTERNATES, so pair 2 lands LSB-then-MSB exactly as
    pair 1 did: one recompute per pair, and the read pair returns the reload.
    """
    return PROLOGUE + [
    (0x40, MOVR1(0x34), MOVTXT(0x34),           ""),
    (0x44, STRB43[0],   STRB43[1],              "MODE <- 0x34  (the ONLY mode write)"),
    (0x48, MOVR1(lo),   MOVTXT(lo),             ""),
    (0x4c, STRB40[0],   STRB40[1],              "pair 1 LSB"),
    (0x50, MOVR1(hi),   MOVTXT(hi),             ""),
    (0x54, STRB40[0],   STRB40[1],              "pair 1 MSB  -> recompute #1"),
    (0x58, MOVR1(lo),   MOVTXT(lo),             ""),
    (0x5c, STRB40[0],   STRB40[1],              "pair 2 LSB  <- lands in the HIGH half pre-fix"),
    (0x60, MOVR1(hi),   MOVTXT(hi),             ""),
    (0x64, STRB40[0],   STRB40[1],              "pair 2 MSB"),
    (0x68, 0xE5D06040,  "ldrb r6,[r0,#64]",     "W1: readback low  byte"),
    (0x6c, 0xE5D07040,  "ldrb r7,[r0,#64]",     "W2: readback high byte"),
    (0x70, 0xE5D09043,  "ldrb r9,[r0,#67]",     "M1: mode_byte after all of it"),
    ]


def body_ilv(lo, hi):
    """#440: the i8254 datasheet's own p. 8 interleave --

        1) Read least significant byte   2) Write new least significant byte
        3) Read most significant byte    4) Write new most significant byte

    -- which it calls a valid sequence.  ONE shared read/write flip-flop cannot
    produce it (step 1 would advance the selector past step 2's LSB), so this arm
    is what makes two independent flip-flops a measurement rather than a taste.

    Counter is programmed to (hi<<8)|lo, then steps 1-4 rewrite it to 0x4011.
    """
    return PROLOGUE + [
    (0x40, MOVR1(0x34), MOVTXT(0x34),           ""),
    (0x44, STRB43[0],   STRB43[1],              "MODE <- 0x34  (rewinds both flip-flops)"),
    (0x48, MOVR1(lo),   MOVTXT(lo),             ""),
    (0x4c, STRB40[0],   STRB40[1],              "write LSB"),
    (0x50, MOVR1(hi),   MOVTXT(hi),             ""),
    (0x54, STRB40[0],   STRB40[1],              "write MSB -> counter = 0x2e9c"),
    (0x58, 0xE5D06040,  "ldrb r6,[r0,#64]",     "I1: step 1, read LSB       expect 0x9c"),
    (0x5c, MOVR1(0x11), MOVTXT(0x11),           ""),
    (0x60, STRB40[0],   STRB40[1],              "I2: step 2, write new LSB -> 0x2e11"),
    (0x64, 0xE5D07040,  "ldrb r7,[r0,#64]",     "I3: step 3, read MSB       expect 0x2e"),
    (0x68, MOVR1(0x40), MOVTXT(0x40),           ""),
    (0x6c, STRB40[0],   STRB40[1],              "I4: step 4, write new MSB -> 0x4011"),
    (0x70, 0xE5D02040,  "ldrb r2,[r0,#64]",     "I5: readback LSB   expect 0x11"),
    (0x74, 0xE5D09040,  "ldrb r9,[r0,#64]",     "I6: readback MSB   expect 0x40"),
    ]


def body_rewind(lo, hi, port, cw):
    """#440 PASS 2: does a Control Word rewind the WRITE flip-flop, for THIS counter?

    *** THE ONLY ARM THAT COVERS THE CONTROL-WORD REWIND.  Without it, deleting

            d->wr_msb[d->counter_select] = 0;

    passes every other row in this file. ***  Two seats found that mutant independently -- one
    by building it (readback 0x1140 for 0x4011, and the guest gets 265 Hz where it asked for
    73), one by reading -- and neither the write-pair arms nor the interleave arm can see it,
    because a COMPLETE pair returns the flip-flop to LSB on its own.  Only an ABANDONED pair
    leaves it at MSB where the rewind is the thing that matters.

    The sequence is the datasheet's own convention 1 (p. 8: "the Control Word must be written
    before the initial count is written"), applied to a counter left mid-pair:

        Control Word, write LSB, Control Word, write LSB, write MSB

    A correct model rewinds at the second Control Word, so the last two bytes are LSB then MSB
    and the counter reads back 0x4011.  Without the rewind the third write is taken as an MSB
    and the bytes land swapped.

    PARAMETERISED BY COUNTER on purpose.  The sibling mutant replaces d->counter_select with a
    literal 0 in the rewind, which a counter-0-only arm cannot see -- it too passed all ten
    rows.  The comment in dev_8253.c claims the rewind is "per counter, like the hardware", so
    the detector has to exercise a second counter or that sentence is unbacked.
    """
    strb = (0xE5C01000 | port, "strb r1,[r0,#%d]" % port)
    ldrb = lambda rn: (0xE5D00000 | (rn << 12) | port, "ldrb r%d,[r0,#%d]" % (rn, port))
    return PROLOGUE + [
    (0x40, MOVR1(cw),   MOVTXT(cw),             ""),
    (0x44, STRB43[0],   STRB43[1],              "MODE <- 0x%02x  (16-bit, this counter)" % cw),
    (0x48, MOVR1(lo),   MOVTXT(lo),             ""),
    (0x4c, strb[0],     strb[1],                "write LSB -- pair now HALF DONE"),
    (0x50, MOVR1(cw),   MOVTXT(cw),             ""),
    (0x54, STRB43[0],   STRB43[1],              "MODE <- 0x%02x AGAIN: abandons the pair" % cw),
    (0x58, MOVR1(0x11), MOVTXT(0x11),           ""),
    (0x5c, strb[0],     strb[1],                "write LSB -- MSB iff the rewind happened"),
    (0x60, MOVR1(0x40), MOVTXT(0x40),           ""),
    (0x64, strb[0],     strb[1],                "write MSB -> counter = 0x4011"),
    (0x68, ldrb(6)[0],  ldrb(6)[1],             "W1: readback LSB   expect 0x11"),
    (0x6c, ldrb(7)[0],  ldrb(7)[1],             "W2: readback MSB   expect 0x40"),
    ]


def body_latch(lo, hi):
    """#440: does a latch command RELEASE?  Program the counter, latch it, then
    read FOUR times.  Reads 1-2 are the two bytes the 16-bit format calls for and
    are 0 (there is no captured count -- #439, deliberately, unchanged here).
    Reads 3-4 must be the counter again: i8254 p. 7, the count "is held in the
    latch until it is read by the CPU ... then unlatched automatically".

    #439 cleared latched[] only on a mode write, so reads 3-4 stayed 0 for ever.
    """
    return PROLOGUE + [
    (0x40, MOVR1(0x34), MOVTXT(0x34),           ""),
    (0x44, STRB43[0],   STRB43[1],              "MODE <- 0x34"),
    (0x48, MOVR1(lo),   MOVTXT(lo),             ""),
    (0x4c, STRB40[0],   STRB40[1],              "CNTR0 LSB"),
    (0x50, MOVR1(hi),   MOVTXT(hi),             ""),
    (0x54, STRB40[0],   STRB40[1],              "CNTR0 MSB -> counter = 0x2e9c"),
    (0x58, MOVR1(0x00), MOVTXT(0x00),           "TIMER_SEL0|TIMER_LATCH"),
    (0x5c, STRB43[0],   STRB43[1],              "MODE <- 0x00  (LATCH counter 0)"),
    (0x60, 0xE5D06040,  "ldrb r6,[r0,#64]",     "K1: latched byte 1   expect 0x00"),
    (0x64, 0xE5D07040,  "ldrb r7,[r0,#64]",     "K2: latched byte 2   expect 0x00, RELEASES"),
    (0x68, 0xE5D02040,  "ldrb r2,[r0,#64]",     "K3: AFTER the latch  expect 0x9c, not 0"),
    (0x6c, 0xE5D09040,  "ldrb r9,[r0,#64]",     "K4: AFTER the latch  expect 0x2e"),
    ]


def body_mid(lo, hi):
    """#440: the LATCH lands BETWEEN the two halves of a 16-bit read pair.

    This is the one sequence where #439 and #440 actually meet, so it is measured
    rather than reasoned about.  Read 1 takes the LSB and advances the read
    flip-flop; the latch command then arrives mid-pair; read 2 is therefore the
    MSB half, which is the last byte the format calls for, so it both completes
    the guest's pair AND releases the latch.  The pair that follows must read
    normally again.

    Real hardware would hand back the latched count's high byte at read 2 where
    this returns 0x00 -- that is the documented "there is no live count" limit
    (#439), NOT a state-machine defect.  What this arm asserts is the STATE
    MACHINE: that the pair completes and the latch lets go.
    """
    return PROLOGUE + [
    (0x40, MOVR1(0x34), MOVTXT(0x34),           ""),
    (0x44, STRB43[0],   STRB43[1],              "MODE <- 0x34"),
    (0x48, MOVR1(lo),   MOVTXT(lo),             ""),
    (0x4c, STRB40[0],   STRB40[1],              "CNTR0 LSB"),
    (0x50, MOVR1(hi),   MOVTXT(hi),             ""),
    (0x54, STRB40[0],   STRB40[1],              "CNTR0 MSB -> counter = 0x2e9c"),
    (0x58, 0xE5D06040,  "ldrb r6,[r0,#64]",     "N1: first half of a read pair  expect 0x9c"),
    (0x5c, MOVR1(0x00), MOVTXT(0x00),           ""),
    (0x60, STRB43[0],   STRB43[1],              "MODE <- 0x00: LATCH, MID-PAIR"),
    (0x64, 0xE5D07040,  "ldrb r7,[r0,#64]",     "N2: second half  expect 0x00, RELEASES"),
    (0x68, 0xE5D02040,  "ldrb r2,[r0,#64]",     "N3: next pair LSB  expect 0x9c"),
    (0x6c, 0xE5D09040,  "ldrb r9,[r0,#64]",     "N4: next pair MSB  expect 0x2e"),
    ]


def tail_for(b):
    """#440: landing pad one word past whichever body was built -- the bodies are
    no longer all the same length.  Planted, never stepped."""
    return [(b[-1][0] + 4, NOP, NOPTXT, "landing pad -- planted, never stepped")]


REGS_OF_INTEREST = (0, 1, 2, 3, 5, 6, 7, 8, 9)
COMPLAINT = "huh? reading from counter"
#  #440: every recompute the device logs.  The FIRST match in every body is the
#  A1 signature's own 0x55AA; the ones under test follow it.
RECOMPUTE = re.compile(r"8253: counter 0 set to (\d+) \((\d+) Hz\)")
MMUOFF = ("D", "F", "P", "Z", "I", "L", "M")


def run_arm(prog):
    pid, fd = pty.fork()
    if pid == 0:
        os.execvp(BIN, [BIN, "-V", "-T", "-E", "cats", "-M", "32",
                        "0x%x:%s" % (CODE, STUB)])
        os._exit(127)
    buf = ""
    dead = [False]

    def rd(t=0.4):
        nonlocal buf
        r, _, _ = select.select([fd], [], [], t)
        if fd not in r:
            return True
        try:
            d = os.read(fd, 65536)
        except OSError:
            dead[0] = True
            return False
        if not d:
            dead[0] = True
            return False
        buf += d.decode("latin1", "replace")
        return True

    #  gate_hygiene.sh pins the CANONICAL #392 call form as a literal
    #  `return wait(mark=_mark, echo=<x> if <x> else None)`; timeout goes last.
    def wait(mark=0, echo=None, timeout=60):
        t = time.time()
        while time.time() - t < timeout:
            if not rd():
                return False
            resp = buf[mark:]
            if echo is not None and echo not in resp:
                continue
            if len(buf) > mark and resp.rstrip().endswith("GXemul>"):
                return True
        return False

    def send(x, timeout=60):
        b = (x + "\n").encode("latin1")
        _mark = len(buf)
        n = 0
        try:
            while n < len(b):
                n += os.write(fd, b[n:])
        except OSError:
            dead[0] = True
            return False
        return wait(mark=_mark, echo=x if x else None)

    status, regs, badis, seen = "?", {}, [], []
    if not wait(timeout=120):
        status = "NO-PROMPT"
    else:
        send("put w 0x%08x, 0x%08x" % (DATA, 0x11223344))
        for off, word, _t, _c in prog:
            send("put w 0x%08x, 0x%08x" % (CODE + off, word))
        send("pc=0x%08x" % CODE)
        status = "SURVIVED"
        for off, word, text, _c in prog[:-1]:
            mark = len(buf)
            if not send("step 1", timeout=30) or dead[0]:
                status = "HOST-DIED"
                break
            seg = buf[mark:]
            m = re.search(r"%08x:\s+%08x\s+([^\r\n<]+)" % (CODE + off, word), seg)
            got = re.sub(r"\s+", " ", m.group(1)).strip() if m else "(no step line)"
            seen.append((off, word, got))
            if text is not None and got != text:
                badis.append("0x%02x planted 0x%08x -> %r, expected %r"
                             % (off, word, got, text))
        if status == "SURVIVED":
            mark = len(buf)
            if send("reg", timeout=30) and not dead[0]:
                for n in REGS_OF_INTEREST:
                    mm = re.search(r"\br%d\s*=\s*0x([0-9a-fA-F]+)" % n, buf[mark:])
                    if mm:
                        regs[n] = int(mm.group(1), 16)
            else:
                status = "HOST-DIED" if dead[0] else "NO-REG"

    lines = re.findall(r"(\[[^\r\n\]]*8253[^\r\n\]]*\])", buf)
    try:
        os.write(fd, b"quit\n")
        time.sleep(0.3)
    except OSError:
        pass
    try:
        os.close(fd)
    except OSError:
        pass
    try:
        os.waitpid(pid, 0)
    except Exception:
        pass
    return status, regs, lines, badis, seen


ARMS = [
    ("D", MMU_OFF, body,       0x9c, 0x2e, "MMU off, counter 0x2e9c = TIMER_DIV(100)"),
    ("F", MMU_OFF, body,       0xff, 0xff, "MMU off, counter 0xffff = findcpuspeed() shape"),
    ("T", MMU_NOP, body,       0x9c, 0x2e, "MMU LEFT ON -- negative control"),
    ("P", MMU_OFF, body_flip,  0x9c, 0x2e, "#440 pitflip: two write pairs, 0x2e9c"),
    ("Z", MMU_OFF, body_flip,  0x00, 0x2e, "#440 pitflip: two write pairs, 0x2e00 (low byte 0)"),
    ("I", MMU_OFF, body_ilv,   0x9c, 0x2e, "#440 pitflip: the i8254 p.8 read/write interleave"),
    ("L", MMU_OFF, body_latch, 0x9c, 0x2e, "#440: is the counter latch ever RELEASED?"),
    ("M", MMU_OFF, body_mid,   0x9c, 0x2e, "#440: a LATCH mid-way through a 16-bit read pair"),
    #  #440 pass 2: TWO counters, because two DIFFERENT one-line mutants passed all ten rows
    #  without them -- dropping the write rewind, and hardcoding counter 0 in it.  Counter 2
    #  (port 66, Control Word 0xb6) is what makes "per counter" a measurement.
    ("W", MMU_OFF, lambda lo, hi: body_rewind(lo, hi, 64, 0x34), 0x9c, 0x2e,
     "#440 pass 2: Control Word rewinds the WRITE flip-flop, counter 0"),
    ("X", MMU_OFF, lambda lo, hi: body_rewind(lo, hi, 66, 0xb6), 0x9c, 0x2e,
     "#440 pass 2: ...and counter 2, so the rewind is per-counter"),
]

#  #440: what each write-pair arm programmed, for the readback rows.
EXPECT = {"P": 0x2e9c, "Z": 0x2e00}


def main():
    print("=" * 76)
    print("pit8253 latch probe -- %s" % BIN)
    print("=" * 76)
    R = {}
    for name, head, bodyfn, lo, hi, desc in ARMS:
        b = bodyfn(lo, hi)
        st, regs, lines, bad, seen = run_arm(head + b + tail_for(b))
        R[name] = (st, regs, lines, bad)
        print("\n--- arm %s : %s ---" % (name, desc))
        print("    status %s" % st)
        if LEARN:
            for off, word, got in seen:
                print("      0x%02x  %08x  %s" % (off, word, got))
        if bad and name != "T":       # arm T aborts at the first device access by design
            print("    *** DISASSEMBLY MISMATCH (hand-assembled-encoding trap) ***")
            for b in bad:
                print("        " + b)
        print("    regs " + ", ".join("r%d=0x%x" % (n, v) for n, v in sorted(regs.items())))
        for c in dict.fromkeys(lines):
            print("      %-58s x%d" % (c, lines.count(c)))

    stD, rD, lD, badD = R["D"]
    stF, rF, lF, _    = R["F"]
    stT, rT, lT, _    = R["T"]
    rP, rZ, rI, rL, rM = (R[a][1] for a in ("P", "Z", "I", "L", "M"))

    def recomputes(a):
        """#440: (count, hz) per recompute in arm `a`, A1's own signature DROPPED.

        A1's write pair is always the first and always 0x55AA=21930 at 54 Hz.
        That is ASSERTED rather than assumed: if it ever moves, every index here
        silently shifts, and a row that counts recomputes would be counting the
        wrong ones while still going green.  None means "did not lead with A1".
        """
        out = [(int(m.group(1)), int(m.group(2)))
               for m in (RECOMPUTE.search(l) for l in R[a][2]) if m]
        return out[1:] if out[:1] == [(21930, 54)] else None

    def gettick(r):
        return (r.get(7, 0) << 8) | r.get(6, 0)

    print("\n" + "=" * 76)
    print("CONTROLS  (if any is RED every row below is meaningless)")
    print("=" * 76)
    ok = True

    def row(tag, good, detail):
        nonlocal ok
        ok &= bool(good)
        print("  %-4s %-44s %s" % ("ok" if good else "FAIL", tag, detail))

    #  #440: the controls now cover EVERY MMU-off arm, not just D.  P/Z/I/L carry
    #  new hand-assembled encodings and make their own device accesses; a control
    #  proved only on arm D says nothing whatever about them.
    def per_arm(fmt, f):
        return " ".join(fmt % (a, f(R[a][1])) for a in MMUOFF)

    row("C1 liveness", all(R[a][1].get(5) == 0x11223344 for a in MMUOFF),
        "RAM through the same decode " + per_arm("%s=0x%x", lambda r: r.get(5, -1)))
    row("C2 MMU state", all((R[a][1].get(3, 1) & 1) == 0 for a in MMUOFF),
        "CP15 c1 bit0 " + per_arm("%s=0x%x", lambda r: r.get(3, -1)))
    row("A1 device signature", all(R[a][1].get(8) == 0xAA for a in MMUOFF),
        per_arm("%s=0x%x", lambda r: r.get(8, -1)) + "  (RAM 0x55, absent 0x00)")
    row("T  MMU-ON control", rT.get(8) != 0xAA and not lT,
        "r8=0x%x, 8253 log lines=%d" % (rT.get(8, -1), len(lT)))
    row("E  encodings", not any(R[a][3] for a in MMUOFF),
        "disassembly mismatches " + " ".join("%s=%d" % (a, len(R[a][3])) for a in MMUOFF))
    row("A2 recompute stream", all(recomputes(a) is not None for a in MMUOFF),
        "A1's own 0x55AA recompute leads every arm: " +
        " ".join("%s=%s" % (a, "y" if recomputes(a) is not None else "NO") for a in MMUOFF))

    print("\n" + "=" * 76)
    print("MEASURED")
    print("=" * 76)
    for nm, r, l in (("D", rD, lD), ("F", rF, lF)):
        n = sum(x.count(COMPLAINT) for x in l)
        print("  arm %s   M1 mode_byte after programming  0x%02x" % (nm, r.get(9, -1)))
        print("          M2 mode_byte after LATCH        0x%02x   <- pitclobber"
              % r.get(2, -1))
        print("          L1/L2 latched bytes             0x%02x 0x%02x   <- pitlatch"
              % (r.get(6, -1), r.get(7, -1)))
        print("          gettick() would return          0x%04x" % gettick(r))
        print("          '%s' lines        %d" % (COMPLAINT, n))
        if nm == "F":
            d = 0xffff - gettick(r)
            print("          clock.c:344 divisor (0xffff-gettick) = %d %s"
                  % (d, "*** ZERO -> guest divide-by-zero ***" if d == 0 else "(nonzero, safe)"))
        print()

    #  ---------------------------------------------------------- #440 arms
    for a in ("P", "Z"):
        r = R[a][1]
        print("  arm %s   readback (r7<<8)|r6            0x%04x   (programmed 0x%04x)"
              % (a, (r.get(7, 0) << 8) | r.get(6, 0), EXPECT[a]))
        print("          mode_byte after 2 pairs        0x%02x" % r.get(9, -1))
        print("          recomputes after A1's          %s" % (recomputes(a),))
        print()
    print("  arm I   step1 read LSB  r6=0x%02x  (expect 0x9c)" % rI.get(6, -1))
    print("          step3 read MSB  r7=0x%02x  (expect 0x2e)" % rI.get(7, -1))
    print("          readback        0x%04x  (expect 0x4011)"
          % ((rI.get(9, 0) << 8) | rI.get(2, 0)))
    print()
    print("  arm L   latched bytes   r6=0x%02x r7=0x%02x  (expect 0x00 0x00)"
          % (rL.get(6, -1), rL.get(7, -1)))
    print("          AFTER the latch r2=0x%02x r9=0x%02x  (expect 0x9c 0x2e)"
          % (rL.get(2, -1), rL.get(9, -1)))
    print()
    print("  arm M   pair half 1     r6=0x%02x  (expect 0x9c) <- BEFORE the latch"
          % rM.get(6, -1))
    print("          pair half 2     r7=0x%02x  (expect 0x00) <- latched, releases"
          % rM.get(7, -1))
    print("          next pair       r2=0x%02x r9=0x%02x  (expect 0x9c 0x2e)"
          % (rM.get(2, -1), rM.get(9, -1)))
    print()

    print("=" * 76)
    print("VERDICT ROWS")
    print("=" * 76)
    nD = sum(x.count(COMPLAINT) for x in lD)
    #  ABSENT DATA MUST FAIL, NOT PASS.  The first draft compared rD.get(2) to
    #  rD.get(9); when the emulator never started, both were the -1 default and the
    #  row reported ok on a run that had measured nothing.  Every value a row
    #  consults is required to be present first.
    #  #440: R0 now demands EVERY arm, not just D and F -- an arm that never ran
    #  leaves .get() defaults behind, which is the same absent-data trap again.
    have = (all(k in rD for k in (2, 9))
            and all(R[a][0] == "SURVIVED" for a, *_ in ARMS)
            and all(recomputes(a) is not None for a in MMUOFF))
    row("R0 the run produced data", have,
        " ".join("%s=%s" % (a, R[a][0]) for a, *_ in ARMS))
    #  R1/R2 fail on the PRE-FIX build (that is the reproduction).  R3 passes pre-fix
    #  and post-fix but fails on the plausible OVER-fix -- un-clobbering mode_byte
    #  without also declining to hand back the reload value.  A detector that only
    #  had R1/R2 would go green on that mutant, which is the vacuity trap.
    row("R1 latch preserves programming", have and rD.get(2) == rD.get(9),
        "mode_byte after latch 0x%02x, after programming 0x%02x"
        % (rD.get(2, -1), rD.get(9, -1)))
    row("R2 latch is not an error", have and nD == 0,
        "%d '%s' lines" % (nD, COMPLAINT))
    row("R3 latched read is not the reload", have and (0xffff - gettick(rF)) != 0,
        "findcpuspeed divisor = %d" % (0xffff - gettick(rF)))

    #  ------------------------------------------------------ #440 pitflip rows
    #  Every one of these FAILS on the committed pre-#440 build; that is the
    #  reproduction.  R7 additionally fails on the plausible SMALLER fix (one
    #  flip-flop shared by reads and writes), which R4/R5/R6 all pass -- so R7 is
    #  the row that stops this being over-modelled by taste rather than measured.
    rb = lambda a: (R[a][1].get(7, 0) << 8) | R[a][1].get(6, 0)
    row("R4 16-bit readback is the reload",
        have and all(rb(a) == EXPECT[a] for a in ("P", "Z")),
        " ".join("%s=0x%04x/0x%04x" % (a, rb(a), EXPECT[a]) for a in ("P", "Z")))
    row("R5 one recompute per write pair",
        have and all(len(recomputes(a)) == 2 for a in ("P", "Z")),
        " ".join("%s=%d" % (a, len(recomputes(a))) for a in ("P", "Z")))
    row("R6 no transient count of zero",
        have and not [x for a in ("P", "Z") for x in recomputes(a) if x[0] == 0],
        "arm Z recomputes %s" % (recomputes("Z"),))
    row("R7 read and write flip-flops are separate",
        have and rI.get(6) == 0x9c and rI.get(7) == 0x2e
        and ((rI.get(9, 0) << 8) | rI.get(2, 0)) == 0x4011,
        "i8254 p.8 interleave: r6=0x%02x r7=0x%02x readback=0x%04x"
        % (rI.get(6, -1), rI.get(7, -1), (rI.get(9, 0) << 8) | rI.get(2, 0)))
    #  R9 is the ONE sequence where #439 and #440 meet, so it is measured.  Half 1
    #  must still be the LSB (pre-fix the selector was stuck at MSB and returned
    #  0x2e), half 2 completes the guest's pair AND releases, and the pair after it
    #  must read normally -- pre-fix it stayed 0x00 for ever.
    row("R9 a mid-pair latch completes the pair and lets go",
        have and rM.get(6) == 0x9c and rM.get(7) == 0x00
        and rM.get(2) == 0x9c and rM.get(9) == 0x2e,
        "halves 0x%02x 0x%02x then next pair 0x%02x 0x%02x"
        % (rM.get(6, -1), rM.get(7, -1), rM.get(2, -1), rM.get(9, -1)))
    #  #440 pass 2.  R10/R11 are the ONLY rows covering the control-word rewind; two seats
    #  independently produced one-line mutants that passed R0-R9 while swapping a legal
    #  guest's counter bytes.  R11 exists separately from R10 because the sibling mutant
    #  (a literal 0 for d->counter_select in the rewind) leaves counter 0 CORRECT and breaks
    #  only the others -- so a single-counter row cannot see it.
    rW, rX = R["W"][1], R["X"][1]
    row("R10 a Control Word rewinds the write flip-flop",
        all(k in rW for k in (6, 7)) and rW.get(6) == 0x11 and rW.get(7) == 0x40,
        "counter 0 readback 0x%02x%02x (expect 0x4011)" % (rW.get(7, 0), rW.get(6, 0)))
    row("R11 ...and it does so PER COUNTER, not just counter 0",
        all(k in rX for k in (6, 7)) and rX.get(6) == 0x11 and rX.get(7) == 0x40,
        "counter 2 readback 0x%02x%02x (expect 0x4011)" % (rX.get(7, 0), rX.get(6, 0)))

    row("R8 the latch is released by reading it",
        have and rL.get(6) == 0x00 and rL.get(7) == 0x00
        and rL.get(2) == 0x9c and rL.get(9) == 0x2e,
        "latched 0x%02x 0x%02x then 0x%02x 0x%02x (must not stay 0)"
        % (rL.get(6, -1), rL.get(7, -1), rL.get(2, -1), rL.get(9, -1)))

    print("\n  %s" % ("PASS" if ok else "FAIL"))
    sys.exit(0 if ok else 1)


main()
