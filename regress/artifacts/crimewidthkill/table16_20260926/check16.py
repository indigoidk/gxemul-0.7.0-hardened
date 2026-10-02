#!/usr/bin/env python3
"""check16.py -- #529 table 16 (repair 16): score each leg MECHANICALLY against PRETABLE16.out's exact sets.  Written
BEFORE the table runs.  The shape is check14.py's: anchored row extraction, tally cross-check, pinned denominator,
predicted CONTROL verdict per leg, and a log without its CRIMEP_DONE sentinel refused rather than read.

Two kinds of leg, scored differently:
  * a leg PREDICTED TO RED rows: an escape (222/222) is a FAILURE -- the rows it was built for do not carry it;
  * a leg PREDICTED TO ESCAPE (the disclosed clause-(e) cells, measured for the adjudicators): a red is a PREDICTION
    MISS, reported with the rows -- it would mean the cell was carried after all.
Run: python3 check16.py   (reads logs/ beside this file)
"""
import io, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
LOGS = os.path.join(HERE, "logs")
ROWS = 226
TL = {"tl lb", "tl sb", "tl lh", "tl sh"}
RL = {"rl lb pc", "rl lh pc", "rl sb pc", "rl sh pc"}
M1_T12 = {"sb08 msg", "sh08b run", "imask sb", "imask lh", "imask sh", "istat sb", "istat lh", "istat sh",
          "gate run", "mid nodflt"}
EXACT = {
    "base":               set(),
    "G_glm_tim4clear":    {"c t4w gap", "c t4r gap"},
    "G_clr_ist4r":        {"acc istat lw"},
    "G_clr_ctl4r":        set(),
    "G_clr_imk4r":        {"gate line"},
    "G_lane_ctl":         {"p acc ctl4r"},
    "K_ctl4w_reset_post": {"rst 4w"},
    "K_ctl8w_reset_post": {"rst 8w"},
    "M1_gotolatch":       M1_T12 | TL | RL,
    "M2_ld278clr":        {"top8 clear"},
    "M3_timelatch":       set(TL),
    "M4_timeplain":       {"time lb", "time sb", "time lh", "time sh"} | TL,
    "M5_revlatch":        set(RL),
    "M6_istlatch":        {"istat sb", "istat lh", "istat sh"},
    "W_ctl8w":            {"p acc ctl msg", "rst 8w", "rearm ctl msg"},
    "M7_intmasklatch":    {"imask sb", "imask lh", "imask sh"},
    "M8_ctllatch":        {"sb08 msg", "sh08b run", "gate run"},
    "D_nodogclear":       {"ctldog sw msg", "ctldog sd msg", "rearm ctl msg", "latch ctl msg"},
    "H_noresetclear":     {"ctlrst sw msg", "ctlrst sd msg", "rst 4w msg", "rst 8w msg"},
    "S_rst8clr":          {"ctlrst sd halt"},
    "E_noendianclear":    {"rearm ctl msg", "latch ctl msg"},
    "W_istlb":            set(),
    "W_imklb":            set(),
    "L_dogclr":           {"rearm ctl msg"},
    "L_rstclr":           {"rst 4w msg", "rst 8w msg"},
}
ESCAPE_EXPECTED = {"base", "G_clr_ctl4r", "W_istlb", "W_imklb"}
CONTROL = dict((leg, "OK") for leg in EXACT)
CONTROL["G_clr_imk4r"] = "FAIL"          # `gate line' is in the CRIMEP_CONTROL set
ORDER = ("base", "G_glm_tim4clear", "G_clr_ist4r", "G_clr_ctl4r", "G_clr_imk4r", "G_lane_ctl", "K_ctl4w_reset_post",
         "K_ctl8w_reset_post", "M1_gotolatch", "M2_ld278clr", "M3_timelatch", "M4_timeplain", "M5_revlatch",
         "M6_istlatch", "W_ctl8w", "M7_intmasklatch", "M8_ctllatch", "D_nodogclear", "H_noresetclear", "S_rst8clr",
         "E_noendianclear", "W_istlb", "W_imklb", "L_dogclr", "L_rstclr")
assert sorted(ORDER) == sorted(EXACT), "ORDER and EXACT disagree"
assert all((not EXACT[l]) == (l in ESCAPE_EXPECTED) for l in ORDER), "ESCAPE_EXPECTED disagrees with EXACT"


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
            bad.append((leg, "CRIMEP_CONTROL=%s, predicted %s" % (ctl, CONTROL[leg])))
        if r == EXACT[leg]:
            v = "exact" + (" (escape, as predicted)" if leg in ESCAPE_EXPECTED and leg != "base" else "")
        else:
            v = "*** PREDICTED %s GOT %s ***" % (sorted(EXACT[leg]), sorted(r))
            miss.append((leg, v))
        if EXACT[leg] and tally[0] >= ROWS:
            bad.append((leg, "*** ESCAPE %d/%d -- the rows built for this cell do not carry it ***" % tally))
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
        print("CHECK16_FAIL")
        return 1
    print("CHECK16_PASS_WITH_PREDICTION_MISSES" if miss else "CHECK16_PASS")
    return 0


sys.exit(main())
