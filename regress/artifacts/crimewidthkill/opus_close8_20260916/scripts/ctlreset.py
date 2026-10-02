#!/usr/bin/env python3
"""ctlreset.py BIN LABEL -- #529 closing pass 8.  THE OWED ROW for the codex seat's cell, measured before it is
written: a CONTROL write carrying HARD_RESET (0x800), at BOTH accepted widths, with the latch SET.

WHY IT IS OWED.  The 2026-09-04 generating-set clause: "at each floor cell, every idata bit the guarded body TESTS
is written both clear and set."  The CONTROL arm tests three idata bits -- DOG_ENABLE 0x200, HARD_RESET 0x800 and
the `idata != 0' leftover.  Post-latch the 188-row probe writes CONTROL with 0x01 (8W), 0x0001 and 0x0201 (4W):
HARD_RESET is CLEAR in every one.  The only session that writes 0x800 is `sw08 halts' (session #2) and it writes it
BEFORE any refusal.  So at the latch-SET CONTROL-4W and CONTROL-8W floor cells the bit is never set.

THE CHANNEL: `:364-373' -- an accepted CONTROL write with HARD_RESET set runs `cpu->machine->cpus[j]->running = 0'
for every CPU.  The guest then executes NOTHING further, so a RAM round trip issued afterwards leaves its
destination register at the SENTINEL.  A declined write leaves the CPUs running and the round trip completes.
That is the same oracle the shipped `sw08 halts' row uses, moved into the latch-SET state.

    sess A   refused lb +0x07   then   sw +0x08 <- 0x800   then a RAM round trip     -> halted: v1 == SENTINEL
    sess B   refused lb +0x07   then   sd +0x08 <- 0x800   then a RAM round trip     -> halted: v1 == SENTINEL
    sess C   (NEGATIVE CONTROL) refused lb +0x07, NO CONTROL write, RAM round trip   -> alive:  v1 == LIVE_VAL

Sentinel: CTLRESET_DONE (plus CTLRESET_RESULT=n/N).
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
R = {"zero": 0, "at": 1, "v0": 2, "v1": 3, "a0": 4, "a1": 5, "a2": 6, "a3": 7, "t0": 8, "t1": 9,
     "s0": 16, "s1": 17, "s2": 18, "s3": 19, "ra": 31}
OPC = {"lb": 0x20, "lh": 0x21, "lw": 0x23, "lbu": 0x24, "lhu": 0x25, "ld": 0x37,
       "sb": 0x28, "sh": 0x29, "sw": 0x2b, "sd": 0x3f}
OP_B_SELF = 0x1000ffff
OP_NOP = 0
rows = []


def enc(op, rs, rt, imm=0):
    return (OPC[op] << 26) | (R[rs] << 21) | (R[rt] << 16) | (imm & 0xffff)


assert enc("lb", "at", "v0") == 0x80220000 and enc("sw", "a3", "t0") == 0xace80000
assert enc("sd", "a3", "t0") == 0xfce80000


def row(name, got, want, note=""):
    rows.append((name, got == want))
    print("%-16s %-14s %-14s %-50s %s" % (name, str(got), str(want), note, "ok" if got == want else "FAIL"))
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


def trip(A):
    return st(A, "sw", SCRATCH_RAM, LIVE_VAL) + ld(A, "lw", SCRATCH_RAM, "v1") + ["print v1"]


def halt_session(op):
    """refused lb (sets the latch), then a HARD_RESET write at CONTROL, then a RAM round trip"""
    A = Addr(CODE)
    c = ld(A, "lb", CRIME + 0x07, "v0")
    if op is not None:
        c += st(A, op, CRIME + 0x08, 0x800)
    c += trip(A)
    t, clean = session(c)
    return pr(t, "v1"), (t.count("-- declined.") if clean else "unclean")


print("CRIME CONTROL HARD_RESET POST-LATCH PROBE (#529 closing pass 8)  binary=%s  label=%s" % (BIN, LABEL))
print("%-16s %-14s %-14s %-50s %s" % ("row", "got", "want", "note", ""))

alive, n_alive = halt_session(None)
row("post alive", alive, "0x%x" % LIVE_VAL,
    "NEGATIVE CONTROL: refusal, no CONTROL write -- the guest runs on")
row("post alive once", n_alive, 1, "CONTROL: the control session refused exactly once")

for op, w in (("sw", 4), ("sd", 8)):
    v, n = halt_session(op)
    row("post rst %dw" % w, v, "0x%x" % SENT,
        "*** %s 0x800 at CONTROL with the latch SET halts every CPU ***" % op)
    row("post rst %dw n" % w, n, 1, "CONTROL: exactly one refusal announced")

npass = sum(1 for _, ok in rows if ok)
print("")
print("FAILING: " + ", ".join(nm for nm, ok in rows if not ok))
print("CTLRESET_RESULT=%d/%d" % (npass, len(rows)))
print("CTLRESET_DONE")
