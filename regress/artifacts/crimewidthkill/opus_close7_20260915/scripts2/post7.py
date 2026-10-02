#!/usr/bin/env python3
"""post7.py BIN LABEL -- #529 closing pass 7, Opus FINISHING seat.  A PROTOTYPE of the proposed repair-13 rows and
NOTHING ELSE.  It is not the shipped detector and the shipped detector is not edited by it.

THE CLASS IT IS BUILT FOR.  The #529 fix declines an unsupported width and announces ONCE, latched in
"d->warned & CRIME_W_LEN".  An accept guard grown with that latch as a conjunct --
"else if (len == 4 && !(W && relative_addr == CRIME_INTMASK && (d->warned & CRIME_W_LEN)))" -- routes an ACCEPTED
cell into the width arm, where "if (!(d->warned & CRIME_W_LEN))" is now FALSE, so the cell is declined with NO
announce.  The notice count stays 1 and every notice-counting row stays green.  The shipped 157-row probe measures
every VALUE row in a session that has not refused anything, so the whole latch-SET half of the cross is unrowed:
K1/K2/K3 each scored 157/157 (logs/lane_A.out) while a PRE/POST discriminator showed a guest difference
(logs/disc_K*.out).

Every row here is the SAME check the shipped probe already makes, repeated ONCE with the latch SET -- one refused
lb +0x07 at the head of the session.  Sessions and helpers are copied from regress/crime_width_probe.py.
Sentinel: POST7_DONE (plus POST7_RESULT=n/N).
"""
import os, pty, re, select, signal, sys, time

BIN = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "?"
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
SMALL = 66 * 100000

R = {"zero": 0, "at": 1, "v0": 2, "v1": 3, "a0": 4, "a1": 5, "a2": 6, "a3": 7, "t0": 8, "t1": 9,
     "s0": 16, "s1": 17, "s2": 18, "s3": 19, "ra": 31}
OPC = {"lb": 0x20, "lh": 0x21, "lw": 0x23, "lbu": 0x24, "lhu": 0x25, "ld": 0x37,
       "sb": 0x28, "sh": 0x29, "sw": 0x2b, "sd": 0x3f}
OP_B_SELF = 0x1000ffff
OP_NOP = 0


def enc(op, rs, rt, imm=0):
    return (OPC[op] << 26) | (R[rs] << 21) | (R[rt] << 16) | (imm & 0xffff)


assert enc("lb", "at", "v0") == 0x80220000 and enc("lhu", "at", "v0") == 0x94220000
assert enc("sb", "a3", "t0") == 0xa0e80000 and enc("sh", "a3", "t0") == 0xa4e80000
assert enc("sw", "a3", "t0") == 0xace80000 and enc("lw", "at", "v0") == 0x8c220000

rows = []


def row(name, got, want, note=""):
    rows.append((name, got == want))
    print("%-16s %-22s %-22s %-38s %s" % (name, str(got), str(want), note, "ok" if got == want else "FAIL"))
    sys.stdout.flush()


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


def pr(t, reg):
    m = re.search(r"print\s+%s\s*\n\s*(0x[0-9a-f]+)" % reg, t)
    return ("0x%x" % int(m.group(1), 16)) if m else "absent"


def nth(t, reg, n):
    ms = re.findall(r"print\s+%s\s*\n\s*(0x[0-9a-f]+)" % reg, t)
    return int(ms[n], 16) if len(ms) > n else None


def count(t, s, clean):
    return t.count(s) if clean else "unclean"


def ip2(v):
    return "absent" if v is None else ("set" if v & 0x400 else "clear")


def mag(v):
    return "absent" if v is None else ("small" if v < SMALL else "large")


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


def POST(A):
    """THE ONE STRUCTURAL CHANGE: a refused lb at +0x07 sets d->warned & CRIME_W_LEN before anything else."""
    x, _ = ld(A, "lb", CRIME + 0x07, "v0")
    return x


def roundtrip(A):
    c1, _ = st(A, "sw", SCRATCH_RAM, LIVE_VAL)
    c2, _ = ld(A, "lw", SCRATCH_RAM, "v1")
    return c1 + c2 + ["print v1"]


print("POST7 (repair-13 row prototype) binary=%s label=%s" % (BIN, LABEL))
print("%-16s %-22s %-22s %-38s %s" % ("row", "got", "want", "note", ""))

# ---- P1: the REV PROM-probe window, POST.  CHANNEL: pc = ra, which only an ACCEPTED access reaches ----
A = Addr(CODE)
c = ["ra=0x%x" % RA] + POST(A)
for op in ("sw", "sd", "ld", "lw"):
    if op[0] == "s":
        x, _ = st(A, op, CRIME + 0, 0, at=PROBE_PC)
    else:
        x, _ = ld(A, op, CRIME + 0, "s0", at=PROBE_PC)
    c += x + ["print pc"]
t, clean = session(c)
for i, k in enumerate(("sw", "sd", "ld", "lw")):
    v = nth(t, "pc", i)
    row("p revP %s pc" % k, "absent" if v is None else "0x%x" % v, "0x%x" % RA,
        "POST: accepted %s CRIME_REV from the window -> ra" % k)
row("p revP once", count(t, "-- declined.", clean), 1, "CONTROL: the session refused exactly once (the lb)")

# ---- P2: the twelve-cell value session, POST ----
A = Addr(CODE)
c = POST(A)
x, _ = ld(A, "ld", CRIME + 0x08, "s0"); c += x
x, _ = st(A, "sd", CRIME + 0x20, BIT); c += x
x, _ = ld(A, "ld", CRIME + 0x10, "s1"); c += x
x, _ = st(A, "sw", CRIME + 0x18, 0x10000000); c += x
x, _ = ld(A, "ld", CRIME + 0x18, "s2"); c += x
x, _ = st(A, "sd", CRIME + 0x38, 0x11111111); c += x
x, _ = ld(A, "ld", CRIME + 0x38, "s3"); c += x
x, _ = st(A, "sd", CRIME + 0x40, 0); c += x
x, _ = st(A, "sw", CRIME + 0x40, 0x0a0b0c0d); c += x
x, _ = ld(A, "lw", CRIME + 0x40, "a1"); c += x
x, _ = ld(A, "ld", CRIME + 0x40, "a2"); c += x
x, _ = st(A, "sd", CRIME + 0x08, 0x01); c += x
t, clean = session(c + ["print s0", "print s1", "print s2", "print s3", "print a1", "print a2"])
tv = nth(t, "s3", 0)
row("p acc ctl ld", pr(t, "s0"), "0x100", "POST: accepted ld +0x08 answers CONTROL")
row("p acc istat ld", pr(t, "s1"), "0x%x" % BIT, "POST: accepted ld +0x10 answers INTSTAT")
row("p acc imask sw", pr(t, "s2"), "0x1000000000000000", "POST: accepted sw +0x18 lands high")
row("p acc time sd", "absent" if tv is None else ("odd" if tv & 1 else "even"), "odd",
    "POST: accepted sd +0x38 odd seed stays odd (raw %s)" % tv)
row("p acc 40 lw", pr(t, "a1"), "0xa0b0c0d", "POST: accepted lw +0x40 answers the stored half")
row("p acc 40 sw", pr(t, "a2"), "0xa0b0c0d00000000", "POST: accepted sw +0x40 lands high")
row("p acc ctl sd", count(t, "CRIME_CONTROL: unimplemented", clean), 1, "POST: accepted sd 0x01 +0x08 prints")
row("p acc once", count(t, "-- declined.", clean), 1, "CONTROL: exactly one refusal (the lb)")

# ---- P3: INTSTAT's reassert channel (cause.IP2), POST ----
A = Addr(CODE)
c = POST(A)
x, _ = st(A, "sd", CRIME + 0x18, BIT); c += x
x, _ = st(A, "sd", CRIME + 0x20, BIT); c += x
c += ["print cause"]
x, _ = st(A, "sd", CRIME + 0x10, 0); c += x
c += ["print cause"]
x, _ = st(A, "sd", CRIME + 0x20, 0); c += x
x, _ = st(A, "sd", CRIME + 0x18, BIT); c += x
x, _ = st(A, "sd", CRIME + 0x20, BIT); c += x
c += ["print cause"]
x, _ = st(A, "sw", CRIME + 0x10, 0); c += x
c += ["print cause"]
t, clean = session(c)
row("p istw pre", ip2(nth(t, "cause", 0)), "clear", "CONTROL: IP2 low after SOFTINT default-arm store")
row("p istw sd", ip2(nth(t, "cause", 1)), "set", "POST: accepted sd +0x10 reasserts")
row("p istw mid", ip2(nth(t, "cause", 2)), "clear", "CONTROL: lowered again")
row("p istw sw", ip2(nth(t, "cause", 3)), "set", "POST: accepted sw +0x10 reasserts")

# ---- P4/P5: the TIME 4-byte cells, POST.  CHANNEL: a read's odata is taken BEFORE its own
#      crime_update_crime_time(), so an update skipped at the 4-byte access arrives one access late ----
for op in ("sw", "lw"):
    A = Addr(CODE)
    c = POST(A)
    x, _ = ld(A, "ld", CRIME + 0x38, "s0"); c += x
    if op == "sw":
        x, _ = st(A, "sw", CRIME + 0x38, 0)
    else:
        x, _ = ld(A, "lw", CRIME + 0x38, "a0")
    c += x
    x, _ = ld(A, "ld", CRIME + 0x38, "s1"); c += x
    t, clean = session(c + ["print s0", "print s1"])
    v = nth(t, "s1", 0)
    row("p time 4%s upd" % ("w" if op == "sw" else "r"), mag(v), "large",
        "POST: accepted %s +0x38 advanced TIME (raw %s)" % (op, None if v is None else hex(v)))

# ---- P6: the remaining post-latch ACCEPT cells that carry a value ----
A = Addr(CODE)
c = POST(A)
x, _ = ld(A, "ld", CRIME + 0x00, "s0"); c += x                      # REV 8R from CODE
x, _ = ld(A, "lw", CRIME + 0x04, "s1"); c += x                      # REV 4R low lane (devsig cell)
x, _ = st(A, "sd", CRIME + 0x30, 0x1122334455667788); c += x        # DOG 8W
x, _ = ld(A, "ld", CRIME + 0x30, "s2"); c += x                      # DOG 8R
x, _ = ld(A, "lw", CRIME + 0x30, "a0"); c += x                      # DOG 4R high
x, _ = ld(A, "lw", CRIME + 0x34, "a1"); c += x                      # DOG 4R low
x, _ = st(A, "sw", CRIME + 0x34, 0x0badcafe); c += x                # DOG 4W low
x, _ = ld(A, "ld", CRIME + 0x30, "s3"); c += x
x, _ = st(A, "sd", CRIME + 0x18, BIT); c += x                       # INTMASK 8W
x, _ = ld(A, "ld", CRIME + 0x18, "a2"); c += x                      # INTMASK 8R
x, _ = st(A, "sd", CRIME + 0x278, 0x0102030405060708); c += x       # far block 8W
x, _ = ld(A, "ld", CRIME + 0x278, "t1"); c += x
t, clean = session(c + ["print s0", "print s1", "print s2", "print a0", "print a1", "print s3",
                        "print a2", "print t1"] + roundtrip(A))
row("p rev ld", pr(t, "s0"), "0x11", "POST: accepted ld +0x00 answers CRIME_REV")
row("p rev lw4", pr(t, "s1"), "0x11", "POST: accepted lw +0x04 answers REV low lane")
row("p dog st+ld", pr(t, "s2"), "0x1122334455667788", "POST: 8W then 8R at CRIME_DOG")
row("p dog rhi", pr(t, "a0"), "0x11223344", "POST: 4R of the high half (+0x30)")
row("p dog rlo", pr(t, "a1"), "0x55667788", "POST: 4R of the low half (+0x34)")
row("p dog wlo", pr(t, "s3"), "0x112233440badcafe", "POST: 4W low half lands, high half kept")
row("p imask st+ld", pr(t, "a2"), "0x%x" % BIT, "POST: 8W then 8R at CRIME_INTMASK")
row("p top st+ld", pr(t, "t1"), "0x102030405060708", "POST: 8W then 8R at +0x278")
row("p resid once", count(t, "-- declined.", clean), 1, "CONTROL: exactly one refusal (the lb)")
row("p resid surv", pr(t, "v1"), "0x%x" % LIVE_VAL, "CONTROL: the host survives (a RAM trip)")

npass = sum(1 for _, ok in rows if ok)
print("")
print("FAILING: " + ", ".join(n for n, ok in rows if not ok))
print("POST7_RESULT=%d/%d" % (npass, len(rows)))
print("POST7_DONE")
