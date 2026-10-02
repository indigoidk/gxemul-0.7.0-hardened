#!/usr/bin/env python3
"""analyze46.py -- every COUNT the answer states, DERIVED from the 92 replay logs (never hand-tallied).
Classes: EQUIVALENT = no row red in either latch state (40 excepted: its debug() line is the host difference);
TEXT = 10, 11, 14, 15 (the difference is the CONTROL fatal() text, counted by rows); GUEST = the rest.
Also: which guest-visible entries a `p *' row holds latch-SET, which cells only CONTROL rows hold, and the
repair-13 incidental eight checked against the measured latch-SET reds.  Sentinel: ANALYZE46_DONE."""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from predict46 import CONTROL_ROWS


def red(k, lt):
    t = open(os.path.join(HERE, "runs", "k%02d%s.raw" % (k, lt)), encoding="latin-1").read()
    assert "REPLAY46_DONE" in t and "CRIMEP_DONE" in t, (k, lt)
    return [x.strip() for x in re.search(r"^FAILING: ?(.*)$", t, re.M).group(1).split(",") if x.strip()]


R = {k: (red(k, "C"), red(k, "S")) for k in range(1, 47)}
TEXT = {10, 11, 14, 15}
EQ = [k for k in R if not R[k][0] and not R[k][1] and k != 40]
HOST = [k for k in R if not R[k][0] and not R[k][1] and k == 40]
TXT = [k for k in R if k in TEXT]
GUEST = [k for k in R if k not in EQ and k not in HOST and k not in TEXT]
both = [k for k in GUEST if R[k][0] and R[k][1]]
set_only = [k for k in GUEST if R[k][1] and not R[k][0]]
clr_only = [k for k in GUEST if R[k][0] and not R[k][1]]
p_set = [k for k in GUEST if any(r.startswith("p ") for r in R[k][1])]
nop_set = [k for k in GUEST if R[k][1] and not any(r.startswith("p ") for r in R[k][1])]
ctl_only = [(k, lt) for k in R for i, lt in enumerate("CS") if R[k][i] and all(r in CONTROL_ROWS for r in R[k][i])]
text_both = [k for k in TXT if R[k][0] and R[k][1]]
INC8 = (21, 23, 25, 27, 31, 34, 35, 46)
inc_ok = [(k, [r for r in R[k][1] if not r.startswith("p ")]) for k in INC8]
P23 = (2, 5, 6, 7, 9, 18, 19, 20, 22, 24, 26, 28, 29, 30, 32, 33, 36, 37, 38, 39, 41, 42, 45)
p23_ok = [k for k in P23 if any(r.startswith("p ") for r in R[k][1])]
print("EQUIVALENT (no row, either state, 40 excepted) n=%d %s" % (len(EQ), EQ))
print("HOST-DIAGNOSTIC ONLY n=%d %s" % (len(HOST), HOST))
print("TEXT-ROWED n=%d %s  -- rowed in BOTH states: %s" % (len(TXT), TXT, text_both))
print("GUEST n=%d  both-states=%d  SET-only=%s  CLEAR-only=%s" % (len(GUEST), len(both), set_only, clr_only))
print("GUEST held latch-SET by a `p *' row: n=%d; by non-p rows only: %s" % (len(p_set), nop_set))
print("cells held ONLY by CONTROL rows: %s" % ["%d%s %s" % (k, lt, R[k]["CS".index(lt)]) for k, lt in ctl_only])
print("repair 13's 23 p-rowed, each holding a p-row latch-SET now: %d of %d" % (len(p23_ok), len(P23)))
print("repair 13's incidental 8, their NON-p latch-SET reds now:")
for k, rows in inc_ok:
    print("   %2d  %s" % (k, rows))
print("TOTAL %d = %d guest + %d text + %d host + %d equivalent" % (len(R), len(GUEST), len(TXT), len(HOST), len(EQ)))
print("ANALYZE46_DONE")
