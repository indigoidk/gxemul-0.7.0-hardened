#!/usr/bin/env python3
"""disc7.py BIN LABEL [NFREE] -- #529 closing pass 7, Opus seat: guest-visible DISCRIMINATOR sessions (not part of the
shipped probe).  The pty/session machinery is copied from regress/crime_width_probe.py (same flags, same machine).
Sentinel: DISC7_DONE.  (disc7b: +0x04 read-back register fixed, TIME tests as a tight loop.)"""
import os, pty, re, select, signal, sys, time

BIN = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "?"
NFREE = int(sys.argv[3]) if len(sys.argv) > 3 else 1
DUMMY = "/tmp/dummy_crimep.bin"
if not os.path.exists(DUMMY):
    with open(DUMMY, "wb") as f:
        f.write(b"\0" * 16)

CODE = 0x80001000
CRIME = 0xb4000000
SENT = 0xdeadbeef
RA = 0x80004000
PROBE_PC = 0xbfc05180
R = {"zero": 0, "at": 1, "v0": 2, "v1": 3, "a0": 4, "a1": 5, "a2": 6, "a3": 7, "t0": 8, "t1": 9,
     "s0": 16, "s1": 17, "s2": 18, "s3": 19, "ra": 31}
OPC = {"lb": 0x20, "lh": 0x21, "lw": 0x23, "lbu": 0x24, "lhu": 0x25, "ld": 0x37,
       "sb": 0x28, "sh": 0x29, "sw": 0x2b, "sd": 0x3f}
OP_B_SELF = 0x1000ffff
OP_NOP = 0


def enc(op, rs, rt, imm=0):
    return (OPC[op] << 26) | (R[rs] << 21) | (R[rt] << 16) | (imm & 0xffff)


assert enc("lb", "at", "v0") == 0x80220000 and enc("sw", "a3", "t0") == 0xace80000 and enc("lw", "at", "v0") == 0x8c220000


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
            if c == "<RUN>":
                os.write(fd, b"continue\n")
                ok = rd(2.0)
                os.write(fd, b"\x03")
                ok = ok and rd(1.5)
            else:
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


def nth(t, reg, n):
    ms = re.findall(r"print\s+%s\s*\n\s*(0x[0-9a-f]+)" % reg, t)
    return ("0x%x" % int(ms[n], 16)) if len(ms) > n else "absent"


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
    return ["at=0x%x" % addr, "%s=0x%x" % (rt, SENT)] + run_ops([enc(op, "at", rt)], here)


def st(A, op, addr, val, at=None):
    here = A.take(1) if at is None else at
    return ["a3=0x%x" % addr, "t0=0x%x" % val] + run_ops([enc(op, "a3", "t0")], here)


def out(name, got, note=""):
    print("%-22s %-22s %s" % (name, got, note))
    sys.stdout.flush()


print("DISC7 binary=%s label=%s" % (BIN, LABEL))

# ---- K1/K2/K3: the same three accepted accesses, PRE (no refusal first) and POST (after one refused lb +0x07) ----
for phase in ("PRE", "POST"):
    A = Addr(CODE)
    c = ["ra=0x%x" % RA]
    if phase == "POST":
        c += ld(A, "lb", CRIME + 0x07, "v1")
    c += st(A, "sw", CRIME + 0x18, 0x10000000)
    c += ld(A, "ld", CRIME + 0x18, "s2")
    c += ld(A, "ld", CRIME + 0x08, "s0")
    c += ld(A, "lw", CRIME + 0x00, "s1", at=PROBE_PC) + ["print pc"]
    t, clean = session(c + ["print s2", "print s0", "print s1"])
    out("%s imask sw->ld" % phase, nth(t, "s2", 0), "want 0x1000000000000000 (K1 POST: 0x0)")
    out("%s ctl ld" % phase, nth(t, "s0", 0), "want 0x100 (K3 POST: 0x0)")
    out("%s revP lw pc" % phase, nth(t, "pc", 0), "want 0x%x (K2 POST: 0x%x)" % (RA, PROBE_PC + 4))
    out("%s notices" % phase, t.count("-- declined.") if clean else "unclean",
        "POST: 1 (the lb's own); a K mutant stays 1 -- silent")
    out("%s lb said" % phase, t.count("unimplemented len=1 at 0x7 -- declined.  (once) ]") if clean else "unclean", "")

# ---- EQV: REV / CONTROL / +0x04 accesses outside the window, values and the default-arm text ----
A = Addr(CODE)
c = []
c += st(A, "sw", CRIME + 0x00, 0x12345678)      # REV 4W (hi lane) out of window
c += ld(A, "lw", CRIME + 0x00, "a0")             # REV 4R hi
c += ld(A, "ld", CRIME + 0x00, "a1")             # REV 8R (not bypassed by E3)
c += st(A, "sd", CRIME + 0x00, 0x1122334455667788)   # REV 8W out of window
c += ld(A, "ld", CRIME + 0x00, "a2")
c += st(A, "sw", CRIME + 0x04, 0x0abcdef0)       # default 4W at +0x04 (REV low lane)
c += ld(A, "lw", CRIME + 0x04, "t1")
c += ld(A, "lw", CRIME + 0x08, "s0")             # CONTROL 4R hi
c += ld(A, "ld", CRIME + 0x08, "s1")
c += st(A, "sw", CRIME + 0x38, 0x0a0b0c0d)       # TIME 4W hi (stepped: the arm's update truncates)
c += ld(A, "lw", CRIME + 0x38, "s2")             # TIME 4R hi
t, clean = session(c + ["print a0", "print a1", "print a2", "print t1", "print s0", "print s1", "print s2"])
for r, n in (("a0", "EQV rev lw"), ("a1", "EQV rev ld"), ("a2", "EQV rev sd->ld"), ("t1", "EQV +4 sw->lw"),
             ("s0", "EQV ctl lw"), ("s1", "EQV ctl ld"), ("s2", "EQV time sw->lw(step)")):
    out(n, nth(t, r, 0))
out("EQV dflt write 0x4", t.count("[ crime: write to 0x4:") if clean else "unclean", "default-arm debug text (stepped)")
out("EQV dflt read 0x4", t.count("[ crime: read from 0x4,") if clean else "unclean", "")

# ---- CONTROL writes with DOG set + a leftover bit (the F1/F1b cells): the arm's text, host log only ----
A = Addr(CODE)
c = st(A, "sd", CRIME + 0x08, 0x0201) + st(A, "sw", CRIME + 0x08, 0x0201) + ld(A, "ld", CRIME + 0x08, "s3")
t, clean = session(c + ["print s3"])
out("CTL 0x0201 text", t.count("CRIME_CONTROL: unimplemented") if clean else "unclean", "sd + sw 0x0201: base 2")
out("CTL after ld", nth(t, "s3", 0), "CONTROL after both writes (prelude: 0x100)")

# ---- TIME same-microsecond, FREE-RUNNING: three consecutive CRIME accesses at +0x38 ----
def loop3(ops, regs):
    A = Addr(CODE)
    here = A.take(len(ops) + 2)
    c = ["at=0x%x" % (CRIME + 0x38)] + regs
    for i, op in enumerate(ops):
        c.append("put w 0x%x, 0x%08x" % (here + 4 * i, op))
    back = (-(len(ops) + 1)) & 0xffff               # b here (from here + 4*len(ops); delay slot after it)
    c += ["put w 0x%x, 0x%08x" % (here + 4 * len(ops), 0x10000000 | back),
          "put w 0x%x, 0x%08x" % (here + 4 * len(ops) + 4, OP_NOP),
          "pc=0x%x" % here, "<RUN>", "print v0", "print v1"]
    return session(c)


SD = (OPC["sd"] << 26) | (R["at"] << 21) | (R["t0"] << 16)
for k in range(NFREE):
    t, clean = loop3([enc("ld", "at", "v1"), enc("sw", "at", "t0"), enc("ld", "at", "v0")],
                     ["t0=0x0a0b0c0d", "v0=0x%x" % SENT, "v1=0x%x" % SENT])
    v0 = nth(t, "v0", 0)
    hi = ("0x%x" % (int(v0, 16) >> 32)) if v0 != "absent" else "absent"
    out("T4W loop%d v0" % k, v0, "HIGH half %s (base, same-us window: 0xa0b0c0d; E2: 0x0) clean=%s" % (hi, clean))
for k in range(NFREE):
    t, clean = loop3([enc("ld", "at", "v1"), SD, enc("lw", "at", "v0")],
                     ["t0=0x0a0b0c0d11111111", "v0=0x%x" % SENT, "v1=0x%x" % SENT])
    out("T4R loop%d v0" % k, nth(t, "v0", 0), "lw hi after sd (base, same-us window: 0xa0b0c0d; E2: 0x0) clean=%s" % clean)

# ---- the SKIPPED UPDATE (codex's "U"), first pass, no loop: a read returns odata computed BEFORE its own update, so
#      an update skipped at a 4-byte TIME access arrives one access LATE.  P4W = ld; sw; ld  (disc7's T4W, again) and
#      P4R = ld; lw; ld at +0x38.  base: v0 = 66 x (us between the first ld and the 4-byte access); E2: 0 (see disc7 T4W)
def once3(ops, regs):
    A = Addr(CODE)
    here = A.take(len(ops) + 2)
    c = ["at=0x%x" % (CRIME + 0x38)] + regs
    for i, op in enumerate(ops):
        c.append("put w 0x%x, 0x%08x" % (here + 4 * i, op))
    c += ["put w 0x%x, 0x%08x" % (here + 4 * len(ops), OP_B_SELF),
          "put w 0x%x, 0x%08x" % (here + 4 * len(ops) + 4, OP_NOP),
          "pc=0x%x" % here, "<RUN>", "print v0", "print v1"]
    return session(c)


for k in range(NFREE):
    t, clean = once3([enc("ld", "at", "v1"), enc("sw", "at", "t0"), enc("ld", "at", "v0")],
                     ["t0=0x0a0b0c0d", "v0=0x%x" % SENT, "v1=0x%x" % SENT])
    out("P4W run%d v0" % k, nth(t, "v0", 0), "ld;sw;ld first pass (v1 %s) clean=%s" % (nth(t, "v1", 0), clean))
for k in range(NFREE):
    t, clean = once3([enc("ld", "at", "v1"), enc("lw", "at", "a0"), enc("ld", "at", "v0")],
                     ["v0=0x%x" % SENT, "v1=0x%x" % SENT, "a0=0x%x" % SENT])
    out("P4R run%d v0" % k, nth(t, "v0", 0), "ld;lw;ld first pass (v1 %s) clean=%s" % (nth(t, "v1", 0), clean))

# ---- a STEPPED candidate row for the TIME 4-byte cells (the shipped `time <op>' shape with the refused access replaced
#      by an ACCEPTED sw / lw at +0x38): the arm's update adds 66 x the debugger interval, so the NEXT ld reads LARGE;
#      a silent bypass (E2) skips it and the ld reads the first tick's SMALL value
for op in ("sw", "lw"):
    A = Addr(CODE)
    c = ld(A, "ld", CRIME + 0x38, "s0")
    c += st(A, "sw", CRIME + 0x38, 0) if op == "sw" else ld(A, "lw", CRIME + 0x38, "a0")
    c += ld(A, "ld", CRIME + 0x38, "s1")
    t, clean = session(c + ["print s0", "print s1"])
    v = nth(t, "s1", 0)
    mg = "absent" if v == "absent" else ("small" if int(v, 16) < 66 * 100000 else "large")
    out("STEP time %s acc" % op, mg, "s1 %s after an accepted %s +0x38 (base: large; E2: small)" % (v, op))

print("DISC7_DONE")
