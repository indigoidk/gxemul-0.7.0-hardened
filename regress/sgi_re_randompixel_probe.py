#!/usr/bin/env python3
#
#  sgirandompixel -- RUNG-3 WITNESS for dev_sgi_re.c horrible_getputpixel().
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
#    CATCHES   the default arm substituting a value instead of declining: `copy lin_b' reds if the
#              destination receives anything other than a value distinct from BOTH the source and
#              the pre-painted destination.  Restoring `exit(1)' there kills the machine and reds
#              every row.  Making the arm leave *color untouched turns `copy lin_b' green-by-accident
#              ONLY if the pre-paint is removed -- which is why the destination is PRE-PAINTED with a
#              known value and the row rejects it: "left alone" and "wrote random" are then distinct.
#              [#556, 2026-10-02 -- a records correction; the text above is kept as it was written] Under CATCHES,
#              the defect rows are lin_b not src and lin_b is fg: the first wants the destination unequal to the
#              source, and the second wants FG exactly, not an inequality against both source and pre-paint.
#              Restoring exit(1) kills only the LIN_B session; earlier controls are separate sessions and stay
#              green.  (hbundle_regress28:F11:
#              regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md)
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
MODE_LIN_B = 0x1620               # LIN_B 0x1400 | BUFDEPTH_32 0x200 | TYPE_RGBA 0x20
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

def setup(A, src_mode):
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
    c += store(A, DE_MODE_DST,   MODE_LIN_A)
    c += store(A, DE_MODE_SRC,   src_mode)
    c += store(A, DE_DRAWMODE,   DRAWMODE)
    c += store(A, DE_XFER_ADDR,  SRC_OFS)              # linear: src_x = addr_src, src_y = 0
    c += store(A, DE_XFER_STEPX, 4)                    # must equal src bufdepth or the XFER arm warns
    c += store(A, DE_FG,         FG_VAL)               # what a declined GET leaves in `color'
    c += store(A, DE_XVERTEX_0,  0x00000000)           # (x1,y1) = (0,0)
    #  *** (x2,y2) = (0,3): ONE COLUMN, FOUR ROWS.  The height is load-bearing and the width must
    #  NOT be used instead. ***  `lin_b diag once' pins that the announce is LATCHED, and its channel
    #  is the announcement COUNT -- which cannot vary at all if the rectangle is one pixel, because an
    #  unlatched announce then also fires exactly once.  Measured: with (0,0)-(0,0) the M_NOLATCH
    #  mutant scored 8/8, a clean escape, and the row was VACUOUS BY CONSTRUCTION.
    #  It is the HEIGHT and not the width because LIN_A addressing is `ofs = x & 4095' -- y is
    #  ignored -- so four ROWS write the same byte four times (the value oracle survives) while four
    #  COLUMNS would write overlapping bytes at ofs 0..3 and destroy it.
    c += store(A, DE_XVERTEX_1,  0x00000003)           # (x2,y2) = (0,3): 4 pixels, all at ofs 0
    c += store(A, DE_PRIM_START, PRIM_RECT)            # PRIMITIVE|START fires the draw
    return c

print("sgirandompixel RUNG-3 WITNESS -- binary=%s label=%s" % (BIN, LABEL))
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
#  LIN_B source: the GET hits `default:', sets *color = random(), and the PUT writes it.
#  Two rows, because one is not enough: the value must differ from the SOURCE (so the copy
#  did not happen) AND from the PRE-PAINT (so the destination was actually written).
A = Addr(CODE)
t, alive = session(setup(A, MODE_LIN_B) + load(A, DST_KSEG1) + ["print v0"])
got_b = printed(t, "v0") if alive else "died"
row("lin_b not src", got_b, "0x%x" % SRC_VAL,
    "the copy did not happen -- true before AND after the fix", negate=True)
#  *** THE INVERTING ROW.  It is RED on the committed build (which writes random()) and GREEN once the
#  `*color = random()' assignment is deleted, because the caller's `uint32_t color = fg' then stands.
#  It also discriminates every REJECTED disposition: zeroing leaves 0, suppressing the PUT leaves the
#  pre-paint, implementing LIN_B leaves the source.  Only "leave *color alone" leaves FG.
row("lin_b is fg", got_b, "0x%x" % FG_VAL,
    "FIX: a declined GET leaves *color, so the PUT writes FG")
row("lin_b alive", "alive" if alive else "died", "alive",
    "the host survives: the arm's exit(1) is commented out")

#  ATTRIBUTION: the value could only have come from this device's default arm.
#  ATTRIBUTION and the LATCH, in one row.  Bare presence was enough for a witness; for the fix it must
#  also pin that the announce is BOUNDED -- the house idiom is N = 1 per device instance with `(once)' in
#  the message text, and this helper is PER-PIXEL, so an unlatched announce is a per-pixel flood.  This
#  row is the discriminator against a SILENT decline (member 2), which would emit nothing at all.
n_diag = t.count("unimplemented dst_mode")
row("lin_b diag", "yes" if n_diag else "no", "yes",
    "ATTRIBUTION: the arm's own diagnostic; RAM emits no text")
row("lin_b diag once", "%d" % n_diag, "1",
    "LATCH: one announcement for FOUR pixels, not one each")

ok = sum(1 for _, o in rows if o)
print("")
print("SGIRAND_RESULT=%d/%d" % (ok, len(rows)))
print("SGIRAND_WITNESS=%s" % ("PASS" if ok == len(rows) else "FAIL"))
print("SGIRAND_DONE")
sys.exit(0 if ok == len(rows) else 1)
