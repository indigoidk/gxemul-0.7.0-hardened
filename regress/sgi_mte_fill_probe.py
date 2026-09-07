#!/usr/bin/env python3
#
#  sgimtedepth4dead -- RUNG-3 WITNESS: `if (depth == 4)' is dead, so MTE never selects RGBA.
#
#      :1311  int depth = 8 << ((mode & MTE_MODE_DEPTH_MASK) >> MTE_DEPTH_SHIFT);   /* BITS */
#      :1359  src_x1 /= (depth / 8);                     <- the author converting bits -> bytes
#      :1369  // ... this makes sure that we copy 32 bits when doing 32-bit transfers.
#      :1371  if (depth == 4) { src_mode |= DE_MODE_TYPE_RGBA; dst_mode |= ...; }
#
#  The field is two bits, so `depth' is 8/16/32/64 -- never 4.  The branch is dead, the constructed
#  modes carry no type bits, `color_mode' stays CI, and CI's PUT assigns buf[0] only while the
#  transfer moves `bufdepth' bytes.
#
#  *** IT BEGAN AS A 6-ROW WITNESS AND IS NOW A 14-ROW DETECTOR.  The banner that used to stand
#  here -- "a witness, not a detector; its rows are expected to FAIL; it must not be gated" --
#  was true of the 6-row version against HEAD and is FALSE of this one, which scores 14/14 on the
#  fix and 10/14 on a verbatim reinstatement.  The pass-2 codex seat caught the staleness. ***
#
#  It is STILL NOT WIRED INTO A GATE, and that is a separate decision from what it is.
#
#  ---------------------------------------------------------------------------------------------
#  THE ORACLE IS `dest[0]' OF A TILED **FILL**, AND EVERY OTHER CHANNEL I PROPOSED WAS REFUSED.
#  From the grok design review, each point measured against the source rather than argued:
#
#  * A PRE-PAINTED TAIL CANNOT WORK.  CI PUT does not replicate buf[0] across the span and does not
#    leave a tail: it writes buf[0] at the lowest address and buf[1..bufdepth-1] as uninitialised
#    stack, and memory_rw memcpys `bufdepth' bytes.  So the paint is OVERWRITTEN WITH GARBAGE.  A row
#    asserting "tail still painted" reds on HEAD because the path RAN -- which reads as "the witness
#    never reached MTE".  A row asserting "tail != paint" is true on HEAD *and* after the fix.
#
#  * COPY CANNOT WITNESS THIS AT ALL.  Source `aa bb cc dd': CI GET takes buf[0] == 0xaa and CI PUT
#    writes 0xaa at dest[0]; RGBA GET reconstructs 0xaabbccdd and RGBA PUT also writes 0xaa there.
#    The first byte of a copy is the one byte CI already gets right, and the broken bytes are exactly
#    the uninitialised ones that must not be read.  "If the witness is a blit, refuse it."
#
#  * FILL IS DETERMINISTIC BECAUSE IT NEVER GETs.  With bg = 0x11223344:
#        CI   PUT -> buf[0] = (uint8_t)bg          -> dest[0] = 0x44   (the LOW byte)
#        RGBA PUT -> [bg>>24, bg>>16, bg>>8, bg]   -> dest[0] = 0x11   (the HIGH byte)
#    dest[1..3] are uninitialised on HEAD.  **DO NOT ASSERT THEM THERE.**
#
#  *** THAT SENTENCE USED TO END "only the top byte of the big-endian word is READ", WHICH IS
#  FALSE AND WAS CAUGHT BY THE PASS-1 CODEX SEAT.  The probe executes `lw' and masks afterwards:
#  it READS four bytes and ASSERTS one.  Corrected 2026-09-07 -- the distinction matters because
#  the tail IS assertable once the fix lands (RGBA writes all four), which is what `fill bot'
#  below now does. ***
#
#  * TLB_A WITHOUT BIT 15 RETURNS SILENTLY and leaves the destination painted, which looks like "MTE
#    did nothing".  sgi_re_rgb_probe.py paid for that trap twice; TLBA_TILE = 0x8002 is why.
#
#  * MTE LIN_A/B at depth 32 would `exit(1)' in the LINEAR arm -- host death, not a red row.
#
#  Usage:  sgi_mte_fill_probe.py <gxemul-binary> [label]
import os, sys, pty, select, time, re

BIN   = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "?"

rows = []
def row(name, got, want, note="", negate=False):
    ok = (got != want) if negate else (got == want)
    rows.append((name, ok))
    shown = ("NOT " + str(want)) if negate else str(want)
    print("%-12s %-14s %-16s %-52s %s" % (name, str(got), shown, note, "ok" if ok else "FAIL"))
    return ok

# ---------------------------------------------------------------- guest instructions
OP_SW_T0_A3 = 0xace80000          # sw   $t0, 0($a3)
OP_SD_T0_A3 = 0xfce80000          # sd   $t0, 0($a3)
OP_LW_V0_AT = 0x8c220000          # lw   $v0, 0($at)
OP_B_SELF   = 0x1000ffff          # b    .
OP_NOP      = 0x00000000

CODE      = 0x80001000
SCRATCH   = 0xa0001800
LIVE_VAL  = 0x5a5a5a5a
SENTINEL  = 0xdeadbeef
DE_STATUS = 0xb5004000
DE_STAT   = "0x1e000000"          # CRIME_DE_STATUS; RAM reads 0 -- the device signature

#  *** A LOAD FILE IS REQUIRED, NOT COSMETIC.  `main.c' with extra_argc == 0 and no `-d' prints
#  "No filename given. Aborting." and exit(1) -- so the FIRST DRAFT OF THIS PROBE COULD NOT START,
#  and its `fill ran' row would have reported GREEN on that (see the row's own comment). ***
#  `-M 64' is copied from the siblings for uniformity only: IP32 defaults to 128 MB and DEST is at
#  128 KB, so it changes nothing here.
DUMMY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sgi_mte_dummy.bin")
if not os.path.exists(DUMMY):
    with open(DUMMY, "wb") as f:
        f.write(b"\0" * 8)

# ---------------------------------------------------------------- the MTE registers
#  CRIME RE base 0xb5000000; CRIME_MTE_* offsets from crmfbreg.h.
MTE_MODE       = 0xb5003000
MTE_BG         = 0xb5003018
MTE_DST0       = 0xb5003030
MTE_DST1_START = 0xb5003838       # CRIME_MTE_DST1 0x3038 | CRIME_DE_START 0x0800
#  `if (startFlag) do_mte_transfer(cpu, d);' sits at the END of DEVICE_ACCESS(sgi_mte), so any MTE
#  write with bit 0x800 in its ADDRESS fires the transfer.  DST1 is written last, with START.

#  dst_tlb = (mode & MTE_MODE_DST_BUF_MASK 0x1c) >> 2  -> MTE_TLB_A = 0
#  depth   = 8 << ((mode & 0x300) >> 8)                -> MTE_DEPTH_32 = 2 gives 32
#  MTE_MODE_COPY 0x800 CLEAR = fill.  (0x800 here is a MODE bit; the 0x800 in the address is START.)
MODE_TILED_FILL = 0x200
BG_VAL          = 0x11223344      # four distinct bytes, so dest[0] names which arm ran
CI_TOP          = 0x44            # what the DEFECT writes at dest[0]
RGBA_TOP        = 0x11            # what a CORRECT RGBA selection writes there
PAINT           = 0x99999999      # neither -- liveness only, NOT a tail oracle
PAINT_TOP       = 0x99

#  DEPTH IS AN AXIS, NOT A CONSTANT.  Two seats independently showed the six-row witness blind to
#  an OVER-REACH mutant: `depth >= 16' fires at 32 (so `fill top' stays green) and is cold at 8
#  (so `depth8 top' stays green).  The adjacent DOCUMENTED cell -- 16 -- is what catches it.
MODE_D8    = 0x000                # MTE_DEPTH_8  << MTE_DEPTH_SHIFT
MODE_D16   = 0x100                # MTE_DEPTH_16 << MTE_DEPTH_SHIFT
MODE_D32   = 0x200                # MTE_DEPTH_32 << MTE_DEPTH_SHIFT
#  *** FIELD VALUE 3.  The header defines NO MTE_DEPTH_64, but the code computes 8 << 3 = 64 for
#  it, and the branch under repair is reachable there.  A row here does NOT assert what 64bpp
#  OUGHT to do -- it asserts what this round does NOT CHANGE, exactly like depth8/depth16. ***
MODE_D64   = 0x300                # field value 3: undefined by the header, computed as 64
MODE_COPY  = 0x800                # MTE_MODE_COPY (a MODE bit; the 0x800 in an ADDRESS is START)
MTE_SRC0   = 0xb5003020           # CRIME_MTE_SRC0 0x3020 -- no 0x800, so it does not fire START

#  *** THE FIRST SOURCE BYTE IS DELIBERATELY BELOW 0x80. ***  The RGB and RGBA GET arms compute
#  `buf[0] << 24' on a uint8_t, which promotes to signed int -- so a first byte >= 0x80 shifts
#  past INT_MAX and is undefined behaviour.  That is a SEPARATE filed defect ([[sgirebufshiftub]],
#  re-derived independently by the pass-1 codex seat); this probe must not stand on it, so the
#  copy rows use 0x1a as byte 0.  Four distinct bytes, so each names its own position.
#  (An earlier draft said "EVERY GET arm".  False, and the pass-2 codex seat caught it: CI shifts
#  nothing at all, and ABGR and the default arm shift `buf[3]', not `buf[0]'.  Four of five arms,
#  two of them a different byte.  The filed [[sgirebufshiftub]] row's own TITLE carried the same
#  overclaim and is corrected there too.)
SRC_WORD   = 0x1a2b3c4d
SRC_B0     = 0x1a                 # what BOTH correct copy shapes put at dest[0]
SRC_B1     = 0x2b                 # what only a REAL RGBA copy puts at dest[1]
SRC_B3     = 0x4d                 # the byte RGB DROPS -- the only channel that sees it
SRC_PIX_X  = 4                    # src0's x field; /(depth/8) = 1 -> source byte offset 4

RE_TLB_A   = 0xb5001000
TLBA_TILE  = 0x8002               # re_tlb_a[0].  BIT 15 IS THE VALID BIT.
TLBA_PHYS  = (TLBA_TILE << 16) & ~0x80000000       # -> 0x20000
DEST       = 0xa0000000 + TLBA_PHYS                # pixel (0,0) of the tile

#  dst0/dst1 pack as x=(v>>16)&0xfff, y=v&0xfff.  Both zero draws exactly one pixel at (0,0):
#  `for (y = y1; y != y2+dy; y += dy)' with dy = 1 runs once.
DST0 = 0x00000000
DST1 = 0x00000000

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

def topbyte(s):
    if not s.startswith("0x"):
        return s
    return "0x%02x" % ((int(s, 16) >> 24) & 0xff)

def byte_n(s, n):
    """Byte n of the big-endian word, n = 0 at the LOWEST address."""
    if not s.startswith("0x"):
        return s
    return "0x%02x" % ((int(s, 16) >> (8 * (3 - n))) & 0xff)

def fill(A, depth=MODE_D32):
    """Program a tiled FILL at `depth' and fire it.  Every store is a REAL GUEST INSTRUCTION."""
    #  re_tlb_a[0] = 0x8002.  The RE TLB write walks `len' in halfwords from tlbi 0, so an `sd'
    #  carrying the tile in its TOP halfword lands it at index 0 -- the packing sgi_re_rgb_probe.py
    #  established, and getting it wrong leaves the valid bit clear and the transfer silent.
    c  = store(A, RE_TLB_A, TLBA_TILE << 48, op=OP_SD_T0_A3)
    c += store(A, DEST, PAINT)                     # pre-paint: liveness, NOT a tail oracle
    c += store(A, MTE_MODE, depth)
    c += store(A, MTE_BG,   BG_VAL)
    c += store(A, MTE_DST0, DST0)
    c += store(A, MTE_DST1_START, DST1)            # START fires do_mte_transfer()
    return c

def copy(A):
    """Tiled 32-bit COPY of ONE pixel: source (1,0) -> dest (0,0), both in TLB_A's tile.

    These rows exist because a FILL never reads `src_mode': deleting only
    `src_mode |= DE_MODE_TYPE_RGBA' is invisible to every fill row.  Three seats confirmed both
    the prediction and the byte walk.  dest[0] is 0x1a under BOTH correct shapes -- so `copy top'
    distinguishes neither HEAD nor the fix, and that IS its job: it reds only under a ONE-SIDED
    edit (source-only -> 0x4d, dest-only -> 0x00).

    A note the kimi seat asked for, so a future reader does not "correct" the want: the
    dest-only cell gives 0x00 because the CI GET *assigns* `*color = buf[0]', zero-extending it.
    Had the GET left `bg' untouched, an RGBA PUT would have emitted bg>>24 instead.  The row is
    right; the reason is the assignment, not "the high byte of a low-byte colour" in general.

    The destination is PRE-PAINTED so that a transfer which silently does nothing (an invalid
    TLB entry, say) reports 0x99 rather than looking like a plausible byte."""
    c  = store(A, RE_TLB_A, TLBA_TILE << 48, op=OP_SD_T0_A3)
    c += store(A, DEST + 4, SRC_WORD)              # the source pixel, four distinct bytes
    c += store(A, DEST,     PAINT)                 # the destination, so a no-op is visible
    c += store(A, MTE_MODE, MODE_D32 | MODE_COPY)
    c += store(A, MTE_SRC0, SRC_PIX_X << 16)       # src x=4 -> pixel 1 at depth 32, y=0
    c += store(A, MTE_DST0, DST0)
    c += store(A, MTE_DST1_START, DST1)            # START fires do_mte_transfer()
    return c

print("sgi_mte_fill_probe -- binary=%s label=%s machine=sgi/ip32" % (BIN, LABEL))
print("%-12s %-14s %-16s %-52s %s" % ("row", "got", "want", "note", ""))

A = Addr(CODE)
t, alive = session(store(A, SCRATCH, LIVE_VAL) + load(A, SCRATCH) + ["print v0"])
row("live", printed(t, "v0") if alive else "died", "0x%x" % LIVE_VAL,
    "LIVENESS: guest store then load, through RAM")

A = Addr(CODE)
t, alive = session(load(A, DE_STATUS) + ["print v0"])
row("devsig", printed(t, "v0") if alive else "died", DE_STAT,
    "DEVSIG: CRIME_DE_STATUS reads 0x1e000000; RAM reads 0")

#  *** THE PAINT MUST BE PINNED AT THE ORACLE ADDRESS, IN ITS OWN SESSION. ***
#  `live' proves RAM works at SCRATCH, which is NOT where the fill lands.  Without this row an
#  inequality against the paint passes on zeros, on the leftover sentinel, on a missed print and
#  on a dead session.  A SEPARATE session because `printed()' returns the FIRST match: two reads
#  of v0 in one session return the same sample.
A = Addr(CODE)
t, alive = session(store(A, DEST, PAINT) + load(A, DEST) + ["print v0"])
row("paint ok", topbyte(printed(t, "v0")) if alive else "died", "0x%02x" % PAINT_TOP,
    "CONTROL: the paint really lands AT the oracle address, not just at SCRATCH")

A = Addr(CODE)
t, alive = session(fill(A) + load(A, DEST) + ["print v0"])
got = topbyte(printed(t, "v0")) if alive else "died"

row("fill alive", "alive" if alive else "died", "alive",
    "CONTROL: the host survives a tiled 32-bit fill")
#  *** AN INEQUALITY AGAINST THE PAINT PASSES ON EVERY NON-OUTCOME. ***  0x00 (paint never
#  landed), 0xde (the `lw' never ran, v0 still SENTINEL), "absent" (the print regex missed) and
#  "died" (gxemul never started) are all != 0x99, so the first draft scored them all GREEN.
#  Stated POSITIVELY instead: dest[0] must be a byte the fill can actually produce, so each of
#  those four is a FAILURE that names itself in the got column.
produced = got in ("0x%02x" % CI_TOP, "0x%02x" % RGBA_TOP)
row("fill ran", "yes" if produced else got, "yes",
    "CONTROL: dest[0] is 0x%02x (CI) or 0x%02x (RGBA) -- not paint/zero/sentinel/died"
    % (CI_TOP, RGBA_TOP))
#  *** THE DEFECT ROW.  It asserts the CORRECT byte and is expected to FAIL on HEAD. ***
row("fill top", got, "0x%02x" % RGBA_TOP,
    "dest[0] must be bg>>24 (RGBA), not (uint8_t)bg = 0x%02x (CI)" % CI_TOP)

#  *** `fill top' CANNOT TELL RGBA FROM RGB, AND THAT MUTANT PASSES EVERY OTHER ROW HERE. ***
#  Found independently by two seats.  The RGB PUT arm writes {bg>>24, bg>>16, bg>>8, 0x00} --
#  IDENTICAL to RGBA at dest[0], different at dest[3].  So a one-token `|= DE_MODE_TYPE_RGB'
#  substitution is invisible to dest[0] no matter how many fill rows exist.
#
#  The tail is assertable only once the fix is in, because CI leaves dest[1..3] as host stack.
#  So this row is GATED on the leading byte proving the RGBA arm ran: on HEAD it reports `n/a'
#  and FAILS -- deterministically, naming its own reason -- instead of scoring a nondeterministic
#  stack byte.  Honest in all three states:
#      HEAD (CI)      n/a: dest[0] not RGBA   FAIL
#      fixed (RGBA)   0x44                    ok
#      fixed + RGB    0x00                    FAIL
#  `printed()' returns the FIRST match, which is what is wanted here: `got' and `fullword' are
#  deliberately the SAME sample, read at two byte positions.
#
#  *** THE GATE IS ONE SHARED FLAG COMPUTED FROM THE **FILL** SESSION, NOT A PER-ROW TEST. ***
#  It is named `fill_top_ok' and not `rgba_ran' on the pass-2 codex seat's correction: fill
#  dest[0] == 0x11 is produced by the RGB arm as well as by RGBA, so the flag means "the fill PUT
#  put bg>>24 at dest[0]" -- NOT "RGBA specifically ran".  `fill bot' is the row that separates
#  those two.  A flag whose name overclaims is how a future reader builds on a fact nobody has.
#  The pass-2 glm seat derived this from the packet alone -- under a per-row reading the copy
#  rows could never pass, since their own dest[0] is 0x1a and not 0x11, so BASE 13/13 would be
#  impossible.  It is a FIX-PRESENCE indicator: it says the repaired branch fired at all, which
#  is the precondition for any tail byte being defined.  A copy row therefore reports n/a when
#  the FILL was CI, even if the copy path itself was fine -- see the message text below.
#
#  *** TWO MEASURED LIMITS OF THIS PROXY, both from the pass-2 grok seat, recorded rather than
#  glossed because they are the kind of thing a future round would otherwise rediscover: ***
#
#  (a) UNDER A `&& (mode & MTE_MODE_COPY)' MUTANT THE COPY ROWS ARE A WRONG-REASON KILL.  The
#      copy path there really does take RGBA -- dest[3] would be 0x4d and would PASS -- but the
#      FILL is CI, so the gate closes and both rows red anyway.  Their own bytes do not move.
#      That mutant is still killed by `fill top', so nothing escapes; but the CHANNEL those two
#      rows report under it is vacuous, and the pre-table CHANNEL check is what should have
#      caught it.
#  (b) THE DUAL, `if (depth == 32 && !(mode & MTE_MODE_COPY))', IS NOT PINNED AND CANNOT BE.
#      Every fill row stays green; `copy top' stays green because dest[0] of a same-type copy
#      is invariant; and the gate OPENS, so these two rows would score dest[1]/dest[3] of a
#      CI-CI copy -- bytes the PUT never wrote.  There is no copy-local four-byte signal that
#      is not those bytes themselves.  DISCLOSED as clause-(e) coverage debt.
#
#      *** AND THAT IS WHY M4 IS CLAUSE (e), NOT (d).  DEPENDS-ON enumerates the predicates
#      DOMINATING the edited line plus the lvalues the GUARDED BODY reads.  The guarded body is
#      exactly `src_mode |= ...; dst_mode |= ...' -- it does not read MTE_MODE_COPY, which is
#      tested later in the transfer loop and does not dominate.  Filing M4 as (d) would import
#      its dual into the FLOOR, and (b) shows that dual cannot be legitimately killed. ***
fill_top_ok = (got == "0x%02x" % RGBA_TOP)
fullword = printed(t, "v0") if alive else "died"
row("fill bot", byte_n(fullword, 3) if fill_top_ok else "n/a: FILL dest[0] not RGBA -- fix absent",
    "0x%02x" % CI_TOP,
    "dest[3] must be bg's LOW byte -- RGB writes 0x00 there and still passes `fill top'")

#  ---- THE DEPTH AXIS.  Both rows want the CI byte, because at 8 and 16 bits CI is CORRECT and
#  the branch must stay COLD.  Green on HEAD and green after the fix; they red only if the
#  repaired comparison OVER-REACHES.  16 is not optional -- it is the cell that catches
#  `depth >= 16', which 8 cannot see, and it is a DOCUMENTED encoding (MTE_DEPTH_16).
A = Addr(CODE)
t8, alive8 = session(fill(A, MODE_D8) + load(A, DEST) + ["print v0"])
row("depth8 top", byte_n(printed(t8, "v0"), 0) if alive8 else "died", "0x%02x" % CI_TOP,
    "8bpp: CI is CORRECT here -- reds under an ALWAYS-TRUE comparison.  NOT under `!= 8'")
#  *** THAT NOTE USED TO CLAIM `!= 8' TOO, AND IT IS FALSE.  Walked: `!= 8' is FALSE at depth 8,
#  so the branch stays cold and this row is GREEN.  `>= 16' and `!= 8' agree on ALL FOUR reachable
#  depths -- they are EQUIVALENT MUTANTS -- and `depth16 top' is what kills both.
#  **Table 1 had already shown it**: M7_ne8 was killed by `depth16 top' ALONE, one red, not two.
#  I read the score and not the row list.  Found by the pass-2 codex seat. ***

A = Addr(CODE)
t16, alive16 = session(fill(A, MODE_D16) + load(A, DEST) + ["print v0"])
row("depth16 top", byte_n(printed(t16, "v0"), 0) if alive16 else "died", "0x%02x" % CI_TOP,
    "16bpp: the ADJACENT documented cell -- reds under `depth >= 16', invisible at 8bpp")

#  *** ADDED BY PASS 2 AFTER A MEASURED TOTAL ESCAPE.  The glm seat derived that
#  `depth == 32' -> `depth >= 32' fires additionally at field value 3 and that NOTHING drove
#  64bpp, so it would sweep the detector.  Built and measured: 13/13, a clean sweep
#  (killtable_20260907/M9_ge32.raw).  That is a clause-(d) widening of the repaired predicate,
#  i.e. an L2 floor breach -- and `>= 32' is not hypothetical, it is option F2, which this
#  round considered and rejected on the arithmetic.
#
#  Note what this row does and does not claim.  It wants the CI byte, which is the behaviour
#  the round LEAVES ALONE at field 3; it takes no position on what 64bpp should do, which
#  nothing in the header or any local manual would warrant.
A = Addr(CODE)
t64, alive64 = session(fill(A, MODE_D64) + load(A, DEST) + ["print v0"])
row("depth64 top", byte_n(printed(t64, "v0"), 0) if alive64 else "died", "0x%02x" % CI_TOP,
    "field 3: the branch must stay COLD -- reds under `depth >= 32', which nothing else sees")

#  ---- THE COPY AXIS.  A fill never reads `src_mode', so these are the only rows that can see a
#  source-side edit.  See copy() for the byte walk and for why dest[0] is 0x1a either way.
A = Addr(CODE)
tc, alivec = session(copy(A) + load(A, DEST) + ["print v0"])
cw = printed(tc, "v0") if alivec else "died"
row("copy alive", "alive" if alivec else "died", "alive",
    "CONTROL: the host survives a tiled 32-bit copy")
row("copy top", byte_n(cw, 0), "0x%02x" % SRC_B0,
    "source byte 0 survives BOTH correct shapes -- reds only on a ONE-SIDED type edit")
#  *** THIS ROW'S NOTE USED TO SAY IT "proves the COPY path really took RGBA".  IT DOES NOT,
#  and the pass-2 grok seat measured why: an RGB GET yields dest[1] == 0x2b as well, so this
#  byte does not separate RGBA from RGB.  `copy 4th' is the row that does.  On the eight
#  mutants this row never UNIQUELY kills anything -- M3 is already killed by `copy top' and
#  `copy 4th'.  It is kept as a second reading of the same event, honestly labelled. ***
row("copy 2nd", byte_n(cw, 1) if fill_top_ok else "n/a: FILL dest[0] not RGBA -- fix absent", "0x%02x" % SRC_B1,
    "dest[1]: a FOUR-byte PUT ran.  Does NOT separate RGBA from RGB -- that is `copy 4th'")

#  *** THE SOURCE-SIDE RGB SUBSTITUTION ESCAPES ALL TWELVE ROWS ABOVE, AND THE PRE-TABLE CHECK
#  IS WHERE THAT WAS SUPPOSED TO SURFACE -- so it is closed here, before the table runs. ***
#  `src_mode |= DE_MODE_TYPE_RGB' makes the GET compute (b0<<24)+(b1<<16)+(b2<<8) -- it DROPS
#  the low byte.  dest[0] and dest[1] are unchanged, so `copy top' and `copy 2nd' stay green.
#  Only the LAST byte moves: 0x4d becomes 0x00.  The grok seat named this channel by predicting
#  the row set would need `dest[3] == 0x00 vs 0xdd'.
#  It closes three cells at once -- source RGB (0x00), dest RGB (0x00), and a deleted source
#  assignment (0x1a, because a CI GET zero-extends and RGBA then writes the colour at dest[3]).
row("copy 4th", byte_n(cw, 3) if fill_top_ok else "n/a: FILL dest[0] not RGBA -- fix absent", "0x%02x" % SRC_B3,
    "source byte 3 -- the ONLY byte an RGB-for-RGBA substitution moves on either side")

ok = sum(1 for _, o in rows if o)
print()
print("MTEFILL_RESULT=%d/%d" % (ok, len(rows)))
print("MTEFILL_DONE")
sys.exit(0 if ok == len(rows) else 1)
