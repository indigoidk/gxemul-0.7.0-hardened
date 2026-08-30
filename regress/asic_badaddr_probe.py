#!/usr/bin/env python3
"""asicbadaddr -- #463 detector (rung-3): a single guest LOAD ended the host.

Lived at _scratchpad/asic_badaddr_witness.py while it was the round's WITNESS.
It is a DETECTOR now and the two default paths changed with the move: from
regress/ the prefix is ../../ , which is what every other probe here uses.
The gate passes "$PMAX" "$KERNEL" explicitly, so the gate would NOT have
caught a wrong default -- only a manual run would, which is exactly how a
probe ends up carrying a default nobody can use.

dev_dreamcast_asic.c AS OF HEAD 6cae5e4 (:118-123) computed
r = (relative_addr / 4) & 3  and ran
exit(1) when r == 3 -- ABOVE the switch and ABOVE the writeflag test.  So the
kill needs no store, no staging and no command sequence: one load does it.

*** THE STRUCTURAL FORM MATTERS MORE THAN THE ENUMERATION. ***  r == 3 is
exactly (relative_addr & 0x0c) == 0x0c -- the FOURTH WORD of every 16-byte
group -- while every implemented case is three CONSECUTIVE words at the group
bases 0x00, 0x10, 0x20 and 0x30 (written with commas, not slashes: a
slash-separated hex list parses as a score claim -- see `scoreclaimhex`).  A census that lists today's offsets tells a future
edit nothing; the invariant tells it what it must not do.

*** AND relative_addr NEED NOT BE WORD-ALIGNED. ***  A BYTE access at +0x0d
gives 0x0d/4 == 3 and dies exactly like +0x0c.  The killing set is therefore
SIXTY-FOUR byte addresses -- ONE contiguous 4-byte span (0x0c..0x0f) in each
of the sixteen 16-byte groups, not four ranges per group -- not the
sixteen word-aligned ones.  A brief stated 16; six of nine panel seats ratified
it.  `kill byte` below is the row that pins the correction -- a detector built
from the wrong census walks a quarter of the defect and reports full coverage.

The sub-word delivery is not assumed: `src/cpus/memory_rw.c:494` computes
`paddr -= mem->devices[i].baseaddr` with NO sub-word mask -- the only nearby
guard is the `paddr + len > length` truncation -- so a byte load at 0xa05f690d
reaches the handler as relative_addr 0x0d, len 1.  Cited because `kill byte`
dies pre-fix either way; what this secures is its INTERPRETATION as the
unaligned witness rather than a duplicate of `kill word`.

*** AND THE FIRST DRAFT OF THIS FILE COMMITTED THE SIN THE PARAGRAPH ABOVE
NAMES. ***  Its three killing rows were +0x0c, +0x0d and +0x0c -- ALL INSIDE
THE SINGLE 16-BYTE GROUP [0x0c,0x0f], i.e. group 0 of 16 -- while the header
asserted the fourth word of EVERY group.  A group-narrowing mutant
(`if (r == 3 && relative_addr < 0x10)`) re-introduces the kill for 15 of the 16
groups and every row would have stayed green.  `kill far` at +0xfc (group 15,
the maximally distant one, and in the `default:` region so no case interaction
can confound it) is the row that closes it.  Caught in design review before the
first run, which is the only reason it cost nothing.

CONTRACT (vacuity floor clause (e)) -- this witness is designed to catch:
  * removal or narrowing of the r == 3 guard's REACH (kill word, kill byte)
  * the guard being made write-only, i.e. moved below the writeflag test
    (kill store, which must die on a build where only stores are guarded)
  * a "fix" that widens the kill to adjacent selectors (safe 8, safe 4)
  * an edit to the INDEXING half of the bound on r.  THE UNIT OF COVERAGE IS
    THE COLLISION PAIR, not "aliasing" in the abstract -- three register words
    admit distinct pairs and one distinctness row pins exactly one pair:
        (Scores below are HISTORICAL and are marked `13-row` because they were
        measured against the THIRTEEN-row table #463 shipped.  The gate pin is 14
        as of #492: #474 -- a footbridge round -- added the `asicoffsetkill` sweep
        row to this probe and did not move the pin, so the drift surfaced only at
        the weekly battery.  The old scores remain TRUE of the table they were
        measured against; they are not claims about today's denominator.)

        `& 3` -> `& 2`  collides words 0 and 1  -> `alias`     (12/13, 13-row)
        `& 3` -> `& 1`  collides words 0 and 2  -> `alias2`    (12/13, 13-row)
        `/ 4` -> `/ 2`  collides words 0 and 2  -> `alias2`    (12/13, 13-row)
        `& 3` -> `& 7`  goes OUT OF BOUNDS       -> `crossarr` (12/13, 13-row)
        `+1` TRANSLATION  injective, collides   -> `mask9 rt` (12/13, 13-row)
                          NOTHING on the probed set -- see below
    All four MEASURED; artifacts under regress/artifacts/asic463/.  The three
    rows are complementary and NONE catches another's mutant.
  * a +/-1 TRANSLATION of the whole index, which the three DISTINCTNESS rows
    above cannot see at all (see `mask9 rt`).  `-1` is caught by `crossarr`
    -- by COLLISION, which is why clause (ii) below matters -- and `+1` by
    `mask9 rt`.  BOTH MEASURED at this pin.

*** THREE HONESTY CLAUSES, so this contract does not overclaim again a week
out.  Each is a limit a records panel would otherwise find. ***

  (i)  ONLY +/-1 IS MEASURED.  Larger translations are NOT.  A derivation
       says +2 likely escapes BOTH the distinctness rows and `mask9 rt` --
       under +2, +0x34 writes asserted_13 and no row touches +0x34, while
       +0x38 round-trips at r=0.  Unmeasured, so it is DISCLOSED, not
       claimed.
  (ii) `-1` IS PINNED BY COLLISION, AND COLLISION IS LAYOUT-DEPENDENT.
       `crossarr` catches it because at -1 the probed cells collide; a
       struct REORDER could remove that collision and silently unpin it.
       `mask9 rt` IS ALSO LAYOUT-DEPENDENT, and an earlier draft of this
       clause denied it.  It is anchored to a cell by a SIDE EFFECT (the
       tick zeroes the latch), which makes it absolute with respect to
       the DECODE -- but `mask_9[3]` lands on `asserted_13` at byte 48
       purely by ADJACENCY (verified by offsetof further down this file),
       so a struct REORDER unpins it exactly as it unpins `crossarr`.
       Anchoring buys decode-absoluteness, not layout-independence.
  (iii) ARRAY GEOMETRY IS OUT OF CONTRACT.  `uint32_t mask_13[3]` ->
       `[2]` also scored a clean 12/12 against the then 12-row detector
       (measured; a historical quote, hence the 12-row marker).  It edits the ARRAY
       BOUND, not the bound on r, and no row here verifies the struct
       declaration the whole invariant rests on.  Filed.

*** WHAT IS STILL OUTSIDE THIS CONTRACT, stated so a later escape is a known
gap rather than an argument about overclaiming: *** the `% 3` PERMUTATION
(bijective, collides nothing, so every write round-trips through the same
permuted cell -- see the note below), and a CASE-LABEL MISROUTE (e.g. changing
`case 0x10:` to `case 0x14:`), which moves addresses no row here exercises.
The rows touch TEN offsets: +0x04, +0x08, +0x0c, +0x0d, +0x10, +0x14, +0x18, +0x24, +0x38, +0xfc.
Of the TWELVE case labels (0, 4, 8, 0x10, 0x14, 0x18, 0x20, 0x24, 0x28, 0x30,
0x34, 0x38) that leaves FIVE pinned by nothing here: 0x0, 0x20, 0x28, 0x30, 0x34.

*** THIS PARAGRAPH HAS NOW BEEN WRONG TWICE, BOTH TIMES BY MY OWN LATER EDIT. ***
The first draft listed +0x00 among the offsets touched AND omitted `case 0:`
from the unpinned list -- wrong in both directions, from a grep whose pattern
matched a word inside a comment.  The second said EIGHT offsets and SEVEN
unpinned labels, because `alias2` (+0x18) was added AFTER the census was
written, which both adds an offset and PINS `case 0x18:`.  Two audit seats
caught the second independently.  A THIRD staleness was pre-empted rather
than found: adding `mask9 rt` (+0x38) moved the counts again, and this
paragraph was re-derived MECHANICALLY from the constants the rows actually
reference instead of edited by hand.  **Re-derive this census after any row is
added; it is not a sentence that survives editing the file it describes.**
A THIRD out-of-contract class, added because a records panel found the round
block claiming this paragraph disclosed it when it did not: a PER-OFFSET KILL
planted at any r == 3 offset no row touches -- `if (relative_addr == 0x1c)
exit(1)`.  `kill far` (+0xfc) defeats a GROUP-NARROWING mutant; it cannot
defeat a single-offset one.  Filed as `asicoffsetkill`.

All three are filed, not fixed -- a detector that names its holes is falsifiable.
It is NOT designed to observe interrupt assertion; no row here does -- and that
absence has a specific consequence worth stating, because "no assertion row"
does not convey it:

*** BECAUSE NOTHING OBSERVES ASSERTION, AN INDEX PERMUTATION IS INVISIBLE TO
EVERY ROW HERE, INCLUDING A BATCHED WRITE-ALL-THEN-READ-ALL SWEEP. ***  The
mutant is `(relative_addr / 4) % 3` in place of `& 3`.  It maps each group
bijectively -- {4,5,6} -> {1,2,0}, {8,9,10} -> {2,0,1} -- so every write and its
readback round-trip through the SAME permuted cell and agree.  Batched ordering
does not help: batching catches ALIASING (two offsets colliding on one cell),
and a permutation collides nothing.  Yet the tick's `pending_irq[i] & mask_13[i]`
then pairs the wrong words.

`% 3` is the most plausible naive "repair" anyone writes at this site -- it is
what someone reaches for when worried about an index out of range -- so this is
the highest-probability future edit in this file, and it is OUTSIDE this
contract.  Closing it needs either a free-running assertion row (filed; the
step-observable event routes are dev_dreamcast_gdrom.c and dev_dreamcast_maple.c,
which fire synchronously inside a guest store, NOT dev_pvr's VBlank, which is a
tick route a stepping probe cannot drive) or the cheaper source-text presence pin
that greps the index expression for `& 3`.

Two further non-coverages, named so a rediscovery is a contract question and not
an argument about overclaiming:

  * `len == 8` re-kills.  No guest instruction reaches an 8-byte memory_rw --
    but `SYSASIC_TRIGGER_EVENT` does, so a `len == 8` guard escapes every
    guest-driven row that will ever exist here.
  * `d->pending_irq[...]`-keyed re-kills.  Setting a pending bit requires
    bit 32 of idata, which no 32-bit guest store can produce, so no row here can
    build the non-zero state such a guard would need.

Usage: asic_badaddr_witness.py <gxemul-binary> <kernel-image>
"""
import os
import pty
import re
import select
import sys
import time

BIN = sys.argv[1] if len(sys.argv) > 1 else "../../build/gxemul"
KERNEL = sys.argv[2] if len(sys.argv) > 2 else "../../_images/openbsd76-landisk-bsd.rd"

CODE = 0x8c001000
SCRATCH = 0x8c001800
LIVE = 0x5eed
SH4_IPRD = 0xffd00010
IPRD_RESET = 0xda74

ASIC = 0xa05f6900              # SYSASIC window, size 0x100
ASIC_MASK13 = ASIC + 0x10      # mask_13[0] -- plain read/write, r = (0x10/4)&3 = 0
ASIC_SAFE8 = ASIC + 0x08       # r = (0x08/4)&3 = 2 -- implemented, adjacent, must LIVE
ASIC_KILL = ASIC + 0x0c        # r = (0x0c/4)&3 = 3 -- word-aligned killing offset
ASIC_KILLB = ASIC + 0x0d       # r = (0x0d/4)&3 = 3 -- UNALIGNED killing offset
ASIC_SAFE4 = ASIC + 0x04       # r = (0x04/4)&3 = 1 -- the accept side nothing else pins
ASIC_FAR   = ASIC + 0xfc       # r = (0xfc/4)&3 = 3 in GROUP 15, not group 0
ASIC_MASK13_1 = ASIC + 0x14    # mask_13[1] -- r = 1, SAME array as +0x10
ASIC_MASK13_2 = ASIC + 0x18    # mask_13[2] -- r = 2, the THIRD word
ASIC_MASK9_2  = ASIC + 0x38    # mask_9[2] -- the LAST modelled word; under a
#  +1 translation this lands on `int asserted_13`, OUTSIDE all four arrays.
ASIC_MASK11_1 = ASIC + 0x24    # mask_11[1] -- r = 1, DIFFERENT array
#  mask_13[4] IS mask_11[1]: the struct is pending_irq[3], mask_13[3],
#  mask_11[3], mask_9[3], CONSECUTIVE (dev_dreamcast_asic.c:54-57).

NOP = 0x0009
BRA_SELF = 0xaffe
MOV_L_R8_AT_R7 = 0x2782
MOV_L_AT_R1_R2 = 0x6212
MOV_W_R8_AT_R7 = 0x2781
MOV_W_AT_R1_R2 = 0x6211
MOV_B_AT_R1_R2 = 0x6210        # mov.b @r1,r2 (0110nnnnmmmm0000, n=2 m=1)

rows = []


def row(name, got, want, note=""):
    ok = (got == want)
    rows.append((name, ok))
    print("%-14s %-12s %-12s %-34s %s" % (name, got, want, note,
                                          "ok" if ok else "FAIL"))
    return ok


def session(cmds, settle=8.0, spin=2.0):
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN, [BIN, "-V", "-x", "-E", "dreamcast", "-M", "64", KERNEL])
        os._exit(127)
    buf = ""

    def rd(t):
        nonlocal buf
        end = time.time() + t
        while time.time() < end:
            r, _, _ = select.select([fd], [], [], 0.25)
            if not r:
                continue
            try:
                d = os.read(fd, 65536)
            except OSError:
                return False
            if not d:
                return False
            buf += d.decode("latin-1", "replace")
        return True

    alive = rd(settle)
    for i, c in enumerate(cmds):
        try:
            os.write(fd, (c + "\n").encode("latin-1"))
        except OSError:
            alive = False
            break
        if not rd(spin if i == len(cmds) - 1 else 0.35):
            alive = False
            break
    try:
        os.write(fd, b"quit\n")
        rd(0.6)
    except OSError:
        pass
    for fn in (lambda: os.close(fd), lambda: os.waitpid(pid, 0)):
        try:
            fn()
        except OSError:
            pass
    return buf, alive


def printed(t, reg):
    m = re.search(r"print\s+%s\s*\r?\n\s*(0x[0-9a-f]+)" % reg, t)
    return m.group(1) if m else "absent"


def run(steps, at=CODE):
    put = ["put h 0x%x, 0x%04x" % (at + 2 * i, op) for i, op in enumerate(steps)]
    put += ["put h 0x%x, 0x%04x" % (at + 2 * len(steps), BRA_SELF),
            "put h 0x%x, 0x%04x" % (at + 2 * len(steps) + 2, NOP)]
    return put + ["pc=0x%x" % at, "step %d" % len(steps)]


def ld(reg):
    return ["r1=0x%x" % reg, "r2=0"]


def st(reg, val):
    return ["r7=0x%x" % reg, "r8=0x%08x" % val]


def pair(setup, ops):
    return setup + run(ops)


#  ------------------------------------------------------------- controls
t, alive = session(st(SCRATCH, LIVE) + ld(SCRATCH)
                   + run([MOV_L_R8_AT_R7, MOV_L_AT_R1_R2]) + ["print r2"])
row("live", printed(t, "r2") if alive else "died", "0x%x" % LIVE,
    "RAM: guest store then guest load")

t, alive = session(ld(SH4_IPRD) + run([MOV_L_AT_R1_R2]) + ["print r2"])
g = printed(t, "r2") if alive else "died"
row("devsig", ("0x%x" % (int(g, 16) & 0xffff)) if g.startswith("0x") else g,
    "0x%x" % IPRD_RESET, "SH4 IPRD reset value -- dispatch works")

#  DEVICE SIGNATURE FOR *THIS* DEVICE.  A value-only read cannot work here:
#  every asic register reads 0 on a fresh machine, so 'served' and 'declined'
#  are indistinguishable by value -- the exact trap that made the sibling
#  probe's first `impl ok` row vacuous.  mask_13 is plain read/write
#  (dev_dreamcast_asic.c:194-203 on this tree; the citation was :144-152 before
#  this round's comment displaced it), which RAM cannot fake and a deleted case
#  cannot satisfy.
t, alive = session(pair(st(ASIC_MASK13, 0x5a) + ld(ASIC_MASK13),
                        [MOV_L_R8_AT_R7, MOV_L_AT_R1_R2]) + ["print r2"])
row("asic ok", printed(t, "r2") if alive else "died", "0x5a",
    "mask_13[0] (+0x10) stores and reads back")

#  ------------------------------------------------------------- the defect
t, alive = session(ld(ASIC_SAFE8) + run([MOV_L_AT_R1_R2]) + ["print r2"])
row("safe 8", "survived" if alive else "died", "survived",
    "+0x08 r==2 at 32-bit -- must live AT THIS WIDTH")
#  *** THE UNQUALIFIED FORM OF THAT CLAIM IS FALSE, AND A SEAT CAUGHT IT. ***  This row
#  said "+0x08 is r==2 -- adjacent, implemented, must live", which asserts a property of
#  the OFFSET.  It is a property of the offset AT THIS WIDTH ONLY: an SZ=1 `fmov.d` at
#  0xa05f6908 is 8-byte aligned, passes SH_ALIGN_CHECK_LD(addr, 7), and issues its FIRST
#  access at addr+4 (cpu_sh_instr.c:798 load, :1478 store) -- relative 0x0c, r == 3, and
#  the pre-fix build DIES.  The same holds at +0x18/+0x28/+0x38: the THIRD REGISTER OF
#  EVERY IMPLEMENTED GROUP.  So a guest need not touch reserved space at all -- it need
#  only use a documented register at the wrong SZ.  An `fmov.d` row is owed.

t, alive = session(ld(ASIC_KILL) + run([MOV_L_AT_R1_R2]) + ["print r2"])
row("kill word", "survived" if alive else "died", "survived",
    "ONE guest LOAD at +0x0c -- no store, no staging")

t, alive = session(ld(ASIC_KILLB) + run([MOV_B_AT_R1_R2]) + ["print r2"])
row("kill byte", "survived" if alive else "died", "survived",
    "+0x0d UNALIGNED -- the 16-vs-64 census correction")

t, alive = session(st(ASIC_KILL, 0x1) + run([MOV_L_R8_AT_R7]) + ["print r8"])
row("kill store", "survived" if alive else "died", "survived",
    "and a STORE too -- the guard is above the writeflag test")

#  *** THE ACCEPT SIDE OF `r == 3` IS r IN {0,1,2}, AND r == 1 WAS PINNED BY
#  NOTHING. ***  `asic ok` pins r == 0 and `safe 8` pins r == 2, so a growth
#  mutant that moves the kill onto r == 1 escapes both.
#
#  *** THE WARRANT FIRST WRITTEN HERE WAS FALSE AND A SEAT CAUGHT IT. ***  It said
#  the mutant was `(relative_addr / 4) & 1` "which kills +0x04, +0x14, +0x24".
#  Under `& 1` the value of r is in {0,1}, so `r == 3` is NEVER TRUE and NOTHING
#  dies -- `& 1` is an INDEX-ALIASING mutant, which is exactly how this round's own
#  aliasing table uses it, not a guard-growth one.  The mutant that actually kills
#  +0x04 is `if (r == 3 || r == 1)`.  The ROW is right; its stated reason was not,
#  and a wrong reason gets reused.
t, alive = session(ld(ASIC_SAFE4) + run([MOV_L_AT_R1_R2]) + ["print r2"])
row("safe 4", "survived" if alive else "died", "survived",
    "+0x04 is r==1 -- the accept side no other row pins")

#  *** THE GROUP ROW.  Without it this witness walks ONE 16-byte group and
#  claims a property of all sixteen -- see the header. ***  +0xfc is r == 3 in
#  group 15, and it falls in the `default:` region, so the death is the guard
#  and nothing else.
t, alive = session(ld(ASIC_FAR) + run([MOV_L_AT_R1_R2]) + ["print r2"])
row("kill far", "survived" if alive else "died", "survived",
    "+0xfc -- r==3 in group 15, not group 0")

#  --------------------------------------------------------------- the SWEEP
#
#  *** `asicoffsetkill`: NINE TOUCHED OFFSETS CANNOT DEFEND 256. ***  A grok seat on
#  the #463 pass-2 panel pointed out that `if (relative_addr == 0x1c) exit(1)` scores
#  CLEAN against every row above -- `kill far` defeats a GROUP-NARROWING mutant but
#  cannot defeat a SINGLE-OFFSET one.
#
#  ONE SESSION, NOT SIXTEEN ROWS.  Every row here is a full emulator boot and
#  `probeslow` is already filed about session cost, so the sweep re-points r1 between
#  single steps inside a single session.  A kill planted at ANY offset kills this
#  session, and the row reds.
#
#  ALL 256 BYTE OFFSETS, not the sixteen word-aligned r==3 ones.  The carrier records
#  a census that was wrong by 4x because `relative_addr` need not be word-aligned: a
#  BYTE access at +0x0d dies exactly like +0x0c, so the killing set is 64 byte
#  addresses and not 16.  Sweeping the whole window costs the same single session and
#  is immune to that arithmetic being re-derived wrongly a second time.  `mov.b` is
#  legal at every address, so no offset is skipped for alignment.
#
#  SURVIVE-ONLY, deliberately, and it does NOT close `asickillsurvive`.  It proves no
#  offset terminates the host; it says nothing about what a declined offset RETURNS.
sweep_cmds = ["put h 0x%x, 0x%04x" % (CODE, MOV_B_AT_R1_R2),
              "put h 0x%x, 0x%04x" % (CODE + 2, BRA_SELF)]
for _off in range(0x100):
    sweep_cmds += ["r1=0x%x" % (ASIC + _off), "pc=0x%x" % CODE, "step 1"]
#  A liveness marker AFTER the sweep: reaching it proves the session survived all 256
#  accesses rather than that the pty merely stayed open.
sweep_cmds += ["r2=0x%x" % LIVE, "print r2"]

t, alive = session(sweep_cmds, settle=12.0)
row("sweep 256", (printed(t, "r2") if alive else "died"), "0x%x" % LIVE,
    "every offset in the window, one session")

#  --------------------------------------------- the INDEXING half of the bound
#
#  *** THE INVARIANT HAS TWO HALVES AND THE FIRST NINE ROWS ONLY PINNED ONE. ***
#  r is bounded by (i) every case label satisfying (label & 0x0c) != 0x0c, and
#  (ii) the `& 3` mask itself.  A panel seat pointed out that `& 3` -> `& 7`
#  breaks half (ii) while leaving EVERY case label compliant -- so the comment
#  in dev_dreamcast_asic.c would not even be violated, and no row here saw it.
#  These two rows pin half (ii).  They are deliberately COMPLEMENTARY: neither
#  catches the other's mutant, which is why both ship.

#  `alias` -- kills `& 3` -> `& 2` (r restricted to {0,2}, so +0x10 and +0x14
#  collide on mask_13[0] and the second write wins).  Named independently by
#  two packet-fed seats in the same pass.
t, alive = session(st(ASIC_MASK13, 0xa1) + run([MOV_L_R8_AT_R7], CODE)
                   + st(ASIC_MASK13_1, 0xb2) + run([MOV_L_R8_AT_R7], CODE + 0x40)
                   + ld(ASIC_MASK13) + run([MOV_L_AT_R1_R2], CODE + 0x80)
                   + ["print r2"])
row("alias", printed(t, "r2") if alive else "died", "0xa1",
    "+0x10 and +0x14 are DISTINCT cells, not one aliased cell")

#  `crossarr` -- kills `& 3` -> `& 7` (r reaches 4, and mask_13[4] IS
#  mask_11[1], so a mask_11 write silently overwrites a mask_13 cell).  A
#  same-array distinctness row CANNOT see this: under `& 7` the three mask_13
#  words map to [4],[5],[6], which are still three distinct cells that
#  round-trip.  Only a cross-ARRAY read exposes it.
t, alive = session(st(ASIC_MASK13, 0xc3) + run([MOV_L_R8_AT_R7], CODE)
                   + st(ASIC_MASK11_1, 0xd4) + run([MOV_L_R8_AT_R7], CODE + 0x40)
                   + ld(ASIC_MASK13) + run([MOV_L_AT_R1_R2], CODE + 0x80)
                   + ["print r2"])
row("crossarr", printed(t, "r2") if alive else "died", "0xc3",
    "mask_13[0] survives a mask_11[1] write -- r stays IN BOUNDS")

#  `alias2` -- kills `& 3` -> `& 1`, which the OTHER TWO ROWS BOTH MISS.
#
#  *** THIS ROW EXISTS BECAUSE A SEAT REFUTED THE 11-ROW DETECTOR. ***  `alias`
#  pins words 0 and 1 (+0x10, +0x14); `& 1` maps them to 0 and 1, so they stay
#  distinct and it goes GREEN.  `crossarr` pins a cross-array pair that `& 1`
#  also leaves distinct, so it goes green too.  What `& 1` actually collides is
#  words 0 and TWO -- +0x18 maps to (0x18/4) & 1 == 0, onto +0x10.
#
#  So the collision PAIR is the unit of coverage here, not "aliasing" in the
#  abstract: three mask bits admit three distinct pairs and one row can pin one
#  pair.  `& 1` is the carrier's own canonical clause-(d) example, and the first
#  two rows were blind to it.
t, alive = session(st(ASIC_MASK13, 0xa1) + run([MOV_L_R8_AT_R7], CODE)
                   + st(ASIC_MASK13_2, 0xb2) + run([MOV_L_R8_AT_R7], CODE + 0x40)
                   + ld(ASIC_MASK13) + run([MOV_L_AT_R1_R2], CODE + 0x80)
                   + ["print r2"])
row("alias2", printed(t, "r2") if alive else "died", "0xa1",
    "+0x10 and +0x18 are DISTINCT cells too")

#  ------------------------------------------------- THE ANCHORED ROW
#
#  *** THE THREE ROWS ABOVE PIN NOTHING ABOUT WHERE AN ACCESS LANDS. ***
#  They assert only that cell(+0x10) differs from cell(+0x14), cell(+0x18)
#  and cell(+0x24).  **Distinctness is invariant under any INJECTIVE re-map,
#  and a translation is injective** -- slide every address one word and all
#  three pairs stay distinct.  A capped adversarial re-ask measured exactly
#  that: `((relative_addr / 4) + 1) & 3` scored a CLEAN 12/12 sweep against
#  the then 12-row detector -- a historical quote, hence the 12-row marker.
#  THAT ESCAPE IS WHY THIS ROW EXISTS, so the number must stay quoted at its
#  own era rather than be silently restated against today's pin.
#
#  It is not a cosmetic escape.  Under +1 every `+0x?8` register moves from
#  r=2 to r=3 -- one past a [3] array -- and mask_9[3] IS `int asserted_13`
#  (verified by offsetof: mask_9 at byte 36, asserted_13 at byte 48).  So a
#  single aligned 32-bit guest store to +0x38, a documented register, writes
#  the interrupt-assertion latch, and the write arm's own tick then issues a
#  spurious INTERRUPT_DEASSERT and drops a legitimately pending IRQ13.
#
#  THIS ROW IS AN ACCEPT-SIDE OBLIGATION, NOT COVERAGE.  Apply +1 to the
#  PRE-FIX code and the old `exit(1)` fires on the first legal access to
#  +0x08/+0x18/+0x28/+0x38 -- so the edit ANNOUNCED ITSELF before #463, and
#  deleting the guard de-announced it.  That is precisely the class the
#  de-escalation clause covers, and such a row is discharged only by a
#  MEASURED KILL.  (The same test puts `-1` in the class too; `crossarr`
#  already kills it, so that member is discharged.)
#
#  The oracle is ANCHORED rather than relative: it is tied to a specific
#  cell by a channel OUTSIDE the decode under test -- the tick zeroes
#  asserted_13, so the readback is 0x0 rather than merely different.
t, alive = session(st(ASIC_MASK9_2, 0xb2) + ld(ASIC_MASK9_2)
                   + run([MOV_L_R8_AT_R7, MOV_L_AT_R1_R2]) + ["print r2"])
row("mask9 rt", printed(t, "r2") if alive else "died", "0xb2",
    "+0x38 round-trips -- r's IMAGE stays inside the arrays")

n_ok = sum(1 for _, ok in rows if ok)
print("ASIC_BADADDR_RESULT=%d/%d" % (n_ok, len(rows)))
print("ASIC_BADADDR_VECTOR=%s" % ",".join("1" if ok else "0" for _, ok in rows))
