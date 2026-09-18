#!/usr/bin/env python3
"""Apply ONE named mutant to /tmp/gxopus531/tree/src/devices/dev_sgi_ip30.c.
Source of truth for the baseline is /tmp/gxopus531/ip30.BASE.c (a copy of the
GXEMUL-SEC working tree taken before mutant 1), NEVER the script's own backup.
MUTANT-TEXT-NOT-FOUND is a hard FAIL, so every find-text doubles as a presence pin.
"""
import sys

W = "/tmp/gxopus531"
TGT = W + "/tree/src/devices/dev_sgi_ip30.c"
BASE = W + "/ip30.BASE.c"

src = open(BASE, encoding="utf-8").read()

ANN = ('\t\t\tif (!(d->warned & IP30_W_ISR)) {\n'
       '\t\t\t\td->warned |= IP30_W_ISR;\n'
       '\t\t\t\tfatal("[ sgi_ip30: interrupt-status rewrite "\n'
       '\t\t\t\t    "not implemented  (once) ]\\n");\n'
       '\t\t\t}\n')

TICKANN = ('\t\tif (!(d->warned & IP30_W_TICK)) {\n'
           '\t\t\td->warned |= IP30_W_TICK;\n'
           '\t\t\tfatal("[ sgi_ip30: timer interrupt delivery not "\n'
           '\t\t\t    "implemented  (once) ]\\n");\n'
           '\t\t}\n')

name = sys.argv[1]


def occ(s, n):
    """0-based index of the n-th occurrence of s in src."""
    i = -1
    for _ in range(n + 1):
        i = src.find(s, i + 1)
        if i < 0:
            sys.exit("MUTANT TEXT NOT FOUND (occurrence %d)" % n)
    return i


if name == "BASE":
    out = src

elif name == "M1_silent30":
    #  Delete the latched announce from the 0x10030 WRITE arm (the 5th ISR
    #  announce block).  Keep survival.  Member 2 (silent decline).
    #  This is *exactly* the mutant `kill 30 txt' claims to close.
    n = src.count(ANN)
    if n != 5:
        sys.exit("expected 5 ISR announce blocks, found %d" % n)
    i = occ(ANN, 4)
    out = src[:i] + src[i + len(ANN):]

elif name == "M2_nolatch":
    #  One-token clause-(d) weakening of the ADDED predicate: the latch mask
    #  goes to zero, so `!(d->warned & IP30_W_ISR)' is always true and every
    #  ISR access announces.  A guest-drivable log flood (floodclass).
    old = "#define\tIP30_W_ISR\t(1 << 1)"
    if old not in src:
        sys.exit("MUTANT TEXT NOT FOUND: " + old)
    out = src.replace(old, "#define\tIP30_W_ISR\t(0 << 1)")

elif name == "M3_sharedbit":
    #  One-CHARACTER collision: the two latches share bit 0.  This is the
    #  precise defect the fix's own header comment says two bits prevent.
    old = "#define\tIP30_W_ISR\t(1 << 1)"
    if old not in src:
        sys.exit("MUTANT TEXT NOT FOUND: " + old)
    out = src.replace(old, "#define\tIP30_W_ISR\t(1 << 0)")

elif name == "M4_silenttick":
    #  Delete the latched announce from DEVICE_TICK.  Keep survival.
    if src.count(TICKANN) != 1:
        sys.exit("expected 1 tick announce block, found %d" % src.count(TICKANN))
    out = src.replace(TICKANN, "")

elif name == "M5_silent28wr":
    #  Delete the latched announce from the 0x10028 WRITE arm (3rd block).
    if src.count(ANN) != 5:
        sys.exit("expected 5 ISR announce blocks")
    i = occ(ANN, 2)
    out = src[:i] + src[i + len(ANN):]

else:
    sys.exit("unknown mutant " + name)

if name != "BASE" and out == src:
    sys.exit("MUTANT WAS A NO-OP -- refusing")
open(TGT, "w", encoding="utf-8", newline="").write(out)
print("applied %s: %d -> %d bytes" % (name, len(src), len(out)))
