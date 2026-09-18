#!/usr/bin/env python3
"""check_pred.py -- #530 kill table 7: score every leg MECHANICALLY against PRETABLE 7's predictions.

Written BEFORE the table runs, and its mtime says so.  That order is the whole point: #529's table 11 shipped
without one, its predictions were compared BY EYE, and a wrong per-row prediction survived the run and had to be
found by reading afterwards.  A claimed check that cannot fail is worse than no check because it reassures.

It reports a PREDICTION ERROR AS a prediction error -- it never quietly adopts whichever set it is handed.

Run: python3 check_pred.py            (from this directory; reads logs/)
"""
import io, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
LOGS = os.path.join(HERE, "logs")
ROWS = 352

#  ---- the decomposition PRETABLE 7 asserts, checked against `base' rather than assumed ----
FAMILY_SIZES = {"pit0": 37, "pit1": 37, "pit2": 37, "pitT": 39, "kbcmd": 16}
LEGACY = 185

#  ---- EXACT red-set predictions: the falsifiable ones ----
EXACT = {
    "base":   set(),
    "cdxZL3": {"stub3 z1"},
    "nox":    {"stub0 live", "stub1 live", "stub2 live", "stub3 live"},
}

#  ---- COMPONENT-SUM predictions.  (legacy, pit, kbcmd, z1); None = UNMEASURED component, low confidence. ----
#  legacy/pit are CARRIED measurements and name their logs in PRETABLE 7; kbcmd and z1 are FRESH derivations.
COMPONENTS = {
    "noff":    (0,   73,  0, 0),
    "WWtail":  (0,   16,  0, 0),
    "WW6":     (0,    4,  0, 0),
    "dNZtail": (0,    8,  0, 0),
    "RD2z":    (0,   32,  0, 0),
    "W23":     (1, None,  0, 0),      # pit component UNMEASURED; predicted 8
    "RWtail":  (2,    4,  0, 0),
    "WWall":   (16,  64,  4, 1),
    "RWall":   (18,  10,  4, 0),
    "RD2post": (24,  42,  0, 0),
    "RXW":     (42,  53,  8, 0),
    "WXR":     (45,  32,  8, 0),
    "Rdrop":   (58, None, 0, 0),      # pit component UNMEASURED; predicted 53
    "Wdrop":   (49, None, 8, 0),      # pit component UNMEASURED; predicted 64
    "Wpure":   (32,  64,  4, 1),
}
UNMEASURED_GUESS = {"W23": 8, "Rdrop": 53, "Wdrop": 64}

#  legs that are NOT mutants of the fix: a 352/352 here is not an escape of the fix's enumeration
NOT_A_FIX_MUTANT = {"noff", "nox"}


def reds(leg):
    """(the row names that FAILED, the leg's own tally, whether the log carries its completion sentinel)"""
    p = os.path.join(LOGS, "probe_%s.raw" % leg)
    if not os.path.exists(p):
        return None, None, False
    txt = io.open(p, encoding="utf-8", errors="replace").read()
    names, ctl = set(), None
    for ln in txt.split(chr(10)):
        s = ln.rstrip()
        if s.endswith("FAIL") and not s.startswith("LCAISALANE_"):
            #  #530 closing pass 6: a FIXED-WIDTH slice bleeds the next column into the name.
            #  EVERY row name in this instrument is shorter than 16 chars (max 13), so ln[:16]
            #  appended part of the `got' field to all 352 of them.  Score rows survive it -- a
            #  bled name still COUNTS -- but the two EXACT RED-SET predictions (cdxZL3, nox)
            #  could never match, and were reported as PREDICTION MISSES while being CORRECT.
            #  Split on runs of 2+ spaces: row names contain single spaces, columns are wider.
            names.add(re.split(r'\s{2,}', ln.rstrip(), 1)[0])
        m = re.match(r"LCAISALANE_RESULT=(\d+)/(\d+)", ln)
        if m:
            ctl = (int(m.group(1)), int(m.group(2)))
    #  A PRESERVED LOG IS VERIFIED BY ITS COMPLETION SENTINEL, NOT BY ITS EXISTENCE.
    return names, ctl, ("LCAISALANE_DONE" in txt)


def census(leg):
    """row-name family census, so a changed instrument is caught rather than silently scored"""
    p = os.path.join(LOGS, "probe_%s.raw" % leg)
    fam = {}
    for ln in io.open(p, encoding="utf-8", errors="replace"):
        m = re.match(r"^([a-z0-9]\S*)\s.*\s(ok|FAIL)\s*$", ln.rstrip())
        if m:
            fam[m.group(1)] = fam.get(m.group(1), 0) + 1
    return fam


def main():
    if not os.path.isdir(LOGS):
        print("no logs/ directory -- the table has not run")
        sys.exit(2)
    legs = sorted(f[6:-4] for f in os.listdir(LOGS) if f.startswith("probe_") and f.endswith(".raw"))
    bad, escapes, predmiss = [], [], []
    print("leg          score      reds  verdict")
    for leg in legs:
        r, ctl, done = reds(leg)
        if ctl is None or not done:
            bad.append((leg, "NO TALLY or NO LCAISALANE_DONE -- log truncated or absent; RE-RUN, do not read"))
            print("%-12s %-10s %4s  *** TRUNCATED ***" % (leg, "-", "-"))
            continue
        score = "%d/%d" % ctl
        if ctl[1] != ROWS:
            bad.append((leg, "denominator %d, expected %d -- the instrument is not the one PRETABLE 7 names"
                        % (ctl[1], ROWS)))
        if ctl[1] - ctl[0] != len(r):
            bad.append((leg, "tally says %d red, extraction found %d" % (ctl[1] - ctl[0], len(r))))

        v = "-"
        if leg == "base":
            fam = census(leg)
            for k, n in FAMILY_SIZES.items():
                if fam.get(k, 0) != n:
                    bad.append((leg, "family %s has %d rows, PRETABLE 7 says %d" % (k, fam.get(k, 0), n)))
            v = "OK" if ctl[0] == ROWS else "*** BASE NOT CLEAN ***"
            if ctl[0] != ROWS:
                bad.append((leg, v))
        elif leg in EXACT:
            if r == EXACT[leg]:
                v = "exact"
            else:
                v = "*** PREDICTED %s GOT %s ***" % (sorted(EXACT[leg]), sorted(r))
                predmiss.append((leg, v))
        elif leg in COMPONENTS:
            lg, pit, kb, z1 = COMPONENTS[leg]
            if pit is None:
                pit = UNMEASURED_GUESS[leg]
                tag = " (pit component was UNMEASURED -- low-confidence prediction)"
            else:
                tag = ""
            want = ROWS - (lg + pit + kb + z1)
            if ctl[0] == want:
                v = "matches the component sum %d = 352 - (%d+%d+%d+%d)%s" % (want, lg, pit, kb, z1, tag)
            else:
                v = "*** PREDICTED %d/%d, GOT %s%s ***" % (want, ROWS, score, tag)
                predmiss.append((leg, v))
        if leg not in NOT_A_FIX_MUTANT and leg != "base" and ctl[0] >= ROWS:
            escapes.append(leg)
            v = "*** ESCAPE -- 352/352 on a mutant of the fix ***"
        print("%-12s %-10s %4d  %s" % (leg, score, len(r), v))

    print("")
    print("legs scored: %d" % len(legs))
    if predmiss:
        print("PREDICTION MISSES (%d) -- the prediction was wrong, or the mutant/instrument is:" % len(predmiss))
        for leg, why in predmiss:
            print("  %-12s %s" % (leg, why))
    if escapes:
        print("*** ESCAPES (%d): %s -- CLOSING PASS 5 DOES NOT CLOSE ***" % (len(escapes), ", ".join(escapes)))
    if bad:
        print("APPARATUS DISAGREEMENTS (%d):" % len(bad))
        for leg, why in bad:
            print("  %-12s %s" % (leg, why))
    if bad or escapes:
        print("CHECK_PRED7_FAIL")
        sys.exit(1)
    if predmiss:
        print("CHECK_PRED7_PASS_WITH_PREDICTION_MISSES  (no escape, no apparatus fault)")
        sys.exit(0)
    print("every leg agrees with PRETABLE 7")
    print("CHECK_PRED7_PASS")


if __name__ == "__main__":
    main()
