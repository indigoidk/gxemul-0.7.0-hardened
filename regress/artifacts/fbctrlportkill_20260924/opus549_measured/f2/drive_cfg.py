#!/usr/bin/env python3
"""Exploratory driver: start gxemul -V @<config> on a pty, run debugger commands, print the whole transcript.
usage: drive_cfg.py <gxemul> <n_machines> <serial_nr or -> <cmd>..."""
import os
import pty
import select
import sys
import time

BIN, NM, SER = sys.argv[1], int(sys.argv[2]), sys.argv[3]
CMDS = sys.argv[4:]
stub = "/tmp/gx_fbctrl549f2d_%d.bin" % os.getpid()
cfg = "/tmp/gx_fbctrl549f2d_%d.cfg" % os.getpid()
with open(stub, "wb") as f:
    f.write(b"\x00\x00\x00\x00")
with open(cfg, "w") as f:
    for i in range(NM):
        f.write('machine(\n\tname("m%d")\n\ttype("testmips")\n\tmemory(64)\n' % i)
        if SER != "-":
            f.write("\tserial_nr(%s)\n" % SER)
        f.write('\tload("0x%x:%s")\n)\n' % (0xffffffff80100000, stub))
print("----- config -----")
print(open(cfg).read())
pid, fd = pty.fork()
if pid == 0:
    os.execvp(BIN, [BIN, "-V", "@" + cfg])
    os._exit(127)
buf = ""


def rd(t):
    global buf
    end = time.time() + t
    while time.time() < end:
        r, _, _ = select.select([fd], [], [], 0.2)
        if fd in r:
            try:
                d = os.read(fd, 65536)
            except OSError:
                return False
            if not d:
                return False
            buf += d.decode("latin1", "replace")
            if buf.rstrip().endswith("GXemul>"):
                return True
    return True


rd(20)
for c in CMDS:
    os.write(fd, (c + "\n").encode())
    time.sleep(0.2)
    rd(5)
os.write(fd, b"quit\n")
rd(5)
try:
    os.close(fd)
except OSError:
    pass
try:
    _, st = os.waitpid(pid, 0)
    print("----- exit status", os.WEXITSTATUS(st) if os.WIFEXITED(st) else st)
except OSError:
    pass
print("----- transcript -----")
print(buf)
for p in (stub, cfg):
    try:
        os.unlink(p)
    except OSError:
        pass
