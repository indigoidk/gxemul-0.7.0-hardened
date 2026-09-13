#!/usr/bin/env python3
"""
MAPLE_DMAADDR rung-3 cold-debugger witness.

Exercises guest reads and writes of MAPLE_DMAADDR (0xa05f6c04) on unmodified
machine -E dreamcast, using real SH4 instructions (mov.l) through address decode.
"""

import os
import pty
import re
import select
import sys
import time

if len(sys.argv) < 2:
    sys.stderr.write("usage: agy_maple_witness_20260912.py <gxemul> [kernel]\n")
    sys.exit(2)

BIN = sys.argv[1]
KERNEL = sys.argv[2] if len(sys.argv) > 2 else "/mnt/c/DocumentNoSnc/CC/GXEMUL/_images/openbsd76-landisk-bsd.rd"

MAPLE_BASE = 0xa05f6c00
MAPLE_DMAADDR = 0xa05f6c04
MAPLE_ENABLE = 0xa05f6c14
MAPLE_STATE = 0xa05f6c18
MAPLE_SPEED = 0xa05f6c80

CODE = 0x8c001000
SCRATCH = 0x8c001800
MARKER = 0x8c001f04

BRA_SELF = 0xaffe
NOP = 0x0009
SEED = 0xdead

def run(ops, at):
    put = ["put h 0x%x, 0x%04x" % (at + 2 * i, op) for i, op in enumerate(ops)]
    put += ["put h 0x%x, 0x%04x" % (at + 2 * len(ops), BRA_SELF),
            "put h 0x%x, 0x%04x" % (at + 2 * len(ops) + 2, NOP)]
    return put + ["pc=0x%x" % at, "step %d" % len(ops)]

def load32(reg, at, dest=2):
    # mov.l @r1, r{dest}
    return ["r1=0x%x" % reg, "r%d=0x%x" % (dest, SEED)] + \
           run([0x6002 | (1 << 4) | (dest << 8)], at) + \
           ["print r%d" % dest]

def store32(reg, val, at):
    # mov.l r2, @r1
    return ["r1=0x%x" % reg, "r2=0x%08x" % val] + \
           run([0x2122], at)

def session(cmds, settle=2.5, spin=1.2):
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN, [BIN, "-V", "-x", "-E", "dreamcast", "-M", "64", KERNEL])
        os._exit(127)
    buf = ""

    def rd(t):
        nonlocal buf
        end = time.time() + t
        while time.time() < end:
            r, _, _ = select.select([fd], [], [], 0.20)
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

    alive = rd(settle)
    for i, c in enumerate(cmds):
        try:
            os.write(fd, (c + "\n").encode("latin-1"))
        except OSError:
            alive = False
            break
        if not rd(spin if i == len(cmds) - 1 else 0.20):
            alive = False
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
    return buf, alive, how

def printed(t, reg):
    m = re.findall(r"print\s+%s\s*\r?\n\s*(0x[0-9a-f]+)" % reg, t)
    return m[-1] if m else "absent"

def hex_norm(v):
    if isinstance(v, int):
        return "0x%x" % v
    if isinstance(v, str) and v.startswith("0x"):
        try:
            return "0x%x" % int(v, 16)
        except ValueError:
            return v
    return str(v)

rows = []

def row(name, got, want):
    g = hex_norm(got)
    w = hex_norm(want)
    ok = (g == w)
    rows.append((name, ok))
    print("%-18s %-14s %-14s %s" % (name, g, w, "ok" if ok else "FAIL"))
    sys.stdout.flush()
    return ok

print("MAPLE_DMAADDR WITNESS -- rung 3, unmodified -E dreamcast")
print("binary: %s" % BIN)
print("")
sys.stdout.flush()

# 1. Liveness control (RAM)
t, alive, how = session(["put w 0x8c001800, 0x12345678"] + load32(0x8c001800, CODE))
row("ctrl live", printed(t, "r2"), 0x12345678)

# 2. Device signature control: SH4 IPRD
t, alive, how = session(load32(0xffd00010, CODE))
g = printed(t, "r2")
val = ("0x%x" % (int(g, 16) & 0xffff)) if g.startswith("0x") else g
row("ctrl devsig sh4", val, 0xda74)

# 3. Device signature control: MAPLE_SPEED masks/shifts (0x12345678 -> 0x12340000)
t, alive, how = session(store32(MAPLE_SPEED, 0x12345678, CODE) + load32(MAPLE_SPEED, CODE + 0x20))
row("ctrl devsig maple", printed(t, "r2"), 0x12340000)

# 4. Subject: initial read from fresh device
t, alive, how = session(load32(MAPLE_DMAADDR, CODE))
row("initial zero", printed(t, "r2"), 0x0)

# 5. Subject: write value A (nonzero high bit, nonzero low 5 bits)
t_a, alive_a, how_a = session(store32(MAPLE_DMAADDR, 0x8c012345, CODE) + load32(MAPLE_DMAADDR, CODE + 0x20))
row("read val_a", printed(t_a, "r2"), 0x8c012345)

# 6. Subject: write value B (all five low bits set: 0x1f)
t_b, alive_b, how_b = session(store32(MAPLE_DMAADDR, 0x0c00001f, CODE) + load32(MAPLE_DMAADDR, CODE + 0x20))
row("read val_b", printed(t_b, "r2"), 0x0c00001f)

# 7. Subject: second write replaces what read reports
t_rep, alive_rep, how_rep = session(
    store32(MAPLE_DMAADDR, 0x8c012345, CODE) +
    store32(MAPLE_DMAADDR, 0x13579bdf, CODE + 0x20) +
    load32(MAPLE_DMAADDR, CODE + 0x40)
)
row("write replace", printed(t_rep, "r2"), 0x13579bdf)

# 8. Subject: unaligned address alignment refusal independent observation
# Writing 0x13579bdf, enable=1, state=1 triggers refusal log naming 0x13579bdf, then readback
cmds_ref = store32(MAPLE_DMAADDR, 0x13579bdf, CODE) + \
           store32(MAPLE_ENABLE, 1, CODE + 0x20) + \
           store32(MAPLE_STATE, 1, CODE + 0x40) + \
           load32(MAPLE_DMAADDR, CODE + 0x60)
t_ref, alive_ref, how_ref = session(cmds_ref)
row("align refusal", printed(t_ref, "r2"), 0x13579bdf)

# 9. Subject: process survival and marker execution after read
# Guest reads MAPLE_DMAADDR into r2, then writes marker 0x55aa55aa to RAM MARKER (0x8c001f04)
# Then reads MARKER from RAM into r5
# mov.l @r1, r2 is 0x6212; mov.l r3, @r4 is 0x2432
ops_survive = [
    0x6212,  # mov.l @r1, r2 (r1 = MAPLE_DMAADDR)
    0x2432,  # mov.l r3, @r4 (r3 = 0x55aa55aa, r4 = MARKER)
]
cmds_survive = [
    "put w 0x%x, 0x0" % MARKER,
    "r1=0x%x" % MAPLE_DMAADDR,
    "r2=0x%x" % SEED,
    "r3=0x55aa55aa",
    "r4=0x%x" % MARKER,
] + run(ops_survive, CODE) + load32(MARKER, CODE + 0x20, dest=5)
t_surv, alive_surv, how_surv = session(cmds_survive)
row("marker survive", printed(t_surv, "r5"), 0x55aa55aa)

# 10. Subject: read quiet (TODO diagnostic absent from read transcript)
todo_present = ("TODO: read from dmaaddr" in t_a) or ("TODO: read from dmaaddr" in t_surv)
row("read quiet", "found" if todo_present else "absent", "absent")

# 11. Subject: exit status is clean exit0
row("exit status", how_surv, "exit0")

# 12. Trailing liveness control
t_end, alive_end, how_end = session(["put w 0x8c001800, 0xdeadbeef"] + load32(0x8c001800, CODE))
row("ctrl zlive", printed(t_end, "r2"), 0xdeadbeef)

ok_count = sum(1 for _, o in rows if o)
total_count = len(rows)
print("")
print("SCORE %d/%d" % (ok_count, total_count))
print("MAPLE_WITNESS_DONE")
sys.stdout.flush()
sys.exit(0 if ok_count == total_count else 1)
