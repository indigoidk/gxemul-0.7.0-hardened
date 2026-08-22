#!/usr/bin/env python3
"""`#451` DETECTOR: the two command-byte validators in sh4_sci_cmd() decline instead of
ending the host process -- and, more importantly, DECLINE MEANS DECLINE.

This is the detector, not the witness.  sh4_sci_witness.py asserts the PRE-FIX symptom
(three guest-clocked bytes that killed the host) and is RED now that they do not; this
file asserts the post-fix property and must stay green.

*** WHY SURVIVAL IS NOT THE PROPERTY. ***  #451 deleted two exit(1) calls, and with them
the accidental tripwire that made every mistake in this function LOUD.  Before the fix, a
guard that grew or a `return` that went missing announced itself by ending the host on the
first offending byte.  After it, the same mistakes are SILENT: a missing `return` performs
an invented transfer against the RS5C313 and says nothing, and a guard that grew declines a
legal command and says nothing.  A row that checks only "the host is still alive" cannot
see either, and would have passed every mutant the pass-1 panel named.

So the oracle here is the TRANSFER, observed through the same bit-banged protocol a guest
uses.  Two facts make that possible, both measured before this file was written:

  *  a legal pair -- 0xa5 (set address 5) then 0x9c (write data c) -- prints
     `[ SCI: write addr=5 data=c ]` from dev_sh4.c:685.  The address and the data are
     values THIS FILE chose, so the line is a device signature and not merely output.
  *  a declined byte prints its own `command declined` line and NO transfer line at all.

The debug() lines are visible because these sessions SINGLE-STEP.  debug() early-outs at
debugmsg.c:375 on `(quiet_mode && !ss) || v < 0`, and stepping sets `ss`.  A free-running
variant of this probe would go quiet WITHOUT SAYING SO -- do not convert these rows to a
free run without re-establishing the oracle.

THE ROWS, and which mutant each one exists to kill.  Every one of these was named by a
pass-1 seat, and the ones marked (*) survive a detector built the obvious way.

  R1  byte 0x10   site 1 declines, and NO transfer follows.                          (*)
                  0x10 has bit 7 CLEAR but a LEGAL AD/DT field, so if site 1 latches
                  and then falls through -- the one-line mutant -- 0x10 reaches the
                  data-write arm and really writes.  Byte 0x00 CANNOT see this: its
                  0x30 field is also invalid, so site 2 catches what site 1 dropped and
                  masks the defect.  Three seats converged on this independently.
  R2  byte 0x80   site 2 declines (encoding 0), no transfer.
  R3  0x80 then 0xb0 IN ONE SESSION -- 0xb0 must ALSO print.                         (*)
                  Both bytes reach the same else arm, so a latch keyed per SITE reports
                  the first and swallows the second forever.  This row is the whole
                  argument for keying on the field.  It is also vacuity-floor clause (b)
                  for the 0x30 value, which had no witness until the pass-1 panel.
  X   all THREE fault categories in ONE session -- all three must print.            (*)
                  R3 catches a collision between the two SITE-2 values; nothing caught a
                  collision ACROSS the sites.  TWO pass-2 seats keyed site 1 to collide
                  and picked DIFFERENT bits, so a two-byte row catches one and misses the
                  other; driving 0x10, 0x80 and 0xb0 together catches both.  Measured.
  RPT1 a SITE-1 offender TWICE -- one line, no transfer.                             (*)
                  THE ROOT CAUSE THREE SEATS FOUND SEPARATELY: every repeat and cross row
                  drove site 2, so site 1 ran exactly once in a fresh session.  Three
                  real-defect mutants walked through that gap, and the measuring seat
                  scored one of them 10/10 against the shipped file.
  N   0xa5, 0x20, 0x20, 0x9c -- a declined byte must not re-latch sci_cur_addr.      (*)
  N2  0xa5, 0x80, 0x9c -- the SITE-2 twin of N.                                      (*)
                  Site 2 can be made to fall through with address_transfer = 1 instead
                  of 0.  1 pokes sci_cur_addr WITHOUT reaching the write arm, so it
                  emits no line and every `transfers == []` row stays green.  Measured
                  at 12/12 before this row existed.
  CEIL 0x80 then 0xc0 -- two DIFFERENT bytes of ONE category, still ONE line.        (*)
                  RPT repeats the SAME byte, which is a weaker claim.  Widening the key
                  mask 0x30 -> 0xf0 keys 0x80 and 0xc0 apart and draws two lines,
                  silently breaking the stated three-line ceiling.  Measured at 12/12.
                  0x20 is declined but its field is the ADDRESS arm, which emits no
                  transfer line, so `transfers == []` looks clean while the address latch
                  is corrupt.  The oracle is structurally blind without this shape.
  RPT the SAME offender twice in one session: exactly ONE line, still declined.      (*)
                  Kills the sharpest mutant the panel found -- moving the `return`
                  INSIDE the latch guard, which is the natural typo since the braces are
                  already there.  It declines the first bad byte and lets every later
                  one fall through, and a detector that drives each offender once in a
                  fresh emulator scores it perfect.  The same row kills an unlatched
                  fatal() from the other side, by counting.
  A1  byte 0xa5   ACCEPT: a legal address transfer is silent.
  A2  0xa5, 0x9c  ACCEPT: a legal data write LANDS, with the address and data this file
                  chose.  C1 in the witness covers one valid command shape only; the
                  0x10 arm had no accept row before this one.
  J   0x80 then 0xa5, 0x9c -- a legal pair still works AFTER a decline.
                  dev_sh4.c:731 zeroes sci_bits_outputed in the CALLER, so a decline
                  re-arms the shifter.  Moving that line into the callee below the new
                  returns is a realistic tidy-up that jams the shift register at 8
                  forever, and nothing else here would notice.
  O   the transfer oracle is LIVE (A2 saw its line) -- without this, every "no transfer"
                  row above is unfalsifiable rather than true.
  I   identity: row count.

usage:  sh4_sci_probe.py <gxemul-binary> <landisk-kernel>
"""
import os
import re
import sys

import sh4_pcic_probe as P

SHREG_SCSPTR = 0xffe0001c       # thirdparty/sh4_scireg.h:64  (byte-wide)
SPB1IO, SPB1DT = 0x08, 0x04     # :83, :84
SPB0IO, SPB0DT = 0x02, 0x01     # :85, :86

#  dev_sh4.c:664 and :685.  Matching "SCI: read"/"SCI: write" would also match the
#  DECLINE lines, which contain "SCI: command byte ..." -- anchor on the word that only
#  a real transfer prints.
XFER_RE = re.compile(r"\[ SCI: (read|write) addr=([0-9a-f]+) data=([0-9a-f]+) \]")
DECLINE_RE = re.compile(r"sh4: SCI: command byte 0x([0-9a-f]{2}) ")

EXPECT_ROWS = 14

rows = []


def row(name, ok, got, want):
    rows.append((name, bool(ok)))
    print("  %-4s %s" % ("ok" if ok else "FAIL", name))
    if not ok:
        print("       got  %s\n       want %s" % (got, want))


def clock_byte(value):
    """Opcodes that clock `value` in, most-significant bit first.  See the witness."""
    ops = []

    def store(v):
        ops.append(0xE000 | (v & 0xff))     # mov #v,r0
        ops.append(0x2100)                  # mov.b r0,@r1
    store(SPB1IO | SPB0IO)                  # prime: SPB0IO must be in the OLD value
    for i in range(7, -1, -1):
        d = SPB1DT if (value >> i) & 1 else 0
        store(SPB1IO | SPB0IO | d)
        store(SPB1IO | SPB0IO | SPB0DT | d)
    return ops


def drive(seq, label, kw):
    """Clock every byte in `seq` through one session.  Returns (transfers, declines)."""
    ops = []
    for v in seq:
        ops += clock_byte(v)
    ops += [0x0009]
    buf, alive, st = P.session(
        ["put w 0x%x, 0x%08x" % (P.DEST, P.POISON), "r1=0x%x" % SHREG_SCSPTR]
        + P.poke(ops) + ["pc=0x%x" % P.CODE],
        len(ops) - 1, label, disasm_upto=0, **dict(kw, timeout=120))
    text = buf or ""
    return (st, alive,
            XFER_RE.findall(text), DECLINE_RE.findall(text))


def main():
    if len(sys.argv) != 3:
        print("usage:  sh4_sci_probe.py <gxemul-binary> <landisk-kernel>")
        return 2
    b, k = sys.argv[1], sys.argv[2]
    kw = dict(binary=b, kernel=k)
    for p in (b, k):
        if not os.path.exists(p):
            print("OPERATIONAL FAILURE: %s does not exist (cwd=%s)" % (p, os.getcwd()))
            print("SH4SCI_RESULT=0/%d" % EXPECT_ROWS)
            print("SH4SCI_FAIL")
            return 2

    #  ---- R1: bit 7 clear, AD/DT LEGAL -- the row byte 0x00 cannot replace ------------
    st, alive, xf, dec = drive([0x10], "R1", kw)
    row("R1 byte 0x10 (bit 7 clear, AD/DT legal) declines with NO transfer",
        st and alive and dec == ["10"] and xf == [],
        "alive=%s declines=%s transfers=%s" % (alive, dec, xf),
        "alive, exactly one decline naming 0x10, and NO transfer: without the `return` "
        "at site 1 this byte reaches the data-write arm and really writes")

    #  ---- R2 / R3: both values of the transfer field, IN ONE SESSION ------------------
    #  Two rows off ONE session deliberately: they must share it (the point of R3 is
    #  that an earlier 0x80 does not silence 0xb0), but a single combined row could not
    #  say WHICH byte went wrong, and an unattributable red is most of a wasted round.
    st, alive, xf, dec = drive([0x80, 0xb0], "R23", kw)
    row("R2 byte 0x80 (field 0x00) declines, naming the byte",
        st and alive and "80" in dec and xf == [],
        "alive=%s declines=%s transfers=%s" % (alive, dec, xf),
        "a decline naming 0x80, and no transfer")
    row("R3 byte 0xb0 (field 0x30) ALSO declines in that SAME session",
        st and alive and dec == ["80", "b0"] and xf == [],
        "alive=%s declines=%s transfers=%s" % (alive, dec, xf),
        "both 0x80 and 0xb0, in that order: a latch keyed per SITE reports the first "
        "and swallows the second forever, so this row is the case for keying on the "
        "field.  It is also vacuity-floor clause (b) for the 0x30 value")

    #  ---- X: a site-1 fault and a site-2 fault in ONE session --------------------------
    #  R3 catches a collision BETWEEN THE TWO SITE-2 VALUES, and nothing before this row
    #  caught a collision ACROSS the two sites: no other row drives a site-1 fault and a
    #  site-2 0x30 fault together, so keying site 1 as `1u << 3` -- which is exactly site
    #  2's key for field 0x30 -- passed all nine of them.  MEASURED as a survivor at 9/9
    #  before this row existed; a pass-2 seat predicted it and the mutant confirmed it.
    st, alive, xf, dec = drive([0x10, 0x80, 0xb0], "X", kw)
    row("X all THREE fault categories in ONE session -- all three print",
        st and alive and dec == ["10", "80", "b0"] and xf == [],
        "alive=%s declines=%s transfers=%s" % (alive, dec, xf),
        "all of 0x10, 0x80 and 0xb0.  TWO seats independently keyed site 1 to collide "
        "and they chose DIFFERENT bits -- 1u<<0 (site 2's field-0x00 key) and 1u<<3 "
        "(its field-0x30 key).  A two-byte row catches one variant and not the other; "
        "only driving all three categories together catches both")

    #  ---- RPT: the same offender twice -- one line, still declined --------------------
    st, alive, xf, dec = drive([0x80, 0x80], "RPT", kw)
    row("RPT the same offender twice -- exactly ONE line, and STILL no transfer",
        st and alive and dec == ["80"] and xf == [],
        "alive=%s declines=%s transfers=%s" % (alive, dec, xf),
        "one decline (the latch holds) and zero transfers (the `return` is outside the "
        "latch guard).  Moving that `return` inside declines only the first byte")

    #  ---- RPT1: the SITE-1 half of RPT, and the gap three seats found independently ---
    #  RPT drives 0x80 twice -- a SITE-2 byte.  Before this row, site 1 was exercised
    #  exactly once, in a fresh session, so three separate real-defect mutants scored a
    #  clean pass: the latch guard deleted at site 1 only (the "(once)" in that message
    #  becomes false and the ceiling becomes unbounded), and the `return` moved inside
    #  the latch guard at site 1 only, which invents a transfer on the SECOND bad byte.
    #  The measuring seat built the second one against the shipped file and scored it
    #  10/10 PASS.  One row closes both.
    st, alive, xf, dec = drive([0x10, 0x10], "RPT1", kw)
    row("RPT1 a SITE-1 offender twice -- exactly ONE line, and STILL no transfer",
        st and alive and dec == ["10"] and xf == [],
        "alive=%s declines=%s transfers=%s" % (alive, dec, xf),
        "one decline and zero transfers.  Without this row the site-1 message's "
        "'(once)' is asserted rather than measured, and a brace slip confined to site 1 "
        "is invisible")

    #  ---- N: a corrupted address latch, which the transfer oracle cannot otherwise see -
    #  0x20 is bit-7-clear and so is declined -- but its transfer field is the ADDRESS
    #  arm, which performs no memory_rw and therefore prints NO transfer line at all.
    #  So `transfers == []` is clean for a mutant that silently re-latches sci_cur_addr;
    #  the oracle is STRUCTURALLY blind to it.  The only shape that sees it is a legal
    #  address set, then the declined byte, then a legal data write: the write lands at
    #  the corrupted address instead of the chosen one.  Named by the measuring seat.
    st, alive, xf, dec = drive([0xa5, 0x20, 0x20, 0x9c], "N", kw)
    row("N a declined byte must not re-latch sci_cur_addr (write still lands at 5)",
        st and alive and xf == [("write", "5", "c")] and dec == ["20"],
        "alive=%s transfers=%s declines=%s" % (alive, xf, dec),
        "exactly [('write','5','c')]: a mutant that assigns sci_cur_addr before "
        "validating sends this write to address 0, and NO other row can see it because "
        "the address arm emits no transfer line of its own")

    #  ---- N2: the SITE-2 twin of N, and it caught a mutant N could not ----------------
    #  N drives a site-1 declined byte (0x20).  A pass-2 seat pointed out that site 2 can
    #  be made to fall through with `address_transfer = 1` rather than 0 -- and 1 pokes
    #  sci_cur_addr WITHOUT reaching the write arm, so it emits no transfer line and
    #  every `transfers == []` row stays green.  MEASURED as a survivor at 12/12 before
    #  this row existed; with it, the write lands at 0 instead of 5.
    st, alive, xf, dec = drive([0xa5, 0x80, 0x9c], "N2", kw)
    row("N2 a SITE-2 declined byte must not re-latch sci_cur_addr either",
        st and alive and xf == [("write", "5", "c")] and dec == ["80"],
        "alive=%s transfers=%s declines=%s" % (alive, xf, dec),
        "exactly [('write','5','c')].  M3 defaulted address_transfer to 0, which reaches "
        "the write arm and fires the transfer oracle; defaulting to 1 is silent and only "
        "this shape sees it")

    #  ---- CEIL: the three-line ceiling, MEASURED rather than asserted ------------------
    #  RPT drives the SAME byte twice.  The ceiling claim is about DIFFERENT bytes in the
    #  same fault category: 0x80 and 0xc0 both have bit 7 set and transfer field 0x00, so
    #  the fix must draw ONE line for the pair.  A pass-2 seat found that widening the key
    #  mask from 0x30 to 0xf0 -- one character -- keys them apart and draws TWO, silently
    #  breaking the ceiling the enum comment states.  MEASURED as a survivor at 12/12.
    st, alive, xf, dec = drive([0x80, 0xc0], "CEIL", kw)
    row("CEIL two DIFFERENT bytes of one fault category -- still exactly ONE line",
        st and alive and dec == ["80"] and xf == [],
        "alive=%s declines=%s transfers=%s" % (alive, dec, xf),
        "one decline for 0x80 and 0xc0 together.  This is what makes the comment's "
        "'THREE lines for the device lifetime' a measurement instead of a claim: the key "
        "must be the FIELD, not the byte, and only an unbounded shift breaks it")

    #  ---- A1 / A2: the ACCEPT side of all three de-fatalised predicates ---------------
    st, alive, xf, dec = drive([0xa5], "A1", kw)
    row("A1 ACCEPT byte 0xa5 -- a legal address transfer is silent",
        st and alive and dec == [],
        "alive=%s declines=%s" % (alive, dec),
        "no decline line at all: a start-bit guard that grew, or an address arm "
        "narrowed to require a zero low nibble, reddens here")

    st, alive, xf, dec = drive([0xa5, 0x9c], "A2", kw)
    a2_xf = xf                  # codex, pass 2: J overwrites `xf` before row O reads
    landed = xf == [("write", "5", "c")]      # it.  The boolean was right; the MESSAGE
                                              # would have printed J's transfers.
    row("A2 ACCEPT 0xa5 then 0x9c -- the data write LANDS at the chosen addr/data",
        st and alive and landed and dec == [],
        "alive=%s transfers=%s declines=%s" % (alive, xf, dec),
        "exactly [('write','5','c')] and no declines.  Dropping the 0x10 arm reddens "
        "here; the witness C1 row covers the address arm only")

    #  ---- J: a decline must not jam the shift register --------------------------------
    st, alive, xf, dec = drive([0x80, 0xa5, 0x9c], "J", kw)
    row("J a legal pair still works AFTER a declined byte (the shifter re-arms)",
        st and alive and xf == [("write", "5", "c")] and dec == ["80"],
        "alive=%s transfers=%s declines=%s" % (alive, xf, dec),
        "the write still lands: sci_bits_outputed is zeroed in the CALLER, and moving "
        "that into the callee below the returns jams the shifter at 8 forever")

    #  ---- O: the oracle itself -- without this the 'no transfer' rows are unfalsifiable
    row("O the transfer oracle is LIVE (A2 observed a real transfer line)",
        landed, "A2 transfers=%s" % (a2_xf,),
        "A2 must have seen [('write','5','c')]; if no transfer is EVER visible then "
        "every 'NO transfer' row above passes for the wrong reason")

    #  ---- identity --------------------------------------------------------------------
    row("I IDENTITY row count -- guards against a stale copy",
        len(rows) + 1 == EXPECT_ROWS, len(rows) + 1, EXPECT_ROWS)

    bad = sum(1 for _, ok in rows if not ok)
    print()
    print("SH4SCI_RESULT=%d/%d" % (len(rows) - bad, len(rows)))
    print("SH4SCI_PASS" if bad == 0 else "SH4SCI_FAIL")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
