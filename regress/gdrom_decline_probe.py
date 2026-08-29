#!/usr/bin/env python3
#
#  #490: the DECLINE detector for dev_dreamcast_gdrom.c's two de-fatalised sites.
#
#      Site A   case 0x30, an unimplemented data format      (GDROM_W_FMT)
#      Site B   default:, an unimplemented command byte      (GDROM_W_CMD)
#
#  Both were `fatal()` + `exit(1)` reached by an ordinary guest store, so a guest chose
#  whether the emulator kept running.  Both now decline, announced ONCE per device instance
#  behind their own latch bit, and `break` to the common tail.
#
#  *** WHY THIS IS A NEW PROBE RATHER THAN ROWS BOLTED ONTO gdrom_default_probe.py. ***
#  #489's precedent, and it is about coupling rather than tidiness: gdrom_default's
#  denominator is pinned as a literal in gate_sh_rounding.sh AND spelled out as a matching
#  `for v in ...` name list, so every added row edits two places that must agree.  A separate
#  probe with its own section and its own denominator has no such coupling.  Only the rows
#  that must observe the EXISTING stale session stayed there.
#
#  *** THIS PARAGRAPH SAID "the 58-row probe" AND "a 58-name list" TWICE.  gdrom_default is
#  now SIXTY -- this very round added `stale quiet` and `stale how` to it.  Corrected
#  2026-08-29; the count is deliberately no longer written here at all. ***  Naming a
#  sibling's row count in THIS file is the coupling the paragraph is arguing against, and it
#  went stale in the same round that wrote it.
#
#  AND THE COUNT HAS NO SOUND STATIC DERIVER, which is why it must not be transcribed:
#  `grep -c '^row('` on gdrom_default gives 52 and any-`row(` gives 55, because some rows are
#  emitted from loops.  **The MEASURED `GDROM_DEF_RESULT=60/60` is the only authority.**  This
#  probe is the easy case -- `^row(` = 20, agreeing with its measured 20/20 -- and that
#  difference between two sibling files is exactly why a count needs its deriver named.
#
#  ---------------------------------------------------------------------------------------
#  *** THE CONTRACT: WHAT THIS DETECTOR IS DESIGNED TO CATCH, so a later escape is either
#  outside it or a breach of it rather than an argument about overclaiming. ***
#
#    1. reinstating either exit(1)                         -- `fmt surv` / `unk surv`
#    2. the decline not announcing at all                  -- `fmt says` / `unk says`
#    3. the announce losing its once-only latch            -- `fmt x2`  / `unk x2`
#    4. the two sites sharing ONE latch bit                -- `both sites`
#    5. either latch bit colliding WITH `GDROM_W_TOCLEN`    -- `crossbit`
#    6. `break` becoming `return` (skipping the tail)      -- `fmt cnt` / `unk cnt`,
#                                                             `fmt event` / `unk event`
#    7. the `break` slipping INSIDE the latch `if`         -- `latch cond`
#    8. the guard growing to swallow a legal format        -- `acceptA`
#    9. the upstream 0x24 arm being folded into a decline  -- `fmt 0x24`
#
#  *** CLAIM 5 READ "COLLIDING WITH AN EXISTING BIT" AND THAT OVERCLAIMED BY A FACTOR OF
#  SEVEN.  Narrowed 2026-08-29 after a pass-2 seat named the escape. ***  `crossbit` stages
#  only a TOC decline, so it can see a collision with `GDROM_W_TOCLEN` and NOTHING ELSE.
#  Aliasing either new bit onto any of the other six -- e.g.
#  `#define GDROM_W_FMT (1u << GDROM_W_OVERREAD_B)` -- is PREDICTED to score 20/20, because
#  no decline session performs an overread, a length mismatch or a DMA arm first, so the
#  aliased bit is clear in every session and every latch behaves normally.
#
#  DELIBERATELY NOT CLOSED BY BUILDING TWELVE MORE ALIAS MUTANTS: that fails the addition
#  licence's economics, and the enum-by-construction shape bounds the realistic edit to a
#  hand-written raw mask.  `Ma_toclen`/`Mb_toclen` prove the most-benign-traffic instance IS
#  caught.  The contract now claims what was measured and discloses the rest, which is what
#  clause (e) is for.
#
#  *** THREE MEASURED 20/20 ESCAPES, BUILT BY THE PASS-2 ASK-AGAIN.  Disclosed 2026-08-29;
#  artifacts/gdromexitsix/p2askagain_20260829/, every log sentinel-verified, each mutant's
#  20-row block BYTE-IDENTICAL to base -- total escapes, not ties. ***
#
#    E1_aliasover  (1u << GDROM_W_FMT_B) -> (1u << GDROM_W_OVERREAD_B)          20/20
#    E2_assignA    `d->warned |= GDROM_W_FMT;` -> `d->warned = GDROM_W_FMT;`    20/20
#    E3_widenA     `& GDROM_W_FMT` -> `& (GDROM_W_FMT | GDROM_W_CMD)`           20/20
#
#  **E2 IS ONE CHARACTER AND IT IS THE WORST OF THE THREE.**  Site A still announces exactly
#  once, so every Site-A row stays green -- but the ASSIGNMENT clears the other eight latches.
#  A guest alternating a short TOC with a bad format then re-announces #489's diagnostic
#  WITHOUT BOUND, and `fatal()` cannot be silenced by `-q`.  **No row observes any latch
#  ACROSS a Site-A decline**, which is the structural gap: every latch row checks its OWN bit.
#
#  **E3 IS INVISIBLE ONLY BECAUSE OF ROW ORDER.**  Both two-site rows run Site A before
#  Site B, so widening Site A's test is unobservable; *the same edit at Site B WOULD be
#  caught* (`1,0`).  And pass 1's `S3 both` ran the OPPOSITE order -- the shipped rows
#  inverted it and nothing recorded that.
#
#  SEVERITY: **coverage debt, not a floor breach**, per #464's precedent (`wdcperopcode`,
#  `wdcsectorreset` -- the latter is E2's structural twin).  The floor's four clauses are all
#  measured clean.  These are hypothetical future edits in uncovered cells, which is exactly
#  what clause (e) exists to make FALSIFIABLE rather than argued.
#
#  A ONE-DECLARATION FIX FOR THE E1 CLASS EXISTS AND WAS CONTROLLED IN FIVE STATES -- a
#  compile-time disjointness assert in this file's own `gdrom_w_fits_its_carriers` idiom:
#  correct COMPILES; E1's alias REFUSED; `Ma_toclen`'s shape REFUSED; `M3shared`'s shape
#  REFUSED; and E1 WITHOUT the assert COMPILES (the negative control).  **The addition-licence
#  objection that declined the twelve alias mutants does NOT apply to a compile-time bound**,
#  which costs no rows and fails CLOSED when a tenth bit arrives.  Filed for the owner.
#
#  NOT claimed:
#    * collision with the other six latch bits -- see above, and now MEASURED as E1;
#    * any latch's state ACROSS a decline at the other site (E2);
#    * a latch test widened to cover a sibling bit at Site A (E3, order-dependent);
#    * the tail's THIRD channel.  The added comments say the tail "zeroes d->cnt, clears
#      COND_DATA_AVAIL and fires the completion event".  `cnt` has `fmt cnt`/`unk cnt` and
#      the event has `fmt event`/`unk event`; **the COND_DATA_AVAIL clear has NO ROW.**  It
#      is guest-observable through the `cond` read arm, and a row is buildable (stage
#      DATA_AVAIL with a good TOC, decline, read cond).  It is NOT owed under the row-demand
#      bound -- both `M_ret*` mutants are already killed twice over -- so this sentence is
#      the explicit no-row discharge the CLAIM->ROW check requires, not an omission;
#    * anything about the three exit(1) sites still live in dev_dreamcast_gdrom_access(),
#      which are a different round; and nothing about exploitability of the heap overflow
#      #489's guard prevents -- see artifacts/gdromexitsix/asan_m0_20260828/.
#
#  *** A ROW THAT FAILS **OPEN**, recorded because it is invisible in a green table. ***
#  `latch cond` wants 0 and reads `REJ`, the unlatched `rejecting sector_count` diagnostic --
#  which is OUTSIDE this diff, guest-drivable, and a natural future target of this very
#  de-fatalisation campaign.  Reword that text and the regex matches nothing, the row goes
#  permanently and silently GREEN, and no other row reads `REJ` with a non-zero want.  `HUH`
#  is presence-pinned by `acceptA` and the 0x24 text by `fmt 0x24`; **`REJ` is pinned by
#  nothing.**  A one-line presence row would close it.
#  ---------------------------------------------------------------------------------------
#
#  *** EVERY ROW BELOW NAMES THE MUTANT IT KILLS AND THE OBSERVABLE THAT DIFFERS UNDER IT.
#  Five of them were built and MEASURED by the pass-1 measuring seat before this file
#  existed; three of those ESCAPED an earlier 13-row plan.  ***  The measured table is at
#  artifacts/gdromexitsix/opus_r2full_20260828/ and every mutant name below matches it.
#
#  A NOTE ON WHY THE LATCH ROWS ARE NOT ONE ROW.  `M2nolatch` (bit tested, never set) and
#  `M3shared` (both sites on one bit) are ORTHOGONAL -- measured, neither session catches
#  the other's mutant.  A single "the latch fires once" row catches exactly one of them.
#
#  AND A NOTE ON THE STAGING OF `fmt cnt`, which would otherwise be VACUOUS.  `M_retA`'s
#  `S3 both` session measured CNT=0x0 and ESCAPED, because the unknown command ran first and
#  its tail had already zeroed `cnt`.  **The CNT channel discriminates only when d->cnt is
#  non-zero on entry to the declined command.**  So `fmt cnt` writes CNTLO/CNTHI directly
#  and then sends the bad packet -- one command, no prior dispatch.  The same construction
#  is what `fmt event` needs, because `pending_irq` is STICKY and a staging TOC would
#  pre-set the bit and kill that channel.

import os, pty, re, select, sys, time

if len(sys.argv) < 3:
    sys.stderr.write("usage: gdrom_decline_probe.py <gxemul> <kernel>\n")
    sys.exit(2)

BIN = sys.argv[1]
KERNEL = sys.argv[2]

CODE = 0x8c001000
SCRATCH = 0x8c001800

GDROM_DATA = 0xa05f7080
GDROM_BUSY = 0xa05f7018
GDROM_CNTLO = 0xa05f7090
GDROM_CNTHI = 0xa05f7094
GDROM_COND = 0xa05f709c

#  event 32 = bit 0 of the SECOND pending word.  Derived in #489 and re-checked here:
#  SYSASIC_EVENT_GDROM is 32 in dreamcast_sysasicvar.h, and 32/32 = word 1.  The DMA rows in
#  gdrom_default_probe.py read pending_irq[0] bit 14 -- a DIFFERENT event at a DIFFERENT
#  address.  This is a one-address variant of that machinery, not a copy of it.
SYSASIC_PEND1 = 0xa05f6904
SYSASIC_GDROM_BIT = 0x00000001

IPRD_RESET = 0xda74
LIVE = 0x12345678
BRA_SELF = 0xaffe
NOP = 0x0009

#  *** THE DECLINE REGEXES ARE ANCHORED ON `-- declined`, AND THAT IS MEASURED, NOT TIDY. ***
#  The pass-1 measuring seat found that a bare `unimplemented data format` matches BOTH the
#  upstream 0x24 warn-and-continue line AND the new Site-A decline, because the fix's message
#  contains that exact substring.  A row on the bare form cannot tell them apart.
FMT_DECL = re.compile(r"unimplemented data format 0x[0-9a-f]+ -- declined")
CMD_DECL = re.compile(r"unimplemented command 0x[0-9a-f]+ -- declined")
#  the upstream arm, which must stay byte-identical and must NOT match either regex above
FMT_0X24 = re.compile(r"unimplemented data format 0x24\. Continuing anway")
#  two unlatched diagnostics one guard further in, used as accept-side oracles
REJ = re.compile(r"rejecting sector_count")
HUH = re.compile(r"Huh\? GDROM data_len")

rows = []


#  Row-name column: `%-14s` plus a literal space, and gate_sh_rounding.sh matches `^$v  `.
#  A 13-character name leaves EXACTLY two spaces and matches; 14 leaves one and the check
#  becomes unsatisfiable.  **The limit is 13.**  Measured -- gdrom_default_probe.py's own
#  comment said "13 or 14" and was wrong about 13, corrected in #490.  Longest name here is
#  10.  *** AN EARLIER DRAFT OF THIS LINE SAID 10 WHILE THE FILE HELD A 13-CHARACTER
#  NAME -- caught by a length check on this very file before it ran.  Names here are now
#  <= 10, and NO NAME IS A PREFIX OF ANOTHER FOLLOWED BY A SPACE: `acceptA` / `accept sil`
#  rather than `acceptA` / `acceptA quiet`.  The two-space rule makes the latter safe, but
#  relying on it is the padded-column trap wearing a seatbelt. ***
def row(name, got, want, note=""):
    ok = (got == want)
    rows.append((name, ok))
    print("%-14s %-12s %-12s %-40s %s" % (name, got, want, note,
                                          "ok" if ok else "FAIL"))
    return ok


def session(cmds, settle=8.0, spin=2.0):
    """Run one gxemul, feed debugger commands, return (transcript, alive, how).

    `how` is the DEATH MODE and it is not decoration: `alive` is False only when a read
    raises OSError or returns empty INSIDE a budget window, so it is true of a HUNG
    emulator, a FROZEN one, and -- measured -- one already killed after the last budget
    check.  Every survival row here reads `how`, never `alive`."""
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
    #  spelling COPIED VERBATIM from gdrom_toclen_probe.py -- two gdrom probes must not
    #  disagree about what "died" means
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


def MOVW_ST(n, m):
    return 0x2001 | (n << 8) | (m << 4)


def MOVW_LD(n, m):
    return 0x6001 | (n << 8) | (m << 4)


def MOVL_ST(n, m):
    return 0x2002 | (n << 8) | (m << 4)


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


#  *** THE OPERANDS WERE REVERSED HERE AND IT MADE THREE ROWS PASS VACUOUSLY. ***
#  MOVW_LD(n, m) is `mov.w @Rm, Rn`.  This built MOVW_LD(1, dest) -- `mov.w @Rdest, R1`
#  -- reading from the address in Rdest (0) into R1, then printing Rdest, which was
#  never written.  **Every load16 row read 0x0 whatever the device held.**  `gdrom map`
#  passed because "0x0" starts with "0x"; `fmt cnt` and `unk cnt` passed because they
#  WANT 0x0.  Only `fmt stage`, whose wanted value is 0x98, could see it -- the whole
#  argument for a row whose wanted value differs from its failure value.
#
#  AND IT CORRECTS A DIAGNOSIS ONE EDIT OLD: `devsig sh4` reading 0x0 was blamed on a
#  16-bit access width the register would not serve.  FALSE -- the cause was this
#  reversal.  That row was switched to load32 and worked, for a reason that was not the
#  reason given, and a wrong reason gets reused.
def load16(reg, A, dest=2):
    return ["r1=0x%x" % reg, "r%d=0" % dest] + run([MOVW_LD(dest, 1)], A.take(1)) \
        + ["print r%d" % dest]


def load32(reg, A, dest=2):
    return ["r1=0x%x" % reg, "r%d=0" % dest] + run([0x6002 | (1 << 4) | (dest << 8)],
                                                   A.take(1)) + ["print r%d" % dest]


def packet(words, A):
    """Arm the device and push a 12-byte command packet, low halfword first."""
    out = store16(GDROM_COND, 0xa0, A)
    for w in words:
        out += store16(GDROM_DATA, w, A)
    return out


#  A packet is SIX halfwords and dispatch fires on the sixth.  cmd[0] is the LOW byte of
#  word 0, so 0x2030 means cmd[0]=0x30, cmd[1]=0x20 -- a pass-1 seat read this backwards and
#  its conclusion happened to survive, which is why the byte order is stated here.
def cmd(c0, c1=0x00, c10=0x0000):
    return [c1 * 256 + c0, 0, 0, 0, 0, c10]


GOOD_FMT = cmd(0x30, 0x20)       # the legal read-sectors packet
BAD_FMT = cmd(0x30, 0x21)        # Site A: an unimplemented data format
FMT_24 = cmd(0x30, 0x24)         # the upstream warn-and-continue arm -- NOT a decline
BAD_CMD = cmd(0x31)              # Site B: an unimplemented command byte
MOUNT = cmd(0x70)                # implemented, allocates nothing
TOC_SHORT = [0x0014, 0, 0, 0, 0, 0]   # a TOC whose cnt will be wrong -> #489's decline


# ---------------------------------------------------------------- identity controls
#  A detector that cannot fail on a null medium is vacuous.  These three fail on a stale
#  copy, a comment-only file, or a binary that never reached the device.

A = Addr(CODE)
t, alive, how = session(["r7=0x%x" % SCRATCH, "r8=0x%08x" % LIVE]
                        + run([MOVL_ST(7, 8)], A.take(1))
                        + ["r1=0x%x" % SCRATCH, "r2=0"]
                        + run([0x6002 | (1 << 4) | (2 << 8)], A.take(1)) + ["print r2"])
row("live", printed(t, "r2") if alive else "died", "0x%x" % LIVE,
    "LIVENESS: a guest store then a guest load, through RAM")

#  *** A 32-BIT LOAD, MASKED -- NOT A 16-BIT ONE.  MEASURED: the 16-bit form reads 0x0
#  and this control FAILED on the probe's first run. ***  SH4_IPRD does not serve a
#  halfword access here, so `mov.w` returns nothing and the row cannot tell a live
#  device from a dead one -- a CONTROL that fails open is worse than no control.
#  Copied from gdrom_toclen_probe.py, which had already solved it.
#
#  *** THIS IS THE THIRD TIME IN THIS FILE I INVENTED A VARIANT OF A SOLVED PROBLEM
#  RATHER THAN COPYING THE WORKING ONE *** -- after a bogus write-1-to-clear pre-clear
#  on the event rows, and a summed pair on `fmt 0x24`.  The sibling probe is the
#  reference implementation; deviate from it only with a reason worth writing down.
A = Addr(CODE)
t, alive, how = session(load32(0xffd00010, A))
g = printed(t, "r2")
row("devsig sh4", ("0x%x" % (int(g, 16) & 0xffff)) if g.startswith("0x") else g,
    "0x%x" % IPRD_RESET, "DEVSIG: the SH4 IPRD reset value; RAM would read 0")

A = Addr(CODE)
t, alive, how = session(load16(GDROM_BUSY, A))
g = printed(t, "r2")
row("gdrom map", ("mapped" if g.startswith("0x") else g) if alive else "died", "mapped",
    "the GDROM window is served, not a paddr fault")

#  *** CONTROL IS EMITTED HERE, OVER THE THREE IDENTITY ROWS ONLY -- NOT AT THE END OVER
#  EVERYTHING.  MEASURED WHY ON THIS PROBE'S FIRST RUN: it printed CONTROL=DEAD because ONE
#  PRODUCT ROW FAILED, which is exactly the conflation the gate section exists to prevent. ***
#  The gate reads this to say "a run whose controls died is an APPARATUS failure and must not
#  be read as product failures".  A CONTROL line that also goes DEAD on a product failure
#  makes that sentence false and sends a reader hunting a broken rig for a real defect.
#  `rows and` is load-bearing too: all([]) is True, so an empty list would certify a run that
#  measured nothing.
print("GDROM_DECL_CONTROL=%s"
      % ("OK" if rows and all(ok for _, ok in rows) else "DEAD"))


# ---------------------------------------------------------------- SITE A: the format decline
#  kills: reinstating exit(1) at Site A          via: how
#  kills: the arm not declining at all           via: the anchored decline text
A = Addr(CODE)
t, alive, how = session(packet(BAD_FMT, A))
row("fmt surv", how, "exit0", "a bad data format must not end the host")
row("fmt says", "%d" % len(FMT_DECL.findall(t)), "1",
    "and it announces itself, exactly once")

#  kills: M_braceA -- `break` moved INSIDE the latch `if`, so the SECOND identical bad
#         format falls through into sector_nr.  MEASURED escaping a 13-row plan, because
#         "announces once" reads 1 either way.
#  via:   a DECLINE channel read after the SECOND command, not the announce count
A = Addr(CODE)
t, alive, how = session(packet(BAD_FMT, A) + packet(BAD_FMT, A))
row("fmt x2", "%d" % len(FMT_DECL.findall(t)), "1",
    "two bad formats, ONE line -- the latch holds")
row("latch cond", "%d" % len(REJ.findall(t)), "0",
    "and the SECOND one still declines -- no fallthrough to sector_nr")

#  kills: M_retA -- `break` -> `return`, which skips the common tail.
#  via:   d->cnt, which the tail zeroes.  *** STAGED WITH NO PRIOR DISPATCH: the CNT channel
#         discriminates ONLY when d->cnt is non-zero on entry, and M_retA measured CNT=0x0
#         (escaping) in a session where an earlier command had already zeroed it. ***
#         pending_irq is STICKY, so the same single-command staging is what `fmt event`
#         needs -- a staging TOC would pre-set the bit and make that row vacuous.
A = Addr(CODE)
#  *** `fmt cnt` WANTS 0x0 -- AND A FAILED READ ALSO GIVES 0x0.  So the staging is read
#  BACK IN THE SAME SESSION FIRST: without `fmt stage` proving 0x98 actually landed,
#  `fmt cnt` is green whether the tail zeroed the count or the read simply did not
#  work.  The pair is the oracle; neither half is one alone. ***
t, alive, how = session(store16(GDROM_CNTLO, 0x98, A) + store16(GDROM_CNTHI, 0x01, A)
                        + load16(GDROM_CNTLO, A, dest=3)
                        + packet(BAD_FMT, A) + load16(GDROM_CNTLO, A))
row("fmt stage", printed(t, "r3"), "0x98",
    "the staged count is really there BEFORE the command")
row("fmt cnt", printed(t, "r2"), "0x0",
    "and the tail zeroed it -- a return would have left 0x98")

A = Addr(CODE)
t, alive, how = session(packet(BAD_FMT, A) + load32(SYSASIC_PEND1, A))
g = printed(t, "r2")
row("fmt event", ("set" if (int(g, 16) & SYSASIC_GDROM_BIT) else "clear")
    if g.startswith("0x") else g, "set",
    "a declined command still reports completion -- a return would hang the guest")

#  *** NO PRE-CLEAR OF THE PENDING REGISTER, AND THE OBVIOUS 'CAREFUL' FORM IS WRONG. ***
#  An earlier draft of these two rows wrote 0 to SYSASIC_PEND1 first, to clear the bit
#  before the command set it.  `dev_dreamcast_asic.c`'s write arm is
#  `d->pending_irq[r] &= ~idata` -- **WRITE-1-TO-CLEAR** -- so writing 0 clears NOTHING.
#  The bit would never have been cleared, and the row would pass whether or not the
#  decline fired the event: VACUOUS, and vacuous in the direction that looks diligent.
#  It was also a 16-bit store to a 32-bit register.  The correct construction needs no
#  clear at all: each session is a FRESH process, so the bit starts clear and only the
#  dispatched command can set it.  Copied from gdrom_toclen_probe.py's `bad event`,
#  which had already solved this.  Found by desk-check against the device source
#  before this file was ever run.
#  kills: an accept-set growth that folds the upstream 0x24 arm into the decline.
#  via:   the 0x24 line is byte-identical upstream text and must match NEITHER new regex.
A = Addr(CODE)
t, alive, how = session(packet(FMT_24, A))
#  *** ASSERT THE PAIR, NOT THE SUM.  An earlier draft summed the two counts and wanted
#  1 -- which is BLIND TO EXACTLY THE MUTANT IT NAMES: folding 0x24 into the decline
#  converts one match into the other and the SUM STAYS 1.  A sum hides a swap. ***
row("fmt 0x24", "%d,%d" % (len(FMT_0X24.findall(t)), len(FMT_DECL.findall(t))), "1,0",
    "0x24 keeps its own unlatched line and is NOT this site's decline")


# ---------------------------------------------------------------- SITE B: the command decline
A = Addr(CODE)
t, alive, how = session(packet(BAD_CMD, A))
row("unk surv", how, "exit0", "an unknown command must not end the host")
row("unk says", "%d" % len(CMD_DECL.findall(t)), "1",
    "and it announces itself, exactly once")

#  kills: M2nolatch -- the bit tested but never set, so every occurrence announces.
A = Addr(CODE)
t, alive, how = session(packet(BAD_CMD, A) + packet(BAD_CMD, A))
row("unk x2", "%d" % len(CMD_DECL.findall(t)), "1",
    "two unknown commands, ONE line -- the latch holds")

#  kills: M_retA at Site B.  Same staging rule as `fmt cnt`.
A = Addr(CODE)
t, alive, how = session(store16(GDROM_CNTLO, 0x98, A) + store16(GDROM_CNTHI, 0x01, A)
                        + packet(BAD_CMD, A) + load16(GDROM_CNTLO, A))
row("unk cnt", printed(t, "r2"), "0x0", "the tail zeroed the count")

A = Addr(CODE)
t, alive, how = session(packet(BAD_CMD, A) + load32(SYSASIC_PEND1, A))
g = printed(t, "r2")
row("unk event", ("set" if (int(g, 16) & SYSASIC_GDROM_BIT) else "clear")
    if g.startswith("0x") else g, "set", "the declined command reports completion")


# ---------------------------------------------------------------- the two-site rows
#  kills: M3shared -- both sites folded onto ONE latch bit.  MEASURED escaping: the second
#         site falls silent because the first already latched.  ORTHOGONAL to `unk x2` and
#         `fmt x2` -- neither of those sees it, and it does not see them.
A = Addr(CODE)
t, alive, how = session(packet(BAD_FMT, A) + packet(BAD_CMD, A))
row("both sites", "%d,%d" % (len(FMT_DECL.findall(t)), len(CMD_DECL.findall(t))), "1,1",
    "each site speaks for itself -- separate latch bits")

#  kills: Ma_toclen / Mb_toclen -- either new bit COLLIDING with an existing one.
#  *** THE WORST OF THE MEASURED ESCAPES.  d->warned has NINE writers sharing one field and
#  SIX of the pre-existing ones are set from inside DEVICE_ACCESS by ordinary guest register
#  reads, so a collision is silenced by traffic that looks entirely normal. ***  A short TOC
#  sets GDROM_W_TOCLEN first; if either new bit aliases it, that site prints NOTHING.
A = Addr(CODE)
t, alive, how = session(packet(TOC_SHORT, A) + packet(BAD_FMT, A) + packet(BAD_CMD, A))
row("crossbit", "%d,%d" % (len(FMT_DECL.findall(t)), len(CMD_DECL.findall(t))), "1,1",
    "a prior TOC decline must not silence either new site")


# ---------------------------------------------------------------- the accept side
#  The de-escalation clause: a fatal->survive fix DELETES the accidental tripwire that made
#  guard growth self-announcing.  Before this round, widening `!= 0x20` meant exit(1) on the
#  first legal write -- unmissable.  After it, the same edit means a silently refused write.
#  kills: M_growA (`!= 0x20` -> `!= 0x21`), MEASURED giving huh 1->0.
A = Addr(CODE)
t, alive, how = session(store16(GDROM_CNTLO, 0x98, A) + store16(GDROM_CNTHI, 0x01, A)
                        + packet(cmd(0x30, 0x20, 0x0001), A))
row("acceptA", "%d" % len(HUH.findall(t)), "1",
    "the LEGAL format still enters the arm -- growth would silence this")
row("accept sil", "%d" % len(FMT_DECL.findall(t)), "0",
    "and it is not declined")


n = sum(1 for _, ok in rows if ok)
print("GDROM_DECL_RESULT=%d/%d" % (n, len(rows)))
print("GDROM_DECL_VECTOR=" + ",".join(("1" if ok else "0") for _, ok in rows))
sys.exit(0 if n == len(rows) else 1)
