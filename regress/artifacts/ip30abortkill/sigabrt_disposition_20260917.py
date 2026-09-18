#!/usr/bin/env python3
"""Did the ip30 abort() actually kill the process, or did I SAMPLE TOO EARLY?

The first run reported `STILL RUNNING' 3 s after the diagnostic printed.  There is no SIGABRT
handler in the tree, so the candidate explanation is that the kernel was still writing a core
dump for a 6 MB binary under WSL and the process sat in the table while it did.

This POLLS the child's disposition for 30 s and prints WHEN it changes, so `died slowly' and
`survived' cannot render the same.  A wrong answer here would mis-rank a HIGH: a host DEATH and
a guest-visible HANG are different defects with different fixes.
"""
import os
import pty
import select
import signal
import time

BIN = "/mnt/c/DocumentNoSnc/CC/GXEMUL/build/gxemul"
DUMMY = "/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/ip30abortkill/ip30_dummy.bin"
CODE = 0x80001000
ADDR = 0xFFFFFFFFAFF10020

pid, fd = pty.fork()
if pid == 0:
    os.execv(BIN, [BIN, "-V", "-x", "-E", "sgi", "-e", "ip30", "-M", "64",
                   "0x%x:" % CODE + DUMMY])
    os._exit(127)

buf = ""


def rd(t):
    global buf
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


rd(2.0)
for c in ["at=0x%x" % ADDR,
          "put w 0x%x, 0x8c220000" % CODE,
          "put w 0x%x, 0x1000ffff" % (CODE + 4),
          "pc=0x%x" % CODE,
          "step 1"]:
    os.write(fd, (c + "\n").encode())
    rd(0.4)

t0 = time.time()
print("stepped at t=0; polling the child for 30 s")
outcome = None
for _ in range(300):
    rd(0.1)
    wpid, status = os.waitpid(pid, os.WNOHANG)
    if wpid == pid:
        dt = time.time() - t0
        if os.WIFSIGNALED(status):
            s = os.WTERMSIG(status)
            outcome = "KILLED BY SIGNAL %d (%s) after %.1f s" % (s, signal.Signals(s).name, dt)
        elif os.WIFEXITED(status):
            outcome = "EXITED code %d after %.1f s" % (os.WEXITSTATUS(status), dt)
        break

if outcome is None:
    outcome = "STILL RUNNING after %.1f s -- it really did survive" % (time.time() - t0)
    try:
        os.kill(pid, signal.SIGKILL)
        os.waitpid(pid, 0)
    except OSError:
        pass

print("OUTCOME: %s" % outcome)
print("diagnostic printed: %s" % ("YES" if "IP30 legacy interrupt rewrite" in buf else "NO"))
print("prompt returned after step: %s"
      % ("YES" if buf.rstrip().endswith("GXemul>") or "GXemul>" in buf.split("step 1")[-1] else "NO"))
print("---- last 300 bytes ----")
print(buf[-300:])
try:
    os.close(fd)
except OSError:
    pass
