#!/usr/bin/env python3
"""
crime_opus_rows.py BIN LABEL -- OBSERVATIONAL rows for the crimewidthkill design question (opus seat, pass 1).

Same apparatus as regress/artifacts/crimewidthkill/crime_width_witness_20260913.py (cold debugger, unmodified
`-E sgi -e ip32 -M 64', real guest instructions through real address decode and memory_rw).  It does not grade a
candidate; it prints WHAT THE GUEST SEES so candidates can be compared column by column:

  * the destination of a refused load, seeded with a sentinel (FAULT leaves it; a decline writes 0 via the tail)
  * pc / cause.ExcCode / epc straight after the refused instruction (a data bus error is ExcCode 7)
  * whether a refused store lands (CRIME_DOG word pre-written with an accepted sw, then read back)
  * the switch side-effect cells a refused access could reach (CRIME_CONTROL HARD_RESET by a halfword at +0x08,
    CRIME_CONTROL at the architecturally-correct lane +0x0e, a byte to CRIME_CONTROL, the CRIME_REV PROM-probe hack)
  * accept cells for len 4 and 8, read and write (must be identical in every candidate)
  * the latch: text counts across five refused accesses in one session
  * FREE-RUNNING (breakpoint + continue): what the host prints when the guest is not single-stepped, and where the
    guest ends up
  * the -M 48 RAM-size kill (premise 7), which sits ABOVE the width guard

Sentinel: CRIMEO_DONE
"""
import os, pty, re, select, signal, sys, time

BIN = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "?"
DUMMY = "/tmp/dummy_crimew.bin"
if not os.path.exists(DUMMY):
    with open(DUMMY, "wb") as f:
        f.write(b"\0" * 16)

CODE = 0x80001000
SCRATCH_RAM = 0xa0001800
LIVE_VAL = 0x12345678
CRIME = 0xb4000000
SENT = 0xdeadbeef
RA = 0x80004000

R = {"zero": 0, "at": 1, "v0": 2, "v1": 3, "a0": 4, "a1": 5, "a2": 6, "a3": 7, "t0": 8, "t1": 9,
     "s0": 16, "s1": 17, "s2": 18, "ra": 31}
OPC = {"lb": 0x20, "lh": 0x21, "lw": 0x23, "lbu": 0x24, "lhu": 0x25, "ld": 0x37,
       "sb": 0x28, "sh": 0x29, "sw": 0x2b, "sd": 0x3f}
OP_B_SELF = 0x1000ffff
OP_NOP = 0


def enc(op, rs, rt, imm=0):
    return (OPC[op] << 26) | (R[rs] << 21) | (R[rt] << 16) | (imm & 0xffff)


# hand-assembled encodings cross-checked against the witness's constants (the witness is the committed source)
assert enc("lb", "at", "v0") == 0x80220000 and enc("lhu", "at", "v0") == 0x94220000
assert enc("sb", "a3", "t0") == 0xa0e80000 and enc("sh", "a3", "t0") == 0xa4e80000
assert enc("sw", "a3", "t0") == 0xace80000 and enc("lw", "at", "v0") == 0x8c220000


def session(cmds, mem="64", settle=1.5, spin=1.2):
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN, [BIN, "-V", "-x", "-E", "sgi", "-e", "ip32", "-M", mem, "0x80001000:" + DUMMY])
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
                if not d:
                    return False
                buf += d.decode("latin-1", "replace")
            except OSError:
                return False
        return True

    rd(settle)
    for i, c in enumerate(cmds):
        try:
            os.write(fd, (c + "\n").encode("latin-1"))
        except OSError:
            break
        if not rd(spin if i == len(cmds) - 1 else 0.3):
            break
    try:
        os.write(fd, b"quit\n")
        rd(2.0)
    except OSError:
        pass
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
    return buf.replace("\r", ""), how


def pr(t, reg):
    m = re.search(r"print\s+%s\s*\n\s*(0x[0-9a-f]+)" % reg, t)
    return ("0x%x" % int(m.group(1), 16)) if m else "absent"


def exc(t):
    c = pr(t, "cause")
    return ("%d" % ((int(c, 16) >> 2) & 0x1f)) if c != "absent" else "absent"


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
    """one load `op rt, 0(at)'; rt seeded with SENT; returns (cmds, code address)"""
    here = A.take(1) if at is None else at
    return ["at=0x%x" % addr, "%s=0x%x" % (rt, SENT)] + run_ops([enc(op, "at", rt)], here), here


def st(A, op, addr, val):
    here = A.take(1)
    return ["a3=0x%x" % addr, "t0=0x%x" % val] + run_ops([enc(op, "a3", "t0")], here), here


def after(tag):
    return ["print pc", "print cause", "print epc"]


def roundtrip(A):
    c1, _ = st(A, "sw", SCRATCH_RAM, LIVE_VAL)
    c2, _ = ld(A, "lw", SCRATCH_RAM, "v1")
    return c1 + c2 + ["print v1"]


def texts(t):
    return ("kill=%d decl=%d failed=%d dflt=%d ctlmsg=%d" %
            (t.count("crime access len"), t.count("-- declined."),
             t.count("device 'crime' addr"), t.count("[ crime: "), t.count("CRIME_CONTROL: unimplemented")))


def out(name, **kv):
    print("%-18s %s" % (name, "  ".join("%s=%s" % (k, v) for k, v in kv.items())))
    sys.stdout.flush()


print("CRIME OPUS ROWS -- binary=%s  label=%s" % (BIN, LABEL))

# ---- controls / accept cells (must be identical across every candidate) ----
A = Addr(CODE)
t, how = session(roundtrip(A))
out("ctl live", v1=pr(t, "v1"), how=how)

A = Addr(CODE)
c = []
x, _ = st(A, "sd", CRIME + 0x30, 0x1122334455667788); c += x
x, _ = ld(A, "ld", CRIME + 0x30, "a0"); c += x
x, _ = ld(A, "lw", CRIME + 0x30, "a1"); c += x
x, _ = ld(A, "lw", CRIME + 0x34, "a2"); c += x
x, _ = st(A, "sw", CRIME + 0x34, 0x0badcafe); c += x
x, _ = ld(A, "ld", CRIME + 0x30, "s0"); c += x
x, _ = ld(A, "lw", CRIME + 0x04, "s1"); c += x
x, _ = ld(A, "ld", CRIME + 0x00, "s2"); c += x
t, how = session(c + ["print a0", "print a1", "print a2", "print s0", "print s1", "print s2"])
out("acc 8/4 r+w", sd_ld=pr(t, "a0"), lw_hi=pr(t, "a1"), lw_lo=pr(t, "a2"), sw_then_ld=pr(t, "s0"),
    lw_rev_lo=pr(t, "s1"), ld_rev=pr(t, "s2"), how=how, txt=texts(t))

# ---- refused LOADS: destination / pc / exccode / epc / survival ----
for op, off in (("lb", 7), ("lbu", 7), ("lh", 6), ("lhu", 6), ("lb", 0x3f), ("lh", 0x10)):
    A = Addr(CODE)
    x, here = ld(A, op, CRIME + off, "v0")
    t, how = session(x + after(op) + ["print v0"] + roundtrip(A))
    out("%s +0x%02x" % (op, off), code=hex(here), v0=pr(t, "v0"), pc=pr(t, "pc"), exccode=exc(t), epc=pr(t, "epc"),
        v1_after=pr(t, "v1"), how=how, txt=texts(t))

# ---- refused STORES: does the store land? (CRIME_DOG word pre-written by an accepted sw) ----
for op, off, val in (("sb", 0x37, 0xab), ("sh", 0x36, 0xabcd), ("sb", 0x1f, 0xff), ("sh", 0x1e, 0xffff)):
    A = Addr(CODE)
    c, _ = st(A, "sw", CRIME + 0x34, 0x0badcafe)
    x, here = st(A, op, CRIME + off, val)
    y, _ = ld(A, "lw", CRIME + (off & ~3), "a0")
    t, how = session(c + x + after(op) + y + ["print a0"] + roundtrip(A))
    out("%s +0x%02x" % (op, off), code=hex(here), pc=pr(t, "pc"), exccode=exc(t), epc=pr(t, "epc"),
        readback=pr(t, "a0"), v1_after=pr(t, "v1"), how=how, txt=texts(t))

# ---- switch side-effect cells a refused access could reach ----
for name, op, off, val in (("sh CTL+08 0x800", "sh", 0x08, 0x0800),     # relative_addr == CRIME_CONTROL, idata 0x800
                           ("sh CTL+0e 0x800", "sh", 0x0e, 0x0800),     # the BE lane that actually holds bit 11
                           ("sb CTL+08 0x01", "sb", 0x08, 0x01),
                           ("sw CTL+0c 0x800", "sw", 0x0c, 0x0800)):    # control: the existing 4-byte arm at +0x0c
    A = Addr(CODE)
    x, here = st(A, op, CRIME + off, val)
    t, how = session(x + after(op) + roundtrip(A))
    out(name, code=hex(here), pc=pr(t, "pc"), exccode=exc(t), v1_after=pr(t, "v1"), how=how, txt=texts(t),
        halted=("yes" if re.search(r"(?i)halt|all cpus|stopped", t) else "no"))

# CRIME_REV PROM-probe hack: a read of relative_addr 0 from pc 0xbfc051xx sets pc = ra
PROBE_PC = 0xbfc05180
for name, op in (("revhack lw ctl", "lw"), ("revhack lb", "lb"), ("revhack lh", "lh")):
    A = Addr(CODE)
    x, here = ld(A, op, CRIME + 0, "v0", at=PROBE_PC)
    t, how = session(["ra=0x%x" % RA] + x + after(op) + ["print v0", "dump 0x%x 0x%x" % (PROBE_PC, PROBE_PC + 8)])
    m = re.search(r"bfc05180[^\n]*", t)
    out(name, pc=pr(t, "pc"), exccode=exc(t), v0=pr(t, "v0"), how=how, txt=texts(t),
        mem=(m.group(0)[:48] if m else "absent"))

# ---- latch: five refused accesses in one session ----
A = Addr(CODE)
c = []
for op, off in (("lb", 7), ("lh", 6), ("lbu", 0x3f)):
    x, _ = ld(A, op, CRIME + off, "v0"); c += x
for op, off, val in (("sb", 0x37, 0xab), ("sh", 0x36, 0xabcd)):
    x, _ = st(A, op, CRIME + off, val); c += x
t, how = session(c + roundtrip(A))
out("latch x5", v1_after=pr(t, "v1"), how=how, txt=texts(t))
for ln in t.split("\n"):
    if "declined" in ln or "crime access len" in ln or "device 'crime'" in ln:
        print("    | " + ln.strip()[:110])

# ---- FREE-RUNNING: breakpoint + continue (single_step false while the access executes) ----
A = Addr(CODE)
here = A.take(1)
c = ["at=0x%x" % (CRIME + 7), "v0=0x%x" % SENT,
     "put w 0x%x, 0x%08x" % (here, enc("lb", "at", "v0")),
     "put w 0x%x, 0x%08x" % (here + 4, OP_NOP),
     "put w 0x%x, 0x%08x" % (here + 8, OP_B_SELF),
     "put w 0x%x, 0x%08x" % (here + 12, OP_NOP),
     "breakpoint add 0x%x" % (here + 8),
     "breakpoint add 0x80000180", "breakpoint add 0xffffffffbfc00380",
     "pc=0x%x" % here, "continue"]
t, how = session(c + after("fr") + ["print v0", "print status"], spin=2.0)
seg = t.split("continue", 1)[1] if "continue" in t else ""
out("freerun lb +0x07", v0=pr(t, "v0"), pc=pr(t, "pc"), exccode=exc(t), epc=pr(t, "epc"), status=pr(t, "status"),
    how=how, txt=texts(t), txt_after_continue=texts(seg))
for ln in seg.split("\n")[:12]:
    if ln.strip():
        print("    | " + ln.strip()[:110])

# ---- premise 7: -M 48 constructs, then the FIRST CRIME access (of an accepted width) ends the process ----
A = Addr(CODE)
x, _ = ld(A, "lw", CRIME + 4, "v0")
t, how = session(x + ["print v0"] + roundtrip(A), mem="48")
out("M48 lw +0x04", v0=pr(t, "v0"), v1_after=pr(t, "v1"), how=how,
    ramkill=("yes" if "RAM size needs to be divisible" in t else "no"))

print("CRIMEO_DONE")
