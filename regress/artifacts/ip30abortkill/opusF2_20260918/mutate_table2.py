#!/usr/bin/env python3
"""#531 F2 mutator, SECOND TABLE -- the LATCH-SET statements per site, and the
DEVICE_TICK counter update.  MUTANT-TEXT-NOT-FOUND is a HARD FAIL (presence pin).

NO BACKSLASH ESCAPES ANYWHERE IN THIS FILE.  The first version of it was written
through a bash heredoc and one backslash level was consumed in each direction --
the carrier's own documented hazard -- which turned a Python string literal into a
syntax error and aborted the table at mutant 1.
"""
import sys

SRC = "/tmp/gxopusf2/src/devices/dev_sgi_ip30.c"
BASE = "/tmp/gxopusf2_BASELINE.c"
LATCH_ISR = "d->warned |= IP30_W_ISR;"
LATCH_TICK = "d->warned |= IP30_W_TICK;"
COUNTER = "d->reg_0x20000 += 1000;"


def drop_nth(block, needle, n):
    """Delete the n-th (0-based) occurrence of `needle` from `block`."""
    parts = block.split(needle)
    assert len(parts) - 1 > n, "only %d occurrences, wanted #%d" % (len(parts) - 1, n)
    out = needle.join(parts[:n + 1]) + parts[n + 1]
    for p in parts[n + 2:]:
        out = out + needle + p
    assert out != block, "MUTANT TEXT NOT FOUND -- HARD FAIL"
    return out


def apply(name):
    txt = open(BASE).read()
    i20 = txt.index("case 0x10020:")
    i28 = txt.index("case 0x10028:")
    i30 = txt.index("case 0x10030:")
    i20000 = txt.index("case 0x20000:")

    if name == "MH_nocounter":
        #  THE DE-ESCALATION ACCEPT SIDE AT THE TICK ARM.  The shipped product comment
        #  says "The counter update above still runs, which is what `acc 20000' pins".
        #  `acc 20000' accepts (readback - 0x1234) % 1000 == 0 and N == 0 IS ADMISSIBLE,
        #  so deleting the increment should leave it GREEN.  Predicted 27/27.
        head = txt[:i20]
        assert head.count(COUNTER) == 1, head.count(COUNTER)
        out = head.replace(COUNTER, "", 1) + txt[i20:]
    elif name == "ME_nolatchsettick":
        #  LATCH DEFEAT AT THE TICK SITE.  Guest arms imask0 bit 50 once -> one announce
        #  PER TICK forever.  The unqualified "(once)" marker becomes false; floodclass.
        head = txt[:i20]
        assert head.count(LATCH_TICK) == 1, head.count(LATCH_TICK)
        out = head.replace(LATCH_TICK, "", 1) + txt[i20:]
    elif name == "MF_nolatchset28rd":
        #  LATCH DEFEAT AT THE 0x10028 **READ** ARM -- the SECOND access `latch 1x' makes.
        blk = txt[i28:i30]
        assert blk.count(LATCH_ISR) == 2, blk.count(LATCH_ISR)
        out = txt[:i28] + drop_nth(blk, LATCH_ISR, 1) + txt[i30:]
    elif name == "MG_nolatchset30wr":
        blk = txt[i30:i20000]
        assert blk.count(LATCH_ISR) == 1, blk.count(LATCH_ISR)
        out = txt[:i30] + blk.replace(LATCH_ISR, "", 1) + txt[i20000:]
    elif name == "RESTORE":
        open(SRC, "w").write(txt)
        print("RESTORED from frozen baseline")
        return
    else:
        print("UNKNOWN MUTANT " + name)
        sys.exit(9)

    assert out != txt, "MUTANT TEXT NOT FOUND -- HARD FAIL"
    open(SRC, "w").write(out)
    print("MUTANT " + name + " APPLIED")


apply(sys.argv[1])
