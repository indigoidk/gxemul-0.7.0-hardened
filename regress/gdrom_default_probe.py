#!/usr/bin/env python3
"""DETECTOR for gdromdefault, carrying the round's witness measurement.

THE DEFECT: dev_dreamcast_gdrom.c registers a 0x100 window at 0x005f7000 and
its switch implements EIGHT offsets -- 0x18, 0x80, 0x84, 0x88, 0x8c, 0x90,
0x94, 0x9c.  Every other address in that window falls to `default:`, which
prints and then runs exit(1), for a READ or a WRITE, at any width.

*** ONE PREDICATE, ROUGHLY 248 OF 256 BYTE OFFSETS LETHAL. ***  A driver or a
diagnostic that scans the device's register space -- an ordinary thing to do
before you know what is there -- ends the host process on its first unhandled
address.  That is a wider blast radius than the whole GDROM_DATA arm #460
fixed, which needed a specific register and, for two of three sites, specific
device state.

CENSUS, measured on an unmodified `-E dreamcast -x`, one 32-bit guest load per
offset: 21 sampled, 19 DIED via this arm, 2 survived (0x90 and 0x94, both
implemented).  32-bit was chosen deliberately -- it reaches `default:` for an
unhandled offset WITHOUT first tripping GDROM_DATA's own width guard, so a
death is attributable to this arm and not to another.

THE LATCH SHAPE IS THE ROUND'S DESIGN QUESTION, and #443 already answered the
same question in this tree: `uint32_t pcic_reported[NCLASS][(N_REGS+31)/32]`,
a PER-WORD BITMAP keyed by fault class, with its own comment recording why --
"A per-device flag would hide it ... 137 named flags would be absurd.  This is
five words."  A single flag here would let ONE unimplemented access silence
the other 247; a named constant per offset is absurd at this width.

*** DREAMCAST NEEDS -x OR IT NEVER REACHES THE DEBUGGER PROMPT. ***  Two
console inputs, and console.c:994-1007 makes that fatal without allow_slaves.
Without it a session dies for a CONFIGURATION reason and prints the same
"died" the defect prints -- that cost #459 a false positive.

Rung 3 by the witness ladder: real guest instructions through real address
decode on an UNMODIFIED in-tree machine description.

CONTROLS RUN IN THEIR OWN SESSIONS AND NEVER TOUCH AN UNIMPLEMENTED OFFSET,
so a red trigger row cannot be confused with a broken session.
"""
import os
import pty
import re
import select
import sys
import time

BIN = sys.argv[1] if len(sys.argv) > 1 else "../../build/gxemul"
KERNEL = sys.argv[2] if len(sys.argv) > 2 else "../../_images/openbsd76-landisk-bsd.rd"

#  Dreamcast RAM is 16 MB at 0x0c000000; the loaded ELF lands at 0x8c002000
#  and grows up, so plant below it.  -M 64 is passed only for uniformity with
#  the other SH probes; this machine's RAM is a fixed dev_ram regardless.
CODE = 0x8c001000
SCRATCH = 0x8c001800

BASE = 0xa05f7000              # the 0x100 window, via P2 (uncached)
DMA = 0xa05f7400               # the DMA window, 0x80, SEPARATELY registered
IMPLEMENTED_WORDS = (0x18, 0x80, 0x84, 0x88, 0x8c, 0x90, 0x94, 0x9c)
IMPL_BUSY = BASE + 0x18        # implemented: returns d->busy
IMPL_CNTLO = BASE + 0x90       # implemented: returns d->cnt & 0xff
IMPL_COND = BASE + 0x9c        # implemented
UNIMPL_A = BASE + 0x00         # unimplemented -> default:
UNIMPL_B = BASE + 0x04         # unimplemented, a DIFFERENT word
UNIMPL_Z = BASE + 0xfc         # unimplemented, far end of the window

SH4_IPRD = 0xffd00010
IPRD_RESET = 0xda74
LIVE = 0x12345678

MOV_W_R8_AT_R7 = 0x2781
MOV_L_R8_AT_R7 = 0x2782
MOV_W_AT_R1_R2 = 0x6211
MOV_L_AT_R1_R2 = 0x6212
MOV_L_AT_R3_R2 = 0x6232       # mov.l @r3,r2
MOV_W_AT_R3_R2 = 0x6231       # mov.w @r3,r2
ADD_4_R1 = 0x7104             # add #4,r1
MOV_B_R6_AT_R5 = 0x2560       # mov.b r6,@r5
MOV_W_R6_AT_R5 = 0x2561       # mov.w r6,@r5
MOV_L_R6_AT_R5 = 0x2562       # mov.l r6,@r5  (0010nnnnmmmm0010, n=5 m=6)
BRA_SELF = 0xaffe
NOP = 0x0009

rows = []


#  *** THE ROW-NAME COLUMN IS 14 AND THE LONGEST NAME IS 12, WHICH IS NOT
#  SLACK -- IT IS THE DISCRIMINATOR. ***
#
#  gate_sh_rounding.sh counts rows with `^$v  .*ok$` -- TWO spaces after the
#  name.  Four names here are prefixes of others (`dma rd`/`dma rd x1`,
#  `dma rd`/`dma rdleak`, `dma alias`/`dma alias x1`, `scan`/`scan uniq`),
#  and they are unambiguous ONLY because %-14s leaves at least two spaces
#  after every one of them.  `dma rd` cannot match the `dma rdleak` row
#  because that row has an `l` where the pattern needs a space.
#
#  A row named 13 or 14 characters leaves fewer than two spaces and its
#  check becomes UNSATISFIABLE.  Checked, and this is the SAFE direction:
#  the count reads 0 against a wanted 1, so the gate fails LOUDLY rather
#  than quietly dropping the row -- the opposite of the padded-column trap
#  the carrier records, where a too-long name makes a row stop being
#  tested in silence.  Widen the column if a longer name is ever needed;
#  do not shorten the name to fit and leave the constraint unstated.
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
    try:
        os.close(fd)
    except OSError:
        pass
    try:
        os.waitpid(pid, 0)
    except OSError:
        pass
    return buf, alive


def printed(t, reg):
    m = re.search(r"print\s+%s\s*\r?\n\s*(0x[0-9a-f]+)" % reg, t)
    return m.group(1) if m else "absent"


def run(steps, at=CODE):
    """Plant a run of instructions, then a self-branch, and step them all."""
    put = ["put h 0x%x, 0x%04x" % (at + 2 * i, op) for i, op in enumerate(steps)]
    put += ["put h 0x%x, 0x%04x" % (at + 2 * len(steps), BRA_SELF),
            "put h 0x%x, 0x%04x" % (at + 2 * len(steps) + 2, NOP)]
    return put + ["pc=0x%x" % at, "step %d" % len(steps)]


def ld(reg):
    return ["r1=0x%x" % reg, "r2=0"]


def pair(setup, ops):
    """Plant SEVERAL accesses contiguously and step them all.

    *** USE THIS FOR EVERY MULTI-ACCESS ROW. ***  Calling run() twice does NOT
    work: each call emits its own `pc=`/`step`, so the second overrides the
    first and only ONE access ever executes.  #460 hit exactly this and it
    made four latch rows vacuous -- they read a count of 1 whether the latch
    worked or not.  Here it turned a CONTROL red instead, which is the loud
    direction, and one measurement found it.
    """
    return setup + run(ops)


def st(reg, val):
    return ["r7=0x%x" % reg, "r8=0x%08x" % val]


#  ---------------------------------------------------------------- controls
t, alive = session(st(SCRATCH, LIVE) + ld(SCRATCH)
                   + run([MOV_L_R8_AT_R7, MOV_L_AT_R1_R2]) + ["print r2"])
row("live", printed(t, "r2") if alive else "died", "0x%x" % LIVE,
    "RAM: guest store then guest load")

t, alive = session(ld(SH4_IPRD) + run([MOV_L_AT_R1_R2]) + ["print r2"])
g = printed(t, "r2") if alive else "died"
row("devsig", ("0x%x" % (int(g, 16) & 0xffff)) if g.startswith("0x") else g,
    "0x%x" % IPRD_RESET, "SH4 IPRD reset value -- dispatch works")

#  An IMPLEMENTED offset, to prove the device is mapped and its arm serves.
#
#  *** THE FIRST VERSION OF THIS ROW WAS VACUOUS, AND MEASURED SO. ***  It read
#  +0x18 and asserted only that the answer started with "0x" -- but `print r2`
#  ALWAYS prints hex, so it was green even on a build with `case GDROM_BUSY:`
#  DELETED, where +0x18 falls through to the default arm.  It was a
#  session-liveness row duplicating `live`, wearing a device row's label.
#
#  The root cause is worth keeping, because it constrains the fix: a DECLINED
#  read at +0x00 returns 0, and a SERVED read of +0x18 ALSO returns 0 on a
#  fresh device -- busy, cond, stat and cnt are all zero.  No value-only row
#  can tell served from declined here.  So this is now store-then-read-back on
#  CNTHI, which RAM cannot fake and a deleted case cannot satisfy.
t, alive = session(pair(st(BASE + 0x94, 0x5a) + ld(BASE + 0x94),
                        [MOV_W_R8_AT_R7, MOV_W_AT_R1_R2]) + ["print r2"])
row("impl ok", printed(t, "r2") if alive else "died", "0x5a",
    "CNTHI (+0x94) stores and reads back")

print("GDROM_DEF_CONTROL=%s" % ("OK" if all(ok for _, ok in rows) else "DEAD"))

#  ---------------------------------------------------------------- triggers
#  Each is ONE guest instruction at an UNIMPLEMENTED offset.  Post-fix every
#  one must leave the host alive AND name itself exactly once.
SAYS = re.compile(r"dreamcast_gdrom: (?:read from|write to) addr 0x")
#  The DMA arm needs its OWN pattern: SAYS cannot match it, because after
#  "dreamcast_gdrom" that pattern expects ": " and the DMA text has "_dma: ".
#  A seat flagged that before it could become a silently-zero count.
DMA_SAYS = re.compile(r"dreamcast_gdrom_dma: (?:read from|write to) addr 0x")

for label, cmds, note in (
        ("rd lo", ld(UNIMPL_A) + run([MOV_L_AT_R1_R2]),
         "32-bit READ at +0x00"),
        ("wr lo", st(UNIMPL_B, 0x5a5a5a5a) + run([MOV_L_R8_AT_R7]),
         "32-bit WRITE at +0x04"),
        ("rd hi", ld(UNIMPL_Z) + run([MOV_L_AT_R1_R2]),
         "32-bit READ at +0xfc, far end"),
        ("rd w16", ld(UNIMPL_A) + run([MOV_W_AT_R1_R2]),
         "16-bit read: width must not matter here")):
    t, alive = session(cmds)
    row(label, "survived" if alive else "died", "survived", note)
    row(label.replace(" ", "") + " x1",
        ("%d" % len(SAYS.findall(t))) if alive else "died", "1",
        "names itself EXACTLY once")

#  ------------------------------------------------------- latch SCOPE rows
#
#  *** THESE ARE THE ROWS THAT DECIDE THE DESIGN, AND NOTHING ELSE CAN SEE IT.
#
#  A single per-device flag makes ONE unimplemented access silence the other
#  247, which is the "1 of 4 kinds" hazard #438 recorded and #443 refused.  A
#  per-word bitmap keyed by fault class is the shape #443 shipped for the same
#  problem in the same tree.  Only rows that drive TWO DIFFERENT offsets, and
#  the SAME offset in BOTH directions, can tell those apart.

t, alive = session(ld(UNIMPL_A) + run([MOV_L_AT_R1_R2, MOV_L_AT_R1_R2]))
row("same twice", ("%d" % len(SAYS.findall(t))) if alive else "died", "1",
    "SAME offset twice -> one line")

#  r1 then r3, so both loads have their own address register and both can be
#  planted contiguously.
t, alive = session(pair(["r1=0x%x" % UNIMPL_A, "r3=0x%x" % UNIMPL_B, "r2=0"],
                        [MOV_L_AT_R1_R2, MOV_L_AT_R3_R2]))
row("two offs", ("%d" % len(SAYS.findall(t))) if alive else "died", "2",
    "DIFFERENT offsets -> TWO lines, not one")

#  *** RE-PINNED 2 -> 1 -> 2. THE SECOND REVERSAL IS THE ONE THAT MATTERS, AND
#  IT IS A MEASUREMENT OVERTURNING A VOTE. ***
#
#  The first draft expected TWO lines, which silently pre-answered the brief's
#  own open question about a read/write class split.  The pass-1 panel answered
#  it the other way 3-1, on reasoning that read well: #443's classes are KINDS
#  OF COMPLAINT rather than directions, the fault here is spatial, and direction
#  is already printed in the first line.  I re-pinned to 1 on that.
#
#  THEN THE MEASURING SEAT BUILT BOTH AND RAN A READ PASS FOLLOWED BY A WRITE
#  PASS OVER THE SAME 31 DECLINED OFFSETS:
#
#      direction x offset   ->  62 lines, 31 unique offsets
#      offset only          ->  31 lines, and ZERO WRITE DIAGNOSTICS
#
#  The read pass latches every offset first, so under offset-only keying a
#  guest's writes to unimplemented space are reported NOWHERE.  And the write
#  line is the only one that carries `idata` -- the value you need in order to
#  model the register later.  That is not padding, and the three seats that
#  called it padding were reasoning from #443's structure rather than from this
#  arm's behaviour.
#
#  Restored to 2.  Recorded at length because the project's rule is that
#  disagreements are settled EMPIRICALLY and never by vote, and this is the
#  case where the vote and the measurement pointed opposite ways -- a 3-1
#  majority, overturned by one build.
t, alive = session(pair(ld(UNIMPL_A) + st(UNIMPL_A, 0x1234),
                        [MOV_L_AT_R1_R2, MOV_L_R8_AT_R7]))
row("rd then wr", ("%d" % len(SAYS.findall(t))) if alive else "died", "2",
    "SAME offset, both directions -> TWO lines")

#  GRANULARITY, and it is a design commitment nothing else pins.  Per-WORD
#  keying merges +0x00..+0x03 into one bit; per-BYTE keying would give four.
#  A seat flagged that the brief chose per-word silently, and a second named the
#  mutant it protects against: indexing the bitmap with `relative_addr` instead
#  of `relative_addr >> 2`, which under a [2] array writes past the end while
#  still printing exactly once -- every other row green, host memory corrupted.
#  Under raw-byte indexing these two accesses latch different bits and print
#  twice, so this row reddens where the others cannot see it.
t, alive = session(pair(["r1=0x%x" % UNIMPL_A, "r3=0x%x" % (UNIMPL_A + 2), "r2=0"],
                        [MOV_L_AT_R1_R2, MOV_W_AT_R3_R2]))
row("granularity", ("%d" % len(SAYS.findall(t))) if alive else "died", "1",
    "+0x00 then +0x02 are ONE word -> one line")

#  ---------------------------------------------------------------- accept side
#
#  The de-escalation clause: this fix removes a host-fatal predicate, so the
#  detector must pin that the IMPLEMENTED offsets still work.  Without these,
#  a mutant that turns the whole switch into `default:` -- or simply deletes
#  the implemented arms -- scores full marks on every row above.

t, alive = session(pair(st(IMPL_CNTLO, 0x98) + ld(IMPL_CNTLO),
                        [MOV_W_R8_AT_R7, MOV_W_AT_R1_R2]) + ["print r2"])
row("accept cnt", printed(t, "r2") if alive else "died", "0x98",
    "CNTLO (+0x90) still stores and reads back")

t, alive = session(pair(st(IMPL_COND, 0xa0) + ld(IMPL_BUSY),
                        [MOV_W_R8_AT_R7, MOV_W_AT_R1_R2]) + ["print r2"])
row("accept cond", printed(t, "r2") if alive else "died", "0x8",
    "COND=0xa0 (+0x9c) still sets BUSY bit 3")

#  ------------------------------------------------------------- the window scan
#
#  *** THE SCAN AND THE GRANULARITY ROW KILL DIFFERENT MUTANTS AND NEITHER
#  SUBSUMES THE OTHER -- measured, against the measuring seat's own prediction
#  that the scan would cover everything. ***
#
#      counter capped at 4   scan 4 != 56  KILLED   granularity 1  survives
#      key mask off & 0x7f   scan 32 != 56 KILLED   granularity 1  survives
#      index by raw address  scan 15 != 56 KILLED   granularity 2  KILLED
#
#  *** THE THIRD ROW SAID `scan 56 == 56 SURVIVES` UNTIL A PASS-2 SEAT
#  MEASURED IT AT 15. ***  The old number was the pass-1 analysis of a design
#  WITHOUT the bounds guard, and it survived into the shipped comment beside a
#  table that already refuted it.  With the guard, raw indexing makes every
#  offset >= 0x40 exceed the 64 keys and be rejected, so 41 of the 56 declined
#  offsets never report and the scan reads 15.
#
#  So the scan DOES kill this one, and `granularity` is no longer its sole
#  killer.  *** KEEP THE GRANULARITY ROW ANYWAY, but for the honest reason:
#  it pins a DESIGN COMMITMENT (per-word keying) cheaply and directly, rather
#  than because it is the only row that can see this mutant. ***  The same
#  seat measured that across six mutants `scan uniq` kills everything anything
#  kills -- so the subsumption claim this block was built on is false in the
#  other direction too, and saying so is cheaper than a row that pretends.
#
#  The magnitude claim was overstated as well.  A guardless `bits[k]` reaches
#  dma_reg[0..3] -- count, destination and length -- but NOT dma_reg[5], the
#  enable, which needs word index 11 against a maximum of 9.  "The two fields
#  that authorise a transfer" was wrong; it is three of the four.
#
#  EQUALITY, not >=, so this doubles as an IDENTITY row: 64 word keys minus 8
#  implemented offsets is exactly 56.  A ninth implemented register moves it to
#  55 in the same commit, which is the fail-closed ratchet gate_hygiene already
#  uses for EXPECT_CONVERTED.
#  ONE session, not 56.  A per-offset session took over ten minutes; a planted
#  linear run of `mov.l @r1,r2 ; add #4,r1` walks the whole window in one.
#  Implemented offsets are NOT skipped -- they emit nothing matching SAYS, which
#  is exactly what `accept8` proves independently, so the count is still 56.
ops = []
for _ in range(0x100 // 4):
    ops += [MOV_L_AT_R1_R2, ADD_4_R1]
t, alive = session(["r1=0x%x" % BASE, "r2=0"] + run(ops), settle=8.0, spin=3.0)
hits = SAYS.findall(t)
row("scan", "survived" if alive else "died", "survived",
    "all 64 words of the window, one run")
row("scan uniq", ("%d" % len(hits)) if alive else "died", "56",
    "64 words - 8 implemented = 56 declines")

#  ------------------------------------------------- the accept side that MATTERS
#
#  *** THREE OF FOUR NARROWING MUTANTS SCORED A PERFECT 16/16 WITHOUT THIS ROW,
#  AND ONE OF THEM SILENTLY UNDOES THE PREVIOUS ROUND. ***
#
#  The measuring seat built Option B and then deleted ONE `case` label at a
#  time -- a one-line edit, exactly the shape a "fold this stub into the
#  default" tidy-up takes:
#
#      delete case GDROM_STAT  (+0x8c)  ->  16/16   the register NetBSD polls
#                                                   before every command is dead
#      delete case GDROM_DATA  (+0x80)  ->  16/16   #460'S ENTIRE ROUND UNDONE
#      delete case GDROM_CNTHI (+0x94)  ->  16/16   transfer-count high byte dead
#      delete case GDROM_BUSY  (+0x18)  ->  15/16   caught, but only by accident
#
#  This is the de-escalation clause's own scenario at its sharpest: BEFORE this
#  fix, deleting `case GDROM_STAT:` meant exit(1) on the first status poll --
#  unmissable.  AFTER it, a silently wrong status forever.  The fix destroys the
#  accidental tripwire for its own accept side, so the round owes this row.
#
#  Read all EIGHT implemented offsets and require the default arm
#
#  *** THIS SAID "in one session" AND THE LOOP BELOW REFUTES IT. ***  It runs
#  EIGHT emulator processes and concatenates their output, which the comment
#  eight lines down states correctly -- so two drafts of the same paragraph
#  disagreed and the wrong one was on top.  It is equivalent HERE only because
#  the expectation is a count of ZERO, which concatenation preserves; a row
#  expecting a NON-zero count would have been silently wrong.
#  to have printed NOTHING.  Safe by reading: none of the eight arms emits text
#  matching SAYS -- BUSY/STAT/CNTLO/CNTHI/COND are silent, REGX says
#  "[ Read to GDROM_REGX? ]", UNKNOWN_0x88 says "Read from GDROM_UNKNOWN_0x88?"
#  with no `dreamcast_gdrom:` prefix, and #460's warns say "read from
#  GDROM_DATA", not "read from addr 0x".
#  Same tuple as the scan uses -- one definition, so the two rows can never
#  disagree about which offsets are implemented.
IMPLEMENTED = IMPLEMENTED_WORDS
#  Eight loads through ONE address register, re-pointed between steps is not
#  possible in a single run -- so use r1 and step the loads one at a time with
#  an explicit pc per access, which is the one place the two-run hazard does
#  NOT apply because each access is its own complete run.
t = ""
alive = True
for i, off in enumerate(IMPLEMENTED):
    tt, aa = session(pair(["r1=0x%x" % (BASE + off), "r2=0"], [MOV_W_AT_R1_R2]))
    t += tt
    alive = alive and aa
row("accept8", ("%d" % len(SAYS.findall(t))) if alive else "died", "0",
    "all EIGHT implemented offsets stay off the default arm")

#  And GDROM_DATA's own accept side, which also closes an escape already filed
#  against #460: no row there pinned what a declined DATA read returns.
t, alive = session(ld(BASE + 0x80) + run([MOV_W_AT_R1_R2]) + ["print r2"])
g = printed(t, "r2") if alive else "died"
row("data 0xffff", ("0x%x" % (int(g, 16) & 0xffff)) if g.startswith("0x") else g,
    "0xffff", "+0x80 still declines with 0xffff, not via default")

#  ---------------------------------------------------------------- the DMA window
#
#  *** THE DMA ARM JOINED THIS ROUND ON A MEASUREMENT AND HAD NO ROW AT ALL. ***
#  Every row above drives the CONTROL window at 0x005f7000; the sibling arm at
#  0x005f7400 was fixed and pinned by nothing.  A round that claims to fix two
#  arms and covers one is making a claim its own detector cannot support, so
#  these ship with the fix rather than after it.
t, alive = session(pair(["r1=0x%x" % DMA, "r2=0"], [MOV_L_AT_R1_R2]))
row("dma rd", "survived" if alive else "died", "survived",
    "32-bit READ at DMA+0x00")
row("dma rd x1", ("%d" % len(DMA_SAYS.findall(t))) if alive else "died", "1",
    "the DMA arm names itself EXACTLY once")

t, alive = session(pair(["r1=0x%x" % (DMA + 0x00), "r3=0x%x" % (DMA + 0x7c), "r2=0"],
                        [MOV_L_AT_R1_R2, MOV_L_AT_R3_R2]))
row("dma two", ("%d" % len(DMA_SAYS.findall(t))) if alive else "died", "2",
    "DIFFERENT DMA offsets -> TWO lines, separate array")

#  *** THE ASYMMETRY THIS ROUND HAD TO NAME, NOW PINNED. ***  In the control
#  window declining returns 0 and a declined write does nothing.  Here `odata`
#  is preloaded from the shadow register file before the switch and the tail
#  STORES a declined write into it -- so "decline" means store-and-return, which
#  is what the five implemented cases already do and is kept deliberately.
#  Without this row that difference is a claim in a comment and nothing else.
t, alive = session(pair(["r7=0x%x" % DMA, "r8=0x12345678", "r1=0x%x" % DMA, "r2=0"],
                        [MOV_L_R8_AT_R7, MOV_L_AT_R1_R2]) + ["print r2"])
row("dma shadow", printed(t, "r2") if alive else "died", "0x12345678",
    "a declined DMA write STORES and reads back")

#  *** THE ROW A PASS-2 SEAT'S DO-NOT-SHIP REQUIRED. ***
#
#  The tail store indexes with TRUNCATING division, so a byte write at DMA+0x05
#  does not match `case 0x04`, reaches the default arm, is declined -- and then
#  the tail writes it into dma_reg[1], the DMA DESTINATION.  The same alias
#  reaches dma_reg[2] (length), dma_reg[3] (count) and dma_reg[5] (enable) from
#  +0x09, +0x0d and +0x15, which between them are the whole transfer.
#
#  PRE-FIX those accesses exited instead, so the fix would have CREATED the
#  capability.  This row pins that it does not: write 0xff at +0x05, then read
#  +0x04 back and require it UNCHANGED.
t, alive = session(pair(["r7=0x%x" % (DMA + 0x04), "r8=0x11223344",
                         "r1=0x%x" % (DMA + 0x04), "r2=0"],
                        [MOV_L_R8_AT_R7, MOV_L_AT_R1_R2]) + ["print r2"])
row("dma seed", printed(t, "r2") if alive else "died", "0x11223344",
    "the implemented +0x04 takes a known value")

t, alive = session(pair(["r7=0x%x" % (DMA + 0x04), "r8=0x11223344",
                         "r5=0x%x" % (DMA + 0x05), "r6=0xff",
                         "r1=0x%x" % (DMA + 0x04), "r2=0"],
                        [MOV_L_R8_AT_R7, MOV_B_R6_AT_R5, MOV_L_AT_R1_R2])
                   + ["print r2"])
row("dma alias", printed(t, "r2") if alive else "died", "0x11223344",
    "a declined +0x05 must NOT reach dma_reg[1]")
#  ... and the row above is only meaningful if the store EXECUTED.  A wrong
#  opcode constant would leave +0x04 untouched and the row green -- the
#  hand-assembled-encoding trap exactly.  The declined +0x05 must announce.
row("dma alias x1", ("%d" % len(DMA_SAYS.findall(t))) if alive else "died", "1",
    "the +0x05 store really reached the default arm")

#  *** ONE CHARACTER RE-OPENS THE DEFECT ABOVE, AND `dma alias` CANNOT SEE IT. ***
#
#  A pass-2 seat weakened the guard to `relative_addr & 1` and scored 27/27.
#  That form still drops the ODD address `dma alias` uses, so that row is
#  STRUCTURALLY BLIND to it -- yet a 16-bit store at +0x06 is 2-byte aligned,
#  passes `& 1`, and the tail writes it into dma_reg[1] exactly as before.
#
#  The discriminator is WIDTH, not oddness.  This row uses mov.w at an EVEN but
#  not word-aligned address, which is the cheapest access the weaker guard lets
#  through -- and it is architecturally legal, so a real guest can issue it.
t, alive = session(pair(["r7=0x%x" % (DMA + 0x04), "r8=0x11223344",
                         "r5=0x%x" % (DMA + 0x06), "r6=0xffff",
                         "r1=0x%x" % (DMA + 0x04), "r2=0"],
                        [MOV_L_R8_AT_R7, MOV_W_R6_AT_R5, MOV_L_AT_R1_R2])
                   + ["print r2"])
row("dma align16", printed(t, "r2") if alive else "died", "0x11223344",
    "a 2-byte-aligned +0x06 must NOT reach dma_reg[1]")

#  THE SAME DEFECT POINTING THE OTHER WAY.  The source comment claims the guard
#  "also stops leaking the aliased word's value" -- and no row pinned it, so a
#  seat restricted the guard to `&& writeflag == MEM_WRITE`, scored 27/27, and
#  read dma_reg[1] out through a 16-bit load at +0x06.  An UNPINNED CLAIM IN A
#  COMMENT IS NOT A PROPERTY.
t, alive = session(pair(["r7=0x%x" % (DMA + 0x04), "r8=0x11223344",
                         "r3=0x%x" % (DMA + 0x06), "r2=0"],
                        [MOV_L_R8_AT_R7, MOV_W_AT_R3_R2]) + ["print r2"])
row("dma rdleak", printed(t, "r2") if alive else "died", "0x0",
    "an unaligned declined READ returns 0, not the aliased word")

#  *** THE SEPARATE-ARRAYS CLAIM, WHICH NO ROW REACHED. ***
#
#  Two windows, two latch arrays, and the source calls confusing them
#  "invisible by construction".  It WAS: every row above drives ONE window, so
#  a DMA arm keyed into the control array passes all of them, and so does a
#  control arm keyed into the DMA array (which additionally writes past it).
#
#  Both windows in ONE session at the SAME word index, so a shared array
#  latches the first access and SILENCES the second.  Different indices would
#  not do it -- that is why this row is not `dma two` with a control offset.
#
#  *** IT DRIVES BOTH DIRECTIONS, AND THE READ-ONLY VERSION WAS WEAKER. ***  A
#  seat pointed out that a read-only row is blind to a DIRECTION-ASYMMETRIC
#  cross-wiring -- only the WR arms swapped -- because every other row that
#  counts a write diagnostic drives ONE window.  Four accesses in the same
#  session cost nothing extra and expect 2/2, which additionally kills that
#  variant (it would read 2/1).
t, alive = session(pair(["r1=0x%x" % UNIMPL_A, "r3=0x%x" % (DMA + 0x00),
                         "r7=0x%x" % UNIMPL_A, "r8=0x5a5a5a5a",
                         "r5=0x%x" % (DMA + 0x00), "r6=0x5a", "r2=0"],
                        [MOV_L_AT_R1_R2, MOV_L_AT_R3_R2,
                         MOV_L_R8_AT_R7, MOV_L_R6_AT_R5]))
row("both windows",
    ("%d/%d" % (len(SAYS.findall(t)), len(DMA_SAYS.findall(t)))) if alive else "died",
    "2/2", "same word index, both windows, BOTH directions")

#  *** THE OBLIGATION THIS ROUND OWED AND HAD NOT PAID. ***
#
#  `accept8` exists because three narrowing mutants -- deleting ONE `case`
#  label at a time -- each scored full marks against the control window.  The
#  de-escalation clause says a fatal->survive fix DELETES the accidental
#  tripwire that made such an edit self-announcing, so the detector must pin
#  the ACCEPT SIDE of every de-fatalised predicate.
#
#  The DMA window got the same fix and NO accept row.  A seat traced it: delete
#  `case 0x18:` and the DMA trigger silently dies forever, where BEFORE this
#  round that deletion was a loud exit on the first touch.  That is the clause's
#  own scenario, applied to one window and not the other.
#
#  *** A READ AT +0x18 IS SAFE, AND THE REASON IS NOT THE ONE THE FIRST
#  DRAFT OF THIS COMMENT GAVE. ***  It said 'the arm is guarded on idata',
#  which is true but stops one step short of the property that matters.
#
#  `case 0x18` arms on `if (idata != 0)` with NO write-direction test of its
#  own.  What makes a read safe is 140 lines above it: `idata` is declared
#  `= 0` and assigned ONLY under `if (writeflag == MEM_WRITE)`, so on a read
#  it keeps its initialiser and the arm cannot fire.  That is a real, local,
#  self-contained guarantee -- NOT an accident of memory_rw memsetting the
#  caller's buffer, which is what it would be if idata were loaded
#  unconditionally.
#
#  Written out because a pass-3 seat asked for an explicit write-direction
#  condition around the arming, not seeing that one already exists at that
#  distance.  A guard 140 lines from what it protects is correct and hard to
#  see, and this row depends on it.
t = ""
alive = True
for off in (0x04, 0x08, 0x0c, 0x14, 0x18):
    tt, aa = session(pair(["r1=0x%x" % (DMA + off), "r2=0"], [MOV_L_AT_R1_R2]))
    t += tt
    alive = alive and aa
row("dma accept", ("%d" % len(DMA_SAYS.findall(t))) if alive else "died", "0",
    "all five implemented DMA offsets stay off the default arm")

n = sum(1 for _, ok in rows if ok)
print("GDROM_DEF_RESULT=%d/%d" % (n, len(rows)))
print("GDROM_DEF_VECTOR=" + ",".join(("1" if ok else "0") for _, ok in rows))
