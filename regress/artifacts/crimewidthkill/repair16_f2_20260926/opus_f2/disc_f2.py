#!/usr/bin/env python3
"""disc_f2.py BIN -- one accepted `sw 0x0001' at CRIME_CONTROL (+0x08), once FREE-RUNNING and once STEPPED; counts the
CONTROL arm's residue text in each.  The probe's own session() (with its <RUN> branch) and encodings, copied verbatim
from crime_width_probe.table16.py (5f770991).  Prints two lines, then DISC_F2_DONE."""
import os, pty, re, select, signal, sys, time

BIN = sys.argv[1]
DUMMY = "/tmp/dummy_crimep.bin"
if not os.path.exists(DUMMY):
    with open(DUMMY, "wb") as f:
        f.write(b"\0" * 16)
CODE = 0x80001000
CRIME = 0xb4000000
R = {"a3": 7, "t0": 8}
OP_SW, OP_B_SELF, OP_NOP = 0x2b, 0x1000ffff, 0


def session(cmds, settle=1.5, spin=1.2):
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

    rd(settle)
    for i, c in enumerate(cmds):
        try:
            if c == "<RUN>":
                os.write(fd, b"continue\n")
                ok = rd(2.0)
                os.write(fd, b"\x03")
                ok = ok and rd(1.5)
            else:
                os.write(fd, (c + "\n").encode("latin-1"))
                ok = rd(spin if i == len(cmds) - 1 else 0.25)
        except OSError:
            break
        if not ok:
            break
    eof = True
    try:
        os.write(fd, b"quit\n")
        eof = not rd(10.0)
    except OSError:
        pass
    if not eof:
        try:
            os.kill(pid, signal.SIGKILL)
        except OSError:
            pass
    try:
        os.close(fd)
    except OSError:
        pass
    how = "nostatus"
    try:
        _, stat = os.waitpid(pid, 0)
        how = ("sig%d" % os.WTERMSIG(stat)) if os.WIFSIGNALED(stat) else ("exit%d" % os.WEXITSTATUS(stat))
    except OSError:
        pass
    return buf.replace("\r", ""), (eof and how == "exit0")


sw = (OP_SW << 26) | (R["a3"] << 21) | (R["t0"] << 16)
assert sw == 0xace80000
base = ["a3=0x%x" % (CRIME + 8), "t0=0x1",
        "put w 0x%x, 0x%08x" % (CODE, sw), "put w 0x%x, 0x%08x" % (CODE + 4, OP_NOP),
        "put w 0x%x, 0x%08x" % (CODE + 8, OP_B_SELF), "put w 0x%x, 0x%08x" % (CODE + 12, OP_NOP), "pc=0x%x" % CODE]
print("DISC_F2 binary=%s" % BIN)
t, clean = session(base + ["<RUN>"])
ran = t.split("continue", 1)[1] if "continue" in t else ""
print("free-running sw 0x0001 +0x08: CONTROL texts after `continue' = %s (clean=%s)"
      % (ran.count("CRIME_CONTROL: unimplemented") if clean else "unclean", clean))
t, clean = session(base + ["step 1"])
print("stepped      sw 0x0001 +0x08: CONTROL texts               = %s (clean=%s)"
      % (t.count("CRIME_CONTROL: unimplemented") if clean else "unclean", clean))
print("DISC_F2_DONE")
