#!/usr/bin/env python3
"""check_pred.py -- #529 kill table 12 (repair 14): score every leg MECHANICALLY against PRETABLE 12.

*** WRITTEN BEFORE THE TABLE RUNS, AND THAT ORDER IS THE POINT. ***  Kill table 11 shipped WITHOUT one --
its PRETABLE claimed a checker that did not exist -- so its predictions were compared BY EYE, and that is
how its K2 prediction error survived the run and had to be found by reading afterwards.  A claimed check
that cannot fail is worse than no check, because it reassures.

IT REPORTS A PREDICTION ERROR AS A PREDICTION ERROR.  It never adopts whichever set it is handed.

*** AND IT DISTINGUISHES A **DISCLOSED** ESCAPE FROM A BREACH, WHICH IS THE WHOLE REASON CLAUSE (e)
EXISTS. ***  M3_timelatch and M5_revlatch are PREDICTED to escape: their carriers are deliberately not in
this diff, the probe's contract says so, and the flagship ruling scoped repair 14 to the accept side.  An
escape that was named in advance is `outside the contract, as stated'.  An UNPREDICTED 204/204 on a mutant
of the fix is a breach and fails this checker.

Run: python3 check_pred.py   (from this directory; reads logs/)
"""
import io, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
LOGS = os.path.join(HERE, "logs")
ROWS = 204          # 188 shipped + 16 added by repair 14.  The base leg CONFIRMS this; it is not assumed.

#  EXACT red sets -- the falsifiable predictions, transcribed from PRETABLE 12 before any build.
EXACT = {
    "base":               set(),
    "G_glm_tim4clear":    {"c t4w gap", "c t4r gap"},
    "G_clr_ist4r":        {"acc istat lw"},
    "G_lane_ctl":         {"acc ctl4r", "acc ctl0c", "p acc ctl4r", "p acc ctl0c"},
    "K_ctl4w_reset_post": {"rst 4w"},
    "K_ctl8w_reset_post": {"rst 8w"},
    "M2_ld278clr":        {"top8 clear"},
    "W_ctl8w":            {"p acc ctl msg", "rst 8w"},
    "G_clr_ctl4r":        set(),      # the EQUIVALENT cell -- predicted clean, and that is a claim
}

#  Legs that must stay KILLED but whose exact row set is not predicted here (they were measured against the
#  188-row instrument; repair 14 may add rows they also move, which is not an error).
MUST_STAY_KILLED = {"G_clr_imk4r", "M4_timeplain", "M6_istlatch", "M1_gotolatch"}

#  *** PREDICTED, DISCLOSED ESCAPES.  Named in advance; NOT failures. ***
DISCLOSED_ESCAPES = {
    "M3_timelatch": "the decline-suppression face at CRIME_TIME -- carrier deliberately not in this diff",
    "M5_revlatch":  "the same at CRIME_REV -- ditto; both are named in the probe contract",
}


def reds(leg):
    p = os.path.join(LOGS, "probe_%s.raw" % leg)
    if not os.path.exists(p):
        return None, None, False
    txt = io.open(p, encoding="utf-8", errors="replace").read()
    names, ctl = set(), None
    for ln in txt.split(chr(10)):
        s = ln.rstrip()
        #  ANCHORED: only a ROW line ends in FAIL.  An unanchored match also catches summary tokens such as
        #  CRIMEP_CONTROL=FAIL, which is the phantom-count trap this project already records.
        if s.endswith("FAIL") and not s.startswith("CRIMEP_"):
            names.add(ln[:15].strip())
        m = re.match(r"CRIMEP_RESULT=(\d+)/(\d+)", ln)
        if m:
            ctl = (int(m.group(1)), int(m.group(2)))
    return names, ctl, ("CRIMEP_DONE" in txt)


def main():
    if not os.path.isdir(LOGS):
        print("no logs/ -- the table has not run")
        return 2
    legs = sorted(f[6:-4] for f in os.listdir(LOGS) if f.startswith("probe_") and f.endswith(".raw"))
    bad, predmiss, disclosed = [], [], []
    print("leg                  score      reds  verdict")
    for leg in legs:
        r, ctl, done = reds(leg)
        if ctl is None or not done:
            bad.append((leg, "NO TALLY or NO CRIMEP_DONE -- truncated or absent; RE-RUN, do not read"))
            print("%-20s %-10s %4s  *** TRUNCATED ***" % (leg, "-", "-"))
            continue
        score = "%d/%d" % ctl
        if ctl[1] != ROWS:
            bad.append((leg, "denominator %d, expected %d -- the instrument is not the one PRETABLE 12 names"
                        % (ctl[1], ROWS)))
        if ctl[1] - ctl[0] != len(r):
            bad.append((leg, "tally says %d red, extraction found %d" % (ctl[1] - ctl[0], len(r))))

        if leg in DISCLOSED_ESCAPES:
            if ctl[0] == ROWS:
                v = "DISCLOSED ESCAPE, as predicted -- %s" % DISCLOSED_ESCAPES[leg]
                disclosed.append(leg)
            else:
                v = "*** PREDICTED a disclosed escape, but it was KILLED (%s) -- the contract is now WRONG " \
                    "in the safe direction; correct it ***" % score
                predmiss.append((leg, v))
        elif leg in EXACT:
            if r == EXACT[leg]:
                v = "exact"
            else:
                v = "*** PREDICTED %s GOT %s ***" % (sorted(EXACT[leg]), sorted(r))
                predmiss.append((leg, v))
            if leg != "base" and leg != "G_clr_ctl4r" and ctl[0] >= ROWS:
                bad.append((leg, "*** ESCAPE -- %d/%d on a mutant repair 14 was written to close ***"
                            % (ctl[0], ROWS)))
        elif leg in MUST_STAY_KILLED:
            if ctl[0] < ROWS:
                v = "still killed (%d red)" % len(r)
            else:
                v = "*** REGRESSION -- this leg was KILLED before repair 14 and is now clean ***"
                bad.append((leg, v))
        else:
            v = "killed" if ctl[0] < ROWS else "*** UNPREDICTED ESCAPE -- a breach, not a disclosure ***"
            if ctl[0] >= ROWS:
                bad.append((leg, v))
        print("%-20s %-10s %4d  %s" % (leg, score, len(r), v))

    print("")
    print("legs scored: %d   disclosed escapes: %d" % (len(legs), len(disclosed)))
    if predmiss:
        print("PREDICTION MISSES (%d) -- the prediction was wrong, or the mutant/instrument is:" % len(predmiss))
        for leg, why in predmiss:
            print("  %-20s %s" % (leg, why))
    if bad:
        print("FAILURES (%d):" % len(bad))
        for leg, why in bad:
            print("  %-20s %s" % (leg, why))
        print("CHECK_PRED12_FAIL")
        return 1
    if predmiss:
        print("CHECK_PRED12_PASS_WITH_PREDICTION_MISSES  (no breach, no apparatus fault)")
        return 0
    print("every leg agrees with PRETABLE 12, and the two disclosed escapes are the ones named in advance")
    print("CHECK_PRED12_PASS")
    return 0


sys.exit(main())
