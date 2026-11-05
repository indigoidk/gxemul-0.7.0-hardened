#!/usr/bin/env python3
"""mk_gate_r7.py -- gate_pvr_block.new for the 164-row probe: ../r5_20261105/gate_pvr_block.new with its counts at 164, the sixteen
repair-7 row names added to the named-row list (on its one line), and the header's session count, scope, timing and table list
brought up to date.  Every edit is an exact, once-only replacement.  usage: mk_gate_r7.py <table-7 phrase file> <out>"""
import io
import sys

s = io.open("../r5_20261105/gate_pvr_block.new", encoding="utf-8", newline="").read()
T7 = io.open(sys.argv[1], encoding="utf-8").read().rstrip("\n")
NEW = ["fbhi s px", "fbhi t px", "zfbhi s px", "zfbhi t px", "fbedge l tip", "fbedge x2 tip", "zfbedge l tip", "zfbedge x2 tip",
       "fbtedge l tip", "fbtedge x2 tip", "zfbtedge l tip", "zfbtedge x2 tip", "palcfg x2 tip", "palcfg l tip", "zpalcfg x2 tip",
       "zpalcfg l tip"]
EDITS = [
    ("NOT run here; this is its detector: 148 rows -- the witness's nine plus fifty render sessions whose pixels are read back",
     "NOT run here; this is its detector: 164 rows -- the witness's nine plus fifty-eight render sessions whose pixels are read back"),
    ("#  swap body read from above and span starts at a negative x, each with its Z-off twin).  Needs only the binary: -E dreamcast with\n"
     "#  a 4-byte dummy image at 0x8c010000, about two seconds (r5_20261105/base148f/: 2.1 s).",
     "#  swap body read from above and span starts at a negative x, and repair 7's renders with a non-zero frame base or a non-zero\n"
     "#  PALETTE_CFG and first PALETTE register, each with its Z-off twin).  Needs only the binary: -E dreamcast with a 4-byte dummy\n"
     "#  image at 0x8c010000, 1-4 s (r7_20261105/base164/: 4.0 s; table7/probe_base.out: 1.4 s)."),
    ("PRETABLE_4.errata.md) and r5_20261105/table5/ (this probe: all 192 of PRETABLE_5.out's\n",
     "PRETABLE_4.errata.md), r5_20261105/table5/ (the 148-row probe: all 192 of PRETABLE_5.out's\n"),
    ("thirteen non-finite forms excluded).\n",
     "thirteen non-finite forms excluded);\n" + T7 + "\n"),
    ('check "pvr_zwrite rows run"     "${pzres#*/}" 148', 'check "pvr_zwrite rows run"     "${pzres#*/}" 164'),
    ('check "pvr_zwrite rows correct" "${pzres%/*}" "148"', 'check "pvr_zwrite rows correct" "${pzres%/*}" "164"'),
    ('"negx n start" "znegx n start" "texnegx n start" "ztnegx n start"; do',
     '"negx n start" "znegx n start" "texnegx n start" "ztnegx n start" ' + " ".join('"%s"' % n for n in NEW) + "; do"),
    ('+ $(count "$PVRLOG" " FAIL$") ))" "148"', '+ $(count "$PVRLOG" " FAIL$") ))" "164"'),
    ('check "pvr zwrite rows green"   "$(count "$PVRLOG" " ok$")"   "148"', 'check "pvr zwrite rows green"   "$(count "$PVRLOG" " ok$")"   "164"'),
]
for old, new in EDITS:
    assert s.count(old) == 1, ("not exactly once", old[:70])
    s = s.replace(old, new)
assert "148" not in s.replace("148-row", "").replace("all 148 of its predictions", ""), [l for l in s.split("\n") if "148" in l]
wide = [(len(l), l[:60]) for l in s.split("\n") if l.startswith("#") and len(l) > 134]
assert not wide, wide
io.open(sys.argv[2], "w", encoding="utf-8", newline="").write(s)
names = s.split('for v in ', 1)[1].split('; do', 1)[0]
print("wrote", sys.argv[2], "- named rows:", names.count('" "') + 1)
