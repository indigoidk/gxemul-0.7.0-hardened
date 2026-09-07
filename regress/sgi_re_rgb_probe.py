#!/usr/bin/env python3
#
#  sgirergbroundtrip -- RUNG-3 WITNESS for dev_sgi_re.c horrible_getputpixel()'s RGB arms.
#
#  COPIED from regress/sgi_re_randompixel_probe.py, whose session already drives an XFER copy
#  through this helper on an unmodified `-E sgi -e ip32'.  Only the SOURCE COLOUR TYPE changes.
#
#  THE DEFECT: the RGB PUT and GET arms disagree about which byte holds which channel.
#      PUT  buf[0] = c>>24;  buf[1] = c>>16;  buf[2] = c>>8;  buf[3] = 0;
#      GET  *color = (buf[1]<<24) + (buf[2]<<16) + (buf[3]<<8);
#  PUT writes the top three bytes at 0,1,2; GET reads 1,2,3.  RGB is the ONLY multi-byte mode
#  that fails its own round trip -- RGBA and ABGR both round-trip, using OPPOSITE byte orders,
#  which is why this is an internal inconsistency and not an endianness question.
#
#  WHY THE ORACLE IS A VALUE AND NOT AN INEQUALITY: an XFER copy GETs with src_mode and PUTs
#  with dst_mode, which are INDEPENDENT guest registers.  With src RGB and dst RGBA the
#  corruption is a computable one-byte left shift with a zero fill, so the row asserts an exact
#  value on both the defective and the fixed build.  No uninitialised byte is read, so the
#  `separate automatic objects have no architectural promise' objection that killed a
#  neighbouring witness design does not apply here -- checked, not assumed.
#
#  (original header follows)
#  sgirandompixel -- the probe this was copied from.
#
#  THE DEFECT.  horrible_getputpixel() extracts `tlb_mode = (mode >> 10) & 0x7' and switches on it.
#  Cases 0, 1, 2 and 4 are implemented.  The `default:' arm prints, has its exit(1) COMMENTED OUT,
#  and then executes `*color = random(); return;'.  So a failed GET does not decline -- it hands the
#  caller a random 32-bit value.  In draw_primitive() the failed source GET and the destination PUT
#  share one `color' variable in one loop iteration:
#
#      if (drawmode & DE_DRAWMODE_XFER_EN)
#              horrible_getputpixel(0, ..., src_x, src_y, &color, src_mode);   // may set random()
#      ...
#      if (draw)
#              horrible_getputpixel(1, ..., x, y, &color, dst_mode);           // writes it
#
#  AND THE UNHANDLED VALUE IS A DOCUMENTED MODE.  src/include/thirdparty/crmfbreg.h defines five:
#    DE_MODE_TLB_A 0x0000 -> 0 handled     DE_MODE_LIN_A 0x1000 -> 4 handled
#    DE_MODE_TLB_B 0x0400 -> 1 handled     DE_MODE_LIN_B 0x1400 -> 5 *** default -> random() ***
#    DE_MODE_TLB_C 0x0800 -> 2 handled
#
#  CONTRACT (vacuity-floor clause (e)) -- what this witness catches and what it does NOT:
#    CATCHES   the RGB GET arm re-indexing: `rgb corrupt' pins the EXACT post-GET value, so a
#              destination receives anything other than a value distinct from BOTH the source and
#              the pre-painted destination.  Restoring `exit(1)' there kills the machine and reds
#              fix that merely changes the value without correcting the byte positions still reds.
#              ONLY if the pre-paint is removed -- which is why the destination is PRE-PAINTED with a
#              known value and the row rejects it: "left alone" and "wrote random" are then distinct.
#    DOES NOT  establish that any real driver selects LIN_B.  It appears only in crmfbreg.h and the
#              function's own comment; the PROM's MTE zero-fill path does not call this function; and
#              there is no O2/sgimips image in the tree to boot.  **Documented and storable is NOT
#              driver-selected**, and this probe claims only the former (grok, the witness panel).
#
#  DESIGN CREDIT AND THE FALSE NEGATIVE IT AVOIDS (grok, panel_20260906_224008).  The obvious probe --
#  set the source mode to LIN_B, draw, read the destination -- FINDS NOTHING.  At reset the
#  destination mode is TLB_A and re_tlb_a[] has bit 31 clear, so the PUT returns WITHOUT WRITING and
#  the destination is unchanged: a false negative that looks like a clean run.  Using LIN_A as the
#  DESTINATION closes it, because case 4 forces the valid bit:
#      tileptr = 0x80000000 | (d->re_linear_a[x >> 12] << 12);  ofs = x & 4095;
#  so re_linear_a[0] = 0x10 puts the tile at physical 0x10000, and the byte offset is x itself.
#
#  THE ORACLE IS CERTAIN, NOT PROBABILISTIC.  glibc random() is 31-bit, so the value written has bit
#  31 CLEAR and can never equal a source of 0xAABBCCDD.  Inequality is guaranteed, not 2^-32.
#
#  usage: sgi_re_randompixel_probe.py <gxemul-binary> [label]
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
DE_STATUS = 0xb5004000
DE_STAT   = "0x1e000000"

#  CRIME base is 0xb5000000: CRIME_DE_STATUS is 0x4000 and the shipped width probe reads 0xb5004000.
RE_LINEAR_A   = 0xb5001700
DE_MODE_SRC   = 0xb5002000
DE_MODE_DST   = 0xb5002008
DE_DRAWMODE   = 0xb5002018
DE_XVERTEX_0  = 0xb5002070
DE_XVERTEX_1  = 0xb5002074
DE_XFER_ADDR  = 0xb50020a0
DE_FG         = 0xb50020d0        # CRIME_DE_FG -- `uint32_t color = fg' is what a declined GET leaves
DE_XFER_STEPX = 0xb50020a8
DE_PRIM_START = 0xb5002860        # CRIME_DE_PRIMITIVE 0x2060 | CRIME_DE_START 0x0800

MODE_LIN_A = 0x1220               # LIN_A 0x1000 | BUFDEPTH_32 0x200 | TYPE_RGBA 0x20
MODE_RGB   = 0x1210               # LIN_A 0x1000 | BUFDEPTH_32 0x200 | TYPE_RGB  0x10
#  The ONE nibble that differs from MODE_LIN_A.  dst stays MODE_LIN_A (RGBA) because setup()
#  hardcodes DE_MODE_DST and takes only src_mode as its parameter -- so this changes the
#  observation path WITHOUT moving the accept control, which is what made the neighbouring
#  row's witness objection inapplicable.
#
#  PREDICTED (pre-fix), computed before the run:  source bytes aa bb cc dd
#    GET RGB reads buf[1..3]   -> color = 0xbbccdd00
#    PUT RGBA writes buf[0..3] -> bb cc dd 00
#    destination reads back    -> 0xbbccdd00   (a correct GET would give 0xaabbccdd)
RGB_CORRUPT = 0xbbccdd00           # what the SHIPPED GET produces
RGB_FIXED   = 0xaabbcc00           # what a CORRECTED GET produces
MODE_RGB64 = 0x1310               # LIN_A 0x1000 | BUFDEPTH_64 0x300 | TYPE_RGB 0x10
MODE_RGB_TLBA = 0x0210            # TLB_A 0x0000 | BUFDEPTH_32 0x200 | TYPE_RGB 0x10
MODE_RGB_TLBA64 = 0x0310          # TLB_A 0x0000 | BUFDEPTH_64 0x300 | TYPE_RGB 0x10
#  *** A TILED SOURCE, AND IT EXISTS TO CLOSE A MEASURED FLOOR BREACH. ***  `tlb_mode = (mode>>10)&7'
#  is 0 here, so `linear = tlb_mode > 3' is FALSE -- which is the whole point.  Every other row in
#  this file drives LIN_A (tlb_mode 4), so `linear' was TRUE in all of them and a repair conditioned
#  on it was invisible: mutant M12_linear scored 8/8, a clean sweep.
RE_TLB_A   = 0xb5001000           # CRIME_RE_TLB_A 0x1000, same base as RE_LINEAR_A's 0x1700
TLBA_TILE  = 0x8002               # re_tlb_a[0].  *** BIT 15 IS NOT DECORATION. ***
TLBA_PHYS  = (TLBA_TILE << 16) & ~0x80000000   # -> 0x20000
#  *** A TILED TILE POINTER MUST CARRY ITS OWN VALID BIT, AND LIN_A'S DOES NOT TELL YOU THAT. ***
#  The helper gates on it before using tileptr at all:
#
#      // The highest bit seems to be set for a "valid" tile pointer.
#      if (!(tileptr & 0x80000000))
#              return;                       <- silent decline
#      tileptr &= ~0x80000000;
#
#  LIN_A sets the bit EXPLICITLY -- `tileptr = 0x80000000 | (re_linear_a[n] << 12)' -- so a probe
#  built from the linear path never has to know.  TLB_A takes it from the STORED VALUE:
#  `tileptr = re_tlb_a[n] << 16', and re_tlb_a is uint16_t, so bit 31 of tileptr is bit 15 of the
#  register.  `re_tlb_a[0] = 2' yields 0x00020000, the guard rejects it, and the GET returns without
#  touching *color -- which leaves the caller's `fg' behind.
#
#  MEASURED TWICE: the row read 0x77665544 = FG_VAL, which this probe's own DE_FG comment names as
#  what a declined GET leaves.  The first correction (a halfword-vs-word shift) was a real bug and
#  fixed a real thing; it was not THIS thing, and the row said so again.  **Two wrong guesses, two
#  identical red rows, and the value never once looked like a tiled pixel.**
#  Tiled addressing is NOT the linear formula: `ofs = 512*y + (x % tilewidth)*bufdepth' rather than
#  `ofs = x & 4095'.  With a 1-wide, 4-tall rectangle the four source rows are 512 bytes apart, so
#  all four are painted -- unlike the LIN_A rows, which collide on one byte by design.
TLBA_ROWS  = [0xa0000000 + TLBA_PHYS + 512 * i for i in range(4)]
#  The SAME colour type at a DIFFERENT TRANSFER WIDTH.  bufdepth = 1 << ((mode>>8)&3),
#  so 0x300 gives 8 where 0x200 gives 4.  buf[0..2] are filled either way, so the expected
#  value is unchanged -- which is exactly what makes it a clean second width to test.
#
#  *** THE FIXED VALUE IS NOT THE SOURCE VALUE, AND AN EARLIER DRAFT OF THIS FILE ASSUMED IT
#  WAS.  That row would have gone RED against a CORRECT fix. ***
#
#  RGB is a THREE-channel mode.  A corrected GET reads buf[0..2] and leaves the low byte of
#  *color at zero -- there is no fourth channel to carry, and PUT's own `buf[3] = 0' says so
#  from the other side.  So a source word 0xaabbccdd copies as:
#
#      source memory      aa bb cc dd
#      GET RGB (fixed)    (aa<<24)+(bb<<16)+(cc<<8)  =  0xaabbcc00      <- dd is DROPPED
#      PUT RGBA           aa bb cc 00
#      destination        0xaabbcc00
#
#  Caught on pass 1 by FOUR seats independently naming 0xaabbcc00 -- grok, glm, the kimi
#  substitute and codex -- against a brief that had stated 0xaabbccdd.  **The dropped byte is
#  CORRECT BEHAVIOUR, not residual corruption**, which is exactly the distinction a row
#  asserting the source value could never draw.
DRAWMODE   = 0x002000f8           # XFER_EN 0x200000 | PLANEMASK 0x80 | BYTEMASK 0x78
PRIM_RECT  = 0x03020000           # DE_PRIM_RECTANGLE 0x03000000 | DE_PRIM_TB 0x00020000

TILE_PHYS  = 0x10000              # re_linear_a[0] = 0x10 -> (0x10 << 12)
DST_KSEG1  = 0xa0000000 + TILE_PHYS          # x = 0    -> ofs 0
SRC_OFS    = 0x40
SRC_KSEG1  = 0xa0000000 + TILE_PHYS + SRC_OFS  # x = 0x40 -> ofs 0x40
SRC_VAL    = 0xaabbccdd           # bit 31 SET: random() (31-bit) can never equal it
DST_PAINT  = 0x11111111           # pre-paint, so "left untouched" is distinguishable
FG_VAL     = 0x77665544           # DISTINCTIVE and NON-ZERO on purpose: with fg = 0 the rows
                                  # "left *color untouched" and "zeroed *color" are the SAME
                                  # observation and the oracle is vacuous by construction.

OP_NOP      = 0x00000000
OP_B_SELF   = 0x1000ffff
OP_SW_T0_A3 = 0xace80000          # sw $t0, 0($a3)
OP_SD_T0_A3 = 0xfce80000          # sd $t0, 0($a3)
OP_LW_V0_AT = 0x8c220000          # lw $v0, 0($at)

rows = []
def row(name, got, want, note="", negate=False):
    ok = (got != want) if negate else (got == want)
    rows.append((name, ok))
    print("%-16s %-12s %-12s %-44s %s" % (name, str(got), ("NOT " if negate else "") + str(want),
                                          note, "ok" if ok else "FAIL"))
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
    #  MASK TO 32 BITS.  `lw' sign-extends into a 64-bit register, so a value with bit 31 set
    #  reads back as 0xffffffffaabbccdd and a row comparing raw strings fails on FORMATTING
    #  rather than on behaviour -- measured on this probe's first run.  The shipped
    #  sgi_re_width_probe.py carries the same normalisation for the same reason.
    m = re.search(r"print\s+%s\s*\n\s*(0x[0-9a-f]+)" % reg, t)
    return "absent" if not m else "0x%x" % (int(m.group(1), 16) & 0xffffffff)

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

def setup(A, src_mode, dst_mode=None, stepx=4, tiled_src=False):
    """Program the engine, paint source and destination, then fire one rectangle.
       Every store is a REAL GUEST INSTRUCTION through memory_rw -- no device_add,
       no debugger `put' to a device register."""
    #  *** THE 64-BIT STORE WRITES THE HIGH WORD TO [n] AND THE LOW WORD TO [n+1]. ***  Measured:
    #  `sd' of 0x10 gave `re_linear_a[0] = 0, [1] = 0x10', so the tile pointer was 0 and every pixel
    #  went to PHYSICAL ADDRESS 0 -- the destination stayed at its pre-paint and the ACCEPT control
    #  failed, which is precisely the "do not leave it 0: that writes phys 0" trap grok named.  The
    #  value below puts 0x10 in the HIGH word so re_linear_a[0] = 0x10.
    c  = store(A, RE_LINEAR_A, 0x0000001000000000, op=OP_SD_T0_A3)  # sd: a 4-byte sw is DECLINED here
    c += store(A, DST_KSEG1, DST_PAINT)
    c += store(A, SRC_KSEG1, SRC_VAL)
    if tiled_src:
        #  *** re_tlb_a IS uint16_t[256] AND ITS STORE LOOP IS PER-HALFWORD, WHICH IS NOT
        #  RE_LINEAR_A'S SHAPE.  Getting this wrong is what the row caught on its first run. ***
        #      for (hwi = 0; hwi < len; hwi += 2)
        #              d->re_tlb_a[tlbi] = data[hwi]*256 + data[hwi+1];
        #  So an 8-byte store fills re_tlb_a[0..3] from FOUR big-endian halfwords, and the one
        #  that lands in [0] is bits 63..48.  `TLBA_TILE << 32' -- the shift RE_LINEAR_A needs,
        #  because re_linear_a is uint32_t -- puts the value in re_tlb_a[2] and leaves [0] at
        #  zero, giving tileptr 0 and a DECLINED get.  Measured: the row read FG_VAL
        #  (0x77665544), which this probe's own DE_FG comment names as what a declined GET
        #  leaves.  **The row reported my setup error instead of passing quietly.**
        c += store(A, RE_TLB_A, TLBA_TILE << 48, op=OP_SD_T0_A3)
        for a in TLBA_ROWS:
            c += store(A, a, SRC_VAL)
    c += store(A, DE_MODE_DST,   MODE_LIN_A if dst_mode is None else dst_mode)
    c += store(A, DE_MODE_SRC,   src_mode)
    c += store(A, DE_DRAWMODE,   DRAWMODE)
    c += store(A, DE_XFER_ADDR,  0 if tiled_src else SRC_OFS)   # linear: src_x = addr_src (a BYTE
                                                      # offset).  Tiled: src_x is a PIXEL
                                                      # coordinate, so 0 is the tile's origin.
    c += store(A, DE_XFER_STEPX, stepx)                # must equal src bufdepth or the XFER arm warns
    c += store(A, DE_FG,         FG_VAL)               # what a declined GET leaves in `color'
    c += store(A, DE_XVERTEX_0,  0x00000000)           # (x1,y1) = (0,0)
    #  *** (x2,y2) = (0,3): ONE COLUMN, FOUR ROWS.  The height is load-bearing and the width must
    #  NOT be used instead. ***  (The latch row that needed the height lives in the probe this
    #  file was copied from, not here -- but the geometry is kept so the two sessions stay
    #  comparable, and because LIN_A addressing is `ofs = x & 4095' either way.
    #  is the announcement COUNT -- which cannot vary at all if the rectangle is one pixel, because an
    #  unlatched announce then also fires exactly once.  Measured: with (0,0)-(0,0) the M_NOLATCH
    #  mutant scored 8/8, a clean escape, and the row was VACUOUS BY CONSTRUCTION.
    #  It is the HEIGHT and not the width because LIN_A addressing is `ofs = x & 4095' -- y is
    #  ignored -- so four ROWS write the same byte four times (the value oracle survives) while four
    #  COLUMNS would write overlapping bytes at ofs 0..3 and destroy it.
    c += store(A, DE_XVERTEX_1,  0x00000003)           # (x2,y2) = (0,3): 4 pixels, all at ofs 0
    c += store(A, DE_PRIM_START, PRIM_RECT)            # PRIMITIVE|START fires the draw
    return c

print("sgirergbroundtrip RUNG-3 WITNESS -- binary=%s label=%s" % (BIN, LABEL))
print("%-16s %-12s %-12s %-44s %s" % ("row", "got", "want", "note", ""))

# ---------------------------------------------------------------- controls
A = Addr(CODE)
t, alive = session(store(A, SCRATCH, LIVE_VAL) + load(A, SCRATCH) + ["print v0"])
row("live", printed(t, "v0") if alive else "died", "0x%x" % LIVE_VAL,
    "LIVENESS: guest store then load, through RAM")

A = Addr(CODE)
t, alive = session(load(A, DE_STATUS) + ["print v0"])
row("devsig", printed(t, "v0") if alive else "died", DE_STAT,
    "DEVSIG: CRIME_DE_STATUS reads 0x1e000000; RAM reads 0")

# ---------------------------------------------------------------- the accept control
#  Both modes LIN_A: the copy is the operation the defect corrupts.  If this row does not
#  land the source value, the probe has not driven the engine and the defect row below is
#  VACUOUS -- which is why it is a row and not an assumption.
A = Addr(CODE)
t, alive = session(setup(A, MODE_LIN_A) + load(A, DST_KSEG1) + ["print v0"])
row("copy lin_a", printed(t, "v0") if alive else "died", "0x%x" % SRC_VAL,
    "ACCEPT: LIN_A source copies to the destination")

# ---------------------------------------------------------------- the defect
#  Source RGB, destination RGBA.  The XFER GET decodes the source with the RGB arm and the PUT
#  encodes it with the RGBA arm, so the destination shows exactly what the RGB GET produced.
#
#  *** THESE ROWS ARE WRITTEN RED-NOW / GREEN-AFTER, WHICH IS THE ONLY SHAPE A WITNESS MAY SHIP IN.
#  An earlier draft had them the other way round -- asserting the CORRUPT value, so both would have
#  gone RED the moment the fix landed.  That is a fine one-shot demonstration and an unshippable
#  gate row, and the ladder says so in clause (i): a witness shows the symptom on the pre-fix
#  committed HEAD AND GOES GREEN POST-FIX WITH THE SAME SCRIPT.  The exact pre-fix value is not
#  lost by the inversion -- it is pinned by `rgb not corrupt' below and printed in the GOT column
#  of every run, so the pre-fix log records it verbatim without any row having to expect it. ***
A = Addr(CODE)
t, alive = session(setup(A, MODE_RGB) + load(A, DST_KSEG1) + ["print v0"])
got_rgb = printed(t, "v0") if alive else "died"

#  THE FIX'S SUCCESS CRITERION.  RED on the committed build (it reads 0xbbccdd00), GREEN once
#  GET RGB reads buf[0..2].  It pins the EXACT post-fix value rather than merely "not the corrupt
#  one", so a fix that moves the bytes to some THIRD wrong place still reds.
row("rgb chan", got_rgb, "0x%x" % RGB_FIXED,
    "R,G,B must survive at their own byte offsets; the pad is not carried")

#  FLOOR CLAUSE (b): reds if the removed defect is reinstated VERBATIM.  It is not redundant with
#  the row above -- that one fails for ANY wrong value, this one names the SPECIFIC wrong value, so
#  a future edit that reintroduces the off-by-one is distinguishable from one that breaks the copy
#  some other way.  Both are needed and neither implies the other.
row("rgb not corrupt", got_rgb, "0x%x" % RGB_CORRUPT,
    "must not be the buf[1..3] shift: 0xaabbccdd -> 0xbbccdd00", negate=True)

row("rgb alive", "alive" if alive else "died", "alive",
    "the host survives: this is a wrong-value defect, not a kill")

# ---------------------------------------------------------------- same-mode RGB -> RGB
#  *** ASKED FOR INDEPENDENTLY BY TWO PASS-1 SEATS, and the reason is coverage this file did not
#  have: every row above is an RGB->RGBA copy, so the RGB *PUT* arm is never executed. ***
#      grok: "pin both with a same-mode RT row AND a raw-memory GET whose byte 3 is nonzero"
#      glm:  "a same-mode RGB->RGB copy, raw-seeded -- the most guest-realistic corruption
#             (today every pixel word shifts left 8) and the natural detector row; S4 is
#             RGB->RGBA only"
#
#  It is also the shape a real guest takes, which the mixed-mode row is not: a driver that has
#  programmed RGB does not usually change the destination type mid-copy.
#
#  THE VALUES ARE THE SAME AS THE MIXED-MODE ROW, AND THAT IS NOT REDUNDANCY.  PUT RGB writes the
#  top three bytes of whatever GET produced and zeroes buf[3], so the destination word matches the
#  RGBA case -- but the code path executed is different, so a mutant in the RGB PUT arm reds HERE
#  and is invisible to every row above.
#
#  grok's "byte 3 nonzero" condition is met by SRC_VAL itself: 0xaabbccdd has 0xdd at byte 3, so
#  this row additionally proves the pad is NOT carried rather than merely being zero already.
A = Addr(CODE)
t, alive = session(setup(A, MODE_RGB, dst_mode=MODE_RGB) + load(A, DST_KSEG1) + ["print v0"])
got_same = printed(t, "v0") if alive else "died"

row("rgb samemode", got_same, "0x%x" % RGB_FIXED,
    "RGB->RGB: exercises the RGB PUT arm, which no other row reaches")

# ---------------------------------------------------------------- the WIDTH axis
#  *** THIS ROW CLOSES A MEASURED CLAUSE-(d) FLOOR BREACH.  L2, repaired in-round. ***
#
#  Table 1 built the canonical clause-(d) mutant -- guard KEPT, repair CONDITIONED on a field the
#  guarded body reads:
#
#      case DE_MODE_TYPE_RGB:
#              if (bufdepth == 4)
#                      *color = (buf[0] << 24) + (buf[1] << 16) + (buf[2] << 8);   /* the fix */
#              else
#                      *color = (buf[1] << 24) + (buf[2] << 16) + (buf[3] << 8);   /* the defect */
#
#  and it scored a CLEAN SWEEP, 6/6, against every row above -- because EVERY session in this file
#  used BUFDEPTH_32, so bufdepth is 4 in all of them and the mutant's fix branch is the only one the
#  detector ever executes.  **The detector proved the fix works exactly where it was measured and
#  said nothing about anywhere else.**
#
#  `bufdepth' is squarely inside the DEPENDS-ON closure: it is read by the guarded body (it is
#  memory_rw's transfer length) and it comes from bits 8-9 of the SAME mode word whose bits 4-7 the
#  guard reads.  So this is not an exotic mutant -- it is the shape the closure enumerates first.
#
#  Driving a SECOND width is what makes the width axis observable at all.  bufdepth 8 keeps
#  buf[0..2] filled by memory_rw, so the expected value is unchanged and the row stays a value
#  oracle; bufdepth 1 or 2 would leave buf[1..2] uninitialised, which is `sgirebufuninit' and would
#  make this row non-deterministic -- so 8 is the only other width that can carry a value oracle.
A = Addr(CODE)
t, alive = session(setup(A, MODE_RGB64, stepx=8) + load(A, DST_KSEG1) + ["print v0"])
got_d64 = printed(t, "v0") if alive else "died"

row("rgb depth64", got_d64, "0x%x" % RGB_FIXED,
    "the fix must hold at bufdepth 8, not only at the width the other rows use")

# ---------------------------------------------------------------- the ADDRESSING-MODE axis
#  *** THIS ROW CLOSES A SECOND MEASURED CLAUSE-(d) FLOOR BREACH, found by pass 2. ***
#
#  Mutant M12_linear -- guard kept, repair conditioned on `linear':
#
#      case DE_MODE_TYPE_RGB:
#              if (linear) *color = (buf[0]<<24)+(buf[1]<<16)+(buf[2]<<8);   /* the fix    */
#              else        *color = (buf[1]<<24)+(buf[2]<<16)+(buf[3]<<8);   /* the defect */
#
#  scored **8/8, a CLEAN SWEEP**, because every row above drives LIN_A (tlb_mode 4) and `linear' is
#  therefore true in all of them.  `linear' is `tlb_mode > 3' and it DOMINATES the edited lines via
#  the `if (!linear && (x < 0 || ...)) return;' guard, so it sits inside the DEPENDS-ON closure --
#  this is a floor breach, not coverage debt.
#
#  The seat that named the axis proposed conditioning on `tileptr'.  That cannot work as stated:
#  `tileptr &= ~0x80000000' strips the linear flag BEFORE the switch, so `tileptr' carries no
#  addressing-mode information by the time the arm runs.  `linear' is the variable that survives, and
#  building the mutant in the form the source permits is what turned a prediction into a measurement.
#
#  THE SOURCE is tiled and the DESTINATION stays LIN_A, deliberately: the RGB arm under test is the
#  GET, and the GET's `linear' comes from src_mode.  A tiled DESTINATION would exercise the PUT and
#  leave this mutant untouched.
A = Addr(CODE)
t, alive = session(setup(A, MODE_RGB_TLBA, tiled_src=True) + load(A, DST_KSEG1) + ["print v0"])
got_tiled = printed(t, "v0") if alive else "died"

row("rgb tiled", got_tiled, "0x%x" % RGB_FIXED,
    "the fix must hold for a TILED source, not only for LIN_A")

# ---------------------------------------------------------------- the JOINT cell
#  *** THIS ROW CLOSES THE CROSS-PRODUCT, AND IT EXISTS BECAUSE I REPAIRED CELL-BY-CELL TWICE. ***
#
#  Two axes were each closed on their own:  WIDTH by `rgb depth64' (LIN_A, bufdepth 8) and
#  ADDRESSING by `rgb tiled' (tiled, bufdepth 4).  That leaves a 2x2 with one corner empty:
#
#                     bufdepth 4                  bufdepth 8
#      LIN_A          rgb chan / rgb samemode     rgb depth64
#      tiled          rgb tiled                   *** was UNROWED ***
#
#  and a repair conditioned on `(bufdepth == 4 || linear)' is TRUE in all three rowed cells, so it
#  scores 9/9 BY CONSTRUCTION.  Three pass-3 seats named that cell independently -- grok, the kimi
#  substitute and deepseek -- and the kimi seat wrote the mutant out in exactly that form.
#
#  The carrier's class-closure amendment is explicit about the remedy: when two consecutive passes
#  find breaches of ONE CLASS, the next repair owes the CLASS CLOSURE -- enumerate the full space and
#  close every cell in ONE diff, rather than adding the cell the latest mutant happened to name.
#  **Repairing at exactly the address the mutant used is what produced breaches two and three.**
#
#  Geometry check for bufdepth 8 under tiled addressing: tilewidth_in_pixels = 512/8 = 64, so
#  tile_nr = (y>>7)*16 + x/64 = 0 for x=0, y=0..3, and ofs = 512*y + (x % 64)*8 = 512*y -- the same
#  four source rows TLBA_ROWS already paints.  No new setup is needed, only the mode and the step.
A = Addr(CODE)
t, alive = session(setup(A, MODE_RGB_TLBA64, tiled_src=True, stepx=8)
                   + load(A, DST_KSEG1) + ["print v0"])
got_t64 = printed(t, "v0") if alive else "died"

row("rgb tiled64", got_t64, "0x%x" % RGB_FIXED,
    "the JOINT cell: tiled source AND bufdepth 8, which no other row reaches")

ok = sum(1 for _, o in rows if o)
print("")
print("SGIRGB_RESULT=%d/%d" % (ok, len(rows)))
print("SGIRGB_WITNESS=%s" % ("PASS" if ok == len(rows) else "FAIL"))
print("SGIRGB_DONE")
sys.exit(0 if ok == len(rows) else 1)
