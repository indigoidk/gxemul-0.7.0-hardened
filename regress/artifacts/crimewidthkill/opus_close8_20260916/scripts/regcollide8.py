#!/usr/bin/env python3
"""regcollide8.py -- discharge the P6 REGISTER-COLLISION audit the repair-13 comment could not.  For every session,
list each destination register and how many DISTINCT accesses write it.  A register written by two accesses whose
results are BOTH read by rows is a collision: one row reads the other's value and goes green for the wrong reason.
Sentinel: REGCOLLIDE8_DONE."""
import io, re, sys, contextlib
SRC = "/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/crime_width_probe.py"
src = open(SRC).read().replace("t, clean = session(", "t, clean = _rec(")
src = re.sub(r"(?m)^(\s*)row\(", lambda m: m.group(1) + "_row(", src)
RN = {0: "zero", 1: "at", 2: "v0", 3: "v1", 4: "a0", 5: "a1", 6: "a2", 7: "a3", 8: "t0", 9: "t1",
      16: "s0", 17: "s1", 18: "s2", 19: "s3", 31: "ra"}
OPC = {0x20: ("lb", 1, "R"), 0x21: ("lh", 2, "R"), 0x23: ("lw", 4, "R"), 0x24: ("lbu", 1, "R"),
       0x25: ("lhu", 2, "R"), 0x37: ("ld", 8, "R"), 0x28: ("sb", 1, "W"), 0x29: ("sh", 2, "W"),
       0x2b: ("sw", 4, "W"), 0x3f: ("sd", 8, "W")}
CRIME = 0xb4000000
S, PEND = [], []
def _row(name, got, want, note=""): PEND.append(name)
def _rec(cmds, settle=1.5, spin=1.2):
    regs, dests, prints = {}, [], []
    for c in cmds:
        m = re.match(r"^([a-z0-9]+)=0x([0-9a-f]+)$", c)
        if m: regs[m.group(1)] = int(m.group(2), 16); continue
        m = re.match(r"^print ([a-z0-9]+)$", c)
        if m: prints.append(m.group(1)); continue
        m = re.match(r"^put w 0x([0-9a-f]+), 0x([0-9a-f]{8})$", c)
        if m:
            w = int(m.group(2), 16); op, rs, rt = w >> 26, (w >> 21) & 0x1f, (w >> 16) & 0x1f
            if op in OPC and OPC[op][2] == "R" and rs in (1, 7):
                b = regs.get("at" if rs == 1 else "a3")
                dests.append((RN.get(rt, "r%d" % rt), OPC[op][0], b))
    S.append([dests, prints, list(PEND)]); del PEND[:]; return "", True
sys.argv = ["crime_width_probe.py", "/nonexistent", "map"]
try:
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(src, SRC, "exec"), {"__name__": "__main__", "_rec": _rec, "_row": _row})
except SystemExit: pass
S.append([[], [], list(PEND)])
bad = 0
for i in range(len(S) - 1):
    dests, prints, _ = S[i]
    myrows = S[i + 1][2]
    cnt = {}
    for rt, op, b in dests:
        cnt.setdefault(rt, []).append("%s@%s" % (op, ("+0x%x" % (b - CRIME)) if b and b >= CRIME else hex(b or 0)))
    multi = {r: v for r, v in cnt.items() if len(v) > 1 and r in prints}
    if multi:
        bad += 1
        print("#%-3d COLLISION CANDIDATE  rows: %s" % (i, ", ".join(myrows)))
        for r, v in sorted(multi.items()):
            print("      %-4s written by %d loads and PRINTED: %s" % (r, len(v), " ".join(v)))
print("")
print("sessions with a printed register written by MORE THAN ONE load: %d" % bad)
print("(one write per printed register = no row can read another row's value)")
print("REGCOLLIDE8_DONE")
