#!/usr/bin/env python3
"""p3_tables.py <sgirekills artifacts dir> -- for #564's pass-3 packet, computed from kill table 3's logs rather than
typed: per row of the repaired 68-row detector, the table-3 mutants that turned it red, with the 15 rows the repair
ADDED marked; and each row's value on the HEAD 2951694f leg.  Every log must end with its completion sentinel, or this
refuses (exit 9) instead of printing a partial table."""
import glob, io, os, sys

A = sys.argv[1]
K = os.path.join(A, "killtable3_564_20261017", "raw3")
NEW = {"src 3 b", "src 3 c", "src 3 lin b", "stip b clr", "src c clr", "stip c clr", "src b clr", "stip la clr",
       "src lb clr", "stip lb clr", "src la clr", "fill b ok", "fill c ok", "xbit primed", "xbit texts"}

def rows(path):
    t = io.open(path, encoding="utf-8", errors="replace").read()
    if not t.rstrip().endswith("MTEDECL_DONE"):
        print("REFUSE: %s has no completion sentinel" % path); sys.exit(9)
    lines = t.splitlines()
    hdr = next(l for l in lines if l.startswith("row ") and " got " in l)
    w, g = hdr.index("got") - 1, hdr.index("want")
    out = []
    for l in lines:
        s = l.rstrip()
        if l is hdr or not (s.endswith(" ok") or s.endswith(" FAIL")):
            continue
        out.append((l[:w].strip(), l[w:g].strip(), "ok" if s.endswith(" ok") else "FAIL"))
    return out

base = rows(os.path.join(K, "base.out"))
head = {n: (v, s) for n, v, s in rows(os.path.join(K, "head.out"))}
red = {n: [] for n, _, _ in base}
for p in sorted(glob.glob(os.path.join(K, "*.out"))):
    mu = os.path.basename(p)[:-4]
    if mu in ("base", "null", "head"):
        continue
    for n, _, s in rows(p):
        if s == "FAIL":
            red[n].append(mu)
print("%-16s %-4s %-22s %s" % ("row", "new", "HEAD 2951694f", "table-3 mutants that turned it red"))
for n, _, _ in base:
    hv, hs = head.get(n, ("-", "-"))
    print("%-16s %-4s %-22s %s" % (n, "NEW" if n in NEW else "", "%s %s" % (hv, hs), ", ".join(red[n]) or "-"))
missing = sorted(NEW - set(red))
print("new rows emitted: %d of %d%s" % (len(NEW & set(red)), len(NEW), ("; MISSING: " + ", ".join(missing)) if missing else ""))
print("new rows red under no table-3 mutant: %s" % (", ".join(n for n in sorted(NEW & set(red)) if not red[n]) or "none"))
