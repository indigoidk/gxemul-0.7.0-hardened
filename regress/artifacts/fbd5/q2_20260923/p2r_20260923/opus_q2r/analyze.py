#!/usr/bin/env python3
"""Group the variant table by (family, arm): red counts, distinct first-failing rows, and for the
thin kills (<= 3 red rows) the complete list of red rows, read from each variant's own log."""
import csv, collections, re
O = "/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2r/opus"
LOGS = "/tmp/opusq2r/logs"
rows = list(csv.DictReader(open(O + "/results.tsv", encoding="utf-8"), delimiter="\t"))


def reds(vid):
    out = []
    for ln in open(LOGS + "/" + vid + ".log", encoding="utf-8"):
        if ln.startswith("  FAIL  ") and "@@SELFCHECK@@" not in ln:
            out.append(ln[8:].rstrip())
    return out


g = collections.OrderedDict()
for r in rows:
    g.setdefault((r["family"], r["arm"]), []).append(r)
with open(O + "/by_family.txt", "w", encoding="utf-8") as f:
    for (fam, arm), rs in g.items():
        green = [r for r in rs if r["failures"] == "0"]
        red = [r for r in rs if r["failures"] != "0"]
        f.write("%-12s %s  variants %2d  green %2d  red %2d\n" % (fam, arm, len(rs), len(green), len(red)))
        for r in rs:
            if r["failures"] == "0":
                f.write("     GREEN %-24s %s\n" % (r["vid"], r["variant"]))
            else:
                rr = reds(r["vid"])
                f.write("     red%4s %-24s %-60s first: %s\n" % (r["failures"], r["vid"], r["variant"][:60], rr[0]))
                if len(rr) <= 3:
                    for x in rr:
                        f.write("                  all reds: %s\n" % x)
print(open(O + "/by_family.txt", encoding="utf-8").read())
