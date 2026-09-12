#!/bin/bash
T3=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/sgirandomcolour/killtable3_20260910
python3 - "$T3" <<'PY'
import re, sys, os, collections
T3 = sys.argv[1]
#  the probe prints "%-16s %-14s %-16s %-52s %s" -- the NAME column is 16 wide, not 18.
#  (A first cut used 18, cut into the `got' column, matched nothing, and reported
#   "killed by NOTHING" for all 59 rows while the table plainly lists reds.  The
#   contradiction was the tell.)
names = []
for ln in open(os.path.join(T3, "BASE.raw"), errors="replace"):
    s = ln.rstrip("\n")
    if s.endswith(" ok") or s.endswith(" FAIL"):
        nm = s[:16].strip()
        if nm and nm != "row":
            names.append(nm)
print("rows parsed from BASE.raw: %d  (want 59)" % len(names))
print("first 5: %s" % names[:5])
print("last 5:  %s" % names[-5:])
kills = collections.defaultdict(set)
mutants = []
for ln in open(os.path.join(T3, "SCORES3.txt"), errors="replace"):
    m = re.match(r"^(M\S+)\s+(\d+)/(\d+).*?reds=(.*)$", ln.strip())
    if not m:
        continue
    mut, reds = m.group(1), m.group(4).strip()
    mutants.append(mut)
    for r in [x.strip() for x in reds.split(",") if x.strip()]:
        kills[r].add(mut)
print("mutants scored: %d ; distinct row names appearing in reds: %d" % (len(mutants), len(kills)))
unknown = [r for r in kills if r not in names]
print("red names not matching any parsed row (should be 0): %s" % (unknown if unknown else "none"))
never = [n for n in names if not kills.get(n)]
print()
print("=== CHANNEL CHECK, EMPIRICAL FORM: rows NEVER red under any of the 26 mutants ===")
if never:
    for n in never:
        print("   %s" % n)
    print("   TOTAL %d of %d" % (len(never), len(names)))
else:
    print("   (none)")
print()
print("=== mutants whose ENTIRE red set is announce/silence rows (question 4) ===")
for mu in mutants:
    rs = [n for n in names if mu in kills.get(n, set())]
    if not rs:
        continue
    ann = [r for r in rs if ("ann" in r or "silent" in r or r in ("once", "announce text"))]
    if len(ann) == len(rs):
        print("   %-22s all %d reds are announce/silence" % (mu, len(rs)))
print()
print("=== CONTAINMENT among the per-window rows (strict subset kill sets) ===")
for a in sorted(kills):
    for b in sorted(kills):
        if a != b and kills[a] and kills[b] and kills[a] < kills[b]:
            print("   %-16s {%s}" % (a, ",".join(sorted(kills[a]))))
            print("       strict subset of %-16s {%s}" % (b, ",".join(sorted(kills[b]))))
            break
PY
