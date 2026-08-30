"""Apply the WITNESS FIX LEG to a copy of dev_wdc.c.

    python3 mkfixleg.py <path-to-dev_wdc.c>

EXACT-TEXT REPLACEMENT WITH AN ASSERT, not a context diff.  A diff applied years later
can land on shifted context and still "succeed"; an exact match that occurs exactly once
either fires or says so.  The two asserts below are the whole guard: the anchor must
occur ONCE, and the file must not already carry the edit.

WHAT THE FIX LEG IS AND IS NOT.  It is not a proposed shipped fix.  It exists to prove
the witness CAN go green -- vacuity-floor clause (a)/(b) demand a detector that reds on
the pre-fix build and greens on a repaired one, and without a repaired build to run
against, "capable of showing it green" is an assertion rather than a measurement.

It changes the WRITE path only.  The READ path is left byte-for-byte alone, so the sole
difference between the two legs is the aliased STORE -- which is the defect under test.
A shipped fix would additionally have to decide what a READ of 0x3f7 returns (on real
hardware the Drive Address Register returns an inverted drive/head select, not the alt
status), and that is a separate design question this witness deliberately does not
prejudge.
"""
import io
import sys

P = sys.argv[1]
s = io.open(P, encoding="utf-8", newline="").read()

ANCHOR = (
    '\telse {\n'
    '\t\tdebug("[ wdc: write to ALT. CTRL: 0x%02x ]\\n",\n'
    '\t\t    (int)idata);\n'
)

REPLACEMENT = (
    '\telse if (relative_addr != 0) {\n'
    '\t\t/*  WITNESS FIX LEG ONLY -- NOT a proposed shipped fix.\n'
    '\n'
    '\t\t    dev_wdc_init registers this region TWO BYTES wide, so offset 1\n'
    '\t\t    is 0x3f7 -- the Drive Address Register, READ-ONLY on real ATA\n'
    '\t\t    hardware.  The committed handler reads relative_addr zero times,\n'
    '\t\t    so a guest store there is executed as a store to Device Control\n'
    '\t\t    and (since #481) performs a full soft reset.\n'
    '\n'
    '\t\t    Decline the write.  The READ path above is untouched, so the only\n'
    '\t\t    difference between the two legs of the witness is the aliased\n'
    '\t\t    STORE.  */\n'
    '\t\tdebug("[ wdc: write to DRIVE ADDRESS (read-only): 0x%02x,"\n'
    '\t\t    " ignored ]\\n", (int)idata);\n'
    '\t} else {\n'
    '\t\tdebug("[ wdc: write to ALT. CTRL: 0x%02x ]\\n",\n'
    '\t\t    (int)idata);\n'
)

n = s.count(ANCHOR)
assert n == 1, "anchor occurs %d times in %s (want 1)" % (n, P)
assert "WITNESS FIX LEG ONLY" not in s, "fix leg already applied to %s" % P

io.open(P, "w", encoding="utf-8", newline="").write(s.replace(ANCHOR, REPLACEMENT, 1))
print("  fix leg applied to %s" % P)
