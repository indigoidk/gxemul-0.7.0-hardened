#!/usr/bin/env python3
"""Two semantic questions about the SHIPPED fix that NO row in the 19-row probe asks.

S1  set_isr is a SET, and this file ASSIGNS.  heart.h pairs `set_isr' with
    `clear_isr'; a set/clear PAIR exists precisely because the set is an OR.
    `d->isr = idata' therefore clobbers every other pending bit.  `isr keep'
    cannot see it: it seeds ONE value into a ZERO ISR, where `=' and `|=' agree.

S2  the 0x10020 read declines and returns 0.  Nothing pins the VALUE -- the
    probe's only 0x10020-read row scores `alive'.  grok's smallest clean-sweep
    (add `odata = d->isr' to that arm) is invisible unless the ISR is seeded
    NON-ZERO first and the load's own value is read.

Session machinery copied from the frozen probe so the vehicle is the same.
"""
import os, pty, re, select, signal, sys, time

BIN = sys.argv[1]
DUMMY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ip30_dummy.bin")
if not os.path.exists(DUMMY):
    open(DUMMY, "wb").write(b"\0" * 8)

CODE = 0x80001000
SENTINEL = 0x5a5a5a5a
BASE = 0xFFFFFFFFAFF00000
A_SETISR = BASE + 0x10020
A_CLRISR = BASE + 0x10028
A_ISR = BASE + 0x10030
OP_LW_V0_AT = 0x8C220000
OP_SW_T0_A3 = 0xACE80000
OP_B_SELF = 0x1000FFFF
OP_NOP = 0x00000000


def session(cmds, settle=2.0, spin=2.5):
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN, [BIN, "-V", "-x", "-E", "sgi", "-e", "ip30", "-M", "64",
                       "0x%x:" % CODE + DUMMY])
        os._exit(127)
    buf = ""

    def rd(t):
        nonlocal buf
        end = time.time() + t
        while time.time() < end:
            try:
                r, _, _ = select.select([fd], [], [], 0.1)
            except OSError:
                return
            if not r:
                continue
            try:
                d = os.read(fd, 65536)
            except OSError:
                return
            if not d:
                return
            buf += d.decode("utf-8", "replace")

    rd(settle)
    for c in cmds:
        try:
            os.write(fd, (c + "\n").encode())
        except OSError:
            break
        rd(0.35)
    rd(spin)
    alive = True
    deadline = time.time() + 12.0
    while time.time() < deadline:
        try:
            wpid, st = os.waitpid(pid, os.WNOHANG)
        except ChildProcessError:
            alive = False
            break
        if wpid == pid:
            alive = False
            break
        time.sleep(0.05)
    if alive:
        try:
            os.kill(pid, signal.SIGKILL)
            os.waitpid(pid, 0)
        except OSError:
            pass
    try:
        os.close(fd)
    except OSError:
        pass
    return buf, alive


def run_ops(ops, at=CODE):
    put = ["put w 0x%x, 0x%08x" % (at + 4 * i, op) for i, op in enumerate(ops)]
    put += ["put w 0x%x, 0x%08x" % (at + 4 * len(ops), OP_B_SELF),
            "put w 0x%x, 0x%08x" % (at + 4 * len(ops) + 4, OP_NOP)]
    return put + ["pc=0x%x" % at, "step %d" % len(ops)]


def store(addr, val):
    return ["a3=0x%x" % addr, "t0=0x%x" % val] + run_ops([OP_SW_T0_A3])


def load(addr):
    return ["at=0x%x" % addr, "v0=0x%x" % SENTINEL] + run_ops([OP_LW_V0_AT]) + ["print v0"]


def plast(t, reg="v0"):
    m = re.findall(r"print\s+%s\s*\n\s*(0x[0-9a-f]+)" % reg, t)
    return m[-1] if m else "ABSENT"


print("isrsem -- binary=%s" % BIN)

#  S1: two SETs.  `|=' would give 0x5aff; `=' gives 0x5a00.
t, alive = session(store(A_SETISR, 0x00ff) + store(A_SETISR, 0x5a00) + load(A_ISR))
print("  S1  set_isr 0x00ff then 0x5a00, read 0x10030 -> %s   alive=%s" % (plast(t), alive))
print("      OR-semantics would read 0x5aff ; assignment reads 0x5a00")

#  S1b: control -- does clear_isr behave as AND-NOT?
t, alive = session(store(A_SETISR, 0x00ff) + store(A_CLRISR, 0x000f) + load(A_ISR))
print("  S1b clear_isr 0x000f after set 0x00ff, read 0x10030 -> %s   alive=%s" % (plast(t), alive))
print("      AND-NOT semantics reads 0x00f0 (so the CLEAR side IS a clear, unlike the SET side)")

#  S2: seed the ISR non-zero, then LOAD 0x10020 and read the load's own value.
t, alive = session(store(A_SETISR, 0x5a5a) + load(A_SETISR))
print("  S2  load 0x10020 with ISR seeded 0x5a5a  -> %s   alive=%s" % (plast(t), alive))
print("      declined reads 0x0 ; a mirroring mutant reads 0x5a5a and NO SHIPPED ROW SEES IT")
print("ISRSEM_DONE")
