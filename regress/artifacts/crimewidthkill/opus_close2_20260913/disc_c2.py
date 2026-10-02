#!/usr/bin/env python3
"""disc_c2.py BASEBIN MUTBIN NAME -- one guest-only discriminating session, run on base AND mutant with the SAME
script, unmodified -E sgi -e ip32 -M 64 (the probe's own apparatus, copied). A survivor is REAL iff the observable
differs base vs mutant."""
import os, pty, re, select, signal, sys, time

DUMMY = "/tmp/dummy_crimep.bin"
CODE = 0x80001000
SCRATCH_RAM = 0xa0001800
LIVE_VAL = 0x12345678
CRIME = 0xb4000000
SENT = 0xdeadbeef
R = {"zero": 0, "at": 1, "v0": 2, "v1": 3, "a0": 4, "a1": 5, "a2": 6, "a3": 7, "t0": 8, "t1": 9,
     "s0": 16, "s1": 17, "s2": 18, "s3": 19, "ra": 31}
OPC = {"lb": 0x20, "lh": 0x21, "lw": 0x23, "lbu": 0x24, "lhu": 0x25, "ld": 0x37,
       "sb": 0x28, "sh": 0x29, "sw": 0x2b, "sd": 0x3f}


def enc(op, rs, rt, imm=0):
    return (OPC[op] << 26) | (R[rs] << 21) | (R[rt] << 16) | (imm & 0xffff)


assert enc("lh", "at", "v0") == 0x84220000 and enc("sd", "a3", "t0") == 0xfce80000


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


def allpr(t, reg):
    return ["0x%x" % int(v, 16) for v in re.findall(r"print\s+%s\s*\n\s*(0x[0-9a-f]+)" % reg, t)]


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


def ld(A, op, addr, rt):
    return ["at=0x%x" % addr, "%s=0x%x" % (rt, SENT)] + run_ops([enc(op, "at", rt)], A.take(1))


def st(A, op, addr, val):
    return ["a3=0x%x" % addr, "t0=0x%x" % val] + run_ops([enc(op, "a3", "t0")], A.take(1))


def roundtrip(A):
    return st(A, "sw", SCRATCH_RAM, LIVE_VAL) + ld(A, "lw", SCRATCH_RAM, "v1") + ["print v1"]


def S_rd_hi_lh(A):
    # seed the far slot +0x278 nonzero with an accepted sd, then a REFUSED 2-byte read at +0x27a over it
    return (st(A, "sd", CRIME + 0x278, 0x0102030405060708) +
            ld(A, "lh", CRIME + 0x27a, "v0") + ld(A, "lhu", CRIME + 0x27c, "a0") +
            ["print v0", "print a0"])


def S_rd_hi_lb(A):
    # the far-block 1-byte read channel: refused lb over a nonzero slot (this is o_rd_hi, caught by top rd v0)
    return (st(A, "sd", CRIME + 0x278, 0x0102030405060708) +
            ld(A, "lb", CRIME + 0x27b, "v0") + ["print v0"])


def S_rd_lh_all(A):
    # a refused lh at a NAMED label (INTSTAT +0x10) over a nonzero register -- caught by istat lh v0
    return (st(A, "sd", CRIME + 0x20, 0x10000000) + ld(A, "lh", CRIME + 0x10, "v0") + ["print v0"])


def S_soft_gate(A):
    # SOFTINT set, refused sh 0x0800 at CONTROL -> decline should hold (CPUs run); mutant declines only when SOFTINT set
    # so with SOFTINT==0 (as in sh08 run) it would fall through. Here we show the CONTROL cell in the SOFTINT==0 state.
    return (st(A, "sh", CRIME + 0x08, 0x0800) + roundtrip(A))


def S_istat_leak(A):
    # (1) SOFTINT = 0xff -> INTSTAT's low byte is 0xff; refused lb +0x10 -> v0.
    # (2) SOFTINT = BIT (0x10000000), the probe's own value; refused lb/lh +0x10 -> a0/a1: the oracle's blindness
    return (st(A, "sd", CRIME + 0x20, 0xff) + ld(A, "lb", CRIME + 0x10, "v0") +
            st(A, "sd", CRIME + 0x20, 0x10000000) + ld(A, "lb", CRIME + 0x10, "a0") + ld(A, "lh", CRIME + 0x10, "a1") +
            ["print v0", "print a0", "print a1"])


def S_dog_leak(A):
    return (st(A, "sd", CRIME + 0x30, 0x0123456789abcdef) + ld(A, "lb", CRIME + 0x30, "v0") +
            ld(A, "lh", CRIME + 0x30, "a0") + ["print v0", "print a0"])


def S_istat_lane(A):
    return (st(A, "sd", CRIME + 0x20, 0xff00000000000000) + ld(A, "lb", CRIME + 0x10, "v0") +
            ld(A, "lh", CRIME + 0x10, "a0") + ["print v0", "print a0"])


def observe(name, t, clean):
    decl = t.count("-- declined.") if clean else "unclean"
    ctl = t.count("CRIME_CONTROL: unimplemented") if clean else "unclean"
    extra = {"rd_hi_lh": "v0(lh+0x27a)=%s a0(lhu+0x27c)=%s" % (pr(t, "v0"), pr(t, "a0")),
             "rd_hi_lb": "v0(lb+0x27b)=%s" % pr(t, "v0"),
             "rd_lh_all": "v0(lh+0x10)=%s" % pr(t, "v0"),
             "soft_gate": "v1(RAMtrip)=%s" % pr(t, "v1"),
             "istat_leak": "v0(lb+0x10,SOFTINT=0xff)=%s a0(lb,SOFTINT=BIT)=%s a1(lh,SOFTINT=BIT)=%s"
                           % (pr(t, "v0"), pr(t, "a0"), pr(t, "a1")),
             "dog_leak": "v0(lb+0x30)=%s a0(lh+0x30)=%s" % (pr(t, "v0"), pr(t, "a0")),
             "istat_lane": "v0(lb+0x10)=%s a0(lh+0x10)=%s" % (pr(t, "v0"), pr(t, "a0"))}.get(name, "")
    return "declined_notices=%s control_text=%s %s clean=%s" % (decl, ctl, extra, clean)


base, mut, name = sys.argv[1], sys.argv[2], sys.argv[3]
cmds = globals()["S_" + name](Addr(CODE))
for lbl, b in (("BASE", base), ("MUTANT", mut)):
    t, clean = session(b, cmds)
    print("DISC %-10s %-6s %s" % (name, lbl, observe(name, t, clean)))
    sys.stdout.flush()
print("DISC_DONE %s" % name)
