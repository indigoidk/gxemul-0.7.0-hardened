#!/usr/bin/env python3
"""Classify every GREEN variant from its in-process differential (wit/<vid>.txt).
REACHABLE = start "reset" (exhaustive to length 3 over 200 ops incl. device lines 4/10/11/18, plus 2M random
sequences of length 4..6).  Classes, strongest first:
  GUEST     a reachable sequence changes a read value, a return, or the CPU irq line LEVEL
  HOST      reachable, only the announce channel differs (missed / phantom / misattributed complaint)
  CALLS     reachable, only redundant ASSERT/DEASSERT call counts differ (line level identical)
  INTERNAL  reachable, only internal fields differ at the end, nothing observable within the search
  NONE      no divergence of any kind from reset within the search (equivalent to the search depth)
The harness starts (seeded, wide) are reported separately: they are NOT reachable (fiq_status != 0)."""
import csv, re, os, sys
O = "C:/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2r/opus"
res = {}
for fn in ("results.tsv", "results_dom.tsv"):
    p = O + "/" + fn
    if os.path.exists(p):
        for r in csv.DictReader(open(p, encoding="utf-8"), delimiter="\t"):
            res[r["vid"]] = r


def parse(path):
    t = open(path, encoding="utf-8").read()
    d = {"text": t}
    m = re.search(r"START reset .*?guest-visible (\d+), announce (\d+), internal (\d+), irq-call-count-only (\d+)", t)
    d["reset"] = tuple(map(int, m.groups())) if m else None
    m = re.search(r"RANDOM reset .*?guest-visible (\d+), announce (\d+), internal (\d+), irq-call-count-only (\d+)", t)
    d["random"] = tuple(map(int, m.groups())) if m else None
    for st in ("seeded", "wide"):
        m = re.search(r"START " + st + r" .*?guest-visible (\d+), announce (\d+), internal (\d+), irq-call-count-only (\d+)", t)
        d[st] = tuple(map(int, m.groups())) if m else None
    # shortest sequences, by kind, from the reset block
    blocks = re.split(r"(?m)^(?=START |RANDOM )", t)
    d["seq"] = {}
    for b in blocks:
        if b.startswith("START reset") or b.startswith("RANDOM reset"):
            for m in re.finditer(r"shortest (?:random )?(GUEST-VISIBLE|ANNOUNCE|IRQ-CALL-COUNT-ONLY|INTERNAL-ONLY) divergence "
                                 r"\(start reset, (\d+) steps?\): (.*)", b):
                kind, n, ops = m.group(1), int(m.group(2)), m.group(3).strip()
                if kind not in d["seq"] or n < d["seq"][kind][0]:
                    d["seq"][kind] = (n, ops)
    d["complete"] = "WIT_DONE" in t
    return d


out = []
rows = []
for fn in sorted(os.listdir(O + "/wit")):
    vid = fn[:-4]
    d = parse(O + "/wit/" + fn)
    if not d["complete"] or d["reset"] is None or d["random"] is None:
        rows.append((vid, "INCOMPLETE", "", ""))
        continue
    g = d["reset"][0] + d["random"][0]
    a = d["reset"][1] + d["random"][1]
    i = d["reset"][2] + d["random"][2]
    c = d["reset"][3] + d["random"][3]
    cls = "GUEST" if g else "HOST" if a else "CALLS" if c else "INTERNAL" if i else "NONE"
    kind = {"GUEST": "GUEST-VISIBLE", "HOST": "ANNOUNCE", "CALLS": "IRQ-CALL-COUNT-ONLY", "INTERNAL": "INTERNAL-ONLY"}.get(cls)
    seq = d["seq"].get(kind) if kind else None
    also = ""
    if cls == "GUEST" and "ANNOUNCE" in d["seq"]:
        also = "announce also differs (shortest %d: %s)" % d["seq"]["ANNOUNCE"]
    harness = "seeded g/a/i/c=%s wide g/a/i/c=%s" % ("/".join(map(str, d["seeded"])), "/".join(map(str, d["wide"])))
    rows.append((vid, cls, ("%d steps: %s" % seq) if seq else "-", also + ("; " if also else "") + harness))
with open(O + "/classify.txt", "w", encoding="utf-8") as f:
    f.write("vid\tclass(reachable)\tshortest reachable witness\tnotes\n")
    for r in rows:
        f.write("\t".join(r) + "\n")
counts = {}
for r in rows:
    counts[r[1]] = counts.get(r[1], 0) + 1
print(counts)
for r in rows:
    print("%-26s %-9s %s" % (r[0], r[1], r[2][:150]))
