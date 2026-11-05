#!/usr/bin/env python3
"""traodd_witness.py <gxemul> [label] [pc] -- qhslowifetch pass 5, Mythos breach 2 (MYTHOS.md / MYTHOS_r2.md): arm (a)'s read-ahead
guard conjoined with an alignment test (`&& cpu->pc == addr`, or `&& !(cpu->pc & 3)`) is green on all 79 rows because every measured
read-ahead starts from an aligned pc.  This is `T ra` (a -T continue from cpc700_pci's last word, 0xfec00004, whose translation reads
ahead into 0xfec00008 past the window; no breakpoint, so read-ahead runs) entered at the UNALIGNED pc 0xfec00005: the prologue keeps
pc's low two bits, so the read-ahead fetch reaches the failure block with pc != addr.  The fix's arm (a) returns and the real fetch
halts again (two reports); a conjoined guard sends the read-ahead failure on to arm (c), which parks it (one report).  Prints pc, the
halt-report count, the halted addresses, SRR0, MSR and any checkstop or UNIMPLEMENTED text."""
import os
import re
import subprocess
import sys
import tempfile

BIN = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "local"
PC = int(sys.argv[3], 16) if len(sys.argv) > 3 else 0xfec00005
d = tempfile.mkdtemp(prefix="traodd_")
NOP = os.path.join(d, "nop.bin")
open(NOP, "wb").write(bytes([0x60, 0x00, 0x00, 0x00]))
cmds = ["srr0=0x11111111", "pc=0x%x" % PC, "continue", "reg", "quit"]
argv = [BIN, "-V", "-x", "-E", "pmppc", "-T", "0x2000:%s" % NOP]
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


addrs = ",".join(sorted(set(re.findall(r"non-existant paddr=(0x[0-9a-fA-F]+)", t)))) or "none"
print("TRAODD %s/0x%x how=%s pc=%s nonex=%d addrs=%s srr0=%s msr=%s chkstop=%s unimpl=%s" % (
    LABEL, PC, how, reg("pc"), t.count("non-existant"), addrs, reg("srr0"), reg("msr"), "checkstop" in t, "UNIMPLEMENTED" in t))
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "traodd_%s_0x%x.txt" % (LABEL, PC)), "w", encoding="latin-1").write(
    "$ " + " ".join(argv) + "\n--- stdin ---\n" + "\n".join(cmds) + "\n--- transcript (%s) ---\n" % how + t)
print("TRAODD_DONE")
