#!/usr/bin/env python3
# Does the proposed latch actually bound the flood, and do PER-SITE bits earn
# their keep?  Both need TWO accesses in ONE session -- a dimension no
# one-access-per-session row set can reach.
import os, pty, re, select, sys, time
BIN = sys.argv[1]
DUMMY = "/tmp/dummy497.bin"
CODE = 0x80001000
OP_NOP = 0x00000000
OP_B_SELF = 0x1000ffff
OP_SW_R8_R7 = 0xace80000

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
            if not r: continue
            try:
                d = os.read(fd, 65536)
                if not d: return False
                buf += d.decode("latin-1", "replace")
            except OSError: return False
        return True
    rd(settle)
    for i, c in enumerate(cmds):
        try: os.write(fd, (c + "\n").encode("latin-1"))
        except OSError: break
        rd(spin if i == len(cmds) - 1 else 0.25)
    try: os.write(fd, b"quit\n"); rd(0.4)
    except OSError: pass
    try: os.close(fd)
    except OSError: pass
    try: os.waitpid(pid, 0)
    except OSError: pass
    return buf

class Addr(object):
    def __init__(self, b): self.a = b
    def take(self, n):
        g = self.a; self.a += 4*(n+2) + 0x20; return g

def run_ops(ops, at):
    put = ["put w 0x%x, 0x%08x" % (at+4*i, o) for i, o in enumerate(ops)]
    put += ["put w 0x%x, 0x%08x" % (at+4*len(ops), OP_B_SELF),
            "put w 0x%x, 0x%08x" % (at+4*len(ops)+4, OP_NOP)]
    return put + ["pc=0x%x" % at, "step %d" % len(ops)]

rows = []
def row(n, got, want, note):
    ok = got == want
    rows.append(ok)
    print("%-20s %-6s %-6s %-46s %s" % (n, got, want, note, "ok" if ok else "FAIL"))

print("#497 OPUS5 LATCH PROBE -- two accesses in ONE session.")
print("%-20s %-6s %-6s %-46s" % ("row","got","want","note"))

# (1) THREE declined stores at ONE site -> exactly ONE line?
A = Addr(CODE)
cmds = ["a3=0xb5001000", "t0=0x12345678"]
for _ in range(3):
    cmds += run_ops([OP_SW_R8_R7], A.take(1))
t = session(cmds)
n = t.count("unimplemented len=4 for CRIME_RE_TLB_A")
row("flood 3x1site", str(n), "1", "LATCH: 3 declined stores -> exactly 1 line")

# (2) TWO SITES in one session -> BOTH must announce (per-site bits)
A = Addr(CODE)
cmds = (["a3=0xb5001000", "t0=0x12345678"] + run_ops([OP_SW_R8_R7], A.take(1))
        + ["a3=0xb5001200"] + run_ops([OP_SW_R8_R7], A.take(1)))
t = session(cmds)
a = t.count("unimplemented len=4 for CRIME_RE_TLB_A")
b = t.count("unimplemented len=4 for CRIME_RE_TLB_B")
row("persite a+b", "%d+%d" % (a, b), "1+1", "PER-SITE BITS: both windows announce")

print("")
print("OPUS497_LATCH_RESULT=%d/%d" % (sum(rows), len(rows)))
print("LATCH_DONE")
