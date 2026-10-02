#!/usr/bin/env python3
"""disc_c3.py BASEBIN MUTBIN NAME -- one guest-only discriminating session, run on base AND mutant with the SAME
script, unmodified -E sgi -e ip32 -M 64 (the probe's own apparatus, copied from disc_c2.py / crime_width_probe.py).
A survivor is NON-EQUIVALENT iff the observable differs base vs mutant.  Sentinel DISC_DONE."""
import os, pty, re, select, signal, sys, time

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
R = {"zero": 0, "at": 1, "v0": 2, "v1": 3, "a0": 4, "a1": 5, "a2": 6, "a3": 7, "t0": 8, "t1": 9,
     "s0": 16, "s1": 17, "s2": 18, "s3": 19, "ra": 31}
OPC = {"lb": 0x20, "lh": 0x21, "lw": 0x23, "lbu": 0x24, "lhu": 0x25, "ld": 0x37,
       "sb": 0x28, "sh": 0x29, "sw": 0x2b, "sd": 0x3f}


def enc(op, rs, rt, imm=0):
    return (OPC[op] << 26) | (R[rs] << 21) | (R[rt] << 16) | (imm & 0xffff)


assert enc("lh", "at", "v0") == 0x84220000 and enc("sd", "a3", "t0") == 0xfce80000
assert enc("lb", "at", "v0") == 0x80220000 and enc("sw", "a3", "t0") == 0xace80000


def session(BIN, cmds, settle=1.5, spin=1.2):
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


def pr(t, reg):
    m = re.search(r"print\s+%s\s*\n\s*(0x[0-9a-f]+)" % reg, t)
    return ("0x%x" % int(m.group(1), 16)) if m else "absent"


class Addr(object):
    def __init__(self, base):
        self.a = base

    def take(self, n):
        got = self.a
        self.a += 4 * (n + 2) + 0x20
        return got


def run_ops(ops, at):
    put = ["put w 0x%x, 0x%08x" % (at + 4 * i, op) for i, op in enumerate(ops)]
    put += ["put w 0x%x, 0x%08x" % (at + 4 * len(ops), 0x1000ffff), "put w 0x%x, 0x%08x" % (at + 4 * len(ops) + 4, 0)]
    return put + ["pc=0x%x" % at, "step %d" % len(ops)]


def ld(A, op, addr, rt, at=None):
    return ["at=0x%x" % addr, "%s=0x%x" % (rt, SENT)] + run_ops([enc(op, "at", rt)], A.take(1) if at is None else at)


def st(A, op, addr, val):
    return ["a3=0x%x" % addr, "t0=0x%x" % val] + run_ops([enc(op, "a3", "t0")], A.take(1))


def roundtrip(A):
    return st(A, "sw", SCRATCH_RAM, LIVE_VAL) + ld(A, "lw", SCRATCH_RAM, "v1") + ["print v1"]


BIT = 0x0101000010000001        # the probe's own IRQ seed


S = {
    # re-arm: refusal, ACCEPTED access that takes the cell, refusal -> notice count
    "rearm_ctlrd": lambda A: ld(A, "lb", CRIME + 7, "v0") + ld(A, "lw", CRIME + 8, "a0") + ld(A, "lb", CRIME + 6, "v0")
                             + roundtrip(A),
    "rearm_dogclr": lambda A: ld(A, "lb", CRIME + 7, "v0") + st(A, "sw", CRIME + 8, 0x01) + ld(A, "lb", CRIME + 6, "v0")
                              + roundtrip(A),
    "rearm_ctl0": lambda A: ld(A, "lb", CRIME + 7, "v0") + st(A, "sw", CRIME + 8, 0x0) + ld(A, "lb", CRIME + 6, "v0")
                            + roundtrip(A),
    # pre-set: ACCEPTED access that takes the cell, then one refusal -> notice count
    "pre_istat": lambda A: ld(A, "lw", CRIME + 0x10, "a0") + ld(A, "lb", CRIME + 7, "v0") + roundtrip(A),
    "pre_revbr": lambda A: ["ra=0x%x" % RA] + ld(A, "lw", CRIME + 0, "a0", at=PROBE_PC) + ["print pc"]
                           + ld(A, "lb", CRIME + 7, "v0") + roundtrip(A),
    "pre_dogbr": lambda A: st(A, "sw", CRIME + 8, 0x200) + ld(A, "lb", CRIME + 7, "v0") + roundtrip(A),
    "pre_ctlrd": lambda A: ld(A, "lw", CRIME + 8, "a0") + ld(A, "lb", CRIME + 7, "v0") + roundtrip(A),
    # latch TEST keyed on a label: refusal elsewhere first, then two refusals at the label
    "byp_rev": lambda A: ld(A, "lb", CRIME + 7, "v0") + ld(A, "lb", CRIME + 0, "v0") + ld(A, "lh", CRIME + 0, "v0")
                         + roundtrip(A),
    "byp_time": lambda A: ld(A, "lb", CRIME + 7, "v0") + ld(A, "lb", CRIME + 0x38, "v0")
                          + ld(A, "lh", CRIME + 0x38, "v0") + roundtrip(A),
    # answer: (1) the probe's own seed -> blindness; (2) a seed nonzero in bytes 2-3 -> the leak shows
    "ans_hi32_b5": lambda A: (st(A, "sd", CRIME + 0x20, BIT) + ld(A, "lb", CRIME + 0x10, "a0")
                              + ld(A, "lh", CRIME + 0x10, "a1") + ["print a0", "print a1"]
                              + st(A, "sd", CRIME + 0x20, 0x0000ffff00000000) + st(A, "sd", CRIME + 0x18, 0x00005aa500000000)
                              + ld(A, "lb", CRIME + 0x10, "v0") + ld(A, "lh", CRIME + 0x10, "s0")
                              + ld(A, "lh", CRIME + 0x18, "s1") + ["print v0", "print s0", "print s1"]),
    # landing at an unnamed bit-4-clear slot, read back by an accepted ld
    "land_b4clr": lambda A: (st(A, "sb", CRIME + 0x47, 0xff) + ld(A, "ld", CRIME + 0x40, "a0")
                             + st(A, "sh", CRIME + 0x4c, 0xabcd) + ld(A, "ld", CRIME + 0x48, "a1")
                             + ["print a0", "print a1"]),
    # the CONTROL answer at 1 byte (and at 2, to show ctl v0's cell reads 0 under this mutant)
    "ans_ctl_lb": lambda A: (ld(A, "lb", CRIME + 8, "v0") + ld(A, "lh", CRIME + 8, "a0") + ["print v0", "print a0"]),
}


def observe(name, t, clean):
    decl = t.count("-- declined.") if clean else "unclean"
    ex = ""
    if name == "ans_hi32_b5":
        ex = ("BIT-seed: lb+0x10=%s lh+0x10=%s | SOFTINT=0x0000ffff00000000: lb+0x10=%s lh+0x10=%s; INTMASK=0x00005aa5..: "
              "lh+0x18=%s" % (pr(t, "a0"), pr(t, "a1"), pr(t, "v0"), pr(t, "s0"), pr(t, "s1")))
    elif name == "land_b4clr":
        ex = "ld+0x40 after sb 0xff +0x47=%s  ld+0x48 after sh 0xabcd +0x4c=%s" % (pr(t, "a0"), pr(t, "a1"))
    elif name == "ans_ctl_lb":
        ex = "lb+0x08=%s lh+0x08=%s" % (pr(t, "v0"), pr(t, "a0"))
    elif name == "pre_revbr":
        ex = "pc after lwP=%s v1(RAM trip)=%s" % (pr(t, "pc"), pr(t, "v1"))
    else:
        ex = "v1(RAM trip)=%s" % pr(t, "v1")
    return "declined_notices=%s %s clean=%s" % (decl, ex, clean)


if __name__ == "__main__":
    base, mut, name = sys.argv[1], sys.argv[2], sys.argv[3]
    cmds = S[name](Addr(CODE))
    for lbl, b in (("BASE", base), ("MUTANT", mut)):
        t, clean = session(b, cmds)
        print("DISC %-12s %-6s %s" % (name, lbl, observe(name, t, clean)))
        sys.stdout.flush()
    print("DISC_DONE %s" % name)
