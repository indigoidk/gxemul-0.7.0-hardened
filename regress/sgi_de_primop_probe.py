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
    * *** A WIDENED SWITCH MASK.  `op & 0xff000000' -> `& 0xffff0000' swept an
      earlier 19-row version of this file CLEAN, because both accept rows stored
      0x03000000 and said nothing about the mask's WIDTH.  `acc rect rl' and
      `acc line se' now carry real bits in 16-19 (DE_PRIM_RL, LINE_SKIP_END),
      which the code READS, so a widened mask declines a legal primitive and the
      rows red. ***
    * a repair applied to the WRITE direction only (`rd surv', `rd decl') --
      `if (startFlag)' is not conditioned on MEM_WRITE, so a START-aliased READ
      draws too.  Named by a seat; no row covered it before.

  DOES NOT CATCH
    * the [31:26] stray-bit case -- a legal LINE with a high bit set also lands
      in `default:'.  *** DELIBERATELY NO ROW, WITH ITS REASON: whether a guest
      ever sets those bits is not established, so a row would assert a
      reachability nobody has shown.  A deliberate no-row must not render the
      same as an unrun one. ***
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
DE_STATUS = 0xffffffffb5003000       # sgi_de_status, for the device signature

#  0x060 is CRIME_DE_PRIMITIVE; 0x800 is the START alias.  A single access to
#  0x860 therefore SETS the op and TRIGGERS the draw -- which is why the round's
#  first witness was confounded: a START-aliased WRITE also writes the register,
#  so the trigger value BECOMES op.  That is a feature here, not a hazard: it is
#  exactly how a guest reaches draw_primitive in one instruction.
PRIM_START = 0x860
PRIM_ONLY = 0x060
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

A = Addr(CODE)
t, alive, how = session(load(A, DE_STATUS + 0x0, op=OP_LBU_V0_AT) + ["print v0"])
row("devsig", "yes" if alive and printed(t, "v0") != "absent" else "no", "yes",
    "a DEVICE answers, not RAM -- the address really reaches sgi_de_status")

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
A = Addr(CODE)
t, alive, how = session(store(A, DE + PRIM_START, val="0x03010000")
                        + load(A, 0xffffffff80002000) + ["print v0"])
row("acc rect rl", t.count(DRAW), 0,
    "RECTANGLE|RL is implemented too -- kills a WIDENED op mask")

A = Addr(CODE)
t, alive, how = session(store(A, DE + PRIM_START, val="0x01040000")
                        + load(A, 0xffffffff80002000) + ["print v0"])
row("acc line se", t.count(DRAW), 0,
    "LINE|SKIP_END likewise -- the mask's WIDTH is now pinned, not just its value")

# ------------------------------------------------------------------ summary
bad = [n for n, ok in rows if not ok]
print("OPUS500_RESULT=%d/%d" % (len(rows) - len(bad), len(rows)))
print("OPUS500_LABEL=%s" % LABEL)
if bad:
    print("OPUS500_RED=%s" % ",".join(bad))
print("OPUS500_DONE")
