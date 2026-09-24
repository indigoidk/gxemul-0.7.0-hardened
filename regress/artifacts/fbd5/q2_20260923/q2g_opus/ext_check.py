#!/usr/bin/env python3
"""Mechanical check of ext_results.jsonl against PREDICTIONS_ext.txt (the W rows predicted red per variant) and against
results_all.jsonl (each variant's 864-row failures must be unchanged on the extension: it only adds rows)."""
import io, json, re, os
D = os.path.dirname(os.path.abspath(__file__))
pred = {}
for l in io.open(os.path.join(D, "PREDICTIONS_ext.txt"), encoding="utf-8"):
    m = re.match(r"^([A-Z]+\d+b?)\s+(W\d|none)\b", l)
    if m:
        pred[m.group(1)] = set() if m.group(2) == "none" else {m.group(2)}
ext = {json.loads(l)["vid"]: json.loads(l) for l in io.open(os.path.join(D, "ext_results.jsonl"), encoding="utf-8") if l.strip()}
tab = {json.loads(l)["vid"]: json.loads(l) for l in io.open(os.path.join(D, "results_all.jsonl"), encoding="utf-8") if l.strip()}
bad = 0
for v in sorted(pred):
    e = ext.get(v)
    got = {z.split()[0] for z in (e.get("z_failing") or [])} if e else None
    same864 = e is not None and sorted(e.get("other_failing") or []) == sorted(tab[v].get("failing") or [])
    ok = got == pred[v] and same864
    bad += not ok
    print("%-6s pred %-6s got %-6s 864-row failures unchanged: %s  %s" % (v, ",".join(sorted(pred[v])) or "none",
          ",".join(sorted(got)) if got is not None else "MISSING", same864, "ok" if ok else "MISMATCH"))
print("variants %d, mismatches %d" % (len(pred), bad))
