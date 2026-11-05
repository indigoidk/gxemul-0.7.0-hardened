#!/usr/bin/env python3
"""blr_witness.py (derived from p3_20261105/dhalt_witness.py) <gxemul> [label] -- qhslowifetch pass 3: does a SUCCESSFUL slow-path instruction fetch happen with running == 0?
glm-5.3's finding (A) (p3_20261105/ollama_glm.txt): the fix's failure test widened to `!memory_rw(...) || !cpu->running` keeps all
62 rows green, because every measured successful fetch runs with running == 1.  This session makes one that does not: on an
UNMODIFIED -E pmppc, with -T and a breakpoint set far away (a set breakpoint disables translation read-ahead, cpu_dyntrans.c),
the guest runs `lwz r3,0(r4)` with r4 past RAM (the -T halt clears running inside that load's memory_rw), then `addi r5,r5,1` at
0x2004, whose slot is translated only when reached -- AFTER the halt.  The program is written with `put b` (byte stores do not
warm translations).  Prints the observables a row would read: pc, r5, srr0, the halt-report count, UNIMPLEMENTED text."""
import re
import subprocess
import sys
import tempfile
import os

BIN = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "local"
d = tempfile.mkdtemp(prefix="dhalt_")
NOP = os.path.join(d, "nop.bin")
open(NOP, "wb").write(bytes([0x60, 0x00, 0x00, 0x00]))
MODE = sys.argv[3] if len(sys.argv) > 3 else "ld"
prog = [0x7C6803A6, 0x4E800020]   # mtlr r3 ; blr  (guest-made unaligned pc: r3 = 0x02040001)
cmds = ["srr0=0x11111111", "r3=0x%x" % int(MODE, 16)]
for i, w in enumerate(prog):
    for j in range(4):
        cmds.append("put b 0x%x,0x%02x" % (0x2000 + 4 * i + j, (w >> (24 - 8 * j)) & 0xff))
cmds += ["breakpoint add 0x3000", "continue", "reg", "quit"]
NOT = len(sys.argv) > 4 and sys.argv[4] == "noT"
argv = [BIN, "-V", "-x", "-E", "pmppc"] + ([] if NOT else ["-T"]) + ["0x2000:%s" % NOP]
try:
    p = subprocess.run(argv, input=("\n".join(cmds) + "\n").encode(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60)
    t = p.stdout.decode("latin-1", "replace").replace("\r", "")
    how = "exit%d" % p.returncode
except subprocess.TimeoutExpired as e:
    t = (e.output or b"").decode("latin-1", "replace")
    how = "TIMEOUT"
seg = t[t.rfind("GXemul> reg"):] if "GXemul> reg" in t else ""
def reg(k):
    m = re.search(r"\b%s\s*=\s*(0x[0-9a-fA-F]+)" % k, seg)
    return m.group(1) if m else "none"
print("BLR %s/%s%s how=%s pc=%s lr=%s srr0=%s nonex=%d unimpl=%s chkstop=%s put_ok=%s bp_ok=%s" % (
    LABEL, MODE, "/noT" if NOT else "", how, reg("pc"), reg("lr"), reg("srr0"), t.count("non-existant"), "UNIMPLEMENTED" in t, "checkstop" in t,
    "put" not in t.lower().split("usage")[0][-1:] , "reakpoint" in t))
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "blr_%s_%s%s.txt" % (LABEL, MODE, "_noT" if NOT else "")), "w", encoding="latin-1").write(
    "$ " + " ".join(argv) + "\n--- stdin ---\n" + "\n".join(cmds) + "\n--- transcript (%s) ---\n" % how + t)
print("BLR_DONE")
