#!/usr/bin/env python3
"""cell_witness.py <gxemul> <label> <pc> [msr] [outdir] -- qhslowifetch pass 6 (codex GPT-6 Astra, p6_20261105/codex_codex_qhs_p6.txt):
p5_20261105/traodd_witness.py with an MSR argument and an output directory.  `T ra` -- a -T continue from cpc700_pci's last word,
whose translation reads ahead into 0xfec00008 past the 8-byte window; no breakpoint, so read-ahead runs -- entered at <pc> (0xfec00004
.. 0xfec00007: pc's low two bits 00, 01, 10, 11) with MSR = <msr> (0 or 0x1000, MSR[ME]).  MSR is written only when nonzero, as the
probe's `T ra' / `T ra odd' sessions leave the reset value 0.  The prologue keeps pc's low two bits, so the read-ahead fetch reaches
the failure block at pc = 0xfec00008 | (<pc> & 3).  Prints pc, the halt-report count, the halted addresses, SRR0, MSR and any
checkstop or UNIMPLEMENTED text; the transcript goes to <outdir>/cell_<label>_<pc>_<msr>.txt."""
import os
import re
import subprocess
import sys
import tempfile

BIN = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "local"
PC = int(sys.argv[3], 16) if len(sys.argv) > 3 else 0xfec00005
MSR = int(sys.argv[4], 16) if len(sys.argv) > 4 else 0
OUTD = sys.argv[5] if len(sys.argv) > 5 else os.path.dirname(os.path.abspath(__file__))
d = tempfile.mkdtemp(prefix="cellw_")
NOP = os.path.join(d, "nop.bin")
open(NOP, "wb").write(bytes([0x60, 0x00, 0x00, 0x00]))
cmds = ["srr0=0x11111111"] + (["msr=0x%x" % MSR] if MSR else []) + ["pc=0x%x" % PC, "continue", "reg", "quit"]
argv = [BIN, "-V", "-x", "-E", "pmppc", "-T", "0x2000:%s" % NOP]
try:
    p = subprocess.run(argv, input=("\n".join(cmds) + "\n").encode(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60)
    t = p.stdout.decode("latin-1", "replace").replace("\r", "")
    how = ("sig%d" % -p.returncode) if p.returncode < 0 else ("exit%d" % p.returncode)
except subprocess.TimeoutExpired as e:
    t = (e.output or b"").decode("latin-1", "replace").replace("\r", "")
    how = "TIMEOUT"
seg = t[t.rfind("GXemul> reg"):] if "GXemul> reg" in t else ""


def reg(k):
    m = re.search(r"\b%s\s*=\s*(0x[0-9a-fA-F]+)" % k, seg)
    return hex(int(m.group(1), 16)) if m else "none"


addrs = ",".join(sorted(set(re.findall(r"non-existant paddr=(0x[0-9a-fA-F]+)", t)))) or "none"
print("CELL %-5s pc0=0x%x msr0=0x%x how=%s pc=%s nonex=%d addrs=%s srr0=%s msr=%s chkstop=%s unimpl=%s" % (
    LABEL, PC, MSR, how, reg("pc"), t.count("non-existant"), addrs, reg("srr0"), reg("msr"), "checkstop" in t, "UNIMPLEMENTED" in t))
os.makedirs(OUTD, exist_ok=True)
open(os.path.join(OUTD, "cell_%s_0x%x_0x%x.txt" % (LABEL, PC, MSR)), "w", encoding="latin-1").write(
    "$ " + " ".join(argv) + "\n--- stdin ---\n" + "\n".join(cmds) + "\n--- transcript (%s) ---\n" % how + t)
print("CELL_DONE")
