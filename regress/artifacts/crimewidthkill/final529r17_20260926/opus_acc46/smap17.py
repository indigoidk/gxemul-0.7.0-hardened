#!/usr/bin/env python3
"""smap17.py -- static session map of the r17 crime_width probe (no emulator).

For every session: its accesses in execution order (op, width, dir, CRIME offset, stored value, PROM-window flag,
latch state = whether a refused 1/2-byte CRIME access precedes it in the session), and the rows it feeds.
Then, for each of the 46 ACCEPTS entries, every session access that MATCHES it, split by latch state.

MATCH (the unit of this enumeration): same op width, same direction, same CRIME offset, same PROM-window flag for
offset 0 (REV), and, for a CONTROL (+0x08) write, the same stored value.  Other writes match on width/dir/offset
whatever value they store.  Sentinel: SMAP17_DONE."""
import io, re, sys, contextlib

SRC = sys.argv[1]
src = open(SRC, encoding="utf-8").read()
n_sess = src.count("t, clean = session(")
src = src.replace("t, clean = session(", "t, clean = _rec(")
src = re.sub(r"(?m)^(\s*)row\(", lambda m: m.group(1) + "_row(", src)
assert re.search(r"(?m)^\s*row\(", src) is None
#  every CODE-LEVEL call of session() must have been rewritten (docstring/comment mentions are not calls)
_code = [l for l in src.split("\n") if not l.lstrip().startswith("#")]
_left = [l for l in _code if re.search(r"(?<![a-z_])session\(", l) and "def session(" not in l]
assert not _left, "unmapped session() call: %r" % _left[:3]

OPC = {0x20: ("lb", 1, "R"), 0x21: ("lh", 2, "R"), 0x23: ("lw", 4, "R"), 0x24: ("lbu", 1, "R"),
       0x25: ("lhu", 2, "R"), 0x37: ("ld", 8, "R"), 0x28: ("sb", 1, "W"), 0x29: ("sh", 2, "W"),
       0x2b: ("sw", 4, "W"), 0x3f: ("sd", 8, "W")}
RNUM = {"zero": 0, "at": 1, "v0": 2, "v1": 3, "a0": 4, "a1": 5, "a2": 6, "a3": 7, "t0": 8, "t1": 9,
        "s0": 16, "s1": 17, "s2": 18, "s3": 19, "s4": 20, "ra": 31}
CRIME = 0xb4000000
MACE = 0xbf310000
SESSIONS = []
PEND = []


def _row(name, got, want, note=""):
    PEND.append(name)


def _rec(cmds, settle=1.5, spin=1.2):
    regs, mem, acc, pc = {}, {}, [], None
    for c in cmds:
        m = re.match(r"^([a-z0-9]+)=0x([0-9a-f]+)$", c)
        if m:
            if m.group(1) == "pc":
                pc = int(m.group(2), 16)
            else:
                regs[RNUM[m.group(1)]] = int(m.group(2), 16)
            continue
        m = re.match(r"^put w 0x([0-9a-f]+), 0x([0-9a-f]{8})$", c)
        if m:
            mem[int(m.group(1), 16)] = int(m.group(2), 16)
            continue
        m = re.match(r"^step (\d+)$", c)
        if m or c == "<RUN>":
            n = int(m.group(1)) if m else 10 ** 6
            while n > 0 and pc in mem:
                w = mem[pc]
                if w == 0x1000ffff:          # b . -- a self loop ends the walk
                    break
                op, rs, rt = w >> 26, (w >> 21) & 0x1f, (w >> 16) & 0x1f
                if op in OPC:
                    name, ln, d = OPC[op]
                    base = regs.get(rs)
                    if base is not None:
                        acc.append({"op": name, "len": ln, "dir": d, "addr": base, "pc": pc,
                                    "val": regs.get(rt) if d == "W" else None})
                    if d == "R":             # a load's destination is unknown afterwards (never a base here)
                        regs.pop(rt, None)
                pc += 4
                n -= 1
            continue
    SESSIONS.append([acc, list(PEND)])
    del PEND[:]
    return "", True


sys.argv = ["crime_width_probe.py", "/nonexistent-binary", "map"]
buf = io.StringIO()
g = {"__name__": "__main__", "_rec": _rec, "_row": _row}
with contextlib.redirect_stdout(buf):
    try:
        exec(compile(src, SRC, "exec"), g)
    except SystemExit:
        pass
SESSIONS.append([[], list(PEND)])
ACCEPTS = g["ACCEPTS"]


def crime_off(a):
    return a - CRIME if CRIME <= a < CRIME + 0x280 else None


def win(pc):
    return (pc & 0xffffff00) == 0xbfc05100


sess = []
for i in range(len(SESSIONS) - 1):
    acc, rows = SESSIONS[i][0], SESSIONS[i + 1][1]
    latch = False
    for a in acc:
        off = crime_off(a["addr"])
        a["off"] = off
        a["latch"] = "SET" if latch else "CLR"
        a["win"] = win(a["pc"])
        if off is not None and a["len"] in (1, 2):
            latch = True
    sess.append((acc, rows))

print("SOURCE %s  sessions=%d  rows=%d" % (SRC, len(sess), sum(len(r) for _, r in sess)))
for i, (acc, rows) in enumerate(sess):
    parts = []
    for a in acc:
        if a["off"] is None:
            where = "MACE+0x%x" % (a["addr"] - MACE) if MACE <= a["addr"] < MACE + 0x100 else "RAM"
        else:
            where = "+0x%x" % a["off"]
        v = "" if a["val"] is None else "=0x%x" % a["val"]
        parts.append("%s%s%s%s%s" % (a["op"], "P" if a["win"] else "", where, v, "" if a["latch"] == "CLR" else "*"))
    print("S%-3d rows[%s]" % (i, ", ".join(rows)))
    print("      acc: %s" % " ".join(parts))

print("")
print("=== ACCEPTS entries: matching accesses by session and latch state (* = latch SET) ===")
for k, (op, off, val) in enumerate(ACCEPTS, 1):
    P = op.endswith("P")
    bop = op[:2] if P else op
    ln = {"sd": 8, "ld": 8, "sw": 4, "lw": 4}[bop]
    d = "W" if bop[0] == "s" else "R"
    clr, st = [], []
    for i, (acc, rows) in enumerate(sess):
        for j, a in enumerate(acc):
            if a["off"] != off or a["len"] != ln or a["dir"] != d:
                continue
            if off == 0 and a["win"] != P:
                continue
            if off == 8 and d == "W" and a["val"] != val:
                continue
            tag = "S%d.%d%s" % (i, j, "" if (d == "R" or off == 8) else ("=0x%x" % a["val"]))
            (st if a["latch"] == "SET" else clr).append(tag)
    print("%-3d %-4s +0x%-4x %-7s CLR: %s" % (k, op, off, ("0x%x" % val) if (off == 8 and d == "W") else "",
                                           " ".join(clr)))
    print("                      SET: %s" % " ".join(st))
print("SMAP17_DONE")
