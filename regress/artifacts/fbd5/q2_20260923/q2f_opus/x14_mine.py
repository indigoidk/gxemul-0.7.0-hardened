#!/usr/bin/env python3
"""Opus seat, #545 repair-3 pass: from the MAIN LOOP's own 711 results on the 864 rows (r3_20260923/results_w*.jsonl),
for each X14 row: how many variants redden it, which redden it and NOTHING ELSE (sole kills), and which redden it with
X14 rows only.  Reads their data; runs nothing."""
import glob, io, json, re, collections
R = "/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/fbd5/q2_20260923/r3c_20260923"
rows = []
for l in io.open("/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2f/opus/baseline.log", encoding="utf-8"):
    if l.startswith("  ok    X14 "):
        rows.append(re.sub(r"\s+\d+\s*$", "", l[8:]).rstrip())
recs = []
for f in sorted(glob.glob(R + "/results_w*.jsonl")):
    for l in io.open(f, encoding="utf-8"):
        recs.append(json.loads(l))
print("variants:", len(recs), " X14 rows in the baseline:", len(rows))
by = collections.defaultdict(list)
for r in recs:
    fl = [x for x in (r.get("failing") or []) if not x.startswith("IDENTITY")]
    for x in fl:
        if x.startswith("X14 "):
            by[x].append((r["vid"], len(fl), all(y.startswith("X14 ") for y in fl)))
for row in rows:
    v = by.get(row, [])
    sole = [a for a, n, o in v if n == 1]
    only14 = [a for a, n, o in v if o and n > 1]
    print("%-3d kills  sole: %s  X14-only: %s  %s" % (len(v), ",".join(sole) or "-", ",".join(only14)[:60] or "-", row))
missing = [x for x in by if x not in rows]
print("failing X14 names not in the baseline:", missing)
