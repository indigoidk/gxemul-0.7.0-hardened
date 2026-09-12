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
#
#  CONTRACT, EXTENDED BY THE PASS-3 CLOSURE (the rows above this point are unchanged).  The two
#  clause-(d) mutants `M13_widthdecline' and `M14_lineardecline' were MEASURED TOTAL ESCAPES of the
#  19-row instrument, so the (d) enumeration was reopened over the two lvalues the guarded store
#  actually reads.  NOW CAUGHT, and caught over a DOMAIN rather than a mutant list: all sixteen
#  cells of {tlb_mode in TLB_A, TLB_B, TLB_C, LIN_A} x {bufdepth in 1, 2, 4, 8} are driven with an
#  unsupported colour type and a readback, so no predicate over tlb_mode and bufdepth alone can be
#  false at every declined cell.  Also caught: a decode that sends one window's PUT to another
#  window's array (the three tiles are distinct, and each window has its own four accept cells);
#  a latch or an announce conditioned on the addressing mode (each window has its own silent /
#  first-announce / cumulative-one triple).
#  STILL NOT CAUGHT, disclosed rather than claimed:  (i) a decline conditioned on `color_mode'
#  itself -- two of the twelve reaching nibbles are driven, and `color_mode' is the switch
#  SELECTOR, which does not flow into any lvalue the guarded body reads, so by the 2026-09-09
#  dispatch-label ruling it is clause-(e) coverage debt and not a floor axis (negative control:
#  M28_permit_othernibbles, MEASURED to escape);  (ii) a decline conditioned on x or y beyond the
#  two vertices driven ((0,0) everywhere and (4,1) in `ycrcb x4y1');  (iii) the tile INDEX -- every
#  cell uses tile 0 of its window, so a condition on tile_nr is unrowed;  (iv) what a permitted
#  store WRITES is uninitialised stack, so a cell's kill depends on those bytes differing from the
#  paint: measured for every cell in killtable3_20260910/PRETABLE.out, never assumed.
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
#  paint row is the decline control.  Added on the pass-2 repair chain at codex's finding.  LOAD
#  SENSITIVITY (codex, by reading session()): 197 commands at fixed 0.22 s windows and a 4.0 s final
#  spin -- a delayed-but-healthy emulator can leave `print v0' unread and the paint row reads `absent'.
#  That is a loud false RED on the fix, never a false green; re-run alone before believing it.
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


# ================================================================ #519 CLOSURE -- THE TILED WINDOWS
#  WHY THESE SESSIONS EXIST.  `M13_widthdecline' (ok = 0 -> if (bufdepth == 4) ok = 0;) and
#  `M14_lineardecline' (-> if (linear) ok = 0;) were MEASURED TOTAL ESCAPES of the 14-row and the
#  19-row instruments (killtable_20260910/M13_widthdecline.raw, M14l_lineardecline_vs19.raw).  They
#  are UNDER-declining mutants: where the added condition is false the unsupported type is PERMITTED
#  and the store below runs -- and because #519 deleted the random() fill, a permitted store writes
#  UNINITIALISED buf.  They escaped because EVERY declined row above drives MODE_YCRCB 0x12f0 or
#  MODE_RESERVED 0x1250, i.e. BUFDEPTH_32 on LIN_A, so both conditions are TRUE at every declined
#  cell and neither mutant is ever exercised where it differs.
#
#  THE CLOSURE, and it is a CLASS closure rather than a cell repair (two passes had found the same
#  shape twice).  The guarded body is the one statement
#      cpu->memory_rw(cpu, cpu->mem, tileptr + ofs, buf, bufdepth, MEM_WRITE, ...)
#  and it reads exactly two lvalues the mode word controls:
#      tlb_mode = (mode >> 10) & 7        -- selects the switch arm that ASSIGNS tileptr
#      bufdepth = 1 << ((mode >> 8) & 3)  -- the store's own LENGTH, and ofs via tilewidth
#  tlb_mode's reachable-to-the-store partition is {0 TLB_A, 1 TLB_B, 2 TLB_C, 4 LIN_A}: 3 and 5-7
#  take the BADMODE default, which RETURNS before the store, and >= 8 is impossible after `& 0x7'.
#  bufdepth's domain is exactly {1, 2, 4, 8}.  The rows above hold ONE of those sixteen cells,
#  (LIN_A, 4).  These sessions drive the OTHER FIFTEEN, declined.  With all sixteen present in the
#  declined set, NO predicate over tlb_mode and bufdepth alone can be false at every declined cell,
#  whatever its shape -- which is why the closure is stated over the DOMAIN and not over a list of
#  mutant forms.  MEASURED, not reasoned: table 3's M20..M27 are that claim's negative controls.
#
#  THE THREE TILES ARE DISTINCT ON PURPOSE (clause (f)).  re_tlb_a[0]/b[0]/c[0] are 0x8001/0x8002/
#  0x8003, so the destinations are physical 0x10000/0x20000/0x30000.  An accept cell therefore pins
#  WHICH array the mode word selected, not merely that something was written somewhere; a decode
#  that sent TLB_B's PUT to re_tlb_a would leave this window's paint intact and RED its accept cell.
#  Bit 15 of the stored halfword is the tileptr's bit 31 -- the "valid" bit horrible_getputpixel
#  tests -- so 0x8001 is not decoration: 0x0001 returns without writing.
#
#  READ IMMEDIATELY AFTER EACH OPERATION.  Every cell repaints its own destination, fires one 1x1
#  rectangle and loads the word back inside ONE stepped instruction block, so a cell's oracle
#  observes its own operation and nothing else.
RE_TLB_A_W = 0xb5001000       # CRIME_RE_TLB_A: one 8-byte store fills re_tlb_a[0..3], big-endian halfwords
RE_TLB_B_W = 0xb5001200
RE_TLB_C_W = 0xb5001400
TILE_A     = 0x8001           # tileptr = re_tlb_a[0] << 16 = 0x80010000 -> phys 0x10000
TILE_B     = 0x8002           # -> phys 0x20000
TILE_C     = 0x8003           # -> phys 0x30000
KS_A, KS_B, KS_C = 0xa0010000, 0xa0020000, 0xa0030000
MARK1, MARK2 = "0x519519", "0x519520"     # a register echo used ONLY to split the transcript
OP_SW_T1_A2 = 0xacc90000      # sw $t1, 0($a2)  -- opcode 0x2b, rs=$6 (a2), rt=$9 (t1)

def tiled_prologue(A):
    """The three TLB windows and the DE state that does not change between operations."""
    c  = store(A, RE_TLB_A_W, TILE_A << 48, op=OP_SD_T0_A3)
    c += store(A, RE_TLB_B_W, TILE_B << 48, op=OP_SD_T0_A3)
    c += store(A, RE_TLB_C_W, TILE_C << 48, op=OP_SD_T0_A3)
    c += store(A, DE_DRAWMODE, DRAWMODE_SOLID)
    c += store(A, DE_FG, FG_VAL)
    c += store(A, DE_XVERTEX_0, 0x00000000)
    c += store(A, DE_XVERTEX_1, 0x00000000)
    return c

def cell_op(A, mode, ks):
    """One cell: repaint, then `sw MODE_DST; sw PRIM_START; lw' in ONE stepped block.  The
    primitive fires synchronously inside the second store, so the load that follows it in the
    same block reads the destination after that operation and before anything else."""
    return (["put w 0x%x, 0x%08x" % (ks, DST_PAINT),
             "a3=0x%x" % DE_MODE_DST,   "t0=0x%x" % mode,
             "a2=0x%x" % DE_PRIM_START, "t1=0x%x" % PRIM_RECT,
             "at=0x%x" % ks,            "v0=0x%x" % SENTINEL]
            + run_ops([OP_SW_T0_A3, OP_SW_T1_A2, OP_LW_V0_AT], A.take(3))
            + ["print v0"])

def printed_seq(t):
    return ["0x%08x" % (int(v, 16) & 0xffffffff)
            for v in re.findall(r"print\s+v0\s*\n\s*(0x[0-9a-f]+)", t)]

#  window tag, destination, four ACCEPT cells (name, mode, expected word), four DECLINED cells
#  (name, mode) spanning the whole bufdepth domain, and the mode repeated once with the latch set.
for _tag, _ks, _acc, _dec, _rpt in (
    ("tA", KS_A, (("ci8", 0x0000, "0xdd223344"), ("rgb",  0x0210, "0xaabbcc00"),
                  ("rgba", 0x0220, "0xaabbccdd"), ("abgr", 0x0230, "0xddccbbaa")),
                 (("d1", 0x00f0), ("d2", 0x01f0), ("d4", 0x02f0), ("d8", 0x03f0)), 0x00f0),
    ("tB", KS_B, (("ci8", 0x0400, "0xdd223344"), ("rgb",  0x0610, "0xaabbcc00"),
                  ("rgba", 0x0620, "0xaabbccdd"), ("abgr", 0x0630, "0xddccbbaa")),
                 (("d1", 0x04f0), ("d2", 0x05f0), ("d4", 0x06f0), ("d8", 0x07f0)), 0x04f0),
    ("tC", KS_C, (("ci8", 0x0800, "0xdd223344"), ("rgb",  0x0a10, "0xaabbcc00"),
                  ("rgba", 0x0a20, "0xaabbccdd"), ("abgr", 0x0a30, "0xddccbbaa")),
                 (("d1", 0x08f0), ("d2", 0x09f0), ("d4", 0x0af0), ("d8", 0x0bf0)), 0x08f0)):
    A = Addr(CODE)
    _cmds = tiled_prologue(A)
    for _n, _m, _w in _acc:
        _cmds += cell_op(A, _m, _ks)
    _cmds += ["t9=%s" % MARK1, "print t9"]
    for _n, _m in _dec:
        _cmds += cell_op(A, _m, _ks)
    _cmds += ["t9=%s" % MARK2, "print t9"]
    _cmds += cell_op(A, _rpt, _ks)
    _t, _alive = session(_cmds, spin=3.0)
    _v = printed_seq(_t) if _alive else []
    def _cell(i):
        return _v[i] if i < len(_v) else "absent"
    for _i, (_n, _m, _w) in enumerate(_acc):
        row("%s %s" % (_tag, _n), _cell(_i) if _alive else "died", _w,
            "ACCEPT 0x%04x: the packing lands in THIS window's own tile (anchors the decode)" % _m)
    for _j, (_n, _m) in enumerate(_dec):
        row("%s ycrcb %s" % (_tag, _n), _cell(len(_acc) + _j) if _alive else "died", want_sentinel,
            "DECLINED 0x%04x: tiled, bufdepth %i -- a cell a conditioned decline would PERMIT"
            % (_m, 1 << ((_m >> 8) & 3)))
    row("%s ycrcb rpt" % _tag, _cell(len(_acc) + len(_dec)) if _alive else "died", want_sentinel,
        "a SECOND declined PUT here, latch already set, still skips its store")
    _pre = _t.split(MARK1, 1)[0] if MARK1 in _t else None
    _mid = (_t.split(MARK1, 1)[-1].split(MARK2, 1)[0]
            if (MARK1 in _t and MARK2 in _t) else None)
    row("%s silent" % _tag, "no marker" if _pre is None else _pre.count(ANN), 0,
        "SILENCE BEFORE: the four accept PUTs announce nothing (marker splits; `no marker' reds)")
    row("%s ann1" % _tag, "no marker" if _mid is None else _mid.count(ANN), 1,
        "FIRST DECLINE ANNOUNCES: exactly one announce between the markers, at a TILED window")
    row("%s ann cum" % _tag, _t.count(ANN) if _alive else "died", 1,
        "CUMULATIVE ONE: five declined PUTs in this process announce once -- the latch")

#  ---- the fourth label: LIN_A at the three bufdepths the rows above do not drive ---------------
#  `ycrcb put' already holds (LIN_A, 4).  These three complete the sixteen-cell domain.
A = Addr(CODE)
_cmds = store(A, RE_LINEAR_A, 0x0000001000000000, op=OP_SD_T0_A3)
_cmds += store(A, DE_DRAWMODE, DRAWMODE_SOLID) + store(A, DE_FG, FG_VAL)
_cmds += store(A, DE_XVERTEX_0, 0x00000000) + store(A, DE_XVERTEX_1, 0x00000000)
for _m in (0x10f0, 0x11f0, 0x13f0):
    _cmds += cell_op(A, _m, DST_KSEG1)
t_lin, alive_lin = session(_cmds, spin=3.0)
_vl = printed_seq(t_lin) if alive_lin else []
for _i, (_n, _m) in enumerate((("d1", 0x10f0), ("d2", 0x11f0), ("d8", 0x13f0))):
    row("lin ycrcb %s" % _n, (_vl[_i] if _i < len(_vl) else "absent") if alive_lin else "died",
        want_sentinel,
        "DECLINED 0x%04x: LINEAR, bufdepth %i -- the label the tiled cells cannot reach"
        % (_m, 1 << ((_m >> 8) & 3)))
row("lin ann cum", t_lin.count(ANN) if alive_lin else "died", 1,
    "three declined LIN_A PUTs at three widths announce once")

ok = sum(1 for _, o in rows if o)
print()
print("SGICOLOUR_RESULT=%d/%d" % (ok, len(rows)))
print("SGICOLOUR_DONE")
sys.exit(0 if ok == len(rows) else 1)
