#!/usr/bin/env python3
"""preclear8.py -- the LATCH-CLEAR half of the denominator.  cellmap8.py maps accepted accesses AFTER a session's
first CRIME refusal; this maps the ones BEFORE it (and every access of a session that never refuses), which is the
state the glm seat's mutant fires in.  Sentinel: PRECLEAR8_DONE."""
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
n = len(S) - 1
print("SESSIONS=%d" % n)
cells, tot = {}, 0
for i in range(n):
    acc, myrows = S[i][0], S[i + 1][1]
    ref = len(acc)
    for j, ((op, ln, d), b, w) in enumerate(acc):
        if ln in (1, 2) and CRIME <= b < CRIME + DEVLEN: ref = j; break
    for (op, ln, d), b, w in acc[:ref]:
        if ln in (4, 8) and CRIME <= b < CRIME + DEVLEN:
            off = b - CRIME
            key = (ln, d, LAB.get(off, "DFL"), ((off & 4) >> 2) if ln == 4 else "-")
            cells.setdefault(key, []).append((i, op, off, myrows)); tot += 1
print("TOTAL PRE-latch (latch CLEAR) accepted CRIME accesses: %d" % tot)
print("")
print("=== PRE-LATCH occupancy, {len} x {dir} x {label} x {lane} ===")
empt = []
for lab in ("REV", "CTL", "IST", "IMK", "DOG", "TIM", "DFL"):
    for ln in (8, 4):
        for d in ("W", "R"):
            for lane in ((0, 1) if ln == 4 else ("-",)):
                v = cells.get((ln, d, lab, lane), [])
                nm = "%s %d%s lane=%s" % (lab, ln, d, lane)
                print("%-22s n=%-3d sess=%-22s %s" % (nm, len(v), str(sorted(set(s for s, _, _, _ in v)))[:22],
                      " ".join(sorted(set("+0x%x" % o for _, _, o, _ in v)))))
                if not v: empt.append(nm)
print("EMPTY pre-latch cells: %s" % (empt or "NONE"))
print("")
print("=== THE glm CELL: every PRE-latch 4-byte access at CRIME_TIME, with its session's ROWS ===")
for lane in (0, 1):
    for d in ("W", "R"):
        for i, op, off, myrows in cells.get((4, d, "TIM", lane), []):
            print("  sess #%-3d %s +0x%x  (lane %s, %s)" % (i, op, off, lane, d))
            print("      rows: %s" % ", ".join(myrows))
print("PRECLEAR8_DONE")
