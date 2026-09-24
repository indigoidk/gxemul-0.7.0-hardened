#!/usr/bin/env python3
"""Write one variant's dev_footbridge.c (or the frozen copy for BASE) to <out>, from gen_variants.
Usage: mkvar.py <vid|BASE> <out path>.  Refuses unless the anchor matches exactly once."""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_q2e as gen_variants  # noqa: E402

vid, out = sys.argv[1], sys.argv[2]
fz = io.open(gen_variants.FROZEN, encoding="utf-8", newline="").read()
if vid == "BASE":
    txt = fz
else:
    v = [x for x in gen_variants.variants() if x["vid"] == vid]
    if len(v) != 1:
        print("no such variant", vid)
        sys.exit(2)
    v = v[0]
    if fz.count(v["old"]) != 1:
        print("ANCHOR COUNT != 1 for", vid)
        sys.exit(2)
    txt = fz.replace(v["old"], v["new"])
io.open(out, "w", encoding="utf-8", newline="").write(txt)
print("wrote", vid)
