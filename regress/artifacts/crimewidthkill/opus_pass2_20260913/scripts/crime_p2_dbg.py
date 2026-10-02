#!/usr/bin/env python3
"""crime_p2_dbg.py BIN [LABEL] -- #529 pass-2 Opus seat: does a fall-through into the switch's DEFAULT arm leave a host
trace while single-stepping?  One refused sb at +0x1f (the detector's own `sb' cell) and one refused lb at +0x7;
prints every transcript line mentioning `crime:'.  Sentinel: P2DBG_DONE"""
import os, pty, select, sys, time

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


print("CRIME P2 DBG PROBE  binary=%s label=%s" % (BIN, LABEL))
t = session(["a3=0xb400001f", "t0=0xff", "put w 0x80001000, 0xa0e80000", "put w 0x80001004, 0x1000ffff",
             "put w 0x80001008, 0", "pc=0x80001000", "step 1",
             "at=0xb4000007", "put w 0x80001100, 0x80220000", "put w 0x80001104, 0x1000ffff",
             "put w 0x80001108, 0", "pc=0x80001100", "step 1"])
for l in t.split("\n"):
    if "crime:" in l:
        print("  " + l.strip())
print("P2DBG_DONE")
