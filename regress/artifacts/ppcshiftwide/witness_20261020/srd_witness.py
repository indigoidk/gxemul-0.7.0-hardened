#!/usr/bin/env python3
"""srd_witness.py <gxemul> -- rung-3 witness: PowerPC srd / srad / sradi (64-bit shifts in Book I v2.01) have no decoder
case in cpu_ppc_instr.c at HEAD, so a guest executing one reaches cpu_dyntrans.c's `bad:` ("Abort the emulation").
Unmodified -E bareppc (default CPU PPC970, 64-bit).  One session per instruction (each is expected to stop the run);
each session executes a liveness `ori` first, then the shift, then a second `ori` whose result proves execution
continued.  Control: `sld` (decoded) in its own session must run and give the Book I value."""
import os, re, subprocess, sys, tempfile

BIN = sys.argv[1]
TMP = tempfile.mkdtemp(prefix="srdwit_")
DUMMY = os.path.join(TMP, "dummy.bin")
open(DUMMY, "wb").write(b"\0\0\0\0")
CODE = 0x10000
ORI = lambda ra, rs, imm: ((24 << 26) | (rs << 21) | (ra << 16) | (imm & 0xFFFF))
X = lambda rs, ra, rb, xo: ((31 << 26) | (rs << 21) | (ra << 16) | (rb << 11) | (xo << 1)) & 0xFFFFFFFF
XS = lambda rs, ra, sh, xo: ((31 << 26) | (rs << 21) | (ra << 16) | ((sh & 31) << 11) | (xo << 2) | (((sh >> 5) & 1) << 1)) & 0xFFFFFFFF
CASES = [("sld ctl", X(3, 4, 5, 27), 0x0000000123456780 << 0),     # sld r4,r3,r5 ; r5 = 4 -> r3 << 4
         ("srd", X(3, 4, 5, 539), None),
         ("srad", X(3, 4, 5, 794), None),
         ("sradi", XS(3, 4, 4, 413), None)]


def run(word):
    cmds = ["r3=0x12345678", "r5=4", "r4=0x5a5a", "r15=0x0", "r16=0x0",
            "put w 0x%x, 0x%08x" % (CODE, ORI(15, 0, 0x1234)), "put w 0x%x, 0x%08x" % (CODE + 4, word),
            "put w 0x%x, 0x%08x" % (CODE + 8, ORI(16, 0, 0x5678)),
            "unassemble 0x%x 0x%x" % (CODE, CODE + 12), "pc=0x%x" % CODE, "step 3", "reg", "quit"]
    argv = [BIN, "-V", "-x", "-E", "bareppc", "-M", "64", "0x%x:%s" % (CODE, DUMMY)]
    p = subprocess.run(argv, input=("\n".join(cmds) + "\n").encode(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
    t = p.stdout.decode("latin-1", "replace").replace("\r", "")
    idx = t.rfind("GXemul> reg")
    regs = {int(m.group(1)): int(m.group(2), 16) for m in re.finditer(r"\br(\d\d) = (0x[0-9a-fA-F]+)", t[idx:])} if idx >= 0 else {}
    return p.returncode, regs, t


print("srd_witness -- binary=%s" % BIN)
for name, word, want in CASES:
    rc, r, t = run(word)
    dis = re.findall(r"^[0-9a-f]+: %08x\s+(.*)$" % word, t, re.M)
    stopped = any(k in t for k in ("UNIMPLEMENTED", "unimplemented", "All machines stopped", "TODO"))
    print("== %-6s word 0x%08x rc=%d disasm=%r r15=%s r16=%s r4=%s stop-text=%s" % (
        name, word, rc, dis[:1], hex(r[15]) if 15 in r else None, hex(r[16]) if 16 in r else None,
        hex(r[4]) if 4 in r else None, stopped))
    for line in t.split("\n"):
        if any(k in line for k in ("UNIMPLEMENTED", "unimplemented", "All machines stopped", "TODO", "fatal")):
            print("     | " + line.strip()[:150])
print("SRD_WITNESS_DONE")
