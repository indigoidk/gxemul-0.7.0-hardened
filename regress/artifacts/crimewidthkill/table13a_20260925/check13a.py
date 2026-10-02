#!/usr/bin/env python3
"""check13a.py -- #529 table 13a: score each leg MECHANICALLY against PRETABLE13a.out's sharpened EXACT sets.
Written BEFORE the table runs (its mtime and PRETABLE13a.out's precede every log).  Modelled on repair 14's
check_pred.py: anchored row extraction (only a ROW line ends in FAIL -- never a CRIMEP_ summary token), the tally
cross-checked against the extraction, the denominator pinned, and a truncated log refused rather than read.

A PREDICTION MISS is reported as a miss, never adopted.  An ESCAPE (a mutant at 204/204) is a FAILURE here: both
mutants are floor cells by the flagship's first-hand re-ruling, so an escape means repair 15 owes a carrier.
Run: python3 check13a.py   (reads logs/ beside this file)
"""
import io, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
LOGS = os.path.join(HERE, "logs")
ROWS = 204
EXACT = {
    "base":            set(),
    "M7_intmasklatch": {"imask sb", "imask lh", "imask sh"},
    "M8_ctllatch":     {"sb08 msg", "sh08b run", "gate run"},
}


def reds(leg):
    p = os.path.join(LOGS, "probe_%s.raw" % leg)
    if not os.path.exists(p):
        return None, None, None, False
    txt = io.open(p, encoding="utf-8", errors="replace").read()
    names, tally, ctl = set(), None, None
    for ln in txt.split(chr(10)):
        s = ln.rstrip()
        if s.endswith("FAIL") and not s.startswith("CRIMEP_"):
            names.add(ln[:15].strip())
        m = re.match(r"CRIMEP_RESULT=(\d+)/(\d+)", ln)
        if m:
            tally = (int(m.group(1)), int(m.group(2)))
        m = re.match(r"CRIMEP_CONTROL=(\S+)", ln)
        if m:
            ctl = m.group(1)
    return names, tally, ctl, ("CRIMEP_DONE" in txt)


def main():
    if not os.path.isdir(LOGS):
        print("no logs/ -- the table has not run")
        return 2
    bad, miss = [], []
    print("leg                  score      reds  control  verdict")
    for leg in ("base", "M7_intmasklatch", "M8_ctllatch"):
        r, tally, ctl, done = reds(leg)
        if tally is None or not done:
            bad.append((leg, "NO TALLY or NO CRIMEP_DONE -- truncated or absent; RE-RUN, do not read"))
            print("%-20s %-10s %4s  %-7s  *** TRUNCATED OR ABSENT ***" % (leg, "-", "-", "-"))
            continue
        if tally[1] != ROWS:
            bad.append((leg, "denominator %d, expected %d" % (tally[1], ROWS)))
        if tally[1] - tally[0] != len(r):
            bad.append((leg, "tally says %d red, extraction found %d" % (tally[1] - tally[0], len(r))))
        if ctl != "OK":
            bad.append((leg, "CRIMEP_CONTROL=%s -- a control row failed; the leg is not a measurement" % ctl))
        if r == EXACT[leg]:
            v = "exact"
        else:
            v = "*** PREDICTED %s GOT %s ***" % (sorted(EXACT[leg]), sorted(r))
            miss.append((leg, v))
        if leg != "base" and tally[0] >= ROWS:
            bad.append((leg, "*** ESCAPE %d/%d -- a floor cell with no carrier: repair 15 owes one ***" % tally))
        print("%-20s %-10s %4d  %-7s  %s" % (leg, "%d/%d" % tally, len(r), ctl, v))
    print("")
    if miss:
        print("PREDICTION MISSES (%d):" % len(miss))
        for leg, why in miss:
            print("  %-20s %s" % (leg, why))
    if bad:
        print("FAILURES (%d):" % len(bad))
        for leg, why in bad:
            print("  %-20s %s" % (leg, why))
        print("CHECK13A_FAIL")
        return 1
    print("CHECK13A_PASS_WITH_PREDICTION_MISSES" if miss else "CHECK13A_PASS")
    return 0


sys.exit(main())
