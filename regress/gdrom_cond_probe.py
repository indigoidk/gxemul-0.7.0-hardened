#!/usr/bin/env python3
"""
#496 DETECTOR -- GD-ROM GDROM_UNKNOWN_0x88 and GDROM_COND bad-value declines.

Rung 3.  A real guest instruction through real address decode and real memory_rw on an
UNMODIFIED `-E dreamcast`.  Nothing is #included and nothing is called directly.

WHAT THIS DEFENDS.  Two guest-reachable host kills were de-fatalised in
src/devices/dev_dreamcast_gdrom.c:

    SITE A   GDROM_UNKNOWN_0x88 write, any value != 0x0b
    SITE B   GDROM_COND write, any value not in {0xa0, 0xef}

and -- at site B only -- `d->cond = idata;` MOVED from above the dispatch into the two
accepted arms.  That relocation is not cosmetic: COND_DATA_AVAIL (0x08) is a bit of
d->cond, and the GDROM_DATA read path is gated on it, so leaving the store above the
dispatch would let any declined value forge or revoke data-available.

*** THE SURVIVAL CHANNEL: DEAD ON THE ACCEPT SIDE, LOAD-BEARING ON THE DECLINE SIDE. ***

The fable5 seat named the first half on pass 1, before any table ran: post-fix an ACCEPTED
value exits 0 whether or not the guard is right, so carrying the witness's accept rows over
unchanged would ship the CHANNEL check's canonical vacuous row.  Those rows are therefore
NOT carried over; the accept side is pinned by EFFECT instead (R6, R8, R9, R10).

*** THE SECOND HALF WAS LEARNED THE HARD WAY ON PASS 2, AND STATING THE RULE TOO BROADLY
HAD ALREADY PUT A CLAUSE-(b) FLOOR BREACH IN THIS FILE. ***  A packet-fed seat, reasoning
from the diff alone, pointed out that a presence-only decline row cannot see `exit(1)` being
reinstated -- because the fatal() PRINTS AND THEN THE PROCESS DIES.  Count 1, byte correct,
row green, defect back.  The round's own witness had measured that shape pre-fix (`a88 says`
= 1 and `a88 kill` = exit1 in the same session) and nobody read the two rows together.

So: R1 and R2 assert announced AND survived.  A decline row that omits the exit status is
blind to the exact edit the round exists to prevent.

CLAUSE (e) -- THE CONTRACT.  A detector that says what it is designed to catch is
falsifiable; one claiming completeness is not.  This one is designed to catch:
    * reinstating exit(1) at either site                          (R1, R2)
    * a decline that stops carrying the guest's byte, INCLUDING
      a format-only change such as 0x%02x -> 0x%02d               (R1, R1b, R2, R2b)
    * dropping either latch, so a decline floods                  (R3, R4)
    * non-identity treatment of d->cond on a DECLINE -- restoring
      `= idata` above the dispatch, zeroing it, assigning a
      CONSTANT, or a value-conditional store.  Four pre-states,
      because one sample cannot tell a function from a constant
      and a spanning set cannot see a conjunction  (R5, R5b, R5c, R5d)
    * emptying either accepted arm                                (R6, R8, R9)
    * firing a completion event on a DECLINED write               (R7)
    * touching BUSY on a DECLINED write                           (R7b)
    * forging readiness so a later DATA READ finds data           (R12)
    * widening the accept set at its upper edge, including a
      value ABOVE the register's own width that TRUNCATES into
      it                                                          (R12b, R12c)
    * DELETING the fourth statement of the 0xa0 arm, which re-arms
      cmd_count and is the third leg of another site's
      unreachability warrant                                      (R13)
    * REPLACING that statement's VALUE rather than deleting it --
      a different edit with a different consequence               (R13)
    * growing an effect on, or declining, site A's 0x0b           (R10)
    * collapsing the two latch bits into one                      (R11)

It does NOT claim to observe anything on the DMA arms or the handle_command() decode.  A
later escape in those is OUTSIDE this contract, not a breach of it.

*** AND ONE DISCLOSURE THAT IS THE POINT OF HAVING A CONTRACT AT ALL, because it converts a
silent hole into a stated one. ***  The cond-readback rows are anchored at a FINITE SET of
declined inputs -- {0x00, 0x08, 0x09, 0x55, 0xaa, 0xff}.  A VALUE-CONDITIONAL store whose
predicate is false for every one of them survives every row here.

Two members of that family were found, from opposite directions, and BOTH are closed:
`idata >= 0x80` (closed by 0xaa) and `idata >= 0xef` (closed by 0xff).  A third, `>= 0xb0`,
was derived by a seat reviewing the 22-row version -- and the 0xff row added for the SECOND
finding kills it too, which is worth noticing rather than filing: **two seats reasoning from
different angles found one family, and one row covers all of it above 0xaa.**

*** THE THRESHOLD ACCOUNTING HERE WAS WRONG AND IS CORRECTED IN PLACE. ***  It claimed the
survivors were thresholds K strictly inside (0xaa, 0xff).  **They are not: R12b drives
0xff, which satisfies `idata >= K` for every such K, so that whole interval is covered.**
What survives is K ABOVE 0xff -- reachable because `idata` is the 64-bit datum from
memory_readmax64() while `d->cond` is a uint8_t, so a wide value passes the predicate and
TRUNCATES into the field.  R12c drives 0x0108 for exactly that.

What is left after R12c is a K above 0xffff (beyond a 16-bit store's reach here) or a
predicate keyed on something other than magnitude.  Those are DISCLOSED, not covered:
chasing every K is the unbounded shape this project has paid for once, and a
value-conditional forge triggering only outside the anchored set is OUT-OF-CONTRACT.

*** WHAT THE CONTRACT COST TO GET RIGHT, recorded because the first version was wrong. ***
Pass 2 measured three escapes through the 16-row form and all three are now closed above:
R5 alone admitted `d->cond = 0xef;` in the decline arm (green under the row, and it
fabricates COND_DATA_AVAIL from a fresh decline); site A's presence-only oracle admitted
the format mutant; and R5+R7 together admitted a busy/stat mutation.  The rows that close
them are R5b/R5c, R1b, and R7b.

*** DO NOT RE-NUMBER THE CITATIONS IN THIS FILE -- GREP FOR THEM. ***
    site A     grep -n 'only 0x0b is modelled'   src/devices/dev_dreamcast_gdrom.c
    site B     grep -n 'unimplemented GDROM_COND' src/devices/dev_dreamcast_gdrom.c

Sentinel: GDROMCOND_PROBE_DONE
"""

import os
import pty
import re
import select
import sys
import time

if len(sys.argv) < 3:
    sys.stderr.write("usage: gdrom_cond_probe.py <gxemul> <kernel>\n")
    sys.exit(2)

BIN = sys.argv[1]
KERNEL = sys.argv[2]

CODE = 0x8c001000

#  0x005f7000 + offset through the P2 uncached window.  DEVINIT(dreamcast_gdrom)
#  registers 0x005f7000 for 0x100 bytes; the offsets are the device file's own #defines.
GDROM_BUSY = 0xa05f7018
GDROM_DATA = 0xa05f7080
GDROM_UNK88 = 0xa05f7088        # Site A
GDROM_STAT = 0xa05f708c
GDROM_CNTLO = 0xa05f7090
GDROM_COND = 0xa05f709c         # Site B

#  SYSASIC_EVENT_TO_ADDR(SYSASIC_EVENT_GDROM) with SYSASIC_BASE 0x5f6900 and event 32:
#      0x5f6900 + 4*(32>>5) + 0  ==  0x5f6904          -> pending_irq[1]
#  SYSASIC_EVENT_TO_BITMASK(32) == 1 << (32 & 31) == 1 -> bit 0
#  Derived from src/include/thirdparty/dreamcast_sysasicvar.h, not assumed.
SYSASIC_PEND1 = 0xa05f6904
GDROM_EVENT_BIT = 0x1

IPRD_RESET = 0xda74
LIVE = 0x12345678
BRA_SELF = 0xaffe
NOP = 0x0009

#  The two decline texts.  BOTH leave the echoed byte as a capture, so a row can check the
#  diagnostic TRACKS the guest's datum rather than merely existing.
#
#  *** SITE A'S CAPTURE WAS ADDED ON PASS 2, AFTER A SEAT NAMED THE ESCAPE IT LEAVES. ***
#  The row used to count a plain substring, so `0x%02x` -> `0x%02d` in site A's format
#  string sailed through: a guest byte 0x55 is then reported as "85" and every presence,
#  latch and cross-bit row stays green.  A presence oracle cannot see a fidelity defect.
#
#  Anchored on `write of ... to` deliberately: the message ALSO contains the literal
#  "0x0b" in "only 0x0b is modelled", and an unanchored 0x([0-9a-f]{2}) would be free to
#  match that instead -- a row that reads a CONSTANT out of the message would be green
#  under the very mutant it exists to catch.
A88_TEXT = "only 0x0b is modelled"
A88_RE = re.compile(r"write of 0x([0-9a-f]{2}) to GDROM_UNKNOWN_0x88")
#  *** `+` NOT `{2}`, AND A SEAT HAD TO SAY SO. ***  The diagnostic prints with %02x, so a
#  value ABOVE the byte renders as `0x1ef` -- and `{2}` would capture "1e", silently
#  comparing the wrong thing on exactly the rows added to probe the high byte.
COND_RE = re.compile(r"unimplemented GDROM_COND = 0x([0-9a-f]+)")

rows = []


def row(name, got, want, note=""):
    ok = (got == want)
    rows.append((name, ok))
    print("%-14s %-12s %-12s %-46s %s" % (name, got, want, note,
                                          "ok" if ok else "FAIL"))
    return ok


def session(cmds, settle=8.0, spin=3.0):
    """Run one gxemul, feed debugger commands, return (transcript, alive, how)."""
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
    """The LAST `print rN` in the transcript -- a session with several reads of the same
    register must not silently score the first one."""
    m = re.findall(r"print\s+%s\s*\r?\n\s*(0x[0-9a-f]+)" % reg, t)
    return m[-1] if m else "absent"


def bit(t, reg, mask):
    """"set"/"clear" for one bit -- and "ABSENT" as its OWN token when the read failed.

    *** THIS FUNCTION EXISTS BECAUSE FOLDING A FAILED READ INTO "clear" MADE R7 FAIL OPEN.
    Caught on pass 2 by the fable5 seat. ***  R7's want is "clear", so a session that died
    before the load returned "absent" -> "clear" -> EQUAL TO WANT -> PASS.  The one row
    whose oracle is an ABSENCE was the one row an apparatus failure scored green.

    R6 and R9 want "set" and so fail safe on the same input, which is exactly why the
    defect was invisible: three rows share a helper and only the inverted one is unsafe.
    A row must fail to a DISTINGUISHABLE token or it manufactures agreement.
    """
    v = printed(t, reg)
    if v == "absent":
        return "ABSENT-READ-FAILED"
    #  *** AND THE SEED IS A NON-ANSWER TOO, which is the same defect one level down. ***
    #  0xdead has bit 3 set, so an UNEXECUTED load would score "set" -- green on R6 and R9,
    #  whose want IS "set".  Introducing the seed to make a dead read visible would have
    #  made it invisible again on exactly the two rows the "absent" guard already fails
    #  safe on.  A sentinel is only a sentinel if every consumer knows it is one.
    if int(v, 16) == SEED:
        return "SEED-NEVER-RAN"
    return "set" if (int(v, 16) & mask) else "clear"


def MOVW_ST(n, m):
    return 0x2001 | (n << 8) | (m << 4)     # mov.w Rm, @Rn


def MOVW_LD(n, m):
    return 0x6001 | (n << 8) | (m << 4)     # mov.w @Rm, Rn


class Addr(object):
    """Hands out non-overlapping code addresses so planted runs cannot collide."""

    def __init__(self, base):
        self.a = base

    def take(self, n_ops):
        got = self.a
        self.a += 2 * (n_ops + 2) + 0x20
        return got


def run(ops, at):
    put = ["put h 0x%x, 0x%04x" % (at + 2 * i, op) for i, op in enumerate(ops)]
    put += ["put h 0x%x, 0x%04x" % (at + 2 * len(ops), BRA_SELF),
            "put h 0x%x, 0x%04x" % (at + 2 * len(ops) + 2, NOP)]
    return put + ["pc=0x%x" % at, "step %d" % len(ops)]


def store16(reg, val, A):
    return ["r7=0x%x" % reg, "r8=0x%04x" % val] + run([MOVW_ST(7, 8)], A.take(1))


#  *** THE DESTINATION IS SEEDED 0xdead, NOT 0, AND THAT IS NOT COSMETIC. ***
#
#  Seeding 0 makes an UNEXECUTED LOAD indistinguishable from a load that genuinely read
#  zero -- and "RAM would read 0" is the exact failure every device-signature control here
#  exists to detect.  So under load, when a `step` does not complete, the row reads back its
#  own initialiser and reports the precise defect it was written to catch.
#
#  *** THE MOTIVATING DIAGNOSIS WAS WRONG AND THE SEED IS WHAT PROVED IT. ***  On this
#  probe's first run `devsig sh4` reported got=0x0 want=0xda74, with three agy jobs holding
#  ~10 concurrent gxemul processes, and I wrote it up as a contention artifact -- a step that
#  did not complete, leaving the register at its 0 initialiser.
#
#  It was not.  The row was simply WRONG (wrong address, wrong width -- see its own comment),
#  and it had been failing correctly the whole time.  **The seed settled it on the very next
#  run: a step that never executed would have left 0xdead, and it left 0x0, so the guest ran
#  and the device returned zero.**
#
#  The seed is kept, and its warrant is now the measured one rather than the guessed one: it
#  makes DID-NOT-RUN and READ-ZERO distinguishable, which is what let a wrong diagnosis be
#  refuted in one run instead of being carried. *A sentinel earns its keep by making you
#  wrong faster.*
#
#  0xdead cannot be produced by an unexecuted load, by RAM, or by any register this probe
#  reads, so the three states are now distinct: 0xdead = DID NOT RUN, 0x0 = read zero,
#  anything else = the value.  This is the harness's own distinguishable-token rule applied
#  to the seed rather than to the oracle.
SEED = 0xdead

#  operands as CORRECTED in gdrom_decline_probe.py: MOVW_LD(dest, 1) is `mov.w @R1, Rdest`.
#  Reversing them made three sibling rows pass vacuously, so this is COPIED, not re-derived.
def load16(reg, A, dest=2):
    return ["r1=0x%x" % reg, "r%d=0x%x" % (dest, SEED)] + run([MOVW_LD(dest, 1)], A.take(1)) \
        + ["print r%d" % dest]


def load32(reg, A, dest=2):
    return ["r1=0x%x" % reg, "r%d=0x%x" % (dest, SEED)] + run([0x6002 | (1 << 4) | (dest << 8)],
                                                              A.take(1)) + ["print r%d" % dest]


print("#496 gdromcondlies DETECTOR -- rung 3, unmodified -E dreamcast.")
print("binary: %s" % BIN)
print("")
print("%-14s %-12s %-12s %-46s %s" % ("row", "got", "want", "note", ""))

# ------------------------------------------------------------------ MANDATORY CONTROLS
#  Over the CONTROL ROWS ONLY.  A control that also goes dead on a product failure sends a
#  reader hunting a broken rig for a real defect -- measured on the sibling probe's first run.
A = Addr(CODE)
t, alive, how = session(["put w 0x8c001800, 0x%08x" % LIVE] + load32(0x8c001800, A))
row("live", printed(t, "r2"), "0x%x" % LIVE,
    "LIVENESS: guest store then guest load, through RAM")

#  *** COPIED VERBATIM FROM THE WITNESS, NOT RE-DERIVED, AND THE FIRST VERSION OF THIS ROW
#  WAS WRITTEN FROM MEMORY AND WAS WRONG. ***  It read `load16(0xa4000150)`; the real row is
#  a 32-BIT load from 0xffd00010 masked to 16 bits.  Wrong address AND wrong width, so it
#  read 0 -- and 0 is exactly what this control's own note says a RAM-backed window would
#  give, i.e. it reported the precise defect it exists to detect.
#
#  I diagnosed that as host contention and wrote that reason into this file.  It was not:
#  the SEED change (below) is what refuted it, because a step that never ran would have left
#  0xdead and it left 0x0.  The seed earned its keep on its first run, on a different
#  question from the one it was added for.
#
#  The general rule this file already states for citations applies to APPARATUS too: copy a
#  sibling's control, do not re-derive it.  `gdrom_decline_probe.py` and the witness both
#  carry this row; agreeing with them is the point, since the value of a shared control is
#  that a failure is comparable across probes rather than novel to this one.
A = Addr(CODE)
t, alive, how = session(load32(0xffd00010, A))
g = printed(t, "r2")
row("devsig sh4", ("0x%x" % (int(g, 16) & 0xffff)) if g.startswith("0x") else g,
    "0x%x" % IPRD_RESET, "DEVSIG: SH4 IPRD reset value; RAM would read 0")

A = Addr(CODE)
t, alive, how = session(load16(GDROM_STAT, A))
row("devsig st", printed(t, "r2"), "0x6",
    "DEVSIG: fresh GDROM_STAT = 6 (no IDE image); RAM = 0")

#  The STRONG device-signature form: a TRANSFORMATION only the device performs.  The write
#  arm masks CNTLO to a byte, so storing 0x1234 reads back 0x34.  RAM would return 0x1234
#  verbatim, so this discriminates against a RAM-backed window as well as a dead one.
A = Addr(CODE)
t, alive, how = session(store16(GDROM_CNTLO, 0x1234, A) + load16(GDROM_CNTLO, A))
row("devsig cnt", printed(t, "r2"), "0x34",
    "DEVSIG: device masks CNTLO to a byte; RAM gives 0x1234")

#  *** CONTROLS FIRST AND SEPARATELY. ***  A run whose controls died is an APPARATUS
#  failure and must not be read as a wall of product failures.  The gate keys on this line
#  BEFORE it looks at any score, so a broken rig reports as a broken rig.
print("GDROMCOND_CONTROL=%s" % ("OK" if all(o for _, o in rows) else "DEAD"))
print("")

# ------------------------------------------------------------------ R1, R3, R10  SITE A
#  R1 -- the decline is ANNOUNCED.  Kills a mutant that reinstates exit(1) (the process
#  would die and the text never appear) and one that declines SILENTLY.
#  *** THE EXIT STATUS IS PART OF THIS ROW, AND LEAVING IT OUT WAS A CLAUSE-(b) FLOOR
#  BREACH -- caught on pass 2 by a PACKET-FED seat reasoning from the diff alone. ***
#
#  The header's ban on the survival channel was written too broadly.  Reinstating `exit(1)`
#  after the fatal() PRINTS THE DIAGNOSTIC AND THEN DIES: the message count is 1, the byte
#  is right, and a presence-only row is GREEN on a verbatim reinstatement of the very defect
#  this round removed.  The witness measured exactly that shape pre-fix -- `a88 says` = 1
#  AND `a88 kill` = exit1, in the same session.
#
#  THE CORRECT RULE: survival is a dead channel for rows pinning the ACCEPT side, because
#  the fix makes accepted values survive either way.  On the DECLINE side it is the ONLY
#  channel that sees clause (b).  So a decline row asserts BOTH -- announced, and survived.
A = Addr(CODE)
t, alive, how = session(store16(GDROM_UNK88, 0x0000, A))
m = A88_RE.search(t)
row("R1 a88 says", "%d|%s|%s" % (t.count(A88_TEXT), m.group(1) if m else "absent", how),
    "1|00|exit0", "site A declines, announces the byte, and SURVIVES")

#  R1b -- and the byte TRACKS.  A second, DIFFERENT declined value is what separates a
#  format that prints idata from one that prints a constant, and it is what reddens under
#  the 0x%02x -> 0x%02d fidelity mutant (0xaa would report as "70").
A = Addr(CODE)
t, alive, how = session(store16(GDROM_UNK88, 0x00aa, A))
m = A88_RE.search(t)
row("R1b a88 trk", m.group(1) if m else "absent", "aa",
    "and it tracks the datum, so the predicate saw it")

#  R3 -- the LATCH.  Three bad writes in ONE session must announce exactly once.
A = Addr(CODE)
t, alive, how = session(store16(GDROM_UNK88, 0x0000, A)
                        + store16(GDROM_UNK88, 0x0055, A)
                        + store16(GDROM_UNK88, 0x00aa, A))
row("R3 a88 x3", "%d" % t.count(A88_TEXT), "1",
    "three bad writes at A, ONE diagnostic")

#  R10 -- site A's accepted value is a NO-OP.  If a future edit gives 0x0b an effect, the
#  three device-state bytes stop agreeing with a fresh device.
#  *** R10 READS COND AND BUSY, NOT STAT, AND THE STAT VERSION WAS HOLLOW. ***
#  PRETABLE prescribed "stat/busy/cond unchanged"; the first build read STAT alone -- and
#  `dreamcast_gdrom_update_stat()` RECOMPUTES d->stat on every read, so it normalises to 6
#  whatever site A did.  A mutant adding `d->cond = 0x08;` to the 0x0b arm therefore passed
#  R10 while forging COND_DATA_AVAIL: the row aimed at "site A grew an effect" could not see
#  site A growing an effect.
#
#  That is #490's lost-prescription failure in miniature -- the row list drifted from the
#  block that prescribed it -- caught pre-commit by the fable5 seat rather than by a mutant.
#  The STAT leg is dropped rather than added to: `devsig st` already pins it, and a leg that
#  cannot vary is what made this row hollow in the first place.
A = Addr(CODE)
t, alive, how = session(store16(GDROM_UNK88, 0x000b, A)
                        + load16(GDROM_COND, A, dest=2)
                        + load16(GDROM_BUSY, A, dest=3))
row("R10 a88 nop", "%s|%s|%d" % (printed(t, "r2"), printed(t, "r3"), t.count(A88_TEXT)),
    "0x0|0x0|0", "accepting 0x0b touches no state and says nothing")

# --------------------------------- R10b/R10c  SITE A HAS A STATE CHANNEL TOO
#  *** SIBLING PARITY FAILED THREE TIMES IN ONE ROUND, AND THE THIRD FAILURE IS INSIDE
#  THE REPAIR FOR THE SECOND. ***  The first was byte fidelity (site B captured its byte,
#  site A did not).  The second was the end-to-end consequence, and R12 was written for
#  it AT SITE B ONLY.  The third is this: **every repair this round made to close a
#  site-B gap was made at site B alone**, so until now NO ROW READ ANY DEVICE REGISTER
#  AFTER A SITE-A ACCESS.  Site A was observed by nothing but its own message.
#
#  Three mutants were MEASURED sweeping the whole detector through that hole, each a
#  one-line edit in site A:
#      d->cond |=  0x08;   in the DECLINE arm  -- forges readiness      (21/21 clean)
#      d->cond &= ~0x08;   in the DECLINE arm  -- revokes a genuine one (21/21 clean)
#      SYSASIC_TRIGGER_EVENT on the ACCEPTED 0x0b -- a phantom completion
#
#  R10 could not see any of them: it reads COND and BUSY after ACCEPTING 0x0b, and all
#  three act on the DECLINE path or on a channel it does not read.
#
#  *** THE REVIEWER CHECK THIS EARNS, and it costs two seconds: when a repair closes a
#  gap at one site of a pair, ASK WHAT THE SAME EDIT WOULD DO AT THE OTHER. ***  Three
#  times the answer here was "nothing would notice".
A = Addr(CODE)
t, alive, how = session(store16(GDROM_UNK88, 0x0055, A)
                        + load16(GDROM_COND, A, dest=2)
                        + load32(SYSASIC_PEND1, A, dest=3))
row("R10b a88 decl", "%s|%s|%d" % (printed(t, "r2"),
                                   bit(t, "r3", GDROM_EVENT_BIT),
                                   t.count(A88_TEXT)),
    "0x0|clear|1", "a DECLINED site-A write touches COND and the event NOT AT ALL")

#  and the ACCEPTED value must not grow an event either -- the third mutant acts on the
#  0x0b path, which R10 reads but only through COND and BUSY.
A = Addr(CODE)
t, alive, how = session(store16(GDROM_UNK88, 0x000b, A)
                        + load32(SYSASIC_PEND1, A, dest=2))
row("R10c a88 evt", bit(t, "r2", GDROM_EVENT_BIT), "clear",
    "and ACCEPTING 0x0b fires no completion event")

# ------------------------------------------------------------------ R2, R4  SITE B
#  R2 -- announced, and the echoed byte TRACKS the guest's datum.  A constant would prove
#  far less: it would survive a mutant that stopped reading idata at all.
A = Addr(CODE)
t, alive, how = session(store16(GDROM_COND, 0x0055, A))
m = COND_RE.search(t)
row("R2 cond says", "%s|%s" % (m.group(1) if m else "absent", how), "55|exit0",
    "site B declines, announces the byte, and SURVIVES")

A = Addr(CODE)
t, alive, how = session(store16(GDROM_COND, 0x0001, A))
m = COND_RE.search(t)
row("R2b cond trk", m.group(1) if m else "absent", "01",
    "and it tracks the datum, so the predicate saw it")

#  R4 -- the LATCH at site B.
A = Addr(CODE)
t, alive, how = session(store16(GDROM_COND, 0x0055, A)
                        + store16(GDROM_COND, 0x0056, A)
                        + store16(GDROM_COND, 0x0057, A))
row("R4 cond x3", "%d" % len(COND_RE.findall(t)), "1",
    "three bad writes at B, ONE diagnostic")

# ------------------------------------------------------------------ R5  *** THE KEYSTONE
#  *** ANCHORED, AND THE ANCHOR IS THE WHOLE POINT (clause f). ***
#  A fresh device has cond == 0.  So the naive row -- "write 0x55, read back 0" -- is
#  satisfied by the CORRECT fix and ALSO by a mutant that assigns d->cond = 0 on decline.
#  Driving an ACCEPTED 0xef FIRST puts a value in cond that only the accept arm can have
#  placed there; requiring 0xef back after the declined write separates the two.
#
#  This is the row that kills the clause-(d) mutant BOTH Agent seats named independently on
#  pass 1: keep the latched decline, move `d->cond = idata;` back above the dispatch.  Under
#  that mutant this reads 0x55.  Every other row in this file stays green.
A = Addr(CODE)
t, alive, how = session(store16(GDROM_COND, 0x00ef, A)
                        + store16(GDROM_COND, 0x0055, A)
                        + load16(GDROM_COND, A))
row("R5 cond keep", printed(t, "r2"), "0xef",
    "*** ANCHORED: declined write leaves d->cond UNCHANGED")

#  *** ONE ANCHOR IS NOT ENOUGH, AND A SEAT MEASURED WHY ON PASS 2. ***
#  R5 alone pins "cond == 0xef after the sequence", which the CORRECT fix satisfies and so
#  does a one-line mutant `d->cond = 0xef;` in the decline arm.  That mutant fabricates
#  COND_DATA_AVAIL (0xef & 0x08) out of a fresh or 0xa0-anchored decline and unlocks the
#  GDROM_DATA read path -- the exact defect R5 exists to prevent, walking straight past it.
#
#  THE REPAIR IS PRE-STATES, NOT MORE ROWS OF THE SAME SHAPE.  "Unchanged" is a claim about
#  a FUNCTION of the prior value, and one sample cannot distinguish a function from a
#  constant.  Three samples over the model's principal reachable states pin it: any
#  constant, any zeroing, any OR, and idata itself all differ from the identity on at least
#  one of them.
#  *** THE DECLINED BYTE HERE IS 0xaa, NOT 0x55, AND THE CHANGE IS ONE CONSTANT THAT CLOSES
#  A MEASURED ESCAPE. ***  With 0x55 the three declined values were {0x55, 0x55, 0x08},
#  whose union is 0x5d -- so BITS 1, 5 AND 7 APPEARED IN NO PROBED VALUE, and R5/R5b/R5c
#  were blind to any VALUE-CONDITIONAL store keyed on them.  The opus5 seat built one and
#  measured all 20 rows identical to the fix tree:
#
#      +		if (idata >= 0x80)
#      +			d->cond = idata;
#
#  Its plausible dress writes itself -- "0xa0 and 0xef are both >= 0x80, so high bytes are
#  command codes; let them land" -- and a declined 0x88 then stores 0x88, whose bit 3 FORGES
#  COND_DATA_AVAIL: the exact defect the store relocation exists to prevent.
#
#  {0x55, 0xaa, 0x08} spans all eight bits, so no conditional keyed on any single bit can
#  pass all three.  The three rows now test the map on a spanning set rather than on an
#  arbitrary one.  *Zero new rows; the cost of the original hole was that nobody asked which
#  bits the probed values covered.*
A = Addr(CODE)
t, alive, how = session(store16(GDROM_COND, 0x00aa, A) + load16(GDROM_COND, A))
row("R5b cond 00", printed(t, "r2"), "0x0",
    "FRESH pre-state: decline leaves cond at its reset 0")

A = Addr(CODE)
#  the declined byte here is 0x08 -- COND_DATA_AVAIL itself -- so the row MEASURES the
#  forge subspace instead of inferring it: any mutant that stores or ORs the declined
#  value lands data-available on top of an accepted 0xa0, and this reds.
t, alive, how = session(store16(GDROM_COND, 0x00a0, A)
                        + store16(GDROM_COND, 0x0008, A)
                        + load16(GDROM_COND, A))
row("R5c cond a0", printed(t, "r2"), "0xa0",
    "0xa0 pre-state: decline preserves the ACCEPTED value")

#  *** SPANNING THE BITS KILLS SINGLE-BIT PREDICATES AND NOT CONJUNCTIONS.  Named by the
#  codex seat AFTER the spanning repair had already landed -- which is the useful shape of a
#  finding: accept the repair, then ask what it does NOT buy. ***
#
#  The three declined bytes {0x55, 0xaa, 0x08} union to 0xff, so no SINGLE-bit conditional
#  can pass all three.  A CONJUNCTION can:
#
#      if ((idata & 0x09) == 0x09)
#              d->cond = idata;
#
#  0x55 carries bit 0 and not bit 3; 0xaa and 0x08 carry bit 3 and not bit 0.  **NOT ONE OF
#  THE THREE HAS BOTH**, so every existing row stays green while a declined 0x09 stores 0x09
#  and forges COND_DATA_AVAIL.  0x09 is the smallest value carrying the readiness bit
#  together with a bit no other probed value pairs it with.
#
#  HONEST BOUND, because a spanning argument invites exactly this overclaim: this closes
#  two-bit conjunctions involving bit 3.  It does not close the general k-bit case, and the
#  contract covers every unmodelled value while four samples do not.  Stated rather than
#  implied.
A = Addr(CODE)
t, alive, how = session(store16(GDROM_COND, 0x00ef, A)
                        + store16(GDROM_COND, 0x0009, A)
                        + load16(GDROM_COND, A))
#  THE 09 ANNOUNCEMENT IS IN THE ORACLE because without it this row is store-death-unsafe:
#  if the 0x09 store is missed while the ANCHOR and the LOAD both run, the read still
#  returns 0xef and the row passes having observed nothing.  Named by a seat as an eighth
#  `storesidedead` member -- the class applies to a row that drives TWO stores whenever
#  only one of them is load-bearing.
m = COND_RE.search(t)
#  *** AND THE MUTANT THIS ROW USED TO NAME IS ONE R12b ALREADY SUBSUMES.  Corrected
#  2026-08-30 by the adjudicating seat, which checked rather than agreed. ***
#
#  The stated mutant was a conjunction `(idata & 0x09) == 0x09`.  R12b drives 0xff, and
#  0xff passes EVERY `(idata & M) == M` -- so R12b kills that form on its own and this
#  row adds nothing against it.  A row is justified by a mutant no OTHER row catches,
#  and citing a subsumed one overstates the suite while looking like coverage.
#
#  THE DISCRIMINATING FORM IS AN EXACT LOW-NIBBLE MATCH, `(idata & 0x0f) == 0x09`:
#      0xff -> 0x0f != 0x09   R12b stays GREEN and misses it
#      0x09 -> forges cond=0x09, and this row reds on field 1 (0x9 != 0xef)
#  So R5d earns its place -- on that mutant, not on the one it used to claim.
#
#  LATENT FRAGILITY, worth stating because it is invisible from the row: field 2 works
#  ONLY while 0xef stays an ACCEPTED value.  The device announces nothing for 0xef, so
#  the sole COND_RE match is the 0x09 decline.  If a future round moved 0xef to the
#  declined side, field 2 STOPS OBSERVING THE 0x09 DECLINE and starts observing
#  whatever the anchor's own decline printed instead.  The row reds -- loudly, which is
#  the safe direction -- but for a reason unrelated to the rule under test, so whoever
#  sees it should read this note before re-pinning.
#
#  *** AN EARLIER DRAFT OF THIS NOTE PREDICTED THE OBSERVABLE AND GOT IT WRONG, WHICH
#  IS WHY IT NO LONGER PREDICTS ONE. ***  It said field 2 would read "absent".  It
#  would not: the anchor's decline goes through the SAME else arm and prints
#  `unimplemented GDROM_COND = 0xef ... (once)`, and COND_RE.search returns the FIRST
#  match -- so field 2 reads "ef".  (And if a future decline used different text, the
#  0x09 latch would be unconsumed and field 2 would read "09" with field 1 red
#  instead.)  Caught by the adjudicating seat.  The DIRECTION was right and the
#  mechanism was wrong -- which is `read the line before citing it`, inside a
#  correction written to fix an overclaim.
row("R5d cond 09", "%s|%s" % (printed(t, "r2"), m.group(1) if m else "absent"),
    "0xef|09", "a decline carrying BOTH bits 0 and 3 is refused too")

# ------------------------------------------------------------------ R6, R8, R9  ACCEPTS
#  These are the de-escalation ACCEPT rows.  They pin that legal writes still LAND -- which
#  is the clause's own wording -- and landing means the EFFECT, not the silence.  A quiet
#  row cannot see an emptied arm; these can.
A = Addr(CODE)
t, alive, how = session(store16(GDROM_COND, 0x00a0, A) + load16(GDROM_BUSY, A))
row("R6 a0 busy", bit(t, "r2", 0x08), "set",
    "ACCEPT 0xa0 still sets BUSY bit 0x08")

A = Addr(CODE)
t, alive, how = session(store16(GDROM_COND, 0x00a0, A) + load16(GDROM_COND, A))
row("R8 a0 echo", printed(t, "r2"), "0xa0",
    "ACCEPT 0xa0 still stores idata into d->cond")

A = Addr(CODE)
t, alive, how = session(store16(GDROM_COND, 0x00ef, A) + load32(SYSASIC_PEND1, A))
row("R9 ef event", bit(t, "r2", GDROM_EVENT_BIT), "set",
    "ACCEPT 0xef still fires the SYSASIC event")

# ------------------------------------------------------------------ R7  NO EVENT ON DECLINE
#  *** THE TWO IN-FILE PRECEDENTS DISAGREE, so the choice is PINNED rather than assumed. ***
#  handle_command()'s default arm FIRES a completion event on decline, because a guest that
#  has SENT a packet is waiting on one.  The DMA arm REFUSES one, because a completion on a
#  declined transfer is a false success.  At GDROM_COND the guest has sent no packet and is
#  polling BUSY, so an event would announce a command that never began.
#
#  This row is the CLAIM->ROW discharge for that comment sentence.  It is a counterfactual
#  "would <consequence>" claim, which the five-verb grep form of the check walks straight
#  past -- the trigger is semantic: does the sentence assert something a row could observe?
A = Addr(CODE)
t, alive, how = session(store16(GDROM_COND, 0x0055, A) + load32(SYSASIC_PEND1, A))
row("R7 no event", bit(t, "r2", GDROM_EVENT_BIT), "clear",
    "a DECLINED COND write fires NO completion event")

#  R7b -- and it touches NO OTHER command state either.  R5/R5b/R5c pin `cond` and R7 pins
#  the event; without this row a one-line busy/stat mutation in the decline arm passes both.
#  The comment this discharges says the decline "accepted no new command or packet ... any
#  pre-existing command state is left untouched" -- a counterfactual claim about state, and
#  CLAIM->ROW owes it a row whatever verbs it happens to use.
#
#  BUSY is read-only here on purpose: its write arm is `d->busy &= ~idata` -- WRITE-TO-CLEAR
#  -- so a probe that "initialises" busy by writing it CLEARS bits instead of setting them.
#  BEFORE/AFTER, not an absolute.  Writing "want 0x0|0x6" here would mean reading the fresh
#  values off the binary and pinning them -- which is fitting the test to the answer, and is
#  observationally identical to laundering.  Comparing the pair ACROSS the decline states
#  the actual claim ("unchanged") and needs no knowledge of what the values are.
A = Addr(CODE)
t, alive, how = session(load16(GDROM_BUSY, A, dest=2)
                        + load16(GDROM_STAT, A, dest=3)
                        + store16(GDROM_COND, 0x0055, A)
                        + load16(GDROM_BUSY, A, dest=4)
                        + load16(GDROM_STAT, A, dest=5))
before = "%s|%s" % (printed(t, "r2"), printed(t, "r3"))
after = "%s|%s" % (printed(t, "r4"), printed(t, "r5"))
#  *** A SELF-COMPARING ROW MUST NOT BE ABLE TO PASS ON NOTHING. ***  If the apparatus
#  fails, all four reads return "absent", after == before, and the row goes GREEN having
#  observed nothing whatever -- the check-that-cannot-fail shape, arriving by way of an
#  otherwise correct before/after oracle.  Any "absent" is forced to a value that cannot
#  equal the other side, so an apparatus failure reds instead of passing.
if "absent" in before or "absent" in after or "0x%x" % SEED in before + after:
    before = "READ-FAILED " + before
row("R7b cond st", after, before,
    "and BUSY/STAT are UNCHANGED across the decline")

# ------------------------------------------------------------------ R11  THE CROSS-BIT ROW
#  *** d->warned IS SHARED.  THE COUNT NAMES ITS DERIVER, because every carried version of
#  it in this round's artifacts was wrong: ***
#
#      grep -c 'd->warned |=' src/devices/dev_dreamcast_gdrom.c   ->  12 RAW
#      ... minus ONE that is inside a comment block               ->  11 LIVE writers
#      of which, inside a DEVICE_ACCESS                           ->   8
#
#  (Pre-round: 10 raw, 9 live, 6 inside.)  An earlier draft of this comment said "ten sites,
#  six inside" -- #490's numbers plus two, with #490's own additions never folded in.  The
#  raw grep is the same comment-contamination that `exit_census.py` exists to defeat.
#
#  Not all eight are guest register READS -- GDROM_W_NOTWAIT, GDROM_W_DMANODATA and
#  GDROM_W_DMAARM are write-triggered.  The hazard is unchanged and if anything broader:
#  ordinary guest traffic of EITHER direction can pre-set a colliding bit.  A latch-bit
#  collision is therefore SILENCED BY BENIGN TRAFFIC and looks exactly like a working
#  latch.  #490's `M3shared` escape is this file's recorded cost of shipping without a row
#  for it.
#  *** THE SESSION OPENS WITH AN ORDINARY GDROM_DATA READ, AND THAT ONE COMMAND IS WHAT
#  MAKES THIS ROW MEET #490's STANDARD RATHER THAN A WEAKER ONE. ***
#
#  Without it the row kills only NEW-vs-NEW collapse -- the two new bits aliased onto each
#  other.  It cannot see either new bit aliased onto an OLD one, which compiles clean: the
#  disjointness assert polices the DEFINE level, and an alias written at the USE SITE
#  (testing and setting GDROM_W_NODATA's bit inside site A's guard) never reaches it.
#
#  A GDROM_DATA read ARMS GDROM_W_NODATA inside DEVICE_ACCESS, so if either new latch is
#  aliased onto it, that site falls silent and the row reds.  It touches neither d->cond nor
#  either diagnostic pattern, so it costs the row nothing.  This is the "most benign traffic
#  instance MEASURED" standard `gdrom_decline_probe.py` records #490 arriving at after its
#  own crossbit claim "overclaimed by a factor of seven".
#
#  DISCLOSED, because the contract must claim what it measured and no more: this stages ONE
#  old bit.  Aliases onto the other old bits are NOT covered, and a full alias sweep is not
#  attempted here.
A = Addr(CODE)
t, alive, how = session(load16(GDROM_DATA, A, dest=6)
                        + store16(GDROM_UNK88, 0x0000, A)
                        + store16(GDROM_COND, 0x0055, A))
row("R11 crossbit", "%d|%d" % (t.count(A88_TEXT), len(COND_RE.findall(t))), "1|1",
    "both announce AFTER benign traffic armed an old bit")

# ------------------------------------------------ R12  THE END-TO-END CONSEQUENCE
#  *** EVERY OTHER ROW PINS THE CAUSE; THIS ONE PINS THE EFFECT. ***  Named in the
#  adjudication pass by a PACKET-FED seat as the thing all nine of us missed: the probe
#  checked the decline and the COND readback, and never exercised the READ PATH the whole
#  fix exists to protect.
#
#  The declined byte is 0x08 -- COND_DATA_AVAIL itself.  Under the shipped fix d->cond is
#  untouched, so the DATA read finds readiness clear and announces "no data available".
#  Under any mutant that lets the declined value reach d->cond, readiness is FORGED, the
#  read takes the payload branch instead, and the diagnostic never appears.
#
#  *** IT KEYS ON THE DIAGNOSTIC, NOT ON THE RETURNED VALUE, AND THE DEVICE FILE SAYS WHY
#  IN SO MANY WORDS: *** the no-data path returns 0xffff, and "this device's TOC is
#  memset(0xff), so 0xffff is LEGITIMATE PAYLOAD here and no returned value is
#  self-identifying.  The DIAGNOSTIC is the truthfulness channel, not the value."  A row
#  written against the value would be green under a mutant that forges readiness onto a TOC.
#
#  This discharges a CLAIM->ROW debt the round had missed: the fix's own comment asserts a
#  declined write could "forge data-available ... or revoke a genuine one", which is a
#  consequence claim about the DATA path, and until now no row observed that path at all.
NODATA_TEXT = "read from GDROM_DATA with no data available"
A = Addr(CODE)
t, alive, how = session(store16(GDROM_COND, 0x0008, A) + load16(GDROM_DATA, A))
#  *** THE NODATA TOKEN ALONE IS NOT AN EXECUTION WITNESS, AND TWO SEATS SAID SO AGAINST A
#  THIRD THAT CALLED THIS ROW SAFE. ***  It IS a positive observable -- but it is produced by
#  the FRESH STATE as well: cond is 0 on a fresh device, so if the declining store never
#  executes, the DATA read still finds no data and still announces.  The row would be green
#  having observed nothing.
#
#  So the refined rule is not "wants a positive observable" but **wants an observable ONLY
#  THE STORE CAN PRODUCE**.  The COND decline announcement is one: it cannot appear unless the
#  guest store reached the device handler and was refused there.  Asserting both makes the row
#  say "the store ran, AND it did not unlock the path" -- two claims, one session.
m = COND_RE.search(t)
row("R12 no forge", "%d|%s" % (t.count(NODATA_TEXT), m.group(1) if m else "absent"),
    "1|08", "a DECLINED 0x08 does NOT unlock the DATA read path")

# ------------------------------------------- R12b  THE ACCEPT SET HAS AN UPPER EDGE TOO
#  *** ONE CHARACTER SWEEPS EVERY OTHER ROW IN THIS FILE, AND IT IS AN EQUALITY BECOMING AN
#  INEQUALITY -- the shape a careless edit produces most easily. ***  Predicted by the codex
#  seat from the diff alone:
#
#      -   } else if (idata == 0xef) {
#      +   } else if (idata >= 0xef) {
#
#  Every probed value behaves identically: 0xa0 still takes the first arm, 0xef still takes
#  the second, and every declined value this file drives (0x55, 0xaa, 0x08, 0x09, 0x00) is
#  BELOW 0xef.  So the accept set silently grows an upper tail -- and 0xff then stores 0xff
#  into cond, forging COND_DATA_AVAIL, *and* fires a completion event for a command that was
#  never issued.  Both halves of the defect this round exists to prevent, from one keystroke.
#
#  The row drives 0xff and requires the DECLINE: the diagnostic present, cond unchanged from
#  an anchored 0xa0, and no ASIC event.  **Three channels in one row on purpose** -- the
#  mutant's two consequences land on different ones, and a row that watched only cond would
#  miss the forged event while a row that watched only the event would miss the forged
#  readiness.
#
#  This is the ACCEPT SET's boundary rather than the store's identity, so it is not covered
#  by R5* however many pre-states those grow: they all drive values the mutant still
#  declines.
A = Addr(CODE)
t, alive, how = session(store16(GDROM_COND, 0x00a0, A)
                        + store16(GDROM_COND, 0x00ff, A)
                        + load16(GDROM_COND, A, dest=2)
                        + load32(SYSASIC_PEND1, A, dest=3))
m = COND_RE.search(t)
row("R12b cond ff", "%s|%s|%s" % (m.group(1) if m else "absent",
                                  printed(t, "r2"),
                                  bit(t, "r3", GDROM_EVENT_BIT)),
    "ff|0xa0|clear", "0xff is DECLINED: no store, no event, announced")

# ------------------------------------------------- R12c  ABOVE THE BYTE, AND IT TRUNCATES
#  *** MY CONTRACT'S THRESHOLD ACCOUNTING WAS WRONG AND A SEAT REFUTED IT WITH ARITHMETIC. ***
#  It claimed the surviving thresholds are those strictly inside (0xaa, 0xff).  They are not:
#  R12b drives 0xff, which satisfies `idata >= K` for EVERY K in that range, so the whole
#  interval is already covered.
#
#  What survives is ABOVE 0xff -- and it survives for a reason no row was watching:
#
#      `idata` comes from memory_readmax64() and is 64-BIT.
#      `d->cond` is uint8_t.
#
#  So `if (idata >= 0x100) d->cond = idata;` is declined for every value this file drove --
#  all of them fit in a byte -- while a guest 16-bit store of 0x0108 gives idata = 0x108,
#  passes the guard, and **TRUNCATES INTO cond AS 0x08, forging COND_DATA_AVAIL.**  The
#  forging value never appears in the store; it is manufactured by the assignment's width.
#
#  This row drives exactly that: a 16-bit store of 0x0108, anchored over an accepted 0xa0.
#  *A value-conditional forge does not have to be reachable within the register's own width
#  -- the predicate sees the WIDE datum and the field keeps the narrow one.*
A = Addr(CODE)
t, alive, how = session(store16(GDROM_COND, 0x00a0, A)
                        + store16(GDROM_COND, 0x0108, A)
                        + load16(GDROM_COND, A))
row("R12c cond 108", printed(t, "r2"), "0xa0",
    "a decline ABOVE the byte cannot truncate into cond")

# ------------------------------------- R12d  THE AXIS NOBODY SAMPLED: THE HIGH BYTE
#  *** MEASURED L2 FLOOR BREACH.  `if ((idata & 0xff) == 0xa0)` -- and the same on the
#  0xef arm -- SCORED 24/24 WITH ZERO FAILING ROWS, while a guest store of 0x01ef fired a
#  COMPLETION EVENT FOR A COMMAND NEVER ISSUED and 0x01a0 armed BUSY, both SILENTLY. ***
#
#  Why nothing saw it, derived rather than guessed:
#
#      grep -o 'GDROM_COND, 0x[0-9a-f]*' gdrom_cond_probe.py | sort -u
#      -> 0001 0008 0009 0055 0056 0057 00a0 00aa 00ef 00ff
#
#  **Ten distinct values and EVERY ONE IS 0x00xx.**  The samples span all eight bits of
#  the LOW byte -- three separate repairs saw to that -- and the entire high byte was
#  never varied.  So a predicate that moves into the unsampled dimension is invisible to
#  all of them, however many low-byte values are added.
#
#  *** THE GENERAL LESSON, WHICH IS WHY THIS ROW EXISTS RATHER THAN A FOURTH LOW-BYTE
#  SAMPLE: THREE POINT SAMPLES CANNOT DISCHARGE A FAMILY. ***  For any finite declined set
#  S, a predicate keyed on a DIMENSION S does not vary escapes it.  Each earlier repair
#  added samples along the axis the previous escape used; this one changes axis.
#
#  The mutant is plausibly dressed -- `d->cond` IS a uint8_t, so "mask to the register
#  width" reads like a robustness fix, which is exactly the shape clause (d) asks for.
#
#  Three channels in one session, because the mutant has two distinct harms: the value
#  must not land, the event must not fire, and the decline must still be announced.
A = Addr(CODE)
t, alive, how = session(store16(GDROM_COND, 0x00a0, A)
                        + store16(GDROM_COND, 0x01ef, A)
                        + load16(GDROM_COND, A, dest=2)
                        + load32(SYSASIC_PEND1, A, dest=3))
m = COND_RE.search(t)
row("R12d hi byte", "%s|%s|%s" % (m.group(1) if m else "absent",
                                  printed(t, "r2"),
                                  bit(t, "r3", GDROM_EVENT_BIT)),
    "1ef|0xa0|clear", "0x01ef is DECLINED: the HIGH byte is not ignored")

# ------------------------------------------ R13  THE FOURTH STATEMENT OF THE ACCEPTED ARM
#  *** THE 0xa0 ARM HAS FOUR STATEMENTS AND THIS DETECTOR PINNED TWO.  MEASURED ESCAPE,
#  BUILT AND RUN BY THE opus5 SEAT: deleting `d->cmd_count = 0;` leaves all twenty other
#  rows BYTE-IDENTICAL while restoring a guest-reachable HOST KILL. ***
#
#  R6 reads `d->busy & 0x08` and R8 reads `d->cond`; the mutant touches neither.  The two
#  rows that ought to have caught it cannot, by construction.
#
#  WHY THE LINE IS LOAD-BEARING, and it is not this device's own arm that dies.  The
#  GDROM_DATA *write* arm still holds a live exit(1) -- `fatal("Too much GDROM_DATA?")` --
#  and it is documented UNREACHABLE on a three-leg warrant: cmd_count steps by 2, the == 12
#  equality clears busy at the boundary, and **0xa0 resets it**.  THE THIRD LEG IS THIS
#  LINE.  Delete it and the attack is `0xa0` -> six DATA words -> `0xa0` -> one DATA word,
#  which is any guest issuing two GD-ROM commands in a row; the host dies on the first data
#  write of the second command.  Measured: attack probe 5/5 exit0 on the fix tree, 3/5
#  exit1 on the mutant, with an attribution control (same traffic, no re-arm) green on both.
#
#  *** AND IT IS A CONTRACT BREACH, NOT AN OUT-OF-CONTRACT ESCAPE. ***  Clause (e) claims
#  "emptying either accepted arm (R6, R8, R9)".  The contract disclaims the GDROM_DATA READ
#  path; this consequence lands in the WRITE path.
#
#  *** AND `PRETABLE.out` ENUMERATED `d->cmd_count` BY NAME AS A SITE-B BODY FIELD, TWICE,
#  AND THEN NO ROW WAS WRITTEN. ***  That is #490's lost-prescription failure occurring in
#  the very artifact that exists to prevent it, two sections after it says so.
#
#  The oracle is the absence of the kill, on a LATER access whose outcome depends on state
#  the accepted arm set -- so it does not reach for the accept-side survival channel the
#  header bans.  It doubles as the carrier for `gdromexitsix`'s absence record, whose
#  warrant this round's diff edited without re-running the death measurement.
TOOMUCH_TEXT = "Too much GDROM_DATA?"
A = Addr(CODE)
t, alive, how = session(store16(GDROM_COND, 0x00a0, A)
                        + store16(GDROM_DATA, 0x1111, A)
                        + store16(GDROM_DATA, 0x2222, A)
                        + store16(GDROM_DATA, 0x3333, A)
                        + store16(GDROM_DATA, 0x4444, A)
                        + store16(GDROM_DATA, 0x5555, A)
                        + store16(GDROM_DATA, 0x6666, A)
                        + store16(GDROM_COND, 0x00a0, A)
                        + store16(GDROM_DATA, 0x7777, A))
#  *** R13's WANT IS A NULL OUTCOME, AND A NULL OUTCOME IS WHAT A DEAD SESSION PRODUCES. ***
#  `0|exit0` -- no kill token, host alive -- is BIT-IDENTICAL to a run in which none of these
#  nine stores executed at all.  That is the `storesidedead` class, and this row drives more
#  stores than any other, so it has the most ways to die silently: *a row that drives a longer
#  sequence has MORE ways to die quietly, not fewer*, which inverts the intuition that a
#  richer row is a stronger row.
#
#  THE EXECUTION WITNESS COSTS NOTHING AND WAS FOUND BY A SEAT LOOKING FOR IT.  The sixth
#  DATA word completes the 12-byte packet and DISPATCHES: `cmd[0]` is 0x11 (the low byte of
#  0x1111), which no case implements, so `handle_command()`'s latched default arm announces
#  `[ dreamcast_gdrom: handle_command: unimplemented command 0x11 -- declined.  (once) ]`.
#
#  **That token fires on the correct build AND on the mutant** -- it comes from word 6, and
#  the mutant's kill lands on word 7 -- so folding it in converts R13's want from a NULL
#  outcome to a POSITIVE OBSERVABLE without weakening the kill.  A session whose stores never
#  ran cannot produce it.
#
#  *THE GENERAL DISCRIMINATOR, which is better than the row enumeration the filed class
#  carries: a row wanting a POSITIVE observable is store-death-safe; a row wanting a NULL
#  outcome is not.*  The one refinement is that the positive observable must be one only the
#  STORE can produce -- R12's no-data diagnostic is positive and is ALSO produced by the fresh
#  state, which is why R12 remains a member of the class and this row no longer is.
#  *** AND THE TOKEN CLOSED A SECOND MUTANT NOBODY WAS LOOKING FOR, WHICH IS THE PART WORTH
#  RECORDING. ***  A different seat, reviewing the version WITHOUT this token, showed that
#  R13 pinned less than its comment claimed:
#
#      d->cmd_count = 1;      /* was = 0 -- a REPLACEMENT, not a deletion */
#
#  The six words then step 1, 3, 5, 7, 9, 11 -- **the `== 12` equality NEVER FIRES**, so busy
#  is never cleared, no command ever dispatches, and the seventh word is safe.  The old
#  oracle (`0 kills | exit0`) is exactly that mutant's behaviour, so it escaped: R13 pinned
#  *"the leftover is not still 12"*, NOT *"the fourth statement is `= 0`"*.
#
#  **The dispatch token reds it**, because under `= 1` the packet never completes and
#  `handle_command()` is never reached.  So a witness added for the store-death class also
#  closed a value-replacement mutant -- two seats reasoning about different defects, one row.
#
#  *Which is the argument for execution witnesses generally: a row that proves its own
#  machinery ran gets, for free, every mutant that works by stopping the machinery.*
DISPATCH_TEXT = "handle_command: unimplemented command 0x11"
row("R13 recount", "%d|%s|%d" % (t.count(TOOMUCH_TEXT), how, t.count(DISPATCH_TEXT)),
    "0|exit0|1", "0xa0 RE-ARMS cmd_count: two commands do not kill")

# ------------------------------ R13b  A DECLINE MUST NOT DISTURB A PACKET IN FLIGHT
#  *** MEASURED SWEEPING 21/21: add `d->cmd_count = 0;` to site B's DECLINE arm. ***  It
#  is the mirror of R13's mutant -- same statement, other arm -- and it is the more
#  plausible edit of the two, because a decline that "resets state to be safe" reads like
#  defensive hygiene.
#
#  The harm is not a kill: it CORRUPTS AN IN-FLIGHT COMMAND.  A guest assembling a packet
#  that happens to write a bad COND value mid-sequence has its byte counter silently
#  rewound, so the twelve-byte packet never completes and the command never dispatches.
#
#  The session interleaves the decline INTO the packet, which no other row does: arm with
#  0xa0, three data words, a DECLINED COND write, three more.  On the correct build the
#  count reaches 12 and dispatches; under the mutant it is rewound to 0 at the decline,
#  reaches only 6, and the dispatch token never appears.
#
#  *** AND IT IS ANOTHER SIBLING-PARITY MISS: R13 was written for the ACCEPT arm and the
#  identical statement in the DECLINE arm went unwatched. ***  Same field, same file, two
#  lines apart in intent.
A = Addr(CODE)
t, alive, how = session(store16(GDROM_COND, 0x00a0, A)
                        + store16(GDROM_DATA, 0x1111, A)
                        + store16(GDROM_DATA, 0x2222, A)
                        + store16(GDROM_DATA, 0x3333, A)
                        + store16(GDROM_COND, 0x0055, A)
                        + store16(GDROM_DATA, 0x4444, A)
                        + store16(GDROM_DATA, 0x5555, A)
                        + store16(GDROM_DATA, 0x6666, A))
m = COND_RE.search(t)
row("R13b mid pkt", "%d|%s" % (t.count(DISPATCH_TEXT), m.group(1) if m else "absent"),
    "1|55", "a DECLINE mid-packet does not rewind cmd_count")

# ------------------------------------------------ THE TRAILING CONTROL, AND WHY IT EXISTS
#  *** THE OPENING CONTROLS BRACKET THE START OF THE RUN AND NOTHING BRACKETS THE END.
#  MEASURED: a contended run scored 18/25 with GDROMCOND_CONTROL=OK -- seven late rows
#  reading `absent` or `ABSENT-READ-FAILED`, and one session dying outright -- while the
#  four control rows, all of which ran FIRST, were green. ***
#
#  A reader seeing CONTROL=OK is entitled to read the row scores as product results.  On
#  that run they were apparatus failures, and the header said so nowhere.  The controls
#  were not wrong; they were EARLY, and a per-run control cannot see a per-session
#  degradation that begins after it.
#
#  Re-running ONE liveness and ONE device-signature row at the END costs two sessions and
#  converts "the rig was alive when we started" into "the rig was alive throughout".
#  A run whose trailing control is dead has measured nothing after the point it died,
#  and the score must not be read as a product result.
A = Addr(CODE)
t, alive, how = session(["put w 0x8c001800, 0x%x" % LIVE] + load32(0x8c001800, A))
row("Zlive end", printed(t, "r2"), "0x%x" % LIVE,
    "TRAILING LIVENESS: the rig was alive at the END too")

A = Addr(CODE)
t, alive, how = session(store16(GDROM_CNTLO, 0x1234, A) + load16(GDROM_CNTLO, A))
row("Zdevsig end", printed(t, "r2"), "0x34",
    "TRAILING DEVSIG: the device still answered at the END")

#  The END control is reported SEPARATELY from the opening one, because "died partway"
#  and "never started" are different facts and must not render the same.
print("")
print("GDROMCOND_CONTROL_END=%s"
      % ("OK" if rows[-1][1] and rows[-2][1] else "DEAD"))

# ------------------------------------------------------------------------------- result
ok = sum(1 for _, o in rows if o)
print("")
print("GDROMCOND_PROBE_RESULT=%d/%d" % (ok, len(rows)))
print("GDROMCOND_PROBE_DONE")
sys.exit(0 if ok == len(rows) else 1)
