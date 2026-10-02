#!/usr/bin/env python3
"""t4clear.py BIN LABEL -- #529 closing pass 8.  THE OWED ROW, measured before it is written: the TIME 4-byte
GAPPED pair with the latch CLEAR.

Repair 13's `p t4w gap' / `p t4r gap' are the GAPPED shape WITH an opening refused `lb' -- that is the entire point
of them, and it is why they cannot see a bypass conditioned on `!(d->warned & CRIME_W_LEN)'.  This is the same shape
MINUS the refusal, so every access here runs with the latch CLEAR.

THE CHANNEL, and it is the one closing pass 7 established and RAN: a read takes `odata' BEFORE its own
crime_update_crime_time(), and the debugger's pause BETWEEN `step' commands is the gap -- so an update that HAPPENS
lands before the final 8R and one that is SKIPPED arrives after it.

    step 1  [ld +0x38]      TIME 8R: `last_microseconds' is initialised here, while TIME is still ~0
      ~0.25 s of host time passes (the debugger's own inter-command gap)
    step 1  [sw/lw +0x38]   *** THE CELL UNDER TEST, latch CLEAR ***  its arm's update adds 66 x the gap
      ~0.25 s
    step 1  [ld +0x38]      reads what the cell access left behind, BEFORE its own update

Base: the middle access's update lands, so the final read is LARGE.  Under a latch-clear bypass at that cell the
update never happens and the final read is SMALL.

CONTROLS: `clear once' proves the latch really is CLEAR (zero announces in the whole session); `ram' proves the host
is alive; `devsig' proves this is CRIME and not RAM.

Sentinel: T4CLEAR_DONE (plus T4CLEAR_RESULT=n/N).  Raw values are printed so the record can cite them.
"""
import os
import pty
import re
import select
import signal
import sys
import time

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
SMALL = 66 * 100000                    # the shipped probe's own threshold (crime_width_probe.py, `SMALL')
R = {"zero": 0, "at": 1, "v0": 2, "v1": 3, "a0": 4, "a1": 5, "a2": 6, "a3": 7, "t0": 8, "t1": 9,
     "s0": 16, "s1": 17, "s2": 18, "s3": 19, "ra": 31}
OPC = {"lb": 0x20, "lh": 0x21, "lw": 0x23, "lbu": 0x24, "lhu": 0x25, "ld": 0x37,
       "sb": 0x28, "sh": 0x29, "sw": 0x2b, "sd": 0x3f}
OP_B_SELF = 0x1000ffff
OP_NOP = 0
rows = []


def enc(op, rs, rt, imm=0):
    return (OPC[op] << 26) | (R[rs] << 21) | (R[rt] << 16) | (imm & 0xffff)


assert enc("lb", "at", "v0") == 0x80220000 and enc("lw", "at", "v0") == 0x8c220000
assert enc("sw", "a3", "t0") == 0xace80000


def row(name, got, want, note=""):
    rows.append((name, got == want))
    print("%-16s %-14s %-14s %-52s %s" % (name, str(got), str(want), note, "ok" if got == want else "FAIL"))
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
    v = re.findall(r"print\s+%s\s*\n\s*(0x[0-9a-f]+)" % reg, t)
    return int(v[n], 16) if len(v) > n else None


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


def gapped_clear(kind):
    """the GAPPED shape with NO opening refusal: every access runs with d->warned & CRIME_W_LEN CLEAR"""
    ops = [enc("ld", "at", "v1"),                                            # TIME 8R, TIME still ~0
           enc("sw", "at", "t0") if kind == "w" else enc("lw", "at", "a0"),  # the cell under test
           enc("ld", "at", "v0")]                                            # what it left behind
    c = ["at=0x%x" % (CRIME + 0x38), "t0=0x0a0b0c0d",
         "v0=0x%x" % SENT, "v1=0x%x" % SENT, "a0=0x%x" % SENT]
    for i, op in enumerate(ops):
        c.append("put w 0x%x, 0x%08x" % (CODE + 4 * i, op))
    c += ["put w 0x%x, 0x%08x" % (CODE + 4 * len(ops), OP_B_SELF),
          "put w 0x%x, 0x%08x" % (CODE + 4 * len(ops) + 4, OP_NOP), "pc=0x%x" % CODE]
    c += ["step 1", "step 1", "step 1", "print v0", "print v1", "print a0"]
    t, clean = session(c)
    return nth(t, "v0", 0), nth(t, "v1", 0), nth(t, "a0", 0), (t.count("-- declined.") if clean else "unclean")


print("CRIME TIME-4BYTE LATCH-CLEAR GAPPED PROBE (#529 closing pass 8)  binary=%s  label=%s" % (BIN, LABEL))
print("%-16s %-14s %-14s %-52s %s" % ("row", "got", "want", "note", ""))

#  ---- liveness + device signature, one ordinary session ----
A = Addr(CODE)
c = st(A, "sw", SCRATCH_RAM, LIVE_VAL) + ld(A, "lw", SCRATCH_RAM, "v1") + ld(A, "lw", CRIME + 0x04, "s0")
t0, clean0 = session(c + ["print v1", "print s0"])
row("ram", pr(t0, "v1"), "0x%x" % LIVE_VAL, "LIVENESS: host alive, RAM round trip")
row("devsig", pr(t0, "s0"), "0x11", "DEVICE SIGNATURE: lw +0x04 is CRIME_REV, not RAM")

_note = []
for kind in ("w", "r"):
    v0, v1, a0, n = gapped_clear(kind)
    _note.append(n)
    row("c t4%s gap" % kind, mag(v0), "large",
        "step1[ld] step1[%s] step1[ld] LATCH CLEAR (raw %s, first ld %s, cell %s)"
        % ("sw" if kind == "w" else "lw", None if v0 is None else hex(v0),
           None if v1 is None else hex(v1), None if a0 is None else hex(a0)))
row("clear once", _note, [0, 0], "CONTROL: NO refusal in either session -- the latch stays CLEAR")

npass = sum(1 for _, ok in rows if ok)
print("")
print("FAILING: " + ", ".join(nm for nm, ok in rows if not ok))
print("T4CLEAR_RESULT=%d/%d" % (npass, len(rows)))
print("T4CLEAR_DONE")
