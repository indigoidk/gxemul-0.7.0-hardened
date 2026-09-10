#!/usr/bin/env python3
#
#  sgirandomcolour -- RUNG-3 WITNESS for dev_sgi_re.c horrible_getputpixel() colour-mode default.
#
#  THE DEFECT.  horrible_getputpixel() extracts `color_mode = mode & DE_MODE_TYPE_MASK' (mask 0xf0)
#  and switches on it during a PUT.  Four cases are implemented:
#    case DE_MODE_TYPE_CI:   buf[0] = *color;
#    case DE_MODE_TYPE_RGB:  buf[0] = *color >> 24; buf[1] = *color >> 16; buf[2] = *color >> 8; buf[3] = 0;
#    case DE_MODE_TYPE_RGBA: buf[0] = *color >> 24; buf[1] = *color >> 16; buf[2] = *color >> 8; buf[3] = *color;
#    case DE_MODE_TYPE_ABGR: buf[0] = *color; buf[1] = *color >> 8; buf[2] = *color >> 16; buf[3] = *color >> 24;
#  The `default:' arm executes:
#    buf[0] = random(); buf[1] = random(); buf[2] = random(); buf[3] = random();
#    fatal("[ put: color mode = 0x%x ]\n", color_mode);
#  and then allows the common tail to execute:
#    cpu->memory_rw(cpu, cpu->mem, tileptr + ofs, buf, bufdepth, MEM_WRITE, NO_EXCEPTIONS | PHYSICAL);
#  which writes bufdepth bytes of that buffer to guest memory -- the four random() fills at 32 bpp, one
#  of them at 8 bpp, and at bufdepth 8 those four plus an uninitialised tail (sgirebufuninit).  fatal()
#  does not exit.
#
#  REACHABILITY: 12 of the 16 nibbles reach default:, including the documented DE_MODE_TYPE_YCRCB
#  (0x000000f0 per crmfbreg.h) and reserved encodings such as 0x50.
#
#  POST-FIX BEHAVIOUR: an unhandled / unimplemented colour mode during a PUT declines and skips
#  writing to memory, leaving the destination pre-paint intact.
#
#  CONTRACT (vacuity-floor clause (e)) -- what this witness catches and what it does NOT:
#    CATCHES   the default arm assigning random() and storing it: `ycrcb put' and `reserved put'
#              expect the destination to remain unchanged (post-fix honest decline); on HEAD they
#              fail because host random() bytes overwrite the pre-painted sentinel.
#    DOES NOT  implement YCRCB colour space conversion or other colour modes; it witnesses the defect
#              on unhandled modes under ordinary bounds-correctness engineering.
#
#  usage: sgi_re_colourdefault_probe.py <gxemul-binary> [label]
import os, pty, re, select, sys, time

BIN   = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "?"
DUMMY = "/tmp/dummy_sgirand.bin"
if not os.path.exists(DUMMY):
    with open(DUMMY, "wb") as f:
        f.write(b"\0" * 16)

CODE      = 0x80001000
SCRATCH   = 0xa0001800
LIVE_VAL  = 0x5a5a5a5a

RE_LINEAR_A   = 0xb5001700
DE_MODE_SRC   = 0xb5002000
DE_MODE_DST   = 0xb5002008
DE_DRAWMODE   = 0xb5002018
DE_XVERTEX_0  = 0xb5002070
DE_XVERTEX_1  = 0xb5002074
DE_XFER_ADDR  = 0xb50020a0
DE_FG         = 0xb50020d0
DE_XFER_STEPX = 0xb50020a8
DE_PRIM_START = 0xb5002860

MODE_RGBA     = 0x1220        # LIN_A 0x1000 | BUFDEPTH_32 0x200 | TYPE_RGBA  0x20
MODE_YCRCB    = 0x12f0        # LIN_A 0x1000 | BUFDEPTH_32 0x200 | TYPE_YCRCB 0xf0
MODE_RESERVED = 0x1250        # LIN_A 0x1000 | BUFDEPTH_32 0x200 | TYPE_RESV  0x50
DRAWMODE_SOLID = 0x000000f8   # PLANEMASK 0x80 | BYTEMASK 0x78 (solid fill, no XFER/ROP/STIP)
PRIM_RECT     = 0x03020000    # DE_PRIM_RECTANGLE 0x03000000 | DE_PRIM_TB 0x00020000

TILE_PHYS     = 0x10000       # re_linear_a[0] = 0x10 -> physical 0x10000
DST_KSEG1     = 0xa0000000 + TILE_PHYS
FG_VAL        = 0xaabbccdd    # distinctive foreground colour
DST_PAINT     = 0x11223344    # sentinel pattern: distinct from FG_VAL and random values

OP_NOP        = 0x00000000
OP_B_SELF     = 0x1000ffff
OP_SW_T0_A3   = 0xace80000    # sw $t0, 0($a3)
OP_SD_T0_A3   = 0xfce80000    # sd $t0, 0($a3)
OP_LW_V0_AT   = 0x8c220000    # lw $v0, 0($at)
OP_SB_T0_A3   = 0xa0e80000    # sb $t0, 0($a3)   -- a NARROW store: fires a *_LEN / DE_LEN latch
OP_LD_V0_AT   = 0xdc220000    # ld $v0, 0($at)   -- a 64-bit read: the TEX read decline (#513)

rows = []
def row(name, got, want, note="", negate=False):
    ok = (got != want) if negate else (got == want)
    rows.append((name, ok))
    shown = ("NOT " + str(want)) if negate else str(want)
    print("%-16s %-14s %-16s %-52s %s" % (name, str(got), shown, note, "ok" if ok else "FAIL"))
    return ok

def session(cmds, settle=1.5, spin=1.6):
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

def printed(t, reg):
    m = re.search(r"print\s+%s\s*\n\s*(0x[0-9a-f]+)" % reg, t)
    return "absent" if not m else "0x%08x" % (int(m.group(1), 16) & 0xffffffff)

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

SENTINEL = 0xdeadbeef
def load(A, addr):
    return ["at=0x%x" % addr, "v0=0x%x" % SENTINEL] + run_ops([OP_LW_V0_AT], A.take(1))
def loadop(A, addr, op):
    return ["at=0x%x" % addr, "v0=0x%x" % SENTINEL] + run_ops([op], A.take(1))

def setup_put(A, dst_mode, fg=FG_VAL, paint=DST_PAINT, vertex=0x00000000):
    """Program the engine, paint destination with sentinel, then fire one pixel PUT.
    vertex packs (x << 16) | y for XVERTEX_0/1 (draw_primitive: `>> 16) & 0x7ff' / `& 0x7ff'); the
    default is (0,0).  Added on pass 2 (grok): every PUT sat at (0,0), so a guard qualified
    `if (ok || x)' kept every row green.  The second-word paint is emitted ONLY for a non-origin
    vertex, so every pre-existing session's command stream is unchanged by this parameter."""
    c  = store(A, RE_LINEAR_A, 0x0000001000000000, op=OP_SD_T0_A3)  # re_linear_a[0] = 0x10 -> phys 0x10000
    c += store(A, DST_KSEG1, paint)
    if vertex:
        c += store(A, DST_KSEG1 + 4, paint)            # the word a (4,y) PUT reaches: linear ofs = x & 4095
    c += store(A, DE_MODE_DST, dst_mode)
    c += store(A, DE_DRAWMODE, DRAWMODE_SOLID)
    c += store(A, DE_FG, fg)
    c += store(A, DE_XVERTEX_0, vertex)
    c += store(A, DE_XVERTEX_1, vertex)
    c += store(A, DE_PRIM_START, PRIM_RECT)
    return c

print("sgirandomcolour RUNG-3 WITNESS -- binary=%s label=%s" % (BIN, LABEL))
print("%-16s %-14s %-16s %-52s %s" % ("row", "got", "want", "note", ""))

# ---------------------------------------------------------------- row 1: live
A = Addr(CODE)
t_live, alive_live = session(setup_put(A, MODE_RGBA) + load(A, DST_KSEG1) + ["print v0"])
got_live = printed(t_live, "v0") if alive_live else "died"
row("live", got_live, "0x%08x" % FG_VAL,
    "LIVENESS: supported RGBA DE PUT lands known colour in destination")

# ---------------------------------------------------------------- row 2: ycrcb put
A = Addr(CODE)
t_ycrcb1, alive_ycrcb1 = session(setup_put(A, MODE_YCRCB) + load(A, DST_KSEG1) + ["print v0"])
got_ycrcb1 = printed(t_ycrcb1, "v0") if alive_ycrcb1 else "died"
want_sentinel = "0x%08x" % DST_PAINT
row("ycrcb put", got_ycrcb1, want_sentinel,
    "DEFECT: YCRCB (0xf0) PUT must leave sentinel unchanged; on HEAD clobbered")

# ---------------------------------------------------------------- row 3: ycrcb attrib
diag_ycrcb = "[ put: color mode = 0xf0 ]" in t_ycrcb1
row("ycrcb attrib", "yes" if diag_ycrcb else "no", "yes",
    "ATTRIBUTION: transcript carries `[ put: color mode = 0xf0 ]`")

# ---------------------------------------------------------------- row 4: reserved put
A = Addr(CODE)
t_resv, alive_resv = session(setup_put(A, MODE_RESERVED) + load(A, DST_KSEG1) + ["print v0"])
got_resv = printed(t_resv, "v0") if alive_resv else "died"
row("reserved put", got_resv, want_sentinel,
    "RESERVED: unsupported 0x50 PUT must leave sentinel unchanged; on HEAD clobbered")

# ---------------------------------------------------------------- row 5: determinism
A = Addr(CODE)
t_ycrcb2, alive_ycrcb2 = session(setup_put(A, MODE_YCRCB) + load(A, DST_KSEG1) + ["print v0"])
got_ycrcb2 = printed(t_ycrcb2, "v0") if alive_ycrcb2 else "died"
identical = (got_ycrcb1 == got_ycrcb2 and got_ycrcb1 != "died")
got_det = "identical" if identical else "differ"
row("determinism", got_det, "identical",
    "DETERMINISM: repeat YCRCB put; post-fix identical (sentinel), pre-fix differs across runs")

# ================================================================ #519 DETECTOR ROWS
#  The five rows above are the WITNESS (2/5 on HEAD 1ce8296 -- both unsupported-type PUTs landed host
#  PRNG bytes -- and 5/5 on the fix with the same script).  The rows below DEFEND the fix.
#
#  CONTRACT (clause (e)).  Designed to catch: (b) the verbatim arm reinstated (random fills + an
#  unlatched fatal, the store still taken -- `ycrcb put', `reserved put', `announce text'); (d) the
#  `ok' guard REMOVED (the store taken with an unassigned buf -- `ycrcb put'); the decline turned
#  into a ZERO FILL and a store (`ycrcb put' reads 0); `ok = 0' MOVED INSIDE THE LATCH so only the
#  first declined PUT skips its store (`two declined'); the latch REMOVED (`once' reads 2); the latch
#  SHARED with SGIRE_W_BADMODE (`latch indep' reads 0 after a bad TLB mode fired that bit); the
#  announce SILENCED (`announce text' reads 0); a supported type dropped from the switch (its accept
#  row); the accept side announcing (`live silent').  NOT rowed, disclosed: the GET default arm (a
#  separate row, sgirebufuninit); 16-bit depth (the three 32-bit-type PUT arms assign four bytes, CI
#  one, and a 16-bit store takes two -- the same row's question); `x`/`y` in the announce (the (4,1)
#  row pins them once; other vertices are format only); per-instance latching
#  (one RE instance exists); the YCRCB/reserved values other than 0xf0/0x50 (twelve nibbles reach the
#  arm; two are driven, and the arm's DECISION does not depend on the nibble's value -- the announce
#  prints it, which is the only read); the latch's independence is ROWED against ALL TWELVE other bits in
#  ONE session (`allbits announce', with `allbits primed' proving every priming announce fired -- the
#  class closure sgi_re_width_probe.py's `tex xbit' row established; a first cut of this contract
#  DISCLOSED the eleven non-BADMODE bits as unrowed on a cost premise codex refuted: the cost is one
#  session, not one per bit); a bit added to the enum AFTER this probe cannot be primed here and is the
#  enum's own last-enumerator convention's business;
#  and `two declined' does NOT distinguish the skipped store from an early `return' -- after the PUT
#  switch the guarded store is the only statement, so the two are observationally identical (grok,
#  minimax); the guard form is a readability choice, not an observable one.
#
#  The destination word is read big-endian (ip32): byte 0 of the tile is the word's top byte.

ANN = "unimplemented colour type in horrible_getputpixel"     # the post-fix announce, distinctive part
DECL = "store declined (once)"
MODE_CI8  = 0x1000            # LIN_A | BUFDEPTH_8  | TYPE_CI   -- one byte stored
MODE_RGB  = 0x1210            # LIN_A | BUFDEPTH_32 | TYPE_RGB
MODE_ABGR = 0x1230            # LIN_A | BUFDEPTH_32 | TYPE_ABGR
MODE_LINB_RGBA = 0x1620       # LIN_B | BUFDEPTH_32 | TYPE_RGBA -- the TLB/mode switch's own default (BADMODE)

#  ---- accept rows: the other three supported types land their packing (de-escalation) -----------
A = Addr(CODE)
t_ci, alive_ci = session(setup_put(A, MODE_CI8) + load(A, DST_KSEG1) + ["print v0"])
row("ci8 put", printed(t_ci, "v0") if alive_ci else "died", "0xdd223344",
    "CI at 8 bpp stores ONE byte (fg & 0xff) over the paint's top byte")
A = Addr(CODE)
t_rgb, alive_rgb = session(setup_put(A, MODE_RGB) + load(A, DST_KSEG1) + ["print v0"])
row("rgb put", printed(t_rgb, "v0") if alive_rgb else "died", "0xaabbcc00",
    "RGB stores [R,G,B,pad]: three channels and a zero pad (#505's authoritative arm)")
A = Addr(CODE)
t_abgr, alive_abgr = session(setup_put(A, MODE_ABGR) + load(A, DST_KSEG1) + ["print v0"])
row("abgr put", printed(t_abgr, "v0") if alive_abgr else "died", "0xddccbbaa",
    "ABGR stores the register word byte-reversed")
row("live silent", t_live.count(ANN) if alive_live else "died", 0,
    "the RGBA accept session carries NO colour-type announce (the accept side stays silent)")

#  ---- the announce: present once, with the post-fix text, in the witness's ycrcb session --------
row("announce text", t_ycrcb1.count(DECL) if alive_ycrcb1 else "died", 1,
    "the declined PUT announces with the post-fix text ONCE (a reinstated arm or a silenced decline reads 0)")

#  ---- two declined PUTs in ONE process: the second also skips its store, and one announce -------
A = Addr(CODE)
t_two, alive_two = session(setup_put(A, MODE_YCRCB) + setup_put(A, MODE_RESERVED)
                           + load(A, DST_KSEG1) + ["print v0"])
row("two declined", printed(t_two, "v0") if alive_two else "died", "0x%08x" % DST_PAINT,
    "YCRCB then RESERVED in one process: the SECOND declined PUT leaves the paint too (`ok = 0' inside the latch would store)")
row("once", t_two.count(ANN) if alive_two else "died", 1,
    "two declined PUTs announce EXACTLY ONCE -- the (once) latch")

#  ---- a declined PUT away from the origin (pass 2, grok): the guard qualified on the vertex ---------
#  Every other PUT is at (0,0), so `if (ok || x)' (or `|| y') is invisible to them.  In the LINEAR
#  path (tlb_mode 4) horrible_getputpixel computes `ofs = x & 4095' -- a BYTE offset, y ignored -- so
#  this PUT at (4,1) would land whole on the second pre-painted word (ofs 4) if it stored; both
#  coordinates are non-zero so either one-token qualifier lets the store through.  A first cut of
#  this row used (1,0) and claimed `ofs = 1 * bufdepth': wrong for the linear path (byte 1, straddling
#  two words) -- corrected before any table ran on it.
A = Addr(CODE)
VTX41 = (4 << 16) | 1
t_x1, alive_x1 = session(setup_put(A, MODE_YCRCB, vertex=VTX41) + load(A, DST_KSEG1 + 4) + ["print v0"])
row("ycrcb x4y1", printed(t_x1, "v0") if alive_x1 else "died", "0x%08x" % DST_PAINT,
    "a declined PUT at (4,1) leaves the second word (linear ofs = x & 4095): kills `if (ok || x)' and `|| y'")
row("x4y1 announce", t_x1.count("horrible_getputpixel, x=4 y=1") if alive_x1 else "died", 1,
    "and the one announce names that vertex in its own text (x=4 y=1)")

#  ---- CLASS CLOSURE on the latch-collision axis: every other bit set FIRST, then the colour decline -----
#  sgi_re_width_probe.py's `tex xbit' row proved this priming sequence fires bits 0-10 (bits 0-5 by a byte
#  store to each RE window; 6 a byte store to the DE window; 7/8 a store to and a load from the straggler
#  offset 0x1800; 9 an unimplemented drawing op; 10 a LIN_B rectangle) and its `tex rd lat1' row that a
#  64-bit read of CRIME_RE_TEX fires bit 11.  With bits 0-11 all set, a BADCOLOR latch that SHARES any of
#  them is already silenced when the YCRCB PUT arrives and `allbits announce' reads 0.  `allbits primed'
#  counts the twelve priming announces so a priming access that silently stops firing reds the row
#  instead of leaving a hole (the width probe's own repair for the same vacuity).  One session; the
#  paint row is the decline control.  Added on the pass-2 repair chain at codex's finding.
A = Addr(CODE)
RE_WINDOWS = (0xb5001000, 0xb5001200, 0xb5001400, 0xb5001600, 0xb5001700, 0xb5001780)  # TLB_A..LINEAR_B
DE_BASE   = 0xb5002000            # DEVICE_ACCESS(sgi_de): a byte access fires SGIRE_W_DE_LEN
OUTSIDE   = 0xb5001800            # past LINEAR_B: the straggler arm (UNMAP_WR / UNMAP_RD)
PRIM_BAD  = 0x05020000            # an UNIMPLEMENTED drawing op (only LINE and RECTANGLE exist)
TEX_BASE  = 0xb5001600
prime = []
for _w in RE_WINDOWS:
    prime += store(A, _w, 0x1, op=OP_SB_T0_A3)             # bits 0-5
prime += store(A, DE_BASE, 0x1, op=OP_SB_T0_A3)            # bit 6
prime += store(A, OUTSIDE, 0x1, op=OP_SB_T0_A3)            # bit 7
prime += loadop(A, OUTSIDE, OP_LW_V0_AT)                   # bit 8
prime += setup_put(A, MODE_LINB_RGBA)                      # bit 10 (a real 1x1 rectangle into LIN_B)
prime += store(A, DE_PRIM_START, PRIM_BAD)                 # bit 9
prime += loadop(A, TEX_BASE, OP_LD_V0_AT)                  # bit 11
PRIME_LIT = ["for CRIME_RE_%s -- declined." % _n for _n in ("TLB_A", "TLB_B", "TLB_C", "TEX", "LINEAR_A", "LINEAR_B")] + [
    "[ sgi_de: unimplemented len=",                       # bit 6  DE_LEN
    "unimplemented write to address 0x1800",              # bit 7  UNMAP_WR
    "unimplemented read from address 0x1800",             # bit 8  UNMAP_RD
    "UNIMPLEMENTED drawing op",                           # bit 9  PRIM_OP
    "unimplemented dst_mode",                             # bit 10 BADMODE
    "unimplemented read from CRIME_RE_TEX -- declined."]  # bit 11 TEX_RD
t_all, alive_all = session(prime + setup_put(A, MODE_YCRCB) + load(A, DST_KSEG1) + ["print v0"], spin=4.0)
fired_all = sum(1 for _lit in PRIME_LIT if _lit in t_all)
row("allbits primed", "%i/%i" % (fired_all, len(PRIME_LIT)) if alive_all else "died", "%i/%i" % (len(PRIME_LIT), len(PRIME_LIT)),
    "all twelve other latches PROVEN fired before the colour decline (the row proves its own setup)")
row("allbits announce", t_all.count(ANN) if alive_all else "died", 1,
    "with every other bit set, the colour decline still announces once: a latch sharing ANY bit reads 0")
row("allbits paint", printed(t_all, "v0") if alive_all else "died", "0x%08x" % DST_PAINT,
    "and the declined PUT stored nothing (control)")

#  ---- the latch bit is its own: a BADMODE decline first, then a colour decline still announces --
A = Addr(CODE)
t_ind, alive_ind = session(setup_put(A, MODE_LINB_RGBA) + setup_put(A, MODE_YCRCB)
                           + load(A, DST_KSEG1) + ["print v0"])
row("latch indep", t_ind.count(ANN) if alive_ind else "died", 1,
    "LIN_B fires SGIRE_W_BADMODE first; the colour decline still announces once (a shared bit reads 0)")
row("indep paint", printed(t_ind, "v0") if alive_ind else "died", "0x%08x" % DST_PAINT,
    "the YCRCB PUT after the LIN_B decline stored nothing (the LIN_B half is re-painted over and NOT observed here -- grok)")


ok = sum(1 for _, o in rows if o)
print()
print("SGICOLOUR_RESULT=%d/%d" % (ok, len(rows)))
print("SGICOLOUR_DONE")
sys.exit(0 if ok == len(rows) else 1)
