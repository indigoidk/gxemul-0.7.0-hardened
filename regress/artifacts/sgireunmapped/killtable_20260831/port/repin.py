#!/usr/bin/env python3
#
#  THE ORACLE-CORRECTION ORDER PROOF for sgi_re_width_probe.py's `other kill'.
#
#  That row is SHIPPED and GATE-WIRED (gate_arm.sh:1131) and it asserts
#  `how == "exit1"' -- the catch-all still ends the host.  #499 removes that
#  kill, so the row goes RED on the fix: MEASURED 34/35, in sib.out.
#
#  The carrier's oracle-correction rule says the re-pin must come FIRST and be
#  measured RED on the COMMITTED build under the NEW expectation, otherwise the
#  re-pin is observationally identical to fitting the test to the binary.  This
#  file IS that measurement.  It implements the new oracle ONLY -- it does not
#  edit the shipped probe -- and reports it against base and against fix.
#
#  The new oracle is not invented either: the row's own comment already
#  prescribes it, having been filed as `otherkilldeath' --
#      "DEATH-ONLY.  This row observes THAT the catch-all kills, never WHICH
#       kill it is ... the fix is the ok_txt test the siblings already carry."
#
import os
import pty
import re
import select
import sys
import time

BIN = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "?"
DUMMY = "/tmp/dummy497.bin"
if not os.path.exists(DUMMY):
    with open(DUMMY, "wb") as f:
        f.write(b"\0" * 16)

CODE = 0x80001000
OUTSIDE = 0xb5001800              # past LINEAR_B -> the catch-all
OP_NOP = 0x00000000
OP_B_SELF = 0x1000ffff
OP_SW_T0_A3 = 0xace80000


def session(cmds, settle=1.5, spin=1.2):
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN, [BIN, "-V", "-x", "-E", "sgi", "-e", "ip32", "-M", "64",
                       "0x80001000:" + DUMMY])
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
                if not d:
                    return False
                buf += d.decode("latin-1", "replace")
            except OSError:
                return False
        return True

    alive = rd(settle)
    for i, c in enumerate(cmds):
        try:
            os.write(fd, (c + "\n").encode("latin-1"))
        except OSError:
            break
        if not rd(spin if i == len(cmds) - 1 else 0.25):
            break
    try:
        os.write(fd, b"quit\n")
        rd(0.4)
    except OSError:
        pass
    try:
        os.close(fd)
    except OSError:
        pass
    how = "nostatus"
    try:
        _, stat = os.waitpid(pid, 0)
        if os.WIFSIGNALED(stat):
            how = "sig%d" % os.WTERMSIG(stat)
        elif os.WIFEXITED(stat):
            how = "exit%d" % os.WEXITSTATUS(stat)
    except OSError:
        pass
    return buf.replace("\r", ""), how


at = CODE
cmds = (["a3=0x%x" % OUTSIDE, "t0=0x12345678"]
        + ["put w 0x%x, 0x%08x" % (at, OP_SW_T0_A3),
           "put w 0x%x, 0x%08x" % (at + 4, OP_B_SELF),
           "put w 0x%x, 0x%08x" % (at + 8, OP_NOP),
           "pc=0x%x" % at, "step 1"])
t, how = session(cmds)

ok_txt = ("unimplemented write to address" in t) and ("-- declined." in t)
got = how + ("+txt" if ok_txt else "-txt")

print("  %-14s %-16s got=%-14s want=%-14s %s"
      % ("other decl", LABEL, got, "exit0+txt", "ok" if got == "exit0+txt" else "FAIL"))
print("  (the SHIPPED row's old oracle would read: how=%s want=exit1 -> %s)"
      % (how, "ok" if how == "exit1" else "FAIL"))
print("REPIN_DONE")
