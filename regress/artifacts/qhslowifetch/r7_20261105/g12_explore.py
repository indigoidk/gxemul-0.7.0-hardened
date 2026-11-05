#!/usr/bin/env python3
"""g12_explore.py <gxemul> <label> <outdir> -- the coordinator's G1 question, "check what the isi session's setup allows": can the
probe's ISI route put pc ABOVE the failing addr after an exception, so that arm (b)'s `pc < addr` (G1) and the fix's aligned compare
disagree?  Two sessions on the `isi` setup with MSR[IP] added (msr = IR | IP = 0x60: exceptions vector to 0xfff00000 + offset, so
the ISI vector 0xfff00400 is above the BAT-gap fetch 0x20000000): X1 continue, X2 one step.  Prints the exit status, pc, SRR0, MSR,
the halt-report and exception-entry counts, the checkstop/UNIMPLEMENTED/handler-lookup texts and the last lines; transcripts go to
<outdir>/explore_<label>_<name>.txt."""
import os
import re
import subprocess
import sys
import tempfile

BIN, LABEL, OUTD = sys.argv[1], sys.argv[2], sys.argv[3]
d = tempfile.mkdtemp(prefix="g12x_")
NOP = os.path.join(d, "nop.bin")
open(NOP, "wb").write(bytes([0x60, 0x00, 0x00, 0x00]))
os.makedirs(OUTD, exist_ok=True)
SESS = [("X1_ip_cont", ["srr0=0x11111111", "msr=0x60", "pc=0x20000000", "continue"]),
        ("X2_ip_step", ["srr0=0x11111111", "msr=0x60", "pc=0x20000000", "step 1"])]
for name, cmds in SESS:
    allc = cmds + ["reg", "quit"]
    argv = [BIN, "-V", "-x", "-E", "pmppc", "0x2000:%s" % NOP]
    try:
        p = subprocess.run(argv, input=("\n".join(allc) + "\n").encode(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60)
        t = p.stdout.decode("latin-1", "replace").replace("\r", "")
        how = ("sig%d" % -p.returncode) if p.returncode < 0 else ("exit%d" % p.returncode)
    except subprocess.TimeoutExpired as e:
        t = (e.output or b"").decode("latin-1", "replace").replace("\r", "")
        how = "TIMEOUT"
    seg = t[t.rfind("GXemul> reg"):] if "GXemul> reg" in t else ""

    def reg(k):
        m = re.search(r"\b%s\s*=\s*(0x[0-9a-fA-F]+)" % k, seg)
        return hex(int(m.group(1), 16)) if m else "none"

    last = " | ".join([x for x in t.split("\n") if x.strip()][-3:])
    print("EXPLORE %-5s %s how=%s pc=%s srr0=%s msr=%s nonex=%d exc=%d chkstop=%s unimpl=%s handler_fatal=%s" % (
        LABEL, name, how, reg("pc"), reg("srr0"), reg("msr"), t.count("non-existant"), t.count("[ PPC Exception"),
        "checkstop" in t, "UNIMPLEMENTED" in t, "could not find physical" in t))
    print("   last: %s" % last[:300])
    open(os.path.join(OUTD, "explore_%s_%s.txt" % (LABEL, name)), "w", encoding="latin-1").write(
        "$ " + " ".join(argv) + "\n--- stdin ---\n" + "\n".join(allc) + "\n--- transcript (%s) ---\n" % how + t)
print("EXPLORE_DONE")
