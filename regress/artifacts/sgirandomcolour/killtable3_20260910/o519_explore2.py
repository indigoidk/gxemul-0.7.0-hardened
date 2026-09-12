#!/usr/bin/env python3
#  #519 EXPLORATION -- check the closure prescription's premises by MEASUREMENT, before rows are written.
#  Not a deliverable; throwaway.  usage: o519_explore.py <gxemul-binary> [label]
import os, pty, re, select, sys, time

BIN   = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "?"
DUMMY = "/tmp/dummy_sgirand.bin"
if not os.path.exists(DUMMY):
    with open(DUMMY, "wb") as f:
        f.write(b"\0" * 16)

CODE          = 0x80001000
RE_TLB_A      = 0xb5001000
RE_TLB_B      = 0xb5001200
RE_TLB_C      = 0xb5001400
DE_MODE_DST   = 0xb5002008
DE_DRAWMODE   = 0xb5002018
DE_XVERTEX_0  = 0xb5002070
DE_XVERTEX_1  = 0xb5002074
DE_FG         = 0xb50020d0
DE_PRIM_START = 0xb5002860
DRAWMODE_SOLID = 0x000000f8
PRIM_RECT     = 0x03020000
FG_VAL        = 0xaabbccdd
PAINT         = 0x11223344

TILE_A = 0x8001      # -> phys 0x10000
TILE_B = 0x8002      # -> phys 0x20000
TILE_C = 0x8003      # -> phys 0x30000
KS_A   = 0xa0010000
KS_B   = 0xa0020000
KS_C   = 0xa0030000

OP_NOP      = 0x00000000
OP_B_SELF   = 0x1000ffff
OP_SW_T0_A3 = 0xace80000
OP_SD_T0_A3 = 0xfce80000
OP_LW_V0_AT = 0x8c220000
SENTINEL    = 0xdeadbeef

def session(cmds, settle=1.5, spin=2.0, per=0.22):
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
            alive = False; break
        if not rd(spin if i == len(cmds) - 1 else per):
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

def printed_all(t, reg):
    return ["0x%08x" % (int(v, 16) & 0xffffffff)
            for v in re.findall(r"print\s+%s\s*\n\s*(0x[0-9a-f]+)" % reg, t)]

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

#  ---- session prologue: all three TLB windows programmed with DISTINCT tiles ----
def prologue(A):
    c  = store(A, RE_TLB_A, TILE_A << 48, op=OP_SD_T0_A3)
    c += store(A, RE_TLB_B, TILE_B << 48, op=OP_SD_T0_A3)
    c += store(A, RE_TLB_C, TILE_C << 48, op=OP_SD_T0_A3)
    c += store(A, DE_DRAWMODE, DRAWMODE_SOLID)
    c += store(A, DE_FG, FG_VAL)
    c += store(A, DE_XVERTEX_0, 0x00000000)
    c += store(A, DE_XVERTEX_1, 0x00000000)
    return c

def op(A, mode, dst_ks):
    """repaint dst, set MODE_DST, fire, read back."""
    c  = store(A, dst_ks, PAINT)
    c += store(A, DE_MODE_DST, mode)
    c += store(A, DE_PRIM_START, PRIM_RECT)
    c += load(A, dst_ks)
    c += ["print v0"]
    return c

print("EXPLORE #519 tiled premises -- binary=%s label=%s" % (BIN, LABEL))

for wname, ks, modes in (
        ("TLB_A", KS_A, (0x0000, 0x0210, 0x0220, 0x0230, 0x00f0, 0x01f0, 0x02f0, 0x03f0, 0x00f0)),
        ("TLB_B", KS_B, (0x0400, 0x0610, 0x0620, 0x0630, 0x04f0, 0x06f0, 0x04f0)),
        ("TLB_C", KS_C, (0x0800, 0x0a10, 0x0a20, 0x0a30, 0x08f0, 0x0af0, 0x08f0))):
    A = Addr(CODE)
    cmds = prologue(A)
    for m in modes[:4]:
        cmds += op(A, m, ks)
    cmds += ["t9=0x519519", "print t9"]
    for m in modes[4:-1]:
        cmds += op(A, m, ks)
    cmds += ["t9=0x519520", "print t9"]
    cmds += op(A, modes[-1], ks)
    _t0 = time.time()
    t, alive = session(cmds, spin=3.0)
    _el = time.time() - _t0
    vals = printed_all(t, "v0")
    ANN = "unimplemented colour type in horrible_getputpixel"
    pre = t.split("0x519519", 1)[0] if "0x519519" in t else "<<MARKER1 MISSING>>"
    mid = t.split("0x519519", 1)[-1].split("0x519520", 1)[0] if "0x519520" in t else "<<MARKER2 MISSING>>"
    print("--- %s  alive=%s  cmds=%d  elapsed=%.1fs" % (wname, alive, len(cmds), _el))
    print("    modes  %s" % " ".join("0x%04x" % m for m in modes))
    print("    v0     %s" % " ".join(vals))
    print("    ANN total=%d  before-marker1=%d  between-markers=%d" %
          (t.count(ANN), pre.count(ANN), mid.count(ANN)))
    print("    marker1 seen=%s marker2 seen=%s" % ("0x519519" in t, "0x519520" in t))
    for lit in ("[ put: color mode = 0xf0 ]", "unimplemented dst_mode",
                "d->re_tlb_a[0] = 0x8001", "d->re_tlb_b[0] = 0x8002", "d->re_tlb_c[0] = 0x8003"):
        print("    %-34s %d" % (lit, t.count(lit)))
print("EXPLORE_DONE")
