#!/usr/bin/env python3
"""CORRECTED cross-bit measurement.  My first attempt (latchcount case E) was a
DEFECTIVE APPARATUS, not a finding:

    machine_add_tickfunction sets ticks_till_next[n] = 0 (machine.c), so the
    FIRST machine_run of a session fires every tick function and the next one is
    1<<16 = 65536 cycles away.  Case E spent that one free firing inside the
    SEEDING store -- before imask0 bit 50 was armed -- so the tick could not
    announce for any reason, and a `0' there says nothing about the latch.

Two valid orderings, both used here:
  X  arm bit 50 FIRST (its own step is the session's first machine_run), then
     do the ISR write.  Both messages must appear under the shipped TWO bits.
  Y  ISR write first, arm bit 50, then burn >65536 cycles in the `b .' self-loop
     so a SECOND tick lands.  Same expectation, opposite order.
  Z  CONTROL: ISR write only, burn the cycles, no bit 50 -- the tick message
     must NOT appear, or X/Y prove nothing.
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
OP_SW_T0_A3 = 0xACE80000
OP_SD_T0_A3 = 0xFCE80000
OP_B_SELF = 0x1000FFFF
OP_NOP = 0x00000000
ISRMSG = "sgi_ip30: interrupt-status rewrite not implemented"
TICKMSG = "sgi_ip30: timer interrupt delivery not implemented"


def session(cmds, settle=2.0, spin=3.0):
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
        rd(8.0 if c.startswith("step 7") else 0.35)
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


def store64(addr, val):
    return ["a3=0x%x" % addr, "t0=0x%x" % val] + run_ops([OP_SD_T0_A3])


def cnt(t, m):
    return len(re.findall(re.escape(m), re.sub(r"\s+", " ", t)))


CASES = [
    ("X  arm bit50 FIRST (first machine_run), then WRITE 0x10020",
     store64(A_IMASK0, 1 << 50) + store(A_SETISR, 0x5a5a)),
    ("Y  WRITE 0x10020, arm bit50, then burn 70000 cycles",
     store(A_SETISR, 0x5a5a) + store64(A_IMASK0, 1 << 50) + ["step 70000"]),
    ("Z  CONTROL: WRITE 0x10020, burn 70000 cycles, bit50 NEVER armed",
     store(A_SETISR, 0x5a5a) + ["step 70000"]),
]

print("tickcross -- binary=%s" % BIN)
for name, cmds in CASES:
    t, alive = session(cmds)
    print("  %-58s alive=%-5s ISR=%d  TICK=%d" % (name, alive, cnt(t, ISRMSG), cnt(t, TICKMSG)))
print("  EXPECTED under the SHIPPED two bits: X ISR=1 TICK=1 ; Y ISR=1 TICK=1 ; Z ISR=1 TICK=0")
print("  Under a SINGLE shared bit (M3): whichever message comes SECOND is lost.")
print("TICKCROSS_DONE")
