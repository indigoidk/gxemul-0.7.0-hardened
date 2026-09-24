#!/usr/bin/env python3
"""#545 r3c table: compare every measured variant with PREDICTIONS.tsv (written before the run), and check that no
row a variant reddened on 862 rows went green on 864 (a LOST row is a finding, not noise)."""
import glob, io, json, os

OUT = "/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/fbd5/q2_20260923/r3c_20260923"
pred = {}
for ln in io.open(OUT + "/PREDICTIONS.tsv", encoding="utf-8").read().splitlines()[1:]:
    vid, st, on707, p, why, f707 = ln.split("\t")
    pred[vid] = dict(set=st, on707=on707, pred=p, why=why, f707=[x for x in f707.split("|") if x])
meas = {}
for f in sorted(glob.glob(OUT + "/results_w*.jsonl")):
    for ln in io.open(f, encoding="utf-8"):
        r = json.loads(ln)
        meas[r["vid"]] = r


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


rows, mism, lost, bad = [], [], [], []
for vid in sorted(pred):
    p, r = pred[vid], meas.get(vid)
    v = verdict(r)
    kill = v in ("RED", "DIED")
    ok = (p["pred"] == "RED") == kill and v not in ("MISSING", "BUILD-FAIL", "NO-ROWS", "HUNG")
    lr = []
    if v == "RED" and p["f707"]:
        lr = [x for x in p["f707"] if x not in set(r["failing"])]
    elif v != "RED" and p["f707"]:
        lr = p["f707"]
    if lr:
        lost.append((vid, lr))
    n = r["fails"] if r and r.get("fails") is not None else "-"
    rows.append("%-26s %-8s 862:%-6s pred:%-5s got:%-10s n=%-4s %s" % (
        vid, p["set"], p["on707"], p["pred"], v, n, "" if ok else "<<< MISMATCH"))
    if not ok:
        mism.append((vid, p, v, r))
    if v in ("MISSING", "BUILD-FAIL", "NO-ROWS", "HUNG"):
        bad.append((vid, v))
extra = sorted(set(meas) - set(pred))
print("#545 r3c TABLE -- %d predicted variants, %d measured, %d measured but not predicted" % (
    len(pred), len(meas), len(extra)))
for s in ("opus", "carried", "closing", "codexV"):
    vs = [v for v in pred if pred[v]["set"] == s]
    red = sum(1 for v in vs if verdict(meas.get(v)) in ("RED", "DIED"))
    print("  %-8s %3d variants: %3d killed (RED or DIED), %3d not" % (s, len(vs), red, len(vs) - red))
print("MISMATCHES against the predictions: %d" % len(mism))
for vid, p, v, r in mism:
    print("  %-26s pred %s (%s) got %s%s" % (vid, p["pred"], p["why"], v,
          (" -- first: " + r["failing"][0]) if r and r.get("failing") else ""))
print("ROWS LOST (red on 862, not red on 864): %d variants" % len(lost))
for vid, lr in lost:
    print("  %-26s %d lost: %s" % (vid, len(lr), " | ".join(lr[:4])))
print("NOT SCORED (missing / build failure / hung): %d" % len(bad))
for vid, v in bad:
    print("  %-26s %s" % (vid, v))
if extra:
    print("MEASURED BUT NOT PREDICTED: " + " ".join(extra))
print()
print("\n".join(rows))
print("ANALYZE_DONE")
