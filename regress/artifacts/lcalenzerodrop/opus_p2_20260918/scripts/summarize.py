#!/usr/bin/env python3
"""Tabulate every leg log: per (cell, binary) the score and the getenv value(s); flag any leg whose
completion sentinel is missing.  Reads the logs from the directory given as argv[1]."""
import os, re, sys
L = sys.argv[1]
cells = ["frozen", "k16", "l0w16", "l0w64", "l2w64", "low16", "mc2", "kbc16", "kbc256", "kbc1024"]
bins = ["base", "va", "vb", "vc", "vd", "ve", "vf", "vg", "vh", "vt1", "vt2", "vw64", "vw256"]
res = {}
missing = []
for f in sorted(os.listdir(L)):
    m = re.match(r"(\w+?)__(\w+)\.log$", f)
    if not m:
        continue
    c, b = m.groups()
    t = open(os.path.join(L, f), encoding="utf-8", errors="replace").read()
    lines = t.strip().splitlines()
    done = lines and lines[-1].strip() in ("WIDEWRITE_DONE", "WIDECELL_DONE")
    if not done:
        missing.append(f)
    sc = re.search(r"(?:WIDEWRITE_RESULT=|WIDECELL_RESULT=\S+ \S+ )(\d+/\d+)", t)
    vals = []
    for ln in lines:
        if "getenv" in ln:
            parts = ln.split()
            # frozen: 'wide getenv <got> <want> ...' (decimal); cell: '<cell> getenv <port> <got> <want> ...'
            if parts[0] == "wide":
                vals.append("0x%02x" % int(parts[2]) if parts[2].isdigit() else parts[2])
            else:
                vals.append(parts[3])
    retried = "RETRIED=yes" in t
    res[(c, b)] = ("%s %s%s" % (sc.group(1) if sc else "?", "/".join(vals), " R" if retried else ""))
w = 16
print("cell".ljust(9) + "".join(b.ljust(w) for b in bins))
for c in cells:
    print(c.ljust(9) + "".join(res.get((c, b), "-").ljust(w) for b in bins))
print("legs: %d   missing completion sentinel: %s" % (len(res), missing or "none"))
