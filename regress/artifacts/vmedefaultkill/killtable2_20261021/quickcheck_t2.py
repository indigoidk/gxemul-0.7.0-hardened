#!/usr/bin/env python3
"""quickcheck_t2.py <table2 dir> [LEG...] -- per-batch check of table 2's raws against PRETABLE2_predictions.json:
measured red set vs predicted, CONTROL, elapsed, and any red row whose text names a TIMEOUT (`timeout:') -- a leg whose
ONLY reds are timeouts must be re-run alone before it is scored.  Read-only; the full report is cmp_table2.py's."""
import io, json, os, re, sys

T2 = sys.argv[1]
P = json.load(io.open(os.path.join(T2, "PRETABLE2_predictions.json"), encoding="latin-1"))
pred = {l["leg"]: l for l in P["legs"]}
legs = sys.argv[2:] or [l["leg"] for l in P["legs"]]
for L in legs:
    p = os.path.join(T2, "legs", L + ".raw")
    if not os.path.exists(p):
        print("%-17s (no raw yet)" % L)
        continue
    t = io.open(p, encoding="latin-1").read().rstrip("\n").split("\n")
    if t[-1] == "KT568_BUILD_FAILED_RECORDED":
        print("%-17s BUILD FAILED  predicted: %s" % (L, "BUILD_FAILS" if pred[L]["red"] == "BUILD_FAILS" else pred[L]["red"]))
        continue
    if t[-1] != "VME_DEFAULT_PROBE_DONE":
        print("%-17s INCOMPLETE (last line %r)" % (L, t[-1]))
        continue
    g = lambda k: next((x.split("=", 1)[1] for x in t if x.startswith(k + "=")), "")
    red = set(g("VME_DEFAULT_RED").split(",")) - {""}
    tmo = [x[:16].strip() for x in t if x.rstrip().endswith(" FAIL") and "timeout:" in x]
    pr = pred[L]["red"]
    pr = set(pr) if isinstance(pr, list) else pr
    if pr == "BUILD_FAILS":
        v = "MISS (predicted a build failure; it built)"
    else:
        miss, extra = pr - red, red - pr
        v = "MATCH" if not miss and not extra else "MISS predicted-green:%s unpredicted-red:%s" % (sorted(miss), sorted(extra))
    ctl = g("VME_DEFAULT_CONTROL")
    if ctl != pred[L]["control"]:
        v += " CONTROL=%s(pred %s)" % (ctl, pred[L]["control"])
    print("%-17s %s CONTROL=%s %s  red=%d  %s%s" % (L, g("VME_DEFAULT_RESULT"), ctl, g("VME_DEFAULT_ELAPSED"), len(red), v,
                                                   ("  TIMEOUT-ROWS:%s" % tmo) if tmo else ""))
