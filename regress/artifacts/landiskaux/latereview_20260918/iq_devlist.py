#!/usr/bin/env python3
"""iq_devlist.py <gxemul> [machine args...] -- construct a machine under -V (no guest
instruction runs) and print its wdc / wdc_altstatus rows from `device list`."""
import os, pty, re, select, sys, time
BIN = sys.argv[1]; args = sys.argv[2:]
pid, fd = pty.fork()
if pid == 0:
    os.execv(BIN, [BIN, "-V"] + args); os._exit(127)
buf = b""
def rd(t):
    global buf
    end = time.time() + t
    while time.time() < end:
        r, _, _ = select.select([fd], [], [], 0.25)
        if r:
            try:
                d = os.read(fd, 65536)
            except OSError:
                return
            if not d:
                return
            buf += d
rd(5.0)
try:
    os.write(fd, b"device list\n"); rd(2.0); os.write(fd, b"quit\n"); rd(0.8)
except OSError:
    pass
try:
    os.close(fd); os.waitpid(pid, 0)
except OSError:
    pass
t = buf.decode("latin-1")
for l in t.splitlines():
    if "wdc" in l or "ERROR" in l or "rror" in l or "No " in l[:4]:
        print("  " + l.strip())
print("DEVLIST_DONE bytes=%d" % len(buf))
