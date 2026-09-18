#!/usr/bin/env python3
"""BOUNDARY: pin the exact machine_run() index at which tick #2 fires, so the period is a
MEASUREMENT and not an inference from machine.c.

Derivation under test (machine.c:354 ticks_till_next=0, :355 reset=1<<16, :726-738
`-= single_step ? 1 : ...' then fire while <=0):
    run #1     -> 0-1 = -1 <= 0   FIRES, counter += 65536 -> 65535
    run #k     -> leaves 65537-k
    run #65537 -> 0 <= 0          FIRES

With a 10-step NOP warmup consuming tick #1, arming bit 50, then stepping N:
    total runs = 10 + N, so tick #2 needs N = 65527.
    N = 65526 must SURVIVE; N = 65527 must DIE.  Two rows, opposite sides of one boundary.
"""
import os, pty, select, signal, sys, time

BIN = "/mnt/c/DocumentNoSnc/CC/GXEMUL/build/gxemul"
HERE = os.path.dirname(os.path.abspath(__file__))
DUMMY = os.path.join(HERE, "ip30_dummy.bin")
CODE = 0x80001000
A_IMASK0 = 0xFFFFFFFFAFF10000
SD = 0xFCE80000


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


WARM = plant([0]) + ["step 10"]
ARM = ["a3=0x%x" % A_IMASK0, "t0=0x%x" % (1 << 50)] + plant([SD])

print("BOUNDARY: 10-step warmup consumes tick #1, then bit 50 armed, then step N.")
for n, predict in ((65525, "alive"), (65526, "alive"), (65527, "DEAD"), (65528, "DEAD")):
    t0 = time.time()
    _, alive, sig = session(WARM + ARM + ["step %d" % n], last_wait=120.0)
    got = "alive" if alive else "DEAD(%s)" % (sig or "?")
    print("  N=%-6d predict=%-6s got=%-12s %s   (%.1fs)"
          % (n, predict, got, "ok" if got.startswith(predict) else "MISMATCH", time.time() - t0))
print("BOUNDARY_DONE")
