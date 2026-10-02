#!/usr/bin/env python3
"""specs46.py PROBE -- the 92 replay specs (46 ACCEPTS entries x latch C/S), DERIVED from the probe's own ACCEPTS
tuple (never transcribed).  Prints `k latch SPEC' lines.  Sentinel: SPECS46_DONE."""
import ast, re, sys

src = open(sys.argv[1], encoding="utf-8").read()
m = re.search(r"^ACCEPTS = (\(.*?\))\nKINDS = ACCEPTS", src, re.S | re.M)
ACCEPTS = ast.literal_eval(m.group(1))
assert len(ACCEPTS) == 46, len(ACCEPTS)
for k, (op, off, val) in enumerate(ACCEPTS, 1):
    P = op.endswith("P")
    bop = op[:2] if P else op
    ln = 8 if bop in ("sd", "ld") else 4
    d = "W" if bop[0] == "s" else "R"
    win = ("1" if P else "0") if off == 0 else "*"
    v = ("%x" % val) if (off == 8 and d == "W") else "*"
    for lt in ("C", "S"):
        print("%d %s %d:%s:%x:%s:%s:%s  %s+0x%x%s" % (k, lt, ln, d, off, win, v, lt, op, off,
                                                   ("=0x%x" % val) if v != "*" else ""))
print("SPECS46_DONE")
