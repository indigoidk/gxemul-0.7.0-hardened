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

    # #302: trnc.ss/trnc.sd -- the float->int32 truncations, previously raw C casts
    # (host-UB on the specials; x86 answered 0x80000000 for everything). The m88k
    # contract is OpenBSD's kernel completion (the MC88100 always traps and writes
    # nothing): NaN of EITHER sign -> 0x7fffffff -- SoftFloat forces the sign positive,
    # the signature that distinguishes this table from SH's and MIPS's -- +Inf and
    # positive overflow -> 0x7fffffff, negatives -> 0x80000000, exact -2^31 in range.
    # The positive rows discriminate against the pre-#302 build; the negative rows
    # coincide with x86-UB and are HOST-INDEPENDENCE pins (an aarch64 host's cast
    # saturates differently and turns NaN into 0). trnc ignores the rounding mode, so
    # the fstcr prelude's RN is inert here.
    #   trnc.ss r4,r2 = 0x84805802 ; trnc.sd r4,r2 = 0x84805882 (r2:r3 pair, hi first)
    ("trncSS +Inf",   RN, {"r2": 0x7f800000}, 0x84805802, "r4", 0x7fffffff),
    ("trncSS qNaN-",  RN, {"r2": 0xffc00000}, 0x84805802, "r4", 0x7fffffff),
    ("trncSS -2^40",  RN, {"r2": 0xd3800000}, 0x84805802, "r4", 0x80000000),
    ("trncSD 2^31",   RN, {"r2": 0x41e00000, "r3": 0x00000000}, 0x84805882, "r4",
     0x7fffffff),
    ("trncSD qNaN+",  RN, {"r2": 0x7ff80000, "r3": 0x00000000}, 0x84805882, "r4",
     0x7fffffff),
    ("trncSD -Inf",   RN, {"r2": 0xfff00000, "r3": 0x00000000}, 0x84805882, "r4",
     0x80000000),
    #  negative NaN through the DOUBLE arm: a panel seat noted the signature row
    #  existed only for .ss, so a regression special-casing the sd arm's NaN handling
    #  would pass green. Same want as .ss -- the m88k table forces NaN positive.
    ("trncSD qNaN-",  RN, {"r2": 0xfff80000, "r3": 0x00000000}, 0x84805882, "r4",
     0x7fffffff),

    # #302 second half: int (fcr63-modal) and nint (round-to-nearest). Before this the
    # decoder sent both to goto bad and the emulator HALTED on a legal instruction
    # ("All machines stopped", reproduced). int.ss r4,r2 = 0x84804802; int.sd =
    # 0x84804882; nint.ss = 0x84805002. 5.2 discriminates the modes (toward-+Inf 6,
    # toward-zero 5, and trunc-wired-by-mistake would also read 5 under +Inf); -5.2
    # under toward-MINUS-Inf is the sign-asymmetric row (#298 lesson: a missing 2<->3
    # swap passes every symmetric row); nint's two tie parities catch both a
    # trunc-wired and a half-up-wired mistake; the NaN row proves the shared table
    # through the new arms.
    ("intSS 5.2 +Inf", PINF, {"r2": 0x40a66666}, 0x84804802, "r4", 0x00000006),
    ("intSS 5.2 RZ",   RZ,   {"r2": 0x40a66666}, 0x84804802, "r4", 0x00000005),
    ("intSS -5.2 -Inf", MINF, {"r2": 0xc0a66666}, 0x84804802, "r4", 0xfffffffa),
    ("intSD 5.2 +Inf", PINF, {"r2": 0x4014cccc, "r3": 0xcccccccd}, 0x84804882, "r4",
     0x00000006),
    ("nintSS 2.5 tie", RN,   {"r2": 0x40200000}, 0x84805002, "r4", 0x00000002),
    ("nintSS 3.5 tie", RN,   {"r2": 0x40600000}, 0x84805002, "r4", 0x00000004),
    ("nintSS qNaN-",   RN,   {"r2": 0xffc00000}, 0x84805002, "r4", 0x7fffffff),
    #  nint.sd was the one handler in the triad no row executed (a panel seat's find:
    #  correct by inspection and symmetry, but never once touched by an instrument).
    #  2.5 in double, ties-to-even -> 2, through the .sd pair-assembly path.
    ("nintSD 2.5 tie", RN,   {"r2": 0x40040000, "r3": 0x00000000}, 0x84805082, "r4",
     0x00000002),

    # #300: D-format arithmetic honours the mode via the fma-residual helpers. The
    # result register pair is r6:r7 (big-endian, high word first); the low word under
    # toward-zero is the round-61 witness ...99, where host-nearest gives ...9a.
    # fdiv.ddd r6,r2,r8 = major 0x21, d=6, s1=2, op11 0x0e, size ddd (0x15), s2=8.
    # The divisor pair lives in r8:r9, NOT r4:r5 -- this probe stages the rounding
    # mode in r5 before the guest's fstcr consumes it, and the first version of this
    # row seeded r5 as the divisor's low word, silently reverting the mode to nearest
    # and failing with the RN answer. A probe register plan is part of the vector.
    ("fdiv.ddd 1/10 RZ", RZ, {"r2": 0x3ff00000, "r3": 0x00000000,
                               "r8": 0x40240000, "r9": 0x00000000},
     0x84c272a8, "r7", 0x99999999),

    # #303: subnormal OPERANDS decode to their true IEEE value. Before, every
    # subnormal decoded with the implicit 1 added and the exponent one too low --
    # S 0x00000001 read as (1+2^-23)*2^-127, 4.19e6x its real 2^-149 -- and every
    # m88k FP operand consumed the garble (the MC88100 contract is kernel
    # completion, which computes true IEEE). All committed-build bytes below were
    # MEASURED live before the fix (0x32000001/0xb2000001, 38000000:20000000,
    # 3e800000:00000000, mask 0x9a) and every fixed byte after it.
    #   Same-format compares can NEVER discriminate this defect (the garble maps
    # subnormals monotonically into (0, FLT_MIN), order preserved) -- fcmp.ssd
    # with a DOUBLE comparand INSIDE the (true, garbled) gap is the only
    # discriminating compare shape, hence the 2^-135 row. The fmul rows have
    # NORMAL results, so the #287/#292 store flush never touches them.
    #   fmul.dss r6,r2,r3 = 0x84c20023 (s2 NAMED 1.0f: the pinned bytes are the
    # pure widen); fmul.ddd r6,r2,r8 = 0x84c202a8; fcmp.ssd r4,r2,r6 = 0x84823886.
    ("subn fmul +",    RN, {"r2": 0x00000001, "r3": 0x71800000}, FMUL, "r4",
     0x27000000),
    ("subn fmul -",    RN, {"r2": 0x80000001, "r3": 0x71800000}, FMUL, "r4",
     0xa7000000),
    ("subn fmul.dss",  RN, {"r2": 0x00000001, "r3": 0x3f800000}, 0x84c20023, "r6",
     0x36a00000),
    ("subn fmul.ddd",  RN, {"r2": 0x00000000, "r3": 0x00000001,
                            "r8": 0x7e700000, "r9": 0x00000000}, 0x84c202a8, "r6",
     0x3b500000),
    ("subn fcmp.ssd",  RN, {"r2": 0x00000001,
                            "r6": 0x37800000, "r7": 0x00000000}, 0x84823886, "r4",
     0x0000006a),
    # KNOWN-CHANGE pin, NEGATIVE operand: the garbled product of -S-min * 2.0
    # landed S-NORMAL and stored nonzero (the positive twin measured 0x00800001
    # pre-#303; the negative one is the same path with the sign applied last);
    # the TRUE product -2^-148 is subnormal, so the deliberate #287/#292 store
    # flush now answers MINUS zero -- the sign survives because #287 fixed
    # exactly that. The row is negative BECAUSE of that: a #287 revert (sign
    # lost, +0) trips it, where a positive row reads +0 under both stores and
    # cannot see the revert at all (a diff-review seat's finding). A #303
    # revert trips it too. The guest still observes x != 0 but x*2 == 0 -- the
    # interim half-state the queued store-side round inherits.
    ("subn flip x2.0", RN, {"r2": 0x80000001, "r3": 0x40000000}, FMUL, "r4",
     0x80000000),
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
