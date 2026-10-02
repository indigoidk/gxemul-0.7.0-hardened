#!/usr/bin/env python3
"""check_pred.py -- #529 kill table 11: score every leg MECHANICALLY against PRETABLE 11's predictions.

*** THIS FILE WAS MISSING UNTIL 2026-09-16 20:3x AND `PRETABLE.out' LINE 82 SAID IT EXISTED. ***
Kill tables 4, 5, 6, 7, 8, 9 and 10 each shipped one; table 11 did not, and its predictions were compared BY EYE.
That is how the K2 prediction error survived the run and had to be found by reading afterwards -- and it is a claimed
check that could not fail, which this project's carrier names as worse than no check because it reassures.
Written AFTER the table by the close-8 measuring seat's finding, and it says so rather than pretending otherwise:
what it verifies is the RECORD against the LOGS, which is still worth doing and is what caught nothing new here.

Run: python check_pred.py   (from this directory)
"""
import io, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
LOGS = os.path.join(HERE, "logs")
ROWS = 188

#  PRETABLE 11's predictions, transcribed from the block that predates the run.
EXACT = {                       # leg -> the EXACT set of row names predicted red
    "K1": {"p acc imask sw"},
    "K3": {"p acc ctl ld"},
    "E2": {"p t4w gap", "p t4r gap"},
}
#  K2 is carried separately BECAUSE THE PREDICTION WAS WRONG and the record says so: PRETABLE predicted the four
#  `p revP * pc' rows; K2 sits on the `len == 4' arm, so the 8-byte sd/ld cannot reach it and only two reds are
#  possible.  Kept here as a DEMOTED prediction beside the corrected one, so the checker reproduces the finding
#  instead of quietly agreeing with whichever set it is handed.
K2_PREDICTED_WRONG = {"p revP sw pc", "p revP sd pc", "p revP ld pc", "p revP lw pc"}
K2_CORRECTED       = {"p revP sw pc", "p revP lw pc"}

EQUIVALENT = {"C_ctl4r"}        # the contract calls CONTROL 4R equivalent -> predicted 188/188


def reds(leg):
    """the row names that FAILED in this leg's raw log, and the leg's own tally"""
    p = os.path.join(LOGS, "probe_%s.raw" % leg)
    if not os.path.exists(p):
        return None, None, None
    txt = io.open(p, encoding="utf-8", errors="replace").read()
    names, ctl = set(), None
    for ln in txt.split(chr(10)):
        if ln.rstrip().endswith("FAIL") and not ln.startswith("CRIMEP_"):
            names.add(ln[:15].strip())
        m = re.match(r"CRIMEP_RESULT=(\d+)/(\d+)", ln)
        if m:
            ctl = (int(m.group(1)), int(m.group(2)))
    return names, ctl, ("CRIMEP_CONTROL=OK" in txt)


def main():
    legs = sorted(f[6:-4] for f in os.listdir(LOGS) if f.startswith("probe_") and f.endswith(".raw"))
    bad = []
    print("leg          score     reds  verdict")
    for leg in legs:
        r, ctl, ctlok = reds(leg)
        if ctl is None:
            bad.append((leg, "NO TALLY -- log truncated or absent")); continue
        score = "%d/%d" % ctl
        #  the tally and the red count must agree, or the extraction is wrong and every other line here is noise
        if ctl[1] != ROWS:
            bad.append((leg, "denominator %d, expected %d" % (ctl[1], ROWS)))
        if ctl[1] - ctl[0] != len(r):
            bad.append((leg, "tally says %d red, extraction found %d" % (ctl[1] - ctl[0], len(r))))
        v = "-"
        if leg == "base":
            v = "OK" if (ctl[0] == ROWS and ctlok) else "*** BASE NOT CLEAN ***"
            if ctl[0] != ROWS or not ctlok:
                bad.append((leg, v))
        elif leg in EXACT:
            v = "exact" if r == EXACT[leg] else "*** PREDICTED %s GOT %s ***" % (sorted(EXACT[leg]), sorted(r))
            if r != EXACT[leg]:
                bad.append((leg, v))
        elif leg == "K2":
            if r == K2_CORRECTED:
                v = "matches the CORRECTED prediction (PRETABLE's original named 4, was wrong)"
            elif r == K2_PREDICTED_WRONG:
                v = "*** matches PRETABLE's ORIGINAL prediction -- the correction is then wrong ***"
                bad.append((leg, v))
            else:
                v = "*** neither prediction: %s ***" % sorted(r)
                bad.append((leg, v))
        elif leg in EQUIVALENT:
            v = "equivalent-cell leg, 188/188 as predicted" if ctl[0] == ROWS else "*** MOVED: %s ***" % sorted(r)
            if ctl[0] != ROWS:
                bad.append((leg, v))
        else:
            v = "killed" if ctl[0] < ROWS else "*** ESCAPE -- 188/188 ***"
            if ctl[0] >= ROWS:
                bad.append((leg, v))
        print("%-12s %-9s %4d  %s" % (leg, score, len(r), v))
    print("")
    print("legs scored: %d" % len(legs))
    if bad:
        print("DISAGREEMENTS (%d):" % len(bad))
        for leg, why in bad:
            print("  %-12s %s" % (leg, why))
        print("CHECK_PRED11_FAIL")
        sys.exit(1)
    print("every leg agrees with PRETABLE 11 as corrected")
    print("CHECK_PRED11_PASS")


if __name__ == "__main__":
    main()
