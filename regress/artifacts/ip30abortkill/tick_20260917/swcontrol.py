#!/usr/bin/env python3
"""THE `sw' NEGATIVE CONTROL, plus the CORRECTED period derivation.

(1) WIDTH.  `case 0x10000' assigns imask0 from memory_readmax64(cpu, data, len).  A 4-byte
    store caps idata below 2^32, so bit 50 is UNSETTABLE by a word store however hostile the
    value.  Measured here with 0xffffffff -- every bit a `sw' can reach -- stepped past two
    ticks.  If this survives while the `sd' rows die, the WIDTH of the guest store is a
    load-bearing part of the reachability claim and must be written into the record.

(2) PERIOD, corrected by measurement.  My first derivation said tick #2 lands at
    machine_run #65537; the boundary run measured #65536 (N=65526 died, N=65525 lived).
    Re-derived: MR#1 leaves 65535, so MR#k leaves 65536-k, and it fires when 65536-k <= 0,
    i.e. k = 65536.  The off-by-one was mine.  Re-confirmed here from the OTHER side, with
    no warmup at all: arm bit 50 on MR#1 -- which itself fires tick #1 and dies -- so the
    only clean no-warmup period check is a bit-49 arming plus a step to MR#65536, where a
    LATER swap of the bit would die.  Kept simple instead: two warmups of different length,
    each with its own boundary, which pins the period at 65536 independently of any offset.
"""
import os, pty, select, signal, time

BIN = "/mnt/c/DocumentNoSnc/CC/GXEMUL/build/gxemul"
HERE = os.path.dirname(os.path.abspath(__file__))
DUMMY = os.path.join(HERE, "ip30_dummy.bin")
CODE = 0x80001000
A_IMASK0 = 0xFFFFFFFFAFF10000
SD = 0xFCE80000
SW = 0xACE80000


def session(cmds, settle=2.0, spin=2.5, cmd_wait=0.35, last_wait=None):
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN, [BIN, "-V", "-x", "-E", "sgi", "-e", "ip30", "-M", "64",
                       "0x%x:" % CODE + DUMMY])
        os._exit(127)
    buf = ""

    def rd(t, until_prompt=False):
        nonlocal buf
        end = time.time() + t
        while time.time() < end:
            if until_prompt and buf.rstrip(" ").endswith("GXemul>"):
                return
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
    for i, c in enumerate(cmds):
        try:
            os.write(fd, (c + "\n").encode())
        except OSError:
            break
        if last_wait is not None and i == len(cmds) - 1:
            rd(last_wait, until_prompt=True)
        else:
            rd(cmd_wait)
    rd(spin)
    alive, status = True, None
    deadline = time.time() + 12.0
    while time.time() < deadline:
        try:
            wpid, st = os.waitpid(pid, os.WNOHANG)
        except ChildProcessError:
            alive = False
            break
        if wpid == pid:
            alive, status = False, st
            break
        time.sleep(0.05)
    sig = None
    if status is not None:
        sig = ("SIG%d" % os.WTERMSIG(status)) if os.WIFSIGNALED(status) \
            else ("exit%d" % os.WEXITSTATUS(status))
    if alive:
        try:
            os.kill(pid, signal.SIGKILL); os.waitpid(pid, 0)
        except OSError:
            pass
    try:
        os.close(fd)
    except OSError:
        pass
    return buf, alive, sig


def plant(ops, at=CODE):
    p = ["put w 0x%x, 0x%08x" % (at + 4 * i, o) for i, o in enumerate(ops)]
    p += ["put w 0x%x, 0x%08x" % (at + 4 * len(ops), 0x1000FFFF),
          "put w 0x%x, 0x%08x" % (at + 4 * len(ops) + 4, 0)]
    return p + ["pc=0x%x" % at]


print("=== (1) WIDTH: `sw' 0xffffffff to imask0, then 70000 steps (two ticks) ===")
_, alive, sig = session(["a3=0x%x" % A_IMASK0, "t0=0xffffffff"] + plant([SW])
                        + ["step 70000"], last_wait=120.0)
print("  sw 0xffffffff  -> %s   want=alive (bit 50 unreachable by a 4-byte store)"
      % ("alive" if alive else "DEAD(%s)" % sig))

print("=== (1b) same store WIDTH but `sd': the positive twin ===")
_, alive, sig = session(["a3=0x%x" % A_IMASK0, "t0=0xffffffff"] + plant([SD])
                        + ["step 70000"], last_wait=120.0)
print("  sd 0xffffffff  -> %s   want=alive too (bit 50 still clear -- value, not width)"
      % ("alive" if alive else "DEAD(%s)" % sig))

print("=== (2) PERIOD, second boundary at a DIFFERENT warmup (100), predicts N=65436 ===")
WARM100 = plant([0]) + ["step 100"]
ARM = ["a3=0x%x" % A_IMASK0, "t0=0x%x" % (1 << 50)] + plant([SD])
for n, predict in ((65435, "alive"), (65436, "DEAD")):
    _, alive, sig = session(WARM100 + ARM + ["step %d" % n], last_wait=120.0)
    got = "alive" if alive else "DEAD(%s)" % sig
    print("  warm=100 N=%-6d predict=%-6s got=%-12s %s"
          % (n, predict, got, "ok" if got.startswith(predict) else "MISMATCH"))
print("SWCONTROL_DONE")
