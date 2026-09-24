#!/usr/bin/env python3
"""Score results_all.jsonl against PREDICTIONS_q2g.txt: per variant the measured state (RED n / GREEN / BUILD), the
prediction, and MATCH or MISMATCH (RED predicted -> RED measured; GREEN-* or EQ predicted -> GREEN measured)."""
import io, json, re, os
D = os.path.dirname(os.path.abspath(__file__))
pred = {}
for l in io.open(os.path.join(D, "PREDICTIONS_q2g.txt"), encoding="utf-8"):
    m = re.match(r"^(\S+)\s+(\S+)\s+(\S+)\s+(RED|EQ|GREEN-DISC|GREEN-REAL)\s", l)
    if m:
        pred[m.group(1)] = m.group(4)
res = [json.loads(l) for l in io.open(os.path.join(D, "results_all.jsonl"), encoding="utf-8") if l.strip()]
res.sort(key=lambda r: r["vid"])
mm = 0
for r in res:
    if r.get("build") != "ok":
        st = "BUILD:" + str(r.get("build"))
    elif r.get("rows") is None:
        st = "DIED"
    else:
        st = "RED" if r["fails"] else "GREEN"
    p = pred.get(r["vid"], "?")
    ok = (p == "RED") == (st in ("RED", "DIED")) and st.startswith(("RED", "GREEN", "DIED"))
    mm += not ok
    print("%-6s %-4s pred %-10s got %-5s n=%-3s rows=%s warn=%s %s" % (r["vid"], r["family"], p, st, r.get("fails"),
          r.get("rows"), r.get("warn"), "match" if ok else "MISMATCH"))
    for x in (r.get("failing") or [])[:6]:
        print("         FAIL " + x)
    if len(r.get("failing") or []) > 6:
        print("         ... %d more" % (len(r["failing"]) - 6))
print("variants %d, mismatches %d" % (len(res), mm))
