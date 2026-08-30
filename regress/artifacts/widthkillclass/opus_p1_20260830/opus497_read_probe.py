#!/usr/bin/env python3
# opus5 seat, #497 pass 1.  Extends the witness into the TWO dimensions it
# never varied: DIRECTION (every witness row is a store) and SITE (1 of 6).
import os, pty, re, select, sys, time

BIN = sys.argv[1]
DUMMY = sys.argv[2] if len(sys.argv) > 2 else "/tmp/dummy497.bin"
if not os.path.exists(DUMMY):
    with open(DUMMY, "wb") as f:
        f.write(b"\0" * 16)

CODE = 0x80001000
SCRATCH_RAM = 0xa0001800
LIVE_VAL = 0x12345678
DE_STATUS_VAL = "0x1e000000"
CRIME_DE_STATUS = 0xb5004000

SITES = [
    ("tlb_a",    0xb5001000, "CRIME_RE_TLB_A"),
    ("tlb_b",    0xb5001200, "CRIME_RE_TLB_B"),
    ("tlb_c",    0xb5001400, "CRIME_RE_TLB_C"),
    ("tex",      0xb5001600, "CRIME_RE_TEX"),
    ("linear_a", 0xb5001700, "CRIME_RE_LINEAR_A"),
    ("linear_b", 0xb5001780, "CRIME_RE_LINEAR_B"),
]

OP_NOP = 0x00000000
OP_B_SELF = 0x1000ffff
OP_SW_R8_R7 = 0xace80000
OP_LW_R2_R1 = 0x8c220000
OP_LD_R2_R1 = 0xdc220000

rows = []
def row(name, got, want, note=""):
    ok = (got == want)
    rows.append((name, ok))
    print("%-18s %-10s %-10s %-44s %s" % (name, str(got), str(want), note,
                                          "ok" if ok else "FAIL"))
    return ok

def session(cmds, settle=1.5, spin=1.0):
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
            alive = False
            break
        if not rd(spin if i == len(cmds) - 1 else 0.25):
            alive = False
            break
    try:
        os.write(fd, b"quit\n"); rd(0.4)
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
    return buf, alive, how

def printed(t, reg):
    m = re.search(r"print\s+%s\s*\r?\n\s*(0x[0-9a-f]+)" % reg, t)
    return m.group(1) if m else "absent"

class Addr(object):
    def __init__(self, base): self.a = base
    def take(self, n):
        got = self.a; self.a += 4 * (n + 2) + 0x20; return got

def run_ops(ops, at):
    put = ["put w 0x%x, 0x%08x" % (at + 4 * i, op) for i, op in enumerate(ops)]
    put += ["put w 0x%x, 0x%08x" % (at + 4 * len(ops), OP_B_SELF),
            "put w 0x%x, 0x%08x" % (at + 4 * len(ops) + 4, OP_NOP)]
    return put + ["pc=0x%x" % at, "step %d" % len(ops)]

print("#497 OPUS5 PASS-1 PROBE -- the READ dimension and all six sites.")
print("binary: %s" % BIN)
print("")
print("%-18s %-10s %-10s %-44s %s" % ("row", "got", "want", "note", ""))

# ---- controls ----
A = Addr(CODE)
t, alive, how = session(["a3=0x%x" % SCRATCH_RAM, "t0=0x%x" % LIVE_VAL]
    + run_ops([OP_SW_R8_R7], A.take(1))
    + ["at=0x%x" % SCRATCH_RAM, "v0=0"]
    + run_ops([OP_LW_R2_R1], A.take(1)) + ["print v0"])
row("live", printed(t, "v0") if alive else "died", "0x%x" % LIVE_VAL,
    "LIVENESS: guest store then load, through RAM")

A = Addr(CODE)
t, alive, how = session(["at=0x%x" % CRIME_DE_STATUS, "v0=0"]
    + run_ops([OP_LW_R2_R1], A.take(1)) + ["print v0"])
row("devsig stat", printed(t, "v0") if alive else "died", DE_STATUS_VAL,
    "DEVSIG: CRIME_DE_STATUS = 0x1e000000; RAM = 0")
print("OPUS497_CONTROL=%s" % ("OK" if all(o for _, o in rows) else "DEAD"))
print("")

# ---- Q: does the WIDTH guard fire on a READ, at every site? ----
for nm, addr, sym in SITES:
    A = Addr(CODE)
    t, alive, how = session(["at=0x%x" % addr, "v0=0"]
        + run_ops([OP_LW_R2_R1], A.take(1)))
    row(nm + " lw kill", how, "exit1", "READ len=4 kills host (dimension untested)")
    row(nm + " lw width", "1" if ("unimplemented len=4 for " + sym) in t else "0",
        "1", "cites the WIDTH guard, not the direction guard")

# ---- Q: is the DIRECTION guard separately live at len=8? ----
A = Addr(CODE)
t, alive, how = session(["at=0x%x" % SITES[0][1], "v0=0"]
    + run_ops([OP_LD_R2_R1], A.take(1)))
row("tlb_a ld kill", how, "exit1", "READ len=8 kills host via DIRECTION guard")
row("tlb_a ld dir", "1" if "TODO: read from CRIME_RE_TLB_A" in t else "0", "1",
    "SEPARABILITY: cites direction guard, width guard passed")

# ---- Q: does the WRITE half kill at the five unwitnessed sites? ----
for nm, addr, sym in SITES[1:]:
    A = Addr(CODE)
    t, alive, how = session(["a3=0x%x" % addr, "t0=0x12345678"]
        + run_ops([OP_SW_R8_R7], A.take(1)))
    row(nm + " sw kill", how, "exit1", "WRITE len=4 kills host (site untested)")
    row(nm + " sw width", "1" if ("unimplemented len=4 for " + sym) in t else "0",
        "1", "attribution at an unwitnessed site")

ok = sum(1 for _, o in rows if o)
print("")
print("OPUS497_PROBE_RESULT=%d/%d" % (ok, len(rows)))
print("OPUS497_DONE")
