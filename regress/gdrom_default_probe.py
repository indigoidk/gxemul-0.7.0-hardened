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

*** CONTRACT (vacuity floor clause (e)) -- WHAT THESE ROWS ARE DESIGNED TO
CATCH, WHAT THEY ARE NOT, AND WHAT IS KNOWN TO ESCAPE THEM. ***  A detector
that says so is falsifiable; one claiming completeness is not, and a later
escape then becomes an argument about overclaiming instead of a contract
question with an answer.

SCOPE.  This contract covers the #462 `case 0x18` DMA rows added below.  The
#461 `default:`-arm rows are governed by the census header above; an escape
against one of THOSE is adjudicated there, not here.

DESIGNED TO CATCH -- each backed by a mutant that measurably reddens a row,
not by intent:

  * reinstatement of either `exit(1)`                        (Mb1, Mb2)
  * loss, RELOCATION, CONDITIONING or LATCH-SCOPING of the
    `idata = 0` shadow clear, at either declining arm or at
    the success arm                          (M1, M3, M6, M7, M12)
  * collapse of the two warn-bit latches onto ONE bit (M2), or
    loosening of the ARMING latch into a counter (M4)
  * a completion event SET on a declined transfer            (M8, M9)
  * outward growth of the arming test                        (M10)
  * an operand swap in the no-data guard                     (M11)
    *** #490: THIS CLAIM IS EXPIRED AND THE MEASUREMENT SAYS SO.  M11 IS NOW
    EQUIVALENT -- NO ROW KILLS IT, BECAUSE THERE IS NOTHING LEFT TO KILL. ***
      artifacts/gdromexitsix/m11_rescore_20260828/m11_58row.txt
      (a 58-row measurement: these are the counts AS MEASURED THEN, not today's
       denominator.  The probe has since grown and the gate pin is authoritative;
       rewriting these to match it would falsify the record they exist to preserve.)
        fixed  GDROM_DEF_RESULT=58/58   nodata stale/stale says/stale idle all ok   [58-row denominator, as measured then]
        M11    GDROM_DEF_RESULT=58/58   ... byte-identical   [58-row denominator, as measured then]

    THE CHRONOLOGY, from git rather than memory, because every record here was
    CORRECT WHEN WRITTEN and one of them was overtaken:
      2026-08-25  abf665c  M11 measured DETERMINISTICALLY LETHAL -- five runs, five
                           SIGSEGVs, written out in words rather than as a ratio
                           because an N/N in this docstring is indistinguishable
                           from a stale ROW SCORE against the gate's pin of 58.
                           (The round that first measured it recorded exactly this
                           remedy; I wrote the ratio anyway and section U caught it.)
                           Preceded by
                           `Transfering 408 bytes to 0x00000000` -- a real NULL read.
                           That round recorded, honestly, that A RE-SCORE WAS OWED.
      2026-08-26  4d05cf0  #465 `data and data_len were released apart` -- free_data
                           now clears BOTH.  THE CRASH BECAME IMPOSSIBLE.
      2026-08-28           the owed re-score, finally run: EQUIVALENT.
    `git merge-base --is-ancestor` confirms the fix is NOT an ancestor of the SIGSEGV
    measurement, so the two results do not contradict -- they are one day apart.

    *** THE LESSON IS NOT ABOUT M11.  A KILL RECORD IS TIME-INDEXED EXACTLY AS AN
    ABSENCE RECORD IS. ***  The carrier already requires that an absence record NAME
    ITS WARRANT and that any edit touching that warrant RE-RUNS the death measurement.
    Nothing said the same about a claim that a mutant IS caught -- so #465 edited the
    warrant, the owed re-score was written down the day before, and three rounds ran
    with this contract asserting coverage it no longer had.

    KEPT, NOT DELETED: the mutant is still worth listing.  A future edit that
    re-separates the two fields makes M11 lethal again, and this entry is where a
    reader learns that -- which a deleted line could not do.
  * REFUSAL OR CORRUPTION OF A LEGAL TRANSFER -- legal arming still enters
    the path, the completion still fires, and the device's own TOC byte
    still lands                                              (M5)

*** THE `idata = 0` VERB LIST IS DELIBERATELY WIDE. ***  The mutants do not
merely DELETE that clear: M3 relocates it after the `break`, M6 conditions it
on fresh-device state, M12 scopes it inside the latch.  A contract saying only
"loss" would let a future conditioning escape be argued outside it.

*** AND THE LATCH CLAUSE IS DELIBERATELY NARROW. ***  M4 is anchored on
`GDROM_W_DMAARM`, so only the ARMING latch is measured; NO mutant loosens the
no-data latch alone.  Claiming "either latch" would be an overclaim inside a
contract, which is worse than not writing one.

KNOWN TO ESCAPE -- measured, filed, and named here so a rediscovery can be
adjudicated instead of re-argued:

  * `gdromdmaclear` -- a completion event CLEARED on a decline.  The SET
    direction is caught (M8/M9); the CLEAR direction escapes every row.
  * `gdromdmaguard` -- `count == 1` widened to `count <= 1`, so `(0,1)` is
    accepted.  `arm halfarm` cannot see it.
  * `gdromdmasilent` -- `if (idata != 0)` narrowed to `if (idata == 1)`.

*** THAT LIST IS THE HALF THAT DOES THE ADJUDICATING. ***  Without it, the
next reader to rediscover `gdromdmaclear` cannot tell a FLOOR BREACH (L2, fix
in-round) from FILED COVERAGE DEBT -- which is exactly the distinction clause
(e) exists to make mechanical.

NOT CAUGHT, structurally:

  * *** THE SURVIVAL ROWS DETECT PROCESS TERMINATION ONLY. ***  `arm survive`,
    `nodata live` and `nodata stale` compute `"survived" if alive else "died"`,
    and `alive` is False ONLY when a read raises OSError or returns empty INSIDE
    a budget window -- so they are true of an emulator that is HUNG, one that is
    FROZEN, and, measured, one that has ALREADY BEEN KILLED.

    *** THIS PARAGRAPH SAID "False ONLY on EOF ... true of an emulator that is
    HUNG but has not exited", AND BOTH HALVES ARE MEASURABLY WRONG. ***

      * `rd()` returns False on `except OSError` as well as on EOF, and on Linux
        a pty-master read after the child dies gives EIO -- so the OSError arm is
        the USUAL death path, not an exotic one.  "Only on EOF" mislabels the
        common case.
      * The defect is not on either False path.  It is on the THIRD path: the
        loop is `while time.time() < end:`, so it returns True when the budget
        expires having read nothing.  **A death that lands after the last budget
        check is never read.**  Measured on a rig built from this file's own
        session()/rd(): a process SIGKILLed just before its session's `quit`
        scores `alive == True`.

    So `alive` does not mean "hung but not exited".  It does not even mean
    "not exited".  It means: no EOF and no OSError were observed inside the
    sampled windows.  A red `alive == died` also cannot distinguish a clean exit
    from a pty error.
    Hang-shaped regressions are the IDLE rows' subject, not theirs.

  * The `absent` path is DESIGNED to fire when a readback produces no output
    (e.g. a wedged handler).  It HAS fired once --
    `regress/artifacts/kill462/table3_58rows/probe_M11.raw`, row `stale idle`
    -- and that firing's CAUSE IS UNATTRIBUTED: a hang and a session
    outrunning its spin budget are both consistent with it -- AND SO IS A THIRD
    CAUSE THIS LIST OMITTED, WHICH A CLEAN REBUILD REPRODUCES DETERMINISTICALLY:
    A HOST DEATH THIS PREDICATE MISSED.  The M11 session was re-run five times
    on a tree synced byte-identical to SEC, and EVERY ONE OF THE FIVE gave a SIGSEGV
    -- written out rather than as a ratio, because an `N/N` in a probe docstring
    is indistinguishable from a stale ROW SCORE, and the score-claims gate
    correctly flagged the ratio form against this probe's pin of 58.  Preceded by
    `Transfering 408 bytes to 0x00000000 (guest asked for 0)`.  The shipped
    table3 entry records `survived` for that session.  Detection is proven;
    diagnosis is not claimed -- and the leading diagnosis is now the one the
    original list did not contain.

  * No row observes interrupt ASSERTION.  The completion rows observe the
    SYSASIC pending register, which is a different channel.

Filed for the gaps rather than left implicit: `probetimebased` carries the
liveness predicate's soundness defect and its fix shape (a three-state
predicate -- terminated / responsive / unresponsive), and `lethalonly` carries
the one row whose only kill is lethal.

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
GDROM_CNTLO = 0xa05f7090      # #460's probe drives these to stage a TOC
GDROM_CNTHI = 0xa05f7094
GDROM_COND  = 0xa05f709c
GDROM_DATAP = 0xa05f7080      # ...and the CONTROL window's data port (+0x80)
SYSASIC_PEND = 0xa05f6900     # pending_irq[0], guest-READABLE (dev_dreamcast_asic.c:130)
SYSASIC_DMA_BIT = 0x4000      # SYSASIC_EVENT_GDROM_DMA is 14, so bit 14
DMA_DST_P1 = 0x8c008000       # the accept session's destination, via P1.
#  The session writes 0x0c008000 into +0x04 and the device masks it with
#  0x0fffffff, so physical 0x0c008000 is what the transfer targets.  CODE
#  is 0x8c001000 and the TOC is 408 bytes, so the two never overlap.
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
MOV_L_AT_R1_R3 = 0x6312       # mov.l @r1,r3.  0110nnnnmmmm0010 with n=3 m=1;
#  0x6313 -- which this line first said -- is `mov.l @Rm+,Rn`, a DIFFERENT
#  instruction that also post-increments r1.  Caught by computing the encoding
#  instead of trusting the typing, which is the hand-assembled-encoding trap the
#  carrier records: a wrong field yields a plausible value and no error.  The
#  sibling MOV_L_AT_R1_R2 = 0x6212 (n=2 m=1) is the cross-check.
#  [#556, 2026-10-02 -- a records correction; the text above is kept as it was written] 0x6313 is MOV R1,R3 (low
#  nibble 0011); MOV.L @R1+,R3 is 0x6316 (low nibble 0110).  (hgdromdefaultprobe:F5:
#  regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md)
MOV_L_R2_AT_R1 = 0x2122       # mov.l r2,@r1  (n=1 m=2)
MOV_L_R6_AT_R5 = 0x2562       # mov.l r6,@r5  (0010nnnnmmmm0010, n=5 m=6)
MOV_L_R4_AT_R3 = 0x2342       # mov.l r4,@r3  (0010nnnnmmmm0010, n=3 m=4)
MOV_B_AT_R1_R4 = 0x6410       # mov.b @r1,r4  (0110nnnnmmmm0000, n=4 m=1)
BRA_SELF = 0xaffe
NOP = 0x0009

#  #490: the two decline diagnostics the sibling round added.  ANCHORED on `-- declined`,
#  because the bare `unimplemented data format` also matches the upstream 0x24
#  warn-and-continue line -- measured, not assumed.
FMT_DECL = re.compile(r"unimplemented data format 0x[0-9a-f]+ -- declined")
CMD_DECL = re.compile(r"unimplemented command 0x[0-9a-f]+ -- declined")

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
#  *** #490 L4: THIS SAID "13 or 14" AND 13 IS FINE.  THE LIMIT IS 13. ***
#  The format is `"%-14s %-12s ..."` -- a 14-column field PLUS a literal
#  space -- so the padding and that space add up like this, measured:
#
#      12 chars -> 3 trailing spaces   `^name  ` MATCHES
#      13 chars -> 2 trailing spaces   MATCHES  (the comment denied this)
#      14 chars -> 1 trailing space    UNSATISFIABLE
#
#  Found by the codex seat on #490's pass 1, which also caught that I had
#  copied the wrong bound ("<= 12") out of this comment and into a design
#  brief -- so the error had already propagated once before it was read.
#  The extra character is NOT slack to spend casually: at 13 the margin is
#  exactly the two spaces the gate needs, with nothing left over.
#
#  A row named 14 characters leaves fewer than two spaces and its
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
    #  #490: DEATH-MODE CHANNEL.  `alive` is False only when a read raises OSError or
    #  returns empty inside a budget window, so it is true of a HUNG emulator, a FROZEN
    #  one, and -- measured -- one ALREADY KILLED after the last budget check.  It cannot
    #  tell a clean exit from a signal from a decline.  Round 2 removes two exit(1) sites,
    #  after which every mutant AND the correct decline are alike `exit0`, so a survival
    #  oracle stops discriminating entirely.
    #
    #  Spelling COPIED VERBATIM from gdrom_toclen_probe.py rather than invented: two panel
    #  seats independently said copy the existing oracle, and a third shape would make the
    #  two gdrom probes disagree about what "died" means.
    how = "nostatus"
    try:
        _, stat = os.waitpid(pid, 0)
        if os.WIFSIGNALED(stat):
            how = "sig%d" % os.WTERMSIG(stat)
        elif os.WIFEXITED(stat):
            how = "exit%d" % os.WEXITSTATUS(stat)
    except OSError:
        pass
    return buf, alive, how


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
t, alive, how = session(st(SCRATCH, LIVE) + ld(SCRATCH)
                   + run([MOV_L_R8_AT_R7, MOV_L_AT_R1_R2]) + ["print r2"])
row("live", printed(t, "r2") if alive else "died", "0x%x" % LIVE,
    "RAM: guest store then guest load")

t, alive, how = session(ld(SH4_IPRD) + run([MOV_L_AT_R1_R2]) + ["print r2"])
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
#  [#556, 2026-10-02 -- a records correction; the text above is kept as it was written] which a declined default
#  read (returning 0) cannot satisfy, distinguishing implemented from default.  (hgdromdefaultprobe:F6:
#  regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md)
t, alive, how = session(pair(st(BASE + 0x94, 0x5a) + ld(BASE + 0x94),
                        [MOV_W_R8_AT_R7, MOV_W_AT_R1_R2]) + ["print r2"])
row("impl ok", printed(t, "r2") if alive else "died", "0x5a",
    "CNTHI (+0x94) stores and reads back")

#  #490: `rows and` IS LOAD-BEARING, and its absence was a CHECK THAT CANNOT FAIL.
#  `all([])` is True, so an empty `rows` printed CONTROL=OK -- the control row whose
#  entire job is to prove this probe MEASURED something would certify a run that
#  measured nothing, and gate_sh_rounding.sh's `check "... control proves it
#  measures" "OK"` would pass on it.  Latent today (all 58 rows always run) and
#  reachable the moment any row selection exists, which is why it is closed BEFORE
#  that lands rather than with it.  Found by the opus seat while attacking a row
#  filter that was withdrawn -- the filter went, the hazard it exposed stayed.
#  [#556, 2026-10-02 -- a records correction; the text above is kept as it was written] Latent today (all 60 rows
#  always run) and.  (hgdromdefaultprobe:F11: regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md)
print("GDROM_DEF_CONTROL=%s"
      % ("OK" if rows and all(ok for _, ok in rows) else "DEAD"))

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
    t, alive, how = session(cmds)
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

t, alive, how = session(ld(UNIMPL_A) + run([MOV_L_AT_R1_R2, MOV_L_AT_R1_R2]))
row("same twice", ("%d" % len(SAYS.findall(t))) if alive else "died", "1",
    "SAME offset twice -> one line")

#  r1 then r3, so both loads have their own address register and both can be
#  planted contiguously.
t, alive, how = session(pair(["r1=0x%x" % UNIMPL_A, "r3=0x%x" % UNIMPL_B, "r2=0"],
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
t, alive, how = session(pair(ld(UNIMPL_A) + st(UNIMPL_A, 0x1234),
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
t, alive, how = session(pair(["r1=0x%x" % UNIMPL_A, "r3=0x%x" % (UNIMPL_A + 2), "r2=0"],
                        [MOV_L_AT_R1_R2, MOV_W_AT_R3_R2]))
row("granularity", ("%d" % len(SAYS.findall(t))) if alive else "died", "1",
    "+0x00 then +0x02 are ONE word -> one line")

#  ---------------------------------------------------------------- accept side
#
#  The de-escalation clause: this fix removes a host-fatal predicate, so the
#  detector must pin that the IMPLEMENTED offsets still work.  Without these,
#  a mutant that turns the whole switch into `default:` -- or simply deletes
#  the implemented arms -- scores full marks on every row above.
#  [#556, 2026-10-02 -- a records correction; the text above is kept as it was written] scores full marks on the
#  default-trigger rows above (though impl ok would catch CNTHI deletion).  (hgdromdefaultprobe:F7:
#  regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md)

t, alive, how = session(pair(st(IMPL_CNTLO, 0x98) + ld(IMPL_CNTLO),
                        [MOV_W_R8_AT_R7, MOV_W_AT_R1_R2]) + ["print r2"])
row("accept cnt", printed(t, "r2") if alive else "died", "0x98",
    "CNTLO (+0x90) still stores and reads back")

t, alive, how = session(pair(st(IMPL_COND, 0xa0) + ld(IMPL_BUSY),
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
t, alive, how = session(["r1=0x%x" % BASE, "r2=0"] + run(ops), settle=8.0, spin=3.0)
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
#  [#556, 2026-10-02 -- a records correction; the text above is kept as it was written] The scan hardcodes 64 words
#  and 56 declines; accept8 iterates IMPLEMENTED_WORDS.  (hgdromdefaultprobe:F8:
#  regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md)
IMPLEMENTED = IMPLEMENTED_WORDS
#  Eight loads through ONE address register, re-pointed between steps is not
#  possible in a single run -- so use r1 and step the loads one at a time with
#  an explicit pc per access, which is the one place the two-run hazard does
#  NOT apply because each access is its own complete run.
t = ""
alive = True
for i, off in enumerate(IMPLEMENTED):
    tt, aa, hh = session(pair(["r1=0x%x" % (BASE + off), "r2=0"], [MOV_W_AT_R1_R2]))
    t += tt
    alive = alive and aa
row("accept8", ("%d" % len(SAYS.findall(t))) if alive else "died", "0",
    "all EIGHT implemented offsets stay off the default arm")

#  And GDROM_DATA's own accept side, which also closes an escape already filed
#  against #460: no row there pinned what a declined DATA read returns.
t, alive, how = session(ld(BASE + 0x80) + run([MOV_W_AT_R1_R2]) + ["print r2"])
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
t, alive, how = session(pair(["r1=0x%x" % DMA, "r2=0"], [MOV_L_AT_R1_R2]))
row("dma rd", "survived" if alive else "died", "survived",
    "32-bit READ at DMA+0x00")
row("dma rd x1", ("%d" % len(DMA_SAYS.findall(t))) if alive else "died", "1",
    "the DMA arm names itself EXACTLY once")

t, alive, how = session(pair(["r1=0x%x" % (DMA + 0x00), "r3=0x%x" % (DMA + 0x7c), "r2=0"],
                        [MOV_L_AT_R1_R2, MOV_L_AT_R3_R2]))
row("dma two", ("%d" % len(DMA_SAYS.findall(t))) if alive else "died", "2",
    "DIFFERENT DMA offsets -> TWO lines, separate array")

#  *** THE ASYMMETRY THIS ROUND HAD TO NAME, NOW PINNED. ***  In the control
#  window declining returns 0 and a declined write does nothing.  Here `odata`
#  is preloaded from the shadow register file before the switch and the tail
#  STORES a declined write into it -- so "decline" means store-and-return, which
#  is what the five implemented cases already do and is kept deliberately.
#  Without this row that difference is a claim in a comment and nothing else.
t, alive, how = session(pair(["r7=0x%x" % DMA, "r8=0x12345678", "r1=0x%x" % DMA, "r2=0"],
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
t, alive, how = session(pair(["r7=0x%x" % (DMA + 0x04), "r8=0x11223344",
                         "r1=0x%x" % (DMA + 0x04), "r2=0"],
                        [MOV_L_R8_AT_R7, MOV_L_AT_R1_R2]) + ["print r2"])
row("dma seed", printed(t, "r2") if alive else "died", "0x11223344",
    "the implemented +0x04 takes a known value")

t, alive, how = session(pair(["r7=0x%x" % (DMA + 0x04), "r8=0x11223344",
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
t, alive, how = session(pair(["r7=0x%x" % (DMA + 0x04), "r8=0x11223344",
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
t, alive, how = session(pair(["r7=0x%x" % (DMA + 0x04), "r8=0x11223344",
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
t, alive, how = session(pair(["r1=0x%x" % UNIMPL_A, "r3=0x%x" % (DMA + 0x00),
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
    tt, aa, hh = session(pair(["r1=0x%x" % (DMA + off), "r2=0"], [MOV_L_AT_R1_R2]))
    t += tt
    alive = alive and aa
row("dma accept", ("%d" % len(DMA_SAYS.findall(t))) if alive else "died", "0",
    "all five implemented DMA offsets stay off the default arm")

#  ========================================================================
#  #462: the DMA+0x18 pair.  Both sites ENDED THE HOST PROCESS on the
#  committed build, each measured with its own device-signature control.
#
#  The design came out of a three-way disagreement that measurement settled:
#  two seats said de-fatalising would HANG Linux in its poll loop; one said
#  latch-and-break; the flagship seat read the driver and found BOTH
#  incomplete -- every wait in that path is time-bounded (HZ*7 after the
#  trigger, HZ/2 before it), so a decline gives bounded EIO rather than a
#  hang, BUT a bare `break` leaves the trigger value in the shadow.
DMA_ARM = re.compile(r"unsupported arming, declined")
DMA_NOD = re.compile(r"DMA start with no staged data -- declined")

#  --- the ARMING-MISMATCH arm (on HEAD :845), armed wrongly
#  (count/enable not both 1 on a fresh device) ---
t, alive, how = session(pair(["r7=0x%x" % (DMA + 0x18), "r8=1"],
                        [MOV_L_R8_AT_R7]) + ["print r8"])
row("arm survive", "survived" if alive else "died", "survived",
    "one store to +0x18 no longer ends the host")
row("arm says", ("%d" % len(DMA_ARM.findall(t))) if alive else "died", "1",
    "and the decline SPEAKS -- a silent decline is what this round argued against")

#  *** THE ROW THAT MATTERS, and no panel seat named the defect it pins. ***
#
#  The window's tail store writes idata into dma_reg[6] after every aligned
#  break, and the SUCCESS arm sets `idata = 0` first -- which is why a
#  completed transfer polls idle.  Drop the exit(1) and simply break, the
#  shape #447/#459/#460/#461 all used at their sites, and the guest's
#  trigger value 1 reaches the shadow: +0x18 then reads BUSY FOREVER.
#
#  Linux survives that (bounded waits) -- and Linux is the guest this rests
#  on: mainline byte-reads +0x18 to poll completion.  *** THE NetBSD HALF OF
#  THIS COMMENT WAS WRONG AND IS CORRECTED HERE. ***  It cited
#  `while ((GDROM_BUSY & 0x88) != 0x08) ;` as an unbounded poll of +0x18.
#  That loop needs bit 3 SET and bit 7 CLEAR; +0x18 is {0, 1} and neither
#  ANDs to 0x08, so it would hang on CORRECT hardware.  It is the
#  command-start handshake on the CONTROL window's BUSY register, which
#  dev_dreamcast_gdrom.c's GDROM_COND case documents outright.  This row is
#  still the difference between the fix and the obvious fix.
t, alive, how = session(pair(["r7=0x%x" % (DMA + 0x18), "r8=1",
                         "r1=0x%x" % (DMA + 0x18), "r2=0"],
                        [MOV_L_R8_AT_R7, MOV_L_AT_R1_R2]) + ["print r2"])
row("arm idle", printed(t, "r2") if alive else "died", "0x0",
    "+0x18 reads IDLE after a declined trigger, not busy-forever")

#  *** A CLAUSE (d) ESCAPE, NAMED BY A PACKET-FED SEAT ON THE PASS-2 BRIEF
#  AND CONFIRMED BY READING THIS FILE.  It keeps BOTH guards and BOTH
#  diagnostics and nulls only the repair:
#
#      if (d->dma_reg[0x0c / sizeof(uint32_t)] == 0 &&
#          d->dma_reg[0x14 / sizeof(uint32_t)] == 0)
#              idata = 0;
#
#  `arm idle` above writes ONLY +0x18, so on a fresh device count and enable
#  are both 0, that condition is TRUE, and the row stays green -- while every
#  OTHER arming mismatch sticks busy-forever.  The row written to pin the
#  repair could not see the repair being nulled, which is the same structural
#  blindness `dma alias` had against the one-character `m_align1`.
#
#  This row arms HALF way: count=1 with enable still 0.  That is a real guest
#  state -- a driver interrupted between its two arming stores -- and it makes
#  the mutant's condition FALSE.
#
#  NOTE the poison preset `r2=0x5a`, which the two older idle rows do not use.
#  They preset r2=0 and EXPECT 0x0, so a load that never executed would read
#  as a pass; their measured kills discharge that, but the shape is fragile.
#  0x5a is neither the expected 0x0 nor the sticky 0x1, so this row tells
#  green, sticky and never-ran apart BY VALUE.
t, alive, how = session(pair(["r3=0x%x" % (DMA + 0x0c), "r4=1",
                         "r7=0x%x" % (DMA + 0x18), "r8=1",
                         "r1=0x%x" % (DMA + 0x18), "r2=0x5a"],
                        [MOV_L_R4_AT_R3, MOV_L_R8_AT_R7, MOV_L_AT_R1_R2])
                   + ["print r2"])
row("arm halfarm", printed(t, "r2") if alive else "died", "0x0",
    "+0x18 idle after a HALF-armed decline (count=1, enable=0)")

#  *** ONE SESSION THAT DRIVES BOTH DECLINE ARMS. ***  A seat predicted, before
#  the table ran, that a mutant collapsing the two arms onto a SHARED warn bit
#  would escape every row -- because no session anywhere reaches both arms, so
#  the first arm's latch silencing the second is unobservable.  This closes it:
#  a bare trigger takes the ARMING arm, then arming properly and triggering
#  again takes the NO-STAGED-DATA arm, and BOTH must speak.
t, alive, how = session(pair(["r7=0x%x" % (DMA + 0x18), "r8=1",
                         "r3=0x%x" % (DMA + 0x0c), "r4=1",
                         "r5=0x%x" % (DMA + 0x14), "r6=1",
                         "r1=0x%x" % (DMA + 0x18), "r2=1"],
                        [MOV_L_R8_AT_R7, MOV_L_R4_AT_R3, MOV_L_R6_AT_R5,
                         MOV_L_R2_AT_R1]))
row("both decl",
    ("%d" % (len(DMA_ARM.findall(t)) + len(DMA_NOD.findall(t)))) if alive else "died",
    "2", "BOTH decline arms in one session must EACH speak (separate latches)")

#  the latch: a guest that retries must not flood
t, alive, how = session(pair(["r7=0x%x" % (DMA + 0x18), "r8=1",
                         "r5=0x%x" % (DMA + 0x18), "r6=1"],
                        [MOV_L_R8_AT_R7, MOV_L_R6_AT_R5]) + ["print r8"])
row("arm once", ("%d" % len(DMA_ARM.findall(t))) if alive else "died", "1",
    "TWO triggers -> ONE line")

#  --- the NO-STAGED-DATA arm (on HEAD :829).  NOTE the row name:
#  `nodata survive` was 14 characters, exactly
#  the %-14s column, leaving ZERO trailing spaces -- so the gate's `^$v  `
#  two-space match becomes UNSATISFIABLE and the row silently stops being
#  tested.  Caught by a name-length check before anything ran.  `nodata live`
#  is 11.
#  [#556, 2026-10-02 -- a records correction; the text above is kept as it was written] at L=14 it leaves ONE space,
#  so the gate's ^$v  anchor matches 0 lines and the gate fails.  (hgdromdefaultprobe:F9:
#  regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md)
#  --- the NO-STAGED-DATA arm (on HEAD :829), armed correctly but
#  nothing staged.  A COMPLIANT guest reaches
#  this: Linux programs the four DMA registers BEFORE sending its packet, so
#  a short image or a refused sector count leaves d->data NULL and the guest,
#  told nothing it checks, triggers anyway.
t, alive, how = session(pair(["r7=0x%x" % (DMA + 0x0c), "r8=1",
                         "r5=0x%x" % (DMA + 0x14), "r6=1",
                         "r1=0x%x" % (DMA + 0x18), "r2=1"],
                        [MOV_L_R8_AT_R7, MOV_L_R6_AT_R5, MOV_L_R2_AT_R1]))
row("nodata live", "survived" if alive else "died", "survived",
    "arming with no staged data no longer ends the host")
row("nodata says", ("%d" % len(DMA_NOD.findall(t))) if alive else "died", "1",
    "and it names itself exactly once")

#  *** THE DECLINED PATH MUST NOT ANNOUNCE A TRANSFER IT DOES NOT RUN. ***
#  Two seats found this independently from opposite directions: the
#  `Transfering %i bytes` fatal sits ABOVE the `d->data == NULL` test, so the
#  declined session printed "Transfering 0 bytes ..." and then "declined".  The
#  round's own comment claimed that line "prints data_len, the count actually
#  transferred" -- on this path nothing is transferred at all, so the claim was
#  false about the very path the round adds.  This row costs nothing: it reads
#  the transcript already in hand.
row("nodata notx", ("%d" % t.count("Transfering")) if alive else "died", "0",
    "a declined transfer must not ANNOUNCE itself as running")

#  *** THE STRUCTURAL TWIN OF `arm idle`, AND TWO SEATS FOUND IT MISSING
#  INDEPENDENTLY. ***  Without it the `idata = 0` at the
#  NO-STAGED-DATA arm is UNPINNED, so the
#  smallest possible regression -- deleting one line -- passes green.  The
#  sibling site had its row from the start; this one did not, which is the
#  asymmetry a reader of the fix would never notice.
t, alive, how = session(pair(["r7=0x%x" % (DMA + 0x0c), "r8=1",
                         "r5=0x%x" % (DMA + 0x14), "r6=1",
                         "r1=0x%x" % (DMA + 0x18), "r2=1"],
                        [MOV_L_R8_AT_R7, MOV_L_R6_AT_R5, MOV_L_R2_AT_R1])
                   + ["r1=0x%x" % (DMA + 0x18), "r2=0"]
                   + run([MOV_L_AT_R1_R2], CODE + 0x200) + ["print r2"])
row("nodata idle", printed(t, "r2") if alive else "died", "0x0",
    "+0x18 reads IDLE after the no-data decline too")

#  *** THE ROW THAT CLOSES THE ACTIVELY-HARMFUL MUTANT.  A seat measured that
#  firing SYSASIC_TRIGGER_EVENT on a declined path passes every other row here,
#  because nothing reads the pending register. ***
#
#  Why that mutant is worse than the defect this round fixes: the guest's
#  gdrom_dma_interrupt() clears gd.transfer UNCONDITIONALLY and inspects no
#  error bit, so a completion signalled on an EMPTY transfer ends the wait with
#  BLK_STS_OK -- the block layer is told the read succeeded while zero bytes
#  moved, and the guest consumes the destination page AS DISK DATA.  A host
#  death is loud; that is silent.
t, alive, how = session(pair(["r7=0x%x" % (DMA + 0x0c), "r8=1",
                         "r5=0x%x" % (DMA + 0x14), "r6=1",
                         "r1=0x%x" % (DMA + 0x18), "r2=1"],
                        [MOV_L_R8_AT_R7, MOV_L_R6_AT_R5, MOV_L_R2_AT_R1])
                   #  poison 0x4000, NOT 0 -- these two quiet rows expect "clear",
                   #  so with a 0 preset a load that never executed reads as a PASS
                   #  BY VALUE.  Their M8/M9 kills discharge vacuity today, but the
                   #  shape was fragile and it skipped this file's own 0x5a/0xa5
                   #  poison discipline.  Presetting the FAILURE-reading value makes
                   #  never-ran distinguishable at zero cost.
                   + ["r1=0x%x" % SYSASIC_PEND, "r2=0x4000"]
                   + run([MOV_L_AT_R1_R2], CODE + 0x200) + ["print r2"])
_p = printed(t, "r2") if alive else "died"
row("nodata quiet",
    ("clear" if (_p != "died" and not (int(_p, 16) & SYSASIC_DMA_BIT))
     else _p), "clear",
    "a DECLINED trigger must NOT signal completion")


#  *** THE ACCEPT BOUNDARY WAS ONLY EVER PROBED FROM THE NARROWING SIDE, and
#  THREE SEATS FOUND THAT INDEPENDENTLY on the ask-again. ***
#
#  The arming test is `count == 1 && enable == 1`.  M5 moved the boundary IN
#  (`== 2`) and the accept rows caught it.  Nothing moved it OUT.  Every row in
#  this file drives (count, enable) at (0,0), (1,0) or (1,1) -- and at all three
#  points `== 1` and `!= 0` agree, so widening to `count && enable`, `>= 1` or
#  bare truthiness is INDISTINGUISHABLE to the whole table.
#
#  `arm halfarm` is the row built to probe this predicate off its canonical
#  points, and it cannot see this: it half-arms by ZEROING a register, never by
#  EXCEEDING one, so at (1,0) both forms are false.  Same structural blindness
#  as `dma alias` against `m_align1`.
#
#  TWO rows, not one, because each comparison can be widened ALONE: a (2,1) row
#  is green under an enable-only widening.
t, alive, how = session(pair(["r3=0x%x" % (DMA + 0x0c), "r4=2",
                         "r5=0x%x" % (DMA + 0x14), "r6=1",
                         "r7=0x%x" % (DMA + 0x18), "r8=1"],
                        [MOV_L_R4_AT_R3, MOV_L_R6_AT_R5, MOV_L_R8_AT_R7]))
row("arm count2",
    ("%d/%d" % (len(DMA_ARM.findall(t)), len(DMA_NOD.findall(t)))) if alive else "died",
    "1/0", "count=2 enable=1 must still be REFUSED, not widened into accept")

t, alive, how = session(pair(["r3=0x%x" % (DMA + 0x0c), "r4=1",
                         "r5=0x%x" % (DMA + 0x14), "r6=2",
                         "r7=0x%x" % (DMA + 0x18), "r8=1"],
                        [MOV_L_R4_AT_R3, MOV_L_R6_AT_R5, MOV_L_R8_AT_R7]))
row("arm enable2",
    ("%d/%d" % (len(DMA_ARM.findall(t)), len(DMA_NOD.findall(t)))) if alive else "died",
    "1/0", "enable=2 count=1 must still be REFUSED -- each half widens alone")

#  *** THE NO-DATA ARM'S LATCH-SCOPED TWIN, AND `arm twice` DOES NOT COVER IT. ***
#
#  A seat found this on the capped ask-again and named the gap exactly: "that is
#  the exact shape `arm twice` was written to close.  The row is arming-only.
#  There is no `nodata twice`."  It then sat UNREAD for hours, because its
#  verdict line was recorded and the answer behind it was not opened.
#
#  The mutant, which reads as tidying rather than as a change:
#
#      if (!(d->warned & GDROM_W_DMANODATA)) {
#              d->warned |= GDROM_W_DMANODATA;
#              fatal("[ ... no staged data -- declined ... ] (once) ]");
#              idata = 0;        /* moved INSIDE */
#      }
#      break;
#
#  The FIRST no-data trigger still prints and still clears, so every existing
#  row stays green -- they all trigger that arm exactly once in a freshly forked
#  emulator.  Every LATER trigger leaves the guest's value in dma_reg[6] and
#  +0x18 reads BUSY FOREVER.  Under the corrected clause (d) -- which enumerates
#  the predicates a fix DEPENDS ON, not only those it adds -- that is
#  guard-kept-repair-nulled: an L2 floor breach, fixed in-round however late.
#
#  Poison 0xa5 again, so never-ran (0xa5) is distinguishable from sticky (0x1).
t, alive, how = session(pair(["r7=0x%x" % (DMA + 0x0c), "r8=1",
                         "r5=0x%x" % (DMA + 0x14), "r6=1",
                         "r1=0x%x" % (DMA + 0x18), "r2=1",
                         "r3=0x%x" % (DMA + 0x18), "r4=1"],
                        [MOV_L_R8_AT_R7, MOV_L_R6_AT_R5, MOV_L_R2_AT_R1,
                         MOV_L_R4_AT_R3])
                   + ["r1=0x%x" % (DMA + 0x18), "r2=0xa5"]
                   + run([MOV_L_AT_R1_R2], CODE + 0x220) + ["print r2"])
row("nodata twice", printed(t, "r2") if alive else "died", "0x0",
    "+0x18 idle after the SECOND no-data decline, not only the latched first")

#  *** THE ARMING ARM'S OWN COMPLETION-EVENT ROW, and its absence was the
#  round's one UNDISCHARGED OBLIGATION (L3).  `nodata quiet` above pins "a
#  declined trigger must not signal completion" for ONE of the two declining
#  arms.  The fix's own comment states that requirement as a design rule for
#  BOTH.  Nothing carried it for the arming arm, so adding
#  SYSASIC_TRIGGER_EVENT to that arm alone scored a clean sweep -- the round
#  would have shipped its worst-case mutant half-closed.
t, alive, how = session(pair(["r7=0x%x" % (DMA + 0x18), "r8=1",
                         "r1=0x%x" % SYSASIC_PEND, "r2=0x4000"],
                        [MOV_L_R8_AT_R7, MOV_L_AT_R1_R2]) + ["print r2"])
_a = printed(t, "r2") if alive else "died"
row("arm quiet",
    ("clear" if (_a != "died" and not (int(_a, 16) & SYSASIC_DMA_BIT)) else _a),
    "clear", "the ARMING decline must not signal completion either")

#  *** THE LATCH-STATE MEMBER of the same family `arm halfarm` closes. ***  A
#  seat pointed out that every idle row above triggers exactly ONCE in a
#  freshly forked emulator, so moving `idata = 0` INSIDE the `if (!(d->warned
#  & ...))` block passes all of them: the first and only observed decline still
#  clears, and every later one sticks BUSY FOREVER.  `arm once` does trigger
#  twice, but it counts diagnostics instead of reading +0x18.  This row reads
#  +0x18 after the SECOND decline.
t, alive, how = session(pair(["r7=0x%x" % (DMA + 0x18), "r8=1",
                         "r5=0x%x" % (DMA + 0x18), "r6=1",
                         "r1=0x%x" % (DMA + 0x18), "r2=0x5a"],
                        [MOV_L_R8_AT_R7, MOV_L_R6_AT_R5, MOV_L_AT_R1_R2])
                   + ["print r2"])
row("arm twice", printed(t, "r2") if alive else "died", "0x0",
    "+0x18 idle after the SECOND decline, not only the latched first")

#  *** THE LENGTH BLIND SPOT.  No row anywhere wrote DMA +0x08, so any repair
#  conditioned on the guest's programmed length -- `if (!length) idata = 0;` --
#  cleared on every row here (length is 0 throughout) while sticking BUSY for a
#  Linux-shaped guest, which programs +0x08 BEFORE it triggers.
t, alive, how = session(pair(["r3=0x%x" % (DMA + 0x08), "r4=0x800",
                         "r7=0x%x" % (DMA + 0x0c), "r8=1",
                         "r5=0x%x" % (DMA + 0x14), "r6=1",
                         "r1=0x%x" % (DMA + 0x18), "r2=1"],
                        [MOV_L_R4_AT_R3, MOV_L_R8_AT_R7, MOV_L_R6_AT_R5,
                         MOV_L_R2_AT_R1])
                   + ["r1=0x%x" % (DMA + 0x18), "r2=0x5a"]
                   + run([MOV_L_AT_R1_R2], CODE + 0x200) + ["print r2"])
row("nodata len", printed(t, "r2") if alive else "died", "0x0",
    "+0x18 idle when a LENGTH was programmed first, as Linux does")

#  *** THE WIDTH BLIND SPOT.  Every #462 store to +0x18 was 32-bit, so a repair
#  conditioned on access width -- `if (len == 4) idata = 0;` -- passed the whole
#  table.  This tree ALREADY established, in the `gdromdmawidth` assessment,
#  that mainline Linux BYTE-writes this register, so that mutant is not
#  hypothetical: it breaks the one guest whose behaviour the round documented.
#
#  *** AND THIS ROW ALSO CARRIES THE TRIGGER-VALUE CLOSE. ***  A seat observed
#  that EVERY +0x18 trigger in every other row stores the value 1, so a repair
#  written `idata &= ~1u;` or `idata -= 1;` -- both plausible as "clear the
#  trigger bit" -- passed the whole table while any guest trigger >= 2 stuck.
#  The arm fires on any nonzero and the diagnostic does not print the trigger,
#  so triggering with 0x5a costs nothing and closes that family here.
#
#  NOTE the poison preset is 0xa5, NOT 0x5a as the other rows use.  The seat's
#  suggestion was to trigger with 0x5a while keeping the 0x5a preset -- but then
#  "the mutant left the trigger stuck" and "the load never executed" both read
#  back 0x5a and the row could not tell them apart.  Trigger and poison must
#  DIFFER, which is the same three-outcome discipline `accept data` uses.
t, alive, how = session(pair(["r5=0x%x" % (DMA + 0x18), "r6=0x5a",
                         "r1=0x%x" % (DMA + 0x18), "r2=0xa5"],
                        [MOV_B_R6_AT_R5, MOV_L_AT_R1_R2]) + ["print r2"])
row("arm bytetrig", printed(t, "r2") if alive else "died", "0x0",
    "a BYTE trigger of 0x5a declines and clears -- not just a 32-bit 1")


#  *** #490 L4 -- READ THIS BEFORE THE BLOCK BELOW.  EVERYTHING IN IT WAS TRUE WHEN
#  #462 WROTE IT AND WAS EXPIRED BY #465 THREE ROUNDS LATER.  THE ROWS ARE SOUND; THEIR
#  STATED WARRANT IS NOT, AND A KILL CLAIM RODE ON IT. ***
#
#  THE CHRONOLOGY, from git rather than memory:
#      7c9dd9e (#462)  wrote this block and its three-state model
#      4d05cf0 (#465)  "data and data_len were RELEASED APART" -- the fix for exactly
#                      the hazard this block describes
#
#  Post-#465 `free_data()` sets BOTH `d->data = NULL` and `d->data_len = 0`, and it is
#  `handle_command`'s prologue.  So:
#    * the THIRD state below (`data == NULL, data_len STALE`) is NOT CONSTRUCTIBLE by
#      this route -- the session builds the FIRST state, both fields agreeing at zero;
#    * "handle_command ... NEVER resets d->data_len" is FALSE -- free_data resets it;
#    * "leaving data_len at the TOC's 408" is FALSE -- the prologue already zeroed it;
#    * and the M11 claim -- that swapping the guard to `d->data_len == 0` reaches
#      `memory_rw(..., NULL, 408, ...)` -- IS REFUTED BY MEASUREMENT, not by argument.
#
#  MEASURED 2026-08-28 (artifacts/gdromexitsix/opus_r2table_20260828/): the M11 mutant
#  built as a single line over the R2 fix, both trees run, results BYTE-IDENTICAL --
#      fixed:  alive=True  stale_says=1  stale_idle=0x0  Transfering=0
#      M11:    alive=True  stale_says=1  stale_idle=0x0  Transfering=0
#  M11 is EQUIVALENT.  No row can kill it because there is nothing left to kill.
#
#  *** THE GENERAL LESSON, and it is the reason this is written out rather than deleted:
#  A KILL RECORD IS TIME-INDEXED EXACTLY AS AN ABSENCE RECORD IS. ***  The carrier already
#  says an absence record must name its warrant and that any edit touching that warrant
#  RE-RUNS the death measurement.  The same holds for a claim that a mutant IS killed:
#  #465 edited the warrant, and nothing re-ran the test for three rounds.  The block is
#  kept because its REASONING is still the right reasoning -- it is the WORLD that moved.
#
#  What the rows below actually pin, stated correctly: the NO-DATA decline path, with
#  both fields at zero.  That is real, reachable, and worth a row.  It is simply not the
#  third state.
#
#  *** THE STATE THE FIX WAS WRITTEN FOR, AND UNTIL NOW NO ROW BUILT IT. ***
#
#  A seat observed that this detector sees `d->data` in TWO states and there are
#  THREE:
#      never-allocated      data == NULL, data_len == 0     <- every nodata row
#      successfully-alloc   data != NULL, data_len == 408   <- the accept session
#      FAILED COMMAND       data == NULL, data_len STALE    <- nothing, until now
#
#  The third is exactly what this round's own motivation describes: a command
#  fails, `handle_command` frees `d->data` and leaves it NULL -- but NEVER resets
#  `d->data_len`, which is assigned in `alloc_data` and nowhere else.
#
#  Why it matters beyond completeness: `if (d->data == NULL)` -> `if
#  (d->data_len == 0)` reads as a tidy-up (the guard tests one field while the
#  body it guards uses another) and scores a CLEAN SWEEP on the 52-row table,
#  because in the only two states the table builds, both operands agree.  In the
#  third state the mutated guard is FALSE and control reaches
#  `memory_rw(..., d->data /* NULL */, d->data_len /* 408 */, ...)` -- a
#  multi-kilobyte read from a NULL pointer.  The round's own defect class,
#  restored through a different door.
#
#  CONSTRUCTION, and every constant is derived rather than guessed.  The data
#  port fills the packet LOW BYTE FIRST (`cmd[n] = idata; cmd[n+1] = idata >> 8`),
#  which is why the TOC staging writes 0x0014 to mean command 0x14.  So 0x2030
#  gives cmd[0] = 0x30 (read sectors) and cmd[1] = 0x20 (the ONLY data format
#  that does not itself exit).  cmd[8..10] stay zero, so sector_count is 0, and
#  OB-20's clamp rejects and `break`s BEFORE `alloc_data` -- leaving data_len at
#  the TOC's 408.
t, alive, how = session(
    ["r7=0x%x" % GDROM_CNTLO, "r8=0x98"] + run([MOV_W_R8_AT_R7])
    + ["r7=0x%x" % GDROM_CNTHI, "r8=0x01"] + run([MOV_W_R8_AT_R7], CODE + 0x20)
    + ["r7=0x%x" % GDROM_COND, "r8=0xa0"] + run([MOV_W_R8_AT_R7], CODE + 0x40)
    + ["r7=0x%x" % GDROM_DATAP, "r8=0x0014"]
    + run([MOV_W_R8_AT_R7] * 6, CODE + 0x60)
    #  second command: 0x30 / format 0x20 / sector_count 0 -> OB-20 rejects
    + ["r7=0x%x" % GDROM_COND, "r8=0xa0"] + run([MOV_W_R8_AT_R7], CODE + 0x100)
    + ["r7=0x%x" % GDROM_DATAP, "r8=0x2030"]
    + run([MOV_W_R8_AT_R7], CODE + 0x120)
    + ["r8=0x0000"] + run([MOV_W_R8_AT_R7] * 5, CODE + 0x140)
    #  *** #490 L4: THIS SAID "data is NULL, data_len is STALE" AND THAT STATE HAS NOT
    #  EXISTED SINCE #465. ***  handle_command's prologue is `free_data(d); /* #465 */`
    #  and free_data sets BOTH `d->data = NULL` AND `d->data_len = 0`.  Before #465 the
    #  prologue cleared only the POINTER, which is why the original evidence for this
    #  row read `Transfering 408 bytes to 0x00000000` -- a pre-#465 artefact.
    #  MEASURED, not argued: swapping the DMA arm's guard operand from `data == NULL`
    #  to `data_len == 0` is BEHAVIOURALLY EQUIVALENT -- both trees return
    #  `alive=True stale_says=1 stale_idle=0x0 Transfering=0`, byte for byte.
    #  What the session actually builds is the NO-DATA state: both fields agree at
    #  zero, and the DMA arm declines on that.  The row is sound; its description was
    #  a wrong record.  (Found by the opus seat; the equivalence re-measured here
    #  rather than inherited, because a KILL record is time-indexed exactly as an
    #  absence record is -- #465 edited the warrant and nothing re-ran the test.)
    #  arm correctly and trigger: data NULL and data_len 0 -- the no-data state
    + ["r7=0x%x" % (DMA + 0x0c), "r8=1"] + run([MOV_L_R8_AT_R7], CODE + 0x1a0)
    + ["r7=0x%x" % (DMA + 0x14), "r8=1"] + run([MOV_L_R8_AT_R7], CODE + 0x1c0)
    + ["r7=0x%x" % (DMA + 0x18), "r8=1"] + run([MOV_L_R8_AT_R7], CODE + 0x1e0)
    + ["r1=0x%x" % (DMA + 0x18), "r2=0xa5"]
    + run([MOV_L_AT_R1_R2], CODE + 0x200) + ["print r2"])
row("nodata stale", "survived" if alive else "died", "survived",
    "FAILED-COMMAND state: data NULL, data_len 0 -- the fix's own path")
row("stale says", ("%d" % len(DMA_NOD.findall(t))) if alive else "died", "1",
    "and it declines by the NO-DATA arm, exactly once")
row("stale idle", printed(t, "r2") if alive else "died", "0x0",
    "+0x18 idle after the stale-length decline (0xa5 = the load never ran)")

#  *** #490: `stale quiet` RESTORES WHAT THE SIBLING FIX BLINDED, AND THE LOSS WAS MEASURED
#  BEFORE THE FIX LANDED RATHER THAN INFERRED AFTER. ***
#
#  The three rows above detect a mis-assembled packet only by the HOST DYING: each reads
#  `... if alive else "died"`.  Frozen and measured on the committed build, a packet with
#  cmd[0]=0x31 or cmd[1]=0x21 scored **55/58, CAUGHT** -- all three red, all via `died`.
#
#  #490 de-fatalised both of those sites.  Re-measured against the post-fix binary with the
#  SAME two packets: **58/58 BOTH TIMES** -- the triple reverts and this probe reads exactly   [58-row denominator, as measured then]
#  what a CORRECT packet reads.  Not merely vacuous: ACTIVELY MISLEADING, because a future
#  maintainer whose packet rots gets a clean run.
#      artifacts/gdromexitsix/challenge_freeze_20260828/  (pre-fix, 55/58 twice)
#      artifacts/gdromexitsix/blinding_20260828/          (post-fix, 58/58 twice)   [58-row denominator, as measured then]
#
#  *** THOSE ARE 58-row FIGURES AND STAY THAT WAY. ***  They are what the probe
#  measured when it had 58 rows; the gate pin is authoritative for TODAY's
#  denominator, and restating a past measurement in a later denominator is exactly
#  the frozen-number defect this project keeps correcting.  A score names the
#  artifact that produced it, and these two name theirs.
#
#  This row reads the DECLINE TEXT instead, on the session that is supposed to send a
#  CORRECT packet.  A mis-assembled one now reddens it whether or not the host survives.
#  kills: a rotted test packet, and a deleted `case 0x30` (which would decline at default:)
#  via:   the two anchored decline regexes, which cannot fire on a correct packet
row("stale quiet", "%d" % (len(FMT_DECL.findall(t)) + len(CMD_DECL.findall(t))), "0",
    "the packet is well-formed -- NEITHER new site declines it")

#  *** #490: THE DEATH-MODE ORACLE.  `how` has been threaded through 37 call sites since
#  ea97a10 and UNTIL NOW NO ROW READ IT -- that commit said so in its own message and the
#  plumbing stayed inert. ***  `alive` is False only when a read fails INSIDE a budget
#  window, so it is true of a HUNG emulator, a FROZEN one, and -- measured -- one already
#  killed after the last budget check.  `how` is the exit status and cannot be fooled that
#  way.
#  *** THE kills: LINE HERE READ "floor clause (b) -- reinstating either exit(1) at the
#  sibling sites", AND THAT IS FALSE.  Caught by a pass-2 seat, 2026-08-29. ***  This
#  session sends a CORRECT packet, which reaches NEITHER de-fatalised site -- so under a
#  reinstated exit(1) at either one the session never gets there, exits 0, and this row
#  stays GREEN.  Its named channel cannot vary under its named mutant, which is exactly
#  what the CHANNEL check calls vacuous BY CONSTRUCTION.  The claim was true only JOINTLY
#  with packet rot, and `stale quiet` is the row that carries rot.
#
#  kills: a death the budget-window read pattern CANNOT SEE -- any build that exits after
#         the last budget check, which `alive` reports as True.  That is a real and
#         otherwise-unpinned channel: `how` had been threaded through 37 call sites since
#         ea97a10 with NO row reading it.
#  via:   the exit status, which `alive` structurally cannot see
#
#  *** THIS BLOCK PREDICTED "one rot-packet run reds `stale quiet` AND DISCHARGES BOTH".
#  THE RUN HAPPENED AND REFUTED THE SECOND HALF.  Corrected 2026-08-29. ***
#
#  `regress/artifacts/gdromexitsix/rot_20260829/`, post-fix binary, one-line frozen-probe
#  edit (packed format byte 0x20 -> 0x21):
#
#      base.log   GDROM_DEF_RESULT=60/60    stale quiet  0 vs 0      ok
#      rot.log    GDROM_DEF_RESULT=59/60    stale quiet  1 vs 0    **FAIL**
#
#  The two `GDROM_DEF_VECTOR` lines differ in EXACTLY ONE POSITION, so the rot is
#  discriminating rather than merely disruptive -- proven by the probe's own vector, not
#  asserted.  **`stale quiet` is DISCHARGED by a measured kill.**
#
#  *** `stale how` IS NOT, AND THE REASON IS STRUCTURAL RATHER THAN AN OVERSIGHT. ***  It
#  stayed `exit0` under the rot because the fix DECLINES the bad format instead of dying, so
#  the session still ends cleanly.  A rotted packet cannot red this row at all.
#
#  AND IT IS THE WANTED-EQUALS-FAILURE SHAPE, which the round's own PRETABLE addendum names:
#  **this row WANTS `exit0`, and a BROKEN `how` capture also yields `exit0`.**  So a measured
#  red is not a nicety here -- it is the only thing that distinguishes a working oracle from
#  an inert one.  Killing it needs a mutant that makes the build EXIT AFTER the last budget
#  check; the reinstated-`exit(1)` binaries in the pass-2 ask-again's bins are the obvious
#  candidate, driven through the preserved rot instrument.
#
#  **UNTIL THAT IS MEASURED, TREAT THIS ROW AS UNPROVEN.**  Owed before the round closes.
row("stale how", how, "exit0",
    "and the session ended CLEANLY -- not merely answering when last asked")

#  *** THE DE-ESCALATION ACCEPT ROW.  The fix removed TWO host-fatal
#  predicates -- `d->data == NULL` and `count == 1 && enable == 1` -- and
#  the clause says the detector must pin the ACCEPT SIDE of each, or the
#  round has deleted a tripwire and shipped nothing in its place.
#
#  Before this fix, narrowing either predicate meant exit(1) on the first
#  legal transfer: unmissable.  After it, the same edit means a SILENTLY
#  REFUSED transfer and nothing anywhere notices.
#
#  *** ONE STAGING SESSION, FIVE ROWS -- and the sharing is the point, not the
#  saving. ***  These rows used to stage independently, which cost five full TOC
#  sequences and, worse, meant they observed five SIMILAR transfers.  Driven from
#  one session they observe THE SAME transfer, so "the arming was accepted",
#  "+0x18 polls idle", "no decline fired", "the event fired" and "the bytes
#  landed" are five facts about ONE event.
#
#  A row set describing one transfer can contradict itself and be caught.  Five
#  separate transfers can each be individually consistent and jointly wrong.
#
#  Staging is #460's sequence verbatim: CNTLO=0x98, CNTHI=0x01, COND=0xa0, then
#  six halfword stores of 0x0014 into the data port.  The TOC command allocates
#  d->data and fills it with DEVICE-GENERATED bytes (dev_dreamcast_gdrom.c:352-357
#  writes 0x10,0x00,0x00,0x96 over a 0xff background).
#
#  *** THAT PATTERN IS THE DEVICE-SIGNATURE CONTROL, AND UNTIL `accept data` IT
#  WAS CLAIMED AND NOT IMPLEMENTED. ***  The older wording here asserted "RAM
#  could not produce that pattern" while NO row read the destination at all --
#  a control named in prose and absent in fact, which is the shape this file
#  exists to catch.  `accept data` below reads it back.
#
#  *** AND `accept idle` IS NOT AN ACCEPT ROW.  FOUR SEATS SAID SO INDEPENDENTLY.
#  ***  It cannot redden under growth of EITHER de-fatalised predicate, because
#  all three arms -- success, no-data and arming-mismatch -- clear `idata`.  Its
#  own note admits it: "as the success arm has always done".  It is a LIVE row
#  (deleting the success arm's `idata = 0` kills it) but it is a REGRESSION row
#  for pre-existing success-arm behaviour, not an accept-side row, and counting
#  it toward the de-escalation obligation was a wrong record.
#
#  The obligation is discharged by `accept dma`, `accept event`, `accept quiet`
#  and `accept data`.
t, alive, how = session(
    ["r7=0x%x" % GDROM_CNTLO, "r8=0x98"] + run([MOV_W_R8_AT_R7])
    + ["r7=0x%x" % GDROM_CNTHI, "r8=0x01"] + run([MOV_W_R8_AT_R7], CODE + 0x20)
    + ["r7=0x%x" % GDROM_COND, "r8=0xa0"] + run([MOV_W_R8_AT_R7], CODE + 0x40)
    + ["r7=0x%x" % GDROM_DATAP, "r8=0x0014"]
    + run([MOV_W_R8_AT_R7] * 6, CODE + 0x60)
    #  arm correctly and trigger: the path that must still work
    + ["r7=0x%x" % (DMA + 0x04), "r8=0x0c008000"]
    + run([MOV_L_R8_AT_R7], CODE + 0x100)
    + ["r7=0x%x" % (DMA + 0x0c), "r8=1"]
    + run([MOV_L_R8_AT_R7], CODE + 0x120)
    + ["r7=0x%x" % (DMA + 0x14), "r8=1"]
    + run([MOV_L_R8_AT_R7], CODE + 0x140)
    + ["r7=0x%x" % (DMA + 0x18), "r8=1"]
    + run([MOV_L_R8_AT_R7], CODE + 0x160)
    #  and read BOTH observables from that one transfer
    + ["r1=0x%x" % (DMA + 0x18), "r2=0"]
    + run([MOV_L_AT_R1_R2], CODE + 0x180)
    + ["r1=0x%x" % SYSASIC_PEND, "r3=0"]
    + run([MOV_L_AT_R1_R3], CODE + 0x1a0)
    #  *** AND READ THE DESTINATION.  Until this row, NO row anywhere observed
    #  the DMA's data movement, so mutants that neutered the transfer itself --
    #  `d->data_len` -> 0, or a different `dst` mask -- left every row green
    #  while moving nothing.  The comment above ALSO claimed a device-signature
    #  control that nothing implemented; this is that control.
    #
    #  handle_command's TOC arm fills d->data[0..3] with 0x10,0x00,0x00,0x96
    #  over a 0xff background (dev_dreamcast_gdrom.c:352-357) and the DMA is a
    #  byte copy, so dst+0 is 0x10 whatever the byte order -- a BYTE load needs
    #  no endianness assumption, which a word load here would.
    #
    #  Three outcomes are distinguishable, which is the point:
    #      0x10        the transfer ran and moved DEVICE-generated bytes
    #      0xffffffea  it did NOT run -- see below
    #      0x5a        the load itself never executed (the poison preset)
    #
    #  *** THE MIDDLE LINE SAID `0x0  it never ran (the destination page is
    #  zero beforehand)` AND THE MUTANT TABLE MEASURED THAT FALSE. ***  Under
    #  M5 (`count == 1` -> `count == 2`, so a legal transfer is refused) this
    #  row read back 0xffffffea, not 0x0.  Two facts the original wording got
    #  wrong, and only a mutant that stops the transfer could expose either:
    #
    #    * the destination page is NOT zero beforehand.  DMA_DST_P1 is
    #      0x8c008000, 28 KB past CODE, and the session runs with a real
    #      kernel image loaded -- so the byte already there is 0xea.
    #    * `mov.b` SIGN-EXTENDS.  0xea has bit 7 set, so it arrives as
    #      0xffffffea.  0x10 does not, which is why the ran-case is clean.
    #
    #  The row still discriminates -- 0x10, 0xffffffea and 0x5a are three
    #  distinct values -- so the ROW is sound and only its stated REASON was
    #  wrong.  That is worth separating: a green row with a false explanation
    #  is a wrong record, not a vacuous row, and the fix is the comment.
    #
    #  Do NOT re-pin this row on 0xffffffea: that value is whatever the loaded
    #  image happens to put at that address, so it is an artefact of the
    #  KERNEL argument and not a property of the device.  The row asserts
    #  0x10 -- the device's own TOC byte -- and everything else is a failure.
    + ["r1=0x%x" % DMA_DST_P1, "r4=0x5a"]
    + run([MOV_B_AT_R1_R4], CODE + 0x1c0)
    + ["print r2", "print r3", "print r4"])

#  NOTE the wording.  This row was recorded as proving "a LEGAL armed transfer
#  with staged data still runs"; it proves the ARMING TEST passed and nothing
#  more, because the `Transfering` fatal printed BEFORE the `d->data == NULL`
#  check.  `accept data` below is the row that proves the transfer ran.
#  [#556, 2026-10-02 -- a records correction; the text above is kept as it was written] Transfering formerly printed
#  before the d->data == NULL check; #462 moved it below the check.  (hgdromdefaultprobe:F10:
#  regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md)
row("accept dma", "yes" if ("Transfering" in t and alive) else "no", "yes",
    "a LEGAL arming is still accepted and enters the transfer path")
#  NOT an accept row -- see the block above.  Kept because it is live.
row("accept idle", printed(t, "r2") if alive else "died", "0x0",
    "+0x18 polls IDLE after a real transfer (success-arm regression row)")
_q = printed(t, "r3") if alive else "died"
row("accept event",
    ("set" if (_q != "died" and (int(_q, 16) & SYSASIC_DMA_BIT)) else _q),
    "set", "a REAL transfer DOES signal completion")
row("accept quiet",
    ("%d" % (len(DMA_ARM.findall(t)) + len(DMA_NOD.findall(t)))) if alive else "died",
    "0", "with NEITHER decline diagnostic -- the accept side is not refused")
row("accept data", printed(t, "r4") if alive else "died", "0x10",
    "and the DEVICE's own TOC byte actually LANDED at the destination")


n = sum(1 for _, ok in rows if ok)
print("GDROM_DEF_RESULT=%d/%d" % (n, len(rows)))
print("GDROM_DEF_VECTOR=" + ",".join(("1" if ok else "0") for _, ok in rows))
