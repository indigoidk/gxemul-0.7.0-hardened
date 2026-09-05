#!/usr/bin/env python3
"""pcc2widthkills DETECTOR -- the twelve width-guard blocks in DEVICE_ACCESS(pcc2).

WHAT THE FIX DID.  Twelve `if (len != 1)' blocks -- TEN `fatal(); exit(1)' kills that ended the host on
a guest-chosen access width, and two #119 warn-once latches that refused it with a
process-global static.  The
tree's own header says PCC2 registers "can be accessed as bytes, two-bytes, or
four-bytes", so the width is LEGAL.  The fix is a DIRECTION SPLIT:

    READS   ACCEPT -- the memcpy above the switch already served them, raw bytes in
            address order, width-correct by construction.  The guard discarded a
            correct answer.
    WRITES  DECLINE + per-instance latched announce -- every write arm uses `idata',
            the big-endian-composed value, which is "the addressed byte" ONLY at
            len==1.  Deleting the guard would store the NEIGHBOUR's lane.

CONTRACT (vacuity-floor clause (e)) -- what this detector is designed to catch:

  CATCHES
    * reinstatement of the kill at any of the SIX GUEST-reachable blocks (survival
      rows paired with a liveness observable, because exit status cannot tell
      "declined and quit" from "died with status 0");
    * *** pass 2: the two FOLDED-IN arms, IPL and MASK, had NO ROW -- twelve blocks
      converted, ten given rows, and the shipped contract did not say so.  A seat
      found it by sibling parity: MASK is GENCTL's twin and had none of GENCTL's rows.
      Repaired: IPL is EVEN and therefore the SIXTH guest-reachable block (survival +
      message rows); MASK is odd (operator rows) and gets GENCTL's readback. ***
    * reinstatement at any of the six OPERATOR-only blocks (VECBASE, PSCALEADJ, SCCICR,
      SCCRX, SCSIICR, MASK; the T1CTL/T1ICR labels are odd too but share TxCTL/TxICR's
      blocks), through the debugger's `put h' at an odd address -- MEASURED to warn
      and store and kill
      (artifacts/pcc2widthkills/operator_reach_20260903.out);
    * *** DELETE instead of decline on the write side -- the lane hazard.  `st.h
      0xAABB' to GENCTL must leave GENCTL unchanged; a bare deletion stores 0xBB,
      VECBASE's lane, because (uint8_t) idata is the HIGHEST-address byte ***;
    * an accidental per-lane compose (GENCTL would read 0xAA);
    * the value a wide READ composes -- lane order and width -- not merely survival;
    * loss of the latch in either direction: dropped `|=' floods (same site twice
      must announce ONCE), and one bit shared across blocks silences (two sites must
      announce TWICE);
    * the de-escalation clause: at the five even blocks with `acc' rows a legal byte write
      lands and reads back through the arm's own mask with NO decline message; at all
      twelve, `acc all' pins NO decline and survival (a guard grown to refuse bytes); at
      the two print-only arms the body's own print is the proof (`acc pscale ign',
      `acc ipl ro').  SCCERR's byte side is value-identical (always 0) and is disclosed,
      not claimed.

  THE ENUMERATION (pass 3 class closure, pass 4 domain repair).  Twelve blocks x NINE
  clause-(d) shapes, the helper's own two operations, and four access widths.  Two
  consecutive passes found breaches of ONE class -- a block with no channel for the
  ANNOUNCE-THEN-FALL-THROUGH shape (guard kept, announce kept, `break' removed, the
  halfword LANDS) -- at MASK, then at four odd arms, then (pass 3, MEASURED 82/82 by a
  seat) at VECBASE, whose `rb vecbase' row is GENCTL's neighbour-lane check and never
  writes wide to VECBASE's own arm.  So the space is written down, cell by cell.
  M = measured kill (log named in CHANGELOG/PRETABLE); S = same channel as a measured
  shape at that arm (the mutant lands the write exactly as the measured one does);
  E = equivalent by construction, with its warrant.  Shapes: DEL guard deleted; LEN
  `len != 1' -> `len > 2' (halfword lands, word declined); LEN2 its MIRROR, `len != 1' ->
  `len == 2' (halfword declined, WORD lands -- named by the codex seat on pass 3); KILL
  verbatim exit(1) reinstated; ALIAS one enum member for two blocks; FALL announce-then-
  fall-through; SWAP guard operand `len' -> `idata > 0xff'; GROW the guard widened to
  decline the LEGAL byte width too (`len != 1' -> `len != 0'), the de-escalation clause.

      block      DEL   LEN   LEN2  KILL  ALIAS FALL  SWAP  GROW   FALL channel
      GENCTL     M     S     W     S     C     M     M     A/C    rb genctl (table 1 M_NOBREAK)
      VECBASE    S     S     W     M     C     M     C     C      rb vecbase own  (pass-3 repair)
      PSCALEADJ  S     S     W     S     C     M     C     C      op pscale noig  (message)
      TxCTL      S     M     W     S     C     M     C     A/C    rb t2ctl (FALL: part 3b, t2 and t1)
      TxICR      M     M     W     S     C     S     C     A/C    rb t2icr
      SCCERR     S     M     S     S     C     E     C     A/C    E: the arm stores 0 and nothing in
                                                                  the model ever stores a nonzero
                                                                  SCCERR (deriver: every writer of
                                                                  pcctwo_reg[], grep 'pcctwo_reg\[';
                                                                  the counter memcpy's 8-byte span
                                                                  is pcc2counter8, disclosed)
      SCCICR     S     S     W     S     C     M     C     C      rb sccicr
      SCCTX      M     M     W     S     C     S     C     A/C    rb scctx
      SCCRX      S     S     W     S     C     M     C     C      rb sccrx
      SCSIICR    S     S     W     S     C     M     C     C      rb scsiicr
      IPL        S     S     W     M     C     M     C     C      hwr ipl noig    (pass-3 repair:
                                                                  the write body prints once)
      MASK       M     M     W     M     C     M     C     C      rb mask
      C  = the cardinality row `latch all' (twelve wide writes, twelve announces): ALIAS,
           any collision drops the count; SWAP, its value 0x0003 fits a byte, so a
           value-test guard at ANY arm lets it land and drops the count.
      W  = `latch all w' (twelve WORD writes via put w, twelve announces): a `len == 2'
           guard at ANY arm lets the word land silently and drops the count.  SCCERR's
           own word rows (wrd/wwr sccerr) are its S.
      A/C = the arm's own `acc' row, AND `acc all' (twelve legal GUEST byte stores, ZERO
           declines): a guard grown to refuse bytes at ANY arm announces and reds it.
           Blocks marked C alone have no per-arm acc row; `acc all' is their channel.
           NOT the debugger's `put b': it calls memory_rw with NO_EXCEPTIONS, which does not
           dispatch to a DM_DEFAULT device, so a `put b' row could not see the grown guard
           (MEASURED: 95/96 in part 3 and 96/96 in part 3b, the mutation proven in the binary).  `put h/w/d' go
           through the store_Nbit_word helpers and do reach the arms.
      DEL/LEN/KILL cells marked S land the write, or die, exactly as the measured shape at
      that arm does, and the arm's own dcl / survival
      / readback rows are the channel.  KILL cells' channel is the survival PAIR (exit
      status plus the liveness observable), which varies under a reinstated kill by
      construction; the CHANNEL rule's 'survival-only' names a survival oracle at a
      REFUSAL-effect site, which a kill is not.  `d->warned' is a 32-bit field with twelve bits assigned.

      A NINTH SHAPE, on the input the six-shape list named and never walked: RDDECL, the
      direction split's own conjunct nulled, `writeflag == MEM_WRITE' -> `<= MEM_WRITE'
      (ONE character; MEM_READ is 0).  The Opus seat MEASURED it 82/82 on pass 3: wide
      READS were declined, announced as writes, skipped the arm's read body and consumed
      the block's latch bit -- and no session holding a wide read carried a decline-count
      row.  Closed by `hrd <block> nod' / `wrd sccerr nod' on the SEVEN wide-read sessions
      that already existed (six even blocks by ld.h, SCCERR by ld): a declined read is a
      DECL where zero is expected.  The six ODD blocks' read-side cells are UNREACHABLE by
      construction -- a guest wide read at an odd offset alignment-faults before memory_rw,
      and a debugger read does not dispatch to a DM_DEFAULT device -- and are disclosed,
      not rowed.  One cosmetic gap, disclosed: the seven `op * dcl' rows count the GENERIC
      decline text, and for FIVE arms (VECBASE, PSCALEADJ, SCCICR, SCCRX, SCSIICR) no other
      row pins the name string, so a change of the NAME alone there is invisible; the
      T1 labels share TxCTL/TxICR's fatal() with the named `rb t2ctl dcl' / `rb t2icr dcl'
      rows, and `latch all' pins cardinality.

      THE SHARED BLOCKS.  TxCTL serves T1CTL (0x17, odd) and T2CTL (0x16, even); TxICR
      serves T1ICR (0x1b) and T2ICR (0x1a).  The blocks' readbacks above are at the T2
      offsets; a seat noted that a fall-through reaching only the T1 labels (the block
      split in two) would leave `op t1ctl dcl' at 1 with nothing reading T1CTL back.  So
      the T1 labels carry their own operator-path readbacks, `rb t1ctl' and `rb t1icr'.
      THE THIRTEENTH ARM.  SCCRXIACK has NO width guard and never had one: its body
      ignores `idata' (it clears a bit in SCCRX and reasserts), so its effect is
      width-invariant by construction and it is not a member of the twelve.  It is named
      here so the census is not read as an omission.
      SESSIONS.  Every session() is a fresh pty.fork/execv of the emulator, so no latch
      state survives from one row to the next; `latch all' counts one process.
      THE HELPER'S OWN OPERATIONS (pass 4).  pcc2_width_decline() has two lines that
      every block depends on: the TEST `!(d->warned & (1u << bit))' and the SET
      `d->warned |= (1u << bit)'.  One-token edits to the SET line escaped every row:
      `|=' -> `=' (assign: A, B clears A -- `latch aba' A,B,A = 2) and `(1u << bit)' ->
      `1' (bit 0 always: every other block announces every time -- `latch same2', MASK
      twice = 1).  The TEST line's operand swap (`&' -> `==') is caught by `latch all':
      with the field accumulating, equality fails from the second block on and it
      announces 12 either way -- DISCLOSED as not distinguishable by this instrument.
      WIDTHS.  The debugger drives len 2 (`put h'), 4 (`put w') and 8 (`put d'); the
      guest drives 1, 2 and 4.  `latch all', `latch all w' and `latch all d' pin the
      refusal at every block for each non-byte width, so a guard true on a subset of
      {2,4,8} drops one of the three counts.
      BIT IDENTITY.  `latch all' and `latch all w' are cardinality rows: they assert
      twelve announces, never WHICH bit.  A translation of the bit index
      (`1u << bit' -> `1u << (bit + 1)') is EQUIVALENT by construction -- no code
      outside pcc2_width_decline() reads d->warned's bits -- and was MEASURED 96/96 by a
      pass-4 seat as the clause-(f) control.  That warrant expires the day anything
      indexes or reports those bits.
      ANNOUNCE SEVERITY.  Every row counts TEXT on a pty run under -V; `fatal(' ->
      `debug(' in the helper changes no text these rows read.  NOT CAUGHT, disclosed;
      the fork's recorded warrant for fatal() over debug() is dev_asc.c's (-q makes a
      debug()-level line invisible to the boot-log hygiene grep).
      THE FAULT MEMBER.  `break' -> `return 0' at a guard turns the decline into a bus
      error: the guest's store faults, the program never prints, and the block's `hwr'
      / `lv' pair reds.  Measured as M_RET0_GENCTL in part 4.
      INSTRUMENTS.  Parts 3, 3b and 3c ran three frozen copies (md5 3dcf73de, 280d9ab3,
      72759b4f); the last is the shipped probe.  3 -> 3b changed only `rb t1ctl' /
      `rb t1icr's expected string, 3b -> 3c only `acc all's session; row-name sets are
      identical and no killing row was touched, so the part-3 kills TRANSFER.  `acc all'
      was REWRITTEN, not added: its warrant is that the session is self-contained and
      part 3c measured the rewrite (95/96, `acc all' alone).

  DOES NOT CATCH, stated so an escape is outside the contract rather than an argument
    * per-instance vs process-global latch state: mvme187 instantiates ONE pcc2, so no
      session can hold two instances.  The bitfield is per-instance by construction;
      nothing here measures it;
    * pcc2c040kill -- a LEGAL byte write of 0x04 to GENCTL still ends the host in
      reassert_interrupts().  Every GENCTL lane value here keeps bit 0x04 CLEAR so no
      row dies for that reason;
    * pcc2defaultkill -- an unlisted offset (0x06, 0x14, 0x18, 0x2c ...) still ends the
      host in `default:';
    * pcc2counter8 -- the counter arm's raw memcpy of an 8-byte write;
    * what real hardware does with the LANES of a wide write (not on disk);
    * the SCCERR word-write's stored value: the arm always stores 0, so a decline and
      an accept are value-identical there and the row's channel is the message.

Sentinel: PCC2W_PROBE_DONE
"""

import os, pty, re, select, sys, time

BIN = sys.argv[1] if len(sys.argv) > 1 else "build/gxemul"
LABEL = sys.argv[2] if len(sys.argv) > 2 else "local"

DUMMY = "/tmp/pcc2_dummy.bin"
open(DUMMY, "wb").write(b"\x00\x00\x00\x00")

CODE = 0x00010000
SCRATCH = 0x00020000
PCC2 = 0xfff42000
#  the SIX GUEST-reachable blocks (even offsets; IPL below is the sixth) and the six
#  OPERATOR-only ones (odd offsets; T1CTL/T1ICR are odd labels of the shared TxCTL/TxICR
#  blocks).  An earlier comment here said five and seven: a units slip, blocks vs labels.
GENCTL, T2CTL, T2ICR, SCCERR, SCCTX = 0x02, 0x16, 0x1a, 0x1c, 0x1e
VECBASE, PSCALEADJ, T1CTL, T1ICR, SCCICR, SCCRX, SCSIICR = 0x03, 0x15, 0x17, 0x1b, 0x1d, 0x1f, 0x2f
#  pcc2 pass 2: THE TWO FOLDED-IN ARMS HAD NO ROW AT ALL.  A seat found that the probe
#  touched no offset at 0x3e or 0x3f -- twelve blocks converted, ten given rows.  MASK
#  is GENCTL's byte-identical twin (store byte, reassert); GENCTL's null-repair was
#  caught by `rb genctl', MASK's by nothing, a 60/60 sweep.  AND IPL IS EVEN: it is the
#  SIXTH guest-reachable block, not a seventh operator one.
IPL, MASK = 0x3e, 0x3f
CHIPID = 0x00


def enc(op26, rd, rs1, imm):
    return (op26 << 26) | (rd << 21) | (rs1 << 16) | (imm & 0xffff)


#  r2 = PCC2 base, r3 = scratch, r4 = load target, r5 = store source, r6 = second source
#  ld.b / ld.h (0x07 / 0x06) SIGN-EXTEND: 0x82 would print as 0xffffff82.  Every row that
#  asserts a VALUE uses the unsigned forms ld.bu / ld.hu (0x03 / 0x02); the survival rows
#  only check exit status and keep the signed forms.
def LD_B(rd, off): return enc(0x07, rd, 2, off)
def LD_H(rd, off): return enc(0x06, rd, 2, off)
def LD_BU(rd, off): return enc(0x03, rd, 2, off)
def LD_HU(rd, off): return enc(0x02, rd, 2, off)
def LD_W(rd, off): return enc(0x05, rd, 2, off)
def ST_B(rs, off): return enc(0x0b, rs, 2, off)
def ST_H(rs, off): return enc(0x0a, rs, 2, off)
def ST_W(rs, off): return enc(0x09, rs, 2, off)
I_ST_SCR = enc(0x09, 5, 3, 0)          # st  r5,r3,0   scratch word
I_LD_SCR = enc(0x05, 4, 3, 0)          # ld  r4,r3,0
I_BR_SELF = 0xc0000000

SENTINEL = 0xdeadbeef
DEVSIG = "IGNORING write to read-only PCCTWO_CHIPID"
DECL = "-- declined.  (once) ]"
rows = []


def row(name, got, want, note=""):
    assert name not in [n for n, _ in rows], "DUPLICATE ROW NAME %r" % name
    assert len(name) <= 15, name
    ok = (got == want)
    rows.append((name, ok))
    print("%-16s %-12s %-12s %-46s %s" % (name, str(got), str(want), note,
                                          "ok" if ok else "FAIL"))
    return ok


def session(cmds, settle=1.5, spin=1.2):
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN, [BIN, "-V", "-x", "-E", "mvme88k", "-e", "mvme187", "-M", "64",
                       "0x10000:" + DUMMY])
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
    return "0x%x" % int(m.group(1), 16) if m else "absent"


def program(insns, at=CODE):
    #  `at' lets a session run TWO programs: a second sequence at the SAME address finds
    #  pc already there and the assignment is skipped (the Addr hazard, designed out in
    #  the sgi probes with Addr.take()).  Callers needing two pass at=CODE + 0x100.
    words = list(insns) + [I_BR_SELF, 0]
    cmds = ["put w 0x%x, 0x%08x" % (at + 4 * i, w) for i, w in enumerate(words)]
    return cmds + ["pc=0x%x" % at, "step %d" % len(insns)]


def setup(r5="0x5a5a5a5a", r6="0x0"):
    return ["r2=0x%x" % PCC2, "r3=0x%x" % SCRATCH, "r5=%s" % r5, "r6=%s" % r6,
            "r4=0x%x" % SENTINEL]


print("pcc2widthkills DETECTOR -- binary=%s label=%s" % (BIN, LABEL))
print("%-16s %-12s %-12s %-46s %s" % ("row", "got", "want", "note", ""))

# ------------------------------------------------------------------ controls
t, alive, how = session(setup() + program([I_ST_SCR, I_LD_SCR]) + ["print r4"])
row("live", printed(t, "r4") if alive else "died", "0x5a5a5a5a",
    "RAM word round-trips through the same decode")
t, alive, how = session(setup() + program([ST_B(5, CHIPID)]))
row("devsig", t.count(DEVSIG), 1, "a byte write to CHIPID makes the DEVICE speak")
t, alive, how = session(setup() + program([I_ST_SCR, LD_B(4, GENCTL), I_LD_SCR]) + ["print r4"])
row("byte rd", how, "exit0", "ld.b GENCTL: the legal width, serviced on both builds")
row("byte rd liv", printed(t, "r4") if alive else "died", "0x5a5a5a5a", "...and runs on")

# --------------------------------------- survival pairs at the five reachable blocks
#  Each kill row is PAIRED with a positive post-access observable.
for nm, off in (("genctl", GENCTL), ("t2ctl", T2CTL), ("t2icr", T2ICR),
                ("sccerr", SCCERR), ("scctx", SCCTX)):
    t, alive, how = session(setup() + program([I_ST_SCR, LD_H(4, off), I_LD_SCR]) + ["print r4"])
    row("hrd " + nm, how, "exit0", "ld.h %s (aligned halfword READ) survives" % nm.upper())
    row("hrd %s lv" % nm, printed(t, "r4") if alive else "died", "0x5a5a5a5a", "...and runs on")
    row("hrd %s nod" % nm, t.count(DECL), 0,
        "...and a wide READ is never declined (the direction split's own conjunct)")
    #  r6 = the halfword to store: both lanes keep GENCTL's bit 0x04 CLEAR (pcc2c040kill)
    t, alive, how = session(setup(r6="0xaabb") + program([I_ST_SCR, ST_H(6, off), I_LD_SCR]) + ["print r4"])
    row("hwr " + nm, how, "exit0", "st.h %s (aligned halfword WRITE) survives" % nm.upper())
    row("hwr %s lv" % nm, printed(t, "r4") if alive else "died", "0x5a5a5a5a", "...and runs on")
#  SCCERR is the one 4-aligned block: word read AND write
t, alive, how = session(setup() + program([I_ST_SCR, LD_W(4, SCCERR), I_LD_SCR]) + ["print r4"])
row("wrd sccerr", how, "exit0", "ld SCCERR (the one 4-aligned block) survives")
row("wrd sccerr lv", printed(t, "r4") if alive else "died", "0x5a5a5a5a", "...and runs on")
row("wrd sccerr nod", t.count(DECL), 0, "...and the word READ is never declined")
t, alive, how = session(setup(r6="0x00000000") + program([I_ST_SCR, ST_W(6, SCCERR), I_LD_SCR]) + ["print r4"])
row("wwr sccerr", how, "exit0", "st SCCERR (word WRITE) survives")
row("wwr sccerr lv", printed(t, "r4") if alive else "died", "0x5a5a5a5a", "...and runs on")
#  SCCERR's arm always stores 0, so decline and accept are VALUE-identical there: the
#  only channel that varies is the announcement.
row("wwr sccerr dcl", t.count("write to PCCTWO_SCCERR " + DECL), 1,
    "...and it was DECLINED once -- the message is the only channel here")

# ---------------------------------------------------------- VALUE rows (reads)
#  A wide read must compose the lanes in ADDRESS order.  VECBASE's arm masks & 0xf0
#  and GENCTL's stores the byte, so the halfword at 0x02 is GENCTL<<8 | VECBASE.
#  0x82 keeps bit 0x04 clear.
t, alive, how = session(setup(r5="0x82", r6="0x50")
                        + program([ST_B(5, GENCTL), ST_B(6, VECBASE), LD_HU(4, GENCTL)]) + ["print r4"])
row("val h genctl", printed(t, "r4") if alive else "died", "0x8250",
    "ld.h at GENCTL composes GENCTL:VECBASE in address order -- kills lane-order / zero-fill")
#  word at SCCERR: SCCERR always 0; SCCICR & 0x1f; SCCTX & 0x1f; SCCRX & 0xdf.
t, alive, how = session(setup(r5="0x15", r6="0x1f")
                        + program([ST_B(5, SCCICR), ST_B(6, SCCTX), ST_B(6, SCCRX), LD_W(4, SCCERR)]) + ["print r4"])
row("val w sccerr", printed(t, "r4") if alive else "died", "0x151f1f",
    "ld at SCCERR composes 00:SCCICR:SCCTX:SCCRX -- four lanes, right order")

# ------------------------------------------------ READBACK rows (the DELETE killer)
#  After a declined st.h 0xAABB to GENCTL, BOTH lanes must be unchanged.  Under a bare
#  deletion GENCTL reads 0xBB (the neighbour's lane); under an accidental compose it
#  reads 0xAA and VECBASE 0xB0.  Both lanes of 0xAABB keep bit 0x04 clear.
t, alive, how = session(setup(r5="0x82", r6="0xaabb")
                        + program([ST_B(5, GENCTL), ST_H(6, GENCTL), LD_BU(4, GENCTL)]) + ["print r4"])
row("rb genctl", printed(t, "r4") if alive else "died", "0x82",
    "GENCTL unchanged after a declined st.h -- kills DELETE (0xbb) and compose (0xaa)")
row("rb genctl dcl", t.count("write to PCCTWO_GENCTL " + DECL), 1,
    "...and the decline was announced ONCE")
t, alive, how = session(setup(r5="0x50", r6="0xaabb")
                        + program([ST_B(5, VECBASE), ST_H(6, GENCTL), LD_BU(4, VECBASE)]) + ["print r4"])
row("rb vecbase", printed(t, "r4") if alive else "died", "0x50",
    "VECBASE unchanged too -- the second lane of the declined halfword")

# ---------------------------- per-arm channels (pass 2: sibling parity, arm by arm)
#  A seat pointed out that only GENCTL had a readback: every other reachable arm's
#  halfword-write row checked SURVIVAL alone, so a guard edited at ONE arm (`len > 2',
#  or the guard deleted, at T2ICR only) left every row green.  Each arm now has its own
#  channel, with a lane value its own mask turns into a different byte when it lands.
for nm, off, pre, landed in (("t2ctl", T2CTL, "0x03", "0x3"), ("t2icr", T2ICR, "0x13", "0x13"),
                             ("scctx", SCCTX, "0x1f", "0x1f")):
    t, alive, how = session(setup(r5=pre, r6="0xaab8")
                            + program([ST_B(5, off), ST_H(6, off), LD_BU(4, off)]) + ["print r4"])
    row("rb " + nm, printed(t, "r4") if alive else "died", landed,
        "%s unchanged after a declined st.h -- kills a guard edited at THIS arm" % nm.upper())
    row("rb %s dcl" % nm, t.count("write to PCCTWO_%s " % ("TxCTL" if nm == "t2ctl" else "TxICR" if nm == "t2icr" else "SCCTX") + DECL), 1,
        "...announced once at this arm")
t, alive, how = session(setup(r6="0xaab8") + program([ST_H(6, SCCERR)]))
row("hwr sccerr dcl", t.count("write to PCCTWO_SCCERR " + DECL), 1,
    "halfword write to SCCERR declined once -- value-identical arm, message channel")

#  PRE-TABLE BLOCK yield (section 1, guard field vs body field): the guard reads the access
#  SHAPE (len) and the guarded body reads the VALUE (idata).  An operand swap to a value
#  test -- `idata > 0xff', a plausible "does it fit a byte" reading -- accepts a halfword
#  write whose value fits, and big-endian 0x0022 then stores 0x22, the NEIGHBOUR's lane,
#  into GENCTL: the original defect, behind a guard that still reads like a width check.
#  Every other wide-write row used a value above 0xff, so all 77 were green under it BY
#  CONSTRUCTION.  Written before the repair table ran; the table says whether it kills.
t, alive, how = session(setup(r5="0x11", r6="0x0022")
                        + program([ST_B(5, GENCTL), ST_H(6, GENCTL), LD_BU(4, GENCTL)]) + ["print r4"])
row("rb genctl lo", printed(t, "r4") if alive else "died", "0x11",
    "st.h of a value that FITS a byte is still declined -- the guard is on len, not idata")

# ------------------------- latch CARDINALITY (pass 2, the measuring seat's class closer)
#  `latch same' and `latch two' pin ONE pair out of 66: every other session writes at most
#  one BLOCK, so a bit shared by any other pair announces normally and no row moves.
#  MEASURED by the builder: aliasing SCCTX onto SCCRX's bit -- a ONE-CHARACTER edit --
#  left the 60-row detector at 60/60.  ONE OFFSET PER BLOCK: TxCTL serves T1CTL+T2CTL
#  and TxICR serves T1ICR+T2ICR, so twelve LABELS would give only ten announces -- the
#  same units slip that let "five even blocks + seven odd ones = twelve" read as all
#  twelve blocks.  This row pins the CARDINALITY of the latch: any collision anywhere in
#  the 12-bit space drops the count.  (Operator path for all twelve, so the odd ones are
#  reachable; the guest-reachable halves have their own rows above.)
BLOCKS12 = (("GENCTL", 0x02), ("VECBASE", 0x03), ("PSCALEADJ", 0x15), ("TxCTL", 0x16),
            ("TxICR", 0x1a), ("SCCERR", 0x1c), ("SCCICR", 0x1d), ("SCCTX", 0x1e),
            ("SCCRX", 0x1f), ("SCSIICR", 0x2f), ("IPL", 0x3e), ("MASK", 0x3f))
#  VALUE 0x0003, not 0x0303: it fits a byte, so this row ALSO reds if any arm swaps its
#  guard operand from len to a value test (see `rb genctl lo').  On the fix the value
#  never lands, so the expectation is value-independent.
t, alive, how = session(["put h 0x%x, 0x0003" % (PCC2 + o) for _, o in BLOCKS12])
row("latch all", t.count(DECL), 12,
    "one wide write per BLOCK -> TWELVE announces: bit CARDINALITY, not one pair")
row("latch all lv", how, "exit0", "...and the host survived all twelve blocks")

# ------------------------------------------------------------------ latch rows
t, alive, how = session(setup(r6="0xaabb") + program([ST_H(6, GENCTL), ST_H(6, GENCTL)]))
row("latch same", t.count("write to PCCTWO_GENCTL " + DECL), 1,
    "same block twice -> ONE announce -- kills a dropped |= (flood)")
t, alive, how = session(setup(r6="0x0303") + program([ST_H(6, GENCTL), ST_H(6, T2CTL)]))
row("latch two", t.count(DECL), 2,
    "two blocks -> TWO announces -- kills a bit shared across blocks")
#  PASS 4 (glm, kimi, codex): `latch same' sees only CONSECUTIVE repeats, so `|=' -> `=' in the
#  helper -- the field ASSIGNED instead of accumulated, one character -- passed every row: A
#  then B clears A's bit, and nothing wrote A again afterwards.  Interleave: A, B, A -> TWO.
t, alive, how = session(setup(r6="0x0303") + program([ST_H(6, GENCTL)])
                        + ["put h 0x%x, 0x0303" % (PCC2 + VECBASE)]
                        + program([ST_H(6, GENCTL)], at=CODE + 0x100))
row("latch aba", t.count(DECL), 2,
    "A, B, A -> TWO announces: the latch ACCUMULATES (an assignment would give three)")
#  PASS 4 (minimax): `(1u << bit)' -> `1' in the SET line latches bit 0 for every block, so
#  every block but GENCTL announces on every write.  `latch same' is at GENCTL (bit 0) and
#  stays green.  The same test at a non-zero bit:
t, alive, how = session(["put h 0x%x, 0x0303" % (PCC2 + MASK)] * 2)
row("latch same2", t.count("write to PCCTWO_MASK " + DECL), 1,
    "MASK (bit 11) twice -> ONE announce: the SET line names the block's own bit")

# --------------------------------------------- de-escalation ACCEPT rows (byte writes)
#  Removing twelve exit(1)s destroys the tripwire that announced guard growth.  So the
#  legal width must still LAND at each reachable arm, through its own mask, with no
#  decline message.  Expected values from the arms' own semantics.
for nm, off, wr, rdv in (("genctl", GENCTL, "0x82", "0x82"),     # stores the byte; bit 0x04 clear
                          ("t2ctl", T2CTL, "0x03", "0x3"),       # &= 0xfc; |= (v & 3)
                          ("t2icr", T2ICR, "0x13", "0x13"),      # &= ~0x17; |= (v & 0x17)
                          ("scctx", SCCTX, "0x1f", "0x1f"),      # = v & 0x1f
                          ("sccerr", SCCERR, "0x5a", "0x0")):    # any write clears to 0
    t, alive, how = session(setup(r5=wr) + program([ST_B(5, off), LD_BU(4, off)]) + ["print r4"])
    row("acc " + nm, printed(t, "r4") if alive else "died", rdv,
        "st.b %s at the legal width lands through its own mask" % nm.upper())
    row("acc %s nod" % nm, t.count(DECL), 0, "...with NO decline message")

# ------------------------------- OPERATOR path: the seven odd blocks via `put h'
#  The m88k alignment check makes these guest-unreachable; the debugger warns on a
#  misaligned put and stores anyway, straight to the handler (MEASURED pre-fix: exit1).
for nm, off in (("vecbase", VECBASE), ("pscale", PSCALEADJ), ("t1ctl", T1CTL),
                ("t1icr", T1ICR), ("sccicr", SCCICR), ("sccrx", SCCRX), ("scsiicr", SCSIICR)):
    t, alive, how = session(["put h 0x%x, 0x0303" % (PCC2 + off)])
    row("op " + nm, how, "exit0", "debugger put h at odd %s survives" % nm.upper())
    row("op %s dcl" % nm, t.count(DECL), 1, "...and was declined once")

#  --------- the odd arms' FALL-THROUGH channel (pass 3, ruled a floor breach, not a disclosure)
#  The block above proves each odd arm ANNOUNCES; it cannot see a guard that announces AND
#  then lets the halfword land (the M_FALL shape -- decline nulled, guard kept: clause (d)).
#  PRETABLE Section 2 had disclosed that as "a sentence owed".  The measuring seat asked
#  whether a disclosure can discharge a floor clause; it cannot, or every breach becomes a
#  sentence.  So each of the four arms gets the channel its body offers:
#    SCCICR/SCCRX/SCSIICR store `idata & mask' then reassert_interrupts(): set 0x1f by
#      byte (legal under both masks), decline a wide 0xaab8, read the byte back -- a landed
#      write leaves 0x18 (& 0x1f) or 0x98 (& 0xdf) in an INTERRUPT CONTROL register.
#    PSCALEADJ stores nothing; its write body only prints "ignored (value ...)".  A landed
#      wide write therefore prints that line -- the message is the only channel, and the
#      row counts it at ZERO.
for nm, off in (("sccicr", SCCICR), ("sccrx", SCCRX), ("scsiicr", SCSIICR)):
    t, alive, how = session(setup(r5="0x1f") + program([ST_B(5, off)])
                            + ["put h 0x%x, 0xaab8" % (PCC2 + off)]
                            + program([LD_BU(4, off)], at=CODE + 0x100) + ["print r4"])
    row("rb " + nm, printed(t, "r4") if alive else "died", "0x1f",
        "%s unchanged after a declined put h -- a fall-through lands 0x18/0x98 and reasserts" % nm.upper())
t, alive, how = session(["put h 0x%x, 0x0303" % (PCC2 + PSCALEADJ)])
row("op pscale noig", t.count("PSCALEADJ ignored"), 0,
    "a declined wide write never reaches the 'ignored' print -- fall-through would")

#  PASS 3 (class closure).  `rb vecbase' above writes wide to GENCTL and reads VECBASE: it
#  is GENCTL's neighbour-lane check and never exercises VECBASE's own guard.  A seat
#  MEASURED announce-then-fall-through at VECBASE as 82/82 -- the halfword landed (& 0xf0)
#  while `op vecbase dcl' and `latch all' stayed green by construction.  VECBASE is the
#  interrupt vector base, so the landed lane mis-delivers every vector.  Its own readback:
t, alive, how = session(setup(r5="0x50") + program([ST_B(5, VECBASE)])
                        + ["put h 0x%x, 0xaab8" % (PCC2 + VECBASE)]
                        + program([LD_BU(4, VECBASE)], at=CODE + 0x100) + ["print r4"])
row("rb vecbase own", printed(t, "r4") if alive else "died", "0x50",
    "VECBASE unchanged after a declined put h to ITS OWN arm -- a fall-through lands 0xb0")
#  IPL's write body stores nothing and prints "write to read-only PCCTWO_IPL; ignored"
#  once per process (#119 static).  A declined wide write never reaches it; a fall-through
#  prints it -- PSCALEADJ's shape at the twelfth block.  The message is the channel.
t, alive, how = session(setup(r6="0x0303") + program([ST_H(6, IPL)]))
row("hwr ipl noig", t.count("write to read-only PCCTWO_IPL"), 0,
    "a declined st.h to IPL never reaches the read-only print -- fall-through would")
#  The codex seat, pass 3: the MIRROR of the measured width edit.  `len != 1' -> `len == 2'
#  declines every halfword row here and lets a WORD write land -- every row above stayed
#  green under it.  One cardinality row over WORD writes closes that at all twelve blocks.
#  (Word writes to the counter arms are pcc2counter8's business and are not touched.)
t, alive, how = session(["put w 0x%x, 0x00000003" % (PCC2 + o) for _, o in BLOCKS12])
row("latch all w", t.count(DECL), 12,
    "one WORD write per BLOCK -> TWELVE announces: a `len == 2' guard anywhere drops it")
#  PASS 4 (glm, deepseek, codex): the rows drove widths {1,2,4} and the contract itself says
#  `put d' reaches with len 8, so a guard true on {2,4} and false on 8 (`len & 6', or
#  `len != 1 && len != 8') passed every row.  Twelve DWORD writes, twelve announces:
t, alive, how = session(["put d 0x%x, 0x0000000000000003" % (PCC2 + o) for _, o in BLOCKS12])
row("latch all d", t.count(DECL), 12,
    "one DWORD write per BLOCK -> TWELVE announces: an 8-byte exemption anywhere drops it")
#  And the de-escalation side, closed at all twelve: one LEGAL byte write per block must
#  announce NOTHING.  A guard grown to refuse bytes (`len != 1' -> `len != 0') at any of
#  the seven blocks without a per-arm `acc' row is visible only here.  Values: GENCTL keeps
#  bit 0x04 clear (pcc2c040kill); VECBASE's mask is 0xf0; the rest accept any byte.
#  *** MEASURED, part 3 and 3b: this row's first form used the debugger's `put b' and could
#  NOT SEE a guard grown to refuse bytes at PSCALEADJ -- 96/96 with the mutation PROVEN in the
#  source and the binary newer than it.  `put b' calls memory_rw directly with NO_EXCEPTIONS,
#  and that flag does not dispatch to a DM_DEFAULT device; `put h/w/d' go through the
#  store_Nbit_word helpers and do reach the arms.  So the operator path for BYTES is not a
#  path at all, and the row was vacuous by construction -- the CHANNEL rule's own failure,
#  caught by the table.  Guest `st.b' is legal at every offset (byte accesses skip the m88k
#  alignment check; `rb mask' stores a byte at 0x3f this way), so the accept side is pinned
#  from the GUEST at all twelve blocks, which is the stronger form anyway. ***
t, alive, how = session(setup(r5="0x10") + program([ST_B(5, o) for _, o in BLOCKS12]))
row("acc all", t.count(DECL), 0,
    "twelve legal guest byte stores, ZERO declines -- the accept side at every block")
row("acc all lv", how, "exit0", "...and the host survived all twelve byte stores")
#  PASS 4 (codex): `acc all' proves no DECLINE and survival; it does not prove the byte
#  reached the arm's BODY.  For the two print-only arms the body's own print is the proof:
t, alive, how = session(setup(r5="0x10") + program([ST_B(5, PSCALEADJ)]))
row("acc pscale ign", t.count("PSCALEADJ ignored"), 1,
    "a legal byte write to PSCALEADJ reaches its body -- the ignored print fires once")
t, alive, how = session(setup(r5="0x10") + program([ST_B(5, IPL)]))
row("acc ipl ro", t.count("write to read-only PCCTWO_IPL"), 1,
    "a legal byte write to IPL reaches its body -- the read-only print fires once")
#  The T1 labels of the two SHARED blocks (deepseek, pass 3): their readbacks above are at
#  the T2 offsets, so a fall-through reaching only the T1 half of a split block would leave
#  `op t1ctl dcl' at 1 with nothing reading T1CTL back.  Operator path, own readbacks:
#  (`want' is the value as the debugger PRINTS it -- 0x03 comes back as `0x3'.  The first
#  part-3 BASE run reddened this row on the fix for exactly that string mismatch, 95/96;
#  the value was right.  Re-measured in part 3b.)
for nm, off, pre, want in (("t1ctl", T1CTL, "0x03", "0x3"), ("t1icr", T1ICR, "0x13", "0x13")):
    t, alive, how = session(setup(r5=pre) + program([ST_B(5, off)])
                            + ["put h 0x%x, 0xaab8" % (PCC2 + off)]
                            + program([LD_BU(4, off)], at=CODE + 0x100) + ["print r4"])
    row("rb " + nm, printed(t, "r4") if alive else "died", want,
        "%s unchanged after a declined put h at the T1 label -- a fall-through lands 0xb8 & mask (RMW at TxCTL: 0)" % nm.upper())

# --------------------------------- IPL (guest-reachable, EVEN) and MASK (operator, odd)
#  IPL 0x3e: a halfword at 0x3e lands in the IPL arm.  Its write side is read-only (#119
#  "ignored"), so a wide write is declined by the WIDTH latch first and a readback cannot
#  tell the two refusals apart -- the channel is the message.
t, alive, how = session(setup() + program([I_ST_SCR, LD_H(4, IPL), I_LD_SCR]) + ["print r4"])
row("hrd ipl", how, "exit0", "ld.h IPL (EVEN, the SIXTH guest-reachable block) survives")
row("hrd ipl lv", printed(t, "r4") if alive else "died", "0x5a5a5a5a", "...and runs on")
row("hrd ipl nod", t.count(DECL), 0, "...and the wide READ of IPL is never declined")
t, alive, how = session(setup(r6="0x1234") + program([I_ST_SCR, ST_H(6, IPL), I_LD_SCR]) + ["print r4"])
row("hwr ipl", how, "exit0", "st.h IPL survives")
row("hwr ipl lv", printed(t, "r4") if alive else "died", "0x5a5a5a5a", "...and runs on")
row("hwr ipl dcl", t.count("write to PCCTWO_IPL " + DECL), 1,
    "...declined by the WIDTH latch (not the read-only one) -- the message is the channel")
#  MASK 0x3f: odd, operator path.  It is GENCTL's twin, so it gets GENCTL's readback: set
#  MASK to a known byte at the legal width, decline a wide write through the debugger,
#  then read the byte back through a program at a SECOND address.  A deleted guard stores
#  the wrong lane (0xbb); an accidental compose stores 0xaa.  reassert_interrupts on a
#  MASK byte write is harmless here: GENCTL's C040 bit is clear and nothing is pending.
t, alive, how = session(setup(r5="0x12") + program([ST_B(5, MASK)])
                        + ["put h 0x%x, 0xaabb" % (PCC2 + MASK)]
                        + program([LD_BU(4, MASK)], at=CODE + 0x100) + ["print r4"])
row("op mask", how, "exit0", "debugger put h at odd MASK survives")
row("op mask dcl", t.count("write to PCCTWO_MASK " + DECL), 1, "...and was declined once")
row("rb mask", printed(t, "r4") if alive else "died", "0x12",
    "MASK unchanged after the declined wide write -- GENCTL's twin gets GENCTL's readback")

# ---------------------------------------------------------------------- summary
print("NOROW  two device instances               -- mvme187 has ONE pcc2; per-instance latch state"
      " is by construction, not measured")
print("NOROW  pcc2c040kill                        -- a LEGAL byte write of 0x04 to GENCTL still ends"
      " the host; every GENCTL lane here keeps that bit clear")
print("NOROW  pcc2defaultkill / pcc2counter8      -- other arms, other rounds")
bad = [n for n, ok in rows if not ok]
print("PCC2W_RESULT=%d/%d" % (len(rows) - len(bad), len(rows)))
print("PCC2W_LABEL=%s" % LABEL)
if bad:
    print("PCC2W_RED=%s" % ",".join(bad))
print("PCC2W_PROBE_DONE")
