#!/usr/bin/env python3
"""crime_p2_text.py BIN [LABEL] -- #529 pass-2 Opus seat: the announce TEXT at offsets the detector never uses.
One refused lb at +0x48 (inside the 0x280-byte map, default arm) per session; prints the announce line verbatim.
Sentinel: P2TXT_DONE"""
import os, pty, re, select, sys, time

BIN = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "?"
DUMMY = "/tmp/dummy_crimep.bin"
if not os.path.exists(DUMMY):
    open(DUMMY, "wb").write(b"\0" * 16)


def session(cmds):
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

    rd(1.5)
    for c in cmds:
        os.write(fd, (c + "\n").encode())
        rd(0.3)
    rd(1.0)
    try:
        os.write(fd, b"quit\n")
        rd(5.0)
    except OSError:
        pass
    os.close(fd)
    os.waitpid(pid, 0)
    return buf.replace("\r", "")


print("CRIME P2 TEXT PROBE  binary=%s label=%s" % (BIN, LABEL))
for off in (0x48, 0x208):
    t = session(["at=0x%x" % (0xb4000000 + off), "put w 0x80001000, 0x80220000", "put w 0x80001004, 0x1000ffff",
                 "put w 0x80001008, 0", "pc=0x80001000", "step 1"])
    lines = [l for l in t.split("\n") if "declined" in l]
    print("lb +0x%x -> %s" % (off, lines if lines else "NO ANNOUNCE"))
print("P2TXT_DONE")
