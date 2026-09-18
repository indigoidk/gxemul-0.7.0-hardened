#!/usr/bin/env python3
"""lax_probe.py -- rung-3 cold-debugger witness for `landiskaux`.

ONE SCRIPT, run unchanged against the pre-fix and the post-fix binary.  Every
`want` is the POST-FIX expectation, so the pre-fix build must show red on the
witness rows and green on the controls, and the post-fix build green on all.

Machine: UNMODIFIED `-E landisk` (machine_landisk.c's own device_add of
"wdc ... addr_mult=2 addr=0x14000000"); no device_add, no address override, no
config file.  `-V` stops before the first guest instruction; each row writes
real SH4 instructions into RAM (P1 0x8c001000) and single-steps them, so every
device access goes through real address translation (P2 0xb... -> phys) and
real memory_rw device dispatch.

Session plumbing is copied from regress/wdc_flood_probe.py's session()
(read-only reuse; nothing in GXEMUL-SEC is modified).  `-x` is omitted: the
landisk console is the main console and needs no slave xterm.
"""
import os
import pty
import re
import select
import sys
import time

BIN = sys.argv[1]
LOG = sys.argv[2] if len(sys.argv) > 2 else None
IMG = "/mnt/c/DocumentNoSnc/CC/GXEMUL/_images"
KERNEL = IMG + "/openbsd76-landisk-bsd.rd"
DISK = IMG + "/wdc-scratch-64m.img"

WDC = 0xb4000000            # P2 (uncached) alias of phys 0x14000000
WD_CMD = WDC + 0x0e         # reg 7 at addr_mult=2: status (R) / command (W)
AUX_NEW = WDC + 0x2c        # where OpenBSD 7.6 writes Device Control (census)
AUX_OLD = WDC + 0x206       # where wdc_altstatus is registered at HEAD
CODE = 0x8c001000
SCRATCH = 0x8c001800
WDCC_IDENTIFY = 0xec
CTL_RST_4BIT = 0x0c         # the first value OpenBSD writes: WDCTL_RST|WDCTL_4BIT
CTL_4BIT = 0x08             # the release value: no WDCTL_RST

NOP = 0x0009
BRA_SELF = 0xaffe


def MOVB_ST(m, n):          # mov.b Rm,@Rn   0010nnnnmmmm0000
    return 0x2000 | (n << 8) | (m << 4)


def MOVB_LD(m, n):          # mov.b @Rm,Rn   0110nnnnmmmm0000
    return 0x6000 | (n << 8) | (m << 4)


def MOVL_ST(m, n):          # mov.l Rm,@Rn   0010nnnnmmmm0010
    return 0x2002 | (n << 8) | (m << 4)


def MOVL_LD(m, n):          # mov.l @Rm,Rn   0110nnnnmmmm0010
    return 0x6002 | (n << 8) | (m << 4)


#  Encodings cross-checked against wdc_flood_probe.py's constants.
assert MOVB_ST(8, 7) == 0x2780 and MOVB_LD(1, 2) == 0x6210
assert MOVL_ST(8, 7) == 0x2782 and MOVL_LD(1, 2) == 0x6212

rows = []
transcripts = []


def row(name, got, want, note=""):
    ok = (got == want)
    rows.append((name, ok))
    print("%-12s %-12s %-12s %-50s %s" % (name, got, want, note,
                                          "ok" if ok else "FAIL"))
    sys.stdout.flush()
    return ok


def session(label, cmds, settle=8.0, spin=2.0):
    argv = [BIN, "-V", "-E", "landisk", "-M", "64",
            "-d", "iR:" + DISK, KERNEL]
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN, argv)
        os._exit(127)
    buf = ""

    def rd(t):
        nonlocal buf
        end = time.time() + t
        while time.time() < end:
            r, _, _ = select.select([fd], [], [], 0.25)
            if not r:
                continue
            try:
                d = os.read(fd, 65536)
            except OSError:
                return False
            if not d:
                return False
            buf += d.decode("latin-1", "replace")
        return True

    alive = rd(settle)
    for i, c in enumerate(cmds):
        try:
            os.write(fd, (c + "\n").encode("latin-1"))
        except OSError:
            alive = False
            break
        if not rd(spin if i == len(cmds) - 1 else 0.35):
            alive = False
            break
    try:
        os.write(fd, b"quit\n")
        rd(0.6)
    except OSError:
        pass
    for fn in (lambda: os.close(fd), lambda: os.waitpid(pid, 0)):
        try:
            fn()
        except OSError:
            pass
    transcripts.append(("=" * 30 + " SESSION %s " % label + "=" * 30, buf))
    return buf, alive


def prog(ops, at=CODE):
    """Write `ops` + `bra .; nop` at `at`, set pc, step exactly len(ops)."""
    put = ["put h 0x%x, 0x%04x" % (at + 2 * i, op) for i, op in enumerate(ops)]
    put += ["put h 0x%x, 0x%04x" % (at + 2 * len(ops), BRA_SELF),
            "put h 0x%x, 0x%04x" % (at + 2 * len(ops) + 2, NOP)]
    return put + ["pc=0x%x" % at, "step %d" % len(ops)]


def printed(t, reg):
    m = re.search(r"print\s+%s\s*\r?\n\s*(0x[0-9a-f]+)" % reg, t)
    return m.group(1) if m else "absent"


def nonex(t, paddr):
    return len(re.findall(r"non-existant paddr=0x%08x " % paddr, t))


def b8(v):
    return v if not v.startswith("0x") else "0x%02x" % (int(v, 16) & 0xff)


#  ------------------------------------------------------------ S0: the map
t, alive = session("map", ["device list"], spin=2.5)
m_alt = re.search(r"wdc_altstatus @ 0x0*([0-9a-f]+), len = 0x([0-9a-f]+)", t)
m_wdc = re.search(r"\s(wdc) @ 0x0*([0-9a-f]+), len = 0x([0-9a-f]+)", t)
n_alt = len(re.findall(r"wdc_altstatus @", t))
row("map count", "%d" % n_alt, "1", "exactly ONE wdc_altstatus registered")
row("map main", ("0x%s/0x%s" % (m_wdc.group(2), m_wdc.group(3))) if m_wdc
    else "absent", "0x14000000/0x10", "command block unchanged: base, 8*2 bytes")
row("map aux", ("0x%s/0x%s" % (m_alt.group(1), m_alt.group(2))) if m_alt
    else "absent", "0x1400002c/0x2", "altstatus where the guest writes")

#  ------------------------------------------------------------ controls
t, alive = session("live",
                   ["r7=0x%x" % SCRATCH, "r8=0x5eed", "r1=0x%x" % SCRATCH, "r2=0"]
                   + prog([MOVL_ST(8, 7), MOVL_LD(1, 2)]) + ["print r2"])
row("live", printed(t, "r2") if alive else "died", "0x5eed",
    "RAM round-trip through the same decode path")

t, alive = session("devsig",
                   ["r1=0x%x" % WD_CMD, "r2=0"] + prog([MOVB_LD(1, 2)])
                   + ["print r2"])
STATUS = b8(printed(t, "r2")) if alive else "died"
row("devsig", "nonzero" if STATUS not in ("died", "absent", "0x00") else STATUS,
    "nonzero", "status reg 0x1400000e answers from device state (%s)" % STATUS)

#  ------------------------------------------------------------ the fix address
t, alive = session("aux_rd",
                   ["r1=0x%x" % AUX_NEW, "r2=0"] + prog([MOVB_LD(1, 2)])
                   + ["print r2"])
row("aux rd", b8(printed(t, "r2")) if alive else "died", STATUS,
    "load @0x1400002c == status byte (unmapped reads 0)")
row("aux rd warn", "%d" % nonex(t, 0x1400002c), "0",
    "no non-existant line for 0x1400002c")


def arm_store_read(label, target, value):
    """IDENTIFY -> status (armed) -> store `value` @ target -> status again."""
    cmds = ["r7=0x%x" % WD_CMD, "r8=0x%x" % WDCC_IDENTIFY,
            "r1=0x%x" % WD_CMD, "r2=0", "r3=0",
            "r4=0x%x" % target, "r5=0x%x" % value]
    ops = [MOVB_ST(8, 7),        # IDENTIFY: fills the inbuf ring -> DRQ
           MOVB_LD(1, 2),        # r2 = status, armed
           MOVB_ST(5, 4),        # the Device Control store under test
           MOVB_LD(1, 3)]        # r3 = status afterwards
    t, alive = session(label, cmds + prog(ops) + ["print r2", "print r3"])
    if not alive:
        return "died", "died", t
    return b8(printed(t, "r2")), b8(printed(t, "r3")), t


a, b, t = arm_store_read("aux_rst", AUX_NEW, CTL_RST_4BIT)
row("aux armed", a, "0x58", "IDENTIFY sets DRQ (liveness of the arming)")
row("aux rst", b, "0x50", "0x0c @0x1400002c: SRST purges ring, DRQ drops")
row("aux rst warn", "%d" % nonex(t, 0x1400002c), "0",
    "store @0x1400002c not reported non-existant")

a, b, t = arm_store_read("aux_4bit", AUX_NEW, CTL_4BIT)
row("aux4b armed", a, "0x58", "IDENTIFY sets DRQ")
row("aux 4bit", b, "0x58", "0x08 (no RST) must NOT purge: accept control")

#  ------------------------------------------------------------ the mirror
t, alive = session("old_rd",
                   ["r1=0x%x" % AUX_OLD, "r2=0"] + prog([MOVB_LD(1, 2)])
                   + ["print r2"])
row("old rd", b8(printed(t, "r2")) if alive else "died", "0x00",
    "load @0x14000206: unmapped after the fix")
row("old rd warn", "%d" % nonex(t, 0x14000206), "1",
    "exactly one non-existant line for 0x14000206")

a, b, t = arm_store_read("old_rst", AUX_OLD, CTL_RST_4BIT)
row("old armed", a, "0x58", "IDENTIFY sets DRQ")
row("old rst", b, "0x58", "0x0c @0x14000206: no longer a reset")
row("old rst warn", "%d" % nonex(t, 0x14000206), "1",
    "store @0x14000206 reported non-existant")

nfail = sum(1 for _, ok in rows if not ok)
print("LAX_RESULT=%d/%d" % (len(rows) - nfail, len(rows)))
if LOG:
    with open(LOG, "w") as f:
        for hdr, txt in transcripts:
            f.write(hdr + "\n" + txt + "\n")
print("LAX_PROBE_DONE")
