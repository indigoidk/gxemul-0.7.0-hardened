#!/usr/bin/env python3
"""session_map.py -- #529 closing pass 7 (Opus, finishing seat).  STATIC MAP of the shipped 157-row probe:
for each session() call, the ORDERED list of CRIME accesses it issues, so the LATCH STATE at each accepted
access is derivable by reading rather than by assertion.  It does NOT run the emulator: it replaces session()
with a recorder that parses the command list back into (op, offset, pc) triples and returns ("", True).

An access is REFUSED iff its width is 1 or 2 (lb/lbu/sb/lh/lhu/sh); every other CRIME access is ACCEPTED.
The latch d->warned & CRIME_W_LEN is SET from the first refusal in a session onwards.

Output: one block per session, `#n post=<count of accepted accesses issued AFTER the first refusal>'.
Sentinel: SESSIONMAP_DONE."""
import io, re, sys, contextlib

SRC = sys.argv[1] if len(sys.argv) > 1 else "/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/crime_width_probe.py"
src = open(SRC).read()
# route every call site to the recorder; the definition itself is left alone
src = src.replace("t, clean = session(", "t, clean = _rec(")
assert "t, clean = session(" not in src

OPC = {0x20: ("lb", 1, "R"), 0x21: ("lh", 2, "R"), 0x23: ("lw", 4, "R"), 0x24: ("lbu", 1, "R"),
       0x25: ("lhu", 2, "R"), 0x37: ("ld", 8, "R"), 0x28: ("sb", 1, "W"), 0x29: ("sh", 2, "W"),
       0x2b: ("sw", 4, "W"), 0x3f: ("sd", 8, "W")}
CRIME = 0xb4000000
SESSIONS = []


def _rec(cmds, settle=1.5, spin=1.2):
    regs, pc, acc = {}, None, []
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
            if op in OPC and rs in (1, 7):          # at / a3
                base = regs.get("at" if rs == 1 else "a3")
                if base is not None:
                    acc.append((OPC[op], base, int(m.group(1), 16)))
    SESSIONS.append(acc)
    return "", True


g = {"__name__": "__main__", "sys": sys}
sys.argv = ["crime_width_probe.py", "/nonexistent-binary", "map"]
buf = io.StringIO()
try:
    with contextlib.redirect_stdout(buf):
        exec(compile(src, SRC, "exec"), dict(g, _rec=_rec))
except SystemExit:
    pass

print("SESSIONS=%d" % len(SESSIONS))
tot_post = 0
for i, acc in enumerate(SESSIONS):
    refused_at = None
    for j, ((op, ln, d), base, where) in enumerate(acc):
        if ln in (1, 2):
            refused_at = j
            break
    post = []
    if refused_at is not None:
        for (op, ln, d), base, where in acc[refused_at + 1:]:
            if ln in (4, 8) and (base & ~0xfff) == CRIME:
                post.append("%s%s+0x%x%s" % (op, "P" if (where & 0xffffff00) == 0xbfc05100 else "",
                                             base - CRIME, ""))
    tot_post += len(post)
    print("#%-3d accesses=%-4d firstRefusalIdx=%-5s postLatchAccepted=%d  %s"
          % (i, len(acc), refused_at, len(post), " ".join(post) if post else "-"))
print("TOTAL post-latch accepted CRIME accesses in the shipped probe: %d" % tot_post)
print("SESSIONMAP_DONE")
