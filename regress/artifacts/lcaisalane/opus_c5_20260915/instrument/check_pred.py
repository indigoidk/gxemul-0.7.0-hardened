#!/usr/bin/env python3
"""check_pred.py LOGDIR -- compare each probe_<leg>.raw's red set with PREDICT.out / PREDICT2.out (transcribed here as sets).
A leg counts only if its log ends LCAISALANE_DONE."""
import os, re, sys
L = sys.argv[1]
S = lambda *xs: set(xs)
stubw = {"stub%d w%d" % (l, n) for l in (0, 1, 2, 3) for n in (1, 2, 4, 8)}
stubr = {"stub%d r%d" % (l, n) for l in (0, 1, 2, 3) for n in (1, 2, 4, 8)}
PRED = {
    "base":    set(),
    "RD2z":    set(),
    "WWtail":  set(),
    "WWall":   stubw,
    "dNZtail": set(),
    "W23":     S("stub3 w2"),
    "RWtail":  S("tailr t6", "tailr t3"),
    "nox":     S("stub0 live", "stub1 live", "stub2 live", "stub3 live"),
    "WW6":     set(),
    "RD2post": {"rdq r%d" % n for n in (1, 2, 4, 8)} | stubr | {"tailq r t%d" % t for t in (7, 6, 5, 3)},
    "cdxZL3":  set(),
}
exact = diff = 0
for leg, want in PRED.items():
    p = os.path.join(L, "probe_%s.raw" % leg)
    if not os.path.exists(p):
        print("%-8s NOT RUN" % leg); continue
    t = open(p, encoding="utf-8", errors="replace").read()
    if not t.rstrip().endswith("LCAISALANE_DONE"):
        print("%-8s LOG INCOMPLETE (no LCAISALANE_DONE) -- not scored" % leg); continue
    reds = set()
    for line in t.splitlines():
        if line.endswith(" FAIL") and not line.startswith("LCAISALANE"):
            reds.add(line[:14].strip())
    res = re.search(r"LCAISALANE_RESULT=(\d+)/(\d+)", t).group(0)
    retr = re.search(r"LCAISALANE_RETRIED=(\S+)", t).group(1)
    ok = reds == want
    exact += ok; diff += (not ok)
    print("%-8s %-26s retried=%-5s %s%s" % (leg, res, retr, "EXACT" if ok else "DIFFERS",
          "" if ok else "  unexpected-red=%s missing-red=%s" % (sorted(reds - want), sorted(want - reds))))
print("CHECKPRED exact=%d differs=%d" % (exact, diff))
