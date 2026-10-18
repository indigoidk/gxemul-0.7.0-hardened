#!/usr/bin/env python3
"""summarize_564.py <killtable dir> -- KILLTABLE.txt from raw/<name>.out: per mutant its score, the rows that went red
(the MEASURED catchers) beside the catchers mutants_564.py PREDICTED, and a verdict.  A log without its completion
sentinel is INCOMPLETE, never a score.  base must be all-green and null must be all-red, or the table is void."""
import io, os, re, sys

K = sys.argv[1]
sys.path.insert(0, K)
import mutants_564 as M

def load(name):
    p = os.path.join(K, "raw", name + ".out")
    if not os.path.exists(p):
        return None
    t = io.open(p, encoding="utf-8", errors="replace").read()
    if not t.rstrip().endswith("MTEDECL_DONE"):
        return {"incomplete": True}
    m = re.search(r"MTEDECL_RESULT=(\d+)/(\d+)", t)
    #  the probe prints each row name in a fixed-width field; its width is read off the header line ("row" padded,
    #  then "got"), because the tabled instrument used 14 columns and the shipped one 16
    hdr = next(l for l in t.splitlines() if l.startswith("row ") and " got " in l)
    w = hdr.index("got") - 1
    fails = [l[:w].strip() for l in t.splitlines() if l.rstrip().endswith("FAIL")]
    return {"ok": int(m.group(1)), "n": int(m.group(2)), "fails": fails}

out = []
probe_md5 = None
for name in ("base", "null"):
    r = load(name)
    out.append("%-9s %s" % (name, "MISSING" if r is None else ("INCOMPLETE" if r.get("incomplete") else "%d/%d" % (r["ok"], r["n"]))))
base, null = load("base"), load("null")
void = (base is None or base.get("incomplete") or base["ok"] != base["n"] or null is None or null.get("incomplete")
        or null["ok"] != 0)
out.append("TABLE VOID: base must be all-green and null all-red" if void else "base all-green, null all-red: table valid")
out.append("")
killed = 0
for name, _, pred in M.M:
    r = load(name)
    if r is None:
        out.append("%-9s MISSING (build failed or not run)" % name); continue
    if r.get("incomplete"):
        out.append("%-9s INCOMPLETE run -- no score" % name); continue
    k = r["ok"] < r["n"]
    killed += k
    out.append("%-9s %2d/%-2d %-8s caught by: %s" % (name, r["ok"], r["n"], "KILLED" if k else "ESCAPED", ", ".join(r["fails"]) or "-"))
    out.append("%-9s %-14s predicted: %s" % ("", "", pred))
out.append("")
out.append("KILL TABLE: %d/%d killed" % (killed, len(M.M)))
io.open(os.path.join(K, "KILLTABLE.txt"), "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
print("\n".join(out))
