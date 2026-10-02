#!/usr/bin/env python3
"""crime_f2_obs.py BIN [LABEL] [timing|timingN] -- #529 F2 pass, Opus seat: OBSERVABLES for cells the 71-row detector
does not row.  Same apparatus as regress/crime_width_probe.py (cold debugger, unmodified -E sgi -e ip32 -M 64, one
`step' at a time).  Every row's WANT is the fixed build's behaviour; a mutant that differs prints DIFF.

  H1..H4  HALFWORD at INTMASK/INTSTAT: setup sd INTMASK=bit28, sd SOFTINT=bit28 (default arm: no reassert, IP2 low);
          a refused lh or sh AT the label; cause.IP2 must stay clear; CONTROL: an accepted lw there sets it.
  H5,H6   HALFWORD at TIME: ld +0x38 (latches), refused lh/sh +0x38, ld -> s1 (small on the fix), ld -> s2 (ctl, large)
  L1      LATCH, halfwords only: lh +6, lhu +6, sh +0x1e, lh +0x16 -> exactly one announce
  L2      LATCH, writes first: sb +0x1f, sh +0x1e, sb +0x37, then lb +7 -> exactly one announce
  S1      a refused sb at SOFTINT (+0x20, unlabelled): guest state (cause, SOFTINT via ld) + host default-arm text
  W1      a refused sb at +0x27f, then an accepted ld +0x278: the store must not land (0)
  F1      the free-running session exactly as the probe issues it: where the first `continue' is, whether the
          CTRL-C break-in returned a prompt, and the transcript tail
  timing  the probe's `time lb' session repeated N times, printing the raw s1/s2 values (the SMALL threshold's margin)

Sentinel: F2OBS_DONE
"""
import os, pty, re, select, signal, sys, time

BIN = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "?"
MODE = sys.argv[3] if len(sys.argv) > 3 else "obs"
DUMMY = "/tmp/dummy_crimep.bin"
if not os.path.exists(DUMMY):
    with open(DUMMY, "wb") as f:
        f.write(b"\0" * 16)

CODE = 0x80001000
SCRATCH_RAM = 0xa0001800
LIVE_VAL = 0x12345678
CRIME = 0xb4000000
SENT = 0xdeadbeef
BIT = 0x10000000
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

rows = []


def row(name, got, want, note=""):
    ok = (got == want)
    rows.append((name, ok))
    print("%-16s %-22s %-22s %-44s %s" % (name, str(got), str(want), note, "ok" if ok else "DIFF"))
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


def pr(t, reg):
    m = re.search(r"print\s+%s\s*\n\s*(0x[0-9a-f]+)" % reg, t)
    return ("0x%x" % int(m.group(1), 16)) if m else "absent"


def nth(t, reg, n):
    ms = re.findall(r"print\s+%s\s*\n\s*(0x[0-9a-f]+)" % reg, t)
    return int(ms[n], 16) if len(ms) > n else None


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


def ld(A, op, addr, rt):
    here = A.take(1)
    return ["at=0x%x" % addr, "%s=0x%x" % (rt, SENT)] + run_ops([enc(op, "at", rt)], here)


def st(A, op, addr, val):
    here = A.take(1)
    return ["a3=0x%x" % addr, "t0=0x%x" % val] + run_ops([enc(op, "a3", "t0")], here)


def roundtrip(A):
    return st(A, "sw", SCRATCH_RAM, LIVE_VAL) + ld(A, "lw", SCRATCH_RAM, "v1") + ["print v1"]


def dflt(t):
    return t.count("[ crime: read from") + t.count("[ crime: write to")


def time_session(op, width_op):
    A = Addr(CODE)
    c = ld(A, "ld", CRIME + 0x38, "s0")
    c += ld(A, width_op, CRIME + 0x38, "v0") if op == "r" else st(A, width_op, CRIME + 0x38, 0)
    c += ld(A, "ld", CRIME + 0x38, "s1") + ld(A, "ld", CRIME + 0x38, "s2")
    t, clean = session(c + ["print s1", "print s2"])
    return nth(t, "s1", 0), nth(t, "s2", 0), clean


print("CRIME F2 OBS (#529, Opus F2 seat)  binary=%s  label=%s  mode=%s" % (BIN, LABEL, MODE))

if MODE.startswith("timing"):
    n = int(MODE[6:] or "5")
    for k in range(n):
        s1, s2, clean = time_session("r", "lb")
        print("TIMING %d  s1=%s  s2=%s  clean=%s  s1_%s" % (k, s1, s2, clean, mag(s1)))
        sys.stdout.flush()
    print("F2OBS_DONE")
    sys.exit(0)

# ---- H1..H4: halfword at INTMASK / INTSTAT ----
for lbl, off in (("imask", 0x18), ("istat", 0x10)):
    for op in ("lh", "sh"):
        A = Addr(CODE)
        c = st(A, "sd", CRIME + 0x18, BIT) + st(A, "sd", CRIME + 0x20, BIT) + ["print cause"]
        c += ld(A, "lh", CRIME + off, "v0") if op == "lh" else st(A, "sh", CRIME + off, 0)
        c += ["print cause"] + ld(A, "lw", CRIME + off, "v0") + ["print cause"]
        t, clean = session(c)
        row("%s %s pre" % (lbl, op), ip2(nth(t, "cause", 0)), "clear", "setup leaves IP2 low")
        row("%s %s" % (lbl, op), ip2(nth(t, "cause", 1)), "clear", "refused %s +0x%x: no reassert" % (op, off))
        row("%s %s ctl" % (lbl, op), ip2(nth(t, "cause", 2)), "set", "CONTROL: accepted lw +0x%x reasserts" % off)

# ---- H5, H6: halfword at TIME ----
for op, w in (("r", "lh"), ("w", "sh")):
    s1, s2, clean = time_session(op, w)
    print("   (raw) time %s: s1=%s s2=%s" % (w, s1, s2))
    row("time %s" % w, mag(s1), "small", "ld after a refused %s +0x38" % w)
    row("time %s ctl" % w, mag(s2), "large", "CONTROL: the accepted ld moved TIME")

# ---- L1: latch, halfwords only ----
A = Addr(CODE)
c = ld(A, "lh", CRIME + 6, "v0") + ld(A, "lhu", CRIME + 6, "v0") + st(A, "sh", CRIME + 0x1e, 0xffff)
c += ld(A, "lh", CRIME + 0x16, "v0") + roundtrip(A)
t, clean = session(c)
row("latch lh x4", t.count("-- declined.") if clean else "unclean", 1, "4 refused halfwords -> one announce")

# ---- L2: latch, writes first ----
A = Addr(CODE)
c = st(A, "sb", CRIME + 0x1f, 0xff) + st(A, "sh", CRIME + 0x1e, 0xffff) + st(A, "sb", CRIME + 0x37, 0xab)
c += ld(A, "lb", CRIME + 7, "v0") + roundtrip(A)
t, clean = session(c)
row("latch w-first", t.count("-- declined.") if clean else "unclean", 1, "3 refused writes then a read -> one")

# ---- S1: refused sb at SOFTINT ----
A = Addr(CODE)
c = st(A, "sb", CRIME + 0x20, 0xff) + ["print cause", "print pc"] + ld(A, "ld", CRIME + 0x20, "a0")
c += ld(A, "ld", CRIME + 0x10, "a1") + ["print a0", "print a1"]
t, clean = session(c)
row("sft cause", ip2(nth(t, "cause", 0)), "clear", "refused sb +0x20: IP2")
row("sft softint", pr(t, "a0"), "0x0", "SOFTINT after the refused sb (ld)")
row("sft intstat", pr(t, "a1"), "0x0", "INTSTAT after the refused sb (ld)")
row("sft dflt", t.count("[ crime: write to 0x20") if clean else "unclean", 0,
    "HOST: default-arm write line at 0x20 (stepped)")

# ---- W1: refused sb at +0x27f, readback at +0x278 ----
A = Addr(CODE)
c = st(A, "sb", CRIME + 0x27f, 0xff) + ld(A, "ld", CRIME + 0x278, "a0") + ["print a0"]
t, clean = session(c)
row("mc keeps", pr(t, "a0"), "0x0", "refused sb +0x27f does not land (ld +0x278)")

# ---- F1: the free-running session as the probe issues it ----
A = Addr(CODE)
here = A.take(2)
c = ["at=0x%x" % (CRIME + 7), "v0=0x%x" % SENT,
     "put w 0x%x, 0x%08x" % (here, enc("lb", "at", "v0")),
     "put w 0x%x, 0x%08x" % (here + 4, OP_NOP),
     "put w 0x%x, 0x%08x" % (here + 8, OP_B_SELF),
     "put w 0x%x, 0x%08x" % (here + 12, OP_NOP),
     "pc=0x%x" % here, "<RUN>", "print v0"]
t, clean = session(c)
i_cont = t.find("continue")
i_put = t.find("put w")
ann = "unimplemented len=1 at 0x7 -- declined.  (once) ]"
i_ann = t.find(ann)
print("   (raw) free: first 'continue' at %d, first 'put w' at %d, announce at %d, total 'continue' %d, clean=%s"
      % (i_cont, i_put, i_ann, t.count("continue"), clean))
row("free cont order", "after-put" if i_cont > i_put >= 0 else "BEFORE-put", "after-put",
    "the split point is the typed command")
row("free ann order", "after-cont" if i_ann > i_cont >= 0 else "not-after", "after-cont", "announce after continue")
row("free v0", pr(t, "v0"), "0x0", "break-in worked and v0 read 0")
print("   (raw) free transcript tail:")
for ln in t[max(0, i_cont - 80):][:1200].split("\n"):
    print("   | " + ln)

print("")
print("DIFFS: " + ", ".join(n for n, ok in rows if not ok))
print("F2OBS_RESULT=%d/%d" % (sum(1 for _, ok in rows if ok), len(rows)))
print("F2OBS_DONE")
