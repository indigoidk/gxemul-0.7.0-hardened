#!/usr/bin/env python3
"""mk_probe_r7.py -- the shipped probe for repair 7: table7/probe164_frozen.py (the instrument table 7 measured) with its docstring
brought to the 164 rows -- the records the repair-7 ruling names (the contract's operand-swap sentence, F3's PROBE-DESIGN NOTE),
shape (c)'s register sources, and the counts this diff makes false (the repair list, "this probe's 148 rows", the legs sentence,
"FB_RENDER_ADDR1 is 0 here") -- with pass 8's correction (the first PALETTE register is not a body-read value: 12 FLOOR cells, 39
(c) cells) applied, and the repair-7 block comment narrowed to match.  Every edit is an exact, once-only replacement: EDITS inside
the docstring, CEDITS in comment lines after it.  usage: mk_probe_r7.py <table-7 sentence file> <out>"""
import io
import sys

SRC = "table7/probe164_frozen.py"
s = io.open(SRC, encoding="latin-1", newline="").read()
doc_end = s.index('"""\n', 10)
T7 = io.open(sys.argv[1], encoding="utf-8").read().rstrip("\n")

EDITS = [
    # the repair list in WHAT THE ROWS MEASURE
    ("z 4.0; negx, znegx, texnegx and ztnegx read a span whose start is NEGATIVE.\n",
     "z 4.0; negx, znegx, texnegx and ztnegx read a span whose start is NEGATIVE.  Repair 7: fbhi, fbedge and fbtedge render with\n"
     "FB_RENDER_ADDR1 non-zero, palcfg with PALETTE_CFG and the first PALETTE register non-zero, each with a Z-off twin.\n"),
    # table 5's sentence: this probe has 164 rows now
    ("RAN on 2026-11-05, 06:29:53-06:40:24 local, on this probe's 148 rows: all 192 of its predictions hit",
     "RAN on 2026-11-05, 06:29:53-06:40:24 local, on the 148-row probe: all 192 of its predictions hit"),
    # the repair-7 sentence after table 5's
    ("(table5/CHECK.txt, VERDICT.md).\nCOVERED -- ",
     "(table5/CHECK.txt, VERDICT.md).\n" + T7 + "\nCOVERED -- "),
    # the contract's operand-swap sentence, extended with the register sources and the repair-7 rows (pass 8: two sources, not three)
    ("only, on the Z-off twins (`zyedges t in`, `zedges l in`) [r3];\n",
     "only, on the Z-off twins (`zyedges t in`, `zedges l in`) [r3]; and from the d->reg values the body reads -- fb_base =\n"
     "REG(PVRREG_FB_RENDER_ADDR1) (both rasterizers) and palette_cfg (texturedline) -- into the constant 0 of `y < 0`, `x1 < 0`,\n"
     "`x2 < 0` and `x > 0`, twelve cells, each register 0 in every session above: frame at 0x200000, `fbhi s px` and `fbhi t px`\n"
     "(`y <`, `x >`); at 0x300000, `fbedge l tip`, `fbedge x2 tip`, `fbtedge l tip`, `fbtedge x2 tip` (all four); PALETTE_CFG 3,\n"
     "`palcfg x2 tip`, `palcfg l tip` (all four); Z-off: their z twins [r7].  With PALETTE[0] 0x10000 the palcfg rows also red the\n"
     "four swaps to the first PALETTE register, checks outside the class: dev_pvr.c:842 forms the palette's address, and :843-844 read\n"
     "elements indexed by a VRAM byte.  (Corrected 2026-11-05, pass 8 -- codex: this read \"palette_cfg and the first PALETTE register\n"
     "(texturedline)\" and \"sixteen cells\".)  palette_cfg's partition {0, 1, 2, 3}, tested only by texture format 6's switch, which no\n"
     "session renders, is SAMPLED at 0 and 3 (clause-(e) DEBT); parameters and buffer elements are not swap sources (the repair-7\n"
     "ruling, section 1(c));\n"),
    # F3's PROBE-DESIGN NOTE, extended
    ("PROBE-DESIGN NOTE: the probe's standard depth 2.0 equals d->bytes_per_pixel, so every constant write of B is invisible at depth 2.0.\n",
     "PROBE-DESIGN NOTE: the probe's standard depth 2.0 equals d->bytes_per_pixel, so every constant write of B is invisible at depth 2.0.\n"
     " Likewise every register the probe leaves at its reset 0 equals the guards' constant 0, so a detector of a d->reg consumer owes one\n"
     "session with that register non-zero (repair 7).\n"),
    # shape (c): the exchange bodies' body-read sources include the register spellings (pass 8: 39, not 51)
    ("`tmpf = v1`, `v2 = tmpf` -> X, Y, B.  Remedy: the sets below.\n (d) right-hand side to another local",
     "`tmpf = v1`, `v2 = tmpf` -> X, Y, B.  Remedy: the sets below.\n"
     "The register sources (repair 7) -- fb_base in both bodies and palette_cfg in texturedline's: 39 more cells (DERIVED: 15\n"
     "statements x 1 + 12 x 2), DEBT, not measured; texturedline's 12 to the first PALETTE register are disclosed apart, outside the\n"
     "class.  (Corrected 2026-11-05, pass 8 -- codex: this said \"fb_base in both bodies, palette_cfg and the first PALETTE register in\n"
     "texturedline's: 51 more cells (DERIVED: 15 statements x 1 + 12 x 3)\".)\n (d) right-hand side to another local"),
    # the Y2 disclosure: the frame base is non-zero in repair 7's sessions now
    ("frame (FB_RENDER_ADDR1 is 0 here, so before VRAM itself)",
     "frame (FB_RENDER_ADDR1 is 0 there, so before VRAM itself)"),
    # the legs sentence
    ("(r4_20261105/table4/SCORES.txt).  This 148-row probe (repair 5): the fix 148/148 in ~2 s with",
     "(r4_20261105/table4/SCORES.txt).  The 148-row probe (repair 5): the fix 148/148 in ~2 s with"),
    ("(r5_20261105/table5/SCORES.txt).\n\nSentinel:",
     "(r5_20261105/table5/SCORES.txt).  This 164-row probe (repair 7): the fix 164/164 in 1-4 s with no session timed out (62 sessions),\n"
     "and the pre-fix build 78/164 with the symptom PRESENT (r7_20261105/base164/, head164/: the 148-row probe's 78 red rows plus the\n"
     "eight repair-7 rows whose session carries a Z-off header, the z twins'); its null media 9/164, 0/164 and 1/164, each CONTROL=FAIL\n"
     "(r7_20261105/table7/SCORES.txt).\n\nSentinel:"),
]
CEDITS = [
    # the repair-7 block comment (pass 8: the first PALETTE register is not among the body's reads)
    ("# ---- REPAIR 7 (the REGRESS stage's register cell; ruling adj_reg_20261105/ADJ_MYTHOS_local.md, reading (i)): each guard's constant\n"
     "# ---- 0 swapped for a d->reg value the guarded body reads -- fb_base (REG(PVRREG_FB_RENDER_ADDR1)), palette_cfg (PALETTE_CFG & 3) or\n"
     "# ---- the first PALETTE register.  Every session above leaves those registers at their reset 0, equal to the constant, so no row\n"
     "# ---- above can see such a swap; these sessions set each register non-zero.\n",
     "# ---- REPAIR 7 (the REGRESS stage's register cell; ruling adj_reg_20261105/ADJ_MYTHOS_local.md, reading (i), and its .errata.md):\n"
     "# ---- each guard's constant 0 swapped for a d->reg value the guarded body reads -- fb_base (REG(PVRREG_FB_RENDER_ADDR1)) or\n"
     "# ---- palette_cfg (PALETTE_CFG & 3); palcfg also sets the first PALETTE register, for four checks outside that class (pass 8: this\n"
     "# ---- listed it among the body's reads).  Every session above leaves those registers at their reset 0, equal to the constant, so\n"
     "# ---- no row above can see such a swap; these sessions set each register non-zero.\n"),
]
for old, new in EDITS:
    assert s.count(old) == 1, ("not exactly once", old[:60])
    assert s.index(old) < doc_end, ("outside the docstring", old[:60])
    s = s.replace(old, new)
    doc_end = s.index('"""\n', 10)
for old, new in CEDITS:
    assert s.count(old) == 1, ("not exactly once", old[:60])
    assert s.index(old) > doc_end, ("inside the docstring", old[:60])
    assert all(l.startswith("#") for l in (old + new).rstrip("\n").split("\n")), "a comment edit must touch comment lines only"
    s = s.replace(old, new)
long = [l for _, n in EDITS + CEDITS for l in (n + "\n" + T7).split("\n") if len(l) > 134]
assert not long, long
io.open(sys.argv[2], "w", encoding="latin-1", newline="").write(s)
print("wrote", sys.argv[2], "-", len(EDITS), "docstring edits,", len(CEDITS), "comment edit")
