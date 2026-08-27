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
    filed as `sh4dmacie`, and row X1 below PINS the site's behaviour, so the exclusion is
    visible in the gate rather than silent.
    *** THIS SAID X1 PINS THAT THE SITE IS "STILL FATAL".  THAT WAS TRUE WHEN WRITTEN AND
    IS FALSE AT HEAD: `#453` (f532bb6) de-fatalised it, and X1 now asserts the OPPOSITE --
    `alive` plus exactly one latched diagnostic.  Corrected 2026-08-26 by the sh4dmacie
    regress review, which found the probe's own X1 body contradicting its docstring five
    hundred lines below. ***
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

SH4_SAR0 = 0xffa00000           # src/include/sh4_dmacreg.h:37
SH4_DAR0 = 0xffa00004           # :38
SH4_DMATCR0 = 0xffa00008        # :39
SH4_CHCR0 = 0xffa0000c          # src/include/sh4_dmacreg.h:40
SH4_CHCR1 = 0xffa0001c          # :45
SH4_CHCR3 = 0xffa0003c          # :55
SH4_CHCR7 = 0xffa0008c          # :85  -- NOT a stride from CHCR3; 4..7 restart at 0xffa00050
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

EXPECT_ROWS = 27

rows = []


def row(name, ok, got, want):
    rows.append((name, bool(ok), got, want))
    print("  %-4s %s" % ("ok" if ok else "FAIL", name))
    if not ok:
        print("       got  %s\n       want %s" % (got, want))


def wr(addr, val, label, kw):
    return P.write_arm(addr, val, label, kw, op=ST[4])


#  *** TWO FAMILIES OF DIAGNOSTIC NOW EXIST IN THIS DEVICE, AND A ROW THAT COUNTS ONLY
#  ONE OF THEM IS BLIND TO THE OTHER. ***  VAL_RE matches #448's "encoding N not
#  implemented"; IE_RE matches #453's transfer-end-interrupt line.  A pass-2 seat found
#  that the ACCEPT rows -- whose whole claim is "ZERO diagnostics" -- counted only VAL_RE,
#  so `cause_interrupt = 1` (one token) made every legal transfer print the #453 line on
#  the path A1 names as silent, and all 25 rows stayed green.
IE_RE = re.compile(r"sh4: DMA channel (\d+): a transfer-end interrupt was requested")


def diags(txt):
    return VAL_RE.findall(txt or "")


def any_diag(txt):
    """EVERY diagnostic this device can emit, both families."""
    return VAL_RE.findall(txt or "") + IE_RE.findall(txt or "")


def arm_then_read(chcr_val, read_addr, label, kw,
                  sar=0x0c001000, dar=0x0c002000, tcr=0x00000042):
    """Write NON-RESET values to SAR/DAR/DMATCR, then CHCR, then read one back.

    *** THE NON-RESET VALUES ARE THE WHOLE POINT, AND THE FIRST VERSION OF THESE ROWS WAS
    MEASURED VACUOUS WITHOUT THEM. ***  They asserted SAR/DAR/DMATCR were 0 after the
    declined request -- but 0 is also their RESET value, so a mutant that ZEROES them was
    indistinguishable from correct behaviour and passed at 24/24.  Arming each register
    with a distinct non-zero value first makes "unchanged" a claim that can fail.

    One session throughout: the state lives in the emulator process, so a fresh-emulator
    readback would show the reset value on clean and mutant alike.

    All ten opcodes were checked against the emulator's own disassembler.
    """
    ops = [0x2102,      # mov.l r0,@r1   SAR   <- r0
           0x7104,      # add #4,r1
           0x2142,      # mov.l r4,@r1   DAR   <- r4
           0x7104,      # add #4,r1
           0x2162,      # mov.l r6,@r1   DMATCR<- r6
           0x7104,      # add #4,r1
           0x2152,      # mov.l r5,@r1   CHCR  <- r5   (this is the declined request)
           0x6272,      # mov.l @r7,r2   read the register under test
           0x2322,      # mov.l r2,@r3   park it where the row can see it
           0x0009]
    return P.session(
        ["put w 0x%x, 0x%08x" % (P.DEST, P.POISON),
         "r1=0x%x" % SH4_SAR0, "r0=0x%x" % sar, "r4=0x%x" % dar, "r6=0x%x" % tcr,
         "r5=0x%x" % chcr_val, "r7=0x%x" % read_addr, "r3=0x%x" % P.DEST]
        + P.poke(ops) + ["pc=0x%x" % P.CODE],
        len(ops) - 1, label, disasm_upto=20, **kw)


def store_then_read(store_addr, store_val, read_addr, label, kw):
    """Store to one register and read another back IN THE SAME PROCESS.

    *** THE SINGLE SESSION IS THE WHOLE POINT AND A SEPARATE-SESSION READ WOULD BE
    VACUOUS. ***  These rows exist to catch a mutant that writes DMA state on the
    declined path -- setting CHCR.TE just before the diagnostic, say.  That state lives
    in the emulator process, so reading it back from a FRESH emulator would show the
    reset value on the clean build and on the mutant alike, and the row could never fail.

    r0/r1 carry the store, r4/r3 the load and its destination.
    """
    ops = [0x2102,      # mov.l r0,@r1   -- the store under test
           0x6242,      # mov.l @r4,r2   -- read the register back
           0x2322,      # mov.l r2,@r3   -- park it where the row can see it
           0x0009]
    return P.session(
        ["put w 0x%x, 0x%08x" % (P.DEST, P.POISON),
         "r0=0x%x" % store_val, "r1=0x%x" % store_addr,
         "r4=0x%x" % read_addr, "r3=0x%x" % P.DEST]
        + P.poke(ops) + ["pc=0x%x" % P.CODE],
        len(ops) - 1, label, disasm_upto=8, **kw)


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
        st and alive and len(any_diag(buf)) == 0,
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
            if not (st and alive and len(any_diag(buf)) == 0):
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

    def three_stores(v1, v2, v3, addr, label):
        """Three guest mov.l stores to `addr` in ONE process: r0, r4, then r5.

        0x2152 (mov.l r5,@r1) is the only opcode here not already in
        sh4_pcic_probe's validated OPS table, so disasm_upto covers all three
        stores -- a wrong register field is silent and yields 0, which a
        line-COUNTING oracle would accept by accident."""
        return P.session(
            ["put w 0x%x, 0x%08x" % (P.DEST, P.POISON),
             "r0=0x%x" % v1, "r4=0x%x" % v2, "r5=0x%x" % v3, "r1=0x%x" % addr]
            + P.poke([0x2102, 0x2142, 0x2152, 0x0009]) + ["pc=0x%x" % P.CODE],
            3, label, disasm_upto=8, **kw)

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
    #  ---- L0: THE SAME WORD TWICE, AND IT IS A SAFETY ROW, NOT A LATCH ROW ------------
    #  *** MEASURED 2026-08-22: WITHOUT THIS ROW, TWO CHARACTERS RESTORE A GUEST-REACHABLE
    #  HOST DEATH AND THIS FILE STILL SCORES 18/18. ***  Move the `return;` at the RS
    #  default arm INSIDE the `if (sh4_val_first(...))` body -- one brace pair -- and the
    #  FIRST store still diagnoses and returns, while the SECOND takes the LATCHED path,
    #  which prints nothing and now falls through to the `cause_interrupt` exit(1) that
    #  #448 removed.  Measured: alive=False, "TODO: sh4 dmac interrupt" present.
    #
    #  Every R row stores ONCE, so they only ever exercise the FRESH path.  L1/L2/L3
    #  store twice but with DIFFERENT words, so their second store still carries FRESH
    #  bits and `sh4_val_first` still returns true -- they check which KEY the latch uses.
    #  What had NO coverage is the fully suppressed path, where the helper returns FALSE
    #  and the caller continues.  (An earlier draft said L1/L2/L3 "never test what happens
    #  after it suppresses", which is slightly too broad -- they exercise PARTIAL
    #  suppression; a seat drew the distinction.)  This row uses one identical word so the
    #  second call is fully suppressed, which is the only way to reach that path.
    #
    #  It is the same defect as the `return`->`break` variant the docstring already pins,
    #  DEFERRED BY ONE STORE, and it re-reaches the removed exit(1) -- vacuity-floor
    #  clause (b), found by the measuring seat against the SHIPPED file.
    #  *** EVERY BIT OF THIS WORD IS LOAD-BEARING, and a pass-2 seat traced why. ***
    #  CHCR_TD is what makes the store reach sh4_dmac_transfer() at all.  CHCR_IE is what
    #  makes the mutant FATAL rather than merely wrong: the fall-through lands on
    #  `if (cause_interrupt) { ... exit(1); }`, and cause_interrupt IS CHCR_IE -- so
    #  dropping IE to "simplify" the row leaves the mutant falling harmlessly off the end
    #  of the function, host alive, ROW GREEN, VACUOUS.  RS=1 is an unmodelled encoding
    #  that reaches the `default:` arm; TE is clear and TS/DM/SM are all 0, which are
    #  modelled, so this word raises exactly ONE complaint and no others.
    v = CHCR_IE | CHCR_TD | (1 << 8)            # RS=1, unmodelled; IE and TD set
    buf, alive, st = two_stores(v, v, SH4_CHCR0, "L0")
    d = diags(buf)
    row("L0 SAFETY: the SAME word twice -- host ALIVE on the suppressed second store",
        st and alive and len(d) == 1,
        "alive=%s lines=%d %s" % (alive, len(d), d),
        "alive with exactly ONE line.  The second store is silenced by the latch, so a "
        "`return` moved inside the latch guard falls through it into the exit(1) this "
        "round removed -- and no single-store row can see that")

    buf, alive, st = two_stores(
        CHCR_DM | RS_ACCEPTED | (2 << 4) | CHCR_TD,
        CHCR_DM | RS_ACCEPTED | (3 << 4) | CHCR_TD, SH4_CHCR0, "L1")
    d = diags(buf)
    row("L1 LATCH: the same encoding twice with different other bits -> ONE line",
        st and alive and len(d) == 1,
        "alive=%s lines=%d %s" % (alive, len(d), d),
        "exactly ONE -- two means the latch keys on the whole CHCR word, which lets a "
        "guest walk 32-bit values and draw an unsilenceable line for each")

    #  ---- L4: A, B, A -- the accumulator itself, not the key ---------------------------
    #  *** ONE DELETED CHARACTER IN THE SHARED HELPER DEFEATS THE LATCH FOR EVERY CLASS IN
    #  THIS FILE, AND ALL 19 OTHER ROWS STAY GREEN. ***  Change sh4_val_first's
    #  `d->val_reported[cls][instance] |= bits;` to `= bits;` and the accumulator stops
    #  accumulating: it holds only the LAST reported set.
    #
    #  Nothing else here sees it, and the reason is exact.  R rows report A alone.  L0
    #  reports A then A -- assignment still leaves A recorded.  L1/L2/L3 report A then B,
    #  and B's freshness is computed BEFORE A is discarded.  No row ever returns to A.
    #  A, B, A does, and under the mutant A is diagnosed TWICE.
    #
    #  MEASURED: clean gives resource-select lines ['1', '3']; the mutant gives
    #  ['1', '3', '1'].  Severity is not merely cosmetic -- a guest alternating two
    #  unmodelled encodings then draws a line PER STORE, and fatal() has no quiet_mode
    #  early-out, so it cannot be silenced even with -q.  That is the unbounded burn the
    #  latch exists to prevent.  Named by a pass-2 seat; built before it was believed.
    #
    #  RS=1 and RS=3 deliberately, and NOT RS=2: 0x200 is the one ACCEPTED encoding, and
    #  with CHCR_IE set it reaches the sh4dmacie site, which WAS fatal by design when this
    #  comment was written and was de-fatalised by #453 (f532bb6) -- an
    #  earlier draft of this measurement used it and killed the BASELINE, which is a void
    #  result rather than a negative one.
    buf, alive, st = three_stores(
        CHCR_IE | CHCR_TD | (1 << 8),
        CHCR_IE | CHCR_TD | (3 << 8),
        CHCR_IE | CHCR_TD | (1 << 8), SH4_CHCR0, "L4")
    d = diags(buf)
    row("L4 ACCUMULATOR: A, B, A -- the repeat of A is STILL suppressed",
        st and alive and len(d) == 2,
        "alive=%s lines=%d %s" % (alive, len(d), d),
        "exactly TWO -- three means the latch records only the LAST set instead of "
        "accumulating, so a guest alternating two encodings draws an unsilenceable line "
        "per store")

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
    #  *** X1 USED TO ASSERT THIS SITE WAS STILL FATAL, AND ITS OWN MESSAGE SAID WHAT TO
    #  DO WHEN IT REDDENED: "delete the row rather than the fix".  #453 landed, so it is
    #  gone and these three replace it. ***
    #
    #  What #453 changed: a guest CHCR write of 0x00000205 -- RS=2, the ONE resource
    #  select this model accepts, with IE and TD set -- used to reach
    #  `fatal("TODO: sh4 dmac interrupt!"); exit(1)`.  MEASURED across all sixteen RS
    #  encodings: exactly that one reached it; the other fifteen decline at the RS switch.
    #
    #  Why the interrupt is NOT generated instead, which is the part a reader will
    #  question: the only arm that reaches the site performs no transfer at all -- the
    #  external device is expected to move the data and this model does not simulate it --
    #  so DMATCR has not been consumed and the manual conditions DMTE on exactly that.
    #  Asserting it would report a completion that did not happen.
    #  The #453 diagnostic has its OWN wording, so VAL_RE -- which matches the
    #  "... encoding N not implemented" family -- does not see it.  Counting with the
    #  wrong pattern reported zero lines on a build that was printing one, which is the
    #  vacuous-row shape in miniature: the row would have passed a mutant that removed
    #  the diagnostic entirely.
    x = CHCR_IE | CHCR_TD | RS_ACCEPTED
    buf, alive, st = wr(SH4_CHCR0, x, "X1", kw)
    d = IE_RE.findall(buf or "")
    row("X1 IE on the ACCEPTED resource select -- ALIVE, ONE line, NAMING channel 0",
        st and alive and d == ["0"],
        "alive=%s lines=%d %s" % (alive, len(d), d),
        "alive with one diagnostic.  This is the last guest-reachable host death that was "
        "in this file; pre-#453 the same store ended the process")

    #  ---- X2: the mutant a pass-1 seat named, and it is why X1 alone is not enough ------
    #  Add `dmac_chcr[ch] |= CHCR_TE;` just before the diagnostic and the host still
    #  survives and still prints once -- while falsely reporting an unperformed transfer
    #  COMPLETE, and making the next call return early at the `chcr & CHCR_TE` test.
    #  Nothing on that path may write ANY dma state: SAR, DAR, DMATCR and CHCR are all
    #  read-only there, checked line by line.
    for nm, addr, want in [("CHCR", SH4_CHCR0, x),
                           ("DMATCR", SH4_DMATCR0, 0x00000042),
                           ("SAR", SH4_SAR0, 0x0c001000),
                           ("DAR", SH4_DAR0, 0x0c002000)]:
        b2, a2, s2 = arm_then_read(x, addr, "X2" + nm, kw)
        got = P.dumped(b2)
        row("X2 %s still holds the value the guest armed it with (0x%08x)" % (nm, want),
            s2 and a2 and got == P.le(want),
            "%s readback=%s want=%s" % (nm, got, P.le(want)),
            "the declined path writes NOTHING -- SAR, DAR, DMATCR and CHCR are all "
            "read-only there.  Each is armed with a DISTINCT NON-RESET value first, "
            "because an earlier draft checked for 0 and a mutant that zeroes them passed "
            "at 24/24: 0 is also the reset value, so the row could not fail")

    #  ---- X3: the same request TWICE -- the latch, and the third round to need this ----
    #  X1 stores once, so an UNLATCHED fatal() is invisible to it: one store, one line,
    #  either way.  MEASURED as a survivor at 24/24 before this row existed.  #451 and
    #  #452 each learned the same thing about their own detectors; a latched diagnostic
    #  needs a repeat row or the latch is untested.
    buf3, alive3, st3 = two_stores(x, x, SH4_CHCR0, "X3")
    d3 = IE_RE.findall(buf3 or "")
    row("X3 the SAME declined request twice -- ONE line, still naming channel 0",
        st3 and alive3 and d3 == ["0"],
        "alive=%s lines=%d %s" % (alive3, len(d3), d3),
        "one line for two identical requests.  Two means the guard is gone and a guest "
        "looping on a legal DMA draws an unsilenceable line per store, which fatal() "
        "cannot be quieted out of")

    #  ---- X4: the SAME request on OTHER CHANNELS ---------------------------------------
    #  *** EVERY OTHER ROW IN THIS FILE DRIVES CHANNEL 0, AND A MUTANT THAT RESTORES THE
    #  HOST DEATH ON CHANNELS 1..7 PASSED ALL TWENTY-FIVE OF THEM. ***  Measured:
    #  `if (channel != 0) { fatal("TODO: sh4 dmac interrupt!"); exit(1); }` inserted ahead
    #  of the latch scored 25/25.  A pass-2 seat named it, and it is the FOURTH round
    #  running to find a detector covering one instance of a multi-instance thing --
    #  #451's two SCI sites, #452's two TLB devices, this round's eight channels.
    #
    #  It also makes the enum comment's "eight in total" a measurement rather than an
    #  assertion: without this row only one of the eight latch instances was ever used.
    #
    #  Channel 7 is at 0xffa0008c and NOT a stride past channel 3 -- registers for
    #  channels 4..7 restart at 0xffa00050 (sh4_dmacreg.h:67-85).
    for nm, addr, ch in [("X4a channel 1", SH4_CHCR1, "1"),
                         ("X4b channel 7", SH4_CHCR7, "7")]:
        b4, a4, s4 = wr(addr, x, nm.split()[0], kw)
        d4 = IE_RE.findall(b4 or "")
        row("%s -- host ALIVE, one line, and it NAMES that channel" % nm,
            s4 and a4 and d4 == [ch],
            "alive=%s lines=%s" % (a4, d4),
            "alive with exactly one diagnostic naming channel %s.  Every other row here "
            "drives channel 0, so a mutant that keeps channel 0 correct and kills the "
            "host on the rest is invisible without this" % ch)

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
