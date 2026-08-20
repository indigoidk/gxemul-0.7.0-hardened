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
STRB43 = (0xE5C01043, "strb r1,[r0,#67]")       # MODE  <- r1
STRB40 = (0xE5C01040, "strb r1,[r0,#64]")       # CNTR0 <- r1


def body(lo, hi):
    """The guest sequence.  `lo`/`hi` are the two counter bytes a driver writes."""
    return [
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


TAIL = [(0x70, NOP, NOPTXT, "landing pad -- planted, never stepped")]
REGS_OF_INTEREST = (0, 1, 2, 3, 5, 6, 7, 8, 9)
COMPLAINT = "huh? reading from counter"


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
    ("D", MMU_OFF, 0x9c, 0x2e, "MMU off, counter 0x2e9c = TIMER_DIV(100)"),
    ("F", MMU_OFF, 0xff, 0xff, "MMU off, counter 0xffff = findcpuspeed() shape"),
    ("T", MMU_NOP, 0x9c, 0x2e, "MMU LEFT ON -- negative control"),
]


def main():
    print("=" * 76)
    print("pit8253 latch probe -- %s" % BIN)
    print("=" * 76)
    R = {}
    for name, head, lo, hi, desc in ARMS:
        st, regs, lines, bad, seen = run_arm(head + body(lo, hi) + TAIL)
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

    row("C1 liveness", rD.get(5) == 0x11223344,
        "RAM through the same decode = 0x%x" % rD.get(5, -1))
    row("C2 MMU state", (rD.get(3, 1) & 1) == 0,
        "CP15 c1 read BACK = 0x%x (bit0 must be 0)" % rD.get(3, -1))
    row("A1 device signature", rD.get(8) == 0xAA,
        "0x%x  (RAM would be 0x55, absent 0x00)" % rD.get(8, -1))
    row("T  MMU-ON control", rT.get(8) != 0xAA and not lT,
        "r8=0x%x, 8253 log lines=%d" % (rT.get(8, -1), len(lT)))
    row("E  encodings", not badD, "%d disassembly mismatches in arm D" % len(badD))

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

    print("=" * 76)
    print("VERDICT ROWS")
    print("=" * 76)
    nD = sum(x.count(COMPLAINT) for x in lD)
    #  ABSENT DATA MUST FAIL, NOT PASS.  The first draft compared rD.get(2) to
    #  rD.get(9); when the emulator never started, both were the -1 default and the
    #  row reported ok on a run that had measured nothing.  Every value a row
    #  consults is required to be present first.
    have = all(k in rD for k in (2, 9)) and stD == "SURVIVED" and stF == "SURVIVED"
    row("R0 the run produced data", have,
        "arm D %s, arm F %s, registers %s"
        % (stD, stF, "present" if all(k in rD for k in (2, 9)) else "MISSING"))
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

    print("\n  %s" % ("PASS" if ok else "FAIL"))
    sys.exit(0 if ok else 1)


main()
