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
    * ANY non-identity treatment of d->cond on a decline --
      restoring `= idata` above the dispatch, zeroing it, or
      assigning a CONSTANT.  Three pre-states, because one
      sample cannot tell a function from a constant.             (R5, R5b, R5c)
    * emptying either accepted arm                                (R6, R8, R9)
    * firing a completion event on a DECLINED write               (R7)
    * touching BUSY or STAT on a DECLINED write                   (R7b)
    * growing an effect on, or declining, site A's 0x0b           (R10)
    * collapsing the two latch bits into one                      (R11)

It does NOT claim to observe anything on the GDROM_DATA read path, the DMA arms, or the
handle_command() decode.  A later escape in those is OUTSIDE this contract, not a breach
of it.

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
COND_RE = re.compile(r"unimplemented GDROM_COND = 0x([0-9a-f]{2})")

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
#  MEASURED, on this probe's first run: with agy jobs holding ~10 concurrent gxemul
#  processes, `devsig sh4` reported got=0x0 want=0xda74 -- which reads as "the SH4 register
#  window is dead" and is really "the guest never got to execute".  A contention artifact
#  wearing a product defect's clothes.
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

A = Addr(CODE)
t, alive, how = session(load16(0xa4000150, A))
row("devsig sh4", printed(t, "r2"), "0x%x" % IPRD_RESET,
    "DEVSIG: SH4 IPRD reset value; RAM would read 0")

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
A = Addr(CODE)
t, alive, how = session(store16(GDROM_COND, 0x0055, A) + load16(GDROM_COND, A))
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

# ------------------------------------------------------------------------------- result
ok = sum(1 for _, o in rows if o)
print("")
print("GDROMCOND_PROBE_RESULT=%d/%d" % (ok, len(rows)))
print("GDROMCOND_PROBE_DONE")
sys.exit(0 if ok == len(rows) else 1)
