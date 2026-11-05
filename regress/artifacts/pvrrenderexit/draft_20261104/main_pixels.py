#!/usr/bin/env python3
"""main_pixels.py <gxemul> <label> <zwrite_t1: on|off> [workdir] -- the PIXEL CHANNEL for pvrrenderexit, measured by the main loop
(2026-11-04) after the m_pvr seat stopped on a classifier refusal.  One cold `-E dreamcast` debugger session: every device access a real
SH-4 `mov.l` (store `mov.l r8,@r7` at CODE, load `mov.l @r7,r8` at CODE+4).  Renders, in ONE Tile Accelerator list, a NEAR red triangle
T1 (z = 2.0; the renderer keeps the larger z, `vram_z[ofs] <= z`) and then a FAR green triangle T2 (z = 1.0) that overlaps it, then reads
four framebuffer pixels back through the linear VRAM window (P2 0xa5000000 + fb_base + (y*640 + x)*2, RGB565, little-endian halves).
zwrite_t1 = off sets list word 1 bit 26 on T1's header (Z-write disabled).  Prints one line per pixel and PIXELS_DONE."""
import os
import re
import struct
import subprocess
import sys
import tempfile

BIN, LABEL, ZW = sys.argv[1], sys.argv[2], sys.argv[3]
WORK = sys.argv[4] if len(sys.argv) > 4 else None
d = tempfile.mkdtemp(prefix="pvrpix_")
DUMMY = os.path.join(d, "dummy.bin")
open(DUMMY, "wb").write(bytes(4))
CODE = 0x8c010000
TA = 0xb0000000
VRAM = 0xa5000000


def f32(v):
    return struct.unpack(">I", struct.pack(">f", v))[0]


def store(a, v):
    return ["r7=0x%x" % a, "r8=0x%x" % v, "pc=0x%x" % CODE, "step 1"]


def command(words):
    out = []
    for k, w in enumerate(words):
        out += store(TA + 4 * k, w)
    return out


def triangle(pts, z, rgb, zwrite_off):
    hdr = [0x80000000, 0x04000000 if zwrite_off else 0, 0x00800000, 0, 0, 0, 0, 0]   # cmd 4, list 0, packed colour; fog 2
    cmds = command(hdr)
    for i, (x, y) in enumerate(pts):
        w0 = 0xF0000000 if i == 2 else 0xE0000000                                     # vertex; end of strip on the last
        cmds += command([w0, f32(x), f32(y), f32(z), 0, 0, rgb, 0])
    return cmds


T1 = [(100.0, 100.0), (300.0, 100.0), (200.0, 300.0)]
T2 = [(150.0, 150.0), (350.0, 150.0), (250.0, 350.0)]
PIX = [("overlap", 220, 180), ("t2 only", 320, 180), ("t1 only", 120, 120), ("background", 10, 10)]

cmds = ["put w 0x%x, 0x00092782" % CODE, "put w 0x%x, 0x00096872" % (CODE + 4)]
cmds += store(0xa05f8048, 1)                                                          # FB_RENDER_CFG: RGB565
cmds += triangle(T1, 2.0, 0x00FF0000, ZW == "off")                                    # near, red
cmds += triangle(T2, 1.0, 0x0000FF00, False)                                          # far, green
cmds += store(0xa05f8014, 0)                                                          # STARTRENDER
for name, x, y in PIX:
    cmds += ["r7=0x%x" % (VRAM + (y * 640 + x) * 2), "pc=0x%x" % (CODE + 4), "step 1", "reg"]
cmds += ["quit"]
argv = [BIN, "-V", "-x", "-E", "dreamcast", "0x%x:%s" % (CODE, DUMMY)]
p = subprocess.run(argv, input=("\n".join(cmds) + "\n").encode(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120)
t = p.stdout.decode("latin-1", "replace").replace("\r", "")
if WORK:
    os.makedirs(WORK, exist_ok=True)
    open(os.path.join(WORK, "%s_zw%s.txt" % (LABEL, ZW)), "w", encoding="latin-1").write("$ " + " ".join(argv) + "\n" + t)
#  ONLY the register-dump lines ("cpu0: r8  = 0x..."): the debugger also ECHOES each "r8=0x..." command, and a first draft of this
#  parse read those echoes as pixels (0x0001 = the FB_RENDER_CFG value) -- even in a session that had already exited.
regs = [int(m.group(1), 16) for m in re.finditer(r"^cpu0: .*?\br8 +=\s*(0x[0-9a-fA-F]+)", t, re.M)]
print("label=%s zwrite_t1=%s exit=%d render_line=%s nozwrite_text=%s" % (LABEL, ZW, p.returncode,
      "yes" if "Tile Accelerator commands" in t else "no", "yes" if "no zwrite?" in t else "no"))
names = {0xF800: "RED (T1)", 0x07E0: "GREEN (T2)", 0x0000: "black (background)"}
for i, (name, x, y) in enumerate(PIX):
    if i < len(regs):
        px = regs[i] & 0xFFFF
        print("  %-10s (%3d,%3d) = 0x%04x  %s" % (name, x, y, px, names.get(px, "?")))
    else:
        print("  %-10s (%3d,%3d) = none (no reg output: the session ended first)" % (name, x, y))
print("PIXELS_DONE")
