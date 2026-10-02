#!/usr/bin/env python3
"""check14.py -- #529 table 14 (repair 15): score each leg MECHANICALLY against PRETABLE14.out's exact sets.
Written BEFORE the table runs (its mtime and PRETABLE14.out's precede every log).  The shape is table 13a's
check13a.py: anchored row extraction (only a ROW line ends in FAIL -- never a CRIMEP_ summary token), the tally
cross-checked against the extraction, the denominator pinned, the CONTROL verdict predicted per leg, and a truncated
log refused rather than read.

A PREDICTION MISS is reported as a miss, never adopted.  An ESCAPE -- a leg predicted to red something that scores
218/218 -- is a FAILURE here: every such leg is a floor cell, so an escape means repair 15's rows do not carry it.
Run: python3 check14.py   (reads logs/ beside this file)
"""
import io, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
LOGS = os.path.join(HERE, "logs")
ROWS = 218
TL = {"tl lb", "tl sb", "tl lh", "tl sh"}
RL = {"rl lb pc", "rl lh pc", "rl sb pc", "rl sh pc"}
M1_T12 = {"sb08 msg", "sh08b run", "imask sb", "imask lh", "imask sh", "istat sb", "istat lh", "istat sh",
          "gate run", "mid nodflt"}
EXACT = {
    "base":               set(),
    "G_clr_ctl4r":        set(),
    "G_clr_imk4r":        {"gate line"},
    "G_clr_ist4r":        {"acc istat lw"},
    "G_glm_tim4clear":    {"c t4w gap", "c t4r gap"},
    "G_lane_ctl":         {"p acc ctl4r"},
    "K_ctl4w_reset_post": {"rst 4w"},
    "K_ctl8w_reset_post": {"rst 8w"},
    "M1_gotolatch":       M1_T12 | TL | RL,
    "M2_ld278clr":        {"top8 clear"},
    "M3_timelatch":       set(TL),
    "M4_timeplain":       {"time lb", "time sb", "time lh", "time sh"} | TL,
    "M5_revlatch":        set(RL),
    "M6_istlatch":        {"istat sb", "istat lh", "istat sh"},
    "W_ctl8w":            {"p acc ctl msg", "rst 8w"},
    "M7_intmasklatch":    {"imask sb", "imask lh", "imask sh"},
    "M8_ctllatch":        {"sb08 msg", "sh08b run", "gate run"},
    "D_nodogclear":       {"ctldog sw msg", "ctldog sd msg"},
}
CONTROL = dict((leg, "OK") for leg in EXACT)
CONTROL["G_clr_imk4r"] = "FAIL"          # `gate line' is in the CRIMEP_CONTROL set
ORDER = ("base", "G_glm_tim4clear", "G_clr_ist4r", "G_clr_ctl4r", "G_clr_imk4r", "G_lane_ctl", "K_ctl4w_reset_post",
         "K_ctl8w_reset_post", "M1_gotolatch", "M2_ld278clr", "M3_timelatch", "M4_timeplain", "M5_revlatch",
         "M6_istlatch", "W_ctl8w", "M7_intmasklatch", "M8_ctllatch", "D_nodogclear")
assert sorted(ORDER) == sorted(EXACT), "ORDER and EXACT disagree"


def reds(leg):
    p = os.path.join(LOGS, "probe_%s.raw" % leg)
    if not os.path.exists(p):
        return None, None, None, False
    txt = io.open(p, encoding="utf-8", errors="replace").read()
    names, tally, ctl = set(), None, None
    for ln in txt.split(chr(10)):
        s = ln.rstrip()
        if s.endswith("FAIL") and not s.startswith("CRIMEP_"):
            names.add(ln[:16].strip())          # row(): "%-16s %-20s ..." -- the name is the first 16 columns
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
    for leg in ORDER:
        r, tally, ctl, done = reds(leg)
        if tally is None or not done:
            bad.append((leg, "NO TALLY or NO CRIMEP_DONE -- truncated or absent; RE-RUN, do not read"))
            print("%-20s %-10s %4s  %-7s  *** TRUNCATED OR ABSENT ***" % (leg, "-", "-", "-"))
            continue
        if tally[1] != ROWS:
            bad.append((leg, "denominator %d, expected %d" % (tally[1], ROWS)))
        if tally[1] - tally[0] != len(r):
            bad.append((leg, "tally says %d red, extraction found %d" % (tally[1] - tally[0], len(r))))
        if ctl != CONTROL[leg]:
            bad.append((leg, "CRIMEP_CONTROL=%s, predicted %s -- a control row moved; the leg is not the measurement "
                             "it claims to be" % (ctl, CONTROL[leg])))
        if r == EXACT[leg]:
            v = "exact"
        else:
            v = "*** PREDICTED %s GOT %s ***" % (sorted(EXACT[leg]), sorted(r))
            miss.append((leg, v))
        if EXACT[leg] and tally[0] >= ROWS:
            bad.append((leg, "*** ESCAPE %d/%d -- a floor cell repair 15 was built to carry is NOT carried ***" % tally))
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
        print("CHECK14_FAIL")
        return 1
    print("CHECK14_PASS_WITH_PREDICTION_MISSES" if miss else "CHECK14_PASS")
    return 0


sys.exit(main())
