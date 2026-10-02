#!/usr/bin/env python3
"""session_map2.py -- #529 closing pass 7 (Opus, finishing seat).  As session_map.py, plus the ROW NAMES each
session feeds, so `which rows can observe a post-latch accepted access' is DERIVED from the shipped probe rather
than asserted.  Does not run the emulator.  Sentinel: SESSIONMAP_DONE."""
import io, re, sys, contextlib

SRC = sys.argv[1] if len(sys.argv) > 1 else "/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/crime_width_probe.py"
src = open(SRC).read()
src = src.replace("t, clean = session(", "t, clean = _rec(")
assert "t, clean = session(" not in src
src = re.sub(r"(?m)^(\s*)row\(", lambda m: m.group(1) + "_row(", src)
assert re.search(r"(?m)^\s*row\(", src) is None

OPC = {0x20: ("lb", 1, "R"), 0x21: ("lh", 2, "R"), 0x23: ("lw", 4, "R"), 0x24: ("lbu", 1, "R"),
       0x25: ("lhu", 2, "R"), 0x37: ("ld", 8, "R"), 0x28: ("sb", 1, "W"), 0x29: ("sh", 2, "W"),
       0x2b: ("sw", 4, "W"), 0x3f: ("sd", 8, "W")}
CRIME = 0xb4000000
SESSIONS = []
PEND = []


def _row(name, got, want, note=""):
    PEND.append(name)


def _rec(cmds, settle=1.5, spin=1.2):
    regs, acc, pc = {}, [], None
    for c in cmds:
        m = re.match(r"^([a-z0-9]+)=0x([0-9a-f]+)$", c)
        if m:
            if m.group(1) == "pc":
                pc = int(m.group(2), 16)
            else:
                regs[m.group(1)] = int(m.group(2), 16)
            continue
        m = re.match(r"^put w 0x([0-9a-f]+), 0x([0-9a-f]{8})$", c)
        if m:
            w = int(m.group(2), 16)
            op, rs = w >> 26, (w >> 21) & 0x1f
            if op in OPC and rs in (1, 7):
                base = regs.get("at" if rs == 1 else "a3")
                if base is not None:
                    acc.append((OPC[op], base, int(m.group(1), 16)))
    SESSIONS.append([acc, list(PEND)])          # rows of the PREVIOUS session, flushed here
    del PEND[:]
    return "", True


sys.argv = ["crime_width_probe.py", "/nonexistent-binary", "map"]
buf = io.StringIO()
try:
    with contextlib.redirect_stdout(buf):
        exec(compile(src, SRC, "exec"), {"__name__": "__main__", "_rec": _rec, "_row": _row})
except SystemExit:
    pass
SESSIONS.append([[], list(PEND)])               # the last session's rows

print("SESSIONS=%d" % (len(SESSIONS) - 1))
tot = 0
for i in range(len(SESSIONS) - 1):
    acc = SESSIONS[i][0]
    myrows = SESSIONS[i + 1][1]
    ref = None
    for j, ((op, ln, d), base, where) in enumerate(acc):
        if ln in (1, 2):
            ref = j
            break
    post = []
    if ref is not None:
        for (op, ln, d), base, where in acc[ref + 1:]:
            if ln in (4, 8) and (base & ~0xfff) == CRIME:
                post.append("%s%s+0x%x" % (op, "P" if (where & 0xffffff00) == 0xbfc05100 else "", base - CRIME))
    tot += len(post)
    if post:
        print("#%-3d acc=%-3d firstRefusal=%-4s POST=%d  %s" % (i, len(acc), ref, len(post), " ".join(post)))
        print("      rows: %s" % ", ".join(myrows))
print("TOTAL post-latch accepted CRIME accesses: %d" % tot)
print("SESSIONMAP_DONE")
