#!/usr/bin/env python3
"""cellmap8b.py -- per-session detail behind cellmap8.py.  Sentinel: CELLMAP8B_DONE."""
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
for i in range(len(S) - 1):
    acc, myrows = S[i][0], S[i + 1][1]
    ref = None
    for j, ((op, ln, d), b, w) in enumerate(acc):
        if ln in (1, 2) and CRIME <= b < CRIME + DEVLEN: ref = j; break
    post = []
    if ref is not None:
        for (op, ln, d), b, w in acc[ref + 1:]:
            if ln in (4, 8) and CRIME <= b < CRIME + DEVLEN:
                off = b - CRIME
                post.append("%s%s@+0x%x[%s%s]" % (op, "P" if (w & 0xffffff00) == 0xbfc05100 else "",
                            off, LAB.get(off, "DFL"), (".l%d" % ((off & 4) >> 2)) if ln == 4 else ""))
    print("#%-3d nacc=%-3d firstCrimeRefusal=%-5s POST=%-3d %s" % (i, len(acc), ref, len(post), " ".join(post)))
    print("      rows: %s" % ", ".join(myrows))
print("CELLMAP8B_DONE")
