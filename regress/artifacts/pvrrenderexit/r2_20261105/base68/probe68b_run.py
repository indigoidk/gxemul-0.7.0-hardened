#!/usr/bin/env python3
"""pvrrenderexit -- DETECTOR (built on its rung-3 witness) for the Dreamcast PVR renderer's Z-write-disable exit, dev_pvr.c.

DEFECT (filed 2026-10-02).  src/devices/dev_pvr.c, pvr_render(): a STARTRENDER write renders the Tile Accelerator commands the
guest submitted; for a polygon header whose list word 1 has bit 26 set (Z-write DISABLED, `zwrite = !((list[1] >> 26) & 1)`)
the renderer printed "pvr: no zwrite? not implemented yet." and called exit(1) -- the emulator process ended.

THE FIX (#NNN).  Such a polygon goes through the same depth test and rasterization as any other polygon, and only its depth store
is skipped: both rasterizers (simpleline, texturedline) check d->zwrite_disabled at their vram_z stores, case 4 assigns it from
the header's bit, and every pvr_render clears it first, so a list with no header does not inherit the previous render's value.

WHAT THE ROWS MEASURE (`-E dreamcast`, an UNMODIFIED in-tree machine; one cold debugger session per case).  Every device access is a
REAL guest instruction through the SH-4 decoder and memory_rw: `mov.l r8,@r7` and `mov.l @r7,r8` placed at 0x8c010000.  A render
session writes FB_RENDER_CFG = 1 (RGB565), polygon headers and vertices to the TA (the store at offset 0x1c submits a command), then
STARTRENDER, which renders synchronously inside that store; pixels are read back through the linear VRAM window, one 32-bit guest
load per pixel.  T1 is drawn first at z = 2.0 and T2 second at z = 1.0 over it; the renderer keeps the larger z (vram_z <= z).
  CONTROLS (13): the PVR ID register reads 0x17fd11db through a guest load (RAM would not); a Z-write-enabled render runs to the
end and survives to the prompt; a bogus machine runs nothing; the Z-off render was reached (`zoff rendered`); and the pixels no
enumerated variant moves -- ovon's T2-only, T1-only and background pixels, and the T2-only pixels of texon, equal and texequal.
  zoff (R1): one Z-off header survives to the prompt.  ovoff (R2): a Z-off T1, then T2 -- T1 stored no depth, so T2 draws over
it.  ovon (R3): both Z-on -- T1's depth hides T2.  behind (R6): a Z-off T2 behind a Z-on T1 still fails the depth test.  texoff
(R4), texbeh and texon (R7): the same cells through texturedline, from red and green texels.  two (R5): a Z-off render, then a
second render of bare vertices -- no header, so Z-write is on (the per-render reset).  sticky (R8): a Z-off header, then a Z-on one
in the same render.  edges and texedges (R9): triangles across the left and right screen edges pin the x-range bound above both
stores at its edges.  equal and texequal (R10): two Z-on polygons at the SAME z -- the later one wins under `<=`.

CLAUSE (e) -- catches (test-variant table 1, artifacts/pvrrenderexit/det_20261104/table1/SCORES.txt and VERDICT.md, PRETABLE.out
with its addenda 6 and 7 written before it; 35 of 36 variants red, each on exactly its predicted rows): the removed exit reinstated
verbatim (B1); either rasterizer's store left unguarded, its guard inverted, or its store never made (M1-M4, M15, M16); case 4's
assignment forced to 0 or to 1, inverted, or made set-only (M5-M8); the per-render reset deleted, moved into pvr_reset_ta(), set
to 1, or moved into the command loop (M9, M10, M32, M33); Z-off polygons declined, or the guard folded into the depth test (M11,
M12, M28); the depth test bypassed for Z-off or for Z-on polygons, or deleted (M13, M14, M26, M26b, M27, M27b); its equal edge
tightened (M29, M30); either x-range bound moved by one (M18-M25); the wrong header bit (M31).
  discloses, not claimed: M17 (the reset moved to the end of pvr_render) is EQUIVALENT -- the render loop has no early exit after
the reset's old position, the field's only non-zero writer is inside that loop, and DEVINIT zeroes it -- so no row can see it;
the three sibling exits in the same function (an unimplemented texture pixel format, a non-RGB565 render mode, an unimplemented
list command) keep their own disposition (the list-command exit is witnessed at artifacts/pvrrenderexit/sibling_listcmd_20261104/);
the equal-depth rows rely on z staying exactly 2.0 across a flat triangle (every slope is 0.0 in pvr_render_triangle and in both
rasterizers; measured green on the fix); fog, translucency and the other list types.  On this 51-row probe the pre-fix build
scores 25 of the 51 rows with the symptom PRESENT, and three null media -- /bin/true, an absent binary, /bin/false -- each
CONTROL=FAIL (det_20261104/legs51/LEGS.log).

Sentinel: PVR_ZWRITE_PROBE_DONE (plus PVR_ZWRITE_RESULT=n/N, _CONTROL=OK|FAIL, _SYMPTOM=PRESENT|ABSENT, _RED=none|<names>).
Session transcripts go to the optional [workdir].
"""

import os
import re
import struct
import subprocess
import sys
import tempfile
import time

if len(sys.argv) < 2:
    sys.stderr.write("usage: pvr_zwrite_probe.py <gxemul> [label] [workdir]\n")
    sys.exit(2)

BIN = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "local"
WORK = sys.argv[3] if len(sys.argv) > 3 else None
if WORK:
    os.makedirs(WORK, exist_ok=True)
_TMPDIR = tempfile.mkdtemp(prefix="pvr_zwrite_")
DUMMY = os.path.join(_TMPDIR, "dummy.bin")
open(DUMMY, "wb").write(bytes(4))

CODE = 0x8c010000            # P1 RAM
W_STORE = 0x00092782          # mov.l r8,@r7 ; nop  (little-endian halfwords)
W_LOAD = 0x00096872           # mov.l @r7,r8 ; nop
PVR_ID = 0xa05f8000           # PVRREG_REGSTART + PVRREG_ID (P2)
FB_RENDER_CFG = 0xa05f8048
STARTRENDER = 0xa05f8014
TA = 0xb0000000               # the Tile Accelerator window (P2 of 0x10000000)
POLY0 = 0x80000000            # list word 0: cmd 4 (polygon), list type 0, untextured
ZW_OFF = 0x04000000           # list word 1, bit 26: Z-write DISABLED
FATAL = "no zwrite?"
RENDERED = ", 1 Tile Accelerator commands"   # anchored: ", 11 Tile ..." must not match
VRAM = 0xa5000000             # the linear VRAM window (P2 of 0x05000000): a plain memcpy to and from d->vram
FOG2 = 0x00800000             # list word 2 bits 23-22 = 2, the one fog type the renderer does not warn about
VTX, VTX_EOS = 0xE0000000, 0xF0000000      # list word 0 of a vertex: cmd 7; bit 28 = end of strip
RED, GREEN, BLUE, BLACK = 0xf800, 0x07e0, 0x001f, 0x0000   # RGB565 pixels of packed colours 0xff0000, 0x00ff00, 0x0000ff, background
TEX_RED, TEX_GREEN = 0x200000, 0x200008    # texture addresses; u = v = 0 samples texel (0,0), which the renderer's
TEXEL_LINEAR = {TEX_RED: 0x100000, TEX_GREEN: 0x100004}   # 64-bit-area mapping reads at these linear VRAM offsets
T1 = [(100.0, 100.0), (300.0, 100.0), (200.0, 300.0)]      # drawn first, z = 2.0 (the renderer keeps the larger z: vram_z <= z)
T2 = [(150.0, 150.0), (350.0, 150.0), (250.0, 350.0)]      # drawn second, z = 1.0, overlapping T1
AWAY = [(500.0, 400.0), (620.0, 400.0), (560.0, 470.0)]    # clear of every probed pixel
LEFT = [(-60.0, 200.0), (60.0, 200.0), (0.0, 260.0)]       # spans the left edge: its row 230 runs from x = -30 to 30
RIGHT = [(580.0, 300.0), (700.0, 300.0), (640.0, 360.0)]   # spans the right edge: its row 330 runs from x = 610 to 670
RSPAN = [(639.0, 400.0), (700.0, 400.0), (639.0, 460.0)]   # vertical left edge at x = 639.0: row 430 spans 639.0..669.5
TOP = [(250.0, -30.0), (350.0, -30.0), (300.0, 30.0)]      # reaches row 0 (row 0 spans 275..325)
BOTTOM = [(300.0, 450.0), (350.0, 510.0), (250.0, 510.0)]  # reaches row 479 and, past the frame, row 480
SWAP = [(450.0, 150.0), (350.0, 150.0), (400.0, 250.0)]    # right-then-left: every span arrives x1 > x2; row 180 is 435.0..365.0
MASK27, MASK25 = 0x08000000, 0x02000000   # list word 1 bit 27 (culling mode 1: culls nothing) and bit 25 (texture1: ignored)
PIX = {"overlap": (220, 180), "t2 only": (320, 180), "t1 only": (120, 120), "bg": (10, 10),
       "l in": (1, 230), "l out": (0, 230), "r in": (639, 330), "r out": (0, 331)}   # r out: where x = 640 of row 330 would land
PIX.update({"t in": (300, 0), "b in": (300, 479), "b out": (300, 480), "swap": (400, 180), "s end": (435, 180),
            "s past": (436, 180), "rspan": (639, 430)})

rows = []
controls = []
symptom_hits = 0


def row(name, got, want, note="", control=False):
    assert name not in [n for n, _ in rows], "DUPLICATE ROW NAME %r" % name
    assert len(name) <= 16, name
    ok = (got == want)
    rows.append((name, ok))
    if control:
        controls.append((name, ok))
    print("%-18s %-20s %-20s %-46s %s" % (name, str(got), str(want), note, "ok" if ok else "FAIL"))
    return ok


def store(addr, val):
    return ["r7=0x%x" % addr, "r8=0x%x" % val, "pc=0x%x" % CODE, "step 1"]


def session(name, body, machine="dreamcast", timeout=90):
    """One cold run: the two words placed, then `body`, then `reg`.  Returns (regs, text, how)."""
    global symptom_hits
    cmds = ["put w 0x%x, 0x%08x" % (CODE, W_STORE), "put w 0x%x, 0x%08x" % (CODE + 4, W_LOAD)] + list(body) + ["reg", "quit"]
    argv = [BIN, "-V", "-x", "-E", machine, "0x%x:%s" % (CODE, DUMMY)]
    inp = ("\n".join(cmds) + "\n").encode("latin-1")
    try:
        p = subprocess.run(argv, input=inp, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
        t = p.stdout.decode("latin-1", "replace").replace("\r", "")
        rc = p.returncode
        how = ("sig%d" % -rc) if rc < 0 else ("exit%d" % rc)
    except subprocess.TimeoutExpired as e:
        t = (e.output or b"").decode("latin-1", "replace").replace("\r", "")
        how = "TIMEOUT"
    except OSError as e:            # an ABSENT binary is a null medium: every row fails, the sentinel still prints
        t = ""
        how = "NOBIN(%s)" % e.__class__.__name__
    if WORK:
        open(os.path.join(WORK, name.replace(" ", "_") + ".txt"), "w", encoding="latin-1").write(
            "$ " + " ".join(argv) + "\n--- stdin ---\n" + "\n".join(cmds) + "\n--- transcript (%s) ---\n" % how + t)
    if how != "exit0" and FATAL in t:
        symptom_hits += 1
    regs = {}
    i = t.rfind("GXemul> reg")
    if i >= 0:
        m = re.search(r"\br8\s*=\s*(0x[0-9a-fA-F]+)", t[i:])
        if m:
            regs["r8"] = int(m.group(1), 16)
    return regs, t, how


def prompt(t):
    i = t.rfind("GXemul> reg")
    return "yes" if (i >= 0 and "cpu0:" in t[i:]) else "no"


def render(word1):
    body = store(FB_RENDER_CFG, 1)
    for k, w in enumerate([POLY0, word1, 0, 0, 0, 0, 0, 0]):
        body += store(TA + 4 * k, w)
    return body + store(STARTRENDER, 0)


def f32(v):
    return struct.unpack(">I", struct.pack(">f", v))[0]


def ta(words):
    """One 8-word TA command; the store at offset 0x1c submits it."""
    out = []
    for k, w in enumerate(words):
        out += store(TA + 4 * k, w)
    return out


def header(zoff, tex=None):
    """A polygon header, list type 0: packed colour, or textured (word 0 bit 3) with word 3 = RGB565 (pixel format 1),
    not twiddled (bit 26), texture address tex >> 3; 8 x 8 texels.  zoff sets word 1 bit 26 (Z-write disabled)."""
    w0 = POLY0 | (8 if tex is not None else 0)
    w3 = (0x0c000000 | (tex >> 3)) if tex is not None else 0
    return ta([w0, ZW_OFF if zoff else 0, FOG2, w3, 0, 0, 0, 0])


def tri(pts, z, rgb=0):
    """Three vertices, end of strip on the last; rgb is the packed colour (word 6), u = v = 0 for a textured header."""
    out = []
    for i, (x, y) in enumerate(pts):
        out += ta([VTX_EOS if i == 2 else VTX, f32(x), f32(y), f32(z), 0, 0, rgb, 0])
    return out


def texels():
    return store(VRAM + TEXEL_LINEAR[TEX_RED], RED) + store(VRAM + TEXEL_LINEAR[TEX_GREEN], GREEN)


def psession(name, body, pixels):
    """A render session that reads `pixels` back through the linear VRAM window, one 32-bit guest load each, in order.  Returns
    ({pixel: value or None}, text, how).  Only register-dump lines count: the debugger also echoes each r8=... command."""
    for p in pixels:
        x, y = PIX[p]
        body = body + ["r7=0x%x" % (VRAM + ((y * 640 + x) & ~1) * 2), "pc=0x%x" % (CODE + 4), "step 1", "reg"]
    _, t, how = session(name, body)
    vals = [int(m.group(1), 16) for m in re.finditer(r"^cpu0: .*?\br8 +=\s*(0x[0-9a-fA-F]+)", t, re.M)]
    #  a 32-bit load at an even pixel: little-endian, so an odd pixel is the high half
    half = lambda v, x: ((v >> 16) if x & 1 else v) & 0xffff
    return {p: (half(vals[i], PIX[p][0]) if i < len(vals) else None) for i, p in enumerate(pixels)}, t, how


def px(v):
    return "none" if v is None else "0x%04x" % v


print("pvrrenderexit RUNG-3 WITNESS -- binary=%s label=%s" % (BIN, LABEL))
print("machine: -E dreamcast (UNMODIFIED in-tree); guest mov.l stores at 0x%x" % CODE)
print("%-18s %-20s %-20s %-46s %s" % ("row", "got", "want", "note", ""))
t0 = time.time()

nr, _, nhow = session("neg", ["r7=0x%x" % PVR_ID, "pc=0x%x" % (CODE + 4), "step 1"], machine="nosuchmachine", timeout=30)
row("neg apparatus", "%s/%s" % (nhow, hex(nr["r8"]) if "r8" in nr else "none"), "exit1/none", "a bogus machine runs no guest", control=True)
r, T, how = session("id", ["r7=0x%x" % PVR_ID, "pc=0x%x" % (CODE + 4), "step 1"])
row("id session", how, "exit0", "mov.l @r7,r8 from the PVR ID register", control=True)
row("id r8", hex(r["r8"]) if "r8" in r else "none", hex(0x17fd11db), "the device answers (RAM would not)", control=True)
r, T, how = session("zon", render(0))
row("zon session", how, "exit0", "Z-write ENABLED render: survives", control=True)
row("zon rendered", "yes" if RENDERED in T else "no", "yes", "the renderer saw the one TA command", control=True)
row("zon prompt", prompt(T), "yes", "the debugger ran `reg` afterwards", control=True)
r, T, how = session("zoff", render(ZW_OFF))
row("zoff rendered", "yes" if RENDERED in T else "no", "yes", "the render was reached (both builds)", control=True)
row("zoff session", how, "exit0", "Z-write DISABLED render: survives")
row("zoff prompt", prompt(T), "yes", "the debugger ran `reg` afterwards")

# ---- THE DEPTH-TEST CHANNEL (cloud Fable 5.1's ruling, rows R2-R5; R6-R8 from PRETABLE.out's joint cells; R9 and R10 from its addenda 6 and 7).  One cold
# ---- session each: FB_RENDER_CFG = 1, the polygon headers and vertices as real guest stores, STARTRENDER, then pixels read back.
CFG = store(FB_RENDER_CFG, 1)
GO = store(STARTRENDER, 0)
P, T, how = psession("ovoff", CFG + header(True) + tri(T1, 2.0, 0xff0000) + header(False) + tri(T2, 1.0, 0x00ff00) + GO,
                     ["overlap", "t2 only", "t1 only", "bg"])
row("ovoff session", how, "exit0", "R2: T1 Z-off red, T2 green behind it")
row("ovoff overlap", px(P["overlap"]), px(GREEN), "T1 stored no depth, so T2 draws over it")
row("ovoff t2 only", px(P["t2 only"]), px(GREEN), "T2 drawn")
row("ovoff t1 only", px(P["t1 only"]), px(RED), "T1 drawn (not declined)")
row("ovoff bg", px(P["bg"]), px(BLACK), "the frame was cleared")
P, T, how = psession("ovon", CFG + header(False) + tri(T1, 2.0, 0xff0000) + header(False) + tri(T2, 1.0, 0x00ff00) + GO,
                     ["overlap", "t2 only", "t1 only", "bg"])
row("ovon overlap", px(P["overlap"]), px(RED), "R3: both Z-on: T1's depth hides T2")
row("ovon t2 only", px(P["t2 only"]), px(GREEN), "T2 drawn", control=True)
row("ovon t1 only", px(P["t1 only"]), px(RED), "T1 drawn", control=True)
row("ovon bg", px(P["bg"]), px(BLACK), "the frame was cleared", control=True)
P, T, how = psession("behind", CFG + header(False) + tri(T1, 2.0, 0xff0000) + header(True) + tri(T2, 1.0, 0x00ff00) + GO,
                     ["overlap", "t2 only", "t1 only"])
row("behind session", how, "exit0", "R6: T1 Z-on red, T2 Z-off green behind")
row("behind overlap", px(P["overlap"]), px(RED), "a Z-off T2 still fails the depth test")
row("behind t2 only", px(P["t2 only"]), px(GREEN), "T2 drawn where it passes")
row("behind t1 only", px(P["t1 only"]), px(RED), "T1 drawn")
P, T, how = psession("texoff", CFG + texels() + header(True, TEX_RED) + tri(T1, 2.0) + header(False) + tri(T2, 1.0, 0x00ff00) + GO,
                     ["overlap", "t1 only", "t2 only"])
row("texoff session", how, "exit0", "R4: T1 textured Z-off (red texel)")
row("texoff overlap", px(P["overlap"]), px(GREEN), "texturedline stored no depth for T1")
row("texoff t1 only", px(P["t1 only"]), px(RED), "T1 drawn from its texel")
row("texoff t2 only", px(P["t2 only"]), px(GREEN), "T2 drawn")
P, T, how = psession("texbeh", CFG + texels() + header(False, TEX_RED) + tri(T1, 2.0) + header(True, TEX_GREEN) + tri(T2, 1.0) + GO,
                     ["overlap", "t2 only", "t1 only"])
row("texbeh session", how, "exit0", "R7: textured T1 Z-on, textured T2 Z-off")
row("texbeh overlap", px(P["overlap"]), px(RED), "textured Z-off T2 fails the depth test")
row("texbeh t2 only", px(P["t2 only"]), px(GREEN), "T2 drawn from its texel")
row("texbeh t1 only", px(P["t1 only"]), px(RED), "T1 drawn from its texel")
P, T, how = psession("texon", CFG + texels() + header(False, TEX_RED) + tri(T1, 2.0) + header(False, TEX_GREEN) + tri(T2, 1.0) + GO,
                     ["overlap", "t2 only"])
row("texon overlap", px(P["overlap"]), px(RED), "R7: both textured Z-on: T1 hides T2")
row("texon t2 only", px(P["t2 only"]), px(GREEN), "T2 drawn from its texel", control=True)
P, T, how = psession("two", CFG + header(True) + tri(AWAY, 2.0, 0xff0000) + GO + tri(T1, 2.0, 0xff0000) + tri(T2, 1.0, 0x00ff00) + GO,
                     ["overlap", "t1 only", "t2 only"])
row("two session", how, "exit0", "R5: a Z-off render, then bare vertices")
row("two overlap", px(P["overlap"]), px(RED), "render 2 has no header: Z-write is on")
row("two t1 only", px(P["t1 only"]), px(RED), "headerless vertices draw")
row("two t2 only", px(P["t2 only"]), px(GREEN), "T2 drawn")
P, T, how = psession("sticky", CFG + header(True) + header(False) + tri(T1, 2.0, 0x00ff00) + tri(T2, 1.0, 0x0000ff) + GO,
                     ["overlap", "t2 only"])
row("sticky session", how, "exit0", "R8: a Z-off header, then a Z-on one")
row("sticky overlap", px(P["overlap"]), px(GREEN), "the Z-on header re-enabled the store")
row("sticky t2 only", px(P["t2 only"]), px(BLUE), "the blue triangle drawn")
P, T, how = psession("edges", CFG + header(False) + tri(LEFT, 2.0, 0xff0000) + tri(RIGHT, 2.0, 0xff0000)
                     + tri(RSPAN, 2.0, 0xff0000) + GO, ["l in", "l out", "r in", "r out", "rspan"])
row("edges l in", px(P["l in"]), px(RED), "R9: column 1 drawn (pins x > 0 from above)")
row("edges l out", px(P["l out"]), px(BLACK), "column 0 not drawn (x > 0 from below)")
row("edges r in", px(P["r in"]), px(RED), "column 639 drawn (x < xsize from below)")
row("edges r out", px(P["r out"]), px(BLACK), "x = 640 not wrapped onto row 331")
row("edges rspan", px(P["rspan"]), px(RED), "a span from x = 639.0 draws column 639")
P, T, how = psession("texedges", CFG + texels() + header(False, TEX_RED) + tri(LEFT, 2.0) + tri(RIGHT, 2.0) + tri(RSPAN, 2.0) + GO,
                     ["l in", "l out", "r in", "r out", "rspan"])
row("texedges l in", px(P["l in"]), px(RED), "R9 textured: column 1 drawn")
row("texedges l out", px(P["l out"]), px(BLACK), "column 0 not drawn")
row("texedges r in", px(P["r in"]), px(RED), "column 639 drawn")
row("texedges r out", px(P["r out"]), px(BLACK), "x = 640 not wrapped onto row 331")
row("texedges rspan", px(P["rspan"]), px(RED), "textured: column 639 from x = 639")
# ---- R10 (addendum 7): the depth compare's EQUAL edge.  Z-on T1 then Z-on T2 at the SAME z: under `<=` the later polygon wins.
P, T, how = psession("equal", CFG + header(False) + tri(T1, 2.0, 0xff0000) + header(False) + tri(T2, 2.0, 0x00ff00) + GO,
                     ["overlap", "t2 only"])
row("equal overlap", px(P["overlap"]), px(GREEN), "R10: equal z, the later polygon wins (<=)")
row("equal t2 only", px(P["t2 only"]), px(GREEN), "T2 drawn", control=True)
P, T, how = psession("texequal", CFG + texels() + header(False, TEX_RED) + tri(T1, 2.0) + header(False, TEX_GREEN) + tri(T2, 2.0) + GO,
                     ["overlap", "t2 only"])
row("texequal overlap", px(P["overlap"]), px(GREEN), "R10 textured: equal z, the later wins")
row("texequal t2 only", px(P["t2 only"]), px(GREEN), "T2 drawn from its texel", control=True)
# ---- the class closure (repair 2; the pass-2 adjudication).  Both rasterizers' y early return (TOP reaches row 0; BOTTOM row 479
# and, past the frame, row 480), the x1 > x2 swap (SWAP arrives reversed) and the span end at an EXACT integer (SWAP's slopes are
# +-0.5, so its row-180 span is exactly 365.0..435.0: `x < x2` drops pixel 435, `x <= x2 + 1` adds 436).
GEO = ["t in", "b in", "b out", "swap", "s end", "s past"]
P, T, how = psession("yedges", CFG + header(False) + tri(TOP, 2.0, 0xff0000) + tri(BOTTOM, 2.0, 0xff0000)
                     + tri(SWAP, 2.0, 0xff0000) + GO, GEO)
row("yedges t in", px(P["t in"]), px(RED), "row 0 drawn (y < 0 from above)")
row("yedges b in", px(P["b in"]), px(RED), "row 479 drawn (y >= ysize from below)")
row("yedges b out", px(P["b out"]), px(BLACK), "row 480 not drawn (past the frame)")
row("yedges swap", px(P["swap"]), px(RED), "a reversed span is swapped and drawn")
row("yedges s end", px(P["s end"]), px(RED), "span end x2 = 435.0 drawn (x <= x2)")
row("yedges s past", px(P["s past"]), px(BLACK), "x2 + 1 not drawn")
P, T, how = psession("texyedges", CFG + texels() + header(False, TEX_RED) + tri(TOP, 2.0) + tri(BOTTOM, 2.0) + tri(SWAP, 2.0) + GO,
                     GEO)
row("texyedges t in", px(P["t in"]), px(RED), "textured: row 0 drawn")
row("texyedges b in", px(P["b in"]), px(RED), "textured: row 479 drawn")
row("texyedges b out", px(P["b out"]), px(BLACK), "textured: row 480 not drawn")
row("texyedges swap", px(P["swap"]), px(RED), "textured: a reversed span drawn")
row("texyedges s end", px(P["s end"]), px(RED), "textured: span end 435 drawn")
row("texyedges s past", px(P["s past"]), px(BLACK), "textured: x2 + 1 not drawn")
# ---- the decode mask's two edges (repair 2): word 1 bit 26 is Z-write disable.  A header with bit 27 set (culling mode 1, which
# culls nothing) and one with bit 25 set (texture1, which the renderer decodes and ignores) must both still store depth: T2 (green,
# z 1.0) lies behind T1 (red, z 2.0).  One header per session: a session sending sixteen TA commands outran the 90 s session limit.
P, T, how = psession("mask", CFG + ta([POLY0, MASK27, FOG2, 0, 0, 0, 0, 0]) + tri(T1, 2.0, 0xff0000) + header(False)
                     + tri(T2, 1.0, 0x00ff00) + GO, ["overlap", "t2 only"])
row("mask overlap", px(P["overlap"]), px(RED), "a bit-27 header still stores depth")
row("mask t2 only", px(P["t2 only"]), px(GREEN), "T2 drawn", control=True)
P, T, how = psession("mask25", CFG + ta([POLY0, MASK25, FOG2, 0, 0, 0, 0, 0]) + tri(T1, 2.0, 0xff0000) + header(False)
                     + tri(T2, 1.0, 0x00ff00) + GO, ["overlap"])
row("mask25 overlap", px(P["overlap"]), px(RED), "a bit-25 header still stores depth")

n_ok = sum(1 for _, ok in rows if ok)
red = [n for n, ok in rows if not ok]
print("elapsed %.1fs" % (time.time() - t0))
print("PVR_ZWRITE_RESULT=%d/%d" % (n_ok, len(rows)))
print("PVR_ZWRITE_CONTROL=%s" % ("OK" if all(ok for _, ok in controls) else "FAIL"))
print("PVR_ZWRITE_SYMPTOM=%s" % ("PRESENT" if symptom_hits else "ABSENT"))
print("PVR_ZWRITE_RED=%s" % (",".join(n.replace(" ", "_") for n in red) if red else "none"))
print("PVR_ZWRITE_PROBE_DONE")
