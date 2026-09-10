#!/usr/bin/env python3
#
#  TLB REACHABILITY CONTROL for sgimtedepth4dead / rule question 7g-1.
#
#  NOT a proposed detector row and NOT the shipped instrument.  It answers ONE question the
#  shipped 14-row probe cannot ask, because every one of its rows drives dst_tlb == MTE_TLB_A:
#
#      Is the `#509' repair OBSERVABLE at dst_tlb == MTE_TLB_B and MTE_TLB_C -- i.e. are the
#      two unrowed case labels REACHABLE by an ordinary guest, and does the CI-vs-RGBA
#      difference appear there?
#
#  Reachability of a joint cell is derived from the WRITERS of each lvalue (carrier rule).  The
#  writer of re_tlb_b is dev_sgi_re.c's `relative_addr >= CRIME_RE_TLB_B' arm, which is the
#  exact mirror of the TLB_A arm this probe's parent already drives.  So the same instruction
#  sequence reaches B and C with two constants changed.
#
#  Oracle: dest[0] of a tiled 32-bit FILL with bg = 0x11223344.
#      0x11 = RGBA PUT ran   (bg >> 24)      -- the repaired arm
#      0x44 = CI PUT ran     ((uint8_t)bg)   -- the #509 defect, 3 bytes of host stack follow
#      0x99 = the paint      -- the transfer did nothing (an INVALID cell, not a result)
#
#  Usage: tlb_reach_control.py <gxemul-binary> <label>
import os, sys, pty, select, time, re

BIN   = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "?"

OP_SW_T0_A3 = 0xace80000
OP_SD_T0_A3 = 0xfce80000
OP_LW_V0_AT = 0x8c220000
OP_B_SELF   = 0x1000ffff
OP_NOP      = 0x00000000

CODE     = 0x80001000
SENTINEL = 0xdeadbeef
BG_VAL   = 0x11223344
CI_TOP   = 0x44
RGBA_TOP = 0x11
PAINT    = 0x99999999

MTE_MODE       = 0xb5003000
MTE_BG         = 0xb5003018
MTE_DST0       = 0xb5003030
MTE_DST1_START = 0xb5003838
MODE_D32       = 0x200

#  CRIME_RE_TLB_A/B/C = 0x1000/0x1200/0x1400; MTE_DST_TLB_SHIFT = 2.
TLBS = [("A", 0xb5001000, 0), ("B", 0xb5001200, 1), ("C", 0xb5001400, 2)]
TILE = 0x8002                                  # bit 15 is the VALID bit
DEST = 0xa0000000 + ((TILE << 16) & ~0x80000000)

DUMMY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sgi_mte_dummy.bin")
if not os.path.exists(DUMMY):
    with open(DUMMY, "wb") as f:
        f.write(b"\0" * 8)

def session(cmds, settle=1.5, spin=1.8):
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN, [BIN, "-V", "-x", "-E", "sgi", "-e", "ip32", "-M", "64",
                       "0x%x:" % CODE + DUMMY])
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
            alive = False; break
        if not rd(spin if i == len(cmds) - 1 else 0.22):
            alive = False; break
    try:
        os.write(fd, b"quit\n"); rd(0.4)
    except OSError:
        pass
    try:
        os.close(fd)
    except OSError:
        pass
    return buf.replace("\r", ""), alive

def printed(t, reg):
    m = re.search(r"print\s+%s\s*\n\s*(0x[0-9a-f]+)" % reg, t)
    return "absent" if not m else "0x%x" % int(m.group(1), 16)

class Addr(object):
    def __init__(self, base): self.a = base
    def take(self, n):
        got = self.a; self.a += 4 * (n + 2) + 0x20; return got

def run_ops(ops, at):
    put = ["put w 0x%x, 0x%08x" % (at + 4 * i, op) for i, op in enumerate(ops)]
    put += ["put w 0x%x, 0x%08x" % (at + 4 * len(ops), OP_B_SELF),
            "put w 0x%x, 0x%08x" % (at + 4 * len(ops) + 4, OP_NOP)]
    return put + ["pc=0x%x" % at, "step %d" % len(ops)]

def store(A, addr, val, op=OP_SW_T0_A3):
    return ["a3=0x%x" % addr, "t0=0x%x" % val] + run_ops([op], A.take(1))

def load(A, addr):
    return ["at=0x%x" % addr, "v0=0x%x" % SENTINEL] + run_ops([OP_LW_V0_AT], A.take(1))

def byte0(s):
    if not s.startswith("0x"):
        return s
    return "0x%02x" % ((int(s, 16) >> 24) & 0xff)

print("tlb_reach_control -- binary=%s label=%s machine=sgi/ip32" % (BIN, LABEL))
print("%-10s %-8s %-10s %s" % ("dst_tlb", "dest[0]", "arm", "note"))

results = {}
for name, tlbreg, tlbnr in TLBS:
    A = Addr(CODE)
    mode = MODE_D32 | (tlbnr << 2)
    c  = store(A, tlbreg, TILE << 48, op=OP_SD_T0_A3)   # re_tlb_<x>[0] = 0x8002
    c += store(A, DEST, PAINT)                          # pre-paint, so a no-op is visible
    c += store(A, MTE_MODE, mode)
    c += store(A, MTE_BG,   BG_VAL)
    c += store(A, MTE_DST0, 0)
    c += store(A, MTE_DST1_START, 0)                    # START fires do_mte_transfer()
    c += load(A, DEST) + ["print v0"]
    t, alive = session(c)
    got = byte0(printed(t, "v0")) if alive else "died"
    if got == "0x%02x" % RGBA_TOP:
        arm = "RGBA"; note = "the #509 repair FIRED here"
    elif got == "0x%02x" % CI_TOP:
        arm = "CI"; note = "*** the #509 DEFECT is LIVE here (3 bytes of host stack follow) ***"
    elif got == "0x%02x" % 0x99:
        arm = "NOTHING"; note = "paint survived -- transfer did not run; cell is INVALID, not a result"
    else:
        arm = "?"; note = "neither RGBA nor CI nor paint -- INVALID cell"
    results[name] = arm
    print("%-10s %-8s %-10s %s" % ("MTE_TLB_" + name, got, arm, note))

print()
print("TLBREACH_RESULT=%s" % ",".join("%s=%s" % (n, results[n]) for n, _, _ in TLBS))
print("TLBREACH_DONE")
