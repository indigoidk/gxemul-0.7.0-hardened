#!/usr/bin/env python3
#  #519 PASS-2 CONTROL, FOREGROUND-COLOUR AXIS (Opus measuring seat).
#
#  WHY THIS EXISTS.  M37_fgvalue (`ok = 0;' -> `if (*color == 0xaabbccdd) ok = 0;') scored
#  59/59 on the shipped instrument AND 10/10 on ctrl519p2.py.  That is NOT evidence the
#  mutant is harmless: ctrl519p2.py sets DE_FG to the SAME 0xaabbccdd the instrument uses,
#  so my own control inherited the instrument's blind spot on this axis.  A mutant that
#  will not die is a result with three explanations, and I had not discriminated them.
#
#  This drives ONE cell with a DIFFERENT foreground colour.  Everything else is identical
#  to the instrument's own `ycrcb put' cell: LIN_A, bufdepth 4, colour type YCRCB, at (0,0).
#  The ONLY difference from a cell the 59 rows already drive is the value in DE_FG.
#
#  usage: ctrl519p2_fg.py <gxemul-binary> [label]
import os, pty, re, select, sys, time

BIN   = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "?"
DUMMY = "/tmp/dummy_sgirand.bin"
if not os.path.exists(DUMMY):
    with open(DUMMY, "wb") as f:
        f.write(b"\0" * 16)

CODE          = 0x80001000
RE_LINEAR_A   = 0xb5001700
DE_MODE_DST   = 0xb5002008
DE_DRAWMODE   = 0xb5002018
DE_XVERTEX_0  = 0xb5002070
DE_XVERTEX_1  = 0xb5002074
DE_FG         = 0xb50020d0
DE_PRIM_START = 0xb5002860
PRIM_RECT     = 0x03020000
DRAWMODE_SOLID= 0x000000f8
DST_PAINT     = 0x11223344
SENTINEL      = 0xdeadbeef
KS            = 0xa0010000        # re_linear_a[0] = 0x10 -> phys 0x10000
MODE_YCRCB    = 0x12f0            # LIN_A | BUFDEPTH_32 | TYPE_YCRCB -- the instrument's own mode
FG_INSTRUMENT = 0xaabbccdd        # the value every one of the 59 rows uses
FG_OTHER      = 0x12345678        # any other colour a guest may draw in
ANN           = "unimplemented colour type in horrible_getputpixel"

rows = []
def row(name, got, want, note=""):
    ok = (str(got) == str(want))
    rows.append((name, ok))
    print("%-18s %-14s %-14s %-56s %s" % (name, str(got), str(want), note, "ok" if ok else "FAIL"))

def session(cmds, settle=1.5, spin=2.0):
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
        if not rd(spin if i == len(cmds) - 1 else 0.22):
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
    return buf.replace("\r", ""), alive

class Addr(object):
    def __init__(self, base): self.a = base
    def take(self, n):
        got = self.a; self.a += 4 * (n + 2) + 0x20; return got

def run_ops(ops, at):
    put = ["put w 0x%x, 0x%08x" % (at + 4 * i, op) for i, op in enumerate(ops)]
    put += ["put w 0x%x, 0x%08x" % (at + 4 * len(ops), 0x1000ffff),
            "put w 0x%x, 0x%08x" % (at + 4 * len(ops) + 4, 0)]
    return put + ["pc=0x%x" % at, "step %d" % len(ops)]

def store(A, addr, val, op=0xace80000):
    return ["a3=0x%x" % addr, "t0=0x%x" % val] + run_ops([op], A.take(1))

def load(A, addr):
    return ["at=0x%x" % addr, "v0=0x%x" % SENTINEL] + run_ops([0x8c220000], A.take(1))

def put_cell(fg):
    A = Addr(CODE)
    c  = store(A, RE_LINEAR_A, 0x0000001000000000, op=0xfce80000)
    c += store(A, KS, DST_PAINT)
    c += store(A, DE_MODE_DST, MODE_YCRCB) + store(A, DE_DRAWMODE, DRAWMODE_SOLID)
    c += store(A, DE_FG, fg)
    c += store(A, DE_XVERTEX_0, 0) + store(A, DE_XVERTEX_1, 0)
    c += store(A, DE_PRIM_START, PRIM_RECT)
    c += load(A, KS) + ["print v0"]
    t, alive = session(c)
    m = re.search(r"print\s+v0\s*\n\s*(0x[0-9a-f]+)", t)
    return (("0x%08x" % (int(m.group(1), 16) & 0xffffffff)) if m else "absent") if alive else "died", t

print("#519 PASS-2 CONTROL (fg axis) -- binary=%s label=%s" % (BIN, LABEL))
print("%-18s %-14s %-14s %-56s %s" % ("row", "got", "want", "note", ""))

v_same, t_same = put_cell(FG_INSTRUMENT)
row("fg instrument", v_same, "0x%08x" % DST_PAINT,
    "CONTROL: the instrument's own fg 0xaabbccdd -- must decline (this is `ycrcb put')")
row("fg instr ann", t_same.count(ANN), 1, "and it announces once")

v_other, t_other = put_cell(FG_OTHER)
row("fg other", v_other, "0x%08x" % DST_PAINT,
    "*** THE CELL: same mode, same vertex, ONLY DE_FG differs -- must also decline ***")
row("fg other ann", t_other.count(ANN), 1,
    "REACHABILITY: the colour default arm really ran at the other fg too")

ok = sum(1 for _, o in rows if o)
print()
print("CTRLFG_SAME=%s CTRLFG_OTHER=%s" % (v_same, v_other))
print("SGICTRLFG_RESULT=%d/%d" % (ok, len(rows)))
print("SGICTRLFG_DONE")
sys.exit(0 if ok == len(rows) else 1)
