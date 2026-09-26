#!/usr/bin/env python3
"""#549 v6 pass (Opus measuring seat): floor edits of the fixed PORT arm NOT in table 6, to test whether session B's
per-width aggregate read leaves a joint cell open.  Each is ONE text change with exactly one match (REFUSED otherwise).

  WB_* width x bit    PB_* previous-selector x bit    LB_* latch x bit    MB_* multi-bit value class
  SN_* a real narrowing as a control (must red)       EQ_* an equivalent as a denominator anchor (must be 117/117)
usage: gen_v6floor.py <fix.c> <outdir>"""
import io
import os
import sys

PRED = "else if (idata >= DEV_FBCTRL_NPORTS) {"
N = "DEV_FBCTRL_NPORTS"


def pred(e):
    return "else if (%s) {" % e


EDITS = [
    # width x bit: accept 2^5 only when written by sh -- B walks 2^5 in its sh group, so expect RED
    ("WB_sh32", "accept 0x20 only by sh (len 2)", pred("idata >= %s && !(idata == 0x20 && len == 2)" % N)),
    # latch x bit (set): accept 2^4 only when the latch is already set -- B refuses 2^4 with latch set, expect RED
    ("LB_set16", "accept 0x10 only when warned_port set", pred("idata >= %s && !(idata == 0x10 && d->warned_port)" % N)),
    # latch x bit (unset): accept 2^4 only when latch unset -- no session's FIRST refusal is 2^4, so it never fires: EQUIVALENT
    ("LB_unset16", "accept 0x10 only when warned_port unset (never a first refusal)",
     pred("idata >= %s && !(idata == 0x10 && !d->warned_port)" % N)),
    # previous-selector x bit: accept 2^4 only when the previous selector is 3 -- B is at 5; two-axis, expect 117/117 (NOT CLAIMED (0))
    ("PB_prev3_16", "accept 0x10 only when current_port == 3", pred("idata >= %s && !(idata == 0x10 && d->current_port == 3)" % N)),
    # multi-bit value class: accept any value with exactly 4 bits set -- no row writes one; single axis (value)
    ("MB_pc4", "accept idata>=8 with popcount 4", pred("idata >= %s && __builtin_popcountll(idata) != 4" % N)),
    # multi-bit: accept a specific 2-bit value 0x18 (no row writes it) -- single value, like A1_not10 (disclosed (3))
    ("MB_v18", "accept 0x18 only", pred("idata >= %s && idata != 0x18" % N)),
    # control: a real narrowing that MUST red -- signed compare accepts negative (all-ones); X4/P refuse all-ones
    ("SN_signed", "control: (int64_t) idata >= NPORTS", pred("(int64_t) idata >= (int64_t) %s" % N)),
    # denominator anchor: an equivalent narrowing -- (idata >> 3) nonzero == idata >= 8; expect 117/117, not a breach
    ("EQ_shift3", "equivalent: (idata >> 3) != 0", pred("(idata >> 3) != 0")),
]


def main():
    fixp, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    base = io.open(fixp, encoding="utf-8", newline="").read()
    assert base.count(PRED) == 1
    for name, cls, new in EDITS:
        io.open(os.path.join(out, name + ".c"), "w", encoding="utf-8", newline="").write(base.replace(PRED, new))
        print("%-12s %s" % (name, cls))
    print("EDITS_WRITTEN=%d" % len(EDITS))


if __name__ == "__main__":
    main()
