#!/usr/bin/env python3
"""x1_corpus.py REGRESS_DIR TOKENS_PY OUT_TSV -- every .py under REGRESS_DIR (artifacts/ INCLUDED), classified three
ways by THIS interpreter: census_tokens.py promptless (run as the gate runs it: paths on stdin, relative to the dir),
census_tokens.py whole (same), and the deriver's astcall logic (copied verbatim below).  One TSV line per file."""
import ast, io, os, subprocess, sys

root, tok, out = sys.argv[1], sys.argv[2], sys.argv[3]
rels = []
for dp, dn, fn in os.walk(root):
    dn.sort()
    for f in sorted(fn):
        if f.endswith(".py"):
            rels.append(os.path.relpath(os.path.join(dp, f), root).replace(os.sep, "/"))
rels.sort()
feed = ("\n".join(rels) + "\n").encode("utf-8")


def census(mode):
    r = subprocess.run([sys.executable, tok, mode, root], input=feed, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return r.returncode, [l.strip("\r") for l in r.stdout.decode("utf-8").split("\n") if l.strip("\r")]


def astcall(path):   # verbatim logic of derive_hygiene_pins.sh astcall()
    try:
        t = ast.parse(open(path, encoding="utf-8").read())
    except Exception:
        return 2
    m = "ends" + "with"
    return 0 if any(isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == m
                    for n in ast.walk(t)) else 1


prc, pl = census("promptless")
wrc, wh = census("whole")
pls = set(pl)
whd = {}
for e in wh:
    k, _, v = e.rpartition(":")
    whd[k] = v
with io.open(out, "w", encoding="utf-8", newline="\n") as o:
    o.write("# %s  python %s  files %d  census rc %d/%d\n" % (sys.executable, sys.version.split()[0], len(rels), prc, wrc))
    for r in rels:
        o.write("%s\t%d\t%s\t%d\n" % (r, 1 if r in pls else 0, whd.get(r, "0"), astcall(os.path.join(root, r))))
print("X1 %s: %d files, promptless %d, whole-files %d" % (sys.version.split()[0], len(rels), len(pls), len(whd)))
