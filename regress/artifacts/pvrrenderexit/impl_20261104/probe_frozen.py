#!/usr/bin/env python3
"""pvrrenderexit -- RUNG-3 WITNESS for the Dreamcast PVR renderer's Z-write-disable exit.

DEFECT (filed 2026-10-02).  src/devices/dev_pvr.c, pvr_render(): a STARTRENDER write renders the Tile Accelerator commands the
guest submitted; for a polygon header whose list word 1 has bit 26 set (Z-write DISABLED, `zwrite = !((list[1] >> 26) & 1)`)
the renderer prints "pvr: no zwrite? not implemented yet." and calls exit(1) -- the emulator process ends.

WHAT THE ROWS MEASURE (2026-11-04, `-E dreamcast`, an UNMODIFIED in-tree machine; one cold debugger session per case).  Every
device access is a REAL guest instruction through the SH-4 decoder and memory_rw: `mov.l r8,@r7` (0x2782) and `mov.l @r7,r8`
(0x6872) are placed at CODE with `put w`, and each store is r7 = address, r8 = value, PC = CODE, one `step`.  A render session
writes FB_RENDER_CFG = 1 (RGB565: P2 0xa05f8048), the eight words of ONE polygon header to the TA (P2 0xb0000000..0xb000001c; the
write at offset 0x1c submits the command), then STARTRENDER (0xa05f8014), which renders synchronously inside that store.
CONTROL rows: the PVR ID register reads 0x17fd11db through a guest load (RAM would not), a render with Z-write ENABLED runs to the
end (the device reports "1 Tile Accelerator commands") and the process survives, and a bogus machine runs nothing.  WITNESS rows:
the same render with Z-write DISABLED must leave the process alive with the debugger prompt back.  On the pre-fix build that session
ends with the renderer's text and exit status 1 (PVR_ZWRITE_SYMPTOM=PRESENT).

NOT CLAIMED (owed when the design is ruled): what a Z-write-disabled polygon draws (the depth-test channel needs vertices and a pixel
read-back -- the witness-brief design has seventeen commands for it), whether a once-latched announce prints, the three sibling exits
(texture pixel format, a non-RGB565 render mode, an unimplemented list command), and a render with more than one command.

Sentinel: PVR_ZWRITE_PROBE_DONE (plus PVR_ZWRITE_RESULT=n/N, _CONTROL=OK|FAIL, _SYMPTOM=PRESENT|ABSENT, _RED=none|<names>).
Session transcripts go to the optional [workdir].
"""

import os
import re
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
RENDERED = "1 Tile Accelerator commands"

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
row("zoff rendered", "yes" if RENDERED in T else "no", "yes", "the render was reached (both builds)")
row("zoff session", how, "exit0", "Z-write DISABLED render: survives")
row("zoff prompt", prompt(T), "yes", "the debugger ran `reg` afterwards")

n_ok = sum(1 for _, ok in rows if ok)
red = [n for n, ok in rows if not ok]
print("elapsed %.1fs" % (time.time() - t0))
print("PVR_ZWRITE_RESULT=%d/%d" % (n_ok, len(rows)))
print("PVR_ZWRITE_CONTROL=%s" % ("OK" if all(ok for _, ok in controls) else "FAIL"))
print("PVR_ZWRITE_SYMPTOM=%s" % ("PRESENT" if symptom_hits else "ABSENT"))
print("PVR_ZWRITE_RED=%s" % (",".join(n.replace(" ", "_") for n in red) if red else "none"))
print("PVR_ZWRITE_PROBE_DONE")
