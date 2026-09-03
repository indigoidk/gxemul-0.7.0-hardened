#!/usr/bin/env python3
"""pcc2widthkills DETECTOR -- the twelve width-guard blocks in DEVICE_ACCESS(pcc2).

WHAT THE FIX DID.  Twelve `if (len != 1) { fatal(...); exit(1); }' blocks (ten kills and
two #119 function-static latches) ended the host on a guest-chosen access width.  The
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
    * reinstatement of the kill at any of the five GUEST-reachable blocks (survival
      rows paired with a liveness observable, because exit status cannot tell
      "declined and quit" from "died with status 0");
    * reinstatement at any of the seven OPERATOR-reachable blocks, through the
      debugger's `put h' at an odd address -- MEASURED to warn and store and kill
      (artifacts/pcc2widthkills/operator_reach_20260903.out);
    * *** DELETE instead of decline on the write side -- the lane hazard.  `st.h
      0xAABB' to GENCTL must leave GENCTL unchanged; a bare deletion stores 0xBB,
      VECBASE's lane, because (uint8_t) idata is the HIGHEST-address byte ***;
    * an accidental per-lane compose (GENCTL would read 0xAA);
    * the value a wide READ composes -- lane order and width -- not merely survival;
    * loss of the latch in either direction: dropped `|=' floods (same site twice
      must announce ONCE), and one bit shared across blocks silences (two sites must
      announce TWICE);
    * the de-escalation clause: byte writes at the LEGAL width at every reachable
      arm still land, read back through each arm's own mask, with NO decline message.

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
#  the five GUEST-reachable blocks (even offsets) and the seven OPERATOR-reachable ones
GENCTL, T2CTL, T2ICR, SCCERR, SCCTX = 0x02, 0x16, 0x1a, 0x1c, 0x1e
VECBASE, PSCALEADJ, T1CTL, T1ICR, SCCICR, SCCRX, SCSIICR = 0x03, 0x15, 0x17, 0x1b, 0x1d, 0x1f, 0x2f
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
    #  r6 = the halfword to store: both lanes keep GENCTL's bit 0x04 CLEAR (pcc2c040kill)
    t, alive, how = session(setup(r6="0xaabb") + program([I_ST_SCR, ST_H(6, off), I_LD_SCR]) + ["print r4"])
    row("hwr " + nm, how, "exit0", "st.h %s (aligned halfword WRITE) survives" % nm.upper())
    row("hwr %s lv" % nm, printed(t, "r4") if alive else "died", "0x5a5a5a5a", "...and runs on")
#  SCCERR is the one 4-aligned block: word read AND write
t, alive, how = session(setup() + program([I_ST_SCR, LD_W(4, SCCERR), I_LD_SCR]) + ["print r4"])
row("wrd sccerr", how, "exit0", "ld SCCERR (the one 4-aligned block) survives")
row("wrd sccerr lv", printed(t, "r4") if alive else "died", "0x5a5a5a5a", "...and runs on")
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

# ------------------------------------------------------------------ latch rows
t, alive, how = session(setup(r6="0xaabb") + program([ST_H(6, GENCTL), ST_H(6, GENCTL)]))
row("latch same", t.count("write to PCCTWO_GENCTL " + DECL), 1,
    "same block twice -> ONE announce -- kills a dropped |= (flood)")
t, alive, how = session(setup(r6="0x0303") + program([ST_H(6, GENCTL), ST_H(6, T2CTL)]))
row("latch two", t.count(DECL), 2,
    "two blocks -> TWO announces -- kills a bit shared across blocks")

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
