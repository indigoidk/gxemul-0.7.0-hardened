#!/usr/bin/env python3
"""shift_witness.py <gxemul> -- rung-3 witness: PowerPC slw / srw / sraw with shift amounts 32..63.

PowerPC Book I v2.01 (_scratchpad/ppc_uisa_book1_v201.txt): slw :4404-4414 "The 32-bit result is placed into RA32:63.
RA0:31 are set to zero. Shift amounts from 32 to 63 give a zero result."; srw :4455 (the same rule, rightward); sraw
:4540-4551 "Shift amounts from 32 to 63 give a result of 64 sign bits, and cause CA to receive the sign bit of
(RS)32:63."  Unmodified -E bareppc (default CPU PPC970, 64-bit) and -C PPC603 (32-bit); guest instructions stepped
through the debugger; nothing in the tree changed."""
import os, re, subprocess, sys, tempfile

BIN = sys.argv[1]
TMP = tempfile.mkdtemp(prefix="shiftwit_")
DUMMY = os.path.join(TMP, "dummy.bin")
open(DUMMY, "wb").write(b"\0\0\0\0")
CODE = 0x10000


def X(rs, ra, rb, xo, rc=0):
    return ((31 << 26) | (rs << 21) | (ra << 16) | (rb << 11) | (xo << 1) | rc) & 0xFFFFFFFF


SLW, SRW, SRAW = 24, 536, 792
ORI = lambda ra, rs, imm: ((24 << 26) | (rs << 21) | (ra << 16) | (imm & 0xFFFF))
# r3 = 0x12345678 (source), r5 = 32 (shift), r10 = 4 (control shift), r8 = 0x80000001 (negative low word),
# r12 = 0xaaaaaaaa00000010 (high word set: srw must ignore it).
SEED = [(3, 0x12345678), (5, 32), (10, 4), (8, 0x80000001), (12, 0xAAAAAAAA00000010), (13, 33),
        (4, 0x5A5A), (6, 0x5A5A), (7, 0x5A5A), (9, 0x5A5A), (11, 0x5A5A), (14, 0x5A5A), (15, 0x5A5A)]
PROG = [
    ORI(15, 0, 0x1234),      # liveness: r15 = 0x1234
    X(3, 4, 5, SLW),         # slw  r4,r3,r5   shift 32   -> want 0
    X(3, 6, 5, SRW),         # srw  r6,r3,r5   shift 32   -> want 0
    X(8, 7, 5, SRAW),        # sraw r7,r8,r5   shift 32   -> want all ones, CA = 1
    X(3, 9, 10, SLW),        # slw  r9,r3,r10  shift 4    -> CONTROL want 0x23456780
    X(12, 11, 10, SRW),      # srw  r11,r12,r10 shift 4   -> want 0x1 (the high word must not leak in)
    X(3, 14, 13, SLW),       # slw  r14,r3,r13 shift 33   -> want 0
]


def session(cpu):
    cmds = ["r%d=0x%x" % (r, v) for r, v in SEED] + ["xer=0"]
    for i, w in enumerate(PROG):
        cmds.append("put w 0x%x, 0x%08x" % (CODE + 4 * i, w))
    cmds += ["unassemble 0x%x 0x%x" % (CODE, CODE + 4 * len(PROG)), "pc=0x%x" % CODE, "step %d" % len(PROG), "reg", "quit"]
    argv = [BIN, "-V", "-x", "-E", "bareppc", "-M", "64"] + (["-C", cpu] if cpu else []) + ["0x%x:%s" % (CODE, DUMMY)]
    p = subprocess.run(argv, input=("\n".join(cmds) + "\n").encode(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
    t = p.stdout.decode("latin-1", "replace").replace("\r", "")
    idx = t.rfind("GXemul> reg")
    regs = {int(m.group(1)): int(m.group(2), 16) for m in re.finditer(r"\br(\d\d) = (0x[0-9a-fA-F]+)", t[idx:])}
    mx = re.search(r"\bxer\s*=\s*(0x[0-9a-fA-F]+)", t[idx:])
    regs["xer"] = int(mx.group(1), 16) if mx else None
    dis = re.findall(r"^[0-9a-f]+: ([0-9a-f]{8})\s+(\S+)\t?(\S*)", t, re.M)
    return p.returncode, regs, dis, t


rows = []
def row(name, got, want):
    ok = got == want
    rows.append(ok)
    print("%-22s got=%-22s want=%-22s %s" % (name, got, want, "ok" if ok else "FAIL"))

print("shift_witness -- binary=%s" % BIN)
for cpu, label, mask in ((None, "PPC970(64)", (1 << 64) - 1), ("PPC603", "PPC603(32)", 0xFFFFFFFF)):
    rc, r, dis, t = session(cpu)
    print("== %s rc=%d  disasm: %s" % (label, rc, " | ".join("%s %s" % (m, o) for _, m, o in dis[:7])))
    h = lambda v: None if v is None else hex(v & mask)
    row(label + " live", h(r.get(15)), hex(0x1234))
    row(label + " slw ctl sh4", h(r.get(9)), hex(0x23456780))
    row(label + " slw sh32", h(r.get(4)), hex(0))
    row(label + " slw sh33", h(r.get(14)), hex(0))
    row(label + " srw sh32", h(r.get(6)), hex(0))
    row(label + " sraw sh32", h(r.get(7)), hex(mask))
    ca = None if r.get("xer") is None else (r["xer"] >> 29) & 1
    row(label + " sraw sh32 CA", ca, 1)
    if cpu is None:
        row(label + " srw hiword", h(r.get(11)), hex(0x1))
print("RESULT %d/%d" % (sum(rows), len(rows)))
print("SHIFT_WITNESS_DONE")
