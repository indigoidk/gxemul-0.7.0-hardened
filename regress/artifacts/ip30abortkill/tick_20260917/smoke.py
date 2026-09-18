#!/usr/bin/env python3
"""Smoke: does `sd' reach imask0 with high bits, and does `step 1' after setting bit 50 kill?
Prints the RAW transcript so the apparatus is visible before anything is scored."""
import os, pty, select, signal, sys, time

BIN = "/mnt/c/DocumentNoSnc/CC/GXEMUL/build/gxemul"
HERE = os.path.dirname(os.path.abspath(__file__))
DUMMY = os.path.join(HERE, "ip30_dummy.bin")
CODE = 0x80001000


def session(cmds, settle=2.0, spin=3.0, cmd_wait=0.4, last_wait=None):
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
    for i, c in enumerate(cmds):
        try:
            os.write(fd, (c + "\n").encode())
        except OSError:
            break
        w = last_wait if (last_wait is not None and i == len(cmds) - 1) else cmd_wait
        rd(w)
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
        sig = ("SIG%d" % os.WTERMSIG(status)) if os.WIFSIGNALED(status) else ("exit%d" % os.WEXITSTATUS(status))
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


A_IMASK0 = 0xFFFFFFFFAFF10000
SD = 0xFCE80000
LD = 0xDC220000

print("############ A: sd 1<<49 to imask0, step 1, then ld it back")
t, a, s = session(["a3=0x%x" % A_IMASK0, "t0=0x%x" % (1 << 49)] + plant([SD]) + ["step 1"]
                  + ["at=0x%x" % A_IMASK0, "v0=0x5a5a5a5a"] + plant([LD]) + ["step 1", "print v0"])
print(t)
print(">>> alive=%s sig=%s" % (a, s))

print("############ B: sd 1<<50 to imask0, step 1")
t, a, s = session(["a3=0x%x" % A_IMASK0, "t0=0x%x" % (1 << 50)] + plant([SD]) + ["step 1"])
print(t)
print(">>> alive=%s sig=%s" % (a, s))
