#!/usr/bin/env python3
#
#  #498 sgidewidth -- the detector.
#
#  CONTRACT (vacuity-floor clause (e)) -- which edits this detector is designed
#  to catch, and which it is NOT:
#
#    CATCHES
#      * reinstatement of the width kill, in either direction (`lo_decl',
#        `lo_alive', and the read-side `hi_rd_*' rows);
#      * a decline that returns `return 0', which cpus/memory_rw.c coerces to -1
#        and turns into a guest
#        EXCEPTION_DBE.  `lo_sent' and `hi_rd_sent' preset the destination
#        register to a SENTINEL, so "the tail ran and wrote odata (0)" and "the
#        load never completed" are distinguishable.  A survival-only oracle at
#        a refusal site is vacuous by construction.
#
#        *** THIS BULLET ONCE ALSO CLAIMED an early `return' AND THAT IS FALSE,
#        refuted by this round's own preserved log.  `gxdew_t2_mB.txt' scores the
#        early-`return 1' variant 25/25 with ZERO failing rows -- a clean escape.
#        The reason is `#95' in cpus/memory_rw.c, which memsets the caller's buffer
#        to 0 on a device READ before dispatch: so the value channel CANNOT
#        distinguish "the tail ran and wrote odata (0)" from "the handler skipped
#        the answer and the pre-zero supplied 0".  These rows kill `return 0' (a DBE
#        leaves the sentinel standing) and the pre-fix death; they are BLIND to an
#        early `return 1', which is disclosed as the unshipped mB variant.  A reader
#        trusting the old wording would skip building exactly the mutant that
#        escapes. ***
#      * a decline that FALLS THROUGH to the tail, which would run
#        draw_primitive() for an access we just refused (`hi_draw',
#        `hi_rd_draw').  MEASURED: the naive splice scores 19/25 here;
#      * a decline that falls through to the register SWITCH, which then
#        announces a TODO about a write that never happened (`dec_switch').
#        MEASURED: the otherwise-plausible "clear startFlag and fall through"
#        shape scores 24/25 and this is the row it reds;
#      * a repair qualified to writes only -- the read-direction rows are not
#        redundant with the write ones (`hi_rd_*' kill that mutant at 21/25);
#      * a repair hoisted so it applies to EVERY access, which would silently
#        disable all drawing.  *** THIS ONCE READ "`tail_acc' is the only row that
#        catches it" AND THAT WAS FALSE: the measured mE variant reds THREE rows --
#        tail_acc, tail_acc_x and dec_switch (22/25).  Coverage was never the
#        problem; the uniqueness claim was.  Corrected after a pass-2 seat checked it
#        against gxdew_t2_mE.txt rather than against this comment. ***
#      * accept-set GROWTH at len 2 (`len == 4 || len == 2'), which the `lo_*2' rows
#        below pin and which nothing else could see;
#      * reuse of #497's latch bit instead of a new one (`sharedlatch'):
#        the four handlers share one malloc'd struct, so sharing a bit lets an
#        sgi_re access silence sgi_de's decline entirely.  MEASURED 23/25;
#      * loss of the latch, so the decline floods (`lo_latch' COUNTS).
#
#    CATCHES (added by #500)
#      * reinstatement of draw_primitive()'s host kill, via `tail_acc_x' -- see the
#        re-pin note at that row.  It is a SURVIVAL row at +0xfd0, which the
#        paragraph below used to forbid.
#
#    DOES NOT CATCH
#      * *** THIS CLAUSE WAS TRUE UNTIL #500 AND IS CORRECTED IN PLACE RATHER THAN
#        SILENTLY SUPERSEDED.  It read: "Every access to +0x800..+0xfff already
#        ends the host inside draw_primitive() ... A row that wanted survival up
#        there would be testing the wrong defect."  #500 DE-FATALISED that arm, so
#        the premise is gone -- and this file's own re-pinned `tail_acc_x' IS now a
#        survival row at +0xfd0.  The DOES-NOT-CATCH list was forbidding the row
#        the same diff adds.  Found by a measuring seat, not by a gate. ***
#
#        What remains true: the accept rows below sit at +0x7fc/+0x7f8 rather than
#        at the nominal last slots, and that placement is still deliberate -- it
#        keeps them off the START alias so they test WIDTH and not drawing;
#      * an edit that changes only the message TEXT.  The rows count the
#        decline, they do not pin its wording beyond the `len=' prefix;
#      * anything in sgi_re, sgi_mte or sgi_de_status.
#
#  *** THE ROW SET IS NOT INVENTED HERE.  Each row below killed a specific
#  mutant in a nine-build, 25-row table measured before this file existed;
#  scores and variant sources are preserved under
#  regress/artifacts/sgidewidth/opus_witness_20260831/.  A row whose mutant is
#  named in its note is a row that has failed at least once. ***
#
import os
import pty
import re
import select
import sys
import time

BIN = sys.argv[1] if len(sys.argv) > 1 else "build/gxemul"
LABEL = sys.argv[2] if len(sys.argv) > 2 else "local"

DUMMY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dummy_kernel.bin")
if not os.path.exists(DUMMY):
    DUMMY = "/dev/null"

CODE = 0xffffffff80001000
SCRATCH_RAM = 0xffffffff80002000
DE = 0xffffffffb5002000              # sgi_de   @ phys 0x15002000
RE = 0xffffffffb5001000              # sgi_re   @ phys 0x15001000
DE_STATUS = 0xffffffffb5003000       # sgi_de_status, for the device signature

#  Hand-assembled, and every one is re-derived rather than copied: opcode(6)
#  rs(5) rt(5) imm(16).  Stores use a3 (reg 7) for the address and t0 (reg 8)
#  for the datum; loads use at (reg 1) and v0 (reg 2).
OP_NOP = 0x00000000
OP_B_SELF = 0x1000ffff
OP_SB_T0_A3 = 0xa0e80000             # sb   $t0, 0($a3)   101000 00111 01000
OP_SH_T0_A3 = 0xa4e80000             # sh   $t0, 0($a3)   101001 00111 01000
OP_SW_T0_A3 = 0xace80000             # sw   $t0, 0($a3)   101011 00111 01000
OP_SD_T0_A3 = 0xfce80000             # sd   $t0, 0($a3)   111111 00111 01000
OP_LBU_V0_AT = 0x90220000            # lbu  $v0, 0($at)   100100 00001 00010
OP_LHU_V0_AT = 0x94220000            # lhu  $v0, 0($at)   100101 00001 00010
OP_LW_V0_AT = 0x8c220000             # lw   $v0, 0($at)   100011 00001 00010
OP_LD_V0_AT = 0xdc220000             # ld   $v0, 0($at)   110111 00001 00010

DECL = "sgi_de: unimplemented len="          # the fix's decline announcement
KILL = "sgi_de: len = "                      # the pre-fix host kill
DRAW = "sgi_de: UNIMPLEMENTED drawing op"    # sgideprimop, the SECOND kill
SCIS = "sgi_de: TODO: non-zero CRIME_DE_SCISSOR"
RE_DECL = "sgi_re: unimplemented len=1 for CRIME_RE_TLB_A"

SENTINEL = 0xdeadbeef

rows = []


def row(name, got, want, note=""):
    ok = (got == want)
    rows.append((name, ok))
    print("%-16s %-14s %-14s %-44s %s" % (name, str(got), str(want), note,
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


def printed32(t, reg):
    """The low 32 bits of a register loaded by `lw`.

    *** lw SIGN-EXTENDS.  A 32-bit read of 0xcafebabe lands in the 64-bit
    register as 0xffffffffcafebabe, and a row comparing the raw string then
    FAILS on MIPS semantics rather than on device behaviour.  That bit this
    detector on its first run -- 21/22 with the device entirely correct --
    and the two neighbouring accept rows passed only because their fixtures
    happen to have bit 31 CLEAR. ***

    Masking rather than choosing a friendlier constant is deliberate: it
    makes the row correct BY CONSTRUCTION for any value, instead of correct
    by an accident of the fixture that the next person to edit it cannot
    see.  Nothing is lost -- for a `lw` the upper 32 bits carry no device
    data, only the sign extension.
    """
    v = printed(t, reg)
    if v == "absent":
        return v
    return "0x%x" % (int(v, 16) & 0xffffffff)


class Addr(object):
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


def store(A, addr, op=OP_SW_T0_A3, val="0x12345678"):
    return ["a3=0x%x" % addr, "t0=%s" % val] + run_ops([op], A.take(1))


def load(A, addr, op=OP_LW_V0_AT):
    return ["at=0x%x" % addr, "v0=0x%x" % SENTINEL] + run_ops([op], A.take(1))


print("#498 sgidewidth DETECTOR -- binary=%s label=%s" % (BIN, LABEL))
print("%-16s %-14s %-14s %-44s %s" % ("row", "got", "want", "note", ""))

# ---------------------------------------------------------------- controls (c)
A = Addr(CODE)
t, alive, how = session(store(A, SCRATCH_RAM, val="0xcafe00d")
                        + load(A, SCRATCH_RAM) + ["print v0"])
row("live", printed(t, "v0") if alive else "died", "0xcafe00d",
    "LIVENESS: store then load through RAM")

#  A SMALL NONZERO VALUE, deliberately: a wrong register field in a
#  hand-assembled encoding yields 0, which every sentinel/absent row would
#  accept by accident.  This row is the one that cannot be faked.
A = Addr(CODE)
t, alive, how = session(store(A, DE + 0x048, val="0x12345678"))
row("devsig", t.count(SCIS + ": 0x0000000012345678"), 1,
    "DEVSIG: the device echoes OUR value; RAM cannot")

# ------------------------------------------------- the decline itself, lower half
A = Addr(CODE)
t, alive, how = session(store(A, DE + 0x0d0, op=OP_SB_T0_A3, val="0x5a"))
row("lo_kill", t.count(KILL + "1 not implemented"), 0, "the pre-fix host kill is gone")
row("lo_decl", t.count(DECL + "1 -- declined"), 1, "and is announced instead")
row("lo_alive", how, "exit0", "host survives a 1-byte access")

A = Addr(CODE)
t, alive, how = session(load(A, DE + 0x0d0, op=OP_LBU_V0_AT) + ["print v0"])
row("lo_sent", printed(t, "v0") if alive else "died", "0x0",
    "declined READ answers 0, not the sentinel")

A = Addr(CODE)
t, alive, how = session(store(A, DE + 0x0d0, op=OP_SB_T0_A3, val="0x01")
                        + store(A, DE + 0x0e4, op=OP_SB_T0_A3, val="0x02"))
row("lo_latch", t.count(DECL), 1, "N=1 per device instance, two offsets")

# ------------------------------------------------- len == 2, THE OTHER REACHABLE WIDTH
#  *** ADDED AFTER PASS 2 MEASURED A HOLE: `len == 2' WAS NOT PINNED AS A LIVE DECLINE. ***
#  The witness was 4/4 across sb, sh, lbu and lhu; the rows above use sb and lbu ONLY, and
#  `sh' appeared solely as the SECOND access in `two_widths_*', whose oracle is "len=2 is
#  never announced".
#
#  That row stays GREEN whether len==2 is ACCEPTED, still KILLED with the old text, or
#  correctly DECLINED -- three different machines behind one green row -- and the ONE latch
#  bit is WHY: after `sb', a later `sh' is SUPPOSED to be silent, so silence proves nothing.
#  Two seats reached this independently on pass 2, one predicting the escaping edit as
#  `else if (len == 4 || len == 2)' at a full 25/25.
#
#  Each row runs in its OWN session, where the latch is fresh and len==2 is the FIRST
#  decline -- the only state in which its announcement is observable at all.
A = Addr(CODE)
t, alive, how = session(store(A, DE + 0x0d0, op=OP_SH_T0_A3, val="0x5a5a"))
row("lo_kill2", t.count(KILL + "2 not implemented"), 0, "len=2 host kill is gone too")
row("lo_decl2", t.count(DECL + "2 -- declined"), 1, "len=2 announces on a FRESH latch")
row("lo_alive2", how, "exit0", "host survives a 2-byte access")

A = Addr(CODE)
t, alive, how = session(load(A, DE + 0x0d0, op=OP_LHU_V0_AT) + ["print v0"])
row("lo_sent2", printed(t, "v0") if alive else "died", "0x0",
    "declined 2-byte READ answers 0 -- kills silent acceptance")

# ------------------------------------------------- the tail: a decline must not draw
#  *** THE LOWER-HALF STORE IN FRONT IS LOAD-BEARING, NOT SCENERY.  Without it every row
#  in this file exercised the FIRST decline of a fresh session, and a one-BRACE edit --
#  moving `goto de_declined;' inside the latch braces -- escaped all 25 rows: only the
#  first decline jumps, and every later one falls through to the switch AND
#  draw_primitive(), measured `exit1'.  That is the exact host death this round exists to
#  remove, re-opened by one character of indentation. ***
A = Addr(CODE)
t, alive, how = session(store(A, DE + 0x0d0, op=OP_SB_T0_A3, val="0x01")
                        + store(A, DE + 0x8d0, op=OP_SB_T0_A3, val="0x5a"), spin=1.6)
row("hi_kill", t.count(KILL + "1 not implemented"), 0,
    "len=1 kill gone up here too -- was pinned on an ACCEPTED width and could not vary")
row("hi_draw", t.count(DRAW), 0, "a SECOND declined write must not reach draw_primitive")
row("hi_alive", how, "exit0", "and must not die there either")

A = Addr(CODE)
t, alive, how = session(store(A, DE + 0x0d0, op=OP_SB_T0_A3, val="0x01")
                        + load(A, DE + 0x8d0, op=OP_LBU_V0_AT) + ["print v0"], spin=1.6)
row("hi_rd_draw", t.count(DRAW), 0, "declined READ must not draw -- kills a write-only repair")
row("hi_rd_alive", how, "exit0", "read direction is not redundant with write")
row("hi_rd_sent", printed(t, "v0") if alive else "died", "0x0",
    "declined read up here still answers 0")

# ------------------------------------------------- one latch bit, six widths
A = Addr(CODE)
t, alive, how = session(store(A, DE + 0x0d0, op=OP_SB_T0_A3, val="0x01")
                        + store(A, DE + 0x0d0, op=OP_SH_T0_A3, val="0x02"))
row("two_widths_n", t.count(DECL), 1, "ONE bit: the second width is silenced")
row("two_widths_1", t.count(DECL + "1 -- declined"), 1, "the announced one is len=1")
row("two_widths_2", t.count(DECL + "2 -- declined"), 0, "len=2 never announced")

# ------------------------------------------------- the switch must not lie
A = Addr(CODE)
t, alive, how = session(store(A, DE + 0x048, op=OP_SB_T0_A3, val="0x01"))
row("dec_switch", t.count(SCIS), 0,
    "a declined write must not announce a TODO about it")

# ------------------------------------------------- the SECOND kill must still fire
#  *** THESE THREE ROWS WERE MISSING FROM THE FIRST DRAFT, AND THE CONTRACT ABOVE
#  CLAIMED ONE OF THEM. ***  `tail_acc` is named there as the only row catching a repair
#  hoisted to apply to EVERY access -- a mutant that scores 22/25 and silently disables
#  ALL drawing.  Without the row the claim was a coverage assertion the file did not
#  back, which is the CLAIM -> ROW check failing inside a detector's own header.
#
#  They are ACCEPT rows for the tail rather than for a width: an accepted width with
#  startFlag set must STILL reach draw_primitive().  That it then ends the host is
#  `sgideprimop', a separate filed row -- so `tail_acc_x' pins a host DEATH on purpose,
#  and will need re-pinning when that row is fixed.  The oracle-correction ordering
#  applies: re-pin first, measure red, then edit.
#  *** `hi_kill' USED TO LIVE HERE, ON len=4, AND WAS VACUOUS BY CONSTRUCTION: len 4 is an
#  ACCEPTED width on every build in the story, so a row counting width-kill text there can
#  never vary.  MEASURED identical on the pre-fix build, on all eight of this round's
#  mutants, post-fix, and on all five of the pass-2 seat's.  Even a verbatim reinstatement
#  left it green.  It is re-pinned above onto the measured form (len=1, upper half), which
#  is a channel that moves.  Knowable at writing time by the CHANNEL check. ***
#  *** RE-PINNED FOR #500, AND NOT ONTO THE OBVIOUS ORACLE. ***
#
#  `tail_acc_x' pinned a host DEATH on purpose: an accepted width with startFlag
#  reached draw_primitive(), whose default arm killed on 254 of 256 op classes.
#  #500 de-fatalises that arm, so the row is CERTAIN red and owes a re-pin.
#
#  THE NATURAL CORRECTION IS `exit1' -> `exit0' AND IT IS A TRAP.  Trace the
#  channel rather than the intent: a future one-token reinstatement -- `exit(0)'
#  at the default arm instead of `exit(1)' -- announces once and then DIES.  `how'
#  is then "exit0", so the re-pinned row would read GREEN; `tail_acc' still counts
#  its one message, GREEN; and no other session reaches draw_primitive() at all.
#  TOTAL ESCAPE.  *** EXIT STATUS CANNOT VARY BETWEEN "DECLINED AND THEN QUIT" AND
#  "DIED WITH STATUS 0". ***  That is the `exit0oracle' class, and a sibling round
#  MEASURED exactly this shape as a 48/48 clean sweep on the same day.
#
#  So the re-pin is onto a POSITIVE POST-DRAW OBSERVABLE: after the drawing access,
#  the guest performs a further load through the device and the row asserts the
#  VALUE.  If the host quit at the draw, that load never runs and printed() returns
#  "absent", which is not the value -- so the row reds on a death however the death
#  is spelled.  The exit-status check is KEPT as a second channel (`tail_acc_h'),
#  because two channels that fail differently are worth more than one that fails
#  twice.
A = Addr(CODE)
t, alive, how = session(store(A, DE + 0xfd0, val="0x11223344")
                        + load(A, DE + 0x0d0, op=OP_LBU_V0_AT) + ["print v0"],
                        spin=1.6)
row("tail_acc", t.count(DRAW), 1,
    "accepted width + startFlag STILL reaches draw_primitive")
row("tail_acc_x", printed(t, "v0") if alive else "died", "0x0",
    "...and the guest RUNS ON -- kills a death however it is spelled")
row("tail_acc_h", how, "exit0",
    "...second channel: the process exits cleanly (weak alone -- see the note)")

# ------------------------------------------------- accept rows, LAST legal slot
#  +0x7fc / +0x7f8 and NOT +0xffc / +0xff8: the nominal last slots have bit
#  0x800 set, so they reach draw_primitive and die there (sgideprimop).  The
#  last slots with startFlag CLEAR are the real anchors, and that is a fact
#  about the device rather than a convenience.
A = Addr(CODE)
t, alive, how = session(store(A, DE + 0x7fc, val="0xcafebabe")
                        + load(A, DE + 0x7fc) + ["print v0"])
row("acc4_last", printed32(t, "v0") if alive else "died", "0xcafebabe",
    "len=4 W+R at the last 4-slot, startFlag clear")

A = Addr(CODE)
t, alive, how = session(store(A, DE + 0x7f8, op=OP_SD_T0_A3,
                              val="0x1122334455667788")
                        + load(A, DE + 0x7f8) + ["print v0"])
row("acc8_hi32", printed32(t, "v0") if alive else "died", "0x11223344",
    "len=8 write lands in de_reg[regnr]")

A = Addr(CODE)
t, alive, how = session(store(A, DE + 0x7f8, op=OP_SD_T0_A3,
                              val="0x1122334455667788")
                        + load(A, DE + 0x7fc) + ["print v0"])
row("acc8_lo32", printed32(t, "v0") if alive else "died", "0x55667788",
    "...and de_reg[regnr+1]")

A = Addr(CODE)
t, alive, how = session(store(A, DE + 0x7f8, op=OP_SD_T0_A3,
                              val="0x1122334455667788")
                        + load(A, DE + 0x7f8, op=OP_LD_V0_AT) + ["print v0"])
row("acc8_read", printed(t, "v0") if alive else "died", "0x1122334455667788",
    "len=8 READ direction, full recomposition")

# ------------------------------------------------- the latch must be its OWN bit
A = Addr(CODE)
#  *** SIX PARTNERS, NOT ONE.  This row used to trip only TLB_A (bit 1<<0), which made it a
#  POINT TEST against a six-member set: `1 << 6' -> `1 << 5' collides with LINEAR_B and
#  escaped all 25 rows, one character.  FIVE of the six partners escaped.  The offsets below
#  are CRIME_RE_TLB_A/B/C, TEX, LINEAR_A and LINEAR_B minus the handler's own
#  `relative_addr += 0x1000', so one row now pins every bit sgi_de could collide with. ***
t, alive, how = session(store(A, RE + 0x000, op=OP_SB_T0_A3, val="0x5a")
                        + store(A, RE + 0x200, op=OP_SB_T0_A3, val="0x5a")
                        + store(A, RE + 0x400, op=OP_SB_T0_A3, val="0x5a")
                        + store(A, RE + 0x600, op=OP_SB_T0_A3, val="0x5a")
                        + store(A, RE + 0x700, op=OP_SB_T0_A3, val="0x5a")
                        + store(A, RE + 0x780, op=OP_SB_T0_A3, val="0x5a")
                        + store(A, DE + 0x0d0, op=OP_SB_T0_A3, val="0x5a"), spin=1.8)
row("re_first", t.count(RE_DECL), 1, "#497's own latch fires first")
row("sharedlatch", t.count(DECL), 1,
    "sgi_de keeps its OWN bit -- sharing #497's silences this entirely")

n_ok = sum(1 for _, ok in rows if ok)
print("")
print("OPUS498T_CONTROL=%s" % ("OK" if rows and rows[0][1] and rows[1][1] else "DEAD"))
print("OPUS498T_RESULT=%d/%d" % (n_ok, len(rows)))
print("OPUS498T_DONE")
