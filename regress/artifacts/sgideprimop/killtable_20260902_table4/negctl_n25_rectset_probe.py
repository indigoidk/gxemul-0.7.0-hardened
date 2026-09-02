#!/usr/bin/env python3
"""#500 sgideprimop DETECTOR -- draw_primitive()'s unimplemented drawing op.

WHAT THE FIX DID.  `draw_primitive()' ended with

    default: fatal("[ sgi_de: UNIMPLEMENTED drawing op = 0x%08x, ... ]"); exit(1);

and `op' comes straight from a guest-written register.  The switch discriminates
on the TOP BYTE only, so the domain is 256 values and only two are implemented.
A guest-written drawing op ended the host process.  It is now a latched decline
that falls out of the switch and returns.

*** THE TWO KILLERS THAT MATTER ARE NOT EXOTIC VALUES.  crmfbreg.h names four
primitives, and note the constants are FULL 32-BIT VALUES, not top-byte indices:
DE_PRIM_POINT 0x00000000, LINE 0x01000000, TRIANGLE 0x02000000, RECTANGLE
0x03000000.  Writing them as "0x01" invites a `case 0x02:' that can NEVER match,
because the switch compares `op & 0xff000000'.  The model implements LINE and
RECTANGLE only.  POINT and TRIANGLE are DOCUMENTED
primitives interleaved with the implemented pair.  And POINT is 0x00000000,
which is ALSO THE RESET VALUE: dev_sgi_re_init memsets the device struct, so
CRIME_DE_PRIMITIVE reads 0 until a guest writes it.  A guest that set the START
bit having never written the primitive register at all died here.  It need not
choose a bad value; it need only omit a good one. ***

CONTRACT (vacuity-floor clause (e)) -- which edits this detector is designed to
catch, and which it is NOT:

  CATCHES
    * reinstatement of the host kill, at either killer value (`pt surv',
      `tri surv') and at the reset path (`reset surv');
    * *** THE KILL REINSTATED AS exit(0) RATHER THAN exit(1). ***  This is the
      one that matters most here and it is why no row in this file uses exit
      status as its only oracle.  EXIT STATUS CANNOT VARY between "declined and
      then quit" and "died with status 0" -- a sibling round MEASURED that shape
      as a 48/48 clean sweep on the day this was written.  Every survival row is
      PAIRED with a positive post-draw observable (`* live'), which reads
      "absent" when the host is gone and therefore reds on a death HOWEVER THE
      DEATH IS SPELLED;
    * loss of the latch in EITHER direction, and they are different mutants:
        - dropping the `!' makes the bit never set, so the announce NEVER fires
          -- a SILENT decline, caught by the `* decl' rows wanting one message;
        - dropping the `|=' makes the announce fire EVERY time -- a FLOOD, which
          a "at least one message" row PASSES.  Only `two once' catches it,
          because it performs TWO distinct defaulted draws in ONE session and
          wants EXACTLY one message.
      *** THE FLOOD MUTANT IS THE ONE THAT ESCAPES A NAIVE ROW SET, and this
      file's own author had it backwards in a pass-2 brief until the glm seat
      corrected him. ***
    * *** ANY WIDENING OF THE SWITCH MASK INTO THE LIVE MODIFIER BITS.  This took
      THREE passes and the first two repairs were both cell-shaped: `& 0xffff0000'
      swept the 19-row version clean, so two rows were added carrying bits 16 and
      18 -- and then `& 0xff020000' swept the 21-row version clean, because bit 17
      was still unpinned.  The rows now carry ALL THREE live modifier bits
      (RL 16, TB 17, SKIP_END 18, derived by grepping every read of `op'), so the
      WIDENING half of the class is closed rather than sampled. ***
    * *** AND A NARROWED SWITCH MASK AT ANY OF THE SIX HIGH BITS.  The first
      attempt pinned bit 26 ALONE and a seat swept it with a bit-27 narrowing;
      the space is bits 26-31, which must be zero for an implemented op, so all
      six are now enumerated (`dec b26'..`dec b31').  ***
    * *** the older, narrower form of that clause, kept for its reasoning:
      The implemented values are 0x01 and 0x03, so only bits 24-25 carry
      information and every other row's op has bits 26-31 CLEAR.  `& 0x03000000'
      would therefore leave every one of them green while making an unimplemented
      op ALIAS ONTO an implemented case -- 0x05000000 would be DRAWN AS LINE
      instead of declined, which silently draws rather than wrongly refusing.
      `dec hi bit' is the only row with a bit above 25 and is the only thing that
      can see it. ***
    * a repair applied to the WRITE direction only (`rd surv', `rd decl') --
      `if (startFlag)' is not conditioned on MEM_WRITE, so a START-aliased READ
      draws too.  Named by a seat; no row covered it before.

  DOES NOT CATCH
    * *** BOTH NO-ROW CLAUSES THAT USED TO SIT HERE ARE GONE, AND ONE OF THEM WAS
      A WRONG RECORD THE DIFF ITSELF FALSIFIED.  A seat caught it: the [31:26]
      clause declared "a legal LINE with a high bit set ... DELIBERATELY NO ROW"
      while `dec hi bit' -- added ONE CLAUSE ABOVE IT, in the same diff -- stores
      0x05000000, which is exactly that.  The stale clause is what let an earlier
      pass call a shrink-escape "consistent, deliberately disclaimed".  Both
      ranges are now COVERED: bits 0-23 by the widened accept ops, bits 26-31 by
      `dec b26'..`dec b31'.  Recorded rather than deleted, because a no-row
      clause that outlives its own refutation is how a hole gets blessed. ***

    * *** AND THE "BITS 24-25" GROUPING WAS ITSELF WRONG -- L4, corrected here
      after a packet-fed seat did the arithmetic.  The two bits do NOT behave
      alike and only ONE of them ever needed a new oracle:

          & 0xfd000000  (clear bit 25)   LINE -> LINE,  RECT -> LINE   COLLAPSE
          & 0xfe000000  (clear bit 24)   LINE -> 0x00,  RECT -> 0x02   both to
                                                        `default:', both DECLINED

      Clearing bit 24 sends BOTH implemented ops to the decline arm, so
      `acc rect' and `acc line' redden -- it was COVERED FROM THE START by the
      accept rows and needed nothing new.  Only bit 25 collapses one primitive
      onto the other, and only bit 25 is what `n25 rect' / `n25 line' exist for.
      *** I bundled the two because they are ADJACENT, not because they behave
      alike, and then carried the bundle into four other records. *** ***

    * *** THIS CLAUSE SAID BITS 24-25 WERE UNCOVERABLE.  MEASURED FALSE -- a
      review seat refuted it by reading the product code, and the rows `n25 rect'
      / `n25 line' now cover it.  The refuted text is kept below rather than
      deleted, because a no-row clause that outlives its own refutation is how a
      hole gets blessed -- an earlier clause in this same file did exactly that.
      WHAT WAS WRONG: every FACT in it held (a collapse restores no host kill; a
      pixel oracle does not exist at reset) and the CONCLUSION did not follow,
      because `case DE_PRIM_LINE:' opens with an XFER_EN diagnostic that exists
      in that arm and nowhere else.  I had read that line earlier in the round
      and did not connect it. ***

    * *** (REFUTED, kept for its reasoning) NARROWING AT BIT 24 OR 25 -- the one
      mask cell that is genuinely out of reach, and it is out of reach for a
      reason no row count can fix.  Those two
      bits are the only ones carrying information (LINE 0x01, RECTANGLE 0x03), so
      dropping one COLLAPSES THE TWO IMPLEMENTED CASES ONTO EACH OTHER rather
      than restoring a host kill.  Every row here would stay green, correctly:
      both values are still accepted and the guest still runs.  Seeing it needs a
      DRAWING oracle, and there is none to build at reset -- a seat traced that
      `horrible_getputpixel' returns immediately on a TLB pointer with bit 31
      clear, so even a "successful" draw writes nothing observable.  DISCLOSED,
      NOT COVERED, and it is the same drawing-oracle gap as the last clause
      below rather than a new species. ***
    * anything about WIDTH -- that is sgi_de_width_probe.py, which also owns the
      `tail_acc*' rows that pin draw_primitive's REACHABILITY;
    * the drawing itself.  A declined op draws nothing, and nothing here asserts
      what a correct POINT or TRIANGLE would have rendered.
"""

import os
import pty
import re
import select
import sys
import time

BIN = sys.argv[1] if len(sys.argv) > 1 else "build/gxemul"
LABEL = sys.argv[2] if len(sys.argv) > 2 else "local"

#  A load file is REQUIRED by -V ... 0x80001000:<file>.  The in-tree fixture if
#  it exists, /dev/null if not -- the same fallback the sibling probes use.
DUMMY = "dummy_kernel.bin" if os.path.exists("dummy_kernel.bin") else "/dev/null"

CODE = 0xffffffff80001000
DE = 0xffffffffb5002000              # sgi_de        @ phys 0x15002000
#  *** DE_STATUS IS GONE.  It was UNUSED after devsig attempt 3, and it was
#  MISLABELLED throughout: phys 0x15003000 is the sgi_mte window; sgi_de_status
#  is at 0x15004000 (dev_sgi_re.c:36-37).  A seat found both in one sentence. ***
RE = 0xffffffffb5001000              # sgi_re        @ phys 0x15001000
UNMAP_W = 0x800                      # #499's unmapped-WRITE window -> UNMAP_WR
UNMAP_R = 0x900                      # #499's unmapped-READ  window -> UNMAP_RD

#  0x060 is CRIME_DE_PRIMITIVE; 0x800 is the START alias.  A single access to
#  0x860 therefore SETS the op and TRIGGERS the draw -- which is why the round's
#  first witness was confounded: a START-aliased WRITE also writes the register,
#  so the trigger value BECOMES op.  That is a feature here, not a hazard: it is
#  exactly how a guest reaches draw_primitive in one instruction.
PRIM_START = 0x860
PRIM_ONLY = 0x060
DRAWMODE = 0x018                     # CRIME_DE_DRAWMODE 0x2018, device-relative
XFER_EN = "0x00200000"               # DE_DRAWMODE_XFER_EN
XFER_LINE = "sgi_de: XFER_EN for LINE op?"
START_ONLY = 0x800

OP_NOP = 0x00000000
OP_B_SELF = 0x1000ffff
OP_SB_T0_A3 = 0xa0e80000             # sb   $t0, 0($a3)
OP_SW_T0_A3 = 0xace80000             # sw   $t0, 0($a3)
OP_LW_V0_AT = 0x8c220000             # lw   $v0, 0($at)
OP_LBU_V0_AT = 0x90220000            # lbu  $v0, 0($at)

#  DRAW matches the kill AND the decline -- the prefix is deliberately kept, so
#  that #499's `hi_draw'/`hi_rd_draw' rows are not silently blinded.  That makes
#  it useful for "did a draw happen at all" and USELESS for "was it declined".
DRAW = "sgi_de: UNIMPLEMENTED drawing op"


def declined(opval):
    """The FULL declined literal for one op value.

    *** THE `decl' ROWS ORIGINALLY COUNTED `DRAW', AND A REVIEW SEAT FOUND THAT
    VACUOUS: it is a substring the decline SHARES WITH THE PRE-FIX KILL, so a
    mutant reverting the message text passes, and the row cannot tell a fixed
    build from an unfixed one.  A `DECLINED' constant was defined in this file
    and never used -- the constant existed and the rows did not reach for it. ***

    This form pins the op VALUE and the `-- declined.  (once)' suffix together,
    so it is un-fakeable by either a text revert or a wrong-op decline.
    """
    return ("UNIMPLEMENTED drawing op = %s, x1=0 y1=0 x2=0 y2=0"
            " fg=0x0 bg=0x0 pattern=0x00000000 -- declined.  (once) ]" % opval)
SENTINEL = 0xdeadbeef

rows = []


def row(name, got, want, note=""):
    #  <= 15 chars: the name column is %-16s and the gate's per-row pattern needs
    #  TWO spaces after the name.  A 16-char name emits ONE and the gate check
    #  becomes unsatisfiable -- a RED gate on a GREEN probe.  A sibling round
    #  shipped exactly that and it was found by a review seat, not by the gate.
    #  *** A DUPLICATE ROW NAME IS A CORRUPT INSTRUMENT, AND IT ONCE REPORTED
    #  38/38 GREEN.  A bad splice duplicated seven rows; every one of them passed
    #  twice and the run looked like the best table in the file's history.  The
    #  gate would have caught it -- its per-row check wants exactly 1 -- but only
    #  after a 15-minute run and only as an unexplained got=2.  One line here
    #  fails at the point of construction instead. ***
    assert name not in [n for n, _ in rows], (
        "DUPLICATE ROW NAME %r -- the probe is corrupt, not merely wrong" % name)
    assert len(name) <= 15, (
        "row name %r is %d chars; the gate pattern needs <= 15" % (name, len(name)))
    ok = (got == want)
    rows.append((name, ok))
    print("%-16s %-14s %-14s %-44s %s" % (name, str(got), str(want), note,
                                          "ok" if ok else "FAIL"))
    return ok


def session(cmds, settle=1.5, spin=1.4):
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
        if not rd(spin if i == len(cmds) - 1 else 0.25):
            alive = False
            break
    try:
        os.write(fd, b"quit\n")
        rd(0.4)
    except OSError:
        pass
    try:
        os.close(fd)
    except OSError:
        pass
    how = "nostatus"
    try:
        _, stat = os.waitpid(pid, 0)
        if os.WIFSIGNALED(stat):
            how = "sig%d" % os.WTERMSIG(stat)
        elif os.WIFEXITED(stat):
            how = "exit%d" % os.WEXITSTATUS(stat)
    except OSError:
        pass
    return buf.replace("\r", ""), alive, how


def printed(t, reg):
    m = re.search(r"print\s+%s\s*\n\s*(0x[0-9a-f]+)" % reg, t)
    if not m:
        return "absent"
    return "0x%x" % int(m.group(1), 16)


class Addr(object):
    """A FRESH code address per instruction sequence.

    `step' advances pc, so a second sequence written to the SAME address finds pc
    already set there, the assignment is skipped, and the guest executes the
    following nop instead of the store.  A sibling probe lost a row to exactly
    that, so the hazard is designed out rather than remembered.
    """

    def __init__(self, base):
        self.a = base

    def take(self, n):
        got = self.a
        self.a += 4 * (n + 2) + 0x20
        return got


def run_ops(ops, at):
    put = ["put w 0x%x, 0x%08x" % (at + 4 * i, op) for i, op in enumerate(ops)]
    put += ["put w 0x%x, 0x%08x" % (at + 4 * len(ops), OP_B_SELF),
            "put w 0x%x, 0x%08x" % (at + 4 * len(ops) + 4, OP_NOP)]
    return put + ["pc=0x%x" % at, "step %d" % len(ops)]


def store(A, addr, val, op=OP_SW_T0_A3):
    return ["a3=0x%x" % addr, "t0=%s" % val] + run_ops([op], A.take(1))


def load(A, addr, op=OP_LW_V0_AT):
    #  Preset to a SENTINEL, never 0: preset to 0 and a row cannot tell "the
    #  access completed and returned 0" from "the access never happened".
    return ["at=0x%x" % addr, "v0=0x%x" % SENTINEL] + run_ops([op], A.take(1))


print("#500 sgideprimop DETECTOR -- binary=%s label=%s" % (BIN, LABEL))
print("%-16s %-14s %-14s %-44s %s" % ("row", "got", "want", "note", ""))

# ------------------------------------------------------------ controls (c)
#  Clause (ii) of the witness ladder: an access witness owes a LIVENESS control
#  (a known value returns through the same decode) AND a DEVICE-SIGNATURE
#  control (the value could only have come from the device -- RAM would answer
#  differently).  One is not enough: a sibling probe's first draft returned 0x0
#  everywhere WITH its RAM control green.
A = Addr(CODE)
t, alive, how = session(store(A, 0xffffffff80002000, val="0x5a5a5a5a")
                        + load(A, 0xffffffff80002000) + ["print v0"])
row("live", printed(t, "v0") if alive else "died", "0x5a5a5a5a",
    "RAM round-trips through the same decode -- the probe can see anything at all")

#  *** THIS CONTROL TOOK THREE ATTEMPTS AND THE FIRST TWO ARE WORTH RECORDING,
#  because both failed in ways the carrier already warns about. ***
#
#  ATTEMPT 1 asserted only `printed(...) != "absent"' -- that SOMETHING answered --
#  while its note claimed "a DEVICE answers, not RAM".  RAM answers too, so the row
#  could not distinguish them and the note asserted a test that was not being made:
#  a vacuous row carrying a false record.  A review seat caught it.
#
#  ATTEMPT 2 tried a write-that-does-not-stick at DE_STATUS+0, on the assumption
#  that a device register would not return what was written to it.  MEASURED: it
#  returns 0x5a, exactly what was written.  That address round-trips like RAM, so
#  the premise was false and the row correctly went RED on a good build.
#
#  ATTEMPT 3, and this one is measured rather than assumed: use a channel RAM
#  CANNOT PRODUCE AT ALL -- a device DIAGNOSTIC.  A byte store to sgi_de trips
#  #498's width guard and emits "[ sgi_de: unimplemented len=1 -- declined.
#  (once) ]".  No memory location emits text.  It is also INDEPENDENT of
#  draw_primitive, so it controls for "a device is there" without borrowing the
#  channel the rows under test use.
#
#  *** AND THE FORK ALREADY HAD ONE.  I INVENTED THREE TIMES WITHOUT LOOKING. ***
#  sgi_re_width_probe.py carries `devsig stat': CRIME_DE_STATUS reads the fixed
#  architectural value 0x1e000000, and RAM would read 0.  That is a cleaner
#  signature than this one -- a constant the hardware defines, needing no
#  diagnostic text -- and it was sitting in a sibling file the whole time.
#  Attempt 2 failed at DE_STATUS+0 for exactly the reason that row would have
#  taught me: the discriminating offset is not the base.
#
#  This row is KEPT rather than replaced, because two independent channels are
#  worth more than one: a fixed-value read and a device-only diagnostic fail for
#  different reasons.  But the lesson is the project's own standing rule --
#  GREP THE FORK FOR THE EXISTING IDIOM BEFORE INVENTING -- and it cost three
#  attempts here on the same day it was applied successfully twice elsewhere.
A = Addr(CODE)
t, alive, how = session(store(A, DE + 0x0, val="0x5a", op=OP_SB_T0_A3))
row("devsig", t.count("sgi_de: unimplemented len=1 -- declined.  (once) ]"), 1,
    "a byte access makes the DEVICE speak -- RAM emits no text, ever")

# ------------------------------------------------------- the two named killers
#  POINT and TRIANGLE are DOCUMENTED primitives that the model does not
#  implement.  Each gets survival AND a positive post-draw observable, because a
#  survival-only oracle cannot tell a decline from an exit(0).
for nm, opval in (("pt", "0x00000000"), ("tri", "0x02000000")):
    A = Addr(CODE)
    t, alive, how = session(store(A, DE + PRIM_START, val=opval)
                            + load(A, 0xffffffff80002000) + ["print v0"])
    row(nm + " surv", how, "exit0",
        "%s (%s) is declined, not fatal" % (nm.upper(), opval))
    row(nm + " live", printed(t, "v0") if alive else "died", "0x0",
        "...and the guest RUNS ON -- kills a death however it is spelled")
    row(nm + " decl", t.count(declined(opval)), 1,
        "...announced ONCE with the FULL literal -- kills a text revert")

# ------------------------------------------------- the reachability headline
#  op reads the RESET value, so a START access with CRIME_DE_PRIMITIVE never
#  written draws POINT.  This is the row that pins "it need only omit a good
#  value", and nothing else in the tree asserts it.
A = Addr(CODE)
t, alive, how = session(store(A, DE + START_ONLY, val="0x00000000")
                        + load(A, 0xffffffff80002000) + ["print v0"])
row("reset surv", how, "exit0",
    "START with PRIMITIVE never written -- the reset value IS POINT")
row("reset live", printed(t, "v0") if alive else "died", "0x0",
    "...and the guest RUNS ON")
row("reset decl", t.count(declined("0x00000000")), 1,
    "...announced with the FULL literal -- the draw really happened")

# ------------------------------------------------------------- the LATCH rows
#  TWO distinct defaulted primitives in ONE session, wanting EXACTLY one message.
#  *** THIS IS THE ROW THAT CATCHES THE FLOOD MUTANT (dropping the `|='), which a
#  "at least one message" row passes.  The SILENT mutant (dropping the `!') is
#  caught by the `* decl' rows above.  Two different latch mutants, two different
#  killers, and only this one is exact-count. ***
A = Addr(CODE)
t, alive, how = session(store(A, DE + PRIM_START, val="0x00000000")
                        + store(A, DE + PRIM_START, val="0x02000000")
                        + load(A, 0xffffffff80002000) + ["print v0"])
row("two once", t.count(DRAW), 1,
    "TWO distinct declined ops, ONE message -- kills a dropped |= (flood)")
row("two live", printed(t, "v0") if alive else "died", "0x0",
    "...and the guest survives both")

# ------------------------------------------------------------ the READ arm
#  `if (startFlag)' is not conditioned on MEM_WRITE, so a START-aliased READ
#  draws too -- with whatever op the register already holds, i.e. the reset
#  value.  A repair applied to the write direction only escapes every row above.
A = Addr(CODE)
t, alive, how = session(load(A, DE + START_ONLY) + ["print v0"])
row("rd surv", how, "exit0",
    "a START-aliased READ also draws, and is declined")
row("rd decl", t.count(declined("0x00000000")), 1,
    "...announced with the FULL literal -- kills a write-only repair")

# --------------------------------------------------- the CROSS-LATCH row
#  *** EVERY ROW ABOVE RUNS IN A FRESH SESSION WITH NO PRIOR DEVICE TRAFFIC, AND A
#  REVIEW SEAT POINTED OUT WHAT THAT CANNOT SEE: a bit-value mutant onto an
#  ALREADY-USED bit (1 << 6 is #498's SGIRE_W_DE_LEN, 1 << 8 is #499's UNMAP_RD)
#  leaves those latches CLEAR in a fresh session, so the announce still fires and
#  every row above passes.  The collision is only visible once something else has
#  ALREADY SET the colliding bit. ***
#
#  It matters because the four sgi_re/sgi_de/sgi_mte/sgi_de_status handlers share
#  ONE malloc'd struct, so `d->warned' is shared ACROSS DEVICES -- #498 measured a
#  reused bit at 23/25, and BOTH #499 and this round were originally designed for
#  1 << 7.  The collision was caught by a human listing the enum, which is exactly
#  the kind of catch that should not be relied upon.
#
#  So: fire the #498 width latch FIRST with a byte access, THEN trigger the draw,
#  and require the prim-op decline ANYWAY.  Under a colliding bit the first access
#  pre-sets it and this row goes silent.
A = Addr(CODE)
t, alive, how = session(store(A, DE + 0x0, val="0x5a", op=OP_SB_T0_A3)
                        + store(A, DE + PRIM_START, val="0x02000000")
                        + load(A, 0xffffffff80002000) + ["print v0"])
row("xlatch decl", t.count(declined("0x02000000")), 1,
    "prim-op decline fires even AFTER another latch set -- kills a shared bit")
row("xlatch live", printed(t, "v0") if alive else "died", "0x0",
    "...and the guest survives the composed session")

#  *** AND ONE PRE-SET LATCH IS ONE CELL, NOT THE CLASS -- SAME MISTAKE, SAME
#  ROUND, ONE ROW OVER.  Two seats found it independently. ***
#
#  `xlatch decl' above pre-fires exactly ONE colliding bit, #498's 1 << 6.  The
#  enum's OTHER already-used bits are #499's 1 << 7 (UNMAP_WR) and 1 << 8
#  (UNMAP_RD), and NO row in this file raises either before drawing -- so
#  aliasing SGIRE_W_PRIM_OP onto 1 << 7 or 1 << 8 left all 30 rows green while
#  making the decline go silent after ordinary unmapped traffic.  A one-token
#  edit to the very constant this round ADDED: floor clause (d), not coverage
#  debt.
#
#  The four handlers share one `d->warned', so the unmapped windows on sgi_re
#  set latches that the sgi_de draw path then tests.  Raising BOTH in one
#  session closes the remaining pair; with 1 << 6 above, every already-used bit
#  in the enum is now pre-set by some row.
A = Addr(CODE)
t, alive, how = session(store(A, RE + UNMAP_W, val="0x5a")
                        + load(A, RE + UNMAP_R)
                        + store(A, DE + PRIM_START, val="0x02000000")
                        + load(A, 0xffffffff80002000) + ["print v0"])
row("xlatch unm", t.count(declined("0x02000000")), 1,
    "decline fires after BOTH #499 unmapped latches -- kills an alias onto 1<<7 or 1<<8")
row("xlatch unliv", printed(t, "v0") if alive else "died", "0x0",
    "...and the guest RUNS ON through the four-access session")

#  *** AND THREE PRE-SET BITS IS THREE CELLS, NOT THE CLASS.  FOUND BY THE
#  PRE-TABLE BLOCK -- the mandatory check I had SKIPPED, run late, which located
#  in one grep what four panels had left. ***
#
#  The block asks: WHO ELSE WRITES THIS FIELD, AND CAN THEY SET MY BIT?  The
#  answer is `grep -c "d->warned |=" dev_sgi_re.c` -> TEN sites, bits 0..9.
#  The rows above pre-set THREE of them (1<<6 via a byte access, 1<<7 and 1<<8
#  via the unmapped windows).  Aliasing SGIRE_W_PRIM_OP onto any of 1<<0..1<<5
#  -- the six *_LEN latches -- escaped every row, for exactly the reason 1<<7
#  did: nothing raised those latches before drawing.
#
#  ONE ROW CLOSES THE WHOLE SPACE, and that is the point.  Every *_LEN latch
#  fires on a wrong length at its own window, so a WORD store to each of the six
#  windows raises bits 0-5; the byte access raises 6; the unmapped write and
#  read raise 7 and 8.  With bits 0-8 all set, an alias onto ANY of them goes
#  silent and this row reds.  Nine cells, one row -- because the closure is over
#  the FIELD, not over the individual bits.
#
#  The narrower rows above are KEPT: they are already measured, they cost
#  nothing, and they say WHICH bit collided, which this row cannot.
#  *** THE FIRST VERSION OF THIS ROW WAS MIS-BUILT, AND THE ENUMERATION SWEEP IS
#  WHAT CAUGHT IT.  M_ALIAS0..M_ALIAS5 each scored a CLEAN 34/34 -- the row was
#  green because NOTHING HAD SET THOSE BITS, which is the vacuous-by-construction
#  shape exactly: a row whose channel cannot vary under its named mutant. ***
#
#  The cause is one line of the device.  DEVICE_ACCESS(sgi_re) does
#  `relative_addr += 0x1000;' at dev_sgi_re.c:303, because the device is
#  REGISTERED at `baseaddr + 0x1000' with length 0x1000 -- so memory_rw hands the
#  handler an offset in [0, 0xfff] and the handler adds the window base back.
#
#  CRIME_RE_TLB_A is therefore at DEVICE OFFSET 0x000, not 0x1000:
#
#      window            constant   relative_addr   offset from RE
#      CRIME_RE_TLB_A    0x1000     0x1000          0x000
#      CRIME_RE_TLB_B    0x1200     0x1200          0x200
#      CRIME_RE_TLB_C    0x1400     0x1400          0x400
#      CRIME_RE_TEX      0x1600     0x1600          0x600
#      CRIME_RE_LINEAR_A 0x1700     0x1700          0x700
#      CRIME_RE_LINEAR_B 0x1780     0x1780          0x780
#
#  The first version used the CONSTANTS as offsets, so every one of the six
#  accesses landed at 0x2000..0x2780 -- past the end of a 0x1000-long device, so
#  they reached this device not at all.  `#499's UNMAP_W/UNMAP_R (0x800/0x900)
#  were right for the same reason the others were wrong: they are already
#  device-relative.
#
#  *** THE GENERAL LESSON, AND IT IS THE ONE THIS FILE KEEPS RE-LEARNING: A ROW
#  THAT PASSES PROVES NOTHING UNTIL A MUTANT MAKES IT FAIL.  This row was green
#  on the fixed build, green on every mask mutant, and green on the six alias
#  mutants it was written to kill -- and only the last of those was a defect. ***
A = Addr(CODE)
t, alive, how = session(store(A, RE + 0x000, val="0x5a")       # TLBA_LEN  1<<0
                        + store(A, RE + 0x200, val="0x5a")     # TLBB_LEN  1<<1
                        + store(A, RE + 0x400, val="0x5a")     # TLBC_LEN  1<<2
                        + store(A, RE + 0x600, val="0x5a")     # TEX_LEN   1<<3
                        + store(A, RE + 0x700, val="0x5a")     # LINA_LEN  1<<4
                        + store(A, RE + 0x780, val="0x5a")     # LINB_LEN  1<<5
                        + store(A, DE + 0x0, val="0x5a", op=OP_SB_T0_A3)   # DE_LEN 1<<6
                        + store(A, RE + UNMAP_W, val="0x5a")   # UNMAP_WR  1<<7
                        + load(A, RE + UNMAP_R)                # UNMAP_RD  1<<8
                        + store(A, DE + PRIM_START, val="0x02000000")
                        + load(A, 0xffffffff80002000) + ["print v0"])
row("xlatch all", t.count(declined("0x02000000")), 1,
    "decline fires with ALL NINE other latch bits set -- closes the alias space")
row("xlatch alliv", printed(t, "v0") if alive else "died", "0x0",
    "...and the guest RUNS ON through the eleven-access session")

#  *** AND THE ROW ABOVE ASSERTS A PRECONDITION THAT NOTHING VERIFIED.  That is
#  how its first version shipped green while touching none of the bits it named. ***
#
#  "decline fires with ALL NINE other latch bits set" is only true if the six
#  window stores actually LAND on their windows.  When they did not, the row was
#  green for the wrong reason -- and stayed green under every mask mutant and
#  under the six alias mutants it existed to kill.  Only M_ALIAS0..5 could see it,
#  and only because the enumeration sweep built them.
#
#  THIS ROW MAKES THE PRECONDITION AN OBSERVABLE.  Each of the six *_LEN guards
#  prints one latched decline, so the session must contain exactly six.  If an
#  offset is ever wrong again, THIS row reds on the FIXED BUILD -- no mutant
#  required, and the failure names itself instead of hiding inside a green row.
#
#  *** THE GENERAL FORM, and it is the cheap half of the vacuity floor: A ROW
#  THAT DEPENDS ON A SET-UP STEP OWES A ROW THAT THE SET-UP STEP HAPPENED. ***
row("xlatch pre", t.count("sgi_re: unimplemented len="), 6,
    "the six window stores really landed -- pins the precondition xlatch all needs")

# ------------------------------------------------------------- ACCEPT control
#  The de-escalation clause: a fix that removes a host-fatal guard destroys the
#  accidental tripwire that made over-broad declining self-announcing.  So the
#  ACCEPT side is pinned -- an IMPLEMENTED primitive must still be drawn and must
#  NOT be announced as unimplemented.
A = Addr(CODE)
t, alive, how = session(store(A, DE + PRIM_START, val="0x03000000")
                        + load(A, 0xffffffff80002000) + ["print v0"])
row("acc rect", t.count(DRAW), 0,
    "RECTANGLE is IMPLEMENTED -- it must NOT be declined")
row("acc live", printed(t, "v0") if alive else "died", "0x0",
    "...and the guest runs on")

#  *** THE ACCEPT ROWS ABOVE PIN THE PREDICATE'S VALUE AND NOT ITS WIDTH, AND A
#  MEASURING SEAT SWEPT THIS DETECTOR 19/19 CLEAN WITH ONE HEX DIGIT:
#  `switch (op & 0xff000000)' -> `& 0xffff0000'. ***
#
#  Both rows above store 0x03000000 -- the low 16 bits are ZERO -- so a mask that
#  grew to cover bits 16-31 still matches them and they stay green.  But
#  crmfbreg.h puts THREE REAL, IMPLEMENTED modifier bits down there:
#
#      DE_PRIM_RL            0x00010000   right to left   read at dev_sgi_re.c:703
#      DE_PRIM_TB            0x00020000   top to bottom   read at            :704
#      DE_PRIM_LINE_SKIP_END 0x00040000   line bound      read at            :735
#
#  So `RECTANGLE | RL' and `LINE | SKIP_END' are LEGAL primitives that the widened
#  mask SILENTLY DECLINES INSTEAD OF DRAWING.
#
#  This is the DE-ESCALATION CLAUSE in its purest form: before #500 that mutant
#  `exit(1)'s on the first right-to-left rectangle -- unmissable.  After #500 it is
#  a silent refusal to draw, and the accidental tripwire that announced it is gone.
#  It is also clause (f)'s accept-side lesson wearing a mask: an accept row at the
#  BASE tests one bound twice and the other never.
#  *** CLASS CLOSURE, NOT ANOTHER CELL.  THIRD PASS, THIRD BREACH OF ONE CLASS. ***
#
#  Pass 2 found the mask width unpinned and I added two rows carrying bit 16 and
#  bit 18.  Pass 3 found that bit 17 was STILL unpinned, so `& 0xff000000' ->
#  `& 0xff020000' -- one hex digit again -- swept the repaired 21 rows CLEAN.
#  Patching the demonstrated cell and leaving the symmetric one is the exact
#  pattern a sibling round spent four passes on, and the rule it minted says:
#  when two consecutive passes find breaches of ONE class, the next repair owes
#  the CLASS CLOSURE -- enumerate the full space from the function's own inputs
#  and close every cell in one diff.
#
#  THE ENUMERATION, DERIVED by grepping every read of `op' in draw_primitive()
#  rather than by listing the bits I happened to know:
#
#      bit 16      DE_PRIM_RL              read at dev_sgi_re.c:703  (dx)
#      bit 17      DE_PRIM_TB              read at             :704  (dy)
#      bit 18      DE_PRIM_LINE_SKIP_END   read at             :735  (loop bound)
#      bits 24-31  the primitive selector  read at             :723  (the switch)
#
#      bits 0-15   DE_PRIM_LINE_WIDTH_MASK -- READ BY NOTHING TODAY.  The only
#                  use is COMMENTED OUT at :729-730.  No row, deliberately: a row
#                  there would assert a reachability the code does not have.
#      bits 19-23  read by nothing at all.  No row, same reason.
#
#  So the LIVE modifier set is exactly bits 16, 17, 18, and each accept row now
#  carries ALL THREE.  Any widening of the switch mask that reaches ANY of them
#  reddens both rows -- the class is closed, not sampled.
#
#  AND THEY NOW HAVE POSITIVE COMPANIONS.  A review seat pointed out that
#  `count(DRAW) == 0' is NEGATIVE-ONLY: it is satisfied when the access never
#  happened at all, so a session that silently did nothing would pass.  Every
#  other survival row in this file is paired; these two were not.  The `* live'
#  rows read "absent" if the guest never got that far.
A = Addr(CODE)
#  *** AND `ALL THREE MODIFIER BITS' WAS STILL SAMPLING.  Three seats, reading
#  independently, found the same hole: bits 16-18 are the three the CODE reads,
#  but the mask can be widened to ANY of bits 0-23, and `& 0xff0000ff' or
#  `& 0xfff00000' left every row green while DECLINING the PROM's own LINE|width.
#
#  The fix is not twenty-four rows.  An accept op with ALL 24 low bits SET is
#  declined under a mask widened at ANY of them, so ONE value closes the whole
#  widening direction:  0x03ffffff & 0xff000000 == RECTANGLE (accepted today),
#  while 0x03ffffff & <any wider mask> is not a case value and reds this row. ***
t, alive, how = session(store(A, DE + PRIM_START, val="0x03ffffff")
                        + load(A, 0xffffffff80002000) + ["print v0"])
row("acc rect mod", t.count(DRAW), 0,
    "RECTANGLE|ALL 24 maskable low bits -- ANY mask widening reds this row")
row("acc rect liv", printed(t, "v0") if alive else "died", "0x0",
    "...and the guest RUNS ON -- the row above is not satisfied by nothing happening")

A = Addr(CODE)
t, alive, how = session(store(A, DE + PRIM_START, val="0x01ffffff")
                        + load(A, 0xffffffff80002000) + ["print v0"])
row("acc line mod", t.count(DRAW), 0,
    "LINE|ALL 24 maskable low bits likewise -- both implemented primitives")
row("acc line liv", printed(t, "v0") if alive else "died", "0x0",
    "...and the guest RUNS ON")

#  *** AND THE MASK HAS TWO FAILURE DIRECTIONS, NOT ONE -- AND MY FIRST ATTEMPT AT
#  THE SECOND ONE SAMPLED IT INSTEAD OF CLOSING IT.  FOURTH BREACH, SAME CLASS. ***
#
#  The switch reads bits 24-31.  The implemented values are 0x01 and 0x03, so bits
#  26-31 must be ZERO for an op to be implemented.  A mask NARROWED by clearing any
#  one of those bits makes an unimplemented op ALIAS ONTO an implemented case and be
#  SILENTLY DRAWN instead of declined -- which is worse than wrongly refusing.
#
#  ATTEMPT 1 used ONE op, 0x05000000, which carries bit 26 alone.  A review seat
#  found the hole immediately: `& 0xff000000' -> `& 0xf7000000' clears bit 27, that
#  op still declines, the row stays GREEN, and 0x09000000 gets drawn as LINE with
#  nothing to see it.  I had written "the mask has two failure directions" in this
#  very file, closed the widening one with ALL THREE modifier bits, and then pinned
#  the narrowing one at a SINGLE bit.
#
#  *** THE SPACE IS FINITE AND SMALL, SO IT IS ENUMERATED, NOT SAMPLED. ***  Six
#  bits must be zero for an implemented op, so six ops discriminate them -- each is
#  LINE with exactly one high bit added, so clearing THAT bit from the mask aliases
#  it onto LINE and clearing any other bit does not:
#
#      bit 26  0x05000000     bit 29  0x21000000
#      bit 27  0x09000000     bit 30  0x41000000
#      bit 28  0x11000000     bit 31  0x81000000
#
#  Six rows is not cell-by-cell repair: it is the COMPLETE enumeration of a
#  six-element space, which is what closure means when the space is finite.
for _bit, _op in ((26, "0x05000000"), (27, "0x09000000"), (28, "0x11000000"),
                  (29, "0x21000000"), (30, "0x41000000"), (31, "0x81000000")):
    A = Addr(CODE)
    t, alive, how = session(store(A, DE + PRIM_START, val=_op)
                            + load(A, 0xffffffff80002000) + ["print v0"])
    row("dec b%d" % _bit, t.count(declined(_op)), 1,
        "%s = LINE|bit%d MUST decline -- kills a mask narrowed at bit %d"
        % (_op, _bit, _bit))

#  ONE liveness companion for the family rather than six: the six rows above differ
#  only in which bit they carry, and a host death in any of them would show as a
#  missing message in that row.  This proves the shape of session they all use does
#  reach the tail and run on.
A = Addr(CODE)
t, alive, how = session(store(A, DE + PRIM_START, val="0x81000000")
                        + load(A, 0xffffffff80002000) + ["print v0"])
row("dec hi liv", printed(t, "v0") if alive else "died", "0x0",
    "...and the guest RUNS ON after the highest-bit decline")

#  *** THE `DISCLOSED, NOT COVERED' CLAUSE FOR BITS 24-25 WAS A WRONG RECORD, AND
#  A REVIEW SEAT REFUTED IT BY READING THE PRODUCT CODE.  L4 + L2. ***
#
#  I had recorded a mask narrowing at bit 24 or 25 as UNCOVERABLE: it collapses
#  the two IMPLEMENTED cases onto each other rather than restoring a host kill,
#  and seeing a wrong DRAW needs a pixel oracle, which does not exist at reset
#  (horrible_getputpixel returns early on a zero TLB pointer).  All of that is
#  true and NONE of it supports the conclusion.
#
#  `case DE_PRIM_LINE:' opens with a diagnostic that exists in THAT ARM AND
#  NOWHERE ELSE:
#
#      case DE_PRIM_LINE:
#              if (drawmode & DE_DRAWMODE_XFER_EN)
#                      fatal("[ sgi_de: XFER_EN for LINE op? ]\n");
#
#  So the two primitives ARE distinguishable, with no pixel oracle at all: set
#  XFER_EN, draw a RECTANGLE, and the message must NOT appear.  Under
#  `& 0xfd000000' the RECTANGLE folds onto LINE and it does.
#
#  *** TWO ROWS, NOT ONE, AND THIS IS THE ROUND'S OWN LESSON APPLIED THREE HOURS
#  LATE.  `n25 rect' asserts a count of ZERO, which is NEGATIVE-ONLY: it is
#  satisfied if the channel is dead for ANY reason -- a wrong register offset, a
#  guard I misread, a drawmode that never lands.  `n25 line' proves the SAME
#  channel does fire.  Earlier in this round `xlatch all' shipped green because
#  its set-up silently did nothing, and only a nine-mutant sweep caught it. ***
A = Addr(CODE)
t, alive, how = session(store(A, DE + DRAWMODE, val="0x03000000")
                        + store(A, DE + PRIM_START, val="0x03000000")
                        + load(A, 0xffffffff80002000) + ["print v0"])
row("n25 rect", t.count(XFER_LINE), 0,
    "RECTANGLE must NOT reach the LINE-only diagnostic -- kills a bit-25 narrowing")
row("n25 rectliv", printed(t, "v0") if alive else "died", "0x0",
    "...and the guest RUNS ON through the rectangle session")

#  *** THE PAIR HAD NO IN-SESSION WITNESS, AND A SEAT BUILT THE CLEAN SWEEP THAT
#  PROVES IT.  L2, floor clause (d), repaired here.  THIRD INSTANCE OF ONE CLASS
#  IN ONE ROUND. ***
#
#  The escaping mutant is a single operand swap using a value already present in
#  the edited body -- squarely inside clause (d)'s enumeration:
#
#      store(A, DE + DRAWMODE, val=XFER-EN)   ->   val="0x03000000"
#      (operator DEFANGED above: a verbatim copy of this store makes a mutator
#       searching for it match THREE sites instead of two, and mine did.)
#
#  XFER is then never enabled, so `n25 rect' counts zero LINE messages and stays
#  GREEN for the wrong reason -- and under M_NARROW_25 the folded rectangle
#  reaches the LINE arm with XFER disabled, emits nothing, and THE INTENDED KILL
#  IS DEFEATED.  All 38 rows green, BASE 38/38.
#
#  *** WHY MY EXISTING GUARD DID NOT COVER IT, in the seat's words: "the panel
#  treated a positive control in a DIFFERENT SESSION as proof that the rectangle
#  session did something.  It is not."  `n25 line' proves the LINE setup works in
#  ITS session; `n25 rectliv' proves only that the trailing load ran.  Neither
#  witnesses THIS session's stores.  My comment on the liveness row claimed
#  otherwise and was false; it is corrected above. ***
#
#  This is the `xlatch all' failure for the THIRD time in one round -- a row green
#  because its set-up silently did nothing -- and I had built the repair for the
#  second instance INTO A DIFFERENT SESSION, where it cannot do the job.
#
#  THE WITNESS IS IN THE PRODUCT CODE ALREADY, and it was chosen by DUMPING the
#  session's raw output BEFORE picking an oracle -- picking one after seeing which
#  strings happen to be present is fitting the test to the binary.  draw_primitive
#  announces its entry with BOTH operands this row needs:
#
#      [ sgi_de: STARTING DRAWING COMMAND: op = 0x03000000, drawmode=0x200000 ... ]
#
#  `op = 0x03000000' pins that the RECTANGLE store landed and the draw was
#  entered; `drawmode=0x200000' pins that the XFER_EN store landed.  Under the
#  swap the operand reads 0x3000000 and this row reds.  Under M_NARROW_25 the line
#  is UNCHANGED -- the mask governs the switch, not the announcement -- so the
#  witness does not mask the kill it exists to protect.
row("n25 rectset", t.count("op = 0x03000000, drawmode=0x200000"), 1,
    "BOTH stores of THIS session landed -- the in-session witness n25 rect needs")

A = Addr(CODE)
t, alive, how = session(store(A, DE + DRAWMODE, val=XFER_EN)
                        + store(A, DE + PRIM_START, val="0x01000000")
                        + load(A, 0xffffffff80002000) + ["print v0"])
row("n25 line", t.count(XFER_LINE), 1,
    "...and the SAME channel DOES fire for LINE -- so `n25 rect' is not vacuous")

#  *** WHAT THIS PAIR DOES NOT CATCH, NAMED RATHER THAN LEFT UNKNOWN.  A review
#  seat was asked for the smallest edit that defeats the pair and found one. ***
#
#  ONE ADDED CONJUNCT on the product-code guard defeats both rows:
#
#      if ((drawmode & DE_DRAWMODE_XFER_EN) && !(op & 0x02000000))
#
#  That silences the diagnostic for a FOLDED RECTANGLE while keeping it firing
#  for a genuine LINE -- `n25 rect' 0, `n25 line' 1, both green, and the
#  rectangle still drawn as a line.  The seat reached it by elimination and said
#  why nothing smaller works: the two rows differ in exactly ONE input (the op
#  value), so any edit leaving both green must make the string fire IFF the op
#  is LINE-shaped, i.e. it must consult `op'.  It checked the single-token
#  substitutions (drawmode->op, &->&&, &->|, & ~op, constant swaps) and every
#  one either kills the channel for both ops or fires for both, reddening a row.
#
#  *** DISCLOSED, NOT REPAIRED, AND THE REASON IS A SCOPE RULE RATHER THAN
#  DIFFICULTY: that guard is PRODUCT CODE THIS ROUND DOES NOT TOUCH.  Clause
#  (d)'s enumeration is closed over the diff's own hunks -- predicates dominating
#  the edited lines, plus operand swaps from fields the guarded body reads.  A
#  conjunct added to an unrelated guard is a hypothetical future edit, which is
#  COVERAGE DEBT to state, not a floor breach to repair.  Stating it is what
#  makes a later escape "outside the contract" rather than an argument. ***
#
#  The seat's own summary is the honest one: the two-row SHAPE is right and the
#  ORACLE is the weak point -- no arrangement of string-count rows closes this.
#  Closing it needs a channel that observes WHICH PRIMITIVE RAN rather than a
#  diagnostic that happens to sit in one arm.
#
#  AND ONE DEPENDENCY, because the same seat asked whether `n25 line' could go
#  green for a reason other than the one it claims: it could, if a SECOND site
#  emitted the same string for LINE-shaped ops.  Measured today --
#  `grep -c "XFER_EN for LINE op"` over the device source returns ONE.  That is a
#  layout fact, not an invariant: a future duplicate of that diagnostic silently
#  unpins this row, in the same way a struct reorder can unpin an anchored row.


# ------------------------------------------------------------------ summary
#  *** A DELIBERATE NO-ROW MUST NOT RENDER THE SAME AS AN UNRUN ONE, and a review
#  seat pointed out that a CONTRACT COMMENT does exactly that: nothing appears in
#  the OUTPUT either way.  So the exclusions are PRINTED -- as notes, not as rows.
#  They are deliberately NOT rows: a row that can never fail is the vacuity this
#  file exists to refuse, and printing a note keeps the record visible in every run
#  without pretending a test happened. ***
print("NOROW  the drawing itself                       -- a declined op draws nothing"
      " and no row asserts what a correct POINT or TRIANGLE would render")

bad = [n for n, ok in rows if not ok]
print("OPUS500_RESULT=%d/%d" % (len(rows) - len(bad), len(rows)))
print("OPUS500_LABEL=%s" % LABEL)
if bad:
    print("OPUS500_RED=%s" % ",".join(bad))
print("OPUS500_DONE")
