#!/usr/bin/env python3
"""D4: per-variant failing-row sets, 3c (8309c5b7) vs 3d (6c92d7e5), from the main loop's own results files
(r3c_20260923/results_w*.jsonl = 3c table; r3d_20260923/results_r3c_w*.jsonl = the 6 new shapes on 3c;
q2f/opus/results_all.jsonl = my 22 q2f shapes on 3c) and r3d_20260923/results_r3d_w*.jsonl (739 on 3d).
Renamed rows are normalised to their 3d names.  Reports every variant whose failing set changed, and attributes
each added row to the 3d edit that touches it (E1 E2 E3 E4 E5)."""
import glob, io, json, re, collections
A = "/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/fbd5/q2_20260923"
Q2F = "/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2f/opus/results_all.jsonl"
import os
if not os.path.exists(A):
    A = "C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/fbd5/q2_20260923"
    Q2F = "C:/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2f/opus/results_all.jsonl"

def load(paths, key="vid"):
    out = {}
    for p in paths:
        for l in io.open(p, encoding="utf-8"):
            if l.strip():
                r = json.loads(l)
                out[r[key]] = r
    return out

def norm(n):
    return re.sub(r"^(X14 line 4 raised by a device: Clear (?:0x10 clears it|0x400 keeps it)), CPU line",
                  r"\1, the raw status kept, CPU line", n)

r3c = load(sorted(glob.glob(A + "/r3c_20260923/results_w*.jsonl")))
r3c_new = load(sorted(glob.glob(A + "/r3d_20260923/results_r3c_w*.jsonl")))
q2f = load([Q2F])
r3d = load(sorted(glob.glob(A + "/r3d_20260923/results_r3d_w*.jsonl")))
# q2f ids are the bare P_*/FS*/MC*/TX01; the main loop carried them as OQ_<id>
q2f = {("OQ_" + k): v for k, v in q2f.items()}
before = {}
before.update(r3c); before.update(r3c_new); before.update(q2f)
print("3c records: r3c table %d, new-on-3c %d, q2f %d -> %d distinct" % (len(r3c), len(r3c_new), len(q2f), len(before)))
print("3d records: %d" % len(r3d))
missing = sorted(set(r3d) - set(before))
print("3d variants with no 3c record: %d %s" % (len(missing), missing[:10]))

E = {"E1": re.compile(r"Clear 0x20 keeps 0x10 pending"), "E2": re.compile(r"IRQ_STATUS reads 0x10$"),
     "E3": re.compile(r"line 4 raised by a device: Clear (0x10|0x400)"),
     "E4": re.compile(r"5 declines, then the legal reads and a Clear re-arm no latch"),
     "E5": re.compile(r"^X1[23] IRQ Clear write (0x70|all-ones) len [12] ")}

def st(r):
    if r.get("build") not in ("ok",):
        return "BUILD:" + str(r.get("build"))
    if r.get("rc") == "TIMEOUT" or r.get("verdict") == "TIMEOUT":
        return "TIMEOUT"
    if r.get("rows") is None:
        return "DIED"
    return "RED" if r.get("fails") else "GREEN"

changed = []
stat = collections.Counter()
lost_total = 0
for v in sorted(r3d):
    if v not in before:
        continue
    b, a = before[v], r3d[v]
    sb, sa = st(b), st(a)
    fb = set(norm(x) for x in b.get("failing", []))
    fa = set(a.get("failing", []))
    add, lost = fa - fb, fb - fa
    stat[(sb, sa)] += 1
    if add or lost or sb != sa:
        attrib = collections.Counter()
        for x in add:
            hit = [k for k, p in E.items() if p.search(x)]
            attrib[",".join(hit) or "OTHER"] += 1
        changed.append((v, sb, sa, len(fb), len(fa), sorted(add), sorted(lost), dict(attrib)))
        lost_total += len(lost)
print("state transitions 3c->3d:", dict(stat))
print("variants whose failing set changed: %d; rows lost in total: %d" % (len(changed), lost_total))
for v, sb, sa, nb, na, add, lost, at in changed:
    print("  %-22s %s(%d) -> %s(%d)  +%d %s  -%d" % (v, sb, nb, sa, na, len(add), at, len(lost)))
    for x in add:
        print("        + " + x)
    for x in lost:
        print("        - " + x)
