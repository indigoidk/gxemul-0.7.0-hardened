#!/usr/bin/env python3
"""DETECTOR for sh4pclock, which also carries the round's witness measurement.

Its rows assert the POST-fix state -- the write is declined, the host survives,
the refusal names itself once per timer, and the write does not land -- so it is
green after the fix and safe to gate.  The WITNESS is the recorded fact that this
same script scored 6/16 on the pre-fix build; a probe whose rows asserted the
pre-fix symptom would go red the day the fix landed, and gating it would
manufacture a regression.  The two roles are distinct and this file is the
second one.

The defect: one guest TCR store ended the host on machines that never set pclock.

THE CHAIN, four links, each read rather than assumed:

  1. The sh4 device is added BY THE CPU -- cpu_sh.c, `device_add(machine, "sh4")`
     -- so every arch-4 SH CPU carries the TCR handler whatever machine booted.
  2. Only TWO machines assign pclock: machine_dreamcast.c:51 (50000000) and
     machine_landisk.c:81 (33333333).
  3. But FIVE machine sites name an arch-4 CPU: dreamcast and landisk (which set
     it), plus machine_hpcsh.c:89, and machine_test.c:535 and :541 -- which are
     TWO SEPARATE MACHINES, baresh and testsh.  (An earlier draft of this line
     said FOUR, two sentences above the paragraph that announces the correction.
     Those two are the strdup lines; the MACHINE_DEFAULT_CPU labels are :533/:539.)
  4. So on -e jornada680, -E baresh and -E testsh, pclock is 0, and BEFORE #459 the
     TCR write arm ran `fatal(...); exit(1);`.  (Past tense on purpose: that code is
     gone, and citing its old line numbers here would rot on the next edit.)

*** THREE machine types, not two, and the brief that opened this round said two. ***
Two pass-1 seats independently caught it: `machine_test.c:535` is
`MACHINE_DEFAULT_CPU(baresh)` and `:541` is `MACHINE_DEFAULT_CPU(testsh)` -- two
separate registered machines inside one file.  FIVE registered SH machine types name
an arch-4 CPU; dreamcast and landisk assign pclock, the other three do not.

Rung 3 by the witness ladder: a real guest instruction through real address
decode, on an UNMODIFIED in-tree machine description.  Nothing is added to reach
the site -- the site is reached by an ordinary store to 0xffd80010.

*** THE CONTROLS RUN IN THEIR OWN SESSIONS AND DO NOT TOUCH TCR. ***  A previous
probe in this tree put its "does the session come up" control in the same session
as the trigger, so the control exercised the defect and reported DEAD on a correct
build.  Here `live` and `devsig` never write TCR, so a red `kill` row cannot be
confused with a broken session.

The device signature is IPRD's reset value H'DA74 (SH7750 Hardware Manual
Rev.7.00, stated at :39856, :40194 and :48567).  RAM would answer differently,
and an unmapped address would report `non-existant paddr` -- so a correct read
proves the sh4 device is present and serving, which is link 1 of the chain.
"""
import os
import pty
import re
import select
import sys
import time

BIN = sys.argv[1] if len(sys.argv) > 1 else "../../build/gxemul"
KERNEL = sys.argv[2] if len(sys.argv) > 2 else "../../_images/openbsd76-landisk-bsd.rd"

#  Every SH machine here needs a file argument to construct at all -- bare
#  `-e jornada680` exits with "No filename given" before any device is added.
#  The kernel is only a construction argument: nothing boots, the debugger
#  stops cold, and the guest instruction is planted by hand.  hpcsh also warns
#  about missing -X, which is harmless for a cold-debugger probe.

#  *** EACH MACHINE NEEDS ITS OWN ADDRESS, AND GETTING THIS WRONG VOIDS THE ROW
#  SILENTLY. ***  hpcsh RAM is 32 MB at 0x0c000000 (machine_hpcsh.c:77-80 -- :76 is
#  the comment line above the dev_ram_init calls), so P1 is
#  0x8c000000; testsh has RAM at physical 0, so P1 is 0x80000000.  A previous
#  attempt at this defect reused one machine's scratch on the other, the store
#  never landed, and the machine read as NOT REPRODUCING -- which is a false
#  NEGATIVE, the direction that quietly closes a live defect.
CODE = {"jornada680": 0x8c001000, "testsh": 0x80001000,
        "baresh": 0x80001000, "landisk": 0x8c001000,
        "dreamcast": 0x8c001000}
#  Only jornada680 is listed: the liveness control runs on that machine alone, and a
#  seat flagged the other entries as dead weight that reads like coverage.
SCRATCH = {"jornada680": 0x8c002000}

SH4_TCR0 = 0xffd80010          # Timer Control Register 0 (sh4_tmureg.h:54)
SH4_TCR1 = 0xffd8001c          # Timer Control Register 1 (sh4_tmureg.h:57)
SH4_IPRD = 0xffd00010          # reset value 0xda74 -- the device signature
IPRD_RESET = 0xda74
LIVE = 0x12345678              # asymmetric on purpose: a palindrome once hid a
                               # byte-order defect in another probe's own parser

MOV_W_R8_AT_R7 = 0x2781        # mov.w r8,@r7
MOV_L_R8_AT_R7 = 0x2782        # mov.l r8,@r7
MOV_L_AT_R1_R2 = 0x6212        # mov.l @r1,r2
MOV_W_AT_R1_R2 = 0x6211        # mov.w @r1,r2

TCR_TPSC_P4 = 0x0000           # sh4_tmureg.h:85
TCR_TPSC_P16 = 0x0001          # sh4_tmureg.h:86
LANDISK_PCLOCK = 33333333      # machine_landisk.c:81
DREAMCAST_PCLOCK = 50000000    # machine_dreamcast.c:51
LANDISK_CODE = 0x8c001000
DREAMCAST_CODE = 0x8c001000    # dreamcast RAM is 16 MB at 0x0c000000
BRA_SELF = 0xaffe
NOP = 0x0009

rows = []


def row(name, got, want, note=""):
    ok = (got == want)
    rows.append((name, ok))
    print("%-14s %-12s %-12s %-34s %s" % (name, got, want, note,
                                          "ok" if ok else "FAIL"))
    return ok


def session(cmds, machine="jornada680", flag="-e", settle=6.0, spin=2.0):
    """Run one cold-debugger session.  Returns (transcript, process_survived)."""
    pid, fd = pty.fork()
    if pid == 0:
        #  *** DREAMCAST NEEDS -x OR IT EXITS BEFORE THE DEBUGGER PROMPT. ***
        #  It brings up TWO console inputs -- "SH4 SCIF" and "maple" -- and
        #  console.c:994-1007 makes that fatal unless allow_slaves is set.  The
        #  first draft of the dreamcast row read "died" and that was NOT the
        #  defect: it is the same shape as the trigger rows, so it would have
        #  been scored as a second reproduction.  -x only sets allow_slaves
        #  (console.c:985 returns immediately); no xterm is spawned, because a
        #  cold-debugger probe never drives a slave console.  Verified headless.
        args = [BIN, "-V"]
        if machine == "dreamcast":
            args.append("-x")
        args += [flag, machine, "-M", "64", KERNEL]
        os.execv(BIN, args)
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
        #  Only the LAST command gets the long wait; applying it to every command
        #  once made a single session take ~510 s instead of 30.
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
    try:
        _, st = os.waitpid(pid, 0)
    except OSError:
        st = 0
    return buf, alive


def dumped(t, addr):
    """Read back a word the guest stored, from the debugger's own dump."""
    m = re.search(r"%08x[^\r\n]*?\b([0-9a-f]{8})\b" % addr, t, re.I)
    return ("0x" + m.group(1).lower()) if m else "absent"


def printed(t, reg):
    m = re.search(r"print\s+%s\s*\r?\n\s*(0x[0-9a-f]+)" % reg, t)
    return m.group(1) if m else "absent"


def store_code(at, reg, value, op=MOV_W_R8_AT_R7):
    """r7 <- reg, r8 <- value, one store, then spin."""
    return ["r7=0x%x" % reg, "r8=0x%08x" % value,
            "put h 0x%x, 0x%04x" % (at, op),
            "put h 0x%x, 0x%04x" % (at + 2, BRA_SELF),
            "put h 0x%x, 0x%04x" % (at + 4, NOP),
            "pc=0x%x" % at]


#  ---------------------------------------------------------------- controls
#  NEITHER control writes TCR.  If the trigger row goes red they stay green,
#  which is what makes the red attributable.

#  Read back through a GUEST LOAD, not the debugger's dump.  The first draft
#  dumped memory and compared against 0x12345678; it got 0x78563412, because a
#  byte dump is endian-ordered and the comparison was not.  A guest load and a
#  register read are endian-neutral by construction, and the asymmetric value is
#  what made the mistake visible at all.
AT = CODE["jornada680"]
t, alive = session(["r7=0x%x" % SCRATCH["jornada680"], "r8=0x%08x" % LIVE, "r1=0x%x" % SCRATCH["jornada680"],
                    "r2=0",
                    "put h 0x%x, 0x%04x" % (AT, MOV_L_R8_AT_R7),
                    "put h 0x%x, 0x%04x" % (AT + 2, MOV_L_AT_R1_R2),
                    "put h 0x%x, 0x%04x" % (AT + 4, BRA_SELF),
                    "put h 0x%x, 0x%04x" % (AT + 6, NOP),
                    "pc=0x%x" % AT, "step 2", "print r2"])
row("live", printed(t, "r2") if alive else "died", "0x%x" % LIVE,
    "RAM: guest store then guest load")

t, alive = session(["r1=0x%x" % SH4_IPRD, "r2=0",
                    "put h 0x%x, 0x%04x" % (AT, MOV_L_AT_R1_R2),
                    "put h 0x%x, 0x%04x" % (AT + 2, BRA_SELF),
                    "put h 0x%x, 0x%04x" % (AT + 4, NOP),
                    "pc=0x%x" % AT, "step 1", "print r2"])
got = printed(t, "r2") if alive else "died"
row("devsig", ("0x%x" % (int(got, 16) & 0xffff)) if got.startswith("0x") else got,
    "0x%x" % IPRD_RESET, "IPRD reset value, served by the sh4 device")

print("SH_PCLOCK_CONTROL=%s" % ("OK" if all(ok for _, ok in rows) else "DEAD"))

#  ---------------------------------------------------------------- the trigger
#  One 16-bit store to TCR0.  On the committed build this ends the host process.
#  [#556, 2026-10-02 -- a records correction; the text above is kept as it was written] When pclock is 0 the TCR
#  write is ignored after a one-time fatal print. These rows require survived and quiet.  (regress23:F11:
#  regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md)

KILL = re.compile(r"pclock must be set", re.I)

#  THREE machines, not two.  A pass-1 seat caught that the brief had
#  attributed machine_test.c:535 to testsh; :535 is MACHINE_DEFAULT_CPU(baresh)
#  and :541 is MACHINE_DEFAULT_CPU(testsh) -- two separate machines, both
#  naming SH7750 and neither assigning pclock.  Five sites in the tree name an
#  arch-4 SH CPU; dreamcast and landisk set pclock, these three do not.
for mach, flag, label in (("jornada680", "-e", "hpcsh"),
                          ("baresh", "-E", "baresh"),
                          ("testsh", "-E", "testsh")):
    t, alive = session(store_code(CODE[mach], SH4_TCR0, 0x0000) + ["step 1"],
                       machine=mach, flag=flag)
    #  `alive` is the discriminator: exit(1) closes the pty, so the write of the
    #  NEXT command raises OSError.  The diagnostic text is the corroboration --
    #  it must BOTH die and say why, or the row is measuring something else.
    row("%s kill" % label, "survived" if alive else "died", "survived",
        "one mov.w to SH4_TCR0 (0xffd80010)")
    row("%s diag" % label, "quiet" if not KILL.search(t) else "pclock-fatal",
        "quiet", "the INTERNAL ERROR text must be gone")

#  ---------------------------------------------------------------- accept side
#
#  *** THE DE-ESCALATION CLAUSE'S COST, PAID UP FRONT. ***
#
#  Whatever this round does about the machines that never set pclock, it is a
#  fatal->survive change at a guard, and the project's rule is that such a fix
#  DELETES the accidental tripwire that made guard growth self-announcing.
#  Before the change, widening this predicate meant exit(1) on the first legal
#  write -- unmissable.  After it, the same edit means a silently refused write
#  and NOTHING anywhere notices.  So the accept side has to be pinned.
#
#  These rows are OPTION-INDEPENDENT: landisk assigns pclock = 33333333
#  (machine_landisk.c:81) and must keep accepting TCR writes no matter what is
#  decided for hpcsh and testsh.  They are GREEN on the committed build by
#  construction -- an accept row that is red before the fix is measuring the
#  defect, not the accept side.
#
#  Two channels, because one is not enough.  The frequency print is computed
#  from pclock and so proves the RATE was installed; the TCR read-back proves
#  the WRITE LANDED at all.  #447's own comment cites the read-back as the way
#  "the guest can see the rejection", so it is the channel a refusal moves.

t, alive = session(["r7=0x%x" % SH4_TCR0, "r8=0x%04x" % TCR_TPSC_P4,
                    "put h 0x%x, 0x%04x" % (LANDISK_CODE, MOV_W_R8_AT_R7),
                    "put h 0x%x, 0x%04x" % (LANDISK_CODE + 2, BRA_SELF),
                    "put h 0x%x, 0x%04x" % (LANDISK_CODE + 4, NOP),
                    "pc=0x%x" % LANDISK_CODE, "step 1"],
                   machine="landisk", flag="-E")
want_hz = LANDISK_PCLOCK / 4.0
m = re.search(r"sh4 timer 0 clock set to ([0-9.]+) Hz", t)
row("accept hz", (m.group(1) if m else "absent") if alive else "died",
    "%f" % want_hz, "landisk TPSC=P4 -> pclock/4")

#  Read TCR0 back through a guest load, in the same session as the write, so
#  the two halves cannot disagree about which store they are describing.
t, alive = session(["r7=0x%x" % SH4_TCR0, "r8=0x%04x" % TCR_TPSC_P16,
                    "r1=0x%x" % SH4_TCR0, "r2=0",
                    "put h 0x%x, 0x%04x" % (LANDISK_CODE, MOV_W_R8_AT_R7),
                    "put h 0x%x, 0x%04x" % (LANDISK_CODE + 2, MOV_W_AT_R1_R2),
                    "put h 0x%x, 0x%04x" % (LANDISK_CODE + 4, BRA_SELF),
                    "put h 0x%x, 0x%04x" % (LANDISK_CODE + 6, NOP),
                    "pc=0x%x" % LANDISK_CODE, "step 2", "print r2"],
                   machine="landisk", flag="-E")
got = printed(t, "r2") if alive else "died"
row("accept tcr", ("0x%x" % (int(got, 16) & 0xffff)) if got.startswith("0x") else got,
    "0x%x" % TCR_TPSC_P16, "landisk: the write LANDS and reads back")

#  *** TWO CLOCK VALUES, NOT ONE, AND THAT IS THE WHOLE POINT OF THE SECOND. ***
#  A pass-1 seat observed that a single accept row pinned at 33.33 MHz is passed
#  by a mutant that HARDCODES 33333333 in place of cpu->cd.sh.pclock -- the row
#  cannot tell "reads the machine's clock" from "happens to agree with landisk".
#  Dreamcast's 50 MHz is the discriminator: a hardcode cannot satisfy both.
t, alive = session(["r7=0x%x" % SH4_TCR0, "r8=0x%04x" % TCR_TPSC_P4,
                    "put h 0x%x, 0x%04x" % (DREAMCAST_CODE, MOV_W_R8_AT_R7),
                    "put h 0x%x, 0x%04x" % (DREAMCAST_CODE + 2, BRA_SELF),
                    "put h 0x%x, 0x%04x" % (DREAMCAST_CODE + 4, NOP),
                    "pc=0x%x" % DREAMCAST_CODE, "step 1"],
                   machine="dreamcast", flag="-E")
m = re.search(r"sh4 timer 0 clock set to ([0-9.]+) Hz", t)
row("accept dc hz", (m.group(1) if m else "absent") if alive else "died",
    "%f" % (DREAMCAST_PCLOCK / 4.0), "dreamcast TPSC=P4 -> pclock/4")

#  Landisk had BOTH channels and dreamcast only the frequency -- asymmetric
#  coverage on the two rows that carry the whole de-escalation clause, caught by
#  a measuring seat.  Both machines now pin both channels.
t, alive = session(["r7=0x%x" % SH4_TCR0, "r8=0x%04x" % TCR_TPSC_P16,
                    "r1=0x%x" % SH4_TCR0, "r2=0",
                    "put h 0x%x, 0x%04x" % (DREAMCAST_CODE, MOV_W_R8_AT_R7),
                    "put h 0x%x, 0x%04x" % (DREAMCAST_CODE + 2, MOV_W_AT_R1_R2),
                    "put h 0x%x, 0x%04x" % (DREAMCAST_CODE + 4, BRA_SELF),
                    "put h 0x%x, 0x%04x" % (DREAMCAST_CODE + 6, NOP),
                    "pc=0x%x" % DREAMCAST_CODE, "step 2", "print r2"],
                   machine="dreamcast", flag="-E")
got = printed(t, "r2") if alive else "died"
row("accept dc tcr", ("0x%x" % (int(got, 16) & 0xffff)) if got.startswith("0x") else got,
    "0x%x" % TCR_TPSC_P16, "dreamcast: the write LANDS and reads back")

#  ------------------------------------------------- the decline is OBSERVABLE
#
#  *** THE `diag` ROWS ABOVE ONLY CHECK THAT THE OLD TEXT IS GONE, AND ON THEIR
#  OWN THAT IS VACUOUS. ***  A mutant that deletes the whole guard body and just
#  falls through -- or one that declines SILENTLY with no diagnostic at all --
#  passes every row above.  #459 removed a host-fatal guard, and the project's
#  de-escalation clause says such a fix DELETES the accidental tripwire that made
#  the behaviour self-announcing.  These four rows are that tripwire, rebuilt on
#  purpose rather than left to a future round.

AT = CODE["jornada680"]
SAYS = re.compile(r"no peripheral clock configured for this machine")


def tcr_writes(regs, at=AT):
    """Plant N back-to-back 16-bit TCR stores, then spin."""
    cmds, off = [], 0
    for k, reg in enumerate(regs):
        cmds += ["r%d=0x%x" % (7 - k, reg)]
    cmds += ["r8=0x0000"]
    for k, reg in enumerate(regs):
        cmds += ["put h 0x%x, 0x%04x" % (at + off, 0x2081 | ((7 - k) << 8))]
        off += 2
    cmds += ["put h 0x%x, 0x%04x" % (at + off, BRA_SELF),
             "put h 0x%x, 0x%04x" % (at + off + 2, NOP),
             "pc=0x%x" % at, "step %d" % len(regs)]
    return cmds


t, alive = session(tcr_writes([SH4_TCR0]))
row("hpcsh says", ("said" if SAYS.search(t) else "silent") if alive else "died",
    "said", "the refusal must NAME itself, once")

t, alive = session(tcr_writes([SH4_TCR0, SH4_TCR0]))
row("hpcsh once", ("%d" % len(SAYS.findall(t))) if alive else "died", "1",
    "SAME timer twice -> exactly one line")

t, alive = session(tcr_writes([SH4_TCR0, SH4_TCR1]))
row("hpcsh pertmr", ("%d" % len(SAYS.findall(t))) if alive else "died", "2",
    "TCR0 then TCR1 -> two lines, one per timer")

#  #447's own comment cites the read-back as how "the guest can see the
#  rejection".  This is the channel a guest has; the diagnostic is the operator's.
t, alive = session(["r7=0x%x" % SH4_TCR0, "r8=0x%04x" % TCR_TPSC_P16,
                    "r1=0x%x" % SH4_TCR0, "r2=0xffff",
                    "put h 0x%x, 0x%04x" % (AT, MOV_W_R8_AT_R7),
                    "put h 0x%x, 0x%04x" % (AT + 2, MOV_W_AT_R1_R2),
                    "put h 0x%x, 0x%04x" % (AT + 4, BRA_SELF),
                    "put h 0x%x, 0x%04x" % (AT + 6, NOP),
                    "pc=0x%x" % AT, "step 2", "print r2"])
got = printed(t, "r2") if alive else "died"
row("hpcsh unlatch", ("0x%x" % (int(got, 16) & 0xffff)) if got.startswith("0x") else got,
    "0x0", "the refused write must NOT land: TCR reads back 0")

n = sum(1 for _, ok in rows if ok)
print("SH_PCLOCK_RESULT=%d/%d" % (n, len(rows)))
print("SH_PCLOCK_VECTOR=" + ",".join(("1" if ok else "0") for _, ok in rows))
