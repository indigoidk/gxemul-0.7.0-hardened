#!/usr/bin/env python3
"""Write the Opus seat's 570 variants (its own gen_variants.py) as mutated device files into argv[1]."""
import hashlib, io, os, sys

V = sys.argv[1]
OPUS = "/mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/fbd5/q2c/opus"
SEC_DEV = "/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/devices/dev_footbridge.c"
sys.path.insert(0, OPUS)
import gen_variants  # noqa: E402

fix = io.open(SEC_DEV, encoding="utf-8", newline="").read()
allv = gen_variants.variants()
bad = 0
for v in allv:
    if fix.count(v["old"]) != 1 or v["old"] == v["new"]:
        print("%s ANCHOR-ERROR (%d)" % (v["vid"], fix.count(v["old"])))
        bad += 1
        continue
    out = fix.replace(v["old"], v["new"])
    io.open(os.path.join(V, v["vid"] + ".c"), "w", encoding="utf-8", newline="").write(out)
print("OPUS VARIANTS: %d written, %d anchor errors (gen_variants.py md5 %s)" % (
    len(allv) - bad, bad, hashlib.md5(open(OPUS + "/gen_variants.py", "rb").read()).hexdigest()[:8]))
