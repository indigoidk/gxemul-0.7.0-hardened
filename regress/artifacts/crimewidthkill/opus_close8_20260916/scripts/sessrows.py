#!/usr/bin/env python3
"""sessrows.py -- print, for every session that drives a PRE-latch (latch-CLEAR) 4-byte access at a named label,
its rows.  The question is whether ANY of those rows can see a SILENT decline there.  Sentinel: SESSROWS_DONE."""
import io, re, sys, contextlib
SRC = "/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/crime_width_probe.py"
src = open(SRC).read().replace("t, clean = session(", "t, clean = _rec(")
src = re.sub(r"(?m)^(\s*)row\(", lambda m: m.group(1) + "_row(", src)
OPC = {0x20: ("lb", 1, "R"), 0x21: ("lh", 2, "R"), 0x23: ("lw", 4, "R"), 0x24: ("lbu", 1, "R"),
       0x25: ("lhu", 2, "R"), 0x37: ("ld", 8, "R"), 0x28: ("sb", 1, "W"), 0x29: ("sh", 2, "W"),
       0x2b: ("sw", 4, "W"), 0x3f: ("sd", 8, "W")}
CRIME, DEVLEN = 0xb4000000, 0x280
LAB = {0x00: "REV", 0x08: "CTL", 0x10: "IST", 0x18: "IMK", 0x30: "DOG", 0x38: "TIM"}
S, PEND = [], []
def _row(name, got, want, note=""): PEND.append(name)
def _rec(cmds, settle=1.5, spin=1.2):
    regs, acc = {}, []
    for c in cmds:
        m = re.match(r"^([a-z0-9]+)=0x([0-9a-f]+)$", c)
        if m: regs[m.group(1)] = int(m.group(2), 16); continue
        m = re.match(r"^put w 0x([0-9a-f]+), 0x([0-9a-f]{8})$", c)
        if m:
            w = int(m.group(2), 16); op, rs = w >> 26, (w >> 21) & 0x1f
            if op in OPC and rs in (1, 7):
                b = regs.get("at" if rs == 1 else "a3")
                if b is not None: acc.append((OPC[op], b, int(m.group(1), 16)))
    S.append([acc, list(PEND)]); del PEND[:]; return "", True
sys.argv = ["crime_width_probe.py", "/nonexistent", "map"]
try:
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(src, SRC, "exec"), {"__name__": "__main__", "_rec": _rec, "_row": _row})
except SystemExit: pass
S.append([[], list(PEND)])
want = set()
for i in range(len(S) - 1):
    acc = S[i][0]
    ref = len(acc)
    for j, ((op, ln, d), b, w) in enumerate(acc):
        if ln in (1, 2) and CRIME <= b < CRIME + DEVLEN: ref = j; break
    for (op, ln, d), b, w in acc[:ref]:
        if ln == 4 and CRIME <= b < CRIME + DEVLEN and (b - CRIME) in LAB:
            want.add(i)
for i in sorted(want):
    acc = S[i][0]
    ref = len(acc)
    for j, ((op, ln, d), b, w) in enumerate(acc):
        if ln in (1, 2) and CRIME <= b < CRIME + DEVLEN: ref = j; break
    pre = ["%s+0x%x[%s]" % (op, b - CRIME, LAB.get(b - CRIME, "DFL"))
           for (op, ln, d), b, w in acc[:ref] if ln == 4 and CRIME <= b < CRIME + DEVLEN and (b - CRIME) in LAB]
    print("#%-3d preLatch4byteAtLabel: %s" % (i, " ".join(pre)))
    print("     rows: %s" % ", ".join(S[i + 1][1]))
print("SESSROWS_DONE")
