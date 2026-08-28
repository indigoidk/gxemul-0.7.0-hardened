#!/usr/bin/env python3
"""DETECTOR for `gdromexitsix` Round 1 -- the `case 0x14` TOC length guard in
dev_dreamcast_gdrom.c (`grep -n 'Read TOC with' <file>`).

The WITNESS is a separate, ungated file: artifacts/gdromexitsix/gdrom_toclen_witness.py,
whose badlen/zerolen rows pinned `exit1` and were MEASURED RED on the committed build at
84f6682 (repro_20260828/PREFIX_committed_84f6682.out).  This file pins the REPAIRED
behaviour.  The two exist separately, rather than one file being re-pinned, because a
witness goes red the day its fix lands and gating one manufactures a regression.

DETECTOR CONTRACT (vacuity floor clause (e)) -- what these rows are designed to catch,
stated so a later escape is either "outside the contract" or "a breach of it" rather than
an argument about overclaiming:

  * REINSTATEMENT of the host kill at the TOC length guard, in any form that ends the
    process -- the `bad surv` and `zero surv` rows;
  * a guard whose REPAIR IS NULLED so a short cnt reaches alloc_data() again -- the
    `bad cond` row, which is the clause-(d) carrier and the reason this probe reads
    GDROM_COND at all;
  * loss of the ACCEPT side, i.e. a guard that grows and starts refusing cnt == 408 --
    the `ok data0`/`ok data1`/`ok cond` rows;
  * loss of the once-latch on the decline diagnostic -- the `latch once` row;
  * a decline that RETURNS instead of BREAKING, skipping the common tail -- the
    `bad cnt` and `bad event` rows, added after that edit was MEASURED to escape
    an earlier 13-row version of this file 13/13;
  * a guard that EXEMPTS one end of the refused range -- `zero cond` (the
    exempt-zero form, which re-opens the heap overflow at cnt=0) and `over cond`
    (the `< 408` form, which admits over-length requests).  Both were predicted
    to sweep the 15-row version CLEAN, by three seats on pass 2.

  *** THE SHAPE THAT KEEPS RECURRING HERE, STATED ONCE: A SURVIVE-ONLY ROW IS
  VACUOUS AT THIS SITE. ***  Three separate escapes -- `> 408`, exempt-zero, and
  `< 408` -- all leave the host alive while the guard is wrong, because the
  damage is either a non-faulting overwrite or no damage at all.  Every value the
  guard refuses therefore needs a DECLINE-CHANNEL row (COND stays 0xa0), not just
  a survival row.  `bad surv`, `zero surv` and `over surv` are kept as companions,
  but none of them is the row that kills anything.

  NOT claimed: that a one-BYTE overflow is detected by crashing.  It is not; the
  `> 408` mutant is caught by the COND channel, not by a fault.  See the note on
  `bad cond` below -- that is the whole reason a survive-only row set was refused.

  NOT claimed: coverage of edits to the TOC WRITER itself (the hardcoded indices),
  or of any arm other than `case 0x14`.  The other `exit(1)` sites in this file
  are gdromexitsix Round 2 and the open `gdromcondlies` row.

WHY A SURVIVE-ONLY ROW SET WOULD HAVE BEEN VACUOUS, measured rather than assumed.
The obvious clause-(d) mutant weakens `!= 408` to `> 408`.  Then cnt=407 falls THROUGH to
alloc_data(407), and the writer's hardcoded indices run to byte 407 -- a one-byte heap
overflow that a normal -O3 build does not necessarily fault on.  A row that only asks
"did the host survive?" scores that mutant GREEN while the defect the round closed is
back.  The discriminator is a SECOND OBSERVABLE CHANNEL:

    cnt == 408 accepted  ->  d->data != NULL  ->  tail sets COND_DATA_AVAIL   -> 0xa8
    cnt != 408 declined  ->  d->data == NULL  ->  tail CLEARS it, cnt = 0     -> 0xa0

Both values are DERIVED, not fitted: the guest writes 0xa0 to GDROM_COND to start the
command, and the common tail either ORs in COND_DATA_AVAIL (0x08) or masks it out.  The
`case GDROM_COND:` read arm returns `d->cond` unmodified.

RUNG 3: every access is a real guest instruction through real address decode and real
memory_rw, on the UNMODIFIED committed `dreamcast` machine description.  Nothing is
device_add'ed and no machine is introduced to reach the site.

DREAMCAST NEEDS -x (two console inputs) or the session dies for a CONFIGURATION reason and
reports the same "died" a defect would.

USAGE:  gdrom_toclen_probe.py <gxemul-binary> <kernel-image> [extra args...]
"""
import os
import pty
import re
import select
import sys
import time

BIN = sys.argv[1]
KERNEL = sys.argv[2]
EXTRA = sys.argv[3:]

CODE = 0x8c001000
SCRATCH = 0x8c001800

GDROM_DATA = 0xa05f7080
GDROM_BUSY = 0xa05f7018
GDROM_CNTLO = 0xa05f7090
GDROM_CNTHI = 0xa05f7094
GDROM_COND = 0xa05f709c
#  SYSASIC_EVENT_GDROM is 32 (thirdparty/dreamcast_sysasicvar.h), and the macro
#  addresses SYSASIC_BASE + 4*(e>>5) -- so event 32 lands in pending_irq[1], bit
#  32 & 31 == 0.  The ASIC's read arm is `odata = d->pending_irq[r]` with NO
#  clear-on-read, so the bit LATCHES and a later guest load can still see it.
#  gdrom_default_probe.py already reads pending_irq[0] at 0xa05f6900, so the
#  technique is in-tree precedent rather than invention.
SYSASIC_PEND1 = 0xa05f6904
SYSASIC_GDROM_BIT = 0x00000001
SH4_IPRD = 0xffd00010
IPRD_RESET = 0xda74
LIVE = 0x12345678

BRA_SELF = 0xaffe
NOP = 0x0009

#  The decline diagnostic this round adds.  Latched N=1 per device instance.
DECLINE = re.compile(r"Read TOC with cnt=-?\d+, not 408 -- declined")


def MOVW_ST(n, m):
    return 0x2001 | (n << 8) | (m << 4)


def MOVW_LD(n, m):
    return 0x6001 | (n << 8) | (m << 4)


def MOVL_ST(n, m):
    return 0x2002 | (n << 8) | (m << 4)


def MOVL_LD(n, m):
    return 0x6002 | (n << 8) | (m << 4)


rows = []


def row(name, got, want, note=""):
    ok = (got == want)
    rows.append((name, ok))
    print("%-14s %-12s %-12s %-46s %s" % (name, got, want, note,
                                          "ok" if ok else "FAIL"))
    return ok


def session(cmds, settle=8.0, spin=2.0, step=0.30):
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN, [BIN, "-V", "-x", "-E", "dreamcast", "-M", "64"] +
                 EXTRA + [KERNEL])
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
    if alive:
        for i, c in enumerate(cmds):
            try:
                os.write(fd, (c + "\n").encode("latin-1"))
            except OSError:
                alive = False
                break
            if not rd(spin if i == len(cmds) - 1 else step):
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
    m = re.search(r"print\s+%s\s*\r?\n\s*(0x[0-9a-f]+)" % reg, t)
    return m.group(1) if m else "absent"


class Addr(object):
    def __init__(self, base):
        self.a = base

    def take(self):
        a = self.a
        self.a += 0x40
        return a


def run(ops, at):
    put = ["put h 0x%x, 0x%04x" % (at + 2 * i, op) for i, op in enumerate(ops)]
    put += ["put h 0x%x, 0x%04x" % (at + 2 * len(ops), BRA_SELF),
            "put h 0x%x, 0x%04x" % (at + 2 * len(ops) + 2, NOP)]
    return put + ["pc=0x%x" % at, "step %d" % len(ops)]


def store16(reg, val, A):
    return ["r7=0x%x" % reg, "r8=0x%04x" % val] + run([MOVW_ST(7, 8)], A.take())


def load16(reg, A, dest=2):
    return ["r1=0x%x" % reg, "r%d=0" % dest] + \
        run([MOVW_LD(dest, 1)], A.take()) + ["print r%d" % dest]


def packet(words, A):
    setup = ["r7=0x%x" % GDROM_DATA]
    for i, w in enumerate(words):
        setup.append("r%d=0x%04x" % (8 + i, w))
    return setup + run([MOVW_ST(7, 8 + i) for i in range(len(words))], A.take())


CMD_TOC = [0x0014] * 6


def stage_toc(A, cnt):
    """CNTLO/CNTHI = cnt, COND = 0xa0, then the Read-TOC packet.  9 accesses."""
    return (store16(GDROM_CNTLO, cnt & 0xff, A) +
            store16(GDROM_CNTHI, (cnt >> 8) & 0xff, A) +
            store16(GDROM_COND, 0xa0, A) +
            packet(CMD_TOC, A))


# ------------------------------------------------------------------- controls
A = Addr(CODE)
t, alive, how = session(["r7=0x%x" % SCRATCH, "r8=0x%08x" % LIVE,
                         "r1=0x%x" % SCRATCH, "r2=0"] +
                        run([MOVL_ST(7, 8), MOVL_LD(2, 1)], A.take()) +
                        ["print r2"])
row("live", printed(t, "r2") if alive else "died", "0x%x" % LIVE,
    "LIVENESS: guest store then guest load, through RAM")

A = Addr(CODE)
t, alive, how = session(["r1=0x%x" % SH4_IPRD, "r2=0"] +
                        run([MOVL_LD(2, 1)], A.take()) + ["print r2"])
g = printed(t, "r2") if alive else "died"
row("devsig sh4", ("0x%x" % (int(g, 16) & 0xffff)) if g.startswith("0x") else g,
    "0x%x" % IPRD_RESET, "DEVSIG: SH4 IPRD reset value, RAM reads 0")

A = Addr(CODE)
t, alive, how = session(["r1=0x%x" % GDROM_BUSY, "r2=0"] +
                        run([MOVL_LD(2, 1)], A.take()) + ["print r2"])
g = printed(t, "r2") if alive else "died"
row("gdrom map", ("mapped" if g.startswith("0x") else g) if alive else "died",
    "mapped", "GDROM_BUSY read is served, not a paddr fault")
print("TOCLEN_CONTROL=%s" % ("OK" if all(ok for _, ok in rows) else "DEAD"))

# ------------------------------------------------------------------- accept side
#
#  THE DE-ESCALATION ACCEPT ROWS.  This round removed a host-fatal guard, which
#  deleted the accidental tripwire that made guard growth self-announcing: before
#  the fix, narrowing the accept set meant exit(1) on the first legal write.  These
#  rows pin the accept side so a grown guard reddens instead of going quiet.
A = Addr(CODE)
t, alive, how = session(stage_toc(A, 408) +
                        ["r1=0x%x" % GDROM_DATA, "r2=0", "r3=0"] +
                        run([MOVW_LD(2, 1), MOVW_LD(3, 1)], A.take()) +
                        ["print r2", "print r3"])
row("ok data0", printed(t, "r2") if alive else "died", "0x10",
    "ACCEPT: synthesized TOC halfword 0, device-only value")
row("ok data1", printed(t, "r3") if alive else "died", "0xffff9600",
    "ACCEPT: TOC halfword 1, sign-extended by mov.w")
row("ok surv", how, "exit0", "ACCEPT: the legal length must not kill the host")

A = Addr(CODE)
t, alive, how = session(stage_toc(A, 408) + load16(GDROM_COND, A))
g = printed(t, "r2") if alive else "died"
row("ok cond", ("0x%x" % (int(g, 16) & 0xff)) if g.startswith("0x") else g,
    "0xa8", "ACCEPT: 0xa0 written, COND_DATA_AVAIL(0x08) SET by the tail")

# ------------------------------------------------------------------- the decline
#
#  `bad surv`/`zero surv` are the reinstatement carriers: they pinned exit1 on the
#  committed build and pin exit0 now.
A = Addr(CODE)
t1, alive1, how1 = session(stage_toc(A, 407))
row("bad surv", how1, "exit0",
    "cnt=407 declines instead of ending the host")
row("bad says", "yes" if len(DECLINE.findall(t1)) >= 1 else "no", "yes",
    "the decline ANNOUNCES itself -- not a silent refusal")

A = Addr(CODE)
t2, alive2, how2 = session(stage_toc(A, 0))
row("zero surv", how2, "exit0",
    "cnt=0 declines too -- the malloc(0) end of the same guard")

#  *** THE CLAUSE-(d) CARRIER, and the reason this probe reads COND at all. ***
#  A guard weakened from `!= 408` to `> 408` lets cnt=407 reach alloc_data(407)
#  while the writer indexes byte 407 -- a one-byte heap overflow that need not
#  fault, so `bad surv` alone would score it GREEN.  Under that mutant d->data is
#  non-NULL, so the tail SETS COND_DATA_AVAIL and this row reads 0xa8, not 0xa0.
A = Addr(CODE)
t, alive, how = session(stage_toc(A, 407) + load16(GDROM_COND, A))
g = printed(t, "r2") if alive else "died"
row("bad cond", ("0x%x" % (int(g, 16) & 0xff)) if g.startswith("0x") else g,
    "0xa0", "DECLINE: COND_DATA_AVAIL stays CLEAR -- kills the `> 408` mutant")

#  *** THE break-vs-return ROWS.  ADDED AFTER A MEASURED L1: this detector scored
#  13/13 against `break;` -> `return;`, and the product comment beside the fix
#  CLAIMS that edit "would skip that event and leave the guest waiting forever"
#  while shipping no row for it.  That is the CLAIM -> ROW check, unrun, on the
#  round's own diff.  Found by the opus seat on Round 2's design panel. ***
#
#  *** AND `bad cond` STRUCTURALLY CANNOT SEE IT, which is worth stating because
#  it is the clause-(d) carrier and looks like it should. ***  The guest writes
#  0xa0 to start the command, and BIT 3 IS ALREADY CLEAR in 0xa0.  So the tail's
#  `d->cond &= ~COND_DATA_AVAIL` is a NO-OP on this path: `break` (tail runs,
#  clears an already-clear bit) and `return` (tail never runs) both leave 0xa0.
#  A row can only separate them by observing something the TAIL WRITES.
#
#  On the decline path the tail writes exactly two things -- `d->cnt = 0` and the
#  SYSASIC event -- so there is one row each, and between them they pin both
#  halves of what the comment claims.
A = Addr(CODE)
t, alive, how = session(stage_toc(A, 407) + load16(GDROM_CNTLO, A))
g = printed(t, "r2") if alive else "died"
row("bad cnt", ("0x%x" % (int(g, 16) & 0xff)) if g.startswith("0x") else g,
    "0x0", "DECLINE: the tail zeroed d->cnt -- `return` leaves 0x97")

#  The event itself, pinned directly rather than inferred.  This is the stronger
#  of the two: `bad cnt` shows the tail RAN, this shows the guest was actually
#  TOLD the command completed -- which is the property that stops a hang.
A = Addr(CODE)
t, alive, how = session(stage_toc(A, 407) +
                        ["r1=0x%x" % SYSASIC_PEND1, "r2=0"] +
                        run([MOVL_LD(2, 1)], A.take()) + ["print r2"])
g = printed(t, "r2") if alive else "died"
row("bad event",
    ("set" if (int(g, 16) & SYSASIC_GDROM_BIT) else "clear")
    if g.startswith("0x") else g,
    "set", "DECLINE: SYSASIC_EVENT_GDROM fired -- `return` would skip it")

#  *** THE ZERO AND OVER-LENGTH COND ROWS.  ADDED AFTER PASS 2 MEASURED TWO MORE
#  ESCAPES, ONE OF WHICH RE-OPENS THE HEAP OVERFLOW THIS ROUND CLOSES. ***
#
#  I applied the survive-only-is-vacuous lesson to cnt=407 and NOT to the other two
#  ends of the same guard.  `zero surv` and (as first drafted) the over-length case
#  ask only "did the host survive?", and at this site that question is answerable
#  YES while the defect is fully restored:
#
#    EXEMPT-ZERO   `d->cnt != 408`  ->  `d->cnt != 408 && d->cnt != 0`
#        cnt=0 is then ACCEPTED -> alloc_data(0) -> malloc(0), both memsets become
#        no-ops, and the writer still stores through d->data[101*4+3].  **408 bytes
#        into a zero-byte allocation** -- the round's own §2 defect, back -- and a
#        write past a minimal chunk need not fault, so `zero surv` reads exit0.
#        Found by the glm seat on pass 2; predicted 15/15 clean before this row.
#
#    LOWER-BOUND   `d->cnt != 408`  ->  `d->cnt < 408`
#        cnt >= 409 is then ACCEPTED.  No overflow (409 >= 408), so nothing dies --
#        but the guard now admits lengths it must refuse, and NO SHIPPED ROW USED A
#        VALUE ABOVE 408.  Found independently by the grok and agy seats, both
#        predicting a 15/15 sweep.
#
#  Both are killed the same way the `> 408` mutant was: by asking the DECLINE
#  question on the COND channel instead of the survival question.
A = Addr(CODE)
t, alive, how = session(stage_toc(A, 0) + load16(GDROM_COND, A))
g = printed(t, "r2") if alive else "died"
row("zero cond", ("0x%x" % (int(g, 16) & 0xff)) if g.startswith("0x") else g,
    "0xa0", "DECLINE: cnt=0 declines -- kills the exempt-zero mutant")

A = Addr(CODE)
t4, alive4, how4 = session(stage_toc(A, 409))
row("over surv", how4, "exit0", "cnt=409 declines instead of ending the host")

A = Addr(CODE)
t, alive, how = session(stage_toc(A, 409) + load16(GDROM_COND, A))
g = printed(t, "r2") if alive else "died"
row("over cond", ("0x%x" % (int(g, 16) & 0xff)) if g.startswith("0x") else g,
    "0xa0", "DECLINE: cnt=409 declines -- kills the `< 408` mutant")

#  THE LATCH.  Two bad TOCs in one session must print exactly ONE diagnostic.
#  fatal() cannot be silenced by -q, so an unlatched guest-drivable message is a
#  flood; N=1 per device instance is the house idiom.
#  *** THE SECOND DECLINE IS READ BACK, AND THAT ROW IS THE ONE THAT KILLS THE
#  LATCH-STATE MUTANT.  Added after pass 2; found by ONE seat of nine. ***
#
#  `if (d->cnt != 408 && !(d->warned & GDROM_W_TOCLEN))` -- the nested-if collapse,
#  or equivalently a brace slip that moves `break` inside the latch block -- was
#  measured to sweep the 18-row version CLEAN while re-opening the heap overflow:
#
#    * every NON-latch row runs its own fresh session, where `warned` is clear, so
#      the mutant behaves identically to the correct build and every row passes;
#    * the latch session declines the FIRST bad TOC (setting the bit) and then
#      ACCEPTS the second, because the latch bit now gates the guard itself.  One
#      message is still printed and the host still survives, so `latch once` = 1
#      and `latch surv` = exit0 BOTH PASS -- while the second bad TOC reached
#      alloc_data(406) and the writer stored through byte 407.
#
#  *** SO THE GENERALISATION THE HEADER STATES IS ONE LEVEL SHORT. ***  It says
#  every VALUE the guard refuses needs a decline-channel row.  True -- and every
#  STATE in which it refuses needs one too.  The latched state had only a count row
#  and a survival row, which are exactly the two shapes this file already knows are
#  vacuous here.
#
#  Costs no new session: the read is appended to the existing latch session.
A = Addr(CODE)
t3, alive3, how3 = session(stage_toc(A, 407) + stage_toc(A, 406) +
                           load16(GDROM_COND, A))
row("latch once", str(len(DECLINE.findall(t3))), "1",
    "two declines in one session emit the diagnostic exactly once")
row("latch surv", how3, "exit0", "and neither of them ends the host")
g = printed(t3, "r2") if alive3 else "died"
row("latch cond", ("0x%x" % (int(g, 16) & 0xff)) if g.startswith("0x") else g,
    "0xa0", "the SECOND decline still declined -- kills the latch-state mutant")

ok = all(o for _, o in rows)
print("")
print("TOCLEN_RESULT=%d/%d" % (sum(1 for _, o in rows if o), len(rows)))
print("TOCLEN_PROBE=%s" % ("PASS" if ok else "FAIL"))
sys.exit(0 if ok else 1)
