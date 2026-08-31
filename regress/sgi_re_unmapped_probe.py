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
def wr_decl(off):
    return ("unimplemented write to address 0x1%03x, data=%s -- declined."
            "  (once) ]" % (off, ACC_VAL))


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
row("wr narrow decl", t.count("unimplemented write to address"), 1,
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
    "the 32-byte first component survives too -- kills a grown TEX far bound")
row("clip decl", t.count("unimplemented write to address"), 1,
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
row("clip narrow surv", how, "exit0",
    "a BYTE write to the FIRST component survives -- closes the width x component matrix")
row("clip narrow decl", t.count("unimplemented write to address"), 1,
    "...and is announced: neither component nor width is a special case")

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
