#!/usr/bin/env python3
#
#  #499 sgireunmapped -- the detector.
#
#  DEVICE_ACCESS(sgi_re)'s final catch-all -- every offset in the 4 KB window
#  matching none of the six address arms -- used to end the host process.  This
#  round declines the access and announces it once per direction.  These rows
#  pin the decline, its two latch bits, and the ACCEPT side of all six arms,
#  which the removed exit(1) used to police by accident.
#
#  CONTRACT (vacuity-floor clause (e)) -- which edits this detector is designed
#  to catch, and which it is NOT:
#
#    CATCHES
#      * reinstatement of the catch-all host kill, in EITHER direction
#        (`wr surv', `rd surv', and the `wr kill'/`rd kill' text rows).  Both
#        directions are pinned because a repair qualified to writes only is the
#        commonest partial: MEASURED at 11/14 on the artifact detector's
#        `mwonly' variant;
#      * a decline that returns `return 0', which cpus/memory_rw.c coerces to
#        -1 and raises a guest EXCEPTION_DBE.  `rd sent' presets the
#        destination register to a SENTINEL, so "the tail ran and wrote
#        odata (0)" and "the load never completed" are distinguishable, and
#        `rd nodbe' reads the exception channel directly.  A survival-only
#        oracle at a refusal-effect site is vacuous by construction;
#      * loss of either latch, so the decline floods (`wr lat1', `rd lat1'
#        COUNT over two DIFFERENT offsets; presence would pass an unlatched
#        build, and one offset twice would pass a per-address latch);
#      * the two new bits COLLIDING with any of the seven that already exist.
#        `xwin wr'/`xwin rd' walk all six #497 window latches AND sgi_de's
#        #498 latch first, then take the catch-all: if a new bit is any of
#        those seven, the announcement is silently suppressed.  MEASURED --
#        the `fix6' variant, in which SGIRE_W_UNMAP_WR reuses 1 << 6 and so
#        collides with #498's SGIRE_W_DE_LEN, escapes every other row here.
#        The four sgi_re handlers share one malloc'd struct, so this is a
#        cross-DEVICE collision, not merely a cross-window one, and a row
#        walking only sgi_re's own windows would not have seen it;
#      * the two new bits colliding with EACH OTHER (`wr rd 2msg'): one shared
#        bit for both directions silences whichever comes second;
#      * SHRINKING any window's FAR bound (the `acc hi' rows sit at each
#        window's LAST legal 8-byte slot).  MEASURED at 13/14 each for TLB_A,
#        TLB_B and TLB_C on the artifact detector;
#      * GROWING any window's NEAR bound, and TRANSLATING a whole window.
#        *** THIS IS THE HALF THE FIRST DRAFT DID NOT HAVE, AND IT WAS
#        MEASURED MISSING RATHER THAN REASONED ABOUT. ***  A one-token edit --
#        `>= CRIME_RE_LINEAR_A' to `>= CRIME_RE_LINEAR_A + 0x40' -- swept the
#        14-row artifact detector CLEAN, because every accept row sat at its
#        window's TOP slot, and a top-slot row tests the FAR bound and NEVER
#        the near one.  A base-slot row has the mirrored blindness.  Both
#        halves ship, per window;
#      * MIS-ATTRIBUTION of an offset to the wrong arm, and re-mapping of a
#        window's index arithmetic.  Every `acc' row matches the arm's own
#        debug() text INCLUDING THE ARRAY NAME, THE INDEX AND THE VALUE --
#        e.g. "d->re_tlb_a[252] = 0x1122" -- so it is anchored to a SPECIFIC
#        CELL by a channel outside the decode under test, which is clause
#        (f)'s requirement.  A "did not reach the catch-all" oracle cannot do
#        this: it is satisfied by ANY arm servicing the access.
#      * *** THE CATCH-ALL'S OWN STATE SPACE, ENUMERATED RATHER THAN PATCHED.
#        Added by #499 pass 4 after THREE consecutive passes each found a breach
#        of ONE class -- a cell of this space left empty, repaired at exactly the
#        address the mutant had used, leaving the symmetric cell open for the
#        next pass.  Two of the three were MEASURED CLEAN SWEEPS of a detector
#        that had just come back green. ***
#
#        The catch-all's behaviour is a function of FIVE inputs, so they are
#        listed and each is given a row that varies under a named mutant:
#
#          relative_addr  component 1 (0x16e0-0x16ff) and component 2 (0x1800+),
#                         AND POSITION WITHIN a component.  Component 1 is a
#                         32-byte RANGE, not a point: `>= CRIME_RE_LINEAR_A'
#                         changed to `- 0x10' swept 36 rows CLEAN because all
#                         four component-1 rows sat at the BASE.  `cliphi rd/wr'
#                         sit at its LAST 8-byte slot (0x16f8);
#          writeflag      `else if (relative_addr < CRIME_RE_LINEAR_A)' on the
#                         READ arm also swept 36 rows clean -- component 1 was
#                         probed by two sessions and BOTH were stores.
#                         `clip rd *' and `cliphi rd *' close it;
#          len            8 vs narrow, now at both components (`clip rdn *');
#          idata          every write carried a NONZERO datum, so
#                         `writeflag == MEM_WRITE && idata' had no disagreeing
#                         row.  `wr zero surv'/`wr zero decl' supply one;
#          d->warned      latch state at entry -- the `lat1' rows.
#
#        NOT COVERED IN THIS SPACE, deliberately and stated so a later escape is
#        "outside the contract" rather than an argument about overclaiming:
#          - component 1's LAST slot at NARROW width (the len axis is pinned at
#            the base of both components and at neither far edge);
#          - component 2's FAR edge.  It is bounded by DEV_SGI_RE_LENGTH rather
#            than by a constant in this file, so the one-token shrink that works
#            on component 1 has no analogue here;
#          - a zero datum on the READ side (a read carries none) or at
#            component 1.
#
#    DOES NOT CATCH
#      * a collision among the SIX #497 window bits.  That is
#        sgi_re_width_probe.py's `xsite 6msg' row, which is shipped and
#        gate-wired, and which MEASURED 32/35 against the 1<<0 -> 1<<1 mutant
#        built for this round.  Duplicating it here would add a row that can
#        never fail alone;
#      * the six `TODO: read from <sym>' kills, or sgi_de's drawing-op kill.
#        Those are sgirekills and sgideprimop, deliberately untouched;
#      * a change to the announcement's WORDING beyond the literals below;
#      * anything in sgi_mte, or in sgi_de_status beyond the signature control.
#
#  *** THE ROW SET IS NOT INVENTED HERE.  Every row's mutant was built and
#  scored before this file existed; the table, the variant diffs and the
#  session transcripts are preserved under
#  regress/artifacts/sgireunmapped/killtable_20260831/. ***
#
import os
import pty
import re
import select
import sys
import time

BIN = sys.argv[1] if len(sys.argv) > 1 else "build/gxemul"
LABEL = sys.argv[2] if len(sys.argv) > 2 else "local"

#  A load file is REQUIRED by -V ... 0x80001000:<file>, and this probe must not
#  depend on a file sitting in an artifacts directory.  Same fallback as
#  sgi_de_width_probe.py: the in-tree fixture if it exists, /dev/null if not.
#  /dev/null is the live path today -- regress/dummy_kernel.bin is absent --
#  and the guest never executes the loaded bytes anyway: every instruction this
#  probe runs is written into RAM with `put w'.
DUMMY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dummy_kernel.bin")
if not os.path.exists(DUMMY):
    DUMMY = "/dev/null"

CODE        = 0x80001000
SCRATCH_RAM = 0xa0001800
LIVE_VAL    = 0x12345678
RE          = 0xb5001000          # sgi_re        @ phys 0x15001000
DE          = 0xb5002000          # sgi_de        @ phys 0x15002000
DE_STATUS   = 0xb5004000          # sgi_de_status @ phys 0x15004000
DE_STAT_VAL = "0x1e000000"

#  Offsets past LINEAR_B's far bound, i.e. in the catch-all.  The latch rows
#  use TWO DIFFERENT ones: one offset twice would pass a build that latched
#  per-address instead of per-device.
UNMAP_W  = 0x800
UNMAP_W2 = 0x8c0
UNMAP_R  = 0x900
UNMAP_R2 = 0x9c0

ACC_VAL  = "0x1122334455667788"
SENTINEL = 0xdeadbeef


#  THE FULL LITERAL, WITH OUR OWN DATUM IN IT, IS THE POINT.
#  A hand-assembled encoding with a wrong register field stores 0, and a row
#  matching only "unimplemented write to address" would accept that.  Matching
#  the echoed value makes the row un-fakeable the same way `devsig' is.
#  The kill literal is NOT a substring of the decline literal -- the character
#  after the datum is ' ]' in one and ' -' in the other -- so the two are
#  mutually exclusive rather than merely different.
def wr_decl(off, val=ACC_VAL):
    #  #499 pass 4: `val' was hardcoded to ACC_VAL, so every row whose store used
    #  a different datum -- the narrow rows, the zero-datum row -- had to fall back
    #  to the bare substring "unimplemented write to address", which is ALSO a
    #  prefix of the KILL text.  That abandons the mutual exclusivity the comment
    #  above goes to trouble to establish.  Parameterised, those rows get the full
    #  literal for free.
    return ("unimplemented write to address 0x1%03x, data=%s -- declined."
            "  (once) ]" % (off, val))


def datum(val):
    """the 16-hex-digit form the device prints for a t0 value of `val'"""
    return "0x%016x" % int(val, 16)


def wr_kill(off):
    return "unimplemented write to address 0x1%03x, data=%s ]" % (off, ACC_VAL)


def rd_decl(off):
    return "unimplemented read from address 0x1%03x -- declined.  (once) ]" % off


def rd_kill(off):
    return "unimplemented read from address 0x1%03x ]" % off


#  The six #497 width latches and #498's sgi_de latch -- the SEVEN bits the two
#  new ones must not collide with.  Offsets are the window bases minus the
#  handler's own `relative_addr += 0x1000'.
PARTNERS = [
    (RE + 0x000, "for CRIME_RE_TLB_A -- declined."),
    (RE + 0x200, "for CRIME_RE_TLB_B -- declined."),
    (RE + 0x400, "for CRIME_RE_TLB_C -- declined."),
    (RE + 0x600, "for CRIME_RE_TEX -- declined."),
    (RE + 0x700, "for CRIME_RE_LINEAR_A -- declined."),
    (RE + 0x780, "for CRIME_RE_LINEAR_B -- declined."),
    (DE + 0x0d0, "sgi_de: unimplemented len=1 -- declined."),
]

#  name   base   last 8-byte slot,  anchored text at base,  anchored text at last slot
WINDOWS = [
    ("tlba", 0x000, 0x1f8,
     "d->re_tlb_a[0] = 0x1122", "d->re_tlb_a[252] = 0x1122"),
    ("tlbb", 0x200, 0x3f8,
     "d->re_tlb_b[0] = 0x1122", "d->re_tlb_b[252] = 0x1122"),
    ("tlbc", 0x400, 0x5f8,
     "d->re_tlb_c[0] = 0x1122", "d->re_tlb_c[252] = 0x1122"),
    ("tex", 0x600, 0x6d8,
     "d->re_tex[0] = 0x1122", "d->re_tex[27] = 0x1122"),
    ("lina", 0x700, 0x778,
     "[ d->re_linear_a[0] = 0x11223344, [1] = 0x55667788 ]",
     "[ d->re_linear_a[30] = 0x11223344, [31] = 0x55667788 ]"),
    ("linb", 0x780, 0x7f8,
     "[ d->re_linear_b[0] = 0x11223344, [1] = 0x55667788 ]",
     "[ d->re_linear_b[30] = 0x11223344, [31] = 0x55667788 ]"),
]

OP_NOP      = 0x00000000
OP_B_SELF   = 0x1000ffff
OP_SB_T0_A3 = 0xa0e80000          # sb   $t0, 0($a3)
OP_SW_T0_A3 = 0xace80000          # sw   $t0, 0($a3)
OP_SD_T0_A3 = 0xfce80000          # sd   $t0, 0($a3)
OP_LW_V0_AT = 0x8c220000          # lw   $v0, 0($at)
OP_LD_V0_AT = 0xdc220000          # ld   $v0, 0($at)

rows = []


def row(name, got, want, note=""):
    #  THE NAME COLUMN IS %-16s AND THE GATE'S PER-ROW PATTERN IS "^<name>  .*ok$"
    #  -- TWO literal spaces.  A name of length L is followed by (16 - L) pad
    #  characters plus the format's own space, so L must be <= 15 or the row emits
    #  ONE space, the gate's check becomes UNSATISFIABLE (got=0 against want=1),
    #  and the gate goes RED on a GREEN probe.
    #
    #  #499's pass 3 shipped exactly two 16-char rows and the failure was found by
    #  a review seat rather than by the gate -- because the gate SCRIPT was never
    #  run after they were added, only the probe.  Both were renamed to 13 chars.
    #  This assert designs the trap out instead of asking the next author to
    #  remember it.  Note the trap has an opposite form too: a name that is a
    #  PREFIX of another matches two rows.
    assert len(name) <= 15, (
        "row name %r is %d chars; the gate pattern needs <= 15" % (name, len(name)))
    ok = (got == want)
    rows.append((name, ok))
    print("%-16s %-14s %-14s %-48s %s" % (name, str(got), str(want), note,
                                          "ok" if ok else "FAIL"))
    return ok


def session(cmds, settle=1.5, spin=1.2):
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

    *** THIS IS THE STRUCTURAL FORM OF A DEFECT THAT COST THE ARTIFACT
    DETECTOR A ROW. ***  The gxprobe-based original cached register
    assignments and skipped redundant ones; `step' advances pc, so a second
    sequence written to the SAME address found pc already "set" there, the
    assignment was skipped, and the guest executed the following nop instead
    of the store.  Its `msg once' row then performed ONE access and two nops
    and therefore COULD NOT FAIL -- a mutant that announced without ever
    latching scored a clean sweep because of it.

    This file writes raw debugger commands with no cache, so an assignment can
    never be skipped; handing out a distinct address per sequence additionally
    keeps one sequence's dyntrans translation from being reached by the next.
    The hazard is designed out rather than remembered.
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


def store(A, addr, op=OP_SD_T0_A3, val=ACC_VAL):
    return ["a3=0x%x" % addr, "t0=%s" % val] + run_ops([op], A.take(1))


def load(A, addr, op=OP_LD_V0_AT):
    #  Preset to a SENTINEL, never to 0: preset to 0 a row cannot tell "the
    #  common tail ran and wrote odata (0)" from "the load never completed".
    return ["at=0x%x" % addr, "v0=0x%x" % SENTINEL] + run_ops([op], A.take(1))


print("#499 sgireunmapped DETECTOR -- binary=%s label=%s" % (BIN, LABEL))
print("%-16s %-14s %-14s %-48s %s" % ("row", "got", "want", "note", ""))

# ---------------------------------------------------------------- controls (c)
A = Addr(CODE)
t, alive, how = session(store(A, SCRATCH_RAM, OP_SW_T0_A3, "0x%x" % LIVE_VAL)
                        + load(A, SCRATCH_RAM, OP_LW_V0_AT) + ["print v0"])
row("live", printed(t, "v0") if alive else "died", "0x%x" % LIVE_VAL,
    "LIVENESS: guest store then load, through RAM")

A = Addr(CODE)
t, alive, how = session(load(A, DE_STATUS, OP_LW_V0_AT) + ["print v0"])
row("devsig", printed(t, "v0") if alive else "died", DE_STAT_VAL,
    "DEVSIG: CRIME_DE_STATUS reads 0x1e000000; RAM would read 0")

print("OPUS499T_CONTROL=%s" % ("OK" if all(o for _, o in rows) else "DEAD"))
print("")

# ------------------------------------------------- the catch-all, WRITE side
A = Addr(CODE)
t, alive, how = session(store(A, RE + UNMAP_W))
row("wr surv", how, "exit0", "unmapped WRITE: host survives")
row("wr kill", t.count(wr_kill(UNMAP_W)), 0, "the pre-fix host kill text is gone")
row("wr decl", t.count(wr_decl(UNMAP_W)), 1,
    "the decline is announced, echoing OUR datum")

# ------------------------------------------------- the catch-all, READ side
#  NOT redundant with the write rows: a repair qualified to writes only leaves
#  this half dead.  MEASURED 11/14 on the artifact detector's `mwonly'.
A = Addr(CODE)
t, alive, how = session(load(A, RE + UNMAP_R) + ["print v0"])
row("rd surv", how, "exit0", "unmapped READ: host survives")
row("rd kill", t.count(rd_kill(UNMAP_R)), 0, "the pre-fix read kill text is gone")
row("rd decl", t.count(rd_decl(UNMAP_R)), 1, "the read decline is announced")
row("rd sent", printed(t, "v0") if alive else "died", "0x0",
    "declined READ reaches the tail and returns a DEFINED 0, not the sentinel")

A = Addr(CODE)
t, alive, how = session(load(A, RE + UNMAP_R) + ["print v0"])
row("rd nodbe", ("exception" in t.lower()) or ("DBE" in t), False,
    "a decline is not a guest bus error -- kills `return 0'")

# ----------------------------------- L2 REPAIR: the WIDTH axis, and the FIRST component
#  *** ADDED 2026-08-31 AFTER THE PASS-2 SEAT MEASURED TWO MUTANTS SWEEPING ALL 28 ROWS
#  CLEAN, ONE OF THEM A VERBATIM REINSTATEMENT OF THE REMOVED KILL. ***
#
#  The 28 rows above pin the DIRECTION axis exhaustively -- write, read, per-direction
#  latches, the sentinel, the DBE -- and never touch the WIDTH axis at the catch-all,
#  because store() defaults to OP_SD and load() to OP_LD.  Every catch-all row was len 8.
#  The round's HEADLINE is `no width predicate at all' and its WITNESS is a `lb', so the
#  one axis the fix is about was the one axis the detector could not see.  Mutant `W' --
#  re-adding the pre-#499 `len != 8' kill, lifted verbatim from 9f666a8^ -- scored 28/28
#  while `sb' and `lb' at 0xb5001800 died with the pre-fix text.  Floor clause (b).
#
#  Second blindness, same cause one level up: the catch-all has TWO disjoint components,
#  0x16e0-0x16ff (32 bytes, and it is CRIME_RE_CLIP_IDS -- a NAMED register block the
#  model has not implemented, not anonymous space) and 0x1800-0x1fff (2048).  All four
#  UNMAP_* offsets are 0x800/0x8c0/0x900/0x9c0 -- the second component.  THE 32-BYTE
#  COMPONENT HAD ZERO ROWS, so `T' (CRIME_RE_TEX + 0xe0 -> + 0x100, one hex digit) handed
#  it back to exit(1) and scored 28/28.  Clause (d): a bound relaxed on a dominating
#  predicate.
A = Addr(CODE)
t, alive, how = session(store(A, RE + UNMAP_W, op=OP_SB_T0_A3, val="0x5a"))
row("wr narrow surv", how, "exit0",
    "a BYTE write to the catch-all survives -- kills a re-added len guard")
row("wr narrow decl", t.count(wr_decl(UNMAP_W, datum("0x5a"))), 1,
    "...and is announced: the decline is width-agnostic, as the fix claims")

A = Addr(CODE)
t, alive, how = session(load(A, RE + UNMAP_R, op=OP_LW_V0_AT) + ["print v0"])
row("rd narrow surv", how, "exit0",
    "a 4-byte READ of the catch-all survives -- the witness width, not just len 8")
row("rd narrow sent", printed(t, "v0") if alive else "died", "0x0",
    "...and still lands a DEFINED 0 rather than the sentinel")

#  CLIP_IDS: the FIRST component.  0x6e0 + the handler's own +0x1000 = 0x16e0.
A = Addr(CODE)
t, alive, how = session(store(A, RE + 0x6e0))
row("clip surv", how, "exit0",
    "comp1 base, len8, WRITE survives (killed by the pre-fix build)")
row("clip decl", t.count(wr_decl(0x6e0)), 1,
    "...and is announced, so the component is covered rather than merely alive")

#  *** AND THE SAME AXIS AGAIN, ONE LEVEL DOWN.  Added 2026-08-31 after two packet-fed
#  seats read the repair above and pointed out that its own claim -- `the WIDTH axis is
#  pinned' -- covers only TWO CELLS of a two-by-two.  The rows above pin
#  component2-x-narrow and component2-x-len8 and component1-x-len8; component1 was left
#  at store()'s default OP_SD, so COMPONENT-1-x-NARROW had nothing.
#
#  That is the ORIGINAL breach reproduced inside its own repair: I diagnosed `one axis
#  pinned exhaustively, the other not at all', fixed it at the address the mutants used,
#  and left the identical hole at the other component.  A guard re-added at the catch-all
#  would be caught here; a guard re-added and CONDITIONED on the first component would
#  not have been.
A = Addr(CODE)
t, alive, how = session(store(A, RE + 0x6e0, op=OP_SB_T0_A3, val="0x5a"))
row("clip nar surv", how, "exit0",
    "a BYTE write to the FIRST component survives -- closes the width x component matrix")
row("clip nar decl", t.count(wr_decl(0x6e0, datum("0x5a"))), 1,
    "...and is announced: neither component nor width is a special case")

#  ==================================================================== #499 pass 4
#  THE STATE-SPACE ENUMERATION.  Written because THREE CONSECUTIVE PASSES found a
#  breach of the SAME CLASS -- a cell of this space left empty, repaired at exactly
#  the address the mutant used, leaving the symmetric cell open for the next pass:
#
#      pass 1  "width unpinned"                 -> repaired at component 2 only
#      pass 2  "component unpinned"             -> repaired on the WRITE side only
#      pass 3  "direction AND position unpinned"
#
#  A fourth patch at the corner pass 3 named would have produced a fifth pass.  So
#  the catch-all's inputs are enumerated ONCE, from the function signature, and the
#  cells are closed together.  The CONTRACT below states which are covered and which
#  are deliberately not -- a later escape is then "outside the contract, as stated"
#  or "a breach of it", which are different dispositions.
#
#  THE FIVE INPUTS the catch-all's behaviour is a function of:
#
#      relative_addr  which component (1 = 0x16e0-0x16ff, 2 = 0x1800-0x1fff)
#                     AND where within it -- BASE vs LAST 8-byte slot.  Position is
#                     a real axis: component 1 is a 32-byte RANGE, not a point, and
#                     `>= CRIME_RE_LINEAR_A - 0x10' swept a 36-row detector CLEAN
#                     because all four comp1 rows sat at the base.  That is the
#                     carrier's own accept-row rule -- an accept row at a window's
#                     BASE tests the near bound twice and the far bound never --
#                     applied to the six named windows and NOT to this one.
#      writeflag      read vs write.  `else if (relative_addr < CRIME_RE_LINEAR_A)'
#                     on the READ arm also swept 36 rows clean: comp1 was probed by
#                     two sessions and BOTH were stores.
#      len            8 vs narrow.
#      idata          the datum.  Every comp1/comp2 write here carried a NONZERO
#                     value, so `writeflag == MEM_WRITE && idata' had no disagreeing
#                     row -- the guard-field/body-field check's own shape.
#      d->warned      latch state at entry (the `lat1' rows).
#
#  COVERED, and each row names the mutant it kills and the channel that differs:
A = Addr(CODE)
t, alive, how = session(load(A, RE + 0x6e0) + ["print v0"])
row("clip rd surv", how, "exit0",
    "comp1 base, len8, READ survives -- kills a read-arm kill qualified to comp2")
row("clip rd decl", t.count(rd_decl(0x6e0)), 1,
    "...and is announced with the FULL literal, so a kill cannot satisfy it")
row("clip rd sent", printed(t, "v0") if alive else "died", "0x0",
    "...and lands a DEFINED 0, so the common tail ran")

A = Addr(CODE)
t, alive, how = session(load(A, RE + 0x6e0, op=OP_LW_V0_AT) + ["print v0"])
row("clip rdn surv", how, "exit0",
    "comp1 base, NARROW read: the last empty cell of component 1")
row("clip rdn decl", t.count(rd_decl(0x6e0)), 1,
    "...and is announced")

#  THE FAR EDGE.  0x6f8 is component 1's LAST 8-byte slot (0x16f8; the component
#  ends at CRIME_RE_LINEAR_A = 0x1700).  A read here kills BOTH measured sweeps at
#  once: under a comp2-qualified read kill it reaches CLIP_IDS, and under a widened
#  LINEAR_A near bound it reaches LINEAR_A.
A = Addr(CODE)
t, alive, how = session(load(A, RE + 0x6f8) + ["print v0"])
row("cliphi rd surv", how, "exit0",
    "comp1 LAST slot, READ survives -- the far bound, which no base row can see")
row("cliphi rd decl", t.count(rd_decl(0x6f8)), 1,
    "...and is announced from the far slot, not merely from the base")

A = Addr(CODE)
t, alive, how = session(store(A, RE + 0x6f8))
row("cliphi wr surv", how, "exit0",
    "comp1 LAST slot, WRITE survives")
row("cliphi wr decl", t.count(wr_decl(0x6f8)), 1,
    "...and is announced: a window swallowing the top half goes SILENT here")

#  SIBLING PARITY: comp2's narrow WRITE has an announce channel and its narrow READ
#  had only surv+sent, so a len-conditioned suppression of the read announce alone
#  escaped every row.
A = Addr(CODE)
t, alive, how = session(load(A, RE + UNMAP_R, op=OP_LW_V0_AT) + ["print v0"])
row("rd narrow decl", t.count(rd_decl(UNMAP_R)), 1,
    "comp2 narrow READ is announced, not merely survived")

#  THE VALUE AXIS.  The guard reads writeflag; the guarded body reads relative_addr
#  AND idata.  With every other write carrying a nonzero datum, `&& idata' would
#  reroute a zero-datum write into the READ arm and no row would disagree.
A = Addr(CODE)
t, alive, how = session(store(A, RE + UNMAP_W, val="0x0"))
row("wr zero surv", how, "exit0",
    "a ZERO-datum write survives")
row("wr zero decl", t.count(wr_decl(UNMAP_W, datum("0x0"))), 1,
    "...and is announced AS A WRITE -- kills `writeflag == MEM_WRITE && idata'")

#  ==================================================== #499 pass 4, L2 REPAIR
#  *** MEASURED FLOOR BREACH, clause (d): the guard kept, its repair removed. ***
#
#  Mutant E0W -- the catch-all's WRITE arm announces and then `exit(0)' -- scored
#  a CLEAN SWEEP of the 48-row detector.  Measured, not reasoned:
#
#      E0   exit(0) after the whole catch-all, BOTH directions   47/48
#      E0W  exit(0) in the WRITE arm only                        48/48  TOTAL ESCAPE
#
#  WHY EVERY EXISTING WRITE ROW IS BLIND TO IT, and it is by construction:
#    * a `surv' row wants "exit0", and a clean `exit(0)' IS exit status 0, so the
#      oracle is SATISFIED by the very thing it should catch;
#    * a `decl' row counts the message, which was already printed before the exit.
#  The two together therefore pass.  That is the `exit0oracle' class, and this is
#  its first MEASURED instance rather than a predicted one -- #500's own pre-table
#  block had named the shape (`EXIT STATUS CANNOT VARY between declined-and-quit
#  and died-with-status-0') at a different site, without building it.
#
#  E0 is caught by exactly ONE row, `wr rd 2msg', and only INCIDENTALLY: that row
#  performs two accesses, so it notices the second one never happening.  A single-
#  access write row cannot see this at all.
#
#  THE REPAIR IS A POST-STORE POSITIVE OBSERVABLE, which is what the READ side
#  already had (`rd sent' reads "absent" when the host is gone) and the WRITE side
#  had nowhere.  Each row below seeds RAM, performs the declined device write, then
#  reads the seed back: if the host quit at the write, the load never runs and
#  printed() returns "absent", which is not the datum.
#
#  BOTH COMPONENTS, deliberately.  E0W as built edits the shared write arm, so one
#  row would kill it -- but a write-side exit(0) CONDITIONED on one component is the
#  same asymmetry this round has now been bitten by three times, and the second row
#  costs one session.
A = Addr(CODE)
t, alive, how = session(store(A, SCRATCH_RAM)
                        + store(A, RE + UNMAP_W)
                        + load(A, SCRATCH_RAM) + ["print v0"])
row("wr then live", printed(t, "v0") if alive else "died", ACC_VAL,
    "comp2: the guest RUNS ON after a declined write -- kills announce-then-exit(0)")

A = Addr(CODE)
t, alive, how = session(store(A, SCRATCH_RAM)
                        + store(A, RE + 0x6e0)
                        + load(A, SCRATCH_RAM) + ["print v0"])
row("clip wr live", printed(t, "v0") if alive else "died", ACC_VAL,
    "comp1: same, so a component-conditioned exit(0) cannot hide either")

# ------------------------------------------------- the two latches
A = Addr(CODE)
t, alive, how = session(store(A, RE + UNMAP_W) + store(A, RE + UNMAP_W2))
row("wr lat1", t.count("unimplemented write to address"), 1,
    "(once): COUNT over TWO different offsets, not presence")

A = Addr(CODE)
t, alive, how = session(load(A, RE + UNMAP_R) + load(A, RE + UNMAP_R2))
row("rd lat1", t.count("unimplemented read from address"), 1,
    "(once) on the read side too -- its own bit, its own count")

#  ONE BIT FOR BOTH DIRECTIONS silences whichever comes second.
A = Addr(CODE)
t, alive, how = session(store(A, RE + UNMAP_W) + load(A, RE + UNMAP_R), spin=1.4)
row("wr rd 2msg", t.count(wr_decl(UNMAP_W)) + t.count(rd_decl(UNMAP_R)), 2,
    "write and read declines are SEPARATE bits")


# ------------------------------------------------- the new bits vs the old seven
#  *** THE COLLISION ROW, AND ITS PARTNER SET IS THE WHOLE POINT. ***  Reusing
#  any pre-existing bit makes the catch-all announcement vanish once that
#  partner has fired.  All six #497 window latches AND #498's sgi_de latch are
#  walked first, in ONE session, because the four handlers share one malloc'd
#  struct: the measured escape (`fix6') collided with sgi_de's bit, one device
#  over.
def collide_session(final, spin=2.2):
    A = Addr(CODE)
    cmds = []
    for addr, _lit in PARTNERS:
        cmds += store(A, addr, OP_SB_T0_A3, "0x5a")
    cmds += final(A)
    return session(cmds, spin=spin)


t, alive, how = collide_session(lambda A: store(A, RE + UNMAP_W))
row("xwin7 pre", sum(1 for _a, lit in PARTNERS if t.count(lit) == 1), 7,
    "CONTROL: all seven pre-existing latches fired")
row("xwin wr", t.count(wr_decl(UNMAP_W)), 1,
    "SGIRE_W_UNMAP_WR is none of those seven bits")

t, alive, how = collide_session(lambda A: load(A, RE + UNMAP_R))
row("xwin rd", t.count(rd_decl(UNMAP_R)), 1,
    "SGIRE_W_UNMAP_RD is none of those seven bits either")

# ------------------------------------------------- ACCEPT, anchored, BOTH bounds
#  De-escalation clause: the removed exit(1) was an ACCIDENTAL tripwire that
#  announced any window-bound edit on the first legal access.  These rows are
#  part of the FIX'S COST, not future strengthening.
#
#  TWO rows per window, and the pair is not redundant:
#    `acc lo' at the window BASE       pins the NEAR bound
#    `acc hi' at its LAST 8-byte slot  pins the FAR  bound
#  A suite with only one of them is blind to the other by construction, which
#  was MEASURED, not argued -- see the contract above.
for nm, lo, hi, lotext, hitext in WINDOWS:
    A = Addr(CODE)
    t, alive, how = session(store(A, RE + lo))
    row(nm + " acc lo", "1" if lotext in t else "0", "1",
        "NEAR bound: base slot, anchored to its own cell")

    A = Addr(CODE)
    t, alive, how = session(store(A, RE + hi))
    row(nm + " acc hi", "1" if hitext in t else "0", "1",
        "FAR bound: last legal slot, anchored to its own cell")

n_ok = sum(1 for _, ok in rows if ok)
print("")
print("OPUS499T_RESULT=%d/%d" % (n_ok, len(rows)))
print("OPUS499T_LABEL=%s" % LABEL)
print("OPUS499T_DONE")
