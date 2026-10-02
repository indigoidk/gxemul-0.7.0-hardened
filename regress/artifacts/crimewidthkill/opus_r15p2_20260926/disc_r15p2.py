#!/usr/bin/env python3
"""disc_r15p2.py BIN [NAME...] -- the Opus r15p2 seat's NON-EQUIVALENCE discriminators, one short session each.

Each session drives ONE cell that a candidate mutant opens, with its own in-session control, on an unmodified
`-E sgi -e ip32' (the probe's own session() / ld() / st() helpers, copied verbatim from crime_width_probe.table14.py
f5e915f6).  A candidate that scores 218/218 on the probe AND differs from base here is a real, non-equivalent escape;
one that does not differ here is equivalent (or mis-built) and its 218/218 means nothing.
Prints one line per discriminator, then DISC_DONE.
"""
import os, pty, re, select, signal, sys, time

BIN = sys.argv[1]
ONLY = sys.argv[2:]
DUMMY = "/tmp/dummy_crimep.bin"
if not os.path.exists(DUMMY):
    with open(DUMMY, "wb") as f:
        f.write(b"\0" * 16)

CODE = 0x80001000
SCRATCH_RAM = 0xa0001800
LIVE_VAL = 0x12345678
CRIME = 0xb4000000
SENT = 0xdeadbeef
RA = 0x80004000
PROBE_PC = 0xbfc05180
BIT = 0x0101010111010101

R = {"zero": 0, "at": 1, "v0": 2, "v1": 3, "a0": 4, "a1": 5, "a2": 6, "a3": 7, "t0": 8, "t1": 9,
     "s0": 16, "s1": 17, "s2": 18, "s3": 19, "s4": 20, "ra": 31}
OPC = {"lb": 0x20, "lh": 0x21, "lw": 0x23, "lbu": 0x24, "lhu": 0x25, "ld": 0x37,
       "sb": 0x28, "sh": 0x29, "sw": 0x2b, "sd": 0x3f}
OP_B_SELF = 0x1000ffff
OP_NOP = 0


def enc(op, rs, rt, imm=0):
    return (OPC[op] << 26) | (R[rs] << 21) | (R[rt] << 16) | (imm & 0xffff)


assert enc("lb", "at", "v0") == 0x80220000 and enc("sh", "a3", "t0") == 0xa4e80000


def session(cmds, settle=1.5, spin=1.2):
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN, [BIN, "-V", "-x", "-E", "sgi", "-e", "ip32", "-M", "64", "0x80001000:" + DUMMY])
        os._exit(127)
    buf = ""

    def rd(t):
        nonlocal buf
        end = time.time() + t
        while time.time() < end:
            r, _, _ = select.select([fd], [], [], 0.1)
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

    rd(settle)
    for i, c in enumerate(cmds):
        try:
            os.write(fd, (c + "\n").encode("latin-1"))
            ok = rd(spin if i == len(cmds) - 1 else 0.25)
        except OSError:
            break
        if not ok:
            break
    eof = True
    try:
        os.write(fd, b"quit\n")
        eof = not rd(10.0)
    except OSError:
        pass
    if not eof:
        try:
            os.kill(pid, signal.SIGKILL)
        except OSError:
            pass
    try:
        os.close(fd)
    except OSError:
        pass
    how = "nostatus"
    try:
        _, stat = os.waitpid(pid, 0)
        how = ("sig%d" % os.WTERMSIG(stat)) if os.WIFSIGNALED(stat) else ("exit%d" % os.WEXITSTATUS(stat))
    except OSError:
        pass
    return buf.replace("\r", ""), (eof and how == "exit0")


class Addr(object):
    def __init__(self, base):
        self.a = base

    def take(self, n):
        got = self.a
        self.a += 4 * (n + 2) + 0x20
        return got


def run_ops(ops, at):
    put = ["put w 0x%x, 0x%08x" % (at + 4 * i, op) for i, op in enumerate(ops)]
    put += ["put w 0x%x, 0x%08x" % (at + 4 * len(ops), OP_B_SELF),
            "put w 0x%x, 0x%08x" % (at + 4 * len(ops) + 4, OP_NOP)]
    return put + ["pc=0x%x" % at, "step %d" % len(ops)]


def ld(A, op, addr, rt, at=None):
    here = A.take(1) if at is None else at
    return ["at=0x%x" % addr, "%s=0x%x" % (rt, SENT)] + run_ops([enc(op, "at", rt)], here), here


def st(A, op, addr, val, at=None):
    here = A.take(1) if at is None else at
    return ["a3=0x%x" % addr, "t0=0x%x" % val] + run_ops([enc(op, "a3", "t0")], here), here


def nth(t, reg, n):
    ms = re.findall(r"print\s+%s\s*\n\s*(0x[0-9a-f]+)" % reg, t)
    return int(ms[n], 16) if len(ms) > n else None


def ip2(v):
    return "absent" if v is None else ("set" if v & 0x400 else "clear")


def causes(t):
    return [ip2(v) for v in [nth(t, "cause", i) for i in range(len(re.findall(r"print\s+cause", t)))]]


def arm(A):
    """INTMASK = SOFTINT = BIT, stored with 8-byte writes; SOFTINT's store goes to the default arm (no reassert)"""
    x, _ = st(A, "sd", CRIME + 0x18, BIT)
    y, _ = st(A, "sd", CRIME + 0x20, BIT)
    return x + y


def refuse(A, op, off):
    if op[0] == "l":
        return ld(A, op, CRIME + off, "a0")[0]
    return st(A, op, CRIME + off, 0xff if op == "sb" else 0xffff)[0]


def d_irq_set(op, off):
    """latch SET by a refused lb +0x07, then ONE refused `op' at the label; IP2 before/after; accepted lw reasserts"""
    A = Addr(CODE)
    c = arm(A) + ["print cause"]
    c += ld(A, "lb", CRIME + 0x07, "v1")[0] + ["print cause"]
    c += refuse(A, op, off) + ["print cause"]
    c += ld(A, "lw", CRIME + off, "v0")[0] + ["print cause"]
    t, clean = session(c)
    return "cause[pre, after +0x07, after %s +0x%x, after accepted lw]=%s declined=%s" % (
        op, off, causes(t), t.count("-- declined.") if clean else "unclean")


def d_irq_clear(op, off):
    """the FIRST refusal of the session is `op' at the label (latch CLEAR); IP2 before/after; accepted lw reasserts"""
    A = Addr(CODE)
    c = arm(A) + ["print cause"]
    c += refuse(A, op, off) + ["print cause"]
    c += ld(A, "lw", CRIME + off, "v0")[0] + ["print cause"]
    t, clean = session(c)
    return "cause[pre, after %s +0x%x, after accepted lw]=%s declined=%s" % (
        op, off, causes(t), t.count("-- declined.") if clean else "unclean")


def d_ctl2wrc_set():
    """latch SET, then a refused sh 0x0201 at CONTROL (HARD_RESET clear, DOG set, residue 1); then sh 0x0800 + RAM trip"""
    A = Addr(CODE)
    c = ld(A, "lb", CRIME + 0x07, "v1")[0]
    c += st(A, "sh", CRIME + 0x08, 0x0201)[0]
    c += st(A, "sh", CRIME + 0x08, 0x0001)[0]
    c1, _ = st(A, "sw", SCRATCH_RAM, LIVE_VAL)
    c2, _ = ld(A, "lw", SCRATCH_RAM, "s3")
    t, clean = session(c + c1 + c2 + ["print s3"])
    return "CONTROL texts=%s declined=%s ramtrip=%s" % (
        t.count("CRIME_CONTROL: unimplemented") if clean else "unclean",
        t.count("-- declined.") if clean else "unclean", nth(t, "s3", 0) and hex(nth(t, "s3", 0)))


def d_istprev_set():
    """the line ASSERTED, then SOFTINT cleared by a default-arm store (no reassert: the line stays up), then latch SET and
    a refused lb at INTSTAT.  A fall-through reasserts with status 0 and DEASSERTS the line."""
    A = Addr(CODE)
    c = arm(A)
    c += ld(A, "lw", CRIME + 0x18, "v0")[0] + ["print cause"]
    c += st(A, "sd", CRIME + 0x20, 0)[0] + ["print cause"]
    c += ld(A, "lb", CRIME + 0x07, "v1")[0] + ["print cause"]
    c += ld(A, "lb", CRIME + 0x10, "a0")[0] + ["print cause"]
    t, clean = session(c)
    return "cause[after accepted lw +0x18, after SOFTINT=0, after +0x07, after lb +0x10]=%s declined=%s" % (
        causes(t), t.count("-- declined.") if clean else "unclean")


def d_dog(op, latch):
    """accepted `op' 0x0200 (DOG alone) then 0x0201 at CONTROL, optionally after a refused lb +0x07 (latch SET), then
    a RAM trip: the CONTROL texts printed (their values), and whether the CPU ran on"""
    A = Addr(CODE)
    c = ld(A, "lb", CRIME + 0x07, "v1")[0] if latch else []
    c += st(A, op, CRIME + 0x08, 0x0200)[0]
    c += st(A, op, CRIME + 0x08, 0x0201)[0]
    c1, _ = st(A, "sw", SCRATCH_RAM, LIVE_VAL)
    c2, _ = ld(A, "lw", SCRATCH_RAM, "s3")
    t, clean = session(c + c1 + c2 + ["print s3"])
    texts = re.findall(r"CRIME_CONTROL: unimplemented control (0x[0-9a-f]+)", t)
    return "CONTROL texts=%s values=%s ramtrip=%s declined=%s" % (
        len(texts) if clean else "unclean", texts, nth(t, "s3", 0) and hex(nth(t, "s3", 0)),
        t.count("-- declined.") if clean else "unclean")


DISC = {
    "dog_sw_clr": lambda: d_dog("sw", False),
    "dog_sd_clr": lambda: d_dog("sd", False),
    "dog_sw_set": lambda: d_dog("sw", True),
    "ist_lb_set": lambda: d_irq_set("lb", 0x10),
    "imk_lb_set": lambda: d_irq_set("lb", 0x18),
    "ist_sb_clr": lambda: d_irq_clear("sb", 0x10),
    "ist_sh_clr": lambda: d_irq_clear("sh", 0x10),
    "ist_lh_clr": lambda: d_irq_clear("lh", 0x10),
    "imk_lh_clr": lambda: d_irq_clear("lh", 0x18),
    "imk_sh_clr": lambda: d_irq_clear("sh", 0x18),
    "imk_sb_clr": lambda: d_irq_clear("sb", 0x18),
    "ctl_sh0201_set": d_ctl2wrc_set,
    "ist_prev_set": d_istprev_set,
}

print("DISC r15p2  binary=%s" % BIN)
for k in (ONLY or sorted(DISC)):
    print("%-15s %s" % (k, DISC[k]()))
    sys.stdout.flush()
print("DISC_DONE")
