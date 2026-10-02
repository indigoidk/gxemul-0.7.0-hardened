#!/usr/bin/env python3
"""static_census.py sessions.json -- replay each recorded session's debugger commands symbolically (register
assignments, `put w', `pc=', `step N', free-running `<RUN>') and list every CRIME access it issues, with the width latch
state BEFORE the access.  A cross-check for the MEASURED census (census.log), not a substitute for it."""
import json, sys

CRIME, CRIME_END = 0xb4000000, 0xb4000000 + 0x280
OPS = {0x20: ("lb", 1, "R"), 0x21: ("lh", 2, "R"), 0x23: ("lw", 4, "R"), 0x24: ("lbu", 1, "R"),
       0x25: ("lhu", 2, "R"), 0x37: ("ld", 8, "R"), 0x28: ("sb", 1, "W"), 0x29: ("sh", 2, "W"),
       0x2b: ("sw", 4, "W"), 0x3f: ("sd", 8, "W")}
RN = {0: "zero", 1: "at", 2: "v0", 3: "v1", 4: "a0", 5: "a1", 6: "a2", 7: "a3", 8: "t0", 9: "t1",
      16: "s0", 17: "s1", 18: "s2", 19: "s3", 20: "s4", 31: "ra"}
LABEL = {0x00: "REV", 0x08: "CONTROL", 0x10: "INTSTAT", 0x18: "INTMASK", 0x30: "DOG", 0x38: "TIME"}


def replay(cmds):
    regs, mem, pc, latch, acc = {}, {}, None, False, []

    def execute(n):
        nonlocal pc, latch
        for _ in range(n):
            w = mem.get(pc)
            if w is None or w == 0x1000ffff or w == 0:
                return                              # b self / nop: no access, and the pc stays put
            op, rs, rt = w >> 26, (w >> 21) & 31, (w >> 16) & 31
            if op not in OPS:
                return
            name, ln, d = OPS[op]
            addr = regs.get(RN.get(rs), None)
            if addr is not None and CRIME <= addr < CRIME_END:
                off = addr - CRIME
                narrow = ln in (1, 2)
                acc.append({"op": name, "len": ln, "dir": d, "off": off, "label": LABEL.get(off, "default"),
                            "latch_before": latch, "pc": pc, "val": regs.get(RN.get(rt)) if d == "W" else None,
                            "refused": narrow})
                if narrow:
                    latch = True
            pc += 4

    for c in cmds:
        if c == "<RUN>":
            execute(64)
            continue
        if c.startswith("put w "):
            a, v = c[6:].split(",")
            mem[int(a, 16)] = int(v, 16)
        elif c.startswith("pc="):
            pc = int(c[3:], 16)
        elif c.startswith("step "):
            execute(int(c[5:]))
        elif "=" in c and not c.startswith("print"):
            r, v = c.split("=", 1)
            regs[r] = int(v, 16)
    return acc


d = json.load(open(sys.argv[1]))
cells = {}
for s in d["sessions"]:
    acc = replay(s["cmds"])
    s["acc"] = acc
    ref = [a for a in acc if a["refused"]]
    print("S%02d rows=%s" % (s["idx"], ",".join(s["rows"])))
    for a in ref:
        win = (a["pc"] & 0xffffff00) == 0xbfc05100
        print("      REFUSED %-3s +0x%03x %-8s latch=%s%s%s" % (a["op"], a["off"], a["label"],
              "SET" if a["latch_before"] else "clr", " PROMwin" if win else "",
              (" val=0x%x" % a["val"]) if a["val"] is not None else ""))
        key = (a["label"], a["len"], a["dir"], "SET" if a["latch_before"] else "CLEAR")
        cells.setdefault(key, []).append("S%02d" % s["idx"])
print()
print("REFUSED-ACCESS CELLS (label, len, dir, latch) -> sessions:")
for lab in ("REV", "CONTROL", "INTSTAT", "INTMASK", "DOG", "TIME"):
    for ln in (1, 2):
        for dr in ("R", "W"):
            for lt in ("CLEAR", "SET"):
                print("  %-8s %d%s %-5s %s" % (lab, ln, dr, lt, " ".join(cells.get((lab, ln, dr, lt), ["-- NONE --"]))))
json.dump(d, open(sys.argv[1].replace(".json", ".replayed.json"), "w"), indent=1)
