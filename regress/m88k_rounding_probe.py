#!/usr/bin/env python3
"""Gate 11's measuring instrument: m88k floating-point rounding on real guest code.

Prints one line per row:  <name> <got> <want> ok|FAIL
then M88K_ROUND_RESULT=<passed>/<total>. gate_m88k_rounding.sh does the asserting.

How it measures
---------------
Cold debugger on luna-88k. m88k floating point operates on GENERAL registers, which the
debugger seeds by name and prints with `reg` -- no memory round-trip, unlike SH. The
reset PSR has SFD1 clear, so FP executes from step 0. Every row sets the rounding mode
the guest way -- the guest itself executes `fstcr r5,fcr63` -- because that is the path
OpenBSD's fpsetround() uses, so the decode is proven end-to-end, not just the store arm.

`boot` is a FILE (the LUNA-88K bootloader) living in the images directory, not a
keyword; the machine does not construct without it, so the child chdirs there.

Why the sign-ASYMMETRIC rows exist
----------------------------------
m88k's FPCR.RM directed pair is 10=toward-MINUS-infinity, 11=toward-PLUS-infinity --
the OPPOSITE order from MIPS/SH and from float_emul.h's IEEE_RM_* values, so #298's
decode must swap 2 and 3. A decode that FORGETS the swap passes every sign-symmetric
vector (both directed modes just trade places consistently); only rows where the
expected value differs by the SIGN of the operand catch it. Rows fadd-neg-* and
flt-neg-* are that tripwire.

Encodings, from cpu_m88k_instr.c's own decode:
    fadd.sss r4,r2,r3   0x84822803      fsub.sss r4,r2,r3   0x84823003
    fsub.sds r4,r2,r6   0x84823206      fmul.sss r4,r2,r3   0x84820003
    fdiv.sss r4,r2,r3   0x84827003      flt.ss   r4,r2      0x84802002
    fstcr    r5,fcr63   0x80058fe5      fldcr    r6,fcr63   0x80c04fe0
"""
import os
import pty
import re
import select
import sys
import time

BIN = sys.argv[1]
IMAGES = sys.argv[2]
IMG = IMAGES + "/liveimage-luna88k-raw-20250518.img"
CODE = 0x00010000

FSTCR = 0x80058fe5
FLDCR = 0x80c04fe0
FADD = 0x84822803
FSUB_SSS = 0x84823003
FSUB_SDS = 0x84823206
FMUL = 0x84820003
FDIV = 0x84827003
FLT = 0x84802002

RN = 0x0000
RZ = 0x4000
MINF = 0x8000          # m88k RM field 10: toward -Inf
PINF = 0xc000          # m88k RM field 11: toward +Inf

#  name, fcr63 value, seeds, op word (fstcr prelude added automatically), dest, want
ROWS = [
    # pipeline control -- identical in every mode
    ("control 1+1",        RN,   {"r2": 0x3f800000, "r3": 0x3f800000}, FADD, "r4", 0x40000000),

    # fadd.sss 1.0 + 1.5*2^-24: three quarters up one ulp. The RN row is the flipped
    # defect: the pre-#298 build measured 0x3f800000 here.
    ("fadd-pos RN",        RN,   {"r2": 0x3f800000, "r3": 0x33c00000}, FADD, "r4", 0x3f800001),
    ("fadd-pos RZ",        RZ,   {"r2": 0x3f800000, "r3": 0x33c00000}, FADD, "r4", 0x3f800000),
    ("fadd-pos toward+Inf", PINF, {"r2": 0x3f800000, "r3": 0x33c00000}, FADD, "r4", 0x3f800001),
    ("fadd-pos toward-Inf", MINF, {"r2": 0x3f800000, "r3": 0x33c00000}, FADD, "r4", 0x3f800000),

    # the SWAP TRIPWIRE: same magnitudes, negative sign. toward+Inf now truncates and
    # toward-Inf now grows -- a decode without the 2<->3 swap fails all four directed
    # rows above and below simultaneously.
    ("fadd-neg toward+Inf", PINF, {"r2": 0xbf800000, "r3": 0xb3c00000}, FADD, "r4", 0xbf800000),
    ("fadd-neg toward-Inf", MINF, {"r2": 0xbf800000, "r3": 0xb3c00000}, FADD, "r4", 0xbf800001),

    # fsub.sss: 1.0 - (-1.5*2^-24), same landing spot through the subtract arm
    ("fsub.sss RN",        RN,   {"r2": 0x3f800000, "r3": 0xb3c00000}, FSUB_SSS, "r4", 0x3f800001),
    ("fsub.sss RZ",        RZ,   {"r2": 0x3f800000, "r3": 0xb3c00000}, FSUB_SSS, "r4", 0x3f800000),

    # fsub.sds: double (1 + 1.5*2^-24) minus single 0.0 -- the mixed-format arm.
    # s1 is the r2:r3 register PAIR, high word first.
    ("fsub.sds RN",        RN,   {"r2": 0x3ff00000, "r3": 0x18000000, "r6": 0}, FSUB_SDS, "r4", 0x3f800001),
    ("fsub.sds RZ",        RZ,   {"r2": 0x3ff00000, "r3": 0x18000000, "r6": 0}, FSUB_SDS, "r4", 0x3f800000),

    # fmul.sss: 1.5 * (1 + 2^-23) is an exact midpoint; ties-to-even vs truncation
    ("fmul RN tie",        RN,   {"r2": 0x3fc00000, "r3": 0x3f800001}, FMUL, "r4", 0x3fc00002),
    ("fmul RZ",            RZ,   {"r2": 0x3fc00000, "r3": 0x3f800001}, FMUL, "r4", 0x3fc00001),

    # fdiv.sss: 1.0 / 3.0
    ("fdiv RN",            RN,   {"r2": 0x3f800000, "r3": 0x40400000}, FDIV, "r4", 0x3eaaaaab),
    ("fdiv RZ",            RZ,   {"r2": 0x3f800000, "r3": 0x40400000}, FDIV, "r4", 0x3eaaaaaa),

    # flt.ss: int 2^24+1 is exactly between two representable singles.
    ("flt-pos RN tie",     RN,   {"r2": 0x01000001}, FLT, "r4", 0x4b800000),
    ("flt-pos toward+Inf", PINF, {"r2": 0x01000001}, FLT, "r4", 0x4b800001),
    # negative side of the same tie: the other half of the swap tripwire
    ("flt-neg toward-Inf", MINF, {"r2": 0xfeffffff}, FLT, "r4", 0xcb800001),
    ("flt-neg toward+Inf", PINF, {"r2": 0xfeffffff}, FLT, "r4", 0xcb800000),

    # The sub-double-ulp residue band, FIXED by #299 -- this row was the PIN a #298
    # panel seat demanded, expected at the divergent 0x3f800000 with the instruction
    # that it must flip when round-to-odd landed. It flipped: hardware's sticky bit
    # rounds 1.0 + 2^-60 UP under toward-+Inf, and so does the emulator now.
    ("fadd band toward+Inf", PINF, {"r2": 0x3f800000, "r3": 0x21800000}, FADD, "r4",
     0x3f800001),

    # #299's exact-zero sign contract: x + (-x) is -0 ONLY toward minus infinity.
    # The host computes +0 under its nearest mode, so without the helper's special
    # case the toward-minus-Inf row would read 0x00000000.
    ("fadd zero toward-Inf", MINF, {"r2": 0x3f800000, "r3": 0xbf800000}, FADD, "r4",
     0x80000000),
    ("fadd zero RN",         RN,   {"r2": 0x3f800000, "r3": 0xbf800000}, FADD, "r4",
     0x00000000),

    # #299 panel: Inf must pass through the round-to-odd helper untouched, and
    # fsub.sds makes it DIRECTLY reachable -- its first operand is a full DOUBLE
    # (a seat's find), so +Inf minus 1.0f exercises the helper with an infinite
    # input on this rig. The unguarded helper turned it into DBL_MAX.
    ("fsub.sds inf", RZ, {"r2": 0x7ff00000, "r3": 0x00000000, "r6": 0x3f800000},
     FSUB_SDS, "r4", 0x7f800000),
]


#  The fstcr diagnostic contract (#298): pure-RM writes to fcr63 are IMPLEMENTED and must
#  not warn; bits outside RM still must. The warning goes to the EMULATOR's stdout, which
#  only this probe's pty capture ever sees -- a gate grepping its own log for it would be
#  counting a file that cannot contain the string, i.e. a check that cannot fail (a panel
#  seat caught exactly that in the first version of this gate). So the probe counts the
#  warning INSIDE each session's capture: pure-RM sessions accumulate into
#  M88K_FSTCR_WARNS (must be 0) and one deliberate non-RM write (0x1) is the positive
#  control, M88K_WARN_CONTROL (must be exactly 1, proving the counter can count).
WARN_PAT = "UNIMPLEMENTED fcr = 0x3f"
fstcr_warns = 0


def run(fcr, seeds, op, dest):
    global fstcr_warns
    pid, fd = pty.fork()
    if pid == 0:
        os.chdir(IMAGES)
        os.execvp(BIN, [BIN, "-V", "-e", "luna-88k", "-d", "R:" + IMG, "boot"])
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

    def wait(timeout=60):
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

    if not wait(120):
        try:
            os.kill(pid, 9)
            os.waitpid(pid, 0)
        except Exception:
            pass
        return None

    send("r5=0x%08x" % fcr)
    for k, v in seeds.items():
        send("%s=0x%08x" % (k, v))
    send("put w 0x%08x, 0x%08x" % (CODE, FSTCR))
    send("put w 0x%08x, 0x%08x" % (CODE + 4, op))
    send("pc=0x%08x" % CODE)
    send("step 2")
    #  One retry on a missed parse: under host load the register dump can straggle in
    #  after the prompt-detector fires, which reads as None even though the debugger is
    #  alive and the value is fine. Measured: a single such miss in a 20-row run, and
    #  three targeted re-runs of that row all read the correct value. Retrying the READ
    #  is honest -- the value cannot change between two `reg` commands -- where retrying
    #  the whole ROW until green would not be.
    m = None
    for _ in range(2):
        mark = len(buf)
        send("reg")
        m = re.search(r"\b%s\s*=\s*0x([0-9a-f]+)" % dest, buf[mark:])
        if m:
            break
        time.sleep(1.0)
        rd(1.0)
    try:
        os.write(fd, b"quit\n")
        time.sleep(0.4)
        os.kill(pid, 9)
        os.waitpid(pid, 0)
    except Exception:
        pass
    fstcr_warns += buf.count(WARN_PAT)
    return int(m.group(1), 16) if m else None


def run_warn_control():
    """One deliberate NON-RM write (0x1) to fcr63: must produce exactly one warning.
    This is the positive control that proves the warning counter can count -- without
    it, M88K_FSTCR_WARNS=0 would be indistinguishable from a counter that sees
    nothing."""
    pid, fd = pty.fork()
    if pid == 0:
        os.chdir(IMAGES)
        os.execvp(BIN, [BIN, "-V", "-e", "luna-88k", "-d", "R:" + IMG, "boot"])
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

    def wait(timeout=60):
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

    if not wait(120):
        try:
            os.kill(pid, 9)
            os.waitpid(pid, 0)
        except Exception:
            pass
        return None
    send("r5=0x00000001")
    send("put w 0x%08x, 0x%08x" % (CODE, FSTCR))
    send("pc=0x%08x" % CODE)
    send("step 1")
    time.sleep(1.0)
    rd(1.0)
    try:
        os.write(fd, b"quit\n")
        time.sleep(0.4)
        os.kill(pid, 9)
        os.waitpid(pid, 0)
    except Exception:
        pass
    return buf.count(WARN_PAT)


passed = total = 0
for name, fcr, seeds, op, dest, want in ROWS:
    total += 1
    got = run(fcr, seeds, op, dest)
    ok = (got == want)
    passed += ok
    print("%-24s %-10s 0x%08x %s"
          % (name, ("0x%08x" % got) if got is not None else "None", want,
             "ok" if ok else "FAIL"))

# fcr63 retention through the guest's own fstcr/fldcr -- the #296-shape premise
pid_ok = None


def run_retention():
    global fstcr_warns
    pid, fd = pty.fork()
    if pid == 0:
        os.chdir(IMAGES)
        os.execvp(BIN, [BIN, "-V", "-e", "luna-88k", "-d", "R:" + IMG, "boot"])
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

    def wait(timeout=60):
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

    if not wait(120):
        try:
            os.kill(pid, 9)
            os.waitpid(pid, 0)
        except Exception:
            pass
        return None
    send("r5=0x00004000")
    send("put w 0x%08x, 0x%08x" % (CODE, FSTCR))
    send("put w 0x%08x, 0x%08x" % (CODE + 4, FLDCR))
    send("pc=0x%08x" % CODE)
    send("step 2")
    #  Same one-retry-on-missed-parse as run(); see the comment there.
    m = None
    for _ in range(2):
        mark = len(buf)
        send("reg")
        m = re.search(r"\br6\s*=\s*0x([0-9a-f]+)", buf[mark:])
        if m:
            break
        time.sleep(1.0)
        rd(1.0)
    try:
        os.write(fd, b"quit\n")
        time.sleep(0.4)
        os.kill(pid, 9)
        os.waitpid(pid, 0)
    except Exception:
        pass
    fstcr_warns += buf.count(WARN_PAT)
    return int(m.group(1), 16) if m else None


total += 1
got = run_retention()
ok = (got == 0x4000)
passed += ok
print("%-24s %-10s 0x%08x %s"
      % ("fcr63 retention", ("0x%08x" % got) if got is not None else "None",
         0x4000, "ok" if ok else "FAIL"))

wc = run_warn_control()
print("M88K_FSTCR_WARNS=%d" % fstcr_warns)
print("M88K_WARN_CONTROL=%s" % ("None" if wc is None else wc))
print("M88K_ROUND_RESULT=%d/%d" % (passed, total))
