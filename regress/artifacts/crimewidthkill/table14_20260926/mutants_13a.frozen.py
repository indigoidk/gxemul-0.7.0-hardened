#!/usr/bin/env python3
"""mutants_13a.py NAME SRC DST -- #529 table 13a: the two decline LABEL SWAPS repair 14's stop condition requires MEASURED
(flagship first-hand re-ruling 2026-09-25, rerule_20260925/fable5_rerule_529_20260925.md, STOP: "the INTMASK and
CONTROL-write label-swaps are genuinely unmeasured ... Cost is two builds").

The shape is repair 14's latch_label() (repair14_20260916/mutants_adj.frozen.py), copied VERBATIM so M7/M8 are the same
edit as M3_timelatch/M5_revlatch/M6_istlatch with only the label changed: the goto moves inside the latch block, then
is re-issued for every label EXCEPT the named one -- so once the width latch is SET, a narrow access at that label falls
through into the register switch instead of being declined.

Exact-string edits on the BASELINE (the uncommitted #529 working set, dev_sgi_ip32.c 8c1d1545).  MUTANT-TEXT-NOT-FOUND
is a hard FAIL, so every find-text doubles as a presence pin.  No double backslash anywhere in this file.
"""
import io, sys

name, src, dst = sys.argv[1], sys.argv[2], sys.argv[3]
s = io.open(src, encoding="latin-1", newline="").read()   # newline="": no CRLF translation on Windows

CLOSE_GOTO = "\t\t}\n\t\tgoto crime_declined;\n"


def sub(old, new):
    global s
    n = s.count(old)
    if n != 1:
        sys.exit("MUTANT TEXT NOT FOUND (or not unique) for %s: %d occurrences" % (name, n))
    s = s.replace(old, new)


def latch_label(lab):
    sub(CLOSE_GOTO,
        ("\t\t\tgoto crime_declined;\n"
         "\t\t}\n"
         "\t\tif (relative_addr != " + lab + ")\n"
         "\t\t\tgoto crime_declined;\n"))


if name == "base":
    pass
elif name == "M7_intmasklatch":
    latch_label("CRIME_INTMASK")
elif name == "M8_ctllatch":
    latch_label("CRIME_CONTROL")
else:
    sys.exit("unknown mutant %s" % name)

io.open(dst, "w", encoding="latin-1", newline="").write(s)
print("APPLIED %s" % name)
