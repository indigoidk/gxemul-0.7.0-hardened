#!/usr/bin/env python3
"""check_pred8.py -- score the closing-pass-8 kill tables against PREDICT.md / PREDICT2.md MECHANICALLY.

The predictions are TRANSCRIBED here from those two files, which were written before any build (their mtimes prove
the order).  This script reads the lane outputs and says, per mutant, whether the OUTCOME class matched and whether
the named row actually reddened.  A prediction error is reported as a prediction error, never smoothed away.

Sentinel: CHECKPRED8_DONE.
"""
import os
import re
import sys

A = "/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/opus_close8_20260916"

#  (outcome, rows I named).  outcome: "CLEAN" = predicted 188/188, "KILL" = predicted < 188.
PRED = {
    "base":            ("CLEAN", []),
    "L_dfl4w_hi":      ("KILL",  ["p acc 40 sw", "p acc 40 lw", "top4 w"]),
    "L_dfl4w_lo":      ("KILL",  ["p dog wlo", "p dog whi"]),
    "L_dfl4r_hi":      ("KILL",  ["top4 rhi", "p acc 40 lw"]),
    "L_dfl4r_lo":      ("KILL",  ["top4 rlo", "p rev lw4", "p dog rlo"]),
    "W_rev8r_out":     ("KILL",  ["p rev ld"]),
    "W_rev8w_out":     ("CLEAN", []),
    "W_rev4w_out":     ("CLEAN", []),
    "W_rev4r_out":     ("CLEAN", []),
    "G_lane_ist":      ("CLEAN", []),
    "G_lane_tim":      ("CLEAN", []),
    "G_lane_all":      ("KILL",  ["p dog rhi", "top4 rhi", "p acc 40 lw", "p rev lw4"]),
    "D1_landpost":     ("KILL",  ["sh keeps", "lo keeps", "hi keeps", "mid keeps", "imask keeps"]),
    "D2_remappost":    ("KILL",  ["top8 st+ld", "p rev ld", "p acc ctl ld"]),
    #  PREDICT2.md, the supplementary table
    "C_ctl4r":            ("CLEAN", []),
    "G_lane_ctl":         ("CLEAN", []),
    "G_glm_tim4clear":    ("CLEAN", []),
    "G_clr_ist4r":        ("CLEAN", []),
    "G_clr_ctl4r":        ("CLEAN", []),
    "G_clr_imk4r":        ("KILL",  ["gate line", "gate run"]),
    "K_ctl4w_reset_post": ("CLEAN", []),
    "K_ctl8w_reset_post": ("CLEAN", []),
}

lines = []
for d, pats in ((A + "/logs", ("lane0.out", "lane1.out", "lane2.out", "lane3.out")),
                (A + "/logs2", ("p188_a.out", "p188_b.out", "p188_c.out", "p188_d.out"))):
    for f in pats:
        p = os.path.join(d, f)
        if os.path.exists(p):
            lines += [ln.rstrip("\n") for ln in open(p) if ln.strip()]

print("%-22s %-10s %-9s %-9s %s" % ("mutant", "score", "predicted", "outcome", "rows"))
nmatch = nmiss = 0
seen = set()
for ln in lines:
    m = re.match(r"^(\S+) CRIMEP_RESULT=(\d+)/(\d+) CRIMEP_CONTROL=(\S+) done=(\d+) FAILING:(.*)$", ln)
    if not m:
        print("UNPARSED: %s" % ln)
        continue
    name, got, tot, ctl, done, failing = m.group(1), int(m.group(2)), int(m.group(3)), m.group(4), m.group(5), m.group(6)
    seen.add(name)
    rows = [r.strip() for r in failing.split(",") if r.strip()]
    outcome = "CLEAN" if got == tot else "KILL"
    pred, want_rows = PRED.get(name, ("?", []))
    ok = (outcome == pred)
    nmatch += ok
    nmiss += (not ok)
    missed = [r for r in want_rows if r not in rows]
    extra = [r for r in rows if r not in want_rows]
    note = ""
    if outcome == "KILL":
        if missed:
            note += " ROWS I NAMED THAT DID NOT RED: %s." % ", ".join(missed)
        if extra:
            note += " ALSO RED: %s." % ", ".join(extra)
    if done != "1":
        note += " *** SENTINEL COUNT %s -- the leg did not end cleanly ***" % done
    print("%-22s %-10s %-9s %-9s %s%s" % (name, "%d/%d" % (got, tot), pred, outcome,
                                          "MATCH" if ok else "*** PREDICTION WRONG ***", note))
    if ctl != "OK":
        print("%-22s   CRIMEP_CONTROL=%s -- check the raw log for `unclean'/`absent' before calling it attributable"
              % ("", ctl))
for name in PRED:
    if name not in seen:
        print("%-22s %-10s %-9s %-9s NOT RUN" % (name, "-", PRED[name][0], "-"))
print("")
print("PREDICTIONS MATCHED %d, WRONG %d" % (nmatch, nmiss))
print("CHECKPRED8_DONE")
