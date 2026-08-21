#!/usr/bin/env python3
"""#443 DETECTOR: an unsupported SH-4 PCIC transaction is DIAGNOSED AND SURVIVED
instead of calling exit(1) -- and, just as importantly, is not silently absorbed.

Rung 3.  Real SH-4 guest instructions through real address decode, real
`memory_rw` and real device dispatch, on an UNMODIFIED in-tree `-E landisk`.
No source is edited, no `device_add` of our own, no boot.

WHAT THIS IS AND IS NOT.  The pre-fix WITNESS (`_scratchpad/sh4pcic_witness.py`)
asserted the SYMPTOM -- a MEASURED census of all 137 word offsets in both
directions found 116 killing the host on a plain 32-bit READ and 125 on a write
-- so it goes red once the defect is gone, which is what a witness should do.
This file is the DETECTOR: it asserts the FIXED behaviour, fails on the pre-fix
build, and is built to fail on the mutants listed at the foot of this docstring.
Grading one by the other's clauses is a category error in either direction.

*** THE ROW THAT MATTERS MOST IS P3, NOT P1. ***  Deleting `exit(1)` and nothing
else does not fix this defect -- it makes it worse.  The store into `pcic_reg[]`
at dev_sh4.c:875-879 is UPSTREAM of every guard, so a rejected value has ALREADY
landed by the time the guard runs, and `exit(1)` was the only thing that stopped
a guest reading it back.  P3 writes an accepted value, then a rejected one, then
READS THE REGISTER BACK through the guest; the naive fix turns a host kill into
silent state corruption, and P3 is the only row in this file that sees it.

P3b is its sibling and covers the `default:` arm, whose restore is otherwise
UNOBSERVABLE: nothing else in the tree reads `pcic_reg[]`, and a `default:` read
answers 0 regardless.  It becomes observable through ADDRESS ALIASING -- the
switch dispatches on the FULL address, but PCIC_REG() indexes on the WORD, so
0xfe200015 (a byte inside PCICONF5) reaches `default:` while sharing PCICONF5's
array slot.  A byte store there clobbers the whole word on the way in; only the
restore puts it back.

P2b uses the same aliasing in the other direction, and it is what gives "reads
answer 0" any teeth at all: on a fresh device every unimplemented slot already
holds 0, and writes to unimplemented offsets are dropped, so `odata = 0` and
`odata = pcic_reg[i]` agree EVERYWHERE until a labelled register has put a
non-zero word into a slot that `default:` can reach.

P4 counts the LATCHED SUFFIX, never a register name.  Under a cold debugger
`single_step` is true, so `debug()`'s quiet_mode early-out never fires and a
probe run this way CANNOT distinguish `fatal()` from `debug()` by presence -- a
#441 detector row was passed by a two-character mutant for exactly that reason.
P5 is P4's other half: a PER-DEVICE latch passes P4 and fails P5.

NO SH-4 MANUAL IS CITED ANYWHERE IN THIS FILE.  There is none in this tree
(`_scratchpad/sh4_manual.txt` is one byte).  Every constant below is read out of
a header in this repository, with the file and line named, or measured.

usage:  sh4_pcic_probe.py <gxemul-binary> <landisk-kernel> [--jobs N] [--fast]

    *** KEEP THE "./" ON THE BINARY. ***  `os.execvp` on a bare name searches
    PATH; when it misses, EVERY arm silently reports alive=False and a probe
    written the naive way "passes" having measured nothing.  P0 catches that,
    and the existence check in main() catches it sooner.
"""
import argparse
import os
import pty
import re
import select
import sys
import time
from concurrent.futures import ThreadPoolExecutor

# ----------------------------------------------------------------- constants
#  All READ from this tree.  Every one was opened.
SH4_PCIC = 0xfe200000               # src/include/thirdparty/sh4_pcicreg.h:39
N_PCIC_REGS = 0x224 // 4            # src/devices/dev_sh4.c:72        -> 137

#  The 21 offsets carrying a `case` label in DEVICE_ACCESS(sh4_pcic),
#  dev_sh4.c:885..1036 (`default:` at :1041).  Names from sh4_pcicreg.h:48..110.
LABELLED = {
    0x000: "PCICONF0", 0x004: "PCICONF1", 0x008: "PCICONF2",
    0x014: "PCICONF5", 0x018: "PCICONF6",
    0x100: "PCICR",    0x104: "PCILSR0",  0x108: "PCILSR1",
    0x10c: "PCILAR0",  0x110: "PCILAR1",
    0x1c0: "PCIPAR",   0x1c4: "PCIMBR",   0x1c8: "PCIIOBR",
    0x1e0: "PCIBCR1",  0x1e4: "PCIBCR2",  0x1e8: "PCIWCR1", 0x1ec: "PCIWCR2",
    0x1f0: "PCIWCR3",  0x1f4: "PCIMCR",   0x1f8: "PCIBCR3",
    0x220: "PCIPDR",
}
ALL_OFFS = list(range(0, N_PCIC_REGS * 4, 4))
UNLABELLED = sorted(o for o in ALL_OFFS if o not in LABELLED)

#  The nine labelled offsets whose WRITE arm carries a value guard, each with
#  the substring its diagnostic prints.  dev_sh4.c:885, 929, 941, 953, 965,
#  977, 989, 1001, 1013.
GUARD_MSG = {
    0x000: "write to SH4_PCICONF0",
    0x014: "SH4_PCICONF5 unknown value",
    0x018: "SH4_PCICONF6 unknown value",
    0x104: "SH4_PCILSR0 unknown value",
    0x108: "SH4_PCILSR1 unknown value",
    0x10c: "SH4_PCILAR0 unknown value",
    0x110: "SH4_PCILAR1 unknown value",
    0x1c4: "PCIMBR set to",
    0x1c8: "PCIIOBR set to",
}

#  Guest scratch.  landisk RAM is 64 MB at 0x0c000000 (machine_landisk.c:84);
#  0x8c010000 is its P1 (cached, unmapped) alias, past the 0x8c002000 entry
#  point and inside the loaded image -- the same scratch #441's probe uses.
CODE = 0x8c010000
DEST = 0x8c010100
RAMSRC = 0x8c010200

#  Instruction halfwords.  EVERY ONE IS CHECKED against the emulator's own
#  disassembler in a session that executed it -- row P11.  A wrong register
#  field is silent: it yields 0, which every zero-valued oracle accepts by
#  accident, which is why P7c also insists on a small NON-ZERO value.
OPS = {
    0x0009: "nop",
    0x6212: "mov.l @r1,r2",
    0x6252: "mov.l @r5,r2",
    0x2102: "mov.l r0,@r1",
    0x2142: "mov.l r4,@r1",
    0x2322: "mov.l r2,@r3",
    0x2312: "mov.l r1,@r3",
    0x2540: "mov.b r4,@r5",
    0x6250: "mov.b @r5,r2",
    0x7104: "add #4,r1",
    0x7304: "add #4,r3",
    0x3510: "cmp/eq r1,r5",
    0x8bfa: "bf 0x%x" % CODE,
}

#  Two values the DEVICE synthesises.  Neither is stored anywhere this probe
#  writes, so neither can be echoed back to us by RAM.
PCICONF0_ID = 0x350e1054        # dev_sh4.c:894-896, PCI_ID_CODE(0x1054,0x350e)
PCICONF2_CLASS = 0x06000000     # dev_sh4.c:2205, PCI_CLASS_CODE(0x06,0x00,0)

LATCHED = "(once per offset)"

#  DEST is pre-poisoned, so "the device answered 0" is distinguishable from
#  "the store never happened".
POISON = 0x11111111

#  The IDENTITY constant.  A probe copied into a tree where it no longer runs
#  all of its rows must not report a green verdict over a shorter file.
EXPECT_ROWS = 29

DISASM = {}      # opcode halfword -> the mnemonic text the emulator printed
STARTS = []      # (label, started) for every session this run ever opened


# ------------------------------------------------------------------- session
def session(cmds, nstep, label="", extra=None, disasm_upto=0,
            binary=None, kernel=None, timeout=90):
    """One cold-debugger session.  Returns (buf, alive, started).

    `started` is kept separate from `alive` ON PURPOSE.  A session that never
    reached the debugger prompt ALSO reports alive=False, and scoring that as
    "the guest access killed the host" would let a broken invocation -- missing
    binary, missing image, host out of memory -- masquerade as a measurement.
    P0 requires started of every session this run ever opened.
    """
    pid, fd = pty.fork()
    if pid == 0:
        argv = [binary, "-V", "-E", "landisk", "-M", "64"] + (extra or []) \
               + [kernel]
        try:
            os.execvp(binary, argv)
        except Exception:
            pass
        os._exit(127)
    buf = ""
    died = [False]

    def rd(t=0.4):
        nonlocal buf
        r, _, _ = select.select([fd], [], [], t)
        if fd not in r:
            return True
        try:
            d = os.read(fd, 65536)
        except OSError:
            died[0] = True
            return False
        if not d:
            died[0] = True
            return False
        buf += d.decode("latin1", "replace")
        return True

    def wait(mark=0, echo=None, timeout=timeout):
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

    def send(s):
        #  `_mark`, not `mark`: gate 6's fresh-mark census keys on that exact
        #  spelling, and every other pty probe in the tree writes it that way.
        b = (s + "\n").encode("latin1")
        _mark = len(buf)
        n = 0
        while n < len(b):
            try:
                n += os.write(fd, b[n:])
            except OSError:
                died[0] = True
                return False
        return wait(mark=_mark, echo=s if s else None)

    started = wait(timeout=120)
    STARTS.append((label, started))
    if not started:
        for fn in (lambda: os.kill(pid, 9), lambda: os.waitpid(pid, 0)):
            try:
                fn()
            except Exception:
                pass
        return buf, False, False

    for c in cmds:
        send(c)

    if disasm_upto:
        _m = len(buf)
        send("unassemble 0x%x 0x%x" % (CODE, CODE + disasm_upto))
        for w, txt in re.findall(
                r"^[0-9a-f]{8}:\s+([0-9a-f]{4})\s+(?:<-\s+)?(\S.*?)\s*$",
                buf[_m:].replace("\r", ""), re.M):
            DISASM.setdefault(int(w, 16),
                              re.sub(r"\s+", " ", txt.split(";")[0]).strip())

    if nstep:
        send("step %d" % nstep)

    #  Liveness of the SESSION after the step: a dump that answers proves the
    #  host process is alive; no answer plus a closed pty proves it is not.
    alive = False
    for _ in range(3):
        _m = len(buf)
        if send("dump 0x%x 0x%x" % (DEST, DEST + 16)):
            if re.search(r"0x0*[0-9a-f]+\s+[0-9a-f]{8}", buf[_m:]):
                alive = True
                break
        if died[0]:
            break
        time.sleep(0.3)
        rd(0.3)
    try:
        os.write(fd, b"quit\n")
    except OSError:
        pass
    t = time.time()
    while time.time() - t < 4 and rd(0.3):
        pass
    for fn in (lambda: os.kill(pid, 9), lambda: os.waitpid(pid, 0)):
        try:
            fn()
        except Exception:
            pass
    return buf, alive, True


def dwords(buf):
    """The words the LAST `dump` printed, in ADDRESS order, exactly as printed.

    `dump` renders raw bytes, so a little-endian 32-bit 0xac000000 stored at
    DEST prints as 000000ac.  Anchored on the TWO spaces `dump` puts after the
    address, which `put`'s echo (`0x8c010100: 11111111`) does not have.
    """
    m = re.findall(r"^\s*0x[0-9a-f]+  ((?:[0-9a-f]{8} )*[0-9a-f]{8})",
                   (buf or "").replace("\r", ""), re.M)
    return m[-1].split() if m else []


def dumped(buf):
    """The word at DEST itself -- w[0], not the last word on the line."""
    w = dwords(buf)
    return w[0] if w else None


def le(v):
    """The byte string `dump` prints for a 32-bit value stored little-endian."""
    return "".join("%02x" % ((v >> (8 * i)) & 0xff) for i in range(4))


def poke(hws, at=CODE):
    return ["put h 0x%x, 0x%04x" % (at + 2 * i, h) for i, h in enumerate(hws)]


def read_arm(addr, label, kw, extra=None):
    """Guest 32-bit LOAD from `addr`, then STORE the result to DEST.

    Two instructions, so a row can check the VALUE and not merely survival.
    """
    return session(["put w 0x%x, 0x%08x" % (DEST, POISON),
                    "r1=0x%x" % addr, "r3=0x%x" % DEST]
                   + poke([0x6212, 0x2322]) + ["pc=0x%x" % CODE],
                   2, label, extra=extra, disasm_upto=4, **kw)


def write_arm(addr, val, label, kw, op=0x2102, extra=None):
    """Guest STORE of `val` to `addr` (mov.l unless `op` says otherwise)."""
    return session(["put w 0x%x, 0x%08x" % (DEST, POISON),
                    "r0=0x%x" % val, "r1=0x%x" % addr]
                   + poke([op, 0x0009]) + ["pc=0x%x" % CODE],
                   1, label, extra=extra, disasm_upto=4, **kw)


rows = []


def row(name, ok, got, want):
    rows.append((name, bool(ok), got, want))


def setcmp(got, want, n=6):
    g, w = set(got), set(want)
    return ("extra=%s missing=%s"
            % (["0x%03x" % x for x in sorted(g - w)][:n],
               ["0x%03x" % x for x in sorted(w - g)][:n]))


# =============================================================================
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("binary")
    ap.add_argument("kernel")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--fast", action="store_true",
                    help="skip the 274-process census.  The rows it feeds are "
                         "still EMITTED, as failures: absent data must fail.")
    a = ap.parse_args()
    kw = dict(binary=a.binary, kernel=a.kernel)

    #  A missing binary or image is an OPERATIONAL failure, not a measurement.
    #  Say so before spending half a minute manufacturing alive=False rows.
    for p in (a.binary, a.kernel):
        if not os.path.exists(p):
            print("OPERATIONAL FAILURE: %s does not exist (cwd=%s)"
                  % (p, os.getcwd()))
            print("SH4_PCIC_FAIL")
            return 2

    t_all = time.time()

    # ------------------------------------------------------------ P7 controls
    #  A KNOWN value returns through the SAME decode, the SAME two instructions
    #  and the SAME store.  If this is red, nothing else in the file means
    #  anything.
    buf, alive, st = session(
        ["put w 0x%x, 0x5a5a1234" % RAMSRC,
         "put w 0x%x, 0x%08x" % (DEST, POISON),
         "r1=0x%x" % RAMSRC, "r3=0x%x" % DEST]
        + poke([0x6212, 0x2322]) + ["pc=0x%x" % CODE], 2, "P7a",
        disasm_upto=4, **kw)
    p7a = dumped(buf)
    row("P7a LIVENESS: a known word returns through the same decode",
        st and alive and p7a == le(0x5a5a1234),
        "started=%s alive=%s val=%s" % (st, alive, p7a),
        "val=%s" % le(0x5a5a1234))

    #  *** THE CONTROL THE FOOTBRIDGE PROBE LACKED. ***  That one returned 0x0
    #  everywhere WITH ITS RAM CONTROL GREEN, because 0 is what both a live
    #  device and a dead path answer.  A row whose oracle is a specific
    #  non-zero value only the device knows cannot fail that way -- and this
    #  probe asserts "reads as zero" in three places, so it needs two of them.
    buf, alive, st = read_arm(SH4_PCIC + 0x000, "P7b", kw)
    p7b = dumped(buf)
    row("P7b DEVICE SIGNATURE: PCICONF0 read = 0x350e1054 (SH7751R ID)",
        st and alive and p7b == le(PCICONF0_ID),
        "started=%s alive=%s val=%s" % (st, alive, p7b),
        "val=%s -- synthesised at dev_sh4.c:894; RAM would answer %s"
        % (le(PCICONF0_ID), le(0)))

    #  THE SMALL-NON-ZERO ROW.  0x06000000 accepts nothing but the right
    #  instruction at the right address.
    buf, alive, st = read_arm(SH4_PCIC + 0x008, "P7c", kw)
    p7c = dumped(buf)
    row("P7c DEVICE SIGNATURE: PCICONF2 read = 0x06000000 (small non-zero)",
        st and alive and p7c == le(PCICONF2_CLASS),
        "started=%s alive=%s val=%s" % (st, alive, p7c),
        "val=%s -- planted at dev_sh4.c:2205" % le(PCICONF2_CLASS))

    #  SCOPE.  0xfe200400 is 0x1dc bytes PAST the registered window.  Without
    #  this row the file would be about "P4 control-space accesses" rather than
    #  about this device, and every survival row would also be satisfied by a
    #  decode that never reached it.
    buf, alive, st = read_arm(0xfe200400, "P8", kw)
    p8 = dumped(buf)
    row("P8 SCOPE: a read 0x1dc past the window survives and is NOT this "
        "device",
        st and alive and p8 is not None and "sh4_pcic" not in (buf or ""),
        "started=%s alive=%s val=%s sh4_pcic-said=%s"
        % (st, alive, p8, "sh4_pcic" in (buf or "")),
        "alive=True and no sh4_pcic diagnostic")

    # -------------------------------------------------- P2 unimplemented read
    buf, alive, st = read_arm(SH4_PCIC + 0x00c, "P2", kw)
    p2 = dumped(buf)
    p2msg = buf or ""
    row("P2 a read of an unimplemented offset returns 0 and the host LIVES",
        st and alive and p2 == le(0),
        "started=%s alive=%s val=%s" % (st, alive, p2),
        "alive=True val=%s (DEST was poisoned %08x, so 0 is a real answer and "
        "not an absent store)" % (le(0), POISON))

    #  The diagnostic must say what the code DID.  A swapped read/write ternary
    #  prints the opposite of the truth and passes every presence-only oracle
    #  -- #441 MEASURED exactly that mutant passing 9/9.
    row("P9a the READ diagnostic names the address, says 'reads as zero', and "
        "is latched",
        ("read from unimplemented addr 0xfe20000c" in p2msg
         and "reads as zero" in p2msg and LATCHED in p2msg
         and "ignored" not in p2msg),
        "addr=%s zero=%s latched=%s said-ignored=%s"
        % ("read from unimplemented addr 0xfe20000c" in p2msg,
           "reads as zero" in p2msg, LATCHED in p2msg, "ignored" in p2msg),
        "first three True, said-ignored False")

    buf, alive, st = write_arm(SH4_PCIC + 0x00c, 0xdeadbeef, "P9b", kw)
    p9b = buf or ""
    row("P9b the WRITE diagnostic names address AND value, says 'ignored', "
        "and is latched",
        (st and alive
         and "write to unimplemented addr 0xfe20000c: 0xdeadbeef" in p9b
         and "ignored" in p9b and LATCHED in p9b
         and "reads as zero" not in p9b),
        "alive=%s addr+val=%s ignored=%s latched=%s said-zero=%s"
        % (alive, "write to unimplemented addr 0xfe20000c: 0xdeadbeef" in p9b,
           "ignored" in p9b, LATCHED in p9b, "reads as zero" in p9b),
        "first four True, said-zero False")

    # ----------------------------------------- P2b `default:` really answers 0
    #  *** WITHOUT THIS ROW, `odata = 0` IS UNTESTABLE. ***  See the module
    #  docstring: on a fresh device the assignment is behaviourally invisible.
    #  The switch dispatches on the FULL address while PCIC_REG() indexes on
    #  the WORD, so 0xfe200101 reaches `default:` while sharing PCICR's slot.
    #  Store 0x12345678 into PCICR (labelled and unguarded, dev_sh4.c:919) and
    #  byte-read the alias: the fix answers 0x00, an `odata = pcic_reg[i]`
    #  answers the LOW byte 0x78 (memory.c:97 takes the low `len` bytes on a
    #  little-endian guest).
    buf, alive, st = session(
        ["put w 0x%x, 0x%08x" % (DEST, POISON), "r0=0x12345678",
         "r1=0x%x" % (SH4_PCIC + 0x100), "r5=0x%x" % (SH4_PCIC + 0x101),
         "r3=0x%x" % DEST]
        + poke([0x2102, 0x6250, 0x2322]) + ["pc=0x%x" % CODE], 3, "P2b",
        disasm_upto=6, **kw)
    p2b = dumped(buf)
    row("P2b `default:` answers 0, NOT the aliased register it shares a slot "
        "with",
        st and alive and p2b == le(0),
        "started=%s alive=%s val=%s" % (st, alive, p2b),
        "val=%s -- pcic_reg[PCIC_REG(0xfe200101)] holds 0x12345678, so "
        "`odata = pcic_reg[i]` gives %s" % (le(0), le(0x78)))

    # ================================================== P3  THE CENTRAL ROW
    #  Accept 0xac000000 (dev_sh4.c:931), then offer 0x12345678, then READ THE
    #  REGISTER BACK through the guest.  The store at dev_sh4.c:877 has already
    #  happened by the time the guard runs, so without the restore at :937 the
    #  guest reads its own rejected value back and the device has told it a lie
    #  it will act on.  A "fix" that only deletes exit(1) fails HERE and
    #  nowhere else in this file.
    buf, alive, st = session(
        ["put w 0x%x, 0x%08x" % (DEST, POISON), "r0=0xac000000",
         "r4=0x12345678", "r1=0x%x" % (SH4_PCIC + 0x014), "r3=0x%x" % DEST]
        + poke([0x2102, 0x2142, 0x6212, 0x2322]) + ["pc=0x%x" % CODE], 4,
        "P3", disasm_upto=8, **kw)
    p3 = dumped(buf)
    p3msg = buf or ""
    row("P3 *** A REJECTED WRITE DOES NOT PERSIST *** (PCICONF5, read back "
        "through the guest)",
        st and alive and p3 == le(0xac000000),
        "started=%s alive=%s val=%s" % (st, alive, p3),
        "val=%s -- the accepted value survives.  Deleting exit(1) alone gives "
        "%s: silent state corruption, strictly worse than the host kill it "
        "replaced" % (le(0xac000000), le(0x12345678)))
    row("P3a the rejection was DIAGNOSED (a silent drop is not the fix either)",
        "SH4_PCICONF5 unknown value 0x12345678" in p3msg and LATCHED in p3msg,
        "msg=%s latched=%s"
        % ("SH4_PCICONF5 unknown value 0x12345678" in p3msg, LATCHED in p3msg),
        "both True")

    #  P3b: the same property in the `default:` arm, where it is otherwise
    #  invisible -- see the module docstring.  A BYTE store to 0xfe200015 hits
    #  `default:` and clobbers PCICONF5's whole word on the way in; only the
    #  restore at dev_sh4.c:1060 puts it back.
    buf, alive, st = session(
        ["put w 0x%x, 0x%08x" % (DEST, POISON), "r0=0xac000000", "r4=0xff",
         "r1=0x%x" % (SH4_PCIC + 0x014), "r5=0x%x" % (SH4_PCIC + 0x015),
         "r3=0x%x" % DEST]
        + poke([0x2102, 0x2540, 0x6212, 0x2322]) + ["pc=0x%x" % CODE], 4,
        "P3b", disasm_upto=8, **kw)
    p3b = dumped(buf)
    p3bmsg = buf or ""
    row("P3b a dropped `default:` write does not persist either (byte alias "
        "0xfe200015 into PCICONF5's slot)",
        st and alive and p3b == le(0xac000000)
        and "write to unimplemented addr 0xfe200015: 0xff" in p3bmsg,
        "started=%s alive=%s val=%s msg=%s"
        % (st, alive, p3b,
           "write to unimplemented addr 0xfe200015: 0xff" in p3bmsg),
        "val=%s -- without the restore the byte store leaves %s in PCICONF5"
        % (le(0xac000000), le(0xff)))

    # ------------------------------------------------------------ P6 survivor
    #  The SAME address, instruction and width as P3's second store; ONLY THE
    #  VALUE DIFFERS.  This is what proves the diagnostic belongs to the GUARD
    #  and not to the device, the decode, the width or the address -- and the
    #  quiet clause is the D10 lesson from #441: a mutant that complains about
    #  every access passes every presence-only row and floods a real boot.
    buf, alive, st = session(
        ["put w 0x%x, 0x%08x" % (DEST, POISON), "r0=0xac000000",
         "r1=0x%x" % (SH4_PCIC + 0x014), "r3=0x%x" % DEST]
        + poke([0x2102, 0x6212, 0x2322]) + ["pc=0x%x" % CODE], 3, "P6",
        disasm_upto=6, **kw)
    p6 = dumped(buf)
    p6msg = buf or ""
    row("P6 SURVIVOR: PCICONF5 <- 0xac000000 is accepted AND reaches the "
        "register",
        st and alive and p6 == le(0xac000000),
        "started=%s alive=%s val=%s" % (st, alive, p6),
        "val=%s" % le(0xac000000))
    row("P6b an ACCEPTED access is not diagnosed at all",
        bool(p6msg) and LATCHED not in p6msg and "sh4_pcic" not in p6msg,
        "latched=%s any-sh4_pcic-line=%s"
        % (LATCHED in p6msg, "sh4_pcic" in p6msg),
        "both False -- a correct driver access must produce no complaint, and "
        "fatal() cannot be silenced with -q")

    # ------------------------------------------------------ P4 / P5 the latch
    #  TWO reads of the SAME offset in ONE process.  Each fresh process starts
    #  with every flag clear, so a two-SESSION version of this row cannot see a
    #  latch at all -- #441 shipped that mistake and a mutant passed 9/9.
    buf, alive, st = session(
        ["put w 0x%x, 0x%08x" % (DEST, POISON), "r1=0x%x" % (SH4_PCIC + 0x00c),
         "r3=0x%x" % DEST]
        + poke([0x6212, 0x6212, 0x2322]) + ["pc=0x%x" % CODE], 3, "P4", **kw)
    p4n = (buf or "").count(LATCHED)
    row("P4 THE LATCH: a second access to the SAME offset is not repeated",
        st and alive and p4n == 1,
        "started=%s alive=%s latched-lines=%d" % (st, alive, p4n),
        "latched-lines=1 -- count the SUFFIX, never the register name: under a "
        "cold debugger a probe cannot tell fatal() from debug() by presence")

    #  TWO DIFFERENT offsets in ONE process.  A PER-DEVICE latch passes P4 and
    #  fails here, which is the whole reason both rows exist.
    buf, alive, st = session(
        ["put w 0x%x, 0x%08x" % (DEST, POISON), "r1=0x%x" % (SH4_PCIC + 0x00c),
         "r5=0x%x" % (SH4_PCIC + 0x010), "r3=0x%x" % DEST]
        + poke([0x6212, 0x6252, 0x2322]) + ["pc=0x%x" % CODE], 3, "P5",
        disasm_upto=6, **kw)
    p5n = (buf or "").count(LATCHED)
    p5addrs = set(re.findall(r"unimplemented addr 0x([0-9a-f]+)", buf or ""))
    row("P5 PER-OFFSET, not per-device: two DIFFERENT offsets each report once",
        st and alive and p5n == 2 and p5addrs == {"fe20000c", "fe200010"},
        "started=%s alive=%s latched-lines=%d addrs=%s"
        % (st, alive, p5n, sorted(p5addrs)),
        "latched-lines=2 over both addresses -- a per-DEVICE latch gives 1 and "
        "still passes P4")

    # ---------------------------------------------- P10 the unimplemented CPU
    #  A DIFFERENT CPU SELECTION, not a different machine: SH7750 is an in-tree
    #  type (machine_dreamcast.c:165 selects it), the machine description is
    #  unmodified and no device is added.  Recorded as its own configuration
    #  rather than as a landisk result.
    buf, alive, st = read_arm(SH4_PCIC + 0x000, "P10", kw,
                              extra=["-C", "SH7750"])
    p10 = dumped(buf)
    p10msg = buf or ""
    row("P10 (-C SH7750) PCICONF0 read for an unimplemented CPU answers 0 and "
        "the host LIVES",
        st and alive and p10 == le(0)
        and "PCICONF0 read for unimplemented CPU type SH7750" in p10msg
        and LATCHED in p10msg,
        "started=%s alive=%s val=%s msg=%s"
        % (st, alive, p10,
           "PCICONF0 read for unimplemented CPU type SH7750" in p10msg),
        "alive=True val=%s with the named, latched diagnostic" % le(0))

    # ========================================== P1  THE CENSUS, IN ONE PROCESS
    #  137 offsets x BOTH directions -- 274 device accesses -- in ONE emulator
    #  process, in about a fifth of a second.  Pre-fix the host is gone by the
    #  SECOND access.
    #
    #  The loop body is five instructions; r1 walks the window and r5 is the
    #  end, and the trailing stores of r1 AND r2 are what prove it ran to
    #  completion rather than stopping early with the host still alive.
    def census_loop(order, label):
        body = ([0x6212, 0x2102] if order == "rw" else [0x2102, 0x6212]) \
               + [0x7104, 0x3510, 0x8bfa, 0x2312, 0x7304, 0x2322]
        return session(
            ["put w 0x%x, 0x%08x" % (DEST, POISON),
             "put w 0x%x, 0x%08x" % (DEST + 4, POISON),
             "r0=0xdeadbeef", "r1=0x%x" % SH4_PCIC,
             "r5=0x%x" % (SH4_PCIC + N_PCIC_REGS * 4), "r3=0x%x" % DEST]
            + poke(body) + ["pc=0x%x" % CODE],
            N_PCIC_REGS * 5 + 3, label, disasm_upto=16, timeout=180, **kw)

    t0 = time.time()
    buf, alive, st = census_loop("rw", "P1")
    p1w = dwords(buf)
    p1_reads = sorted(int(x, 16) - SH4_PCIC for x in
                      re.findall(r"read from unimplemented addr 0x([0-9a-f]+)",
                                 buf or ""))
    p1_writes = re.findall(r"write to unimplemented addr 0x([0-9a-f]+)",
                           buf or "")
    p1_guards = sorted(o for o, m in GUARD_MSG.items() if m in (buf or ""))
    row("P1 CENSUS: 137 reads + 137 writes in ONE process; the host LIVES and "
        "the loop finishes",
        st and alive and len(p1w) >= 2 and p1w[0] == le(SH4_PCIC + 0x224),
        "started=%s alive=%s r1=%s r2=%s (%.1f s)"
        % (st, alive, p1w[0] if p1w else None,
           p1w[1] if len(p1w) > 1 else None, time.time() - t0),
        "alive=True and r1 walked to %s" % le(SH4_PCIC + 0x224))
    row("P1b the READ direction reports EXACTLY the %d unlabelled offsets"
        % len(UNLABELLED),
        p1_reads == UNLABELLED,
        "reported=%d %s" % (len(p1_reads), setcmp(p1_reads, UNLABELLED)),
        "the complement of the 21 case labels, and nothing else")
    row("P1c all %d value guards reject 0xdeadbeef and say so by name"
        % len(GUARD_MSG),
        p1_guards == sorted(GUARD_MSG),
        "reported=%d %s"
        % (len(p1_guards), setcmp(p1_guards, sorted(GUARD_MSG))),
        "all nine, each by its own diagnostic")
    #  The latch is per OFFSET, not per (offset, direction).  Pinning it here
    #  STATES the design rather than leaving a reader to infer it from silence.
    row("P1d the latch is per OFFSET: a write at an already-reported offset is "
        "silent",
        p1_writes == [],
        "write reports behind a read at the same offset=%d" % len(p1_writes),
        "0 -- deliberate, and asserted rather than assumed")

    t0 = time.time()
    buf, alive, st = census_loop("wr", "P1e")
    p1ew = dwords(buf)
    p1e_writes = sorted(int(x, 16) - SH4_PCIC for x in
                        re.findall(r"write to unimplemented addr 0x([0-9a-f]+)",
                                   buf or ""))
    p1e_reads = re.findall(r"read from unimplemented addr 0x([0-9a-f]+)",
                           buf or "")
    p1e_guards = sorted(o for o, m in GUARD_MSG.items() if m in (buf or ""))
    row("P1e CENSUS, WRITE FIRST: the other 274 accesses in one process, host "
        "LIVES",
        st and alive and len(p1ew) >= 1 and p1ew[0] == le(SH4_PCIC + 0x224),
        "started=%s alive=%s r1=%s (%.1f s)"
        % (st, alive, p1ew[0] if p1ew else None, time.time() - t0),
        "alive=True and r1 walked to %s" % le(SH4_PCIC + 0x224))
    row("P1f the WRITE direction reports EXACTLY the same %d offsets"
        % len(UNLABELLED),
        p1e_writes == UNLABELLED and p1e_reads == []
        and p1e_guards == sorted(GUARD_MSG),
        "written=%d %s reads-behind=%d guards=%d"
        % (len(p1e_writes), setcmp(p1e_writes, UNLABELLED), len(p1e_reads),
           len(p1e_guards)),
        "the same complement, no read reports behind them, all nine guards")

    # ================================ P12  THE CENSUS, ONE PROCESS PER ACCESS
    #  The direct post-fix mirror of the witness's headline -- 116 read-kills
    #  and 125 write-kills become 0 and 0 -- and independent of P1 in one way
    #  that matters: every access here meets a device whose latch bits are ALL
    #  CLEAR, so no offset's result can depend on an earlier offset's.
    census = {}
    cens_s = 0.0
    if not a.fast:
        def one(spec):
            off, wr = spec
            if wr:
                b, al, s = write_arm(SH4_PCIC + off, 0xdeadbeef,
                                     "cw%03x" % off, kw)
            else:
                b, al, s = read_arm(SH4_PCIC + off, "cr%03x" % off, kw)
            return (off, wr, al, s, dumped(b))

        specs = [(o, w) for w in (0, 1) for o in ALL_OFFS]
        t0 = time.time()
        with ThreadPoolExecutor(max_workers=max(1, a.jobs)) as ex:
            for off, wr, al, s, v in ex.map(one, specs):
                census[(off, wr)] = (al, s, v)
        cens_s = time.time() - t0

    #  `.get(..., (False, ...))` defaults to DEAD, so a missing measurement can
    #  only ever turn these rows RED.  Absent data must not be able to
    #  manufacture a survivor.
    n_start = sum(1 for v in census.values() if v[1])
    dead_r = sorted(o for o in ALL_OFFS
                    if not census.get((o, 0), (False, False, None))[0])
    dead_w = sorted(o for o in ALL_OFFS
                    if not census.get((o, 1), (False, False, None))[0])
    bad_z = sorted(o for o in UNLABELLED
                   if census.get((o, 0), (False, False, None))[2] != le(0))
    skipped = " -- SKIPPED (--fast), which is a FAILURE by design" if a.fast \
              else ""
    row("P12 every one of the %d census sessions started (ABSENT DATA MUST "
        "FAIL)" % (2 * N_PCIC_REGS),
        len(census) == 2 * N_PCIC_REGS and n_start == 2 * N_PCIC_REGS,
        "sessions=%d started=%d%s" % (len(census), n_start, skipped),
        "%d/%d" % (2 * N_PCIC_REGS, 2 * N_PCIC_REGS))
    row("P12a NO offset kills the host on a READ (the witness measured 116 of "
        "%d)" % N_PCIC_REGS,
        not a.fast and dead_r == [],
        "kills=%d %s%s"
        % (len(dead_r), ["0x%03x" % o for o in dead_r][:6], skipped),
        "0 of %d" % N_PCIC_REGS)
    row("P12b NO offset kills the host on a WRITE (the witness measured 125 of "
        "%d)" % N_PCIC_REGS,
        not a.fast and dead_w == [],
        "kills=%d %s (%.0f s)%s"
        % (len(dead_w), ["0x%03x" % o for o in dead_w][:6], cens_s, skipped),
        "0 of %d" % N_PCIC_REGS)
    row("P12c every unlabelled offset reads 0 from a FRESH device, one process "
        "each",
        not a.fast and bad_z == [],
        "wrong=%d %s%s"
        % (len(bad_z), ["0x%03x" % o for o in bad_z][:6], skipped),
        "all %d answer %s" % (len(UNLABELLED), le(0)))

    # --------------------------------------------------------- P11 disassembly
    #  EVERY hand-assembled halfword, checked against the emulator's OWN
    #  disassembler in a session that executed it.  A wrong register field is
    #  silent -- it produces a plausible address and a zero result -- which is
    #  why P7c also insists on a small non-zero value.
    bad = {"%04x" % w: (DISASM.get(w), t) for w, t in OPS.items()
           if DISASM.get(w) != t}
    row("P11 every planted opcode matches the emulator's own disassembler",
        not bad, "mismatches=%s" % (bad or "none"),
        "all of: " + ", ".join("%04x" % w for w in sorted(OPS)))

    # ------------------------------------------------- P0, last: absent data
    n_ses = len(STARTS)
    n_ok = sum(1 for _, s in STARTS if s)
    vals = [p7a, p7b, p7c, p8, p2, p2b, p3, p3b, p6, p10]
    row("P0 EVERY session reached the debugger prompt AND every arm produced "
        "data",
        n_ses > 0 and n_ok == n_ses and all(v is not None for v in vals)
        and p4n >= 1 and p5n >= 1 and len(p1w) >= 2,
        "sessions=%d started=%d failed=%s vals=%s"
        % (n_ses, n_ok, [l for l, s in STARTS if not s][:6], vals),
        "started == sessions > 0, and every value present")

    # ------------------------------------------------------------ P13 identity
    row("P13 IDENTITY row count -- guards against a stale copy",
        len(rows) + 1 == EXPECT_ROWS, "rows=%d" % (len(rows) + 1),
        "rows=%d" % EXPECT_ROWS)

    print("=" * 78)
    print("#443  SH4 PCIC unsupported transaction -- DETECTOR "
          "(-E landisk, unmodified)")
    print("  binary %s   kernel %s" % (a.binary, a.kernel))
    print("=" * 78)
    fails = 0
    for name, ok, got, want in rows:
        fails += 0 if ok else 1
        print("  %-4s %-70s" % ("ok" if ok else "FAIL", name))
        if not ok:
            print("       got  %s\n       want %s" % (got, want))
    print()
    print("  elapsed %.0f s" % (time.time() - t_all))
    print("SH4_PCIC_RESULT=%d/%d" % (len(rows) - fails, len(rows)))
    print("SH4_PCIC_PASS" if fails == 0 else "SH4_PCIC_FAIL")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
