#!/usr/bin/env python3
"""crime_p2_escape.py BIN [LABEL] -- #529 pass-2 Opus seat: OBSERVABLES for the refusal cells kill table 1 did not row.

Same apparatus as regress/crime_width_probe.py (cold debugger, unmodified -E sgi -e ip32 -M 64, one `step' at a time).
Each channel carries a CONTROL on an accepted width showing it can vary.

  E1 INTMASK reassert: sd INTMASK=bit28, sd SOFTINT=bit28 (default arm: stored, NO reassert, so the CPU line stays low),
     then one access AT the INTMASK label.  crime_interrupt_reassert() raises cause.IP2 (0x400) at once, synchronously.
        ctl : lw  +0x18 (accepted, switch INTMASK arm)       -> IP2 set
        test: lb  +0x18 / sb +0x18 (refused)                 -> fix: IP2 clear ; fall-through at INTMASK: IP2 set
  E2 INTSTAT: same, access at +0x10.
  E3 TIME: ld +0x38 (first update only latches last_us, value stays 0); a refused lb +0x38; ld +0x38 -> s1; ld -> s2.
     An accepted ld returns odata read BEFORE the switch's update, so s1 == the value left by the previous update:
        fix: s1 == 0 (nothing updated since) ; fall-through at TIME: s1 != 0 ; ctl: s2 != 0 (the channel moves)
  E4 REV WRITE from pc 0xbfc05180: the CRIME_REV arm does not test writeflag.
        ctl : sw +0 from 0xbfc05180 -> pc = ra ; test: sh +0 -> fix: pc advances ; fall-through at REV: pc = ra
  E5 MEMORY CONTROL (0x200+), accept cells at an address the detector never uses: bank 1 ctrl = 1 for -M 64.
        lw +0x214 (4R low half), ld +0x210 (8R)  -> 0x1 ; an accept arm narrowed by address -> 0x0 (declined)

Sentinel: P2ESC_DONE
"""
import os, pty, re, select, sys, time

BIN = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "?"
DUMMY = "/tmp/dummy_crimep.bin"
if not os.path.exists(DUMMY):
    with open(DUMMY, "wb") as f:
        f.write(b"\0" * 16)

CODE = 0x80001000
CRIME = 0xb4000000
SENT = 0xdeadbeef
RA = 0x80004000
PROBE_PC = 0xbfc05180
BIT = 0x10000000

R = {"zero": 0, "at": 1, "v0": 2, "v1": 3, "a0": 4, "a1": 5, "a2": 6, "a3": 7, "t0": 8, "t1": 9,
     "s0": 16, "s1": 17, "s2": 18, "s3": 19, "ra": 31}
OPC = {"lb": 0x20, "lh": 0x21, "lw": 0x23, "lbu": 0x24, "lhu": 0x25, "ld": 0x37,
       "sb": 0x28, "sh": 0x29, "sw": 0x2b, "sd": 0x3f}
OP_B_SELF = 0x1000ffff


def enc(op, rs, rt, imm=0):
    return (OPC[op] << 26) | (R[rs] << 21) | (R[rt] << 16) | (imm & 0xffff)


assert enc("lb", "at", "v0") == 0x80220000 and enc("sw", "a3", "t0") == 0xace80000

rows = []


def row(name, got, want, note=""):
    ok = (got == want)
    rows.append((name, ok))
    print("%-16s %-20s %-20s %-46s %s" % (name, str(got), str(want), note, "ok" if ok else "DIFF"))
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
        except OSError:
            break
        if not rd(spin if i == len(cmds) - 1 else 0.25):
            break
    try:
        os.write(fd, b"quit\n")
        rd(10.0)
    except OSError:
        pass
    try:
        os.close(fd)
    except OSError:
        pass
    try:
        os.waitpid(pid, 0)
    except OSError:
        pass
    return buf.replace("\r", "")


def prn(t, reg, nth=0):
    ms = re.findall(r"print\s+%s\s*\n\s*(0x[0-9a-f]+)" % reg, t)
    return int(ms[nth], 16) if len(ms) > nth else None


class Addr(object):
    def __init__(self, base):
        self.a = base

    def take(self, n):
        got = self.a
        self.a += 4 * (n + 2) + 0x20
        return got


def run_ops(ops, at):
    put = ["put w 0x%x, 0x%08x" % (at + 4 * i, op) for i, op in enumerate(ops)]
    put += ["put w 0x%x, 0x%08x" % (at + 4 * len(ops), OP_B_SELF), "put w 0x%x, 0x%08x" % (at + 4 * len(ops) + 4, 0)]
    return put + ["pc=0x%x" % at, "step %d" % len(ops)]


def ld(A, op, addr, rt, at=None):
    here = A.take(1) if at is None else at
    return ["at=0x%x" % addr, "%s=0x%x" % (rt, SENT)] + run_ops([enc(op, "at", rt)], here)


def st(A, op, addr, val, at=None):
    here = A.take(1) if at is None else at
    return ["a3=0x%x" % addr, "t0=0x%x" % val] + run_ops([enc(op, "a3", "t0")], here)


def ip2(c):
    return "absent" if c is None else ("set" if c & 0x400 else "clear")


print("CRIME P2 ESCAPE PROBE (#529 pass 2, Opus seat)   binary=%s  label=%s" % (BIN, LABEL))

# ---- E1/E2: reassert at the INTMASK / INTSTAT labels ----
for lbl, off in (("imask", 0x18), ("istat", 0x10)):
    for kind in ("ctl lw", "lb", "sb"):
        A = Addr(CODE)
        c = []
        c += st(A, "sd", CRIME + 0x18, BIT)       # INTMASK = bit (switch INTMASK arm: reassert, status 0)
        c += st(A, "sd", CRIME + 0x20, BIT)       # SOFTINT = bit (default arm: NO reassert)
        c += ["print cause"]
        if kind == "ctl lw":
            c += ld(A, "lw", CRIME + off, "v0")
        elif kind == "lb":
            c += ld(A, "lb", CRIME + off, "v0")
        else:
            c += st(A, "sb", CRIME + off, 0)
        c += ["print cause"]
        t = session(c)
        before, after = prn(t, "cause", 0), prn(t, "cause", 1)
        want = "set" if kind == "ctl lw" else "clear"
        row("%s %s pre" % (lbl, kind), ip2(before), "clear", "IP2 before the access (SOFTINT set, no reassert)")
        row("%s %s" % (lbl, kind), ip2(after), want,
            ("CONTROL: accepted lw at +0x%x reasserts" if kind == "ctl lw" else "refused %s at +0x%%x: no reassert" % kind)
            % off)

# ---- E3: TIME update at the CRIME_TIME label ----
A = Addr(CODE)
c = []
c += ld(A, "ld", CRIME + 0x38, "s0")
c += ld(A, "lb", CRIME + 0x38, "v0")
c += ld(A, "ld", CRIME + 0x38, "s1")
c += ld(A, "ld", CRIME + 0x38, "s2")
c += ["print s0", "print s1", "print s2"]
t = session(c)
s0, s1, s2 = prn(t, "s0"), prn(t, "s1"), prn(t, "s2")
SMALL = 66 * 100000                            # 0.1 s of CRIME_TIME: the one tick after step 1 adds ~66-132


def mag(v):
    return "absent" if v is None else ("small" if v < SMALL else "large")


row("time s0", s0, 0, "first ld: last_us latched, value 0")
row("time s1", mag(s1), "small", "ld after a refused lb +0x38 (raw %s)" % s1)
row("time s2 ctl", mag(s2), "large", "CONTROL: the accepted ld s1 updated TIME (raw %s)" % s2)

A = Addr(CODE)
c = []
c += ld(A, "ld", CRIME + 0x38, "s0")
c += st(A, "sb", CRIME + 0x38, 0)
c += ld(A, "ld", CRIME + 0x38, "s1")
c += ["print s0", "print s1"]
t = session(c)
s1 = prn(t, "s1")
row("time sb s1", mag(s1), "small", "ld after a refused sb +0x38 (raw %s)" % s1)

# ---- E4: narrow WRITE at CRIME_REV from the PROM window ----
for op in ("sw", "sh", "sb"):
    A = Addr(CODE)
    t = session(["ra=0x%x" % RA] + st(A, op, CRIME + 0, 0, at=PROBE_PC) + ["print pc"])
    p = prn(t, "pc")
    want = RA if op == "sw" else PROBE_PC + 4
    row("revw %s pc" % op, ("0x%x" % p) if p is not None else "absent", "0x%x" % want,
        "CONTROL: accepted sw -> ra" if op == "sw" else "refused %s at +0 from 0xbfc05180: pc NOT ra" % op)

# ---- E5: accept cells at memory control (bank 1 ctrl = 1 for -M 64) ----
A = Addr(CODE)
c = []
c += ld(A, "lw", CRIME + 0x214, "s0")
c += ld(A, "ld", CRIME + 0x210, "s1")
c += ld(A, "lw", CRIME + 0x34, "s2")        # a DOG-cell 4R, the address the detector does use
c += ["print s0", "print s1", "print s2"]
t = session(c)
row("mc 4R lo +0x214", prn(t, "s0"), 1, "bank 1 ctrl low half")
row("mc 8R +0x210", prn(t, "s1"), 1, "bank 1 ctrl")

print("")
print("DIFFS: " + ", ".join(n for n, ok in rows if not ok))
print("P2ESC_RESULT=%d/%d" % (sum(1 for _, ok in rows if ok), len(rows)))
print("P2ESC_DONE")
