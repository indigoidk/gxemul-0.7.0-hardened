#!/usr/bin/env python3
"""`sh4pcic` WITNESS -- eleven guest-reachable `exit(1)` sites in
`DEVICE_ACCESS(sh4_pcic)`, plus four more in `DEVICE_ACCESS(sh4)`.

RUNG 3 (WITNESS LADDER).  Real SH-4 guest instructions, through real address
decode, real `memory_rw` and real device dispatch, on an UNMODIFIED in-tree
`-E landisk`.  No source is edited, no `device_add` of ours, no new machine
description, no boot required.

*** THIS IS THE PRE-FIX WITNESS, NOT A DETECTOR. ***  No fix exists yet, so all
it can show -- and all it claims to show -- is the SYMPTOM on the committed
build.  It asserts "these guest accesses END THE HOST PROCESS", so it goes RED
the day the defect is gone.  That is what a witness is for; grading it by a
detector's clauses (or the reverse) is a category error in either direction.

    HEAD at authoring time: 3193d56 ("#442 fbpending")
    binary:  build/gxemul, ELF x86-64, built 2026-08-20 23:24, whose source
             build/src/devices/dev_sh4.c is `cmp`-identical to GXEMUL-SEC's.

THE DEFECT.  `dev_sh4.c:816` `DEVICE_ACCESS(sh4_pcic)` serves the window
registered at `dev_sh4.c:2101`:

    memory_device_register(machine->memory, "sh4_pcic", SH4_PCIC,
        N_PCIC_REGS * sizeof(uint32_t), dev_sh4_pcic_access, d, ...)

`SH4_PCIC` is 0xfe200000 (sh4_pcicreg.h:39) and `N_PCIC_REGS` is
`0x224 / sizeof(uint32_t)` = 137 (dev_sh4.c:72), so the window is
0xfe200000..0xfe200223 -- 137 word offsets.  The `switch (relative_addr)` at
dev_sh4.c:834 carries 21 case labels; the other 116 fall to

    default:if (writeflag == MEM_READ)  fatal("[ sh4_pcic: read from ...
            else                        fatal("[ sh4_pcic: write to ...
            exit(1);                                     /*  dev_sh4.c:964  */

*** THE `default:` ARM KILLS ON A **READ**, NOT ONLY ON A WRITE. ***  An
ordinary `mov.l @r1,r2` -- one instruction, no store, nothing privileged --
ends the emulator process.  Nine more sites are value guards on WRITES to
labelled registers, and an eleventh fires on a PCICONF0 READ when the CPU type
is neither SH7751 nor SH7751R.

REACHABILITY, MEASURED (control C7).  0xfe200000 is SH-4 P4 control space:
with SR.MD cleared the identical instruction at the identical address does NOT
reach the device -- an SH exception is taken and the host survives.  So this is
GUEST-KERNEL reachable and NOT guest-user reachable, and the file states that
rather than leaving it to be assumed in either direction.

WHY `-E landisk`.  The device is not landisk-specific: `cpu_sh.c:200` does
`device_add(machine, "sh4")` for EVERY SH-4 CPU (`cpu_type.arch == 4`), so
every SH-4 machine in the tree registers this window.  landisk is chosen
because it is the SH-4 machine with a working in-tree image
(`_images/openbsd76-landisk-bsd.rd`), and because the guard values in the
source are commented "Hardcoded to what OpenBSD/landisk uses" -- i.e. this is
the machine the guards were written for.

NO SH-4 MANUAL IS CITED ANYWHERE IN THIS FILE.  There is none in the tree
(`sh4_manual.txt` is one byte).  Every constant below is either read out of a
header in this repository, with the file and line named, or measured.

usage:  python3 _scratchpad/sh4pcic_witness.py [options]
        run from the PROJECT ROOT (C:/DocumentNoSnc/CC/GXEMUL), under WSL.

  --binary PATH   default ./build/gxemul   *** KEEP THE "./" ***  `os.execvp`
                  on a bare name searches PATH; when it misses, EVERY arm
                  silently reports alive=False and a witness written the naive
                  way "passes" having measured nothing.  Control C0 exists to
                  catch exactly that, and the existence check in main() catches
                  it sooner.
  --kernel PATH   default _images/openbsd76-landisk-bsd.rd
  --jobs N        census parallelism (default 4).  Sessions are read-only and
                  touch no shared tree; only host CPU is contended.  Do NOT run
                  this while a gate is running -- gate oracles are wall-clock.
  --fast          skip the 274-session census (controls + witness rows only)
  --census-only   run only the census
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
#  All READ from this tree, not from memory.  Every one was opened.
SH4_PCIC = 0xfe200000               # src/include/thirdparty/sh4_pcicreg.h:39
N_PCIC_REGS = 0x224 // 4            # src/devices/dev_sh4.c:72        -> 137

#  sh4_pcicreg.h:48..110.  The 21 offsets that carry a `case` label in
#  DEVICE_ACCESS(sh4_pcic), dev_sh4.c:836..951 (`default:` at :957).
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
#  The nine labelled offsets whose WRITE arm carries a value guard + exit(1):
#  dev_sh4.c:839, 873, 882, 891, 900, 909, 918, 927, 936.
VALUE_GUARDED_WRITE = {0x000, 0x014, 0x018, 0x104, 0x108, 0x10c, 0x110,
                       0x1c4, 0x1c8}

#  Guest scratch.  landisk RAM is 64 MB at 0x0c000000 (machine_landisk.c:84);
#  0x8c010000 is its P1 (cached, unmapped) alias, past the 0x8c002000 entry
#  point and inside the loaded image -- the same scratch the committed #441
#  probe uses.
CODE = 0x8c010000
DEST = 0x8c010100
RAMSRC = 0x8c010200

#  Instruction halfwords.  EVERY ONE IS CHECKED AGAINST THE EMULATOR'S OWN
#  DISASSEMBLER in the same session that executes it -- control C5.
OPS = {
    0x6212: "mov.l @r1,r2",
    0x2322: "mov.l r2,@r3",
    0x2102: "mov.l r0,@r1",
    0x2101: "mov.w r0,@r1",
    0x2100: "mov.b r0,@r1",
    0x0009: "nop",
}

#  Two values the DEVICE synthesises.  Neither is stored anywhere this probe
#  writes, so neither can be echoed back to us by RAM.
PCICONF0_ID = 0x350e1054        # dev_sh4.c:846-847, PCI_ID_CODE(0x1054,0x350e)
PCICONF2_CLASS = 0x06000000     # dev_sh4.c:2107, PCI_CLASS_CODE(0x06,0x00,0)

DISASM = {}      # opcode halfword -> the mnemonic text the emulator printed
STARTS = []      # (label, started) for every session this run ever opened


# ------------------------------------------------------------------- session
def session(cmds, nstep, label="", extra=None, disasm_upto=0,
            binary=None, kernel=None):
    """One cold-debugger session.  Returns (buf, alive, started).

    `started` is kept separate from `alive` ON PURPOSE.  A session that never
    reached the debugger prompt ALSO reports alive=False, and scoring that as
    "the guest access killed the host" would let a broken invocation -- missing
    binary, missing image, host out of memory -- masquerade as the defect.
    Every row below requires started=True; control C0 requires it of all of
    them at once.
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

    def wait(mark=0, echo=None, timeout=90):
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
        mark = len(buf)
        send("unassemble 0x%x 0x%x" % (CODE, CODE + disasm_upto))
        for w, txt in re.findall(
                r"^[0-9a-f]{8}:\s+([0-9a-f]{4})\s+(?:<-\s+)?(\S.*?)\s*$",
                buf[mark:].replace("\r", ""), re.M):
            DISASM.setdefault(int(w, 16),
                              re.sub(r"\s+", " ", txt.split(";")[0]).strip())

    if nstep:
        send("step %d" % nstep)

    #  Liveness of the SESSION after the step: a dump that answers proves the
    #  host process is alive; no answer plus a closed pty proves it is not.
    alive = False
    for _ in range(3):
        mark = len(buf)
        if send("dump 0x%x 0x%x" % (DEST, DEST + 4)):
            if re.search(r"0x0*[0-9a-f]+\s+[0-9a-f]{8}", buf[mark:]):
                alive = True
                break
        if died[0]:
            break
        time.sleep(0.4)
        rd(0.4)
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
    return buf, alive, started


def dumped(buf):
    m = re.findall(r"0x0*[0-9a-f]+\s+([0-9a-f]{8})", buf or "")
    return m[-1] if m else None


def le(v):
    """The byte string `dump` prints for a 32-bit value stored little-endian."""
    return "".join("%02x" % ((v >> (8 * i)) & 0xff) for i in range(4))


# ------------------------------------------------------------------- the arms
def read_arm(addr, label, kw, extra=None):
    """Guest 32-bit LOAD from `addr`, then STORE the result to DEST.

    Two instructions, so the row can check the VALUE and not merely survival.
    DEST is pre-poisoned with 0x11111111, so "the device answered 0" is
    distinguishable from "the store never happened".
    """
    return session(["put w 0x%x, 0x11111111" % DEST,
                    "put h 0x%x, 0x%04x" % (CODE + 0, 0x6212),
                    "put h 0x%x, 0x%04x" % (CODE + 2, 0x2322),
                    "r1=0x%x" % addr, "r3=0x%x" % DEST, "pc=0x%x" % CODE],
                   2, label, extra=extra, disasm_upto=4, **kw)


def write_arm(addr, val, label, kw, op=0x2102, extra=None):
    """Guest STORE of `val` to `addr` (mov.l unless `op` says otherwise)."""
    return session(["put w 0x%x, 0x11111111" % DEST,
                    "put h 0x%x, 0x%04x" % (CODE + 0, op),
                    "put h 0x%x, 0x%04x" % (CODE + 2, 0x0009),
                    "r0=0x%x" % val, "r1=0x%x" % addr, "pc=0x%x" % CODE],
                   1, label, extra=extra, disasm_upto=4, **kw)


rows = []


def row(name, ok, got, want):
    rows.append((name, bool(ok), got, want))


def killed(buf, alive, started, needle):
    """A kill row is green only when the process died FOR THE REASON UNDER TEST.

    started -> the session really ran;  not alive -> the process is gone;
    needle  -> the diagnostic printed belongs to the site we aimed at, not to
    some other fatal path that happens to end the process.  Without the third
    clause "the emulator died" is not evidence about this device at all.
    """
    return started and not alive and needle in (buf or "")


# =============================================================================
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--binary", default="./build/gxemul")
    ap.add_argument("--kernel", default="_images/openbsd76-landisk-bsd.rd")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--fast", action="store_true")
    ap.add_argument("--census-only", action="store_true")
    a = ap.parse_args()
    kw = dict(binary=a.binary, kernel=a.kernel)

    #  A missing binary or image is an OPERATIONAL failure, not a measurement.
    #  Say so before spending five minutes manufacturing 274 alive=False rows.
    for p in (a.binary, a.kernel):
        if not os.path.exists(p):
            print("OPERATIONAL FAILURE: %s does not exist (cwd=%s).\n"
                  "Run this from the PROJECT ROOT." % (p, os.getcwd()))
            print("SH4PCIC_WITNESS_FAIL")
            return 2

    t_all = time.time()
    census = {}

    if not a.census_only:
        # -------------------------------------------------------- C1 liveness
        #  A KNOWN value returns through the SAME decode, the SAME two
        #  instructions and the SAME store.  If this is red, nothing else in
        #  the file means anything.
        buf, alive, st = session(
            ["put w 0x%x, 0x5a5a1234" % RAMSRC,
             "put w 0x%x, 0x11111111" % DEST,
             "put h 0x%x, 0x%04x" % (CODE + 0, 0x6212),
             "put h 0x%x, 0x%04x" % (CODE + 2, 0x2322),
             "r1=0x%x" % RAMSRC, "r3=0x%x" % DEST, "pc=0x%x" % CODE],
            2, "C1", disasm_upto=4, **kw)
        c1 = dumped(buf)
        row("C1 LIVENESS: a known word returns through the same decode",
            st and alive and c1 == le(0x5a5a1234),
            "started=%s alive=%s val=%s" % (st, alive, c1),
            "started=True alive=True val=%s" % le(0x5a5a1234))

        # ------------------------------------------- C2 device signature (A)
        #  PCICONF0 READ.  dev_sh4.c:841-848 SYNTHESISES this from the CPU
        #  type; it lives in no `pcic_reg[]` slot and we never wrote it
        #  anywhere.  RAM cannot produce it.
        #
        #  *** THIS IS THE CONTROL THE FOOTBRIDGE PROBE LACKED. ***  That one
        #  returned 0x0 everywhere WITH ITS RAM CONTROL GREEN, because "0" is
        #  what both a live device and a dead path answer.  A row whose oracle
        #  is a specific non-zero value that only the device knows cannot fail
        #  that way.
        buf, alive, st = read_arm(SH4_PCIC + 0x000, "C2", kw)
        c2 = dumped(buf)
        row("C2 DEVICE SIGNATURE: PCICONF0 read = 0x350e1054 (SH7751R ID)",
            st and alive and c2 == le(PCICONF0_ID),
            "started=%s alive=%s val=%s" % (st, alive, c2),
            "val=%s -- RAM would answer 00000000, and this value is held in "
            "no register anyone wrote" % le(PCICONF0_ID))

        # ------------------------------------------- C3 device signature (B)
        #  PCICONF2 holds PCI_CLASS_CODE(BRIDGE, HOST, 0) = 0x06000000, planted
        #  at dev_sh4.c:2107 and touched by nothing else.
        #
        #  *** THIS IS THE SMALL-NON-ZERO ROW. ***  A wrong register field in a
        #  hand-assembled word is silent: it yields 0, which every sentinel or
        #  NaN oracle accepts by accident.  0x06000000 accepts nothing but the
        #  right instruction at the right address.
        buf, alive, st = read_arm(SH4_PCIC + 0x008, "C3", kw)
        c3 = dumped(buf)
        row("C3 DEVICE SIGNATURE: PCICONF2 read = 0x06000000 (small non-zero)",
            st and alive and c3 == le(PCICONF2_CLASS),
            "started=%s alive=%s val=%s" % (st, alive, c3),
            "val=%s -- planted at dev_sh4.c:2107; RAM would answer 00000000"
            % le(PCICONF2_CLASS))

        # ------------------------------------------------ C4 scope / negative
        #  0xfe200400 is 0x1dc bytes PAST the registered window.  If that
        #  killed the host too, this file would be a witness about "P4
        #  accesses" rather than about this device's `default:` arm, and would
        #  prove nothing about the code under test.
        buf, alive, st = read_arm(0xfe200400, "C4", kw)
        c4 = dumped(buf)
        row("C4 SCOPE: a read 0x1dc past the window SURVIVES",
            st and alive and c4 is not None,
            "started=%s alive=%s val=%s" % (st, alive, c4),
            "alive=True -- the kill belongs to sh4_pcic's default:, not to "
            "0xfe2xxxxx in general")

        # ------------------------------------- C6 SURVIVING control, SAME addr
        #  The same address, the same instruction and the same width as W3;
        #  ONLY THE VALUE DIFFERS.  This is what proves the kill is the GUARD
        #  and not the device, the decode, the width or the address.
        buf, alive, st = write_arm(SH4_PCIC + 0x014, 0xac000000, "C6", kw)
        row("C6 SURVIVOR at the SAME address: PCICONF5 <- 0xac000000 lives",
            st and alive, "started=%s alive=%s" % (st, alive),
            "alive=True -- identical store, accepted value")

        #  ...and the device really took it: read it back through the guest.
        buf, alive, st = session(
            ["put w 0x%x, 0x11111111" % DEST,
             "put h 0x%x, 0x%04x" % (CODE + 0, 0x2102),   # mov.l r0,@r1
             "put h 0x%x, 0x%04x" % (CODE + 2, 0x6212),   # mov.l @r1,r2
             "put h 0x%x, 0x%04x" % (CODE + 4, 0x2322),   # mov.l r2,@r3
             "r0=0xac000000", "r1=0x%x" % (SH4_PCIC + 0x014),
             "r3=0x%x" % DEST, "pc=0x%x" % CODE], 3, "C6b", disasm_upto=6,
            **kw)
        c6b = dumped(buf)
        row("C6b the accepted write really reached the register",
            st and alive and c6b == le(0xac000000),
            "started=%s alive=%s val=%s" % (st, alive, c6b),
            "val=%s" % le(0xac000000))

        # -------------------------------------------------- C7 privilege scope
        #  *** THE HONEST REACHABILITY BOUNDARY, MEASURED RATHER THAN ASSUMED.
        #  ***  0xfe200000 is SH-4 P4 control space, so the natural question is
        #  who can get there.  With SR.MD cleared the SAME instruction at the
        #  SAME address does NOT reach the device: an SH exception is taken
        #  instead, DEST keeps its 0x11111111 poison, and the host survives.
        #
        #  So this defect is reachable by guest KERNEL code and not by guest
        #  USER code, and the row says so instead of letting the reader assume
        #  either.  It is not a small class: the guard VALUES in the source are
        #  commented "Hardcoded to what OpenBSD/landisk uses" (dev_sh4.c:869 and
        #  its siblings), which is a statement that the guest kernel already
        #  walks this window on every boot -- any driver that writes a value
        #  those hardcodes did not anticipate ends the emulator.
        buf, alive, st = session(
            ["put w 0x%x, 0x11111111" % DEST,
             "put h 0x%x, 0x%04x" % (CODE + 0, 0x6212),
             "put h 0x%x, 0x%04x" % (CODE + 2, 0x2322),
             "r1=0x%x" % (SH4_PCIC + 0x00c), "r3=0x%x" % DEST,
             "sr=0x00000000", "pc=0x%x" % CODE], 2, "C7", disasm_upto=4, **kw)
        c7 = dumped(buf)
        row("C7 PRIVILEGE: with SR.MD cleared the same access does NOT reach "
            "the device",
            st and alive and c7 == le(0x11111111)
            and "sh4_pcic: read from addr" not in (buf or ""),
            "started=%s alive=%s val=%s device-reached=%s"
            % (st, alive, c7, "sh4_pcic: read from addr" in (buf or "")),
            "alive=True, DEST still %s (untouched), no sh4_pcic diagnostic -- "
            "the defect is guest-KERNEL reachable, not guest-user reachable"
            % le(0x11111111))

        # --------------------------------------------------------- THE WITNESS
        #  W1 is the headline: ONE ORDINARY GUEST LOAD ENDS THE HOST PROCESS.
        buf, alive, st = read_arm(SH4_PCIC + 0x00c, "W1", kw)
        row("W1 a plain 32-bit READ of 0xfe20000c KILLS the emulator",
            killed(buf, alive, st,
                   "sh4_pcic: read from addr 0xfe20000c: TODO"),
            "started=%s alive=%s msg=%s"
            % (st, alive,
               "sh4_pcic: read from addr 0xfe20000c" in (buf or "")),
            "started=True alive=False, with dev_sh4.c:958's read diagnostic "
            "present (exit(1) at dev_sh4.c:964)")

        buf, alive, st = write_arm(SH4_PCIC + 0x00c, 0xdeadbeef, "W2", kw)
        row("W2 a 32-bit WRITE to 0xfe20000c KILLS the emulator",
            killed(buf, alive, st,
                   "sh4_pcic: write to addr 0xfe20000c: 0xdeadbeef: TODO"),
            "started=%s alive=%s" % (st, alive),
            "started=True alive=False + dev_sh4.c:961 diagnostic")

        buf, alive, st = write_arm(SH4_PCIC + 0x014, 0x12345678, "W3", kw)
        row("W3 PCICONF5 <- a value != 0xac000000 KILLS (dev_sh4.c:873)",
            killed(buf, alive, st, "SH4_PCICONF5 unknown value 0x12345678"),
            "started=%s alive=%s" % (st, alive), "started=True alive=False")

        buf, alive, st = write_arm(SH4_PCIC + 0x000, 0x00000001, "W4", kw)
        row("W4 PCICONF0 WRITE kills, though C2's READ of it lived "
            "(dev_sh4.c:839)",
            killed(buf, alive, st, "TODO: Write to SH4_PCICONF0?"),
            "started=%s alive=%s" % (st, alive), "started=True alive=False")

        #  The remaining six value guards, so the whole family is MEASURED and
        #  not inferred from one member.  (A reading seat can buy the class;
        #  only a run buys the instance.)
        for off, val, needle, line in (
                (0x018, 0x00000000, "SH4_PCICONF6 unknown value", 882),
                (0x104, 0x00000000, "SH4_PCILSR0 unknown value", 891),
                (0x108, 0x00000000, "SH4_PCILSR1 unknown value", 909),
                (0x10c, 0x00000000, "SH4_PCILAR0 unknown value", 900),
                (0x110, 0x00000000, "SH4_PCILAR1 unknown value", 918),
                (0x1c4, 0x00000000, "PCIMBR set to", 927),
                (0x1c8, 0x00000000, "PCIIOBR set to", 936)):
            buf, alive, st = write_arm(SH4_PCIC + off, val, "W-%03x" % off, kw)
            row("W5 %-8s <- 0x%08x KILLS (dev_sh4.c:%d)"
                % (LABELLED[off], val, line),
                killed(buf, alive, st, needle),
                "started=%s alive=%s" % (st, alive),
                "started=True alive=False")

        #  The eleventh site (dev_sh4.c:851) is a READ, and it is UNREACHABLE
        #  on landisk-as-shipped because landisk's default CPU is SH7751R
        #  (machine_landisk.c:125), which the strcmp chain accepts.  It IS
        #  reached with the in-tree CPU selector `-C SH7750` -- the MACHINE is
        #  still unmodified and no device is added; an already-supported CPU
        #  type is selected on the command line, exactly as `-E dreamcast`
        #  would select it (machine_dreamcast.c:165).  RECORDED AS A DIFFERENT
        #  CONFIGURATION, NOT AS A LANDISK RESULT.
        buf, alive, st = read_arm(SH4_PCIC + 0x000, "W6", kw,
                                  extra=["-C", "SH7750"])
        row("W6 (-C SH7750) PCICONF0 READ kills (dev_sh4.c:851) "
            "[different CPU selection, same unmodified machine]",
            killed(buf, alive, st, "PCICONF0 read for unimplemented CPU type"),
            "started=%s alive=%s" % (st, alive), "started=True alive=False")

        # ------------------------- the sibling cluster in DEVICE_ACCESS(sh4)
        #  Same file, same "diagnose an unimplemented case by ending the
        #  process" idiom, DIFFERENT device window (SH4_REG_BASE).  Measured
        #  here because the line numbers this witness was commissioned with
        #  were stale; all four are re-derived from the current file and
        #  re-measured.  A SEPARATE SITE IS A SEPARATE ROUND -- these rows
        #  exist to make the class visible, not to widen the fix.
        for addr, val, op, needle, name, line in (
                (0xffd00000, 0x0080, 0x2101, "IRLM not yet supported",
                 "ICR bit 7 (0x80)", 1692),
                (0xffc80038, 0x0018, 0x2100, "TODO: RTC interrupt enable",
                 "RCR1 & 0x18", 1963),
                (0xffa00008, 0x01000000, 0x2102,
                 "Attempt to set top 8 bits of the count register",
                 "DMATCR0 top 8 bits", 1453),
                (0xffd80010, 0x0004, 0x2101,
                 "Unimplemented SH4 timer control bits",
                 "TCR0 TPSC2", 1369)):
            buf, alive, st = write_arm(addr, val, "S-%x" % addr, kw, op=op)
            row("S  sh4 %-18s <- 0x%08x KILLS (dev_sh4.c:%d)"
                % (name, val, line),
                killed(buf, alive, st, needle),
                "started=%s alive=%s" % (st, alive),
                "started=True alive=False")

        #  ...and the NEGATIVE member of that cluster, which the commissioning
        #  brief had WRONG: DEVICE_ACCESS(sh4)'s own `default:` does NOT exit.
        #  Its `exit(1)` at dev_sh4.c:1992 sits inside `#ifdef SH4_DEBUG`
        #  (dev_sh4.c:1991), and SH4_DEBUG is defined NOWHERE in the tree --
        #  `grep -rn SH4_DEBUG src/` returns only the two `#ifdef`s themselves.
        #  Recording it as live would be a wrong record, so it is measured.
        buf, alive, st = read_arm(0xff000004, "S-neg", kw)
        row("S0 CONTROL: DEVICE_ACCESS(sh4)'s own default: does NOT kill "
            "(exit is #ifdef SH4_DEBUG, dev_sh4.c:1991)",
            st and alive, "started=%s alive=%s" % (st, alive),
            "alive=True -- a claim that it kills would be a WRONG RECORD")

        # ---------------------------------------------------------- C5 disasm
        #  EVERY hand-assembled halfword, checked against the emulator's OWN
        #  disassembler in a session that executed it.  A wrong register field
        #  is silent -- it produces a plausible address and a zero result --
        #  which is why C3 also insists on a small NON-ZERO value.
        bad = {"%04x" % w: (DISASM.get(w), t) for w, t in OPS.items()
               if DISASM.get(w) != t}
        row("C5 every planted opcode matches the emulator's own disassembler",
            not bad, "mismatches=%s" % (bad or "none"),
            "all of: " + ", ".join("%04x=%s" % (w, t)
                                   for w, t in sorted(OPS.items())))

    # ------------------------------------------------------------ THE CENSUS
    #  MEASURED, not inferred.  One process per offset per direction: 137
    #  offsets x 2 directions = 274 sessions.  The arithmetic PREDICTION is
    #  137 - 21 = 116 read-kills and 116 + 9 = 125 write-kills; the whole
    #  point of running it is that the prediction is then not doing the work.
    if not a.fast:
        offs = [i * 4 for i in range(N_PCIC_REGS)]

        def one(spec):
            off, wr = spec
            if wr:
                _b, al, st = write_arm(SH4_PCIC + off, 0xdeadbeef,
                                       "cw%03x" % off, kw)
            else:
                _b, al, st = read_arm(SH4_PCIC + off, "cr%03x" % off, kw)
            return (off, wr, al, st)

        specs = [(o, w) for w in (0, 1) for o in offs]
        t0 = time.time()
        with ThreadPoolExecutor(max_workers=max(1, a.jobs)) as ex:
            for off, wr, al, st in ex.map(one, specs):
                census[(off, wr)] = (al, st)
        print("[census: %d sessions in %.0f s]" % (len(specs), time.time() - t0))

        n_start = sum(1 for v in census.values() if v[1])
        row("N0 every census session actually started "
            "(ABSENT DATA MUST FAIL, NOT PASS)",
            len(census) == 2 * N_PCIC_REGS and n_start == 2 * N_PCIC_REGS,
            "sessions=%d started=%d" % (len(census), n_start),
            "%d/%d" % (2 * N_PCIC_REGS, 2 * N_PCIC_REGS))

        #  `.get(..., (True, 0))` defaults to ALIVE, so a missing measurement
        #  can only ever shrink the kill list and turn N1/N2 red.  Absent data
        #  must not be able to manufacture a kill.
        rk = sorted(o for o in offs if census.get((o, 0), (True, 0))[0] is False)
        wk = sorted(o for o in offs if census.get((o, 1), (True, 0))[0] is False)
        pred_rk = sorted(o for o in offs if o not in LABELLED)
        pred_wk = sorted(o for o in offs
                         if o not in LABELLED or o in VALUE_GUARDED_WRITE)

        row("N1 READ: exactly the %d unlabelled offsets kill, and no other"
            % len(pred_rk),
            rk == pred_rk,
            "killed=%d unexpected=%s survived-but-predicted-dead=%s"
            % (len(rk), ["0x%03x" % o for o in rk if o not in pred_rk][:8],
               ["0x%03x" % o for o in pred_rk if o not in rk][:8]),
            "%d offsets == the complement of the 21 case labels" % len(pred_rk))

        row("N2 WRITE: the %d unlabelled + %d value-guarded offsets kill"
            % (len(pred_rk), len(VALUE_GUARDED_WRITE)),
            wk == pred_wk,
            "killed=%d unexpected=%s survived-but-predicted-dead=%s"
            % (len(wk), ["0x%03x" % o for o in wk if o not in pred_wk][:8],
               ["0x%03x" % o for o in pred_wk if o not in wk][:8]),
            "%d offsets" % len(pred_wk))

        surv_r = sorted(LABELLED.get(o, "0x%03x" % o) for o in offs
                        if o not in rk)
        surv_w = sorted(LABELLED.get(o, "0x%03x" % o) for o in offs
                        if o not in wk)
        row("N3 the SURVIVOR SETS are exactly the named registers, by name",
            surv_r == sorted(LABELLED.values())
            and surv_w == sorted(LABELLED[o] for o in LABELLED
                                 if o not in VALUE_GUARDED_WRITE),
            "read-survivors=%s\n            write-survivors=%s"
            % (surv_r, surv_w),
            "read: all 21 labels; write: the 12 without a value guard")

    # ------------------------------------------------- C0, last: absent data
    n_ses = len(STARTS)
    n_ok = sum(1 for _, s in STARTS if s)
    row("C0 EVERY session reached the debugger prompt "
        "(a run that never started must not score ok)",
        n_ses > 0 and n_ok == n_ses,
        "sessions=%d started=%d failed=%s"
        % (n_ses, n_ok, [l for l, s in STARTS if not s][:8]),
        "started == sessions, and sessions > 0")

    print("=" * 78)
    print("sh4pcic -- RUNG-3 PRE-FIX WITNESS  (-E landisk, unmodified)")
    print("  binary %s   kernel %s" % (a.binary, a.kernel))
    print("=" * 78)
    fails = 0
    for name, ok, got, want in rows:
        fails += 0 if ok else 1
        print("  %-4s %-70s" % ("ok" if ok else "FAIL", name))
        if not ok:
            print("       got  %s\n       want %s" % (got, want))
    print()
    if census:
        rk = [o for o in range(0, N_PCIC_REGS * 4, 4)
              if census.get((o, 0), (True, 0))[0] is False]
        wk = [o for o in range(0, N_PCIC_REGS * 4, 4)
              if census.get((o, 1), (True, 0))[0] is False]
        print("  CENSUS (MEASURED, one emulator process each): of the %d word"
              " offsets in the" % N_PCIC_REGS)
        print("  0x224 window at 0xfe200000 --")
        print("    %3d kill the emulator on a plain 32-bit READ" % len(rk))
        print("    %3d kill the emulator on a 32-bit WRITE of 0xdeadbeef"
              % len(wk))
    print("  elapsed %.0f s" % (time.time() - t_all))
    print("SH4PCIC_WITNESS_RESULT=%d/%d" % (len(rows) - fails, len(rows)))
    print("SH4PCIC_WITNESS_PASS" if fails == 0 else "SH4PCIC_WITNESS_FAIL")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
