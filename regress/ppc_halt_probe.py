#!/usr/bin/env python3
"""Round 87's measuring instrument: which legal PowerPC FP encodings stop the emulator.

Prints one line per row:  <name> <got> <want> ok|FAIL
then PPC_HALT_CONTROL=OK|DEAD and PPC_HALT_RESULT=<passed>/<total>.
gate_ppc_halt.sh does the asserting.

What a halt IS here
-------------------
`cpu_ppc_instr.c`'s translator ends both floating-point blocks with
`default: goto bad;`, and `bad:` is the shared label in `cpu_dyntrans.c` that
prints "UNIMPLEMENTED instruction at 0x..." and sets `cpu->running = 0`. So a
legal encoding the decoder does not know does not raise a program exception the
guest could handle -- it stops the whole emulator. Same class as rounds
70/70B/78/79/80 on other architectures.

How the outcome is classified
-----------------------------
A halt is read off that message, never off a memory marker. The SuperH sweep
(round 80) learned this the hard way: a marker-only classifier cannot tell
"the emulator stopped" from "the instruction ran and simply did not reach the
store", and after a fix lands it reports every repaired row as still broken.
Each row therefore reports one of three named outcomes:

  alive    -- stepped, and the session still answers a dump afterwards
  HALTED   -- the dyntrans abort message appeared      <- the defect
  DEAD     -- the session stopped answering entirely   <- instrument failure

Row classes
-----------
  CTRL  -- an instruction the decoder already handled. These are what make a
           HALTED verdict mean anything: if a control halts, the rig is broken
           (wrong machine, no FP, bad address) and no other row may be
           believed. Round 76 shipped a probe with no control and every mask
           "halted", including the nine that worked.
  FIXED -- halted on the build before #326, must run now. `want` is alive, so
           the row proves the fix today and catches its regression later.
  PEND  -- STILL HALTS, on purpose. #326 stopped short of these, and the row
           records that with `want` = HALTED rather than omitting it. Two
           reasons to keep them: the queue stays honest about what is broken,
           and the row FAILS the day one is implemented, which is the prompt
           to reclassify it instead of leaving a stale expectation in place.

           Why each is deferred is not "we ran out of time":
             fctid/fctidz/fcfid  64-bit-only instructions. The machine this
                                 gate drives is a 32-bit G4, where real
                                 silicon takes a program interrupt -- so the
                                 fix is the missing exception model, and
                                 implementing them unconditionally would make
                                 the model LESS faithful, not more.
             fsqrt/fsqrts        not in the G4's instruction groups; same
                                 argument.
             fres/frsqrte        estimate instructions, whose accuracy is
                                 implementation-defined within a bound.
             fcmpo, fnmadd,      no technical blocker -- these are a few dozen
             fnmsub, fmadds,     lines at the fidelity bar this file already
             fmsubs              ships (fadds and fmuls are aliases of their
                                 double forms today). They are out of #326
                                 only for round size, and that is the honest
                                 reason to record. fmadds is the one to do
                                 first: gcc emits it for ordinary float
                                 arithmetic, so it is likely the most
                                 frequently executed instruction still here.

Encodings are built FROM FIELDS, never typed as hex
---------------------------------------------------
`enc()` below assembles primary opcode, register fields, extended opcode and
the Rc bit at their architectural positions, and every row prints the word it
produced. This is deliberate: hand-assembled instruction words have four times
in this project nearly produced a finding out of nothing, once reaching a
committed gate row that measured an empty register for months (see #325). A
row whose encoding is wrong here shows up as a wrong xo/frB in its own output
instead of as a plausible verdict.
"""
import os
import pty
import re
import select
import sys
import time

BIN = sys.argv[1]
IMAGES = sys.argv[2]
KERNEL = "netbsd401-macppc-GENERIC"

CODE = 0x8000
DEST = 0x9000


def enc(op, rt=0, ra=0, rb=0, frc=0, xo=0, rc=0):
    """Assemble one primary-opcode-59/63 form from its architectural fields.

    Big-endian bit numbering, MSB=0. Two forms share this encoder:

      A-form (fadd, fmul, fmadd, fsel ...):  opcode 0:5, FRT 6:10, FRA 11:15,
        FRB 16:20, FRC 21:25, XO 26:30 (five bits), Rc 31.
      X-form (frsp, fctiwz, fmr, mcrfs ...): opcode 0:5, FRT/BF 6:10,
        FRA/BFA 11:15, FRB 16:20, XO 21:30 (ten bits), Rc 31.

    Both put XO at LSB bit 1, so `xo << 1` serves either: an A-form's five-bit
    value lands in LSB 5:1 and leaves FRC's LSB 10:6 alone. Fields narrower
    than their slot are left-justified by the caller -- mcrfs's three-bit BF
    and BFA are passed as `BF << 2`, which is what puts them at 6:8 and 11:13.
    """
    return (((op & 63) << 26) | ((rt & 31) << 21) | ((ra & 31) << 16)
            | ((rb & 31) << 11) | ((frc & 31) << 6) | ((xo & 1023) << 1)
            | (rc & 1))


def decode(iw):
    """Re-derive the fields from the word, for the row's own printout.

    BOTH extended-opcode widths are printed, because reading only the ten-bit
    one makes every A-form row look mis-encoded: FRC sits at LSB 10:6, inside
    the ten-bit XO slot, so `fmadds` (five-bit XO 29, FRC 3) reads back as
    xo10=125. 125 & 31 == 29, and the row is correct -- but a printout that
    shows only 125 is exactly the kind of thing that gets chased as a bug or,
    worse, hides a genuinely wrong field behind an expected-looking number.
    Read xo5 for A-forms and xo10 for X-forms.
    """
    return (dict(op=(iw >> 26) & 63, rt=(iw >> 21) & 31, ra=(iw >> 16) & 31,
                 rb=(iw >> 11) & 31, frc=(iw >> 6) & 31,
                 xo10=(iw >> 1) & 1023, xo5=(iw >> 1) & 31, rc=iw & 1))


def run(iword):
    """Step one instruction; return "alive", "HALTED", or "DEAD"."""
    pid, fd = pty.fork()
    if pid == 0:
        os.chdir(IMAGES)
        os.execvp(BIN, [BIN, "-V", "-E", "macppc", "-e", "g4", "-M", "64",
                        KERNEL])
        os._exit(127)
    buf = ""

    def rd(t=0.4):
        nonlocal buf
        r, _, _ = select.select([fd], [], [], t)
        if fd not in r:
            return True
        try:
            d = os.read(fd, 65536)
        except OSError:
            return False
        if not d:
            return False
        buf += d.decode("latin1", "replace")
        return True

    def wait(timeout=45):
        t = time.time()
        while time.time() - t < timeout:
            if not rd():
                return False
            if buf.rstrip().endswith(">"):
                return True
        return False

    def send(s):
        b = (s + "\n").encode("latin1")
        n = 0
        while n < len(b):
            n += os.write(fd, b[n:])
        wait()

    if not wait(60):
        try:
            os.kill(pid, 9)
            os.waitpid(pid, 0)
        except Exception:
            pass
        return "DEAD"

    #  msr=0x2000 is mandatory: without FP available every one of these takes
    #  the FPU-unavailable exception and the sweep measures that instead of the
    #  decode. Seed f1/f2/f3 so an implemented instruction has real operands.
    for c in ["msr=0x2000",
              "f1=0x3ff0000000000000",       # 1.0
              "f2=0x4000000000000000",       # 2.0
              "f3=0x4008000000000000",       # 3.0
              "r3=0x%x" % DEST,
              "put w 0x%x, 0x%08x" % (CODE, iword),
              "pc=0x%x" % CODE,
              "step 1"]:
        send(c)

    halted = "UNIMPLEMENTED instruction" in buf

    #  Prove the session still answers, so "not halted" cannot be read off a
    #  dead pty. A dump returning nothing is its own outcome, never "alive".
    responded = False
    for _ in range(3):
        mark = len(buf)
        send("dump 0x%x 0x%x" % (DEST, DEST + 16))
        if re.search(r"0x0*[0-9a-f]+\s+(?:[0-9a-f]{8}\s+)", buf[mark:]):
            responded = True
            break
        time.sleep(0.8)
        rd(0.8)

    try:
        os.write(fd, b"quit\n")
        time.sleep(0.3)
        os.kill(pid, 9)
        os.waitpid(pid, 0)
    except Exception:
        pass

    if halted:
        return "HALTED"
    return "alive" if responded else "DEAD"


#  ---------------------------------------------------------------------------
#  ROWS.  op, then the fields, then the extended opcode and Rc.
#
#  CTRL rows are instructions this decoder already implements. They are what
#  makes a HALTED verdict mean something: if a control row also reads HALTED,
#  the rig is broken (wrong machine, no FP, bad address) and no other row may
#  be believed. Round 76 shipped a probe without one and every mask "halted",
#  including the nine that worked.
#  ---------------------------------------------------------------------------
ROWS = [
    #  (name,               word,                                     class)

    #  --- controls: implemented, must stay alive ---
    ("ctrl fadd",     enc(63, rt=0, ra=1, rb=2, xo=21),               "CTRL"),
    ("ctrl fmr",      enc(63, rt=0, rb=1, xo=72),                     "CTRL"),
    ("ctrl fctiwz",   enc(63, rt=0, rb=1, xo=15),                     "CTRL"),
    ("ctrl mtfsf",    enc(63, rb=1, xo=711) | (0xff << 17),           "CTRL"),

    #  --- the record forms: Rc=1 is rejected for EVERY opcode-59/63 form,
    #      including the ones that work with Rc=0. `fadd.` is what a compiler
    #      emits whenever the result feeds a condition test.
    ("fadd. (Rc=1)",  enc(63, rt=0, ra=1, rb=2, xo=21, rc=1),         "FIXED"),
    ("frsp. (Rc=1)",  enc(63, rt=0, rb=1, xo=12, rc=1),               "FIXED"),
    ("fctiwz. (Rc=1)", enc(63, rt=0, rb=1, xo=15, rc=1),              "FIXED"),
    ("fmr. (Rc=1)",   enc(63, rt=0, rb=1, xo=72, rc=1),               "FIXED"),
    ("fadds. (Rc=1)", enc(59, rt=0, ra=1, rb=2, xo=21, rc=1),         "FIXED"),

    #  --- FPSCR control group: the guest's only way to read, set and clear
    #      FPSCR bits. frsp's own comment names mcrfs as the clearing path for
    #      the sticky VXSNAN #304 introduced, and mcrfs does not exist.
    ("mcrfs",         enc(63, rt=0 << 2, ra=1 << 2, xo=64),           "FIXED"),
    ("mtfsb0",        enc(63, rt=0, xo=70),                           "FIXED"),
    ("mtfsb1",        enc(63, rt=0, xo=38),                           "FIXED"),
    ("mtfsfi",        enc(63, rt=0, rb=0, xo=134),                    "FIXED"),

    #  --- converts ---
    ("fctiw",         enc(63, rt=0, rb=1, xo=14),                     "FIXED"),
    ("fctid",         enc(63, rt=0, rb=1, xo=814),                    "PEND"),
    ("fctidz",        enc(63, rt=0, rb=1, xo=815),                    "PEND"),
    ("fcfid",         enc(63, rt=0, rb=1, xo=846),                    "PEND"),

    #  --- fnabs is DEFINED in opcodes_ppc.h (PPC_63_FNABS 136) and has no
    #      case in the decoder: the define alone does nothing.
    ("fnabs",         enc(63, rt=0, rb=1, xo=136),                    "FIXED"),
    ("fcmpo",         enc(63, rt=0, ra=1, rb=2, xo=32),               "PEND"),

    #  --- arithmetic the decoder never learned. fmadds is the twin of fnabs:
    #      PPC_59_FMADDS is defined, and the five-bit switch has no case, so it
    #      falls through to a ten-bit switch whose only arm is `goto bad`.
    ("fmadds",        enc(59, rt=0, ra=1, rb=2, frc=3, xo=29),        "PEND"),
    ("fmsubs",        enc(59, rt=0, ra=1, rb=2, frc=3, xo=28),        "PEND"),
    #  #344: both were PEND with the probe's own note that they had no
    #  technical blocker. Two legal encodings that stopped the emulator.
    ("fnmadd",        enc(63, rt=0, ra=1, rb=2, frc=3, xo=31),        "FIXED"),
    ("fnmsub",        enc(63, rt=0, ra=1, rb=2, frc=3, xo=30),        "FIXED"),
    ("fsqrt",         enc(63, rt=0, rb=1, xo=22),                     "PEND"),
    ("fsqrts",        enc(59, rt=0, rb=1, xo=22),                     "PEND"),
    ("fsel",          enc(63, rt=0, ra=1, rb=2, frc=3, xo=23),        "FIXED"),
    ("fres",          enc(59, rt=0, rb=1, xo=24),                     "PEND"),
    ("frsqrte",       enc(63, rt=0, rb=1, xo=26),                     "PEND"),
]


def main():
    print("%-20s %-8s %-8s %-6s %s"
          % ("row", "got", "want", "class", "word/fields"))
    passed = 0
    control_ok = True
    results = []
    for name, iword, cls in ROWS:
        got = run(iword)
        f = decode(iword)
        #  PEND rows are the encodings #326 deliberately did NOT decode. They
        #  still stop the emulator, and the row records that rather than
        #  hiding it: `want` is HALTED, so the row passes today and FAILS the
        #  day one of them is implemented -- which is the prompt to move it
        #  out of this class instead of leaving a stale expectation behind.
        want = "HALTED" if cls == "PEND" else "alive"
        ok = (got == want)
        if cls == "CTRL" and not ok:
            control_ok = False
        passed += ok
        results.append((name, got, cls, ok))
        print("%-20s %-8s %-8s %-6s %08x op=%d xo10=%d xo5=%d rt=%d ra=%d "
              "rb=%d frc=%d rc=%d %s"
              % (name, got, want, cls, iword, f["op"], f["xo10"], f["xo5"],
                 f["rt"], f["ra"], f["rb"], f["frc"], f["rc"],
                 "ok" if ok else "FAIL"))
        sys.stdout.flush()

    print("PPC_HALT_CONTROL=%s" % ("OK" if control_ok else "DEAD"))
    print("PPC_HALT_RESULT=%d/%d" % (passed, len(ROWS)))


main()
