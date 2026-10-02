#!/usr/bin/env python3
"""ctl4r.py BIN LABEL -- #529 closing pass 8.  MEASURE the contract's CONTROL-4R EQUIVALENCE claim, which no kill
table has ever driven.  Modelled on opus_close7_20260915/scripts2/post7c.py.

The cell is measured TWICE -- once with the latch CLEAR and once with it SET -- because the whole K-class exists
because a row measured in one latch state cannot see a guard conditioned on the other.

Rows, and what each is for:
    ram          host alive, RAM round trip                     LIVENESS
    devsig       lw +0x04 answers CRIME_REV's 0x11              DEVICE SIGNATURE: this is CRIME, not RAM
    pre ctl4r    lw +0x08 BEFORE any refusal                    the cell with the latch CLEAR
    pre ctl0c    lw +0x0c BEFORE any refusal                    the OTHER lane of the same register: 0x100
    post ctl4r   lw +0x08 AFTER a refused lb +0x07              *** THE CELL UNDER TEST, latch SET ***
    post ctl0c   lw +0x0c after the refusal                     the other lane, latch SET
    post ctl8r   ld +0x08 after the refusal                     CONTROL is live post-latch and answers 0x100
    refused v0   the refused lb answers 0
    once         the announce count                             exactly one refusal in this session

Sentinel: CTL4R_DONE (plus CTL4R_RESULT=n/N).  Values are PRINTED, not only scored, so the record can cite them.
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


assert enc("lb", "at", "v0") == 0x80220000 and enc("lw", "at", "v0") == 0x8c220000
assert enc("sw", "a3", "t0") == 0xace80000


def row(name, got, want, note=""):
    rows.append((name, got == want))
    print("%-14s %-16s %-16s %-46s %s" % (name, str(got), str(want), note, "ok" if got == want else "FAIL"))
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


print("CRIME CONTROL-4R EQUIVALENCE PROBE (#529 closing pass 8)  binary=%s  label=%s" % (BIN, LABEL))
print("%-14s %-16s %-16s %-46s %s" % ("row", "got", "want", "note", ""))

A = Addr(CODE)
c = st(A, "sw", SCRATCH_RAM, LIVE_VAL) + ld(A, "lw", SCRATCH_RAM, "v1")
c += ld(A, "lw", CRIME + 0x04, "s0")            # device signature: CRIME_REV's low lane = 0x11
c += ld(A, "lw", CRIME + 0x08, "s1")            # THE CELL, latch CLEAR
c += ld(A, "lw", CRIME + 0x0c, "s2")            # the other lane of the same register, latch CLEAR
c += ld(A, "lb", CRIME + 0x07, "v0")            # THE REFUSAL -- sets d->warned & CRIME_W_LEN
c += ld(A, "lw", CRIME + 0x08, "s3")            # *** THE CELL, latch SET ***
c += ld(A, "lw", CRIME + 0x0c, "a1")            # the other lane, latch SET
c += ld(A, "ld", CRIME + 0x08, "a2")            # CONTROL is live post-latch (8R answers 0x100)
t, clean = session(c + ["print v1", "print s0", "print s1", "print s2", "print s3",
                        "print a1", "print a2", "print v0"])
n = t.count("-- declined.") if clean else "unclean"

row("ram", pr(t, "v1"), "0x%x" % LIVE_VAL, "LIVENESS: host alive, RAM round trip")
row("devsig", pr(t, "s0"), "0x11", "DEVICE SIGNATURE: lw +0x04 is CRIME_REV, not RAM")
row("pre ctl4r", pr(t, "s1"), "0x0", "lw +0x08, latch CLEAR (high lane of 0x100)")
row("pre ctl0c", pr(t, "s2"), "0x100", "lw +0x0c, latch CLEAR (LOW lane -- nonzero: the lane matters)")
row("post ctl4r", pr(t, "s3"), "0x0", "*** THE CELL: lw +0x08, latch SET ***")
row("post ctl0c", pr(t, "a1"), "0x100", "lw +0x0c, latch SET")
row("post ctl8r", pr(t, "a2"), "0x100", "CONTROL live post-latch: ld +0x08 answers 0x100")
row("refused v0", pr(t, "v0"), "0x0", "the refused lb +0x07 answers 0")
row("once", n, 1, "exactly one refusal announced")

npass = sum(1 for _, ok in rows if ok)
print("")
print("FAILING: " + ", ".join(nm for nm, ok in rows if not ok))
print("CTL4R_RESULT=%d/%d" % (npass, len(rows)))
print("CTL4R_DONE")
