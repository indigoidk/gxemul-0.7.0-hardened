#!/usr/bin/env python3
#  #519 PASS-2 CONTROL PROBE (Opus measuring seat, 2026-09-10).
#
#  WHAT THIS IS FOR.  A mutant that scores 59/59 on the round's instrument has exactly three
#  explanations (carrier: "a mutant that will not die is a result"): it is mis-built, its target
#  is dead, or the rows are mis-cut.  This probe separates them.  It drives the cells the round's
#  59 rows do NOT span and asks whether the fix still declines there and whether a mutant stores.
#
#  It is NOT a proposed detector and it is NOT in the tree.  Its `want' column is pinned to the
#  FIX's behaviour, so a RED row under a mutant means: this mutant writes guest memory at a cell
#  the shipped instrument cannot see.
#
#  THE CELLS, and why each is outside the 59-row span:
#    t1 *      TLB_A, bufdepth 4, at vertex (128,0).  tilewidth_in_pixels = 512/4 = 128, so
#              tile_nr_x = 128/128 = 1 and tile_nr = 1.  EVERY cell in the round's instrument
#              has tile_nr == 0: all its vertices are (0,0) except one (4,1), and 4/128 == 0
#              (tiled) and 4>>12 == 0 (linear).  re_tlb_a[1] = 0x8002 -> phys 0x20000, a
#              DIFFERENT tile from re_tlb_a[0] = 0x8001 -> phys 0x10000, so the paint at 0x10000
#              anchors the index (clause (f)): if the access really landed in tile 0 it would be
#              0x10000 that changed.
#    ty1 *     TLB_A, bufdepth 4, at vertex (0,1).  A SECOND, INDEPENDENT hole: every TILED cell
#              in the instrument sits at y == 0 and the only non-origin cell (4,1) is LINEAR, so
#              a decline conditioned on `linear || y == 0' is invisible to all 59 rows.  Note
#              `y &= 127' runs BEFORE the colour switch, so y must be 1..127 here -- (0,128)
#              would mask to y == 0 and NOT exercise this.  ofs = 512*y + xofs = 512, so this
#              cell also exercises the tiled address arithmetic the round records as unpinned.
#    nib60     LIN_A, bufdepth 4, colour type 0x60 -- a third unsupported nibble.  The round's
#              instrument drives only two of the twelve declining nibbles, 0xf0 and 0x50.
#
#  usage: ctrl519p2.py <gxemul-binary> [label]
import os, pty, re, select, sys, time

BIN   = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "?"
DUMMY = "/tmp/dummy_sgirand.bin"
if not os.path.exists(DUMMY):
    with open(DUMMY, "wb") as f:
        f.write(b"\0" * 16)

CODE          = 0x80001000
RE_TLB_A_W    = 0xb5001000
RE_LINEAR_A   = 0xb5001700
DE_MODE_DST   = 0xb5002008
DE_DRAWMODE   = 0xb5002018
DE_XVERTEX_0  = 0xb5002070
DE_XVERTEX_1  = 0xb5002074
DE_FG         = 0xb50020d0
DE_PRIM_START = 0xb5002860
PRIM_RECT     = 0x03020000
DRAWMODE_SOLID= 0x000000f8
FG_VAL        = 0xaabbccdd
DST_PAINT     = 0x11223344
SENTINEL      = 0xdeadbeef

KS_T0 = 0xa0010000          # re_tlb_a[0] = 0x8001 -> phys 0x10000
KS_T1 = 0xa0020000          # re_tlb_a[1] = 0x8002 -> phys 0x20000
TLBA_2 = 0x8001800200000000 # re_tlb_a[0]=0x8001, [1]=0x8002 (big-endian halfwords)

MODE_T_RGBA  = 0x0220       # TLB_A | BUFDEPTH_32 | TYPE_RGBA
MODE_T_YCRCB = 0x02f0       # TLB_A | BUFDEPTH_32 | TYPE_YCRCB
MODE_L_NIB60 = 0x1260       # LIN_A | BUFDEPTH_32 | TYPE 0x60 (unsupported, and NOT 0xf0/0x50)
VTX_128_0    = (128 << 16) | 0
VTX_0_1      = (0 << 16) | 1      # tile_nr 0, but y == 1 at the colour switch; ofs = 512
VTX_0_0      = 0x00000000
KS_TY1 = 0xa0010200         # re_tlb_a[0] -> phys 0x10000, plus ofs = 512*1 = 0x200

OP_NOP      = 0x00000000
OP_B_SELF   = 0x1000ffff
OP_SW_T0_A3 = 0xace80000
OP_SD_T0_A3 = 0xfce80000
OP_LW_V0_AT = 0x8c220000

ANN  = "unimplemented colour type in horrible_getputpixel"

rows = []
def row(name, got, want, note=""):
    ok = (str(got) == str(want))
    rows.append((name, ok))
    print("%-18s %-14s %-14s %-58s %s" % (name, str(got), str(want), note, "ok" if ok else "FAIL"))
    return ok

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
    put += ["put w 0x%x, 0x%08x" % (at + 4 * len(ops), OP_B_SELF),
            "put w 0x%x, 0x%08x" % (at + 4 * len(ops) + 4, OP_NOP)]
    return put + ["pc=0x%x" % at, "step %d" % len(ops)]

def store(A, addr, val, op=OP_SW_T0_A3):
    return ["a3=0x%x" % addr, "t0=0x%x" % val] + run_ops([op], A.take(1))

def load(A, addr):
    return ["at=0x%x" % addr, "v0=0x%x" % SENTINEL] + run_ops([OP_LW_V0_AT], A.take(1))

def seq(t):
    return ["0x%08x" % (int(v, 16) & 0xffffffff)
            for v in re.findall(r"print\s+v0\s*\n\s*(0x[0-9a-f]+)", t)]

def cell(v, i):
    return v[i] if i < len(v) else "absent"

print("#519 PASS-2 CONTROL -- binary=%s label=%s" % (BIN, LABEL))
print("%-18s %-14s %-14s %-58s %s" % ("row", "got", "want", "note", ""))

# ------------------------------------------------------------------ A: the tile-1 cell is LIVE
#  An ACCEPT at (128,0) must land in tile 1 (phys 0x20000) and leave tile 0 (phys 0x10000) alone.
#  This is the liveness + attribution pair: it proves the cell is reachable, that the decode
#  really selects re_tlb_a[1], and that a store at this cell is observable at all.
A = Addr(CODE)
c  = store(A, RE_TLB_A_W, TLBA_2, op=OP_SD_T0_A3)
c += store(A, KS_T0, DST_PAINT) + store(A, KS_T1, DST_PAINT)
c += store(A, DE_MODE_DST, MODE_T_RGBA) + store(A, DE_DRAWMODE, DRAWMODE_SOLID)
c += store(A, DE_FG, FG_VAL)
c += store(A, DE_XVERTEX_0, VTX_128_0) + store(A, DE_XVERTEX_1, VTX_128_0)
c += store(A, DE_PRIM_START, PRIM_RECT)
c += load(A, KS_T1) + ["print v0"] + load(A, KS_T0) + ["print v0"]
t_acc, alive_acc = session(c)
v = seq(t_acc) if alive_acc else []
row("t1 accept", cell(v, 0) if alive_acc else "died", "0xaabbccdd",
    "LIVENESS: an RGBA PUT at (128,0) lands in re_tlb_a[1] -> phys 0x20000")
row("t1 anchor t0", cell(v, 1) if alive_acc else "died", "0x%08x" % DST_PAINT,
    "ATTRIBUTION: tile 0 (phys 0x10000) untouched, so tile_nr really is 1")

# ------------------------------------------------------------------ B: YCRCB at tile 1
A = Addr(CODE)
c  = store(A, RE_TLB_A_W, TLBA_2, op=OP_SD_T0_A3)
c += store(A, KS_T0, DST_PAINT) + store(A, KS_T1, DST_PAINT)
c += store(A, DE_MODE_DST, MODE_T_YCRCB) + store(A, DE_DRAWMODE, DRAWMODE_SOLID)
c += store(A, DE_FG, FG_VAL)
c += store(A, DE_XVERTEX_0, VTX_128_0) + store(A, DE_XVERTEX_1, VTX_128_0)
c += store(A, DE_PRIM_START, PRIM_RECT)
c += load(A, KS_T1) + ["print v0"]
t_y1, alive_y1 = session(c)
v = seq(t_y1) if alive_y1 else []
got_y1 = cell(v, 0) if alive_y1 else "died"
row("t1 ycrcb", got_y1, "0x%08x" % DST_PAINT,
    "*** THE CELL: declined YCRCB at tile_nr 1 must store NOTHING ***")
row("t1 ycrcb ann", t_y1.count(ANN) if alive_y1 else "died", 1,
    "REACHABILITY: the colour default arm really ran here (not a quiet early return)")

# ------------------------------- C: the y axis -- a TILED cell at (0,1), tile_nr still 0
#  Liveness+attribution pair again: the accept must land at phys 0x10000 + 512 and must NOT
#  disturb the y == 0 word at phys 0x10000.  That anchors `ofs = 512*y + xofs' as well as the cell.
A = Addr(CODE)
c  = store(A, RE_TLB_A_W, TLBA_2, op=OP_SD_T0_A3)
c += store(A, KS_T0, DST_PAINT) + store(A, KS_TY1, DST_PAINT)
c += store(A, DE_MODE_DST, MODE_T_RGBA) + store(A, DE_DRAWMODE, DRAWMODE_SOLID)
c += store(A, DE_FG, FG_VAL)
c += store(A, DE_XVERTEX_0, VTX_0_1) + store(A, DE_XVERTEX_1, VTX_0_1)
c += store(A, DE_PRIM_START, PRIM_RECT)
c += load(A, KS_TY1) + ["print v0"] + load(A, KS_T0) + ["print v0"]
t_a1, alive_a1 = session(c)
v = seq(t_a1) if alive_a1 else []
row("ty1 accept", cell(v, 0) if alive_a1 else "died", "0xaabbccdd",
    "LIVENESS: a tiled RGBA PUT at (0,1) lands at phys 0x10000 + 512*1")
row("ty1 anchor y0", cell(v, 1) if alive_a1 else "died", "0x%08x" % DST_PAINT,
    "ATTRIBUTION: the y==0 word untouched, so ofs really is 512 (pins 512*y arithmetic)")

A = Addr(CODE)
c  = store(A, RE_TLB_A_W, TLBA_2, op=OP_SD_T0_A3)
c += store(A, KS_T0, DST_PAINT) + store(A, KS_TY1, DST_PAINT)
c += store(A, DE_MODE_DST, MODE_T_YCRCB) + store(A, DE_DRAWMODE, DRAWMODE_SOLID)
c += store(A, DE_FG, FG_VAL)
c += store(A, DE_XVERTEX_0, VTX_0_1) + store(A, DE_XVERTEX_1, VTX_0_1)
c += store(A, DE_PRIM_START, PRIM_RECT)
c += load(A, KS_TY1) + ["print v0"]
t_ty1, alive_ty1 = session(c)
v = seq(t_ty1) if alive_ty1 else []
got_ty1 = cell(v, 0) if alive_ty1 else "died"
row("ty1 ycrcb", got_ty1, "0x%08x" % DST_PAINT,
    "*** THE CELL: declined YCRCB at a TILED y != 0 must store NOTHING ***")
row("ty1 ycrcb ann", t_ty1.count(ANN) if alive_ty1 else "died", 1,
    "REACHABILITY: the colour default arm really ran at this cell")

# ------------------------------------------------------------------ D: a third nibble, 0x60
A = Addr(CODE)
c  = store(A, RE_LINEAR_A, 0x0000001000000000, op=OP_SD_T0_A3)
c += store(A, KS_T0, DST_PAINT)
c += store(A, DE_MODE_DST, MODE_L_NIB60) + store(A, DE_DRAWMODE, DRAWMODE_SOLID)
c += store(A, DE_FG, FG_VAL)
c += store(A, DE_XVERTEX_0, VTX_0_0) + store(A, DE_XVERTEX_1, VTX_0_0)
c += store(A, DE_PRIM_START, PRIM_RECT)
c += load(A, KS_T0) + ["print v0"]
t_n6, alive_n6 = session(c)
v = seq(t_n6) if alive_n6 else []
got_n6 = cell(v, 0) if alive_n6 else "died"
row("nib60", got_n6, "0x%08x" % DST_PAINT,
    "*** THE CELL: colour type 0x60 -- a third declining nibble -- must store NOTHING ***")
row("nib60 ann", t_n6.count(ANN) if alive_n6 else "died", 1,
    "REACHABILITY: the colour default arm really ran for nibble 0x60")

ok = sum(1 for _, o in rows if o)
print()
print("CTRL_T1YCRCB=%s CTRL_TY1YCRCB=%s CTRL_NIB60=%s" % (got_y1, got_ty1, got_n6))
print("SGICTRL_RESULT=%d/%d" % (ok, len(rows)))
print("SGICTRL_DONE")
sys.exit(0 if ok == len(rows) else 1)
