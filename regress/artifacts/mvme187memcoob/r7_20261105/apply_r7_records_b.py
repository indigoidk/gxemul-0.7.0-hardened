#!/usr/bin/env python3
"""apply_r7_records_b.py -- the second text-only pass on regress/mvme187_memc_probe.py's docstring (after apply_r7_records.py), from
a second reading of the edited text: (1) table 5's "every one in a debt family disclosed in the CONTRACT above" is false for the
eight own-latch cells (family (6) excepts them; REG_MYTHOS 2(d) places them in the floor) -- deleted; (2) B3's extra row in table
6, R17 f3 r2, varies run to run (r7_20261105/b3repeat/: three runs of one B3 binary) -- said so with the measured values instead of
"table 6 adds R17 f3 r2"; (3) one over-long line re-wrapped.  Exact replacements, each asserted once; proved text-only afterwards.
Usage: python -I apply_r7_records_b.py <probe>
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
vals = []
for i in (1, 2, 3):
    t = io.open(os.path.join(HERE, "b3repeat", "probe_B3run%d.out" % i), encoding="latin-1").read()
    assert t.rstrip().endswith("MVME187_MEMC_PROBE_DONE")
    vals.append(re.search(r"^R17 f3 r2\s+(\S+)", t, re.M).group(1))
t6 = io.open(os.path.join(HERE, "table6", "probe_B3_idx_read.out"), encoding="latin-1").read()
v6 = re.search(r"^R17 f3 r2\s+(\S+)", t6, re.M).group(1)
assert v6 == "0xd8" and vals == ["0x66", "0x34", "0x15"], (v6, vals)

path = sys.argv[1]
s = io.open(path, encoding="latin-1", newline="").read()
assert "\r" not in s


def rep(old, new):
    global s
    assert s.count(old) == 1, (old[:70], s.count(old))
    s = s.replace(old, new)


rep("predicted; one leg missed its prediction: B3 reddened R17 f3 r2 as well as the four below (r7_20261105/table6/VERDICT.md).\n",
    "predicted; one leg missed its prediction: B3 also reddened R17 f3 r2, whose load at +0xf3 reads, under B3, a byte 111 bytes past\n"
    "the device struct's 132-byte allocation -- 0x0 in table 5, %s in table 6, %s, %s and %s on three runs of one B3 binary\n"
    "(r7_20261105/table6/VERDICT.md, r7_20261105/b3repeat/).\n" % (v6, vals[0], vals[1], vals[2]))
rep("26,999 predicted-red cells; 665 green, every one predicted and every one in a debt family disclosed in the CONTRACT above); every\n",
    "26,999 predicted-red cells; 665 green, every one predicted); every\n")
rep("(table 4; the same four in table 5, SCORES.txt:8; table 6 adds R17 f3 r2).",
    "(table 4; the same four in table 5, SCORES.txt:8, and in table 6, with R17 f3 r2 as well on a run-to-run value: TABLE 6 above).")
rep("non-first stores at 0x05, 0xff and 0xffffffff (R3, R5, R9); R18 adds a first store of 0x01 and non-first stores of 0x01 and\n"
    "0x00 in both categories; every store category\n{memconf, default, chipid, chiprev}",
    "non-first stores at 0x05, 0xff and 0xffffffff (R3, R5, R9); R18 adds a\nfirst store of 0x01 and non-first stores of 0x01 and 0x00 in both "
    "categories; every store category {memconf, default, chipid, chiprev}")
io.open(path, "w", encoding="latin-1", newline="").write(s)
print("APPLIED to %s (R17 f3 r2 under B3: table 6 %s; repeats %s)" % (path, v6, ", ".join(vals)))
