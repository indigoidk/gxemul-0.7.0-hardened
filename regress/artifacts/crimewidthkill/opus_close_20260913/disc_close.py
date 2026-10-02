#!/usr/bin/env python3
"""disc_close.py BASEBIN MUTBIN NAME -- #529 closing pass (Opus seat): one guest-only discriminating session per survivor,
run on the baseline and on the mutant with the SAME script.  Real MIPS guest instructions, one `step' at a time, on
unmodified -E sgi -e ip32 -M 64 (the probe's own apparatus, copied).  A survivor is REAL iff the observable differs."""
import os, pty, re, select, signal, sys, time

DUMMY = "/tmp/dummy_crimep.bin"
CODE = 0x80001000
SCRATCH_RAM = 0xa0001800
LIVE_VAL = 0x12345678
CRIME = 0xb4000000
MACE = 0xbf310000
SENT = 0xdeadbeef
R = {"zero": 0, "at": 1, "v0": 2, "v1": 3, "a0": 4, "a1": 5, "a2": 6, "a3": 7, "t0": 8, "t1": 9,
     "s0": 16, "s1": 17, "s2": 18, "s3": 19, "ra": 31}
OPC = {"lb": 0x20, "lh": 0x21, "lw": 0x23, "lbu": 0x24, "lhu": 0x25, "ld": 0x37,
       "sb": 0x28, "sh": 0x29, "sw": 0x2b, "sd": 0x3f}


def enc(op, rs, rt, imm=0):
    return (OPC[op] << 26) | (R[rs] << 21) | (R[rt] << 16) | (imm & 0xffff)


assert enc("lb", "at", "v0") == 0x80220000 and enc("sh", "a3", "t0") == 0xa4e80000


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


def S_rearm4(A):     # refused, accepted 32-bit read, refused -- announce count
    return ld(A, "lb", CRIME + 7, "v0") + ld(A, "lw", CRIME + 0x30, "a0") + ld(A, "lb", CRIME + 7, "v0")


def S_pre4(A):       # accepted 32-bit read FIRST, then a refusal -- announce count
    return ld(A, "lw", CRIME + 0x30, "a0") + ld(A, "lb", CRIME + 7, "v0")


def S_rearm_time(A):  # refused, accepted TIME read, refused
    return ld(A, "lb", CRIME + 7, "v0") + ld(A, "ld", CRIME + 0x38, "a0") + ld(A, "lb", CRIME + 7, "v0")


def S_ctl_collide(A):  # an accepted CONTROL write carrying an unimplemented bit, then a refusal
    return st(A, "sw", CRIME + 0x08, 0x01) + ld(A, "lb", CRIME + 7, "v0")


def S_wst_mc2(A):    # refused 2-byte store at the far block, read back by an accepted ld
    return st(A, "sh", CRIME + 0x27e, 0xbeef) + ld(A, "ld", CRIME + 0x278, "a0") + ["print a0"]


def S_rd_hi(A):      # refused 1-byte read of bank-1 control's low byte (+0x217)
    return ld(A, "lbu", CRIME + 0x217, "v0") + ["print v0"]


def S_lt_blk(A):     # a refusal below 0x200, then one at the far block
    return ld(A, "lb", CRIME + 7, "v0") + st(A, "sb", CRIME + 0x27f, 0xff)


def S_wnz_lbl(A):    # the imask setup, then a refused NONZERO sb at INTMASK
    return (st(A, "sd", CRIME + 0x18, 0x10000000) + st(A, "sd", CRIME + 0x20, 0x10000000) + ["print cause"] +
            st(A, "sb", CRIME + 0x18, 0x01) + ["print cause"])


def S_acc4_210(A):   # 32-bit read at the anchored row's own address
    return ld(A, "lw", CRIME + 0x210, "a0") + ["print a0"]


def S_pa_gate(A):    # CRIME line ASSERTED (SOFTINT & INTMASK, reasserted by an accepted lw), then refused sh 0x0800 +0x08
    return (st(A, "sd", CRIME + 0x18, 0x10000000) + st(A, "sd", CRIME + 0x20, 0x10000000) +
            ld(A, "lw", CRIME + 0x18, "a0") + ["print cause"] + st(A, "sh", CRIME + 0x08, 0x0800) + roundtrip(A))


def S_hi_gate(A):    # HARDINT made nonzero by the GUEST through MACE (status, then mask -> reassert -> CRIME_INT_PERIPH_MISC),
    #                  read back, then refused sh 0x0800 +0x08
    return (st(A, "sd", MACE + 0x10, 0x01) + st(A, "sd", MACE + 0x18, 0x01) + ld(A, "ld", CRIME + 0x28, "s2") +
            ["print s2"] + st(A, "sh", CRIME + 0x08, 0x0800) + roundtrip(A))


def observe(name, t, clean):
    decl = t.count("-- declined.") if clean else "unclean"
    ctl = t.count("CRIME_CONTROL: unimplemented") if clean else "unclean"
    extra = {"wst_mc2": "a0=%s" % pr(t, "a0"), "rd_hi": "v0=%s" % pr(t, "v0"),
             "wnz_lbl": "cause=%s" % allpr(t, "cause"), "acc4_210": "a0=%s" % pr(t, "a0"),
             "pa_gate": "cause=%s v1=%s" % (allpr(t, "cause"), pr(t, "v1")),
             "hi_gate": "HARDINT=%s v1=%s" % (pr(t, "s2"), pr(t, "v1"))}.get(name, "")
    return "declined_notices=%s control_text=%s %s clean=%s" % (decl, ctl, extra, clean)


base, mut, name = sys.argv[1], sys.argv[2], sys.argv[3]
cmds = globals()["S_" + name](Addr(CODE))
for lbl, b in (("BASE", base), ("MUTANT", mut)):
    t, clean = session(b, cmds)
    print("DISC %-12s %-6s %s" % (name, lbl, observe(name, t, clean)))
    sys.stdout.flush()
print("DISC_DONE %s" % name)
