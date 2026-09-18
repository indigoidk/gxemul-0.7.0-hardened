#!/usr/bin/env python3
"""M8 / M9 -- two more cells.

M8 (FUNCTIONAL): delete the clear itself at 0x10028.  De-escalation clause:
0x10028's WRITE used to gate host death, so the detector owes its ACCEPT side --
proof that a legal clear still LANDS.  `isr keep' seeds through 0x10020 and reads
back through 0x10030; nothing in the probe ever writes 0x10028 and reads the
result.

M9 (ATTRIBUTION): delete the announce in the 0x10020 WRITE arm only.  If
`kill 30 txt' stays green, then the shared latch plus the identical string mean
that row cannot attribute to ANY single arm -- the NEXT ISR access in the same
session (the 0x10020 LOAD) announces in its place.
"""
import sys

W = "/tmp/gxopus531"
TGT = W + "/tree/src/devices/dev_sgi_ip30.c"
BASE = W + "/ip30.BASE.c"
src = open(BASE, encoding="utf-8").read()
name = sys.argv[1]

ANN = ('\t\t\tif (!(d->warned & IP30_W_ISR)) {\n'
       '\t\t\t\td->warned |= IP30_W_ISR;\n'
       '\t\t\t\tfatal("[ sgi_ip30: interrupt-status rewrite "\n'
       '\t\t\t\t    "not implemented  (once) ]\\n");\n'
       '\t\t\t}\n')

if name == "BASE":
    out = src
elif name == "M8_noclr28":
    old = "\t\t\td->isr &= ~idata;\n"
    if src.count(old) != 1:
        sys.exit("expected exactly 1 `d->isr &= ~idata;' at that indent, found %d"
                 % src.count(old))
    out = src.replace(old, "")
elif name == "M9_silent20wr":
    if src.count(ANN) != 5:
        sys.exit("expected 5 ISR announce blocks, found %d" % src.count(ANN))
    i = src.find(ANN)          # occurrence 0 == the 0x10020 WRITE arm
    out = src[:i] + src[i + len(ANN):]
else:
    sys.exit("unknown mutant " + name)

if name != "BASE" and out == src:
    sys.exit("MUTANT WAS A NO-OP -- refusing")
open(TGT, "w", encoding="utf-8", newline="").write(out)
print("applied %s: %d -> %d bytes" % (name, len(src), len(out)))
