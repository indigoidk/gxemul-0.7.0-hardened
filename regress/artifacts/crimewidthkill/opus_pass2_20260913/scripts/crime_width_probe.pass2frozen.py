#!/usr/bin/env python3
"""
crime_width_probe.py BIN [LABEL] -- #529 crimewidthkill DETECTOR, rung 3, cold debugger, UNMODIFIED `-E sgi -e ip32'.

src/devices/dev_sgi_ip32.c, DEVICE_ACCESS(crime): an access whose length is neither 8 nor 4 used to reach

        fatal("crime access len = %i!\n", len);
        exit(1);

so one guest lb/lbu/lh/lhu/sb/sh anywhere in CRIME (physical 0x14000000, KSEG1 0xb4000000) ended the emulator
(witnessed 6/6 at rung 3: regress/artifacts/crimewidthkill/crime_width_witness_20260913.py).  #529 DECLINES the width
with one latched `(once)' announce and a `goto' to the function's common tail, skipping the register switch -- the
#498 sgi_de shape.  A read is answered 0 by the tail, a write is dropped, the PC advances, no exception is raised.

Every access here is a real MIPS guest instruction through real address decode and memory_rw, one `step' at a time.

CONTRACT -- the edits this detector is designed to catch (clause (e)):
  1. the kill reinstated verbatim, or any other host death at the width arm       <op> surv (all six widths), latch surv
  2. FAULT: the width arm returning 0 (a guest data bus error, EXCEPTION_DBE)      <op> pc, <op> exc, lb/lh/lbu/lhu v0
  3. the refused access FALLING INTO THE REGISTER SWITCH (the goto lost, or a
     narrower decline), at each width x direction cell:
        1-byte write  sb 0x01   -> +0x08   the CRIME_CONTROL arm's unimplemented-control fatal   sb08 msg
        2-byte write  sh 0x0800 -> +0x08   the CRIME_CONTROL arm's HARD_RESET stops every CPU    sh08 run, sh08 pc
        1-byte read   lb  at +0 from pc 0xbfc05180   the CRIME_REV PROM-probe hack sets pc = ra  lb rev pc
        2-byte read   lh  at +0 from pc 0xbfc05180                                               lh rev pc
     Each channel carries a LIVE control on an accepted width that shows it can vary:
        rev pc ctl (lw redirects), sw08 halts (sw 0x800 stops the CPUs), sw08 msg ctl (sw 0x01 prints the text).
     *** THE sh08 AND sw08 CHANNELS EXIST BECAUSE OF A SEPARATE DEFECT, `crimectllane' (filed): the switch matches
     CRIME_CONTROL by its exact label 0x08 and reads the RAW idata, so a 32-bit write to the high half, or a halfword at
     +0x08, carries bit 11 into HARD_RESET, while NetBSD's +0x0c write does nothing.  A round that fixes that lane
     removes or moves these channels and owes their re-derivation -- the sw08 controls will go red to say so. ***
  4. the latch removed or never set: five refused accesses in one session owe EXACTLY ONE announce      latch x5
  5. the ACCEPT SET shrunk at any single cell (the de-escalation clause: the deleted exit(1) used to announce this):
        8W acc8 st, 8R acc8 ld, 4R high half acc4 rhi, 4R low half acc4 rlo, 4W low half acc4 wlo, 4W high half acc4 whi
     on CRIME_DOG (0x030), a register the switch gives no side effect ("No warning.").
  6. the announce text: each width's own session prints `unimplemented len=N at 0xA -- declined.' exactly once   <op> said

DISCLOSED, not rowed:
  * `goto crime_declined' -> `return 1' is EQUIVALENT on every channel: memory_rw pre-zeroes a device read buffer
    (#95, `if (writeflag == MEM_READ) memset(data, 0, len);' in src/cpus/memory_rw.c), so the tail's write of odata = 0
    and no write at all leave the same bytes.  Measured by the pass-1 Opus seat (opus_pass1_20260913/out/rows_return1.out).
  * a refused store's READBACK is non-varying across every candidate (the store is dropped by decline, FAULT and the
    switch's default arm alike -- measured 0xbadcafe unchanged in all of rows_*.out), so it carries no row.
  * the INTSTAT/INTMASK (reassert), TIME (update) and HARDINT (restore) cells a fall-through could reach: effects are
    idempotent or overwritten by the tail, and no observable here separates them.
  * FREE-RUNNING: fatal() is not verbosity-gated, so the announce prints free-running too (measured by the Opus seat);
    this detector steps only.
  * widths 3, 5, 6, 7 (no MIPS load/store issues them); the unaligned-pair instructions (lwl/lwr/swl/swr, ldl/ldr) are
    not rowed.  The RAM-size checks ABOVE the width arm (`-M 48' exits at the first CRIME access) are filed, not here.

Sentinel: CRIMEP_DONE (plus CRIMEP_RESULT=n/N and CRIMEP_CONTROL=OK|FAIL).
"""
import os, pty, re, select, sys, time

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
PROBE_PC = 0xbfc05180           # inside the CRIME_REV hack's window, (pc & 0xffffff00) == 0xbfc05100

R = {"zero": 0, "at": 1, "v0": 2, "v1": 3, "a0": 4, "a1": 5, "a2": 6, "a3": 7, "t0": 8, "t1": 9,
     "s0": 16, "s1": 17, "s2": 18, "s3": 19, "ra": 31}
OPC = {"lb": 0x20, "lh": 0x21, "lw": 0x23, "lbu": 0x24, "lhu": 0x25, "ld": 0x37,
       "sb": 0x28, "sh": 0x29, "sw": 0x2b, "sd": 0x3f}
OP_B_SELF = 0x1000ffff
OP_NOP = 0


def enc(op, rs, rt, imm=0):
    return (OPC[op] << 26) | (R[rs] << 21) | (R[rt] << 16) | (imm & 0xffff)


#  hand-assembled encodings checked against the committed witness's constants (a wrong register field reads 0, which
#  a decline's own answer would accept by accident -- so the accept rows carry nonzero wants)
assert enc("lb", "at", "v0") == 0x80220000 and enc("lhu", "at", "v0") == 0x94220000
assert enc("sb", "a3", "t0") == 0xa0e80000 and enc("sh", "a3", "t0") == 0xa4e80000
assert enc("sw", "a3", "t0") == 0xace80000 and enc("lw", "at", "v0") == 0x8c220000

rows = []


def row(name, got, want, note=""):
    ok = (got == want)
    rows.append((name, ok))
    print("%-16s %-20s %-20s %-40s %s" % (name, str(got), str(want), note, "ok" if ok else "FAIL"))
    sys.stdout.flush()


def session(cmds, settle=1.5, spin=1.2):
    """one emulator, read to the pty's EOF after `quit'.  Returns (text, clean): clean = EOF reached AND exit 0."""
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
    eof = True                      # a process already gone before `quit' has closed the pty; its status says how
    try:
        os.write(fd, b"quit\n")
        eof = not rd(10.0)          # to EOF, so anything printed on the way out is in the transcript
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


def exc(t):
    c = pr(t, "cause")
    return ("%d" % ((int(c, 16) >> 2) & 0x1f)) if c != "absent" else "absent"


def count(t, s, clean):
    """a text count is evidence only from a whole transcript: an unclean session reads `unclean', never a number"""
    return t.count(s) if clean else "unclean"


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
    """one load `op rt, 0(at)', rt seeded with SENT; returns (cmds, code address)"""
    here = A.take(1) if at is None else at
    return ["at=0x%x" % addr, "%s=0x%x" % (rt, SENT)] + run_ops([enc(op, "at", rt)], here), here


def st(A, op, addr, val):
    here = A.take(1)
    return ["a3=0x%x" % addr, "t0=0x%x" % val] + run_ops([enc(op, "a3", "t0")], here), here


AFTER = ["print pc", "print cause"]


def roundtrip(A):
    """a RAM round trip printed in v1: absent if the host died, the sentinel if the CPU was stopped"""
    c1, _ = st(A, "sw", SCRATCH_RAM, LIVE_VAL)
    c2, _ = ld(A, "lw", SCRATCH_RAM, "v1")
    return c1 + c2 + ["print v1"]


def said(t, ln, off, clean):
    return count(t, "unimplemented len=%d at 0x%x -- declined." % (ln, off), clean)


print("CRIME WIDTH PROBE (#529) -- rung 3, unmodified -E sgi -e ip32   binary=%s  label=%s" % (BIN, LABEL))
print("%-16s %-20s %-20s %-40s %s" % ("row", "got", "want", "note", ""))

# ---- CONTROLS: liveness + device signature, one session ----
A = Addr(CODE)
c = roundtrip(A)
x, _ = ld(A, "lw", CRIME + 4, "s1"); c += x
x, _ = ld(A, "lw", CRIME + 0, "s2"); c += x
t, clean = session(c + ["print s1", "print s2"])
row("live", pr(t, "v1"), "0x%x" % LIVE_VAL, "LIVENESS: RAM round trip, same apparatus")
row("devsig", pr(t, "s1"), "0x11", "CRIME_REV low half = rev 0x11: a device")
row("devsig hi", pr(t, "s2"), "0x0", "CRIME_REV high half reads 0")

# ---- the switch channels are LIVE on an accepted width (else rows 3.x could not vary) ----
A = Addr(CODE)
x, _ = ld(A, "lw", CRIME + 0, "v0", at=PROBE_PC)
t, clean = session(["ra=0x%x" % RA] + x + AFTER)
row("rev pc ctl", pr(t, "pc"), "0x%x" % RA, "CONTROL: lw CRIME_REV from 0xbfc051xx -> ra")

A = Addr(CODE)
x, _ = st(A, "sw", CRIME + 0x08, 0x0800)
t, clean = session(x + AFTER + roundtrip(A))
row("sw08 halts", pr(t, "v1"), "0x%x" % SENT, "CONTROL: sw 0x800 +0x08 stops CPUs (crimectllane)")

A = Addr(CODE)
x, _ = st(A, "sw", CRIME + 0x08, 0x01)
t, clean = session(x + AFTER + roundtrip(A))
row("sw08 msg ctl", count(t, "CRIME_CONTROL: unimplemented", clean), 1, "CONTROL: sw 0x01 +0x08 prints the text")

# ---- ACCEPT cells on CRIME_DOG (0x030): 8W, 8R, 4R hi/lo, 4W lo/hi -- nonzero wants ----
A = Addr(CODE)
c = []
x, _ = st(A, "sd", CRIME + 0x30, 0x1122334455667788); c += x   # 8W
x, _ = ld(A, "ld", CRIME + 0x30, "a0"); c += x                  # 8R
x, _ = ld(A, "lw", CRIME + 0x30, "a1"); c += x                  # 4R high half
x, _ = ld(A, "lw", CRIME + 0x34, "a2"); c += x                  # 4R low half
x, _ = st(A, "sw", CRIME + 0x34, 0x0badcafe); c += x            # 4W low half
x, _ = ld(A, "ld", CRIME + 0x30, "s0"); c += x
x, _ = st(A, "sw", CRIME + 0x30, 0x0defaced); c += x            # 4W high half
x, _ = ld(A, "ld", CRIME + 0x30, "s3"); c += x
t, clean = session(c + ["print a0", "print a1", "print a2", "print s0", "print s3"])
row("acc8 st+ld", pr(t, "a0"), "0x1122334455667788", "8W then 8R at CRIME_DOG")
row("acc4 rhi", pr(t, "a1"), "0x11223344", "4R of the high half (+0x30)")
row("acc4 rlo", pr(t, "a2"), "0x55667788", "4R of the low half (+0x34)")
row("acc4 wlo", pr(t, "s0"), "0x112233440badcafe", "4W low half lands, high half kept")
row("acc4 whi", pr(t, "s3"), "0xdefaced0badcafe", "4W high half lands, low half kept")

# ---- REFUSED widths, one session each: value, pc, exccode, survival, own announce ----
for op, off, full in (("lb", 7, True), ("lh", 6, True), ("lbu", 7, False), ("lhu", 6, False)):
    A = Addr(CODE)
    x, here = ld(A, op, CRIME + off, "v0")
    t, clean = session(x + AFTER + ["print v0"] + roundtrip(A))
    ln = 1 if op in ("lb", "lbu") else 2
    row("%s v0" % op, pr(t, "v0"), "0x0", "declined read answers 0 (dest seeded 0x%x)" % SENT)
    if full:
        row("%s pc" % op, pr(t, "pc"), "0x%x" % (here + 4), "pc advances, no vector")
        row("%s exc" % op, exc(t), "0", "cause.ExcCode 0 (a bus error is 7)")
        row("%s said" % op, said(t, ln, off, clean), 1, "own announce, len=%d at 0x%x, once" % (ln, off))
    row("%s surv" % op, pr(t, "v1"), "0x%x" % LIVE_VAL, "host survives, then a RAM trip")

for op, off, val in (("sb", 0x1f, 0xff), ("sh", 0x1e, 0xffff)):
    A = Addr(CODE)
    x, here = st(A, op, CRIME + off, val)
    t, clean = session(x + AFTER + roundtrip(A))
    ln = 1 if op == "sb" else 2
    row("%s pc" % op, pr(t, "pc"), "0x%x" % (here + 4), "pc advances, no vector")
    row("%s exc" % op, exc(t), "0", "cause.ExcCode 0 (a bus error is 7)")
    row("%s said" % op, said(t, ln, off, clean), 1, "own announce, len=%d at 0x%x, once" % (ln, off))
    row("%s surv" % op, pr(t, "v1"), "0x%x" % LIVE_VAL, "host survives, then a RAM trip")

# ---- the switch is NOT entered by a refused width, per cell (contract 3) ----
A = Addr(CODE)
x, here = st(A, "sh", CRIME + 0x08, 0x0800)
t, clean = session(x + AFTER + roundtrip(A))
row("sh08 pc", pr(t, "pc"), "0x%x" % (here + 4), "2W sh 0x800 +0x08: pc advances")
row("sh08 run", pr(t, "v1"), "0x%x" % LIVE_VAL, "2W: CPUs NOT stopped (RAM trip runs)")

A = Addr(CODE)
x, here = st(A, "sb", CRIME + 0x08, 0x01)
t, clean = session(x + AFTER + roundtrip(A))
row("sb08 msg", count(t, "CRIME_CONTROL: unimplemented", clean), 0, "1W sb 0x01 +0x08: no CONTROL text")

for op in ("lb", "lh"):
    A = Addr(CODE)
    x, _ = ld(A, op, CRIME + 0, "v0", at=PROBE_PC)
    t, clean = session(["ra=0x%x" % RA] + x + AFTER)
    row("%s rev pc" % op, pr(t, "pc"), "0x%x" % (PROBE_PC + 4), "%dR at CRIME_REV from 0xbfc05180: pc NOT ra"
        % (1 if op == "lb" else 2))

# ---- the latch: five refused accesses, one session, exactly one announce ----
A = Addr(CODE)
c = []
for op, off in (("lb", 7), ("lh", 6), ("lbu", 0x3f)):
    x, _ = ld(A, op, CRIME + off, "v0"); c += x
for op, off, val in (("sb", 0x37, 0xab), ("sh", 0x36, 0xabcd)):
    x, _ = st(A, op, CRIME + off, val); c += x
t, clean = session(c + roundtrip(A))
row("latch x5", count(t, "-- declined.", clean), 1, "5 refused accesses -> one (once)")
row("latch surv", pr(t, "v1"), "0x%x" % LIVE_VAL, "host survives all five")

npass = sum(1 for _, ok in rows if ok)
st_ = dict(rows)
control = all(st_.get(n, False) for n in ("live", "devsig", "devsig hi", "rev pc ctl", "sw08 halts", "sw08 msg ctl"))
print("")
print("FAILING: " + ", ".join(n for n, ok in rows if not ok))
print("CRIMEP_RESULT=%d/%d" % (npass, len(rows)))
print("CRIMEP_CONTROL=%s" % ("OK" if control else "FAIL"))
print("CRIMEP_DONE")
