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
#  CONTRACT -- #519 closure design, 2026-09-12.  This is the controlling coverage
#  contract; older CONTRACT/CLOSED/COMPLETE claims below are historical and are
#  superseded wherever they claim a larger domain or describe missing coverage.
#
#  The declined-PUT input projection is
#      {TLB_A, TLB_B, TLB_C, LIN_A} x {bufdepth 1, 2, 4, 8 bytes}
#      x {SGIRE_W_BADCOLOR clear, set ON ENTRY to the colour default arm}.
#  Its 32 cells concern PUTs that reach that arm with eligible coordinates and
#  a valid selected mapping.  Earlier bounds, mapping and BADMODE returns are
#  outside this projection.  The added fixtures use solid 1x1 DE rectangles at
#  (0,0); their supported RGBA/4-byte controls verify the selected destination.
#  At (0,0), the index and offset are zero at every tested depth.
#
#  The design occupies every cell of this projection.  This exhausts its input
#  tuples for a default-store permission predicate depending ONLY on these
#  three axes.  It is not full closure over arbitrary predicates on all function
#  inputs, nor a claim that each cell independently tests every warning property.
#  The projection's cell readbacks cover every attempted transfer byte,
#  including both words at depth eight.  Each added decline is observed before
#  a later repaint or PUT.
#  Preserved bytes do not prove that no write occurred: a write of identical
#  bytes remains invisible.  Zero-initialized negative controls have exact,
#  differing readbacks; kills of uninitialized-buffer mutants need measurement.
#
#  OUTSIDE: exhaustive coordinates, tile indices, descriptor payloads, raw mode
#  bits, foreground values, other device/CPU/memory state and their interactions.
#  All twelve default nibbles are driven, but are not crossed with this
#  entire projection.  GET, accepted-type width semantics, invalid-input
#  paths, per-instance/reset behavior and cold/warm memory paths are not closed.
#  Existing acceptance, nibble, coordinate and latch-independence rows retain
#  their individual assertions without enlarging the projection.
#
#  M28 nib60 adds a fresh LIN_A/depth-4/type-0x60 decline at FG_VAL.  It targets
#  the reported other-nibble permission family.  The exact historical M28/M28r
#  edit is absent from the permitted records; NIB_OTHER_ZERO is a newly specified
#  deterministic control, not an identification of that historical mutant.
#  Every score for this design is a PREDICTION until built and measured.
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
#  *** DISCLOSURES (i), (ii) AND (iii) BELOW WERE MEASURED TO BE FLOOR BREACHES, NOT DEBT, AND
#  ARE NOW CLOSED BY THE PASS-4 BLOCK AT THE END OF THIS FILE.  The text is kept because it is
#  the record being corrected, and because its REASON was wrong in a way worth not repeating. ***
#
#  (i) said `color_mode' "does not flow into any lvalue the guarded body reads".  THAT IS FALSE:
#  color_mode selects among four arms every one of which writes `buf', and `buf' is the store's
#  DATA operand.  The correct reason M28 was survivable is different and narrower -- the body's
#  own tests partition color_mode into five LABELS and all five were driven, so M28 sliced WITHIN
#  a label.  The wrong reason mattered: applied consistently it also excluded `tile_nr', which
#  flows into `tileptr' -- the ADDRESS operand -- at least as directly as tlb_mode does.
#  (ii) and (iii) were disclosed honestly but classified as debt.  Pass 2 measured SIX mutants at
#  59/59 on this instrument, each writing uninitialised host stack into guest memory:
#  M30/M31/M32 (tile index), M33 (tiled y), M28 (nibble), M37 (foreground value).  The smallest
#  was ELEVEN CHARACTERS -- `if (ok)' -> `if (ok || tile_nr)'.  See
#  regress/artifacts/sgirandomcolour/pass2_20260911/.
#
#  NOW CLOSED, over the COMPLETE free input set of the guarded store rather than a mutant list:
#  { bufdepth, tlb_mode } by the sixteen cells above; { color_mode, *color } by the ten-nibble
#  session at a second foreground colour; { x, y } -- and with them every derived coordinate,
#  since tile_nr, tile_nr_x, tile_nr_y, xofs and ofs are pure functions of them -- by the four
#  coordinate cells.  The bound that makes this finite is stated at the pass-4 block.
#  STILL DISCLOSED:  (a) a predicate ENUMERATING the driven cell set by value, which no finite
#  row set excludes;  (b) coordinate cells are driven at one bufdepth and one label, so a
#  coordinate-joined-to-width or -label mutant is debt;  (c) within-class slices (a particular
#  tile_nr, a third fg);  (iv) what a permitted store WRITES is uninitialised stack, so a cell's
#  kill depends on those bytes differing from the paint: measured for every cell in
#  killtable3_20260910/PRETABLE.out, never assumed, and re-measured in pass 2 (0x7063....).
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

DST_PAINT_TAIL = 0x55667788

def cell_want(mode):
    return ("0x%08x%08x" % (DST_PAINT, DST_PAINT_TAIL)
            if ((mode >> 8) & 3) == 3 else "0x%08x" % DST_PAINT)

def cell_op(A, mode, ks):
    """Repaint, fire one synchronous PUT, then read its whole transfer span."""
    depth8 = ((mode >> 8) & 3) == 3
    paint = ["put w 0x%x, 0x%08x" % (ks, DST_PAINT)]
    if depth8:
        paint += ["put w 0x%x, 0x%08x" % (ks + 4, DST_PAINT_TAIL)]
    return (paint
            + ["a3=0x%x" % DE_MODE_DST,   "t0=0x%x" % mode,
               "a2=0x%x" % DE_PRIM_START, "t1=0x%x" % PRIM_RECT,
               "at=0x%x" % ks,            "v0=0x%x" % SENTINEL]
            + run_ops([OP_SW_T0_A3, OP_SW_T1_A2,
                       OP_LD_V0_AT if depth8 else OP_LW_V0_AT], A.take(3))
            + ["print v0"])

def printed_seq(t, modes=None):
    raw = re.findall(r"print\s+v0\s*\n\s*(0x[0-9a-f]+)", t)
    if modes is None:
        return ["0x%08x" % (int(v, 16) & 0xffffffff) for v in raw]
    if len(raw) != len(modes):
        return []
    return [("0x%016x" % (int(v, 16) & 0xffffffffffffffff)
             if ((mode >> 8) & 3) == 3
             else "0x%08x" % (int(v, 16) & 0xffffffff))
            for v, mode in zip(raw, modes)]

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
    _modes = [m for _, m, _ in _acc] + [m for _, m in _dec] + [_rpt]
    _v = printed_seq(_t, _modes) if _alive else []
    def _cell(i):
        return _v[i] if i < len(_v) else "absent"
    for _i, (_n, _m, _w) in enumerate(_acc):
        row("%s %s" % (_tag, _n), _cell(_i) if _alive else "died", _w,
            "ACCEPT 0x%04x: the packing lands in THIS window's own tile (anchors the decode)" % _m)
    for _j, (_n, _m) in enumerate(_dec):
        row("%s ycrcb %s" % (_tag, _n), _cell(len(_acc) + _j) if _alive else "died", cell_want(_m),
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
    #  #519 pass-3: the `%s ann cum' row that used to sit here is DELETED.  Measured over the
    #  26-mutant table 3 its kill set {M1,M11,M5,M7} is a STRICT SUBSET of `%s ann1's, so it
    #  carried no kill of its own -- score noise that perturbs every future mutant total.  The
    #  cross-PUT latch it was meant to pin is still pinned, by `once' (two declined PUTs in one
    #  process, cumulative announce == 1), which is a whole-transcript count and survives.

#  ---- the fourth label: LIN_A at the three bufdepths the rows above do not drive ---------------
#  `ycrcb put' already holds (LIN_A, 4).  These three complete the sixteen-cell domain.
A = Addr(CODE)
_cmds = store(A, RE_LINEAR_A, 0x0000001000000000, op=OP_SD_T0_A3)
_cmds += store(A, DE_DRAWMODE, DRAWMODE_SOLID) + store(A, DE_FG, FG_VAL)
_cmds += store(A, DE_XVERTEX_0, 0x00000000) + store(A, DE_XVERTEX_1, 0x00000000)
for _m in (0x10f0, 0x11f0, 0x13f0):
    _cmds += cell_op(A, _m, DST_KSEG1)
t_lin, alive_lin = session(_cmds, spin=3.0)
_vl = printed_seq(t_lin, (0x10f0, 0x11f0, 0x13f0)) if alive_lin else []
for _i, (_n, _m) in enumerate((("d1", 0x10f0), ("d2", 0x11f0), ("d8", 0x13f0))):
    row("lin ycrcb %s" % _n, (_vl[_i] if _i < len(_vl) else "absent") if alive_lin else "died",
        cell_want(_m),
        "DECLINED 0x%04x: LINEAR, bufdepth %i -- the label the tiled cells cannot reach"
        % (_m, 1 << ((_m >> 8) & 3)))
#  #519 pass-3: `lin ann cum' DELETED here for the same measured reason as the three per-window
#  `ann cum' rows above -- kill set a strict subset of `once'/`ann1', no kill of its own.


# ================================================================ #519 PASS-4 -- THE CLASS CLOSURE
#  WHY THIS BLOCK EXISTS.  Pass 2 measured SIX mutants scoring 59/59 on the instrument as it
#  stood -- zero red rows, six times -- each one writing uninitialised host stack into guest
#  memory (regress/artifacts/sgirandomcolour/pass2_20260911/).  They were three passes of ONE
#  shape: a decline conditioned on an input the rows hold at a SINGLE VALUE.  M13/M14 were that
#  shape on bufdepth and tlb_mode; M28 on color_mode; M30/M31/M32 on the tile index, M33 on y,
#  M37 on the foreground colour.  The rule forbids buying another cell, so this closes the CLASS.
#
#  THE ENUMERATION, from the function's own inputs rather than from a list of mutant forms.
#  The guarded store reads exactly four lvalues -- tileptr, ofs, buf, bufdepth -- and their
#  inputs, walked up only to the enclosing function boundary, are:
#      bufdepth    <- (mode>>8)&3                  domain {1,2,4,8}   CLOSED by the 16 cells
#      tileptr     <- tlb_mode, tile_nr, array     tlb_mode {0,1,2,4} CLOSED by the 16 cells
#      ofs         <- x, y, bufdepth, tlb_mode
#      buf         <- color_mode (arm), *color (value)
#
#  THE BOUND: tile_nr, tile_nr_x, tile_nr_y, xofs and ofs are NOT independent axes.  Each is a
#  pure function of (x, y, bufdepth, tlb_mode).  So "close every derived coordinate" IS "close
#  the pair (x, y)" -- two free variables, not an open-ended demand.
#
#  *** AND THE WORD "COMPLETE" DOES NOT BELONG HERE.  An earlier draft of this block said "the
#  complete free input set is therefore { x, y, *color, color_mode-within-default }" and that
#  claim is FALSE in two ways, both found by a read-only audit seat and both checked here. ***
#
#  EXHAUSTED -- every value in the reachable domain is driven, so no predicate over these alone
#  can be false at every declined cell, whatever its shape:
#      tlb_mode    {0,1,2,4}     4 of 4      (the other four return before the store)
#      bufdepth    {1,2,4,8}     4 of 4
#      color_mode  16 nibbles    16 of 16    (4 accepting arms + 12 reaching `default:')
#
#  SAMPLED -- driven at more than one value, which kills the measured single-value family, but
#  NOT exhausted, so a slice WITHIN a driven class can still escape:
#      x           {0, 4, 132} of 2048          y  {0,1} masked, of 128
#      *color      2 values of 2^32
#      tileptr     {0x10000,0x20000,0x30000,0x40000,0x50000} -- the TLB ARRAY CONTENTS, which
#                  the line above lists as an input to tileptr and which the superseded
#                  sentence then silently dropped.  This one matters most: tileptr IS the
#                  store's address operand, so by the 2026-09-09 flow test the array VALUE is
#                  as much a floor axis as the array CHOICE (tlb_mode) already is.
#      mode        the raw parameter.  Bits 0-3 and 13-31 are read by NOTHING in this function,
#                  and every mode word any row drives has low nibble 0.
#
#  WHAT THAT COSTS, stated rather than glossed: `if (ok || (tileptr & 0xfff00000))',
#  `if (ok || (mode & 1))', `if (ok || (x & 1))' and `if (ok || (y & 2))' are each predicted to
#  score 77/77 and each is reachable by one ordinary guest store.  They are DERIVED, not
#  measured -- no table has run them.  They are filed in killtable4_20260911/RESIDUALS.md.
#
#  WHY THEY ARE NOT REPAIRED HERE, and this is the honest boundary rather than a dodge: a slice
#  within an already-driven class is not closable by any finite row set -- for any cells you
#  drive, a predicate false on exactly those cells exists.  That is the same species the
#  2026-09-04 ruling files as clause-(e) debt, and it is the species this round already accepted
#  for M28 (a value slice inside a driven label).  The tileptr/array-contents axis is the one
#  exception that is genuinely FLOOR-shaped, because the value flows into the address operand;
#  it is filed as owed rather than fixed in this diff, because a repair made in response to a
#  review owes its own pass and this block has not had one.
#
#  STILL DISCLOSED rather than rowed, and named so a later escape is inside or outside the
#  contract by inspection: (a) a predicate that ENUMERATES this cell set by value
#  (`x == 0 || x == 132 || ...'), which no finite row set can exclude and which the floor rules
#  do not demand -- rows are owed per enumerated mutant, never per refusing state; (b) the
#  coordinate cells are driven at ONE bufdepth (4) and ONE label (TLB_A), so a mutant joining a
#  coordinate to a width or a label is coverage debt; (c) tile_nr values beyond {0,1,16,17} and
#  fg values beyond the two driven -- within-class slices, clause (e) by the 2026-09-04 ruling.

FG_ALT = 0x5a3c691e           # a SECOND foreground colour.  See the note below -- this exists
                              # because every one of the rows above draws in FG_VAL.

#  ---- AXIS 1: the colour nibble, and the foreground value, closed in ONE session -------------
#  `ycrcb put' (0xf0) and `reserved put' (0x50) already drive two of the TWELVE nibbles that
#  reach the default arm, both at LIN_A/bufdepth 4/(0,0).  These are the other TEN at that same
#  already-rowed cell, which is why the closure costs ten rows and not twelve.
#
#  AND THE SESSION DRAWS IN FG_ALT, NOT FG_VAL -- which closes the *color axis for free.
#  My own pass-2 CONTROL set DE_FG to the same 0xaabbccdd the instrument uses and therefore
#  scored M37_fgvalue 10/10, reproducing the exact blind spot it was built to expose.  A control
#  must not bake in a constant the thing under test also uses; that is the same failure one
#  level up.  With these ten cells at FG_ALT, `if (*color == 0xaabbccdd) ok = 0;' declines at
#  every older row and PERMITS at all ten of these.
NIB_OTHER = (0x40, 0x60, 0x70, 0x80, 0x90, 0xa0, 0xb0, 0xc0, 0xd0, 0xe0)
A = Addr(CODE)
_cmds = store(A, RE_LINEAR_A, 0x0000001000000000, op=OP_SD_T0_A3)
_cmds += store(A, DE_DRAWMODE, DRAWMODE_SOLID) + store(A, DE_FG, FG_ALT)
_cmds += store(A, DE_XVERTEX_0, 0x00000000) + store(A, DE_XVERTEX_1, 0x00000000)
_cmds += cell_op(A, 0x1220, DST_KSEG1)                      # RGBA accept, at FG_ALT
for _nb in NIB_OTHER:
    _cmds += cell_op(A, 0x1200 | _nb, DST_KSEG1)            # LIN_A | BUFDEPTH_32 | nibble
t_nib, alive_nib = session(_cmds, spin=3.5)
_vn = printed_seq(t_nib) if alive_nib else []
row("nib accept alt", (_vn[0] if _vn else "absent") if alive_nib else "died",
    "0x%08x" % FG_ALT,
    "LIVENESS + fg ACCEPT: an RGBA PUT drawn in a SECOND colour lands whole")
for _i, _nb in enumerate(NIB_OTHER):
    row("nib %02x" % _nb, (_vn[_i + 1] if _i + 1 < len(_vn) else "absent") if alive_nib else "died",
        want_sentinel,
        "DECLINED type 0x%02x at FG_ALT: one of the ten reaching nibbles no row drove" % _nb)
row("nib ann", t_nib.count(ANN) if alive_nib else "died", 1,
    "ten declined nibbles in one process announce ONCE -- the latch spans the nibble axis")

#  ---- AXIS 2: the coordinate pair (x, y), and every quantity derived from it ------------------
#  Every one of the rows above drives vertex (0,0) except `ycrcb x4y1' at (4,1), which is
#  LINEAR -- and on the linear path tile_nr is x>>12, so 4>>12 == 0.  A TILED (4,1) would not
#  have helped either: 4/tilewidth_in_pixels is 0 at every bufdepth.  So EVERY row above holds
#  tile_nr, tile_nr_x and tile_nr_y at ZERO, and `if (ok || tile_nr)' -- eleven characters --
#  swept the 59-row instrument clean while corrupting every tile but the first.
#
#  *** THIS SENTENCE ALSO NAMED `xofs' AND THAT WAS A WRONG RECORD.  Corrected. ***  `xofs' is
#  computed at dev_sgi_re.c:247, BEFORE the switch on tlb_mode, so at `ycrcb x4y1' -- LINEAR
#  (4,1), bufdepth 4 -- it is (4 % 128) * 4 = 16, NOT zero.  The linear arm overrides `ofs' with
#  `x & 4095' and never recomputes `xofs'.  MEASURED: killtable4_20260911's M39_xofsguard
#  (`if (xofs == 0) ok = 0;') reds THREE rows and the third is `ycrcb x4y1' -- a row predating
#  this block.  Found twice independently, by that table and by a read-only audit seat reading
#  this comment against the source.
#
#  THE CELLS, tiled TLB_A at bufdepth 4 so tilewidth_in_pixels is 128:
#      C1 (132,  0)  tile_nr_x 1  tile_nr_y 0  tile_nr  1  y 0  xofs 16  ofs  16 -> tile  1
#      C2 (  0,  1)  tile_nr_x 0  tile_nr_y 0  tile_nr  0  y 1  xofs  0  ofs 512 -> tile  0
#      C3 (  0,128)  tile_nr_x 0  tile_nr_y 1  tile_nr 16  y 0  xofs  0  ofs   0 -> tile 16
#      C4 (132,129)  tile_nr_x 1  tile_nr_y 1  tile_nr 17  y 1  xofs 16  ofs 528 -> tile 17
#  against the existing (0,0), where all seven of those are ZERO.
#
#  x IS 132 AND NOT 128 ON PURPOSE: it makes tile_nr_x AND xofs non-zero in ONE cell, which is
#  what lets C4 be non-zero on all seven derived quantities at once.  (The first version of this
#  note justified 132 by claiming `if (xofs == 0) ok = 0;' would otherwise sweep the table.  That
#  is FALSE -- `ycrcb x4y1' already carries xofs 16, so that mutant was caught before this block
#  existed, and M39 measures it at 76/77 territory rather than a sweep.  The CHOICE is right and
#  the REASON was wrong; corrected rather than left, because a wrong reason gets reused.)
#  [#556, 2026-10-02 -- a records correction; the text above is kept as it was written] and M39 measures it at 74/77
#  territory rather than a sweep.  (hsgirecolourdefaultprobe:F4:
#  regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md)
#  y IS 129 AND NOT 128 IN C4 because `y &= 127' runs BEFORE the colour switch, so 128 masks to
#  zero and would leave the in-scope `y' pinned.
#
#  C4 IS THE JOINT CELL and it is not decoration: a corner-free design is swept by the pairwise
#  disjunctions.  `tile_nr == 0 || y == 0' is TRUE at (0,0), C1, C2 and C3 and false only at C4.
#
#  EACH CELL HAS ITS OWN TILE, SO EACH ACCEPT IS AN ANCHOR (clause (f)): re_tlb_a[0/1/16/17] are
#  0x8001/0x8002/0x8004/0x8005, i.e. physical 0x10000/0x20000/0x40000/0x50000.  An accept row
#  pins WHICH tile and WHICH offset the decode chose, not merely that something was written; and
#  `xy anchor t0' re-reads tile 0's own word afterwards, so an access that silently collapsed to
#  tile 0 reddens even though its own cell looks untouched.
RE_TLB_A_16 = 0xb5001020      # re_tlb_a[16..19]: tlbi = ((0x1020 & 0x1ff) >> 1) & 0xff = 16
TILE_16, TILE_17 = 0x8004, 0x8005
XY_CELLS = (("c1 x132y0",   (132 << 16) | 0,   0xa0020010),   # tile  1, ofs  16
            ("c2 x0y1",     (  0 << 16) | 1,   0xa0010200),   # tile  0, ofs 512
            ("c3 x0y128",   (  0 << 16) | 128, 0xa0040000),   # tile 16, ofs   0
            ("c4 x132y129", (132 << 16) | 129, 0xa0050210))   # tile 17, ofs 528

def xy_prologue(A):
    c  = store(A, RE_TLB_A_W,  (TILE_A << 48) | (TILE_B << 32), op=OP_SD_T0_A3)
    c += store(A, RE_TLB_A_16, (TILE_16 << 48) | (TILE_17 << 32), op=OP_SD_T0_A3)
    c += store(A, DE_DRAWMODE, DRAWMODE_SOLID)
    c += store(A, DE_FG, FG_VAL)
    #  tile 0's OWN word at ofs 0 is painted here and by nothing else: no cell in this session
    #  writes it (C2 lives at ofs 512), so it is a clean attribution target for `xy anchor t0'.
    c += store(A, 0xa0010000, DST_PAINT)
    return c

def xy_cell(A, mode, vertex, ks):
    """One coordinate cell: repaint its own destination, set the vertex, fire, read back."""
    return (["put w 0x%x, 0x%08x" % (ks, DST_PAINT),
             "a3=0x%x" % DE_XVERTEX_0, "t0=0x%x" % vertex]
            + run_ops([OP_SW_T0_A3], A.take(1))
            + ["a3=0x%x" % DE_XVERTEX_1, "t0=0x%x" % vertex]
            + run_ops([OP_SW_T0_A3], A.take(1))
            + ["a3=0x%x" % DE_MODE_DST,   "t0=0x%x" % mode,
               "a2=0x%x" % DE_PRIM_START, "t1=0x%x" % PRIM_RECT,
               "at=0x%x" % ks,            "v0=0x%x" % SENTINEL]
            + run_ops([OP_SW_T0_A3, OP_SW_T1_A2, OP_LW_V0_AT], A.take(3))
            + ["print v0"])

A = Addr(CODE)
_cmds = xy_prologue(A)
for _n, _vtx, _ks in XY_CELLS:                       # four ACCEPTS, each into its own tile
    _cmds += xy_cell(A, 0x0220, _vtx, _ks)
for _n, _vtx, _ks in XY_CELLS:                       # then the same four cells, DECLINED
    _cmds += xy_cell(A, 0x02f0, _vtx, _ks)
_cmds += ["at=0x%x" % 0xa0010000, "v0=0x%x" % SENTINEL] + run_ops([OP_LW_V0_AT], A.take(1)) + ["print v0"]
t_xy, alive_xy = session(_cmds, spin=4.0)
_vx = printed_seq(t_xy) if alive_xy else []
def _xy(i):
    return (_vx[i] if i < len(_vx) else "absent") if alive_xy else "died"
for _i, (_n, _vtx, _ks) in enumerate(XY_CELLS):
    row("xy acc %s" % _n.split()[0], _xy(_i), "0x%08x" % FG_VAL,
        "ACCEPT ANCHOR: lands in THIS cell's own tile at its own offset (0x%08x)" % _ks)
for _i, (_n, _vtx, _ks) in enumerate(XY_CELLS):
    row("xy dec %s" % _n.split()[0], _xy(len(XY_CELLS) + _i), want_sentinel,
        "DECLINED at %s: a cell where a coordinate-derived guard would PERMIT" % _n.split()[1])
row("xy anchor t0", _xy(2 * len(XY_CELLS)), "0x%08x" % DST_PAINT,
    "ATTRIBUTION: tile 0's own word survives, so no cell silently collapsed onto it")
row("xy ann", t_xy.count(ANN) if alive_xy else "died", 1,
    "four declined PUTs across four tiles announce ONCE, and the four ACCEPTS are silent")

# ================================================================ #519 bounded closure
# Ten fresh first-decline sessions, one primed repeat session, and the M28-family row.
# Each table entry contributes ONE assertion: its readbacks and announce count.
# The RGBA control uses four initialized bytes, including for depth-eight declines.
# A fresh session has BADCOLOR clear; the RGBA control leaves it clear.
CL519_CASES = (
    ("tA d2 first",   0x01f0, KS_A,       False, "FIRST_A2_ZERO"),
    ("tA d8 first",   0x03f0, KS_A,       False, "FIRST_A8_ZERO"),
    ("tB d2 first",   0x05f0, KS_B,       False, "FIRST_B2_ZERO"),
    ("tB d4 first",   0x06f0, KS_B,       False, "FIRST_B4_ZERO"),
    ("tB d8 first",   0x07f0, KS_B,       False, "FIRST_B8_ZERO"),
    ("tC d2 first",   0x09f0, KS_C,       False, "FIRST_C2_ZERO"),
    ("tC d4 first",   0x0af0, KS_C,       False, "FIRST_C4_ZERO"),
    ("tC d8 first",   0x0bf0, KS_C,       False, "FIRST_C8_ZERO"),
    ("lin d2 first",  0x11f0, DST_KSEG1,  False, "FIRST_L2_ZERO"),
    ("lin d8 first",  0x13f0, DST_KSEG1,  False, "FIRST_L8_ZERO"),
    ("lin d1 repeat", 0x10f0, DST_KSEG1,  True,  "REPEAT_L1_ZERO"),
    ("M28 nib60",     0x1260, DST_KSEG1,  False, "NIB_OTHER_ZERO"),
)
for _name, _mode, _ks, _repeat, _control in CL519_CASES:
    A = Addr(CODE)
    _cmds = tiled_prologue(A)
    _cmds += store(A, RE_LINEAR_A, 0x0000001000000000, op=OP_SD_T0_A3)
    _modes = [(_mode & 0x1c00) | 0x0220]
    _want = ["0x%08x" % FG_VAL]
    if _repeat:
        # This first decline is itself read before the target cell repaints.
        _modes.append(MODE_YCRCB)
        _want.append(cell_want(MODE_YCRCB))
    _modes.append(_mode)
    _want.append(cell_want(_mode))
    for _m in _modes:
        _cmds += cell_op(A, _m, _ks)
    _t, _alive = session(_cmds, spin=3.0)
    _got = printed_seq(_t, _modes) if _alive else []
    row(_name, (tuple(_got), _t.count(ANN)) if _alive else "died",
        (tuple(_want), 1),
        "readbacks in operation order; one announce; control=" + _control)

ok = sum(1 for _, o in rows if o)
print()
print("SGICOLOUR_RESULT=%d/%d" % (ok, len(rows)))
print("SGICOLOUR_DONE")
sys.exit(0 if ok == len(rows) else 1)
