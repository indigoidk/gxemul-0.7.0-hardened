#!/usr/bin/env python3
"""compare11.py -- table 11 against PRETABLE_11.out, mechanically (run with python -B).  Reads PRETABLE_11.out (written before the table)
and table11/SCORES.txt; one line per leg/variant, MATCH or MISS with what differs, then the tallies.  Prediction kinds: `exactly`
(row-set equality; none = GREEN), `at least` (superset; `none -- predicted GREEN` = no row red), `RED within` (at least one row red
and every red row in one of the listed sessions), `RED` (at least one row red), `NOT PREDICTED` (reported, never a miss).  The HEAD
red set and the null scores are re-derived from qhs_variants_11.py, which wrote them."""
import importlib.util
import io
import os
import re
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("q11", os.path.join(HERE, "qhs_variants_11.py"))
q11 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(q11)


def session_of(row):
    best = None
    for s in q11.SESSIONS:
        if row.startswith(s + "_") and (best is None or len(s) > len(best)):
            best = s
    return best


pred = {}
for line in io.open(os.path.join(HERE, "PRETABLE_11.out"), encoding="utf-8"):
    m = re.match(r"^   (\S+)\s+(exactly|at least|RED within|RED|NOT PREDICTED)(:?)\s*(.*)$", line.rstrip("\n"))
    if not m:
        continue
    name, kind, rest = m.group(1), m.group(2), m.group(4)
    tok = rest.split()[0] if rest.split() else ""
    items = [] if tok in ("none", "") or kind in ("RED", "NOT PREDICTED") else tok.split(",")
    pred[name] = (kind, items, "GREEN" in rest.split("(")[0])

sc = {}
for line in io.open(os.path.join(HERE, "table11", "SCORES.txt"), encoding="utf-8"):
    p = line.split()
    if len(p) < 4:
        continue
    red = line.rsplit("RED=", 1)[1].strip() if "RED=" in line else None
    sc[p[0]] = {"score": p[3], "line": line.rstrip("\n"),
                "red": (None if red is None else ([] if red == "none" else red.split(","))),
                "control": (re.search(r"CONTROL=(\S+)", line) or [None, None])[1],
                "symptom": (re.search(r"SYMPTOM=(\S+)", line) or [None, None])[1], "done": "PPC_IFETCH_PROBE_DONE" in line}

out, miss = [], 0
m10 = q11.scores10()
legs = [("base", "177/177", "OK", "ABSENT", []), ("HEAD", "76/177", "OK", "PRESENT", m10["HEAD"] + q11.HEAD_NEW_RED),
        ("null_true", "70/177", "FAIL", "ABSENT", None), ("null_absent", "48/177", "FAIL", "ABSENT", None),
        ("null_false", "49/177", "FAIL", "ABSENT", None)]
for name, score, ctl, sym, red in legs:
    s = sc.get(name)
    if not s:
        out.append("MISS  %-14s no SCORES line" % name); miss += 1; continue
    ok = s["score"] == score and s["control"] == ctl and s["symptom"] == sym and s["done"]
    eq = red is None or (s["red"] is not None and set(s["red"]) == set(red))
    out.append("%s  %-14s %s CONTROL=%s SYMPTOM=%s (predicted %s CONTROL=%s SYMPTOM=%s%s)" % (
        "MATCH" if ok and eq else "MISS ", name, s["score"], s["control"], s["symptom"], score, ctl, sym,
        "" if red is None else ", red set %s" % ("equal" if eq else "DIFFERS: extra=%s missing=%s" % (
            ",".join(sorted(set(s["red"] or []) - set(red))) or "-", ",".join(sorted(set(red) - set(s["red"] or []))) or "-"))))
    miss += 0 if ok and eq else 1

tally = {"exact": 0, "atleast": 0, "green_pred": 0, "builddep": 0, "within": 0, "notpred": 0}
reds, greens = [], []
for name, _ in q11.V:
    s = sc.get(name)
    kind, items, green = pred[name]
    if not s or s["red"] is None:
        out.append("MISS  %-14s no usable SCORES line (%s)" % (name, s["line"] if s else "absent")); miss += 1; continue
    got = set(s["red"])
    (reds if got else greens).append(name)
    if kind == "exactly":
        ok = got == set(items)
        tally["exact"] += ok
        detail = "" if ok else " extra=%s missing=%s" % (",".join(sorted(got - set(items))) or "-", ",".join(sorted(set(items) - got)) or "-")
    elif kind == "at least" and green:
        ok = not got
        tally["green_pred"] += ok
        detail = "" if ok else " red=%s" % ",".join(s["red"])
    elif kind == "at least":
        ok = set(items) <= got
        tally["atleast"] += ok
        extra = sorted(got - set(items))
        detail = (" +%d beyond its table-10 set (%s)" % (len(extra), ",".join(extra)) if extra else "") if ok else \
            " missing=%s" % ",".join(sorted(set(items) - got))
    elif kind == "RED within":
        outside = sorted(r for r in got if session_of(r) not in items)
        ok = bool(got) and not outside
        tally["within"] += ok
        sess = sorted(set(session_of(r) for r in got))
        detail = " (%d rows in %s)" % (len(got), ",".join(sess)) + ("" if not outside else " OUTSIDE=%s" % ",".join(outside)) + \
            ("" if got else " NO ROW RED")
    elif kind == "RED":
        ok = bool(got)
        tally["builddep"] += ok
        detail = " (%d rows)" % len(got)
    else:
        ok = True
        tally["notpred"] += 1
        detail = " (outcome, not a prediction: %s)" % ("%d rows red" % len(got) if got else "GREEN")
    out.append("%s  %-14s %-8s %-13s%s" % ("MATCH" if ok else "MISS ", name, s["score"], "GREEN" if green else kind, detail))
    miss += 0 if ok else 1

print("\n".join(out))
print("TALLY: %d variants; red %d, green %d (%s)" % (len(q11.V), len(reds), len(greens), ",".join(greens)))
print("TALLY: exact %d/5, at-least held %d, predicted-green held %d, build-dependent red %d/4, red-within held %d/4, not predicted %d" % (
    tally["exact"], tally["atleast"], tally["green_pred"], tally["builddep"], tally["within"], tally["notpred"]))
print("COMPARE11_MISSES=%d" % miss)
print("COMPARE11_DONE")
