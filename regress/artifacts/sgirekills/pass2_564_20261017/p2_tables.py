#!/usr/bin/env python3
"""p2_tables.py <sgirekills artifacts dir> <section> -- two derived tables for #564's pass-2 packet, computed from the
logs rather than typed:
  join      the SHIPPED detector (md5 86caed24) on HEAD 2951694f beside the fix, row by row, from
            detector_564_20261017/probe_{HEAD_2951694f,FIX_564}_shipped.out;
  neverred  per detector row, how many mutants turned it red in kill table 1 (raw/) and table 2 (raw2/), and the
            rows NO mutant turned red.
Every log must end with its completion sentinel, or this refuses (exit 9) instead of printing a partial table."""
import glob, io, os, re, sys

A, SEC = sys.argv[1], sys.argv[2]

def rows(path):
    t = io.open(path, encoding="utf-8", errors="replace").read()
    if not t.rstrip().endswith("MTEDECL_DONE"):
        print("REFUSE: %s has no completion sentinel" % path); sys.exit(9)
    lines = t.splitlines()
    #  the row name sits in a fixed-width field whose width is read off the header ("row" padded, then "got"):
    #  14 columns in the tabled instrument, 16 in the shipped one
    hdr = next(l for l in lines if l.startswith("row ") and " got " in l)
    w, g = hdr.index("got") - 1, hdr.index("want")
    out = []
    for l in lines:
        s = l.rstrip()
        if l is hdr or not (s.endswith(" ok") or s.endswith(" FAIL")):
            continue
        out.append((l[:w].strip(), l[w:g].strip(), "ok" if s.endswith(" ok") else "FAIL"))
    m = re.search(r"MTEDECL_RESULT=(\d+)/(\d+)", t)
    return out, m.group(0)

if SEC == "join":
    D = os.path.join(A, "detector_564_20261017")
    h, hr = rows(os.path.join(D, "probe_HEAD_2951694f_shipped.out"))
    f, fr = rows(os.path.join(D, "probe_FIX_564_shipped.out"))
    if [r[0] for r in h] != [r[0] for r in f]:
        print("REFUSE: the two logs do not list the same rows in the same order"); sys.exit(9)
    print("%-16s %-24s %-24s" % ("row", "HEAD 2951694f", "fix (#564)"))
    for (n, hg, hs), (_, fg, fs) in zip(h, f):
        print("%-16s %-24s %-24s" % (n, "%s %s" % (hg, hs), "%s %s" % (fg, fs)))
    print("HEAD %s    fix %s    (rows: %d)" % (hr, fr, len(h)))
elif SEC == "neverred":
    K = os.path.join(A, "killtable_564_20261017")
    base, _ = rows(os.path.join(K, "raw2", "base.out"))
    names = [r[0] for r in base]
    red = {n: [[], []] for n in names}
    for t, sub in ((0, "raw"), (1, "raw2")):
        for p in sorted(glob.glob(os.path.join(K, sub, "*.out"))):
            mu = os.path.basename(p)[:-4]
            if mu in ("base", "null"):
                continue
            rr, _ = rows(p)
            for n, _, s in rr:
                if s == "FAIL":
                    red[n][t].append(mu)
    #  names are listed only where a row has at most three catchers -- the rows a single lost mutant would leave
    #  unscored; the per-mutant catcher lists are KILLTABLE.txt / KILLTABLE2.txt themselves
    print("%-16s %-9s %-9s %s" % ("row", "table 1", "table 2", "its catchers when 3 or fewer (table 2 marked *)"))
    for n in names:
        a, b = red[n]
        c = a + ["*" + x for x in b]
        print("%-16s %-9d %-9d %s" % (n, len(a), len(b), "-- NONE --" if not c else (", ".join(c) if len(c) <= 3 else "")))
    never = [n for n in names if not red[n][0] and not red[n][1]]
    only2 = [n for n in names if not red[n][0] and red[n][1]]
    print("rows red under NO mutant of either table (%d of %d): %s" % (len(never), len(names), ", ".join(never) or "none"))
    print("rows red ONLY in table 2 (%d): %s" % (len(only2), ", ".join(only2) or "none"))
else:
    print("usage: p2_tables.py <dir> join|neverred"); sys.exit(2)
