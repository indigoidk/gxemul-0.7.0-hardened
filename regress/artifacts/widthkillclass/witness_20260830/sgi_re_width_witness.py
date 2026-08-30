#!/usr/bin/env python3
"""
#497 WITNESS -- SGI O2 dev_sgi_re.c guest access width host kill.

Rung 3. Real guest MIPS instructions through real address decode and real memory_rw
on an UNMODIFIED `-E sgi -e ip32` machine description. Nothing is #included and
nothing is called directly.

WHAT THIS WITNESSES:
src/devices/dev_sgi_re.c line 231 (CRIME_RE_TLB_A):
    if (len != 8) {
        fatal("TODO: unimplemented len=%i for CRIME_RE_TLB_A\n", len);
        exit(1);
    }
A guest executing a 4-byte (sw/lw), 2-byte (sh/lh), or 1-byte (sb/lb) access
to CRIME_RE_TLB_A (base 0x15001000) causes the host emulator to call fatal()
and exit(1), killing the emulator process.

Sentinel: SGIRE_WIDTH_WITNESS_DONE
"""

import os
import pty
import re
import select
import sys
import time

if len(sys.argv) < 2:
    sys.stderr.write("usage: sgi_re_width_witness.py <gxemul> [kernel/dummy]\n")
    sys.exit(2)

BIN = sys.argv[1]
DUMMY = sys.argv[2] if len(sys.argv) > 2 else "/tmp/dummy.bin"

if not os.path.exists(DUMMY):
    with open(DUMMY, "wb") as f:
        f.write(b"\0" * 16)

CODE = 0x80001000
SCRATCH_RAM = 0xa0001800

CRIME_RE_TLB_A = 0xb5001000
CRIME_DE_MODE_SRC = 0xb5002000
CRIME_DE_STATUS = 0xb5004000

LIVE_VAL = 0x12345678
DE_STATUS_VAL = "0x1e000000"

OP_NOP = 0x00000000
OP_B_SELF = 0x1000ffff

OP_SW_R8_R7 = 0xace80000
OP_SH_R8_R7 = 0xa4e80000
OP_SB_R8_R7 = 0xa0e80000
OP_SD_R8_R7 = 0xfce80000
OP_LW_R2_R1 = 0x8c220000
OP_LD_R2_R1 = 0xdc220000

rows = []

def row(name, got, want, note=""):
    ok = (got == want)
    rows.append((name, ok))
    print("%-14s %-12s %-12s %-46s %s" % (name, str(got), str(want), note,
                                          "ok" if ok else "FAIL"))
    return ok

def session(cmds, settle=1.5, spin=1.0):
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
    m = re.search(r"print\s+%s\s*\r?\n\s*(0x[0-9a-f]+)" % reg, t)
    return m.group(1) if m else "absent"

class Addr(object):
    def __init__(self, base):
        self.a = base
    def take(self, n_ops):
        got = self.a
        self.a += 4 * (n_ops + 2) + 0x20
        return got

def run_ops(ops, at):
    put = ["put w 0x%x, 0x%08x" % (at + 4 * i, op) for i, op in enumerate(ops)]
    put += ["put w 0x%x, 0x%08x" % (at + 4 * len(ops), OP_B_SELF),
            "put w 0x%x, 0x%08x" % (at + 4 * len(ops) + 4, OP_NOP)]
    return put + ["pc=0x%x" % at, "step %d" % len(ops)]

print("#497 SGI_RE_WIDTH WITNESS -- rung 3, unmodified -E sgi -e ip32.")
print("binary: %s" % BIN)
print("")
print("%-14s %-12s %-12s %-46s %s" % ("row", "got", "want", "note", ""))

# ------------------------------------------------------------------ MANDATORY CONTROLS
A = Addr(CODE)
t, alive, how = session([
    "a3=0x%x" % SCRATCH_RAM,
    "t0=0x%x" % LIVE_VAL,
] + run_ops([OP_SW_R8_R7], A.take(1)) + [
    "at=0x%x" % SCRATCH_RAM,
    "v0=0",
] + run_ops([OP_LW_R2_R1], A.take(1)) + ["print v0"])
row("live", printed(t, "v0") if alive else "died", "0x%x" % LIVE_VAL,
    "LIVENESS: guest store then guest load, through RAM")

A = Addr(CODE)
t, alive, how = session([
    "at=0x%x" % CRIME_DE_STATUS,
    "v0=0",
] + run_ops([OP_LW_R2_R1], A.take(1)) + ["print v0"])
row("devsig stat", printed(t, "v0") if alive else "died", DE_STATUS_VAL,
    "DEVSIG: fresh CRIME_DE_STATUS = 0x1e000000; RAM = 0")

A = Addr(CODE)
t, alive, how = session([
    "a3=0x%x" % CRIME_DE_MODE_SRC,
    "t0=0x34",
] + run_ops([OP_SW_R8_R7], A.take(1)) + [
    "at=0x%x" % CRIME_DE_MODE_SRC,
    "v0=0",
] + run_ops([OP_LW_R2_R1], A.take(1)) + ["print v0"])
row("devsig mode", printed(t, "v0") if alive else "died", "0x34",
    "DEVSIG: store 0x34 to DE_MODE_SRC reads back 0x34")

A = Addr(CODE)
t, alive, how = session([
    "a3=0x%x" % CRIME_RE_TLB_A,
    "t0=0x12345678",
] + run_ops([OP_SD_R8_R7], A.take(1)))
row("accept sd", how, "exit0",
    "ACCEPT: legal 64-bit store (len=8) survives")

print("SGIRE_CONTROL=%s"
      % ("OK" if rows and all(ok for _, ok in rows) else "DEAD"))
print("")

# ------------------------------------------------------------------ DEFECT SITES (WIDTH KILLS)
A = Addr(CODE)
t, alive, how = session([
    "a3=0x%x" % CRIME_RE_TLB_A,
    "t0=0x12345678",
] + run_ops([OP_SW_R8_R7], A.take(1)))
row("tlb_a sw kill", how, "exit1",
    "32-bit store (sw, len=4) kills host emulator")
row("tlb_a sw says", "1" if "unimplemented len=4 for CRIME_RE_TLB_A" in t else "0", "1",
    "ATTRIBUTION: diagnostic cites len=4 for CRIME_RE_TLB_A")

A = Addr(CODE)
t, alive, how = session([
    "a3=0x%x" % CRIME_RE_TLB_A,
    "t0=0x1234",
] + run_ops([OP_SH_R8_R7], A.take(1)))
row("tlb_a sh kill", how, "exit1",
    "16-bit store (sh, len=2) kills host emulator")
row("tlb_a sh says", "1" if "unimplemented len=2 for CRIME_RE_TLB_A" in t else "0", "1",
    "ATTRIBUTION: diagnostic cites len=2 for CRIME_RE_TLB_A")

A = Addr(CODE)
t, alive, how = session([
    "a3=0x%x" % CRIME_RE_TLB_A,
    "t0=0x12",
] + run_ops([OP_SB_R8_R7], A.take(1)))
row("tlb_a sb kill", how, "exit1",
    "8-bit store (sb, len=1) kills host emulator")
row("tlb_a sb says", "1" if "unimplemented len=1 for CRIME_RE_TLB_A" in t else "0", "1",
    "ATTRIBUTION: diagnostic cites len=1 for CRIME_RE_TLB_A")

ok = sum(1 for _, o in rows if o)
print("")
print("SGIRE_WIDTH_WITNESS_RESULT=%d/%d" % (ok, len(rows)))
print("SGIRE_WIDTH_WITNESS_DONE")
sys.exit(0 if ok == len(rows) else 1)
