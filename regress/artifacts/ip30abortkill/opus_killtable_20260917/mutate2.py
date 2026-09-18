#!/usr/bin/env python3
"""Second mutant file -- kept SEPARATE from mutate.py so the first chain's
instrument is never edited underneath it (the frozen-copy rule, python form)."""
import sys

W = "/tmp/gxopus531"
TGT = W + "/tree/src/devices/dev_sgi_ip30.c"
BASE = W + "/ip30.BASE.c"
src = open(BASE, encoding="utf-8").read()
name = sys.argv[1]

if name == "BASE":
    out = src

elif name == "M7_tickbit49":
    #  ONE CHARACTER.  Move the tick guard off bit 50 onto bit 49.
    #  PRE-FIX this reddened `tick 49' (the host died on bit 49).  POST-FIX the
    #  only consequence is a latched announce, so both tick rows -- which score
    #  `alive'/`DEAD' and nothing else -- stay green.
    old = "if (d->imask0 & ((int64_t)1<<50)) {"
    if old not in src:
        sys.exit("MUTANT TEXT NOT FOUND: " + old)
    out = src.replace(old, "if (d->imask0 & ((int64_t)1<<49)) {")

elif name == "M6_clr28_isr":
    #  Clause-(d) operand conjunction at 0x10028: condition the guard on a field
    #  the guarded BODY reads (`d->isr' in `d->isr &= ~idata').  The ISR clear
    #  and its announce are both skipped whenever the ISR is already zero.
    old = ("\tcase 0x10028:")
    i = src.find(old)
    if i < 0:
        sys.exit("MUTANT TEXT NOT FOUND: case 0x10028")
    j = src.find("if (writeflag == MEM_WRITE) {", i)
    if j < 0:
        sys.exit("MUTANT TEXT NOT FOUND: writeflag guard after 0x10028")
    old2 = "if (writeflag == MEM_WRITE) {"
    out = src[:j] + "if (writeflag == MEM_WRITE && d->isr) {" + src[j + len(old2):]

else:
    sys.exit("unknown mutant " + name)

if name != "BASE" and out == src:
    sys.exit("MUTANT WAS A NO-OP -- refusing")
open(TGT, "w", encoding="utf-8", newline="").write(out)
print("applied %s: %d -> %d bytes" % (name, len(src), len(out)))
