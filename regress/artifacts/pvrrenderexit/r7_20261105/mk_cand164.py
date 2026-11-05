#!/usr/bin/env python3
"""mk_cand164.py -- writes cand164_probe.py: the shipped 148-row probe (argv[1]) plus repair 7's sixteen rows in eight sessions
(ruling ../adj_reg_20261105/ADJ_MYTHOS_local.md section 2), inserted before the probe's summary lines.  The pixel-read regex of
psession_at() is copied byte for byte from the probe's own psession(), so no backslash passes through this script's quoting."""
import io
import sys

src_path, out_path = sys.argv[1], sys.argv[2]
src = io.open(src_path, encoding="latin-1", newline="").read()
anchor = "\nn_ok = sum(1 for _, ok in rows if ok)\n"
assert src.count(anchor) == 1
regex_lines = [l for l in src.split("\n") if 're.finditer(r"^cpu0:' in l]
assert len(regex_lines) == 1
REGEX = regex_lines[0]

BLOCK = '''
# ---- REPAIR 7 (the REGRESS stage's register cell; ruling adj_reg_20261105/ADJ_MYTHOS_local.md, reading (i)): each guard's constant
# ---- 0 swapped for a d->reg value the guarded body reads -- fb_base (REG(PVRREG_FB_RENDER_ADDR1)), palette_cfg (PALETTE_CFG & 3) or
# ---- the first PALETTE register.  Every session above leaves those registers at their reset 0, equal to the constant, so no row
# ---- above can see such a swap; these sessions set each register non-zero.
FB_RENDER_ADDR1, PALETTE_CFG, PALETTE0 = 0xa05f8060, 0xa05f8108, 0xa05f9000
FBHI, FBEDGE = 0x200000, 0x300000   # linear frame bases: frame check fb_base <= 8 MB - 614400 holds; texels at 0x100000 lie outside
FBA = [(100.0, 100.0), (140.0, 100.0), (120.0, 120.0)]     # simpleline, red: row 105 spans 105..135
FBB = [(200.0, 100.0), (240.0, 100.0), (220.0, 120.0)]     # textured, u = v = 0: texel (0,0), red; row 105 spans 205..235
LEFT3R = [(-60.0, -57.0), (60.0, -57.0), (0.0, 3.0)]       # LEFT3 raised: row 2, its last, spans -1.0..1.0 (rows -57..-1 return)
LREVM = [(60.0, 10.0), (-60.0, 10.0), (0.0, 70.0)]         # LREV moved: row 69, its last, arrives 1.0 then -1.0
PIX.update({"fb s": (120, 105), "fb t": (220, 105), "p tip": (1, 2), "p l tip": (1, 69)})


def psession_at(name, body, pixels, base):
    """psession() with every pixel read at `base` + its usual linear offset."""
    for p in pixels:
        x, y = PIX[p]
        body = body + ["r7=0x%x" % (VRAM + base + ((y * 640 + x) & ~1) * 2), "pc=0x%x" % (CODE + 4), "step 1", "reg"]
    _, t, how = session(name, body)
@@REGEX@@
    half = lambda v, x: ((v >> 16) if x & 1 else v) & 0xffff
    return {p: (half(vals[i], PIX[p][0]) if i < len(vals) else None) for i, p in enumerate(pixels)}, t, how


#  fbhi: frame at 0x200000 -- `y < fb_base` returns every row and `x > fb_base` draws no column, in either rasterizer.
FBS = CFG + store(FB_RENDER_ADDR1, FBHI) + texels()
for z, nm in ((False, "fbhi"), (True, "zfbhi")):
    P, T, how = psession_at(nm, FBS + header(z) + tri(FBA, 2.0, 0xff0000) + header(z, TEX_RED) + tri(FBB, 2.0) + GO,
                            ["fb s", "fb t"], FBHI)
    row(nm + " s px", px(P["fb s"]), px(RED), ("Z-off twin: " if z else "") + "simpleline, frame at 0x200000")
    row(nm + " t px", px(P["fb t"]), px(RED), ("Z-off twin: " if z else "") + "texturedline, frame at 0x200000")
#  fbedge / fbtedge: frame at 0x300000 (0x200000 is TEX_RED's value) -- LREV's row 259 arrives 1.0 / -1.0, so `x1 < fb_base && x2 < 0`
#  returns it and (1,259) stays black; LEFT3's row 159 spans -1.0..1.0, so `x1 < 0 && x2 < fb_base` returns it and (1,159) stays black.
for z, nm in ((False, "fbedge"), (True, "zfbedge")):
    P, T, how = psession_at(nm, CFG + store(FB_RENDER_ADDR1, FBEDGE) + header(z) + tri(LREV, 2.0, 0xff0000)
                            + tri(LEFT3, 2.0, 0xff0000) + GO, ["l tip", "tip"], FBEDGE)
    row(nm + " l tip", px(P["l tip"]), px(RED), ("Z-off twin: " if z else "") + "LREV row 259 at frame 0x300000")
    row(nm + " x2 tip", px(P["tip"]), px(RED), ("Z-off twin: " if z else "") + "LEFT3 row 159 at frame 0x300000")
for z, nm in ((False, "fbtedge"), (True, "zfbtedge")):
    P, T, how = psession_at(nm, CFG + store(FB_RENDER_ADDR1, FBEDGE) + texel(TEXEL_LINEAR[TEX_RED], RED) + header(z, TEX_RED)
                            + tri(LREV, 2.0) + tri(LEFT3, 2.0) + GO, ["l tip", "tip"], FBEDGE)
    row(nm + " l tip", px(P["l tip"]), px(RED), ("Z-off twin: " if z else "") + "textured LREV row 259, frame 0x300000")
    row(nm + " x2 tip", px(P["tip"]), px(RED), ("Z-off twin: " if z else "") + "textured LEFT3 row 159, frame 0x300000")
#  palcfg: PALETTE_CFG = 3 and PALETTE[0] = 0x10000, frame at 0 (the textures are RGB565, so neither is used): `y < 3` returns
#  LEFT3R's row 2; `x > 3` loses columns 1-3; `x1 < 0 && x2 < 3` returns LEFT3R's row 2 (-1, 1); `x1 < 3 && x2 < 0` returns LREVM's
#  row 69 (1, -1).  At 0x10000 the same reads lose all four forms.
PCS = CFG + store(PALETTE_CFG, 3) + store(PALETTE0, 0x10000) + texel(TEXEL_LINEAR[TEX_RED], RED)
for z, nm in ((False, "palcfg"), (True, "zpalcfg")):
    P, T, how = psession(nm, PCS + header(z, TEX_RED) + tri(LEFT3R, 2.0) + tri(LREVM, 2.0) + GO, ["p tip", "p l tip"])
    row(nm + " x2 tip", px(P["p tip"]), px(RED), ("Z-off twin: " if z else "") + "LEFT3R row 2, PALETTE_CFG 3")
    row(nm + " l tip", px(P["p l tip"]), px(RED), ("Z-off twin: " if z else "") + "LREVM row 69, PALETTE_CFG 3")
'''.replace("@@REGEX@@", REGEX)
out = src.replace(anchor, "\n" + BLOCK + anchor)
io.open(out_path, "w", encoding="latin-1", newline="").write(out)
assert chr(8) not in out
print("wrote", out_path)
