#!/usr/bin/env python3
"""#448 DETECTOR: the four CHCR field decoders in `sh4_dmac_transfer()` DIAGNOSE AND
DECLINE instead of ending the host process -- and a LEGAL configuration still runs.

Rung 3.  Real SH-4 guest instructions through real address decode, real `memory_rw` and
real device dispatch, on an UNMODIFIED in-tree `-E landisk`.

THE DEFECT (witnessed by `sh4_chcr_witness.py`, 13/13 on the pre-fix build).  A guest
write to CHCR with TD set called `sh4_dmac_transfer()`, where four `default:` arms called
`exit(1)`.  *** Only `case 0x200:` survives the RS switch, so a wholly legal configuration
-- 4-byte transfers, both addresses incrementing -- still ended the host on its
resource-select alone. ***  Easier to reach than any site #447 repaired.

*** THE ACCEPT-SIDE ROWS ARE NOT OPTIONAL PADDING.  THEY ARE THE DE-ESCALATION CLAUSE,
AND THIS IS THE FIRST ROUND TO OWE THEM. ***

A flagship adjudication of #447 established the rule this file is built to satisfy:

    a fatal->survive fix DELETES THE ACCIDENTAL TRIPWIRE that made guard growth
    self-announcing.  Before such a fix, widening a guard meant exit(1) on the first
    legal write -- unmissable.  After it, the same edit means a SILENTLY DECLINED
    operation and nothing anywhere notices.  So the detector shipping with the fix must
    pin the ACCEPT SIDE of every predicate that used to gate death.

#447 shipped without those rows and a review seat then found a ONE-IDENTIFIER escape that
scored full marks.  Here every guard is pinned from both directions: A1-A4 prove a legal
encoding is still ACCEPTED (host alive, and ZERO diagnostics), while R1-R6 prove an
unmodelled one is still DECLINED.  Widen any of the four masks and an accept row reddens.

WHY "EXACTLY ONE DIAGNOSTIC" IS THE ORACLE AND NOT "A DIAGNOSTIC".  A review seat named
`return;` -> `break;` as the smallest edit that reintroduces a defect while a naive
detector still passes: the diagnostic and the latch both still run, so an
alive-plus-diagnostic row goes green, while execution falls out of the switch with the
field left at its initialiser -- an unmodelled encoding SILENTLY TREATED AS A LEGAL ONE.
It is caught here because a `break` falls through into the RS switch, which complains in
turn, so one store yields TWO diagnostics.  R1/R2/R3 require exactly one.

WHAT THIS FILE DOES NOT COVER, stated rather than left to be found:
  * `dev_sh4.c`'s IE site (`:486` pre-fix) is DELIBERATELY out of scope -- it is an
    unimplemented FEATURE, not an unimplemented ENCODING: the transfer it guards is the
    one configuration the model accepts, and declining it needs a different oracle
    (interrupt delivery).  Two seats reached that scope conclusion independently.  It is
    filed as `sh4dmacie`, and row X1 below PINS that it is still fatal, so the exclusion
    is visible in the gate rather than silent.
  * Nothing here claims a transfer HAPPENS.  It cannot: `sh4_dmac_transfer()` writes
    nothing to guest state on any path -- `case 0x200:` is `(void)sar; (void)dar;` with
    the comment "No transfer is done here!".  MEASURED by reading the whole function.
    A guest polling for completion already waits forever on the accepted path, before and
    after this fix alike.  That is a REAL pre-existing gap and it is `sh4dmanop`, not this
    round.

usage:  sh4_chcr_probe.py <gxemul-binary> <landisk-kernel>
"""
import os
import re
import sys

import sh4_pcic_probe as P

SH4_CHCR0 = 0xffa0000c          # src/include/sh4_dmacreg.h:40
SH4_CHCR3 = 0xffa0003c          # :55
CHCR_DM = 0x0000c000            # :117
CHCR_SM = 0x00003000            # :121
CHCR_TS_4BYTE = 3 << 4          # :131
CHCR_IE = 0x00000004            # :134
CHCR_TD = 0x00000001            # :136
CHCR_DM_INCREMENTED = 1 << 14   # :119
CHCR_SM_INCREMENTED = 1 << 12   # :123
RS_ACCEPTED = 0x200             # the one arm sh4_dmac_transfer returns from normally

#  A fully LEGAL configuration: 4-byte transfers, both addresses incrementing, the
#  accepted resource select, transfer enabled, no interrupt requested.  This is the
#  accept-side probe value -- it must run silently.
CHCR_LEGAL = (CHCR_DM_INCREMENTED | CHCR_SM_INCREMENTED | RS_ACCEPTED
              | CHCR_TS_4BYTE | CHCR_TD)

ST = {1: 0x2100, 2: 0x2101, 4: 0x2102}    # mov.b/w/l r0,@r1

#  Every #448 diagnostic has this shape.  Counted, never matched on a register name.
VAL_RE = re.compile(r"\[ sh4: DMA channel \d+: [a-z ]+ \d+ not implemented"
                    r" -- transfer declined\.  \(once per encoding\) \]")

EXPECT_ROWS = 18

rows = []


def row(name, ok, got, want):
    rows.append((name, bool(ok), got, want))
    print("  %-4s %s" % ("ok" if ok else "FAIL", name))
    if not ok:
        print("       got  %s\n       want %s" % (got, want))


def wr(addr, val, label, kw):
    return P.write_arm(addr, val, label, kw, op=ST[4])


def diags(txt):
    return VAL_RE.findall(txt or "")


def main():
    if len(sys.argv) != 3:
        print("usage:  sh4_chcr_probe.py <gxemul-binary> <landisk-kernel>")
        return 2
    b, k = sys.argv[1], sys.argv[2]
    kw = dict(binary=b, kernel=k)
    for p in (b, k):
        if not os.path.exists(p):
            print("OPERATIONAL FAILURE: %s does not exist (cwd=%s)" % (p, os.getcwd()))
            print("SH4CHCR_RESULT=0/%d" % EXPECT_ROWS)
            print("SH4CHCR_FAIL")
            return 2

    #  ---- R1..R6: an unmodelled encoding is DECLINED, host survives, ONE line ---------
    rejects = [
        #  *** R1 CARRIED THE ACCEPTED RS UNTIL A PASS-2 SEAT MEASURED IT VACUOUS -- THE
        #  SAME DEFECT AS R2/R3, FIXED THERE IN THE SAME SESSION AND NOT CARRIED HERE. ***
        #  With RS=0x200 a `break` at the TS default falls through into DM=0, SM=0 and an
        #  accepted RS, all legal, so exactly one line printed either way and the mutant
        #  scored a clean 16/16.  The lesson is not the value: it is that fixing two of
        #  three siblings and writing a comment claiming the third was covered is how a
        #  wrong record gets shipped.  The old comment said a `break` here "falls through
        #  to the RS switch, which for most values complains too" -- true of most values,
        #  and R1 was using the one that does not.
        ("R1 TS=5   declined, host alive, EXACTLY ONE line", SH4_CHCR0,
         (5 << 4) | 0x100 | CHCR_TD, "transmit size 5"),
        #  *** R2 AND R3 CARRY AN ILLEGAL RS (1) DELIBERATELY, AND AN EARLIER DRAFT USED
        #  THE ACCEPTED 0x200 AND WAS MEASURED VACUOUS. ***  The `break` escape is caught
        #  by counting diagnostics only if the code AFTER the fallen-through switch has
        #  something to complain about: with RS=0x200 a `break` at the DM default lands in
        #  an RS arm that is perfectly happy, so exactly one line is printed either way and
        #  the mutant scored 15/15.  With RS=1 the fall-through complains in turn, so the
        #  escape shows up as TWO lines from ONE store.
        ("R2 DM=3   declined, host alive, EXACTLY ONE line", SH4_CHCR0,
         CHCR_DM | 0x100 | CHCR_TS_4BYTE | CHCR_TD, "destination address mode 3"),
        ("R3 SM=3   declined, host alive, EXACTLY ONE line", SH4_CHCR0,
         CHCR_SM | 0x100 | CHCR_TS_4BYTE | CHCR_TD, "source address mode 3"),
        #  RS=1 is one of the FIFTEEN encodings that used to end the host.
        ("R4 RS=1    declined, host alive, EXACTLY ONE line", SH4_CHCR0,
         0x100 | CHCR_DM_INCREMENTED | CHCR_SM_INCREMENTED | CHCR_TS_4BYTE | CHCR_TD,
         "resource select 1"),
        #  RS=15 is the HIGHEST encoding, and it is here for a reason beyond coverage:
        #  the latch key is `1u << ((chcr & CHCR_RS) >> 8)`, so 15 exercises the top bit
        #  the shift can produce.  *** AN EARLIER DRAFT OF THIS ROW WAS BYTE-IDENTICAL TO
        #  R4 *** -- a duplicate that killed nothing R4 did not, which the identity row
        #  surfaced by miscounting.  The same "two rows, one mutant" slip is recorded in
        #  #446's kill table; it is easy to make and invisible without a count.
        ("R5 RS=15   declined -- the top encoding the latch shift can reach", SH4_CHCR0,
         0xf00 | CHCR_DM_INCREMENTED | CHCR_SM_INCREMENTED | CHCR_TS_4BYTE | CHCR_TD,
         "resource select 15"),
        #  A DIFFERENT CHANNEL: the latch is per (class, channel), so channel 3 must
        #  complain in its own right rather than be silenced by channel 0's earlier line.
        ("R6 CHCR3 DM=3 -- channel 3 complains in its OWN right", SH4_CHCR3,
         CHCR_DM | RS_ACCEPTED | CHCR_TS_4BYTE | CHCR_TD, "channel 3"),
    ]
    for name, addr, val, needle in rejects:
        buf, alive, st = wr(addr, val, name.split()[0], kw)
        d = diags(buf)
        row("%s (0x%08x)" % (name, val),
            st and alive and len(d) == 1 and needle in d[0],
            "alive=%s lines=%d %s" % (alive, len(d), d),
            "alive, exactly ONE line naming %r -- two lines means a `break` fell "
            "through into the next switch" % needle)

    #  ---- R7: THE ROW THAT MAKES A `break` AT THE RS ARM A VISIBLE HOST DEATH ---------
    #  *** A PASS-2 SEAT PREDICTED THIS ESCAPE AND MEASUREMENT CONFIRMED IT AT 16/16, AND
    #  IT IS THE WORST OF THE THREE BECAUSE IT PUTS exit(1) BACK. ***  With `return` at the
    #  RS default the function leaves before `if (cause_interrupt)`.  Replace it with
    #  `break` and that site becomes reachable from ALL SIXTEEN resource-select encodings
    #  instead of the one X1 pins -- host death this round removed, restored by one keyword.
    #
    #  No other row could see it: every reject row had IE clear, so after the fall-through
    #  `cause_interrupt` was 0 and the function ended alive with the same single line.
    #  This row sets IE with an ILLEGAL RS, which is alive on the correct build (the RS arm
    #  returns first) and DEAD the moment that return becomes a break.
    buf, alive, st = wr(SH4_CHCR0, 0x100 | CHCR_IE | CHCR_TD, "R7", kw)
    d = diags(buf)
    row("R7 an illegal RS with IE SET is still declined, host still alive",
        st and alive and len(d) == 1 and "resource select 1" in d[0],
        "alive=%s lines=%d %s" % (alive, len(d), d),
        "alive with ONE line: the RS arm must RETURN, not fall through into the "
        "interrupt-enable exit(1) that this round deliberately leaves in place")

    #  ---- A1..A4: THE ACCEPT SIDE.  The de-escalation clause. ------------------------
    #  *** A LEGAL CONFIGURATION MUST RUN SILENTLY.  Widen ANY of the four guard masks
    #  and one of these reddens -- which is the tripwire the fix itself destroyed. ***
    buf, alive, st = wr(SH4_CHCR0, CHCR_LEGAL, "A1", kw)
    row("A1 ACCEPT: a fully legal CHCR runs with ZERO diagnostics",
        st and alive and len(diags(buf)) == 0,
        "alive=%s lines=%s" % (alive, diags(buf)),
        "alive and NO diagnostic: TS=4byte, DM/SM=increment, RS=0x200, TD set are all "
        "modelled, so any complaint means a guard mask GREW")

    #  Each accept row varies ONE field to its other legal encodings, so a mask that grew
    #  by one bit is attributable to the field it grew in rather than merely detected.
    accepts = [
        ("A2 ACCEPT: DM=FIXED and DM=DECREMENTED are still legal",
         [RS_ACCEPTED | CHCR_TS_4BYTE | CHCR_TD | (0 << 14),
          RS_ACCEPTED | CHCR_TS_4BYTE | CHCR_TD | (2 << 14)]),
        ("A3 ACCEPT: SM=FIXED and SM=DECREMENTED are still legal",
         [RS_ACCEPTED | CHCR_TS_4BYTE | CHCR_TD | (0 << 12),
          RS_ACCEPTED | CHCR_TS_4BYTE | CHCR_TD | (2 << 12)]),
        ("A4 ACCEPT: every modelled transmit size is still legal",
         [RS_ACCEPTED | CHCR_TD | (n << 4) for n in (0, 1, 2, 3, 4)]),
    ]
    for name, vals in accepts:
        bad = []
        for v in vals:
            buf, alive, st = wr(SH4_CHCR0, v, name.split()[0], kw)
            if not (st and alive and len(diags(buf)) == 0):
                bad.append((hex(v), alive, diags(buf)))
        row(name, not bad, bad or "all accepted silently",
            "every one alive with NO diagnostic")

    #  ---- L1/L2: THE LATCH KEY, and these need TWO STORES IN ONE PROCESS ---------------
    #  *** EVERY ROW ABOVE IS ITS OWN SESSION, SO THE LATCH IS FRESH EACH TIME AND NONE OF
    #  THEM CAN SEE THE LATCH KEY AT ALL. ***  A mutant keying on the whole CHCR word, or
    #  one dropping the encoding sub-key, would pass R1-R6 and A1-A4 untouched.  #447 was
    #  measured to have exactly this gap -- its instance rows counted diagnostic LINES
    #  while its state rows only ever read instance 0 -- so the shape is recorded, and
    #  closing it here costs two rows.
    def two_stores(v1, v2, addr, label):
        """Two guest mov.l stores to `addr` in ONE process: r0 then r4."""
        return P.session(
            ["put w 0x%x, 0x%08x" % (P.DEST, P.POISON),
             "r0=0x%x" % v1, "r4=0x%x" % v2, "r1=0x%x" % addr]
            + P.poke([0x2102, 0x2142, 0x0009]) + ["pc=0x%x" % P.CODE],
            2, label, disasm_upto=6, **kw)

    #  SAME offending encoding (DM=3), DIFFERENT other bits (TS 2-byte then 4-byte, both
    #  legal so both reach the DM switch).  A correct (class, channel, encoding) latch
    #  says it ONCE.  A whole-register latch sees two distinct words and says it twice.
    #
    #  *** THE ORDER OF THESE TWO VALUES IS LOAD-BEARING, AND THE FIRST DRAFT HAD IT
    #  BACKWARDS AND WAS MEASURED VACUOUS. ***  A whole-register latch ORs the word in and
    #  tests `chcr & ~reported`, so if the second store's word is a BIT-SUBSET of the
    #  first, `fresh` is zero and the mutant stays silent -- indistinguishable from the
    #  correct latch.  TS 2-byte (0x20) IS a subset of 4-byte (0x30), so writing the wide
    #  one first hid the mutant at 15/15.  Narrow first, wide second: the second store
    #  carries bit 4 the first lacks, and the mutant has to speak.
    buf, alive, st = two_stores(
        CHCR_DM | RS_ACCEPTED | (2 << 4) | CHCR_TD,
        CHCR_DM | RS_ACCEPTED | (3 << 4) | CHCR_TD, SH4_CHCR0, "L1")
    d = diags(buf)
    row("L1 LATCH: the same encoding twice with different other bits -> ONE line",
        st and alive and len(d) == 1,
        "alive=%s lines=%d %s" % (alive, len(d), d),
        "exactly ONE -- two means the latch keys on the whole CHCR word, which lets a "
        "guest walk 32-bit values and draw an unsilenceable line for each")

    #  TWO DIFFERENT illegal RS encodings on one channel.  A correct latch says it TWICE
    #  -- they are different features.  A latch that dropped the encoding sub-key and kept
    #  only (class, channel) would say it once and silence the second fault.
    buf, alive, st = two_stores(
        0x100 | RS_ACCEPTED * 0 | CHCR_DM_INCREMENTED | CHCR_SM_INCREMENTED
        | CHCR_TS_4BYTE | CHCR_TD,
        0x300 | CHCR_DM_INCREMENTED | CHCR_SM_INCREMENTED | CHCR_TS_4BYTE | CHCR_TD,
        SH4_CHCR0, "L2")
    d = diags(buf)
    row("L2 LATCH: two DIFFERENT illegal encodings on one channel -> TWO lines",
        st and alive and len(d) == 2,
        "alive=%s lines=%d %s" % (alive, len(d), d),
        "exactly TWO -- one means the latch dropped the encoding sub-key and is "
        "silencing a fault the guest has not been told about")

    #  L3: the CHANNEL sub-key, which needs two channels in ONE process.
    #  *** R6 ALREADY WRITES CHANNEL 3, AND A MUTANT DROPPING THE CHANNEL KEY SCORED
    #  15/15 AGAINST IT. ***  R6 runs in its own process, so there is no earlier
    #  channel-0 complaint for the broken latch to silence -- the row proves channel 3
    #  REACHES the guard, not that the latch distinguishes channels.  Those are different
    #  properties and only this one catches the mutant.  Same DM=3 encoding on channel 0
    #  then channel 3: a correct latch says it TWICE, a channel-blind one says it once.
    buf, alive, st = P.session(
        ["put w 0x%x, 0x%08x" % (P.DEST, P.POISON),
         "r0=0x%x" % (CHCR_DM | RS_ACCEPTED | CHCR_TS_4BYTE | CHCR_TD),
         "r1=0x%x" % SH4_CHCR0,
         "r2=0x%x" % (CHCR_DM | RS_ACCEPTED | CHCR_TS_4BYTE | CHCR_TD),
         "r3=0x%x" % SH4_CHCR3]
        + P.poke([0x2102, 0x2322, 0x0009]) + ["pc=0x%x" % P.CODE],
        2, "L3", disasm_upto=6, **kw)
    d = diags(buf)
    row("L3 LATCH: the same encoding on TWO channels -> TWO lines",
        st and alive and len(d) == 2,
        "alive=%s lines=%d %s" % (alive, len(d), d),
        "exactly TWO -- one means the latch dropped the CHANNEL sub-key, so a fault on "
        "one channel silences the same fault on the other seven")

    #  ---- F1: fatal() vs debug(), which needs FREE-RUNNING and nothing else can see ----
    #  *** `fatal` -> `debug` at all four sites SCORED 16/16 AND WAS MEASURED, NOT GUESSED.
    #  ***  Every row above single-steps, and under stepping `debug()` prints exactly like
    #  `fatal()`, so presence cannot distinguish them.  #447 established the mechanism and
    #  this row reuses it: `src/core/debugmsg.c` computes
    #        bool ss = single_step || about_to_enter_single_step;
    #        int v = verbose;  if (emul_executing) v--;  if (ss) v++;
    #        if ((quiet_mode && !ss) || v < 0) return;      /* :375 */
    #  while `fatal()` (:384-390) has NO early-out at all.  Stepping raises v; free-running
    #  lowers it below zero, so `debug()` goes silent and `fatal()` does not.  No -q needed.
    #
    #  *** THE PRECONDITION IS verbose == 0 AND IT IS INVISIBLE IF LOST. ***  Run this with
    #  -v (or -i / -r, which imply it) and free-running gives v == 0, `debug()` prints, and
    #  this row goes quietly green on the mutant.  The session helper passes -V and never
    #  -v; if that ever changes, this row stops discriminating without reddening.
    #
    #  THE SENTINEL IS THE ROW'S OWN LIVENESS CONTROL.  Without it, "no diagnostic" and
    #  "the `continue` never ran the sequence" are the same observation -- so a broken
    #  measurement would read as a detection.
    buf, alive, st = P.session(
        ["put w 0x%x, 0x%08x" % (P.DEST, P.POISON),
         "r0=0x%x" % (0x100 | CHCR_DM_INCREMENTED | CHCR_SM_INCREMENTED
                      | CHCR_TS_4BYTE | CHCR_TD),
         "r1=0x%x" % SH4_CHCR0, "r2=0x5a5a1234", "r3=0x%x" % P.DEST]
        + P.poke([0x2102, 0x2322, 0x0009])
        + ["breakpoint add 0x%x" % (P.CODE + 4), "pc=0x%x" % P.CODE, "continue"],
        0, "F1", disasm_upto=0, **dict(kw, timeout=40))
    sent = P.dumped(buf)
    d = diags(buf)
    row("F1 FREE-RUNNING: the diagnostic survives `continue`, so it is fatal() not debug()",
        st and alive and sent == P.le(0x5a5a1234) and len(d) == 1,
        "alive=%s sentinel=%s lines=%d %s" % (alive, sent, len(d), d),
        "sentinel=%s (proving `continue` really ran the sequence) AND the diagnostic "
        "still present" % P.le(0x5a5a1234))

    #  ---- X1: THE EXCLUSION, PINNED ---------------------------------------------------
    #  *** A SCOPE DECISION THAT NO ROW ASSERTS IS INDISTINGUISHABLE FROM AN OVERSIGHT.
    #  ***  `:486` (IE on the accepted RS) is deliberately NOT repaired by #448, so this
    #  row requires it to STILL end the host.  It reddens the day someone fixes it --
    #  which is correct: that day the row must be deleted and `sh4dmacie` closed, and a
    #  gate that goes red is how anyone finds out the exclusion has expired.
    buf, alive, st = wr(SH4_CHCR0, RS_ACCEPTED | CHCR_IE | CHCR_TD, "X1", kw)
    row("X1 EXCLUSION: the IE site is STILL fatal -- #448 deliberately omits it",
        st and not alive and "sh4 dmac interrupt" in (buf or ""),
        "alive=%s diagnostic=%s" % (alive, "sh4 dmac interrupt" in (buf or "")),
        "NOT alive: this is `sh4dmacie`, a different semantic class.  If this row "
        "reddens, that round has landed -- delete the row rather than the fix.")

    #  ---- W0 / identity ---------------------------------------------------------------
    n_ses = len(P.STARTS)
    n_ok = sum(1 for _, s in P.STARTS if s)
    row("W0 EVERY session reached the debugger prompt (absent data must FAIL)",
        n_ses > 0 and n_ok == n_ses,
        "sessions=%d started=%d" % (n_ses, n_ok), "all %d started" % n_ses)

    row("W-id IDENTITY row count -- guards against a stale copy",
        len(rows) + 1 == EXPECT_ROWS, len(rows) + 1, EXPECT_ROWS)

    bad = sum(1 for _, ok, _, _ in rows if not ok)
    print()
    print("SH4CHCR_RESULT=%d/%d" % (len(rows) - bad, len(rows)))
    print("SH4CHCR_PASS" if bad == 0 else "SH4CHCR_FAIL")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
