#!/usr/bin/env python3
"""#545 r3d table: every measured variant against PREDICTIONS.tsv (written before the run); a row a variant
reddened on r3c that is not red on r3d is LOST (a finding, not noise); the new shapes on both instruments."""
import glob, io, json, os

OUT = "/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/fbd5/q2_20260923/r3d_20260923"
pred = {}
for ln in io.open(OUT + "/PREDICTIONS.tsv", encoding="utf-8").read().splitlines()[1:]:
    vid, st, ib, before, p, n, why, fb = ln.split("\t")
    pred[vid] = dict(set=st, before=before, pred=p, n=n, why=why, fb=[x for x in fb.split("|") if x])


def load(tag):
    m = {}
    for f in sorted(glob.glob(OUT + "/results_%s_w*.jsonl" % tag)):
        for ln in io.open(f, encoding="utf-8"):
            r = json.loads(ln)
            m[r["vid"]] = r
    return m


def verdict(r):
    if r is None:
        return "MISSING"
    if r["build"] != "ok":
        return "BUILD-FAIL"
    if r["rc"] == "TIMEOUT":
        return "HUNG"
    if r["rows"] is None:
        return "DIED" if r["rc"] != 0 else "NO-ROWS"
    return "RED" if r["fails"] else "GREEN"


d, c = load("r3d"), load("r3c")
rows, mism, lost, bad = [], [], [], []
for vid in sorted(pred):
    p, r = pred[vid], d.get(vid)
    v = verdict(r)
    kill = v in ("RED", "DIED")
    ok = (p["pred"] in ("RED", "DIED")) == kill and v not in ("MISSING", "BUILD-FAIL", "NO-ROWS", "HUNG")
    n = r["fails"] if r and r.get("fails") is not None else "-"
    if ok and p["n"] != "-" and str(n) != p["n"]:
        ok = False
    lr = [x for x in p["fb"] if v != "RED" or x not in set(r["failing"])]
    if lr:
        lost.append((vid, lr))
    extra = ""
    if vid in c:
        rc = c[vid]
        extra = "  | on r3c: %s n=%s (pred %s)" % (verdict(rc), rc.get("fails", "-"), p["before"])
        pb = p["before"].split("/")
        if verdict(rc) != pb[0] or (len(pb) > 1 and str(rc.get("fails")) != pb[1]):
            ok = False
    rows.append("%-24s %-8s before:%-8s pred:%-5s n=%-3s got:%-10s n=%-4s%s %s" % (
        vid, p["set"], p["before"], p["pred"], p["n"], v, n, extra, "" if ok else "<<< MISMATCH"))
    if not ok:
        mism.append((vid, p, v, r))
    if v in ("MISSING", "BUILD-FAIL", "NO-ROWS", "HUNG"):
        bad.append((vid, v))
ext = sorted(set(d) - set(pred))
print("#545 r3d TABLE -- %d predicted variants, %d measured on r3d, %d on r3c, %d measured but not predicted" % (
    len(pred), len(d), len(c), len(ext)))
for s in sorted(set(p["set"] for p in pred.values())):
    vs = [v for v in pred if pred[v]["set"] == s]
    red = sum(1 for v in vs if verdict(d.get(v)) in ("RED", "DIED"))
    print("  %-8s %3d variants: %3d killed on r3d (RED or DIED), %3d not" % (s, len(vs), red, len(vs) - red))
print("MISMATCHES against the predictions: %d" % len(mism))
for vid, p, v, r in mism:
    print("  %-24s pred %s n=%s (%s) got %s n=%s%s" % (vid, p["pred"], p["n"], p["why"][:70], v,
          r.get("fails") if r else "-", (" -- first: " + r["failing"][0]) if r and r.get("failing") else ""))
print("ROWS LOST (red before, not red on r3d): %d variants" % len(lost))
for vid, lr in lost:
    print("  %-24s %d lost: %s" % (vid, len(lr), " | ".join(lr[:4])))
print("NOT SCORED (missing / build failure / hung): %d" % len(bad))
for vid, v in bad:
    print("  %-24s %s" % (vid, v))
print("NEW SHAPES' FAILING ROWS ON r3d:")
for vid in sorted(v for v in pred if pred[v]["set"] == "r3dnew"):
    r = d.get(vid)
    print("  %-10s %s" % (vid, " | ".join(r["failing"]) if r and r.get("failing") else "(none)"))
if ext:
    print("MEASURED BUT NOT PREDICTED: " + " ".join(ext))
print()
print("\n".join(rows))
print("ANALYZE_DONE")
