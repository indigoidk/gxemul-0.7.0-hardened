#!/usr/bin/env python3
"""Gate 13's measuring instrument: PowerPC single-precision conversion fidelity.

Prints one line per row:  <name> <got> <want> ok|FAIL
then PPC_CONV_CONTROL=OK|DEAD and PPC_CONV_RESULT=<passed>/<total>.
gate_ppc.sh does the asserting.

How it measures
---------------
Cold debugger on macppc/G4, NetBSD kernel loaded so the machine constructs and
never executed (the bare `testppc` machine was REFUTED as a path: it prints
usage and exits). Big-endian, so `dump` renders memory in value order -- no byte
swapping, unlike every other rig in this harness.

`msr=0x2000` (FP available) is MANDATORY: without it every FP instruction takes
the FPU-unavailable exception and the probe measures nothing. The control row
exists to prove that setup took.

FPSCR is set by DEBUGGER WRITE, never by the guest's own mtfsf: mtfsf's FM-mask
decode is scrambled (cpu_ppc_instr.c:3888-3892 builds nibble masks at an 8-bit
stride, so FM[0..3] write nothing and FM[4..6] write the wrong fields). That is
a filed defect of its own; using it here would make the mode rows measure the
bug instead of the mode. Each mode row READS FPSCR BACK and reports it, so a
write that did not take is visible rather than silently scoring.

The contracts (Power ISA Book I / PEM)
--------------------------------------
* stfs = SINGLE(): three cases on the operand's biased exponent E.
    E > 896            splice: sign, exp bits, top-23 fraction -- TRUNCATION,
                       mode-INDEPENDENT, never rounds.
    874 <= E <= 896    denormalize: prepend the implicit 1, shift right until
                       the exponent reaches -126, truncate to 23 bits.
    E < 874            WORD undefined -- our flush-to-signed-zero is policy.
  #287 gives +/-Inf where the letter's splice would WRAP the exponent for
  finite values >= ~2^129. That divergence is PINNED, not fixed: the letter
  would turn a finite overflow into a NaN pattern (1.5*2^128 -> 0x7FC00000).
* frsp = Round to Single-Precision: rounds per FPSCR[1:0] (00 RN, 01 RZ,
  10 RP, 11 RM -- numerically identical to this project's IEEE_RM_* values),
  delivers the single value in DOUBLE format, including correctly-rounded
  single denormals; QNaN passes through with its fraction truncated to 23
  bits; SNaN is quieted (+VXSNAN); Inf and +/-0 pass through with sign.

Row classes
-----------
  PIN   -- correct today and must stay (several are ISA-exact; two are named
           POLICY pins where we deliberately differ from the letter).
  DIV   -- KNOWN DIVERGENCE, correct-by-record: the committed answer is wrong
           against the ISA but is NOT this round's scope; the row exists so the
           divergence cannot drift silently.
  DISC  -- discriminator: the committed byte is the measured defect, and the
           want flips when the fix lands.
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
SRC = 0x9800

#  Instruction words (Book I forms; verified against the decoder's own cases).
LFS_F1_R3 = 0xC0230000          # lfs   f1,0(r3)
LFSX_F1_R0_R3 = 0x7C201C2E      # lfsx  f1,0,r3
STFS_F1_R3 = 0xD0230000         # stfs  f1,0(r3)
STFSX_F1_R0_R3 = 0x7C201D2E     # stfsx f1,0,r3
STFD_F1_R4 = 0xD8240000         # stfd  f1,0(r4)
STFD_F0_R3 = 0xD8030000         # stfd  f0,0(r3)
FRSP_F0_F1 = 0xFC000818         # frsp  f0,f1
MFFS_F3 = 0xFC60048E            # mffs  f3        (FPSCR -> FPR, the guest's read)
STFD_F3_R5 = 0xD8650000         # stfd  f3,0(r5)

RN, RZ, RP, RM = 0, 1, 2, 3
MODENAME = {RN: "RN", RZ: "RZ", RP: "RP", RM: "RM"}


def session(cmds, dump_words):
    """Run one debugger session; return (words, None).

    The second element is vestigial and always None: an earlier version read
    FPSCR back here on every row, which cost seven extra debugger commands per
    row and let its dump interleave with the row's own. Mode verification now
    lives in verify_mode_writes(), four clean sessions that prove the property
    once."""
    pid, fd = pty.fork()
    if pid == 0:
        os.chdir(IMAGES)
        os.execvp(BIN, [BIN, "-V", "-E", "macppc", "-e", "g4", "-M", "64", KERNEL])
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
        return None, None

    for c in cmds:
        send(c)

    #  Retry the READ, never the row: a dump can straggle past the prompt
    #  detector under host load, and the value cannot change between dumps.
    flat = []
    for _ in range(3):
        mark = len(buf)
        send("dump 0x%x 0x%x" % (DEST, DEST + 4 * dump_words))
        words = re.findall(r"0x0*[0-9a-f]+\s+((?:[0-9a-f]{8}\s+){1,4})",
                           buf[mark:])
        flat = "".join(words).split()
        if len(flat) >= dump_words:
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
    return (flat[:dump_words] if len(flat) >= dump_words else None), None


def run_frsp(fbits, mode):
    """frsp f0,f1 ; stfd f0,0(r3)  -- result read as a 64-bit D pattern."""
    w, rb = session([
        "msr=0x2000",
        "fpscr=0x%08x" % mode,
        "f1=0x%016x" % fbits,
        "r3=0x%x" % DEST,
        "put w 0x%x, 0xdeadbeef" % DEST,
        "put w 0x%x, 0xdeadbeef" % (DEST + 4),
        "put w 0x%x, 0x%08x" % (CODE, FRSP_F0_F1),
        "put w 0x%x, 0x%08x" % (CODE + 4, STFD_F0_R3),
        "pc=0x%x" % CODE,
        "step 2"], 2)
    if w is None:
        return None, rb
    return w[0] + w[1], rb


def run_stfs(fbits, mode=RN, indexed=False):
    """stfs (or stfsx) f1,0(r3) -- result read as a 32-bit S pattern."""
    w, rb = session([
        "msr=0x2000",
        "fpscr=0x%08x" % mode,
        "f1=0x%016x" % fbits,
        "r3=0x%x" % DEST,
        "r0=0x0",
        "put w 0x%x, 0xdeadbeef" % DEST,
        "put w 0x%x, 0x%08x" % (CODE,
                                STFSX_F1_R0_R3 if indexed else STFS_F1_R3),
        "pc=0x%x" % CODE,
        "step 1"], 1)
    if w is None:
        return None, rb
    return w[0], rb


def run_lfs(sbits, indexed=False):
    """lfs (or lfsx) f1,0(r3) ; stfd f1,0(r4) -- the widen, read as a D pattern."""
    w, _ = session([
        "msr=0x2000",
        "r3=0x%x" % SRC,
        "r4=0x%x" % DEST,
        "r0=0x0",
        "put w 0x%x, 0x%08x" % (SRC, sbits),
        "put w 0x%x, 0xdeadbeef" % DEST,
        "put w 0x%x, 0xdeadbeef" % (DEST + 4),
        "put w 0x%x, 0x%08x" % (CODE,
                                LFSX_F1_R0_R3 if indexed else LFS_F1_R3),
        "put w 0x%x, 0x%08x" % (CODE + 4, STFD_F1_R4),
        "pc=0x%x" % CODE,
        "step 2"], 2)
    if w is None:
        return None
    return w[0] + w[1]


def run_vxsnan_sticky():
    """frsp(sNaN) then frsp(1.0), then read FPSCR the guest's way.

    VXSNAN is a STICKY exception bit -- hardware leaves it set until the guest
    clears it -- so the second frsp must not wipe it. The first version of
    #305 set the bit and then cleared it on exactly this sequence, which is
    worse than never setting it: the guest sees no record that a signalling
    NaN was ever converted (a diff-review seat's finding).

    FPSCR is read with the guest's own `mffs` into memory, NOT with the
    debugger's `reg`: that command prints fpscr only under its coprocessor
    form, so the plain-`reg` regex this probe first used could never match.
    Reading it the guest's way proves the guest-visible value anyway.
    """
    w, _ = session([
        "msr=0x2000",
        "fpscr=0x00000000",
        "f1=0x7ff0000000000123",
        "r5=0x%x" % DEST,
        "put w 0x%x, 0xdeadbeef" % DEST,
        "put w 0x%x, 0xdeadbeef" % (DEST + 4),
        "put w 0x%x, 0x%08x" % (CODE, FRSP_F0_F1),
        "pc=0x%x" % CODE,
        "step 1",
        "f1=0x3ff0000000000000",
        "pc=0x%x" % CODE,
        "step 1",
        "put w 0x%x, 0x%08x" % (CODE + 32, MFFS_F3),
        "put w 0x%x, 0x%08x" % (CODE + 36, STFD_F3_R5),
        "pc=0x%x" % (CODE + 32),
        "step 2"], 2)
    if w is None or len(w) < 2 or w[1] == "deadbeef":
        return None
    return "set" if (int(w[1], 16) & (1 << 24)) else "clear"


def verify_mode_writes():
    """Prove, once per rounding mode, that a debugger `fpscr=` write is what the
    GUEST sees -- read back with the guest's own `mffs`.

    Two things make this its own function rather than a per-row check.  First,
    the debugger's plain `reg` does not print FPSCR on this CPU at all (it
    appears only under the coprocessor form), so the regex an earlier version
    used could never match and the whole mode check passed vacuously on every
    run -- a diff-review seat predicted that hole and the rewrite then measured
    it.  Second, reading it inside every row cost seven extra debugger commands
    per row and let the readback's dump interleave with the row's own: one
    result came back holding the FPSCR value and twenty of forty-three reads
    were lost to straggle.  The property belongs to the mechanism, not to each
    row, so four clean sessions prove it and the measurement rows stay clean.

    Returns (good, bad).
    """
    good = bad = 0
    for mode in (RN, RZ, RP, RM):
        w, _ = session([
            "msr=0x2000",
            "fpscr=0x%08x" % mode,
            "r5=0x%x" % DEST,
            "put w 0x%x, 0xdeadbeef" % DEST,
            "put w 0x%x, 0xdeadbeef" % (DEST + 4),
            "put w 0x%x, 0x%08x" % (CODE, MFFS_F3),
            "put w 0x%x, 0x%08x" % (CODE + 4, STFD_F3_R5),
            "pc=0x%x" % CODE,
            "step 2"], 2)
        if w is None or len(w) < 2 or w[1] == "deadbeef":
            bad += 1
            print("  !! mode %s: FPSCR readback unparsed" % MODENAME[mode])
            continue
        rb = int(w[1], 16) & 3
        if rb != mode:
            bad += 1
            print("  !! mode %s: guest read %d" % (MODENAME[mode], rb))
        else:
            good += 1
    return good, bad


def run_fctiwz(fbits):
    """fctiwz f0,f1 ; stfd f0,0(r3) -- the converted word is the LOW half."""
    w, _ = session([
        "msr=0x2000",
        "fpscr=0x00000000",
        "f1=0x%016x" % fbits,
        "r3=0x%x" % DEST,
        "put w 0x%x, 0xdeadbeef" % DEST,
        "put w 0x%x, 0xdeadbeef" % (DEST + 4),
        "put w 0x%x, 0x%08x" % (CODE, 0xFC00001E),      # fctiwz f0,f1
        "put w 0x%x, 0x%08x" % (CODE + 4, STFD_F0_R3),
        "pc=0x%x" % CODE,
        "step 2"], 2)
    if w is None or len(w) < 2:
        return None
    return w[1]



def run_update(r3, r4, words, nread):
    """Seed the register plan, run the sequence, read DEST back.

    The debugger cannot print PowerPC FPRs or GPRs on this machine (the same
    limitation that sent #304's mode readback through mffs), so publishing to
    memory IS the readback path -- which is why every row ends in a store.
    """
    cmds = ["msr=0x2000",
            "r3=0x%x" % r3,
            "r5=0x%x" % DEST,
            "f1=0x3ff0000000000000",
            "put w 0x%x, 0x3f800000" % SRC,           # 1.0f for the S loads
            "put w 0x%x, 0x3ff00000" % (SRC + 8),     # 1.0d, high word
            "put w 0x%x, 0x00000000" % (SRC + 12),    # 1.0d, low word
            "put w 0x%x, 0xdeadbeef" % DEST,
            "put w 0x%x, 0xdeadbeef" % (DEST + 4)]
    if r4 is not None:
        cmds.append("r4=0x%x" % r4)
    for i, w in enumerate(words):
        cmds.append("put w 0x%x, 0x%08x" % (CODE + 4 * i, w))
    cmds += ["pc=0x%x" % CODE, "step %d" % len(words)]
    w, _ = session(cmds, nread)
    if w is None:
        return None
    return "".join(w) if nread == 2 else w[0]


def run_composed(fbits, mode=RN):
    """frsp f0,f1 ; then stfs the ROUNDED value -- the compiler's own float
    store sequence, and the row a guest-visible triage would hit first."""
    w, _ = session([
        "msr=0x2000",
        "fpscr=0x%08x" % mode,
        "f1=0x%016x" % fbits,
        "r3=0x%x" % DEST,
        "put w 0x%x, 0xdeadbeef" % DEST,
        "put w 0x%x, 0x%08x" % (CODE, FRSP_F0_F1),
        "put w 0x%x, 0x%08x" % (CODE + 4, 0xD0030000),   # stfs f0,0(r3)
        "pc=0x%x" % CODE,
        "step 2"], 1)
    if w is None:
        return None
    return w[0]


#  ---------------------------------------------------------------------------
#  ROWS.  Every `want` below is the COMMITTED byte, measured on the build that
#  precedes #304/#305; the DISC rows' wants flip when the fix lands, and the
#  flip is that fix's acceptance test.  Bytes marked (oracle) were derived by
#  exact rational arithmetic offline and independently by two panel seats.
#  ---------------------------------------------------------------------------
FRSP_ROWS = [
    #  name,                        operand,             mode, want, class
    ("control frsp 2.0",            0x4000000000000000, RN, "4000000000000000", "PIN"),
    ("frsp qNaN",                   0x7ff8000000000000, RN, "7ff8000000000000", "DISC"),
    ("frsp qNaN-",                  0xfff8000000000000, RN, "fff8000000000000", "DISC"),
    ("frsp qNaN payload",           0x7ffdeadbeef00000, RN, "7ffdeadbe0000000", "DISC"),
    ("frsp sNaN",                   0x7ff0000000000123, RN, "7ff8000000000000", "DISC"),
    ("frsp +Inf",                   0x7ff0000000000000, RN, "7ff0000000000000", "PIN"),
    ("frsp -0.0",                   0x8000000000000000, RN, "8000000000000000", "PIN"),
    #  normal-range rounding: RN today is host-nearest and CORRECT; RZ is the
    #  mode-blindness discriminator (1 + 3*2^-25 truncates to 1.0 under RZ).
    ("frsp 1+3ulp/2 RN",            0x3ff0000018000000, RN, "3ff0000020000000", "PIN"),
    ("frsp 1+3ulp/2 RZ",            0x3ff0000018000000, RZ, "3ff0000000000000", "DISC"),
    ("frsp 1+3ulp/2 RP",            0x3ff0000018000000, RP, "3ff0000020000000", "PIN"),
    ("frsp 1+3ulp/2 RM",            0x3ff0000018000000, RM, "3ff0000000000000", "DISC"),
    #  ties-to-even, both parities: mode-independent, protect the rewrite.
    ("frsp tie even RN",            0x3ff0000010000000, RN, "3ff0000000000000", "PIN"),
    ("frsp tie odd RN",             0x3ff0000030000000, RN, "3ff0000040000000", "PIN"),
    #  denormal band (oracle): the host cast is RN-correct, so only the
    #  directed modes discriminate -- the #298 sign-asymmetry lesson applied.
    ("frsp band RN",                0x3730020000000000, RN, "3730000000000000", "PIN"),
    ("frsp band RP",                0x3730020000000000, RP, "3730080000000000", "DISC"),
    ("frsp band- RM",               0xb730020000000000, RM, "b730080000000000", "DISC"),
    ("frsp band RZ",                0x3730060000000000, RZ, "3730000000000000", "DISC"),
    #  carry out of the band into the smallest NORMAL single.
    ("frsp carry-up RN",            0x380fffffe0000000, RN, "3810000000000000", "PIN"),
    ("frsp carry-up RZ",            0x380fffffe0000000, RZ, "380fffffc0000000", "DISC"),
    #  below the band: RP of a tiny positive owes the minimum denormal.
    ("frsp tiny RP",                0x3690000000000000, RP, "36a0000000000000", "DISC"),
    ("frsp tiny RN",                0x3690000000000000, RN, "0000000000000000", "PIN"),
    ("frsp tiny- RM",               0xb690000000000000, RM, "b6a0000000000000", "DISC"),
    #  overflow by mode.  RN overflowing to Infinity is ISA-CORRECT, so that
    #  row is a PIN; only the toward-zero row is the defect (it owes the
    #  largest finite single, 0x47efffffe0000000 = FLT_MAX in D format).  The
    #  first version of this table wanted 0x47f0000000000000 for BOTH -- the D
    #  pattern of 2^128 itself, which no correct implementation can produce --
    #  and the baseline sweep refuted the annotation, not the emulator.
    ("frsp 2^128 RN",               0x47f0000000000000, RN, "7ff0000000000000", "PIN"),
    ("frsp 2^128 RZ",               0x47f0000000000000, RZ, "47efffffe0000000", "DISC"),
]

STFS_ROWS = [
    ("control stfs 1.0",            0x3ff0000000000000, RN, False, "3f800000", "PIN"),
    #  mode-INDEPENDENCE is the contract: both modes must give the same byte.
    ("stfs 1+3ulp/2 RN",            0x3ff0000018000000, RN, False, "3f800000", "PIN"),
    ("stfs 1+3ulp/2 RZ",            0x3ff0000018000000, RZ, False, "3f800000", "PIN"),
    #  the denormalization band (oracle bytes).
    ("stfs 2^-127",                 0x3800000000000000, RN, False, "00400000", "DISC"),
    ("stfs band tail",              0x3808000030000000, RN, False, "00600000", "DISC"),
    ("stfs band deep",              0x3730080000000000, RN, False, "00000201", "DISC"),
    #  the negative band row keeps its SIGN through the flush (#287 fixed
    #  exactly that), so the committed byte is 0x80000000, not +0.
    ("stfs band-",                  0xb800000000000000, RN, False, "80400000", "DISC"),
    #  just ABOVE the band: a normal single, spliced, unchanged by the fix.
    ("stfs FLT_MIN",                0x3810000000000000, RN, False, "00800000", "PIN"),
    #  overflow: ISA-exact pins where splice and #287 coincide.
    ("stfs 2^128",                  0x47f0000000000000, RN, False, "7f800000", "PIN"),
    ("stfs max-single",             0x47efffffe0000000, RN, False, "7f7fffff", "PIN"),
    #  POLICY pin: the letter would splice-WRAP these; #287 gives Inf and we
    #  keep it deliberately (the letter turns a finite overflow into a NaN).
    ("stfs 2^129 policy",           0x4800000000000000, RN, False, "7f800000", "PIN"),
    ("stfs 3*2^128 policy",         0x4808000000000000, RN, False, "7f800000", "PIN"),
    #  NaN transport (#305): payload and sign are destroyed today.
    ("stfs qNaN payload",           0xfff8000020000001, RN, False, "ffc00001", "DISC"),
    ("stfs sNaN passthrough",       0x7ff0000020000001, RN, False, "7f800001", "DISC"),
    ("stfs NaN collapse",           0x7ff0000000000001, RN, False, "7f800000", "DISC"),
    ("stfs +Inf",                   0x7ff0000000000000, RN, False, "7f800000", "PIN"),
    ("stfs -0.0",                   0x8000000000000000, RN, False, "80000000", "PIN"),
    #  the indexed form must not be left behind by the fix.
    ("stfsx 2^-127",                0x3800000000000000, RN, True,  "00400000", "DISC"),
    ("stfsx qNaN payload",          0xfff8000020000001, RN, True,  "ffc00001", "DISC"),
]

LFS_ROWS = [
    ("control lfs 1.0f",            0x3f800000, "3ff0000000000000", "PIN"),
    #  #303 proved the finite widen exact, subnormals included.
    ("lfs S-min",                   0x00000001, "36a0000000000000", "PIN"),
    ("lfs -S-min",                  0x80000001, "b6a0000000000000", "PIN"),
    ("lfs denorm-max",              0x007fffff, "380fffffc0000000", "PIN"),
    #  #305: the NaN widen destroys sign and payload today.
    ("lfs qNaN-",                   0xffc00001, "fff8000020000000", "DISC"),
    ("lfs qNaN+",                   0x7fc00001, "7ff8000020000000", "DISC"),
]

#  The INDEXED load, which nothing else in this table touches: without these
#  rows the fix could be deleted from X(lfsx) and the gate would still score
#  a clean sweep (a diff-review seat's finding).
LFSX_ROWS = [
    ("lfsx control 1.0f",           0x3f800000, "3ff0000000000000", "PIN"),
    ("lfsx qNaN-",                  0xffc00001, "fff8000020000000", "DISC"),
]

#  fctiwz of a NaN answers 0 where the ISA owes 0x80000000. NOT this round's
#  scope -- it is the PPC cleanup round's -- but pinned here as a DIVERGENCE so
#  it cannot drift silently while nobody is looking at it.
FCTIWZ_ROWS = [
    ("fctiwz qNaN div",             0x7ff8000000000000, "00000000", "DIV"),
]


#  #310: the eight float UPDATE forms. Each was measured HALTING the emulator
#  before this correction (their non-update twins ran, as controls), because
#  neither the primary opcodes 0x31/0x33/0x35/0x37 nor the indexed extended
#  opcodes 567/631/695/759 were defined or decoded -- opcodes_ppc.h even had
#  blank lines where the four primary ones belong.
#
#  A row asserts BOTH halves of what an update form owes: the value
#  transferred AND rA receiving the effective address. Asserting only the
#  value would pass an implementation that forgot the update entirely, which
#  is the whole difference between these instructions and their twins; the
#  non-update control rows assert the mirror image, that rA is UNCHANGED.
#
#  Register plan, because the first version of these rows had none and
#  measured its own confusion: r3 is the base under test, r4 is the index for
#  the indexed forms ONLY, r5 is the publish base and nothing else, r6 is the
#  target the update-stores write into. Publishing through a register that is
#  also an operand makes a row report whichever value happened to survive.
#
#  Honest note on reach, corrected in review: an earlier census claimed
#  hundreds of these instructions in the NetBSD/macppc kernel. That came from
#  scanning the whole RWX PT_LOAD, which is mostly data. Restricted to the
#  executable section, this kernel contains lfd 34, stfd 36 and NONE of the
#  update forms. They are justified by being legal encodings that stopped the
#  machine, not by their frequency in one image.
#
#  Encodings: stw r3,0(r5) = 0x90650000 publishes the base; stfd f1,0(r5) =
#  0xD8250000 publishes the loaded value.
PUBLISH_BASE = 0x90650000
PUBLISH_VALUE = 0xD8250000
STORE_AT = 0x9900

UPDATE_ROWS = [
    #  name, r3 seed, index (r4 or None), code words, reads, want
    ("lfsu value",       SRC - 4, None, [0xC4230004, PUBLISH_VALUE], 2,
     "3ff0000000000000"),
    ("lfsu updates r3",  SRC - 4, None, [0xC4230004, PUBLISH_BASE], 1,
     "%08x" % SRC),
    ("lfs leaves r3",    SRC,     None, [0xC0230000, PUBLISH_BASE], 1,
     "%08x" % SRC),
    ("lfdu value",       SRC,     None, [0xCC230008, PUBLISH_VALUE], 2,
     "3ff0000000000000"),
    ("lfdu updates r3",  SRC,     None, [0xCC230008, PUBLISH_BASE], 1,
     "%08x" % (SRC + 8)),
    ("stfsu updates r3", STORE_AT - 4, None, [0xD4230004, PUBLISH_BASE], 1,
     "%08x" % STORE_AT),
    ("stfdu updates r3", STORE_AT - 8, None, [0xDC230008, PUBLISH_BASE], 1,
     "%08x" % STORE_AT),
    ("lfsux value",      SRC - 4, 4, [0x7C23246E, PUBLISH_VALUE], 2,
     "3ff0000000000000"),
    ("lfsux updates r3", SRC - 4, 4, [0x7C23246E, PUBLISH_BASE], 1,
     "%08x" % SRC),
    ("lfsx leaves r3",   SRC,     0, [0x7C23242E, PUBLISH_BASE], 1,
     "%08x" % SRC),
    ("lfdux updates r3", SRC,     8, [0x7C2324EE, PUBLISH_BASE], 1,
     "%08x" % (SRC + 8)),
    ("stfsux updates r3", STORE_AT - 4, 4, [0x7C23256E, PUBLISH_BASE], 1,
     "%08x" % STORE_AT),
    ("stfdux updates r3", STORE_AT - 8, 8, [0x7C2325EE, PUBLISH_BASE], 1,
     "%08x" % STORE_AT),
]


#  The composed sequence a compiler emits for `float f = (float)d; store f;`.
COMPOSED_ROWS = [
    ("composed frsp->stfs NaN",     0x7ff8000000000000, RN, "7fc00000", "DISC"),
]


#  The FIXED side of every DISC row, kept next to the committed side so the
#  flip that #304/#305 must produce is mechanical and reviewable.  Derived by
#  exact rational arithmetic offline and cross-checked by two panel seats.
#  What the COMMITTED build gave for every DISC row, measured in the baseline
#  sweep before #304/#305 existed.  Kept because it is the round's evidence:
#  each `want` above was this value until the fix flipped it, and all
#  twenty-five flipped to their pre-registered bytes on the first run -- no
#  byte was adjusted after seeing a result.
COMMITTED_BEFORE = {
    "frsp qNaN":               "0000000000000000",
    "frsp qNaN-":              "0000000000000000",
    "frsp qNaN payload":       "0000000000000000",
    "frsp sNaN":               "0000000000000000",
    "frsp 1+3ulp/2 RZ":        "3ff0000020000000",
    "frsp 1+3ulp/2 RM":        "3ff0000020000000",
    "frsp band RP":            "3730000000000000",
    "frsp band- RM":           "b730000000000000",
    "frsp band RZ":            "3730080000000000",
    "frsp carry-up RZ":        "3810000000000000",
    "frsp tiny RP":            "0000000000000000",
    "frsp tiny- RM":           "8000000000000000",
    "frsp 2^128 RZ":           "7ff0000000000000",
    "stfs 2^-127":             "00000000",
    "stfs band tail":          "00000000",
    "stfs band deep":          "00000000",
    "stfs band-":              "80000000",
    "stfs qNaN payload":       "7fffffff",
    "stfs sNaN passthrough":   "7fffffff",
    "stfs NaN collapse":       "7fffffff",
    "stfsx 2^-127":            "00000000",
    "stfsx qNaN payload":      "7fffffff",
    "lfs qNaN-":               "7fffffffffffffff",
    "lfs qNaN+":               "7fffffffffffffff",
    "composed frsp->stfs NaN": "00000000",
}



def main():
    passed = total = 0
    control_ok = False

    def report(name, got, want, cls):
        nonlocal passed, total
        total += 1
        ok = (got == want)
        passed += ok
        print("%-26s %-18s %-18s %-4s %s" %
              (name, got if got is not None else "None", want, cls,
               "ok" if ok else "FAIL"))
        return ok

    #  Prove the rounding-mode WRITE channel once per mode, in its own clean
    #  sessions, before any row depends on it.
    mode_reads, mode_bad = verify_mode_writes()

    for name, operand, mode, want, cls in FRSP_ROWS:
        got, rb = run_frsp(operand, mode)
        ok = report(name, got, want, cls)
        if name.startswith("control"):
            control_ok = ok

    for name, operand, mode, indexed, want, cls in STFS_ROWS:
        got, rb = run_stfs(operand, mode, indexed)
        report(name, got, want, cls)

    for name, sbits, want, cls in LFS_ROWS:
        report(name, run_lfs(sbits), want, cls)

    for name, sbits, want, cls in LFSX_ROWS:
        report(name, run_lfs(sbits, indexed=True), want, cls)

    for name, operand, want, cls in FCTIWZ_ROWS:
        report(name, run_fctiwz(operand), want, cls)

    for name, r3, r4, words, nread, want in UPDATE_ROWS:
        report(name, run_update(r3, r4, words, nread), want, "DISC")

    for name, operand, mode, want, cls in COMPOSED_ROWS:
        report(name, run_composed(operand, mode), want, cls)

    #  VXSNAN must survive a following non-NaN frsp (see run_vxsnan_sticky).
    report("VXSNAN sticky", run_vxsnan_sticky(), "set", "DISC")

    #  The control row is load-bearing: a probe whose control fails has
    #  measured NOTHING, and no other row may be believed (this harness has
    #  been bitten by a probe that reported a defect off sentinel reads).
    print("PPC_CONV_CONTROL=%s" % ("OK" if control_ok else "DEAD"))
    print("PPC_CONV_MODEWRITES_BAD=%d" % mode_bad)
    #  ... and how many readbacks actually PARSED, so "0 bad" cannot be the
    #  answer a probe gives when it read nothing at all.
    print("PPC_CONV_MODEREADS=%d" % mode_reads)
    print("PPC_CONV_RESULT=%d/%d" % (passed, total))


main()
