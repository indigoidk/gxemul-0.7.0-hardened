#!/usr/bin/env python3
"""disc_c4.py BASEBIN MUTBIN NAME -- one guest-only discriminating session per claim, run on base AND mutant with the
SAME script, unmodified -E sgi -e ip32 -M 64 (the probe's own apparatus).  DIFFERS => the survivor is NON-EQUIVALENT
(a guest-visible behaviour change no 131-row row sees).  Sentinel DISC_C4_DONE."""
import os, pty, re, select, signal, sys, time

DUMMY = "/tmp/dummy_crimep.bin"
if not os.path.exists(DUMMY):
    open(DUMMY, "wb").write(b"\0" * 16)
CODE = 0x80001000
SCRATCH_RAM = 0xa0001800
LIVE_VAL = 0x12345678
CRIME = 0xb4000000
MACE = 0xbf310000
SENT = 0xdeadbeef
RA = 0x80004000
PROBE_PC = 0xbfc05180
R = {"zero": 0, "at": 1, "v0": 2, "v1": 3, "a0": 4, "a1": 5, "a2": 6, "a3": 7, "t0": 8, "t1": 9,
     "s0": 16, "s1": 17, "s2": 18, "s3": 19, "ra": 31}
OPC = {"lb": 0x20, "lh": 0x21, "lw": 0x23, "lbu": 0x24, "lhu": 0x25, "ld": 0x37,
       "sb": 0x28, "sh": 0x29, "sw": 0x2b, "sd": 0x3f}
OP_B_SELF = 0x1000ffff


def enc(op, rs, rt, imm=0):
    return (OPC[op] << 26) | (R[rs] << 21) | (R[rt] << 16) | (imm & 0xffff)


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
            if c == "<RUN>":
                os.write(fd, b"continue\n"); ok = rd(2.0)
                os.write(fd, b"\x03"); ok = ok and rd(1.5)
            else:
                os.write(fd, (c + "\n").encode("latin-1"))
                ok = rd(spin if i == len(cmds) - 1 else 0.25)
        except OSError:
            break
        if not ok:
            break
    eof = True
    try:
        os.write(fd, b"quit\n"); eof = not rd(10.0)
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
    put += ["put w 0x%x, 0x%08x" % (at + 4 * len(ops), OP_B_SELF),
            "put w 0x%x, 0x%08x" % (at + 4 * len(ops) + 4, 0)]
    return put + ["pc=0x%x" % at, "step %d" % len(ops)]


def ld(A, op, addr, rt, at=None):
    here = A.take(1) if at is None else at
    return ["at=0x%x" % addr, "%s=0x%x" % (rt, SENT)] + run_ops([enc(op, "at", rt)], here)


def st(A, op, addr, val, at=None):
    here = A.take(1) if at is None else at
    return ["a3=0x%x" % addr, "t0=0x%x" % val] + run_ops([enc(op, "a3", "t0")], here)


def count(t, s, clean):
    return t.count(s) if clean else "unclean"


# each returns (label -> value) dict describing the discriminating observable
def d_c1_deepseek(BIN):
    # dead-code check: accepted sw 0x0200 at CONTROL, then refused lb +0x07; count announces.  If the pre-set fired the
    # announce would be silenced (0 announces).  Expect base==mut==1 (condition unreachable -> equivalent).
    A = Addr(CODE); c = []
    c += st(A, "sw", CRIME + 0x08, 0x0200)
    c += ld(A, "lb", CRIME + 0x07, "v0")
    t, clean = session(BIN, c + ["print v0"])
    return {"announces": count(t, "-- declined.", clean)}


def d_c2_kimik3(BIN):
    # latch HARDINT via two MACE stores, then a refused lh at CONTROL; a declined read answering HARDINT shows nonzero.
    A = Addr(CODE); c = []
    for off, val in ((0x10, 0x01), (0x18, 0x01)):
        c += st(A, "sd", MACE + off, val)
    c += ld(A, "ld", CRIME + 0x28, "s2")     # HARDINT raw
    c += ld(A, "lh", CRIME + 0x08, "a0")     # refused lh at CONTROL: answer
    c += ld(A, "lb", CRIME + 0x08, "a1")     # refused lb at CONTROL: answer
    t, clean = session(BIN, c + ["print s2", "print a0", "print a1"])
    return {"hardint": pr(t, "s2"), "lh_ans": pr(t, "a0"), "lb_ans": pr(t, "a1")}


def d_c3_codex_dbg(BIN):
    # FREE-RUN a refused lb at +0x0f (bit 3 set): fatal() prints while free-running, debug() does not.
    A = Addr(CODE)
    here = A.take(2)
    c = ["at=0x%x" % (CRIME + 0x0f), "v0=0x%x" % SENT,
         "put w 0x%x, 0x%08x" % (here, enc("lb", "at", "v0")),
         "put w 0x%x, 0x%08x" % (here + 4, 0),
         "put w 0x%x, 0x%08x" % (here + 8, OP_B_SELF),
         "put w 0x%x, 0x%08x" % (here + 12, 0),
         "pc=0x%x" % here, "<RUN>", "print v0"]
    t, clean = session(BIN, c)
    ran = t.split("continue", 1)[1] if "continue" in t else ""
    return {"free_announce_bit3set": ran.count("unimplemented len=1 at 0xf -- declined.")}


def d_c4_kimicli(BIN):
    # refused lb +0x07, accepted sd write at INTMASK +0x18, refused lb +0x07; count announces.  A re-arm on the
    # accepted write resets the latch -> two announces on the mutant.
    A = Addr(CODE); c = ["ra=0x%x" % RA]
    c += ld(A, "lb", CRIME + 0x07, "v0")
    c += st(A, "sd", CRIME + 0x18, 0x0101010101010101)   # accepted 8-byte WRITE at INTMASK
    c += ld(A, "lb", CRIME + 0x07, "v1")
    t, clean = session(BIN, c + ["print v0", "print v1"])
    return {"announces": count(t, "-- declined.", clean)}


def d_c5_codex_b1(BIN):
    # seed INTMASK (reg[3] = +0x18) to 0 via accepted sd; refused sh 0xffff at +0x1e (bit 1 set) LANDS at reg[3];
    # read back +0x18 with an accepted ld.  base: 0.  mutant: 0xffff.
    A = Addr(CODE); c = []
    c += st(A, "sd", CRIME + 0x18, 0x0)          # INTMASK = 0
    c += st(A, "sh", CRIME + 0x1e, 0xffff)       # refused 2-byte store, bit 1 set (0x1e & 2 = 2)
    c += ld(A, "ld", CRIME + 0x18, "a0")         # accepted read back of reg[3]=INTMASK
    t, clean = session(BIN, c + ["print a0"])
    return {"intmask_after": pr(t, "a0")}


def _between(BIN, mid):
    # refused lb +0x07, <mid accepted access>, refused lb +0x07; count announces (a re-arm shows as 2)
    A = Addr(CODE); c = ["ra=0x%x" % RA]
    c += ld(A, "lb", CRIME + 0x07, "v0")
    c += mid(A)
    c += ld(A, "lb", CRIME + 0x07, "v1")
    t, clean = session(BIN, c + ["print v0", "print v1"])
    return {"announces": count(t, "-- declined.", clean)}


def _first(BIN, pre):
    # <pre accepted access>, refused lb +0x07; count announces (a pre-set shows as 0)
    A = Addr(CODE); c = ["ra=0x%x" % RA]
    c += pre(A)
    c += ld(A, "lb", CRIME + 0x07, "v0")
    t, clean = session(BIN, c + ["print v0"])
    return {"announces": count(t, "-- declined.", clean)}


def d_d1(BIN):
    return _between(BIN, lambda A: st(A, "sw", CRIME + 0x08, 0x0200))


def d_d2(BIN):
    return _first(BIN, lambda A: st(A, "sw", CRIME + 0x08, 0x0200))


def d_d3(BIN):
    return _between(BIN, lambda A: st(A, "sd", CRIME + 0x38, 0x11111111))


def d_d4(BIN):
    return _first(BIN, lambda A: st(A, "sd", CRIME + 0x10, 0))


def d_d6(BIN):
    # FREE-RUN a refused lh at +0x06 (a 2-byte refusal): fatal prints free-running, debug does not
    A = Addr(CODE)
    here = A.take(2)
    c = ["at=0x%x" % (CRIME + 0x06), "v0=0x%x" % SENT,
         "put w 0x%x, 0x%08x" % (here, enc("lh", "at", "v0")),
         "put w 0x%x, 0x%08x" % (here + 4, 0),
         "put w 0x%x, 0x%08x" % (here + 8, OP_B_SELF),
         "put w 0x%x, 0x%08x" % (here + 12, 0),
         "pc=0x%x" % here, "<RUN>", "print v0"]
    t, clean = session(BIN, c)
    ran = t.split("continue", 1)[1] if "continue" in t else ""
    return {"free_announce_len2": ran.count("unimplemented len=2 at 0x6 -- declined.")}


def d_d7(BIN):
    return _between(BIN, lambda A: st(A, "sw", CRIME + 0x00, 0))


DISC = {"d1_rearm_dog0200": d_d1, "d2_pre_dog0200": d_d2, "d3_rearm_wtime": d_d3, "d4_pre_wistat": d_d4,
        "d6_chan_len2": d_d6, "d7_rearm_wrev": d_d7,
        "c1_deepseek": d_c1_deepseek, "c2_kimik3": d_c2_kimik3, "c3_codex_dbg": d_c3_codex_dbg,
        "c4_kimicli": d_c4_kimicli, "c5_codex_b1": d_c5_codex_b1}

if __name__ == "__main__":
    base, mut, name = sys.argv[1], sys.argv[2], sys.argv[3]
    fn = DISC[name]
    b = fn(base)
    m = fn(mut)
    differs = any(b[k] != m[k] for k in b)
    print("DISC %s  base=%s  mut=%s  => %s" % (name, b, m, "DIFFERS (NON-EQUIVALENT)" if differs else "SAME (equivalent on this probe)"))
    print("DISC_C4_DONE")
