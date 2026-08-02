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

FPSCR is set by DEBUGGER WRITE, never by the guest's own mtfsf, and each mode row
READS FPSCR BACK so a write that did not take is visible rather than silently
scoring. That precaution was not hypothetical: mtfsf's FM-mask decode WAS
scrambled -- it built nibble masks at an 8-bit stride, so FM[0..3] wrote nothing
and FM[4..6] wrote the wrong fields -- and had the mode rows driven the mode
through it, the defect would have been baked into every measurement instead of
exposed by one. #324 fixed the stride; the debugger write stays, because keeping
the mode rows independent of a second instruction's correctness is what made the
finding reachable. mtfsf now has six rows of its own.

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
           want flips when the fix lands. #327's twelve moved bytes were all
           PRE-REGISTERED -- derived from Book I and written down before the
           code existed -- so the flip is an acceptance test and not a
           transcript of whatever the new build printed.
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

#  #326. Built from fields rather than typed as hex, and each is spelled out
#  so a wrong register cannot hide: fcmpu is X-form with BF in the top three
#  bits of the RT slot (BF=0 -> cr0), fadd/fmul are A-form.
FCMPU_CR0_F1_F2 = (63 << 26) | (0 << 21) | (1 << 16) | (2 << 11) | (0 << 1)
MFCR_R3 = (31 << 26) | (3 << 21) | (19 << 1)            # mfcr r3
STW_R3_R4 = (36 << 26) | (3 << 21) | (4 << 16)          # stw  r3,0(r4)
FADD_F0_F1_F2 = (63 << 26) | (0 << 21) | (1 << 16) | (2 << 11) | (21 << 1)
FMUL_F0_F1_F1 = (63 << 26) | (0 << 21) | (1 << 16) | (1 << 6) | (25 << 1)

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


def _fps(op, rt=0, ra=0, rb=0, xo=0):
    """#327: assemble an X-form FPSCR-control word from its fields."""
    return (((op & 63) << 26) | ((rt & 31) << 21) | ((ra & 31) << 16)
            | ((rb & 31) << 11) | ((xo & 1023) << 1))


def MTFSB0(bt):
    return _fps(63, rt=bt, xo=70)


def MTFSB1(bt):
    return _fps(63, rt=bt, xo=38)


def MCRFS(bf, bfa):
    return _fps(63, rt=bf << 2, ra=bfa << 2, xo=64)


def run_fpscr_seq(preload, seq, seed_f1=None):
    """#327: run a sequence of instructions and read FPSCR back via mffs.

    The instrument for the two SUMMARY bits. Book I derives VX from the nine
    Invalid Operation causes and FEX from the exceptions masked by their
    enables; this fork stored both, so they went stale in both directions and
    a guest could see VX set with no cause -- a state hardware cannot produce.
    Each row drives a real instruction sequence and reads the guest-visible
    register, never the debugger's view.
    """
    cmds = ["msr=0x2000", "fpscr=0x%08x" % preload]
    if seed_f1 is not None:
        cmds.append("f1=0x%016x" % seed_f1)
    cmds += ["r5=0x%x" % DEST,
             "put w 0x%x, 0xdeadbeef" % DEST,
             "put w 0x%x, 0xdeadbeef" % (DEST + 4)]
    for i, iw in enumerate(seq):
        cmds.append("put w 0x%x, 0x%08x" % (CODE + 4 * i, iw))
    n = len(seq)
    cmds += ["pc=0x%x" % CODE, "step %d" % n,
             "put w 0x%x, 0x%08x" % (CODE + 4 * n, MFFS_F3),
             "put w 0x%x, 0x%08x" % (CODE + 4 * n + 4, STFD_F3_R5),
             "pc=0x%x" % (CODE + 4 * n), "step 2"]
    w, _ = session(cmds, 2)
    if w is None or len(w) < 2 or w[1] == "deadbeef":
        return None
    return w[1]


#  #327. Every want here was PRE-REGISTERED -- derived from Book I and written
#  down before the code was built -- so the flip is the fix's acceptance test
#  rather than a transcription of whatever the new build happened to print.
SNAN_D = 0x7ff0000000000123
SUMMARY_ROWS = [
    #  LOWER: clear the only invalid cause; VX must fall. Committed build gave
    #  a0001000 -- VX still set with nothing causing it.
    ("VX falls on last clear", 0x00000000,
     [FRSP_F0_F1, MTFSB0(7)], SNAN_D, "80001000", "DISC"),

    #  RAISE: set a cause; VX must rise. Committed gave 80200000, VX never rose.
    ("VX rises on cause", 0x00000000,
     [MTFSB1(10)], None, "a0200000", "DISC"),

    #  FEX from an enabled pending exception. Committed gave 81000080.
    ("FEX rises on enable", 0x00000000,
     [MTFSB1(7), MTFSB1(24)], None, "e1000080", "DISC"),

    #  FEX must FALL when mcrfs clears the exception that enabled it. The
    #  preload is not stale to begin with -- OX and OE legitimately derive
    #  FEX=1 -- it goes stale only once mcrfs clears OX, which is exactly what
    #  a build that merely stores FEX would fail to notice.
    ("FEX falls with its cause", 0x50000040,
     [MCRFS(0, 0)], None, "00000040", "DISC"),

    #  ORDER INDEPENDENCE: enable-then-cause must equal cause-then-enable.
    #  NOT a pre-existing disagreement -- the old build answered a1001080
    #  BOTH ways, agreeing while missing FEX entirely, and an earlier note
    #  here wrongly claimed otherwise without measuring it. The rows earn
    #  their place now that FEX actually moves: a recompute driven from the
    #  wrong site, or only from frsp, would make these two disagree.
    ("FEX order: enable first", 0x00000000,
     [MTFSB1(24), FRSP_F0_F1], SNAN_D, "e1001080", "DISC"),
    ("FEX order: cause first", 0x00000000,
     [FRSP_F0_F1, MTFSB1(24)], SNAN_D, "e1001080", "DISC"),

    #  FX latches on a 0->1 TRANSITION of an exception bit, so once VXSNAN is
    #  sticky-set, a guest that clears FX must not have it re-set by a second
    #  signalling NaN. frsp used to set FX unconditionally, which answers
    #  a1001000 here; the guard makes it 21001000 -- FX stays clear, VXSNAN and
    #  the derived VX stay set. This row exists because the after-pass noticed
    #  #327 had fixed the FX latch and left nothing measuring it.
    ("FX latches once only", 0x00000000,
     [FRSP_F0_F1, MTFSB0(0), FRSP_F0_F1], SNAN_D, "21001000", "DISC"),
]


def run_vxsnan_sticky_arith(second):
    """frsp(sNaN), then ANOTHER instruction, then read FPSCR the guest's way.

    #326. The sticky row below runs a second `frsp`, and that turned out to be
    the one instruction in the file that could not break the property: every
    OTHER floating-point handler -- fcmpu, fadd, fsub, fmul, fdiv, fmadd,
    fmsub -- cleared VXSNAN on every execution, seven sites in all, because
    they wrote `fpscr &= ~(PPC_FPSCR_FPCC | PPC_FPSCR_VXNAN)` when only the
    FPCC half is theirs to clear. Book I is explicit that the exception bits
    "are sticky ... until they are set to 0 by an mcrfs, mtfsfi, mtfsf, or
    mtfsb0 instruction", and none of those seven is one of the four.

    So the gate proved stickiness against the single instruction that
    preserved it, while the guest lost the record to the first arithmetic that
    followed. This row takes the second instruction as a parameter for exactly
    that reason -- an instrument only refutes what its inputs reach.
    """
    w, _ = session([
        "msr=0x2000",
        "fpscr=0x00000000",
        "f1=0x7ff0000000000123",
        "f2=0x3ff0000000000000",
        "r5=0x%x" % DEST,
        "put w 0x%x, 0xdeadbeef" % DEST,
        "put w 0x%x, 0xdeadbeef" % (DEST + 4),
        "put w 0x%x, 0x%08x" % (CODE, FRSP_F0_F1),
        "pc=0x%x" % CODE,
        "step 1",
        "put w 0x%x, 0x%08x" % (CODE + 16, second),
        "pc=0x%x" % (CODE + 16),
        "step 1",
        "put w 0x%x, 0x%08x" % (CODE + 32, MFFS_F3),
        "put w 0x%x, 0x%08x" % (CODE + 36, STFD_F3_R5),
        "pc=0x%x" % (CODE + 32),
        "step 2"], 2)
    if w is None or len(w) < 2 or w[1] == "deadbeef":
        return None
    return "set" if (int(w[1], 16) & (1 << 24)) else "clear"


def run_fcmpu_cr(a, b):
    """fcmpu cr0,f1,f2 ; mfcr r3 ; stw r3,0(r4) -- read the CR the guest's way.

    #326. The CR field must receive the full four-bit condition LT/GT/EQ/FU.
    The handler masked the low bit off, so an unordered compare wrote 0000 --
    neither less, greater, equal, NOR unordered, which hardware never
    produces. The three ordered rows are the controls that make the two NaN
    rows mean something: they passed before the fix and after it.
    """
    w, _ = session([
        "msr=0x2000",
        "cr=0x00000000",
        "f1=0x%016x" % a,
        "f2=0x%016x" % b,
        "r4=0x%x" % DEST,
        "put w 0x%x, 0xdeadbeef" % DEST,
        "put w 0x%x, 0x%08x" % (CODE, FCMPU_CR0_F1_F2),
        "put w 0x%x, 0x%08x" % (CODE + 4, MFCR_R3),
        "put w 0x%x, 0x%08x" % (CODE + 8, STW_R3_R4),
        "pc=0x%x" % CODE,
        "step 3"], 1)
    if w is None:
        return None
    return w[0]


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


#  #324: mtfsf's FM field selects eight FOUR-bit FPSCR fields. The decoder built
#  the mask with an EIGHT-bit stride, spreading it across sixty-four bits: the
#  first four FM bits landed entirely above the 32-bit FPSCR and wrote nothing,
#  and the rest wrote the wrong fields.
#
#  This is why every mode row in this file sets FPSCR by DEBUGGER WRITE and the
#  header says using the guest's own mtfsf "would make the mode rows measure the
#  bug instead of the mode". These rows measure the bug on purpose, and they are
#  the reason that note can now be read as history.
#
#  FM=0x01 is the row that matters least and is kept anyway: it was correct on
#  the broken build, by the coincidence of being the last loop iteration with no
#  shift after it. A table of only-broken rows would have suggested the whole
#  instruction was dead, which it was not.
def run_mtfsf(fm, fval, preload=0x00000000):
    """mtfsf FM,f1 ; mffs f3 ; stfd f3 -- read FPSCR back through the guest.

    `preload` is the FPSCR the guest starts from. It defaults to zero, which
    measures only the OR half of the handler's `&= ~mask` / `|= mask & frb`
    pair: from zero, a handler that never cleared would still answer correctly
    on every row. One row preloads all ones and writes zeros, so the clearing
    half is measured too.
    """
    mtfsf = (63 << 26) | ((fm & 0xff) << 17) | (1 << 11) | (711 << 1)
    w, _ = session([
        "msr=0x2000",
        "fpscr=0x%08x" % preload,
        "f1=0x%016x" % fval,
        "r5=0x%x" % DEST,
        "put w 0x%x, 0xdeadbeef" % DEST,
        "put w 0x%x, 0xdeadbeef" % (DEST + 4),
        "put w 0x%x, 0x%08x" % (CODE, mtfsf),
        "put w 0x%x, 0x%08x" % (CODE + 4, MFFS_F3),
        "put w 0x%x, 0x%08x" % (CODE + 8, STFD_F3_R5),
        "pc=0x%x" % CODE,
        "step 3"], 2)
    if w is None:
        return None
    #  big-endian: the FPSCR is the low word of the doubleword
    return w[1]


#  #324. Every row writes a source of all ones with FPSCR forced to zero first,
#  so the byte read back IS the mask the decoder built.
#
#  FM=0x80 selects field 0 -- FX, FEX, VX, OX. Book I's mtfsf note says FX and OX
#  come from (FRB)32 and (FRB)35 while "Bits 1 and 2 (FEX and VX) are set
#  according to the usual rule ... and not from (FRB)33:34": they are OR
#  summaries and mtfsf must never copy them. This row USED to record that as a
#  divergence, answering f0000000; #327 masked mtfsf and made the summaries
#  derived, so it now expects hardware's 90000000 -- FX and OX copied, FEX and
#  VX derived to zero because nothing else is set.
#
#  Three rows moved with it, and that is the interesting part: once the
#  summaries are DERIVED, they re-establish themselves from whatever mtfsf did
#  write. FM=0x40 gains VX from the VXSNAN it writes, FM=0x0f gains VX and FEX
#  from VXSOFT/VXSQRT/VXCVI plus VE, and `mtfsf clears` keeps both because its
#  preload's causes and enables survive a field-0 write. FM=0xff is unchanged
#  only by coincidence -- with every cause and enable set, derivation reproduces
#  the copy. All four bytes were registered from Book I before the code existed.
#
#  FM=0x01 is a PIN and not a DISC: the old 8-bit stride left the last iteration
#  unshifted, so this row answered 0000000f before the fix as well. It flips
#  nothing and must not be counted among the rows that do.
#  FM=0x40 tests the top half of the mask, and it is the row that matters most in
#  practice (it does NOT avoid the summary question any more -- since #327 its
#  want carries a derived VX): field 1 holds
#  VXSNAN, the sticky bit #304 made the emulator set. Under the old stride that
#  field's nibble landed at bits 48-51, above the 32-bit FPSCR, so the guest
#  could not clear VXSNAN at all -- mtfsf is the documented way to do it, and it
#  wrote nothing. #324 is what makes that path real.
#
#  The last row preloads all ones and writes a source whose field 0 is zero, so
#  it measures the CLEARING half of `fpscr &= ~mask; fpscr |= mask & frb`. Every
#  other row starts from zero, where a handler that never cleared would still
#  answer correctly on all of them.
MTFSF_ROWS = [
    #  name,           FM,   frB value,           want,       class, preload
    ("mtfsf FM=0xff",  0xff, 0x00000000ffffffff, "ffffffff", "DISC", 0x00000000),
    ("mtfsf FM=0x80",  0x80, 0x00000000ffffffff, "90000000", "DISC", 0x00000000),
    ("mtfsf FM=0x40",  0x40, 0x00000000ffffffff, "2f000000", "DISC", 0x00000000),
    ("mtfsf FM=0x01",  0x01, 0x00000000ffffffff, "0000000f", "PIN",  0x00000000),
    ("mtfsf FM=0x0f",  0x0f, 0x00000000ffffffff, "6000ffff", "DISC", 0x00000000),
    ("mtfsf clears",   0x80, 0x000000000fffffff, "6fffffff", "DISC", 0xffffffff),
]


def run_fctiwz(fbits):
    """fctiwz f0,f1 ; stfd f0,0(r3) -- the converted word is the LOW half."""
    w, _ = session([
        "msr=0x2000",
        "fpscr=0x00000000",
        "f1=0x%016x" % fbits,
        "r3=0x%x" % DEST,
        "put w 0x%x, 0xdeadbeef" % DEST,
        "put w 0x%x, 0xdeadbeef" % (DEST + 4),
        #  frB is bits 11-15. This word carried 0xFC00001E, whose frB is ZERO,
        #  so it converted f0 and never the operand seeded into f1 -- see the
        #  note on FCTIWZ_ROWS below.
        "put w 0x%x, 0x%08x" % (CODE, 0xFC00081E),      # fctiwz f0,f1
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

#  fctiwz. The NaN answer was the divergence this table was created to pin; #325
#  fixed it and the DIV rows became DISC rows.
FCTIWZ_ROWS = [
    #  #325: was pinned at 00000000 as a recorded divergence from #304 onward.
    #  The ISA converts a NaN to the most negative value, the same answer it
    #  gives for an operand below the representable range. Zero was the worse
    #  kind of wrong: a legitimate result the guest cannot tell apart from a
    #  successful conversion of 0.0.
    #
    #  THE ROW WAS ALSO NOT MEASURING WHAT IT SAID. Its instruction word had
    #  frB = 0, so it converted f0 while the probe seeded the operand into f1 --
    #  the answer was 0 because it converted an empty register, not because the
    #  NaN path returned 0. The source reading was right and the row was
    #  measuring something else that happened to agree. Both are fixed here.
    #
    #  The 1.0 row is the control that exposes it: with a wrong frB the answer
    #  is 0 for ANY operand, so a row whose expected value is nonzero cannot
    #  pass while the encoding is wrong. Every NaN and out-of-range row expects
    #  0x80000000 or 0, which a broken encoding can satisfy by accident.
    #
    #  The out-of-range answer is SIGN-DEPENDENT and the NaN answer is not.
    #  Book I gives the instruction's own rule -- "greater than 2^31-1 ->
    #  0x7FFF_FFFF, less than -2^31 -> 0x8000_0000" -- and Appendix A.2's
    #  model splits it three ways: Infinity Operand and Large Operand both
    #  branch on sign, while SNaN Operand and QNaN Operand return
    #  0x8000_0000 unconditionally. The four rows below pin the sign-dependent
    #  half, which #325 does NOT touch and which the NaN rows cannot reach.
    #  They exist because a plausible misreading -- that PowerPC uses one
    #  invalid sentinel for every bad operand, the way x87 does -- would turn
    #  the positive rows into 0x80000000, and nothing in this gate would have
    #  noticed. A panel seat proposed exactly that change; the ISA refuted it.
    #  1.0 proves the operand register is read; it cannot prove the ROUNDING,
    #  because an integer converts the same way under every mode -- a decode
    #  that reached `fctiw` (round per RN, XO 14) instead of `fctiwz` (XO 15)
    #  would pass it. The 1.9 and -1.9 rows are the ones that separate them:
    #  toward zero gives 1 and -1, nearest would give 2 and -2.
    ("fctiwz 1.0 control",          0x3ff0000000000000, "00000001", "PIN"),
    ("fctiwz 1.9 RTZ",              0x3ffe666666666666, "00000001", "PIN"),
    ("fctiwz -1.9 RTZ",             0xbffe666666666666, "ffffffff", "PIN"),
    ("fctiwz qNaN",                 0x7ff8000000000000, "80000000", "DISC"),
    ("fctiwz -qNaN",                0xfff8000000000000, "80000000", "DISC"),
    ("fctiwz +Inf",                 0x7ff0000000000000, "7fffffff", "PIN"),
    ("fctiwz -Inf",                 0xfff0000000000000, "80000000", "PIN"),
    ("fctiwz 2^31",                 0x41e0000000000000, "7fffffff", "PIN"),
    ("fctiwz -(2^31+1)",            0xc1e0000000200000, "80000000", "PIN"),
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
#  the indexed forms ONLY, and r5 is the publish base and nothing else.
#  Publishing through a register that is also an operand makes a row report
#  whichever value happened to survive. The update-stores address their target
#  through r3 like every other form -- into DEST when the row reads the stored
#  VALUE back, into STORE_AT when it reads the updated base -- so no fourth
#  register is involved (an earlier draft of this comment invented an r6 that
#  appears in no row, which is exactly the confusion the plan exists to stop).
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
    #  name, r3 seed, index (r4 or None), code words, reads, want, class
    #
    #  Every update form gets BOTH a value row and a base row. A base row
    #  alone would pass an implementation with the wrong size or direction
    #  that still advanced r3; a value row alone would pass one that forgot
    #  the update entirely. The first version of this table had base-only
    #  rows for five of the eight forms -- a diff-review seat caught it.
    ("lfsu value",       SRC - 4, None, [0xC4230004, PUBLISH_VALUE], 2,
     "3ff0000000000000", "DISC"),
    ("lfsu updates r3",  SRC - 4, None, [0xC4230004, PUBLISH_BASE], 1,
     "%08x" % SRC, "DISC"),
    ("lfdu value",       SRC,     None, [0xCC230008, PUBLISH_VALUE], 2,
     "3ff0000000000000", "DISC"),
    ("lfdu updates r3",  SRC,     None, [0xCC230008, PUBLISH_BASE], 1,
     "%08x" % (SRC + 8), "DISC"),
    #  The store forms publish nothing themselves: their witness is the
    #  MEMORY they wrote, so they store into DEST and the dump reads it back.
    ("stfsu value",      DEST - 4, None, [0xD4230004], 1,
     "3f800000", "DISC"),
    ("stfsu updates r3", STORE_AT - 4, None, [0xD4230004, PUBLISH_BASE], 1,
     "%08x" % STORE_AT, "DISC"),
    ("stfdu value",      DEST - 8, None, [0xDC230008], 2,
     "3ff0000000000000", "DISC"),
    ("stfdu updates r3", STORE_AT - 8, None, [0xDC230008, PUBLISH_BASE], 1,
     "%08x" % STORE_AT, "DISC"),
    ("lfsux value",      SRC - 4, 4, [0x7C23246E, PUBLISH_VALUE], 2,
     "3ff0000000000000", "DISC"),
    ("lfsux updates r3", SRC - 4, 4, [0x7C23246E, PUBLISH_BASE], 1,
     "%08x" % SRC, "DISC"),
    ("lfdux value",      SRC, 8, [0x7C2324EE, PUBLISH_VALUE], 2,
     "3ff0000000000000", "DISC"),
    ("lfdux updates r3", SRC, 8, [0x7C2324EE, PUBLISH_BASE], 1,
     "%08x" % (SRC + 8), "DISC"),
    ("stfsux value",     DEST - 4, 4, [0x7C23256E], 1,
     "3f800000", "DISC"),
    ("stfsux updates r3", STORE_AT - 4, 4, [0x7C23256E, PUBLISH_BASE], 1,
     "%08x" % STORE_AT, "DISC"),
    ("stfdux value",     DEST - 8, 8, [0x7C2325EE], 2,
     "3ff0000000000000", "DISC"),
    ("stfdux updates r3", STORE_AT - 8, 8, [0x7C2325EE, PUBLISH_BASE], 1,
     "%08x" % STORE_AT, "DISC"),
    #  The non-update PINS. Their displacement and index are NONZERO on
    #  purpose: with a zero offset the effective address equals the base, so
    #  an implementation that wrongly updated would write back the value the
    #  row already expects and the control could not fail. Same seat, same
    #  finding -- these two rows were vacuous exactly that way.
    ("lfs leaves r3",    SRC - 4, None, [0xC0230004, PUBLISH_BASE], 1,
     "%08x" % (SRC - 4), "PIN"),
    ("lfsx leaves r3",   SRC - 4, 4, [0x7C23242E, PUBLISH_BASE], 1,
     "%08x" % (SRC - 4), "PIN"),
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

    #  #324, measured on the build that precedes it. The old decoder shifted 8
    #  bits per iteration while ORing in 4, so the mask sprawled across 64 bits
    #  and only its low 32 survived the AND: FM=0xff and FM=0x0f both collapse
    #  to the same 0f0f0f0f, FM=0x80 landed entirely above bit 31 and wrote
    #  nothing, and FM=0x01 was right only as the last iteration with no shift
    #  after it. The first three were measured; FM=0x0f is stated from the same
    #  mask arithmetic and was added after the fix, so it has no measured
    #  pre-fix byte of its own.
    "mtfsf FM=0xff":           "0f0f0f0f",
    "mtfsf FM=0x80":           "00000000",
    "mtfsf FM=0x01":           "0000000f",
}

#  #325 has no entry above, deliberately. The pre-fix byte for `fctiwz` of a
#  NaN cannot be quoted from the row that recorded it: that row's instruction
#  word had frB = 0 and converted an empty f0, so its 00000000 is evidence
#  about an encoding, not about the NaN path. What WAS measured on the
#  committed build, and is why the encoding came under suspicion at all, is
#  that `fctiwz` of 1.0 through the same row also returned 00000000 -- which
#  no account of the NaN path explains. The `fctiwz 1.0 control` row is that
#  diagnostic, kept.



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

    #  #324: FM decode, measured through the guest's own mtfsf and mffs.
    for name, fm, fval, want, cls, preload in MTFSF_ROWS:
        report(name, run_mtfsf(fm, fval, preload), want, cls)

    for name, r3, r4, words, nread, want, cls in UPDATE_ROWS:
        report(name, run_update(r3, r4, words, nread), want, cls)

    for name, operand, mode, want, cls in COMPOSED_ROWS:
        report(name, run_composed(operand, mode), want, cls)

    #  #327: VX and FEX are DERIVED, not stored. Six rows, both directions.
    for name, pre, seq, seed, want, cls in SUMMARY_ROWS:
        report(name, run_fpscr_seq(pre, seq, seed), want, cls)

    #  VXSNAN must survive a following non-NaN frsp (see run_vxsnan_sticky).
    report("VXSNAN sticky", run_vxsnan_sticky(), "set", "DISC")

    #  #326: and it must survive the instructions that were CLEARING it. frsp
    #  was the only handler that did not, so the row above passed while the
    #  property was broken for every other one.
    for nm, iw in (("fadd", FADD_F0_F1_F2), ("fmul", FMUL_F0_F1_F1),
                   ("fcmpu", FCMPU_CR0_F1_F2)):
        report("VXSNAN sticky vs %s" % nm,
               run_vxsnan_sticky_arith(iw), "set", "DISC")

    #  #326: fcmpu must put all four condition bits in the CR, unordered
    #  included. The ordered rows are controls -- they were already right.
    for nm, a, b, want in (
            ("fcmpu LT", 0x3ff0000000000000, 0x4000000000000000, "80000000"),
            ("fcmpu GT", 0x4000000000000000, 0x3ff0000000000000, "40000000"),
            ("fcmpu EQ", 0x3ff0000000000000, 0x3ff0000000000000, "20000000"),
            ("fcmpu FU qNaN-a", 0x7ff8000000000000, 0x3ff0000000000000,
             "10000000"),
            ("fcmpu FU qNaN-b", 0x3ff0000000000000, 0x7ff8000000000000,
             "10000000")):
        report(nm, run_fcmpu_cr(a, b), want,
               "PIN" if nm.startswith("fcmpu ") and "FU" not in nm else "DISC")

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
