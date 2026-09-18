#!/usr/bin/env python3
"""#531 F2 mutator.  MUTANT-TEXT-NOT-FOUND is a HARD FAIL (presence pin)."""
import sys

SRC = "/tmp/gxopusf2/src/devices/dev_sgi_ip30.c"
BASE = "/tmp/gxopusf2_BASELINE.c"

def blocks(txt):
    i20 = txt.index("\tcase 0x10020:")
    i28 = txt.index("\tcase 0x10028:")
    i30 = txt.index("\tcase 0x10030:")
    i20000 = txt.index("\tcase 0x20000:")
    return i20, i28, i30, i20000

def apply(name):
    txt = open(BASE).read()
    i20, i28, i30, i20000 = blocks(txt)
    blk20 = txt[i20:i28]

    if name == "MA_assign20wr":
        #  LATCH COLLISION, ASYMMETRIC.  One character deleted: the ISR arm now
        #  CLEARS the TICK latch bit instead of ORing its own in.
        old = "d->warned |= IP30_W_ISR;"
        new = "d->warned = IP30_W_ISR;"
        assert blk20.count(old) == 2, blk20.count(old)
        nb = blk20.replace(old, new, 1)          # FIRST = the WRITE arm
    elif name == "MB_nolatchset20wr":
        #  LATCH DEFEAT, PER-ARM.  Keep the guard, null its repair (clause (d) canonical).
        old = "\t\t\t\td->warned |= IP30_W_ISR;\n"
        new = ""
        assert blk20.count(old) == 2, blk20.count(old)
        nb = blk20.replace(old, new, 1)
    elif name == "MC_len4":
        #  WIDTH AXIS.  "a condition qualified" -- clause (d)'s own worked example.
        old = "\t\tif (writeflag == MEM_WRITE) {"
        new = "\t\tif (writeflag == MEM_WRITE && len == 4) {"
        assert blk20.count(old) == 1, blk20.count(old)
        nb = blk20.replace(old, new, 1)
    elif name == "MD_assigntick":
        #  The MIRROR of MA, in the TICK arm.
        txt2 = txt[:i20]
        old = "d->warned |= IP30_W_TICK;"
        new = "d->warned = IP30_W_TICK;"
        assert txt2.count(old) == 1, txt2.count(old)
        out = txt2.replace(old, new, 1) + txt[i20:]
        open(SRC, "w").write(out)
        print("MUTANT %s APPLIED (tick arm)" % name)
        return
    elif name == "RESTORE":
        open(SRC, "w").write(txt)
        print("RESTORED from frozen baseline")
        return
    else:
        print("UNKNOWN MUTANT %s" % name); sys.exit(9)

    assert nb != blk20, "MUTANT TEXT NOT FOUND -- HARD FAIL"
    open(SRC, "w").write(txt[:i20] + nb + txt[i28:])
    print("MUTANT %s APPLIED" % name)

apply(sys.argv[1])
