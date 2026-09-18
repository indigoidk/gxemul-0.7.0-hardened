#!/usr/bin/env python3
"""OPUS SEAT, #531 pass 2: measure the SHIPPED fix's latch CONSUMPTION.

Not a mutant.  This asks a question about the fix itself that no row in
ip30_abort_probe.py asks: once an ORDINARY guest write at 0x10020 has consumed
IP30_W_ISR, is a subsequent DECLINED access still announced?

Session machinery copied verbatim from the frozen probe copy so the vehicle is
the same one the 18-row table uses.
"""
import os, pty, re, select, signal, sys, time

BIN = sys.argv[1]
DUMMY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ip30_dummy.bin")
if not os.path.exists(DUMMY):
    open(DUMMY, "wb").write(b"\0" * 8)

CODE = 0x80001000
BASE = 0xFFFFFFFFAFF00000
A_IMASK0 = BASE + 0x10000
A_SETISR = BASE + 0x10020
A_CLRISR = BASE + 0x10028
A_ISR = BASE + 0x10030
OP_LW_V0_AT = 0x8C220000
OP_SW_T0_A3 = 0xACE80000
OP_SD_T0_A3 = 0xFCE80000
OP_B_SELF = 0x1000FFFF
OP_NOP = 0x00000000

ISRMSG = "sgi_ip30: interrupt-status rewrite not implemented"
TICKMSG = "sgi_ip30: timer interrupt delivery not implemented"


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
            wpid, status = os.waitpid(pid, os.WNOHANG)
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


def store64(addr, val):
    return ["a3=0x%x" % addr, "t0=0x%x" % val] + run_ops([OP_SD_T0_A3])


def load(addr):
    return ["at=0x%x" % addr] + run_ops([OP_LW_V0_AT])


def cnt(t, msg):
    #  the pty may wrap the line, so count on whitespace-collapsed text
    return len(re.findall(re.escape(msg), re.sub(r"\s+", " ", t)))


CASES = [
    ("A  lone decline: LOAD 0x10020 only",
     load(A_SETISR), ISRMSG, 1),
    ("B  benign WRITE 0x10020, then DECLINED LOAD 0x10020",
     store(A_SETISR, 0x5a5a) + load(A_SETISR), ISRMSG, 2),
    ("C  benign WRITE 0x10020, then DECLINED WRITE 0x10030 (read-only reg)",
     store(A_SETISR, 0x5a5a) + store(A_ISR, 0x1), ISRMSG, 2),
    ("D  benign WRITE 0x10020, then DECLINED LOAD 0x10028",
     store(A_SETISR, 0x5a5a) + load(A_CLRISR), ISRMSG, 2),
    ("E  benign WRITE 0x10020, then ARM tick bit 50 (cross-bit control)",
     store(A_SETISR, 0x5a5a) + store64(A_IMASK0, 1 << 50) + ["step 1"], TICKMSG, 1),
]

print("latchcount -- binary=%s" % BIN)
for name, cmds, msg, ideal in CASES:
    t, alive = session(cmds)
    print("  %-62s alive=%-5s announces=%d   (distinct guest events: %d)"
          % (name, alive, cnt(t, msg), ideal))
print("LATCHCOUNT_DONE")
