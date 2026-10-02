#!/usr/bin/env python3
"""sum46.py -- score the 92 replays against PREDICT46 (predict46.py, written before any run).
Per spec: the probe's own result line, its FAILING rows, whether they equal the prediction exactly, the mutant's
hit evidence (every re-run session's observed [ACC46HIT count against the static prediction) and which sessions
were served from the capture by declaration.  Sentinel: SUM46_DONE."""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from predict46 import P, CONTROL_ROWS

exact = miss = absent = 0
out = []
for k in range(1, 47):
    for i, lt in enumerate(("C", "S")):
        fn = os.path.join(HERE, "runs", "k%02d%s.raw" % (k, lt))
        if not os.path.exists(fn):
            out.append("%2d %s  ABSENT" % (k, lt))
            absent += 1
            continue
        t = open(fn, encoding="latin-1").read()
        res = re.search(r"^CRIMEP_RESULT=(\d+)/(\d+)$", t, re.M)
        ctl = re.search(r"^CRIMEP_CONTROL=(\w+)$", t, re.M)
        fl = re.search(r"^FAILING: ?(.*)$", t, re.M)
        done = "REPLAY46_DONE" in t and "CRIMEP_DONE" in t
        failing = [x.strip() for x in fl.group(1).split(",") if x.strip()] if fl else None
        mism = len(re.findall(r"MISMATCH", t))
        rr = re.findall(r"^REPLAY46 S(\d+) predicted_matches=(\d+) observed_hits=(\d+)", t, re.M)
        fc = re.findall(r"^REPLAY46 S(\d+) predicted_matches=\d+ FROMCACHE", t, re.M)
        hits = sum(int(h) for _, _, h in rr)
        pred = sorted(P[k][i])
        ok = done and failing is not None and sorted(failing) == pred and mism == 0 and res is not None
        exact += ok
        miss += (not ok)
        out.append("%2d %s  %-8s %-4s %-5s hits=%-3d rerun=%-22s fromcache=%-6s %s  red={%s}%s" % (
            k, lt, "%s/%s" % res.groups() if res else "?", ctl.group(1) if ctl else "?", "done" if done else "NODONE",
            hits, ",".join("S%s" % s for s, _, _ in rr), ",".join("S%s" % s for s in fc) or "-",
            "EXACT" if ok else "DIFF", ", ".join(failing or []),
            "" if ok else "   PREDICTED={%s} mismatches=%d" % (", ".join(pred), mism)))
print("SUM46 -- 92 replays scored against PREDICT46.out (C = latch clear at the access, S = set)")
print("\n".join(out))
print("EXACT=%d DIFF=%d ABSENT=%d" % (exact, miss, absent))
print("SUM46_DONE")
