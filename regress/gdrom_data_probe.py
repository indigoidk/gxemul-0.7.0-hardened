#!/usr/bin/env python3
"""DETECTOR for sh4gdromexit, carrying the round's witness measurement.

*** THE ARM HAS FIVE exit(1) SITES, NOT THREE, AND AN EARLIER DRAFT OF THIS
DOCSTRING HID TWO BEHIND ELLIPSES. ***  :308 width, :315 read-with-no-data,
:334 "Read too much from GDROM_DATA", :340 "Too much GDROM_DATA?", :352
write-when-not-waiting.  A pass-1 seat caught it, and the count matters: the
de-escalation clause enumerates EVERY predicate that used to gate death, so a
false count makes that enumeration incomplete by construction.

THIS ROUND TAKES FOUR OF THE FIVE.  An earlier draft of this docstring said
three and FILED :334, on the reading that witnessing it needed a new probe
shape and a new oracle.  That was OVERTURNED BY MEASUREMENT: the existing
session/run helpers plus a three-instruction loop under `step N` reach it --
same rung, same oracle -- so it joined, and the `overread` rows below drive it.
:315 and :334 are one predicate family ("read when there is nothing to give"),
and fixing one while the other stayed fatal would leave a device where a
declined read is safe in one state and lethal in another.

:340 is assessed UNREACHABLE and left alone: COND=0xa0 is the only setter of
busy|0x08 and it zeroes cmd_count, GDROM_BUSY writes only clear, and cmd_count
steps by 2 from 0 with ==12 clearing busy -- so >=12 with busy set has no path.
Three constructed paths were measured against it and all reached :352.

*** THE SITE LINE NUMBERS ABOVE ARE PRE-FIX (at HEAD e4390ea). *** The fix adds
lines above them, so they do not resolve in the post-fix tree -- the same trap
this project hit twice in #459, recorded here rather than silently rotting.

THE FOUR THIS ROUND TAKES are separate `exit(1)` sites in ONE register's arm --
GDROM_DATA, physical 0x005f7080 on the Dreamcast -- each reached by a SINGLE
ordinary guest instruction on a freshly constructed machine.

  1. WIDTH.  `if (len != sizeof(uint16_t)) { fatal("Non-16bit GDROM data
     access? TODO"); exit(1); }` -- so a byte or longword access, READ OR
     WRITE, ends the host process.  No device state is required at all.
  2. READ WITH NO DATA.  `if (!(d->cond & COND_DATA_AVAIL))` -> exit(1).
     `cond` is zero on a fresh device, so the FIRST 16-bit read kills.
  3. WRITE WHEN NOT EXPECTING DATA.  `if (d->busy & 0x08)` else -> exit(1).
     `busy` is zero on a fresh device, so the FIRST 16-bit write kills.

So every access width and both directions are fatal on a fresh GDROM: there is
no legal first touch of this register.

*** WHAT THAT DOES **NOT** MEAN, because an earlier draft overclaimed it. ***
It does NOT mean a real driver cannot avoid this.  Drivers probe STAT, BUSY and
COND -- not the data FIFO -- and the one driver this model was written against
(NetBSD's dreamcast gdrom.c, cited by the device file itself) writes COND=0xa0
before ever touching DATA, so ITS first touch is legal by construction.  The
true statement is narrower and still severe: no device state makes a first
touch of DATA legal, and any access outside the exact NetBSD-shaped sequence
ends the host process.

*** DREAMCAST NEEDS -x OR IT NEVER REACHES THE DEBUGGER PROMPT. ***  It brings
up TWO console inputs, "SH4 SCIF" and "maple", and console.c:994-1007 makes
that fatal unless allow_slaves is set.  This cost #459 a false positive: the
session died for a CONFIGURATION reason and printed the same "died" the defect
prints.  -x only sets the flag (console.c:985 returns immediately) and spawns
no xterm, because a cold-debugger probe never drives a slave console.

Rung 3 by the witness ladder: a real guest instruction through real address
decode, on an UNMODIFIED in-tree machine description.  Nothing is added to
reach the site.

CONTROLS RUN IN THEIR OWN SESSIONS AND NEVER TOUCH GDROM_DATA, so a red
trigger row cannot be confused with a broken session.
"""
import os
import pty
import re
import select
import sys
import time

BIN = sys.argv[1] if len(sys.argv) > 1 else "../../build/gxemul"
KERNEL = sys.argv[2] if len(sys.argv) > 2 else "../../_images/openbsd76-landisk-bsd.rd"

#  Dreamcast RAM: 16 MB at 0x0c000000 (machine_dreamcast.c:138), so P1 is
#  0x8c000000.  The loaded ELF lands at 0x8c002000 and grows up, so plant below.
#
#  The default kernel is GZIPPED on disk and file.c:307-312 refuses gzip with
#  exit(1) -- which reads as "this probe cannot run".  It can: the SEC-only
#  wrapper in emul.c:75-110 fork/execs `gunzip -c` first (deliberately not
#  system()).  Noted because a pass-1 seat re-derived that false alarm.
#
#  -M 64 is passed for uniformity with the other SH probes ONLY.  Dreamcast RAM
#  is a fixed 16 MB dev_ram regardless, so the flag changes nothing here -- said
#  out loud so a witness-clause (iii) reader need not rule out reach-laundering
#  by a machine parameter.
CODE = 0x8c001000
SCRATCH = 0x8c001800

GDROM_DATA = 0xa05f7080        # 0x005f7000 + 0x80, via P2 (uncached)
GDROM_BUSY = 0xa05f7018        # 0x005f7000 + 0x18 -- a plain read of d->busy
SH4_IPRD = 0xffd00010          # reset value 0xda74 -- the SH4 device signature
IPRD_RESET = 0xda74
LIVE = 0x12345678

MOV_B_R8_AT_R7 = 0x2780
MOV_W_R8_AT_R7 = 0x2781
MOV_L_R8_AT_R7 = 0x2782
MOV_B_AT_R1_R2 = 0x6210
MOV_W_AT_R1_R2 = 0x6211
MOV_L_AT_R1_R2 = 0x6212
BRA_SELF = 0xaffe
NOP = 0x0009

rows = []


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
    try:
        os.waitpid(pid, 0)
    except OSError:
        pass
    return buf, alive


def printed(t, reg):
    m = re.search(r"print\s+%s\s*\r?\n\s*(0x[0-9a-f]+)" % reg, t)
    return m.group(1) if m else "absent"


def load(op, reg, at=CODE):
    """Plant ONE load from `reg` into r2, then read r2 back."""
    return ["r1=0x%x" % reg, "r2=0",
            "put h 0x%x, 0x%04x" % (at, op),
            "put h 0x%x, 0x%04x" % (at + 2, BRA_SELF),
            "put h 0x%x, 0x%04x" % (at + 4, NOP),
            "pc=0x%x" % at, "step 1", "print r2"]


#  ---------------------------------------------------------------- controls
t, alive = session(["r7=0x%x" % SCRATCH, "r8=0x%08x" % LIVE, "r1=0x%x" % SCRATCH, "r2=0",
                    "put h 0x%x, 0x%04x" % (CODE, MOV_L_R8_AT_R7),
                    "put h 0x%x, 0x%04x" % (CODE + 2, MOV_L_AT_R1_R2),
                    "put h 0x%x, 0x%04x" % (CODE + 4, BRA_SELF),
                    "put h 0x%x, 0x%04x" % (CODE + 6, NOP),
                    "pc=0x%x" % CODE, "step 2", "print r2"])
row("live", printed(t, "r2") if alive else "died", "0x%x" % LIVE,
    "RAM: guest store then guest load")

t, alive = session(load(MOV_L_AT_R1_R2, SH4_IPRD))
g = printed(t, "r2") if alive else "died"
row("devsig", ("0x%x" % (int(g, 16) & 0xffff)) if g.startswith("0x") else g,
    "0x%x" % IPRD_RESET, "SH4 IPRD reset value -- device dispatch works")

#  GDROM-SPECIFIC mapping proof: a plain read of d->busy.  It answers 0, which
#  is weak as a VALUE -- but an unmapped address answers "non-existant paddr"
#  instead, so a clean 0 proves the GDROM device itself is registered and
#  serving.  That is the claim this row makes, and no more.
t, alive = session(load(MOV_L_AT_R1_R2, GDROM_BUSY))
g = printed(t, "r2") if alive else "died"
row("gdrom map", ("mapped" if g.startswith("0x") else g) if alive else "died",
    "mapped", "GDROM_BUSY read is served, not a paddr fault")

print("GDROM_CONTROL=%s" % ("OK" if all(ok for _, ok in rows) else "DEAD"))

#  ---------------------------------------------------------------- triggers
#
#  *** THE FIRST VERSION OF THESE ROWS WAS INVERTED, AND A MEASURING SEAT
#  CAUGHT IT BEFORE ANY CODE WAS WRITTEN. ***
#
#  They asserted that the old fatal() TEXT MUST BE ABSENT.  But the fix this
#  round has agreed -- the #447/#459 shape -- KEEPS the diagnostic and drops
#  only the exit(1).  So the old rows PUNISHED THE INTENDED FIX AND REWARDED
#  DELETING THE REGISTER ARM.  Measured across six builds: the arm replaced by
#  `odata = 0xffff; break;` scored 13/13, while the real fix scored 8/13.
#
#  Re-pinned in ORACLE-CORRECTION ORDER: these expectations are written FIRST
#  and measured RED on the committed build, and only then does the code change.
#  Same scripts, opposite colour -- without that red, a re-pin is indistinguish-
#  able from fitting the test to the binary.
#
#  THE SHAPE THAT DISCRIMINATES: drive the SAME site TWICE in ONE session.
#    pre-fix        -> DIES on the first access                     (red)
#    correct fix    -> survives, diagnostic appears EXACTLY ONCE    (green)
#    deleted arm    -> survives, diagnostic appears ZERO times      (red)
#  A survival-only oracle cannot tell the last two apart; the count can.

#  These match the SHIPPED diagnostics, and the first re-pin got that wrong --
#  it kept hunting the pre-fix strings, so every count row read 0 against a
#  correct build.  Re-pointing a regex at text the fix emits is one step from
#  fitting the test to the binary, so the guard is unchanged and mechanical:
#  THE SAME SCRIPT MUST STILL MEASURE THE PRE-FIX BUILD RED.  It does -- there
#  the process dies on the first access, so the count is "died", not a number.
#  A silent-decline mutant reads 0 and is red for a different reason.
#  These match the SHIPPED diagnostic strings.  A seat ruled on the discipline
#  question this raises: a re-pointed regex is NOT made honest by the pre-fix
#  build going red, because pre-fix it dies by PROCESS DEATH before any count is
#  taken -- death-red cannot tell "matches the correct text" from "matches any
#  survival".  What defends it is the SURVIVING-BUT-WRONG negative control: a
#  deleted arm survives and emits nothing, so the exactly-once counts go red.
#  Those rows are live, so the re-point is honest; saying so is the point.
SAYS = {
    "width":   re.compile(r"non-16bit GDROM_DATA access"),
    "nodata":  re.compile(r"read from GDROM_DATA with no data"),
    "notwait": re.compile(r"write to GDROM_DATA while not waiting"),
    "overread": re.compile(r"read past the end of the GDROM_DATA buffer"),
}


#  *** PLANT BOTH ACCESSES CONTIGUOUSLY AND STEP BOTH. ***
#
#  The first draft of these rows set pc to the SECOND site and `step 1`, so
#  ONLY ONE ACCESS EVER RAN -- which made every "twice" row VACUOUS: it read a
#  count of 1 whether the latch worked or not.  It was caught only because the
#  two-DIFFERENT-sites row wanted 2 and kept reading 1.  A row that cannot tell
#  "the latch suppressed the second" from "the second never happened" is not a
#  latch row at all.
def pair(first, second, at=CODE):
    """Two guest accesses back to back, then a self-branch, stepped together.

    `first`/`second` are (opcode, setup-commands) -- the setup is hoisted so
    both instructions are planted adjacently and one `step 2` runs both.
    """
    op1, setup1 = first
    op2, setup2 = second
    return setup1 + setup2 + [
        "put h 0x%x, 0x%04x" % (at, op1),
        "put h 0x%x, 0x%04x" % (at + 2, op2),
        "put h 0x%x, 0x%04x" % (at + 4, BRA_SELF),
        "put h 0x%x, 0x%04x" % (at + 6, NOP),
        "pc=0x%x" % at, "step 2"]


ST = ["r7=0x%x" % GDROM_DATA, "r8=0x00005a5a"]     # store setup
LD = ["r1=0x%x" % GDROM_DATA, "r2=0"]              # load setup

#  *** THE LOAD VARIANTS ARE NOT DECORATION -- LOSING THEM COST A LIVE ESCAPE. ***
#  Pass 1 had them; the pass-2 rebuild wrapped the width rows around STORES only,
#  and a seat immediately named the mutant that walks through the gap: restore
#  exit(1) on WRONG-WIDTH READ ONLY.  Every remaining row is a store, a 16-bit
#  access, or never touches the register, so it scored a clean 14/14 while one
#  guest MOV.B *read* from 0xa05f7080 still ended the host.
for label, op, setup, key, note in (
        ("w8 store", MOV_B_R8_AT_R7, ST, "width", "8-bit store x2: wrong WIDTH"),
        ("w32 store", MOV_L_R8_AT_R7, ST, "width", "32-bit store x2: wrong WIDTH"),
        ("w8 load", MOV_B_AT_R1_R2, LD, "width", "8-bit LOAD x2: wrong WIDTH, read side"),
        ("w32 load", MOV_L_AT_R1_R2, LD, "width", "32-bit LOAD x2: wrong WIDTH, read side"),
        ("w16 load", MOV_W_AT_R1_R2, LD, "nodata", "16-bit load x2: no data"),
        ("w16 store", MOV_W_R8_AT_R7, ST, "notwait", "16-bit store x2: not waiting")):
    t, alive = session(pair((op, setup), (op, [])))
    row(label, "survived" if alive else "died", "survived", note)
    row(label.replace(" ", "") + " x1",
        ("%d" % len(SAYS[key].findall(t))) if alive else "died", "1",
        "SAME site TWICE -> diagnostic exactly once")

#  Two genuinely independent sites, both 16-bit ON PURPOSE.  An earlier draft
#  paired an 8-bit store with a 16-bit one and could never reach 2, because the
#  width guard LOGS AND CONTINUES -- that single 8-bit store falls through and
#  touches TWO sites at once, latching both before the second access runs.
#
#  This row is the ONLY one that separates a per-site latch from ONE SHARED
#  BIT: a measuring seat built both and they score identically on every row
#  that drives one site per session.
t, alive = session(pair((MOV_W_AT_R1_R2, LD), (MOV_W_R8_AT_R7, ST)))
row("two sites", "survived" if alive else "died", "survived",
    "no-data then not-waiting, ONE session")
row("two sites x2",
    ("%d" % (len(SAYS["nodata"].findall(t)) + len(SAYS["notwait"].findall(t))))
    if alive else "died", "2",
    "DIFFERENT sites -> TWO diagnostics, not one")

#  ---------------------------------------------------------------- accept side
#
#  *** THE DE-ESCALATION ACCEPT FOR THE REMOVED PREDICATES. ***
#
#  An earlier banner here claimed these were "the only rows that catch a
#  deleted arm" and listed rows that did not exist.  MEASURED FALSE: the
#  deleted-arm mutant is caught by the six count rows and `two sites x2`, and
#  the accept row as first written caught nothing at all -- it never touched
#  GDROM_DATA.  Replaced rather than patched, because a banner describing
#  absent rows is worse than no banner.
#
#  Coverage of the four de-fatalised predicates: `accept d0`/`accept d1` carry
#  the two read predicates and the busy mask, the 204 good reads inside
#  `overread` carry data_len, and `accept w8` carries the width predicate.
#
#  The values are device-signature quality -- RAM cannot produce them, and
#  they come from the synthesized TOC (d->data[0]=0x10, then 0x9600).

GDROM_CNTLO = 0xa05f7090       # 0x005f7000 + 0x90
GDROM_CNTHI = 0xa05f7094       # 0x005f7000 + 0x94
GDROM_COND = 0xa05f709c        # 0x005f7000 + 0x9c

MOV_W_AT_R1_R3 = 0x6311        # mov.w @r1,r3
BRA_BACK3 = 0xaffd             # bra .-2 : (pc+4) + (-3 * 2) lands on the insn before


def run(steps, at=CODE):
    """Plant a run of instructions, then a self-branch, and step them all."""
    put = ["put h 0x%x, 0x%04x" % (at + 2 * i, op) for i, op in enumerate(steps)]
    put += ["put h 0x%x, 0x%04x" % (at + 2 * len(steps), BRA_SELF),
            "put h 0x%x, 0x%04x" % (at + 2 * len(steps) + 2, NOP)]
    return put + ["pc=0x%x" % at, "step %d" % len(steps)]


setup = ["r7=0x%x" % GDROM_CNTLO, "r8=0x98"]
t, alive = session(setup + run([MOV_W_R8_AT_R7])
                   + ["r7=0x%x" % GDROM_CNTHI, "r8=0x01"] + run([MOV_W_R8_AT_R7], CODE + 0x20)
                   + ["r7=0x%x" % GDROM_COND, "r8=0xa0"] + run([MOV_W_R8_AT_R7], CODE + 0x40)
                   + ["r7=0x%x" % GDROM_DATA, "r8=0x0014"]
                   + run([MOV_W_R8_AT_R7] * 6, CODE + 0x60)
                   + ["r1=0x%x" % GDROM_DATA, "r2=0", "r3=0"]
                   + run([MOV_W_AT_R1_R2, MOV_W_AT_R1_R3], CODE + 0x100)
                   + ["print r2", "print r3"])
row("accept d0", printed(t, "r2") if alive else "died", "0x10",
    "legal TOC PIO: first halfword")
#  0xffff9600, not 0x9600: mov.w SIGN-EXTENDS and 0x9600 has bit 15 set.  The
#  first halfword (0x0010) does not, which is why only this one is extended --
#  a consistency check on the expectation rather than on the emulator.
row("accept d1", printed(t, "r3") if alive else "died", "0xffff9600",
    "legal TOC PIO: second halfword, sign-extended")

#  ---------------------------------------------------------------- the VALUE
#  No row pinned what a DECLINED read returns, so `odata = 0xffff` -> `0` passed
#  every row while the diagnostic still said "returning 0xffff".  A first-touch
#  16-bit load is the one path the TOC sequence cannot explain, so it pins the
#  value on its own.  mov.w sign-extends, so 0xffff arrives as 0xffffffff.
t, alive = session(["r1=0x%x" % GDROM_DATA, "r2=0"] + run([MOV_W_AT_R1_R2])
                   + ["print r2"])
row("declined val", printed(t, "r2") if alive else "died", "0xffffffff",
    "a declined read returns 0xffff, sign-extended")

#  ---------------------------------------------------------------- site :334
#  JOINED into the product, so it must be DRIVEN -- a seat's rule, and it is
#  right: joining a site and then not testing it is the worst of both.  Reached
#  by completing a legal TOC, then setting cnt PAST data_len so the boundary
#  branch never clears COND_DATA_AVAIL, then reading on past 408 bytes.
#  Three instructions per iteration, so ~700 steps covers 204+ halfwords.
t, alive = session(setup + run([MOV_W_R8_AT_R7])
                   + ["r7=0x%x" % GDROM_CNTHI, "r8=0x01"] + run([MOV_W_R8_AT_R7], CODE + 0x20)
                   + ["r7=0x%x" % GDROM_COND, "r8=0xa0"] + run([MOV_W_R8_AT_R7], CODE + 0x40)
                   + ["r7=0x%x" % GDROM_DATA, "r8=0x0014"]
                   + run([MOV_W_R8_AT_R7] * 6, CODE + 0x60)
                   + ["r7=0x%x" % GDROM_CNTHI, "r8=0xff"] + run([MOV_W_R8_AT_R7], CODE + 0xa0)
                   + ["r1=0x%x" % GDROM_DATA, "r2=0",
                      "put h 0x%x, 0x%04x" % (CODE + 0x200, MOV_W_AT_R1_R2),
                      "put h 0x%x, 0x%04x" % (CODE + 0x202, BRA_BACK3),
                      "put h 0x%x, 0x%04x" % (CODE + 0x204, NOP),
                      "pc=0x%x" % (CODE + 0x200), "step 700"], spin=4.0)
row("overread", "survived" if alive else "died", "survived",
    "TOC, cnt past data_len, then read on")
row("overread x1", ("%d" % len(SAYS["overread"].findall(t))) if alive else "died",
    "1", "reading past the buffer -> diagnostic exactly once")

#  ---------------------------------------------------------------- width accept
#
#  *** THE FOURTH DE-ESCALATED PREDICATE, AND THE ONLY ONE THAT HAD NO ROW. ***
#
#  A pass-2 seat built the shipped code with three lines added -- log, then
#  `odata = 0xffff; break;` instead of continuing -- and MEASURED IT AT 22/22
#  WITH A VECTOR BYTE-IDENTICAL TO THE SHIPPED BUILD.  Nothing in the detector
#  could see the difference, and that difference is the round's OWN CENTRAL
#  CLAIM: "this site logs and continues; the other three decline."
#
#  It is also the likeliest future edit here -- it is what the other three
#  sites in this same arm do, and what dev_wdc.c:155-167 does for its own
#  bad-length case, so "harmonise the four sites" reproduces it verbatim.
#
#  The row: SIX 8-BIT stores must still assemble and dispatch the TOC packet,
#  so a legal narrow-access command keeps working.  Measured base -> 0x10,
#  width-declines -> 0xffffffff, pre-fix -> died.
t, alive = session(setup + run([MOV_W_R8_AT_R7])
                   + ["r7=0x%x" % GDROM_CNTHI, "r8=0x01"] + run([MOV_W_R8_AT_R7], CODE + 0x20)
                   + ["r7=0x%x" % GDROM_COND, "r8=0xa0"] + run([MOV_W_R8_AT_R7], CODE + 0x40)
                   + ["r7=0x%x" % GDROM_DATA, "r8=0x0014"]
                   + run([MOV_B_R8_AT_R7] * 6, CODE + 0x60)
                   + ["r1=0x%x" % GDROM_DATA, "r2=0"]
                   + run([MOV_W_AT_R1_R2], CODE + 0x100) + ["print r2"])
row("accept w8", printed(t, "r2") if alive else "died", "0x10",
    "SIX 8-BIT stores assemble and dispatch")

n = sum(1 for _, ok in rows if ok)
print("GDROM_RESULT=%d/%d" % (n, len(rows)))
print("GDROM_VECTOR=" + ",".join(("1" if ok else "0") for _, ok in rows))
