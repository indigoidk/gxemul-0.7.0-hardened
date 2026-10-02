#!/usr/bin/env python3
"""check15a.py -- #529 table 15a: score the two predicted ESCAPES mechanically against PRETABLE15a.out.  Written
before the table runs.  The shape is check14.py's: anchored row extraction, tally cross-check, pinned denominator,
predicted CONTROL verdict, and a log without its CRIMEP_DONE sentinel refused rather than read."""
import io, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
LOGS = os.path.join(HERE, "logs")
ROWS = 218
EXACT = {"H_noresetclear": set(), "E_noendianclear": set()}


def reds(leg):
    p = os.path.join(LOGS, "probe_%s.raw" % leg)
    if not os.path.exists(p):
        return None, None, None, False
    txt = io.open(p, encoding="utf-8", errors="replace").read()
    names, tally, ctl = set(), None, None
    for ln in txt.split(chr(10)):
        s = ln.rstrip()
        if s.endswith("FAIL") and not s.startswith("CRIMEP_"):
            names.add(ln[:16].strip())
        m = re.match(r"CRIMEP_RESULT=(\d+)/(\d+)", ln)
        if m:
            tally = (int(m.group(1)), int(m.group(2)))
        m = re.match(r"CRIMEP_CONTROL=(\S+)", ln)
        if m:
            ctl = m.group(1)
    return names, tally, ctl, txt.rstrip().endswith("CRIMEP_DONE")


def main():
    bad, miss = [], []
    for leg in ("H_noresetclear", "E_noendianclear"):
        r, tally, ctl, done = reds(leg)
        if tally is None or not done:
            bad.append((leg, "NO TALLY or NO CRIMEP_DONE -- truncated or absent; RE-RUN, do not read"))
            print("%-18s *** TRUNCATED OR ABSENT ***" % leg)
            continue
        if tally[1] != ROWS:
            bad.append((leg, "denominator %d, expected %d" % (tally[1], ROWS)))
        if tally[1] - tally[0] != len(r):
            bad.append((leg, "tally says %d red, extraction found %d" % (tally[1] - tally[0], len(r))))
        if ctl != "OK":
            bad.append((leg, "CRIMEP_CONTROL=%s -- a control row moved" % ctl))
        if r == EXACT[leg]:
            v = "exact -- ESCAPE CONFIRMED (%d/%d)" % tally
        else:
            v = "*** PREDICTED ESCAPE, GOT %d/%d, failing %s ***" % (tally[0], tally[1], sorted(r))
            miss.append((leg, v))
        print("%-18s %-8s %s" % (leg, ctl, v))
    if miss:
        print("PREDICTION MISSES (%d): the cell was carried by the rows named" % len(miss))
    if bad:
        for leg, why in bad:
            print("  FAIL %-18s %s" % (leg, why))
        print("CHECK15A_FAIL")
        return 1
    print("CHECK15A_PASS_WITH_PREDICTION_MISSES" if miss else "CHECK15A_PASS")
    return 0


sys.exit(main())
