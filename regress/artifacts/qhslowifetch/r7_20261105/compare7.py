#!/usr/bin/env python3
"""compare7.py -- table 7 against PRETABLE_7.out, mechanically.  Reads PRETABLE_7.out (the predictions, written before the table) and
table7/SCORES.txt; prints one line per leg/variant: MATCH or MISS with the rows that differ, then the tallies.  The HEAD prediction
(table 6's HEAD set + the 21 new rows) and the null-medium scores are re-derived from qhs_variants_7.py, which wrote them."""
import importlib.util
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("q7", os.path.join(HERE, "qhs_variants_7.py"))
q7 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(q7)

pred = {}
for line in io.open(os.path.join(HERE, "PRETABLE_7.out"), encoding="utf-8"):
    m = re.match(r"^   (\S+)\s+(exactly|at least|RED|NOT PREDICTED)(:?)\s*(.*)$", line.rstrip("\n"))
    if not m:
        continue
    name, kind, rest = m.group(1), m.group(2), m.group(4)
    rows = []
    if kind in ("exactly", "at least"):
        tok = rest.split()[0] if rest.split() else ""
        rows = [] if tok in ("none", "") else tok.split(",")
    pred[name] = (kind, rows, "GREEN" in rest)

sc = {}
for line in io.open(os.path.join(HERE, "table7", "SCORES.txt"), encoding="utf-8"):
    p = line.split()
    if len(p) < 3:
        continue
    red = line.rsplit("RED=", 1)[1].strip() if "RED=" in line else None
    sc[p[0]] = {"score": p[3] if p[2] == "rows]" else p[2], "line": line.rstrip("\n"),
                "red": (None if red is None else ([] if red == "none" else red.split(","))),
                "control": (re.search(r"CONTROL=(\S+)", line) or [None, None])[1],
                "symptom": (re.search(r"SYMPTOM=(\S+)", line) or [None, None])[1],
                "done": "PPC_IFETCH_PROBE_DONE" in line}

out, miss = [], 0
m6 = q7.scores6()
legs = [("base", "103/103", "OK", "ABSENT", []),
        ("HEAD", "40/103", "OK", "PRESENT", m6["HEAD"] + q7.NEW_ROWS),
        ("null_true", "41/103", "FAIL", "ABSENT", None), ("null_absent", "24/103", "FAIL", "ABSENT", None),
        ("null_false", "25/103", "FAIL", "ABSENT", None)]
for name, score, ctl, sym, red in legs:
    s = sc.get(name)
    if not s:
        out.append("MISS  %-14s no SCORES line" % name); miss += 1; continue
    ok = s["score"] == score and s["control"] == ctl and s["symptom"] == sym and s["done"]
    if red is not None:
        ok = ok and s["red"] is not None and set(s["red"]) == set(red)
    out.append("%s  %-14s %s CONTROL=%s SYMPTOM=%s (predicted %s CONTROL=%s SYMPTOM=%s%s)" % (
        "MATCH" if ok else "MISS ", name, s["score"], s["control"], s["symptom"], score, ctl, sym,
        "" if red is None else ", red set %s" % ("equal" if s["red"] is not None and set(s["red"]) == set(red) else "DIFFERS")))
    miss += 0 if ok else 1

tally = {"exact": 0, "atleast": 0, "green_pred": 0, "builddep": 0, "notpred": 0}
reds, greens = [], []
for name, _ in q7.V:
    s = sc.get(name)
    kind, rows, green = pred[name]
    if not s or s["red"] is None:
        out.append("MISS  %-14s no usable SCORES line (%s)" % (name, s["line"] if s else "absent")); miss += 1; continue
    got = set(s["red"])
    (reds if got else greens).append(name)
    if kind == "exactly":
        ok = got == set(rows)
        detail = "" if ok else " extra=%s missing=%s" % (",".join(sorted(got - set(rows))) or "-", ",".join(sorted(set(rows) - got)) or "-")
        tally["exact"] += ok
    elif kind == "at least":
        if green:
            ok = not got
            tally["green_pred"] += ok
            detail = "" if ok else " red=%s" % ",".join(s["red"])
        else:
            ok = set(rows) <= got
            tally["atleast"] += ok
            extra = sorted(got - set(rows))
            detail = (" +%d beyond its table-6 set (%s)" % (len(extra), ",".join(extra)) if extra else "") if ok else \
                " missing=%s" % ",".join(sorted(set(rows) - got))
    elif kind == "RED":
        ok = bool(got)
        tally["builddep"] += ok
        detail = " (%d rows: %s)" % (len(got), ",".join(s["red"]))
    else:
        ok = True
        tally["notpred"] += 1
        detail = " (outcome, not a prediction: %s)" % (",".join(s["red"]) or "GREEN")
    out.append("%s  %-14s %-8s %-13s%s" % ("MATCH" if ok else "MISS ", name, s["score"], kind if not green else "GREEN", detail))
    miss += 0 if ok else 1

print("\n".join(out))
print("TALLY: %d variants; red %d, green %d (%s)" % (len(q7.V), len(reds), len(greens), ",".join(greens)))
print("TALLY: exact matches %d/13, at-least held %d, predicted-green held %d, build-dependent red %d/4, not predicted %d" % (
    tally["exact"], tally["atleast"], tally["green_pred"], tally["builddep"], tally["notpred"]))
print("COMPARE7_MISSES=%d" % miss)
print("COMPARE7_DONE")
