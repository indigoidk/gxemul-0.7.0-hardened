#!/usr/bin/env python3
"""census_analyze.py census.log sessions_f5e915f6.replayed.json -- pair the MEASURED census (one pid per probe session,
in session order) with the probe's own session list, check it against the static replay, and print:
  (1) the refused-access cell map (label x len x dir x latch-before) from the MEASURED accesses;
  (2) every TIME update in the tl/time sessions, to settle premise Q1(b) from the device's own view;
  (3) the interrupt state (SOFTINT, INTMASK, HARDINT, prev_asserted) at every refused access at INTSTAT/INTMASK/CONTROL."""
import json, re, sys
from collections import OrderedDict

LABEL = {0x00: "REV", 0x08: "CONTROL", 0x10: "INTSTAT", 0x18: "INTMASK", 0x30: "DOG", 0x38: "TIME"}
groups = OrderedDict()
for line in open(sys.argv[1]):
    f = line.split()
    if len(f) < 3 or f[0] not in ("A", "T"):
        continue
    groups.setdefault(f[1], []).append(line.rstrip("\n"))
d = json.load(open(sys.argv[2]))
S = d["sessions"]
print("census pid groups=%d  probe sessions=%d" % (len(groups), len(S)))
if len(groups) != len(S):
    print("*** COUNT MISMATCH -- pairing by order is NOT valid; stopping ***")
    sys.exit(1)

cells = {}
mism = 0
for (pid, lines), s in zip(groups.items(), S):
    acc = []
    for ln in lines:
        if ln[0] != "A":
            continue
        m = re.match(r"A \d+ ([RW]) len=(\d+) rel=0x([0-9a-f]+) idata=0x([0-9a-f]+) latch=(\d) prev=(\d) "
                     r"soft=0x([0-9a-f]+) mask=0x([0-9a-f]+) hard=0x([0-9a-f]+) time=0x([0-9a-f]+) pc=0x([0-9a-f]+)", ln)
        acc.append(dict(dir=m.group(1), len=int(m.group(2)), off=int(m.group(3), 16), idata=int(m.group(4), 16),
                        latch=int(m.group(5)), prev=int(m.group(6)), soft=int(m.group(7), 16),
                        mask=int(m.group(8), 16), hard=int(m.group(9), 16), time=int(m.group(10), 16),
                        pc=int(m.group(11), 16)))
    st = [(a["len"], a["dir"], a["off"]) for a in s["acc"]]
    me = [(a["len"], a["dir"], a["off"]) for a in acc]
    if st != me:
        mism += 1
        print("S%02d STATIC/MEASURED DIFFER: static %s measured %s" % (s["idx"], st, me))
    for a in acc:
        if a["len"] in (1, 2):
            lab = LABEL.get(a["off"], "default")
            key = (lab, a["len"], a["dir"], "SET" if a["latch"] else "CLEAR")
            cells.setdefault(key, []).append("S%02d" % s["idx"])
            if lab in ("INTSTAT", "INTMASK", "CONTROL"):
                print("S%02d refused %d%s +0x%02x %-7s latch=%d prev=%d soft=%x mask=%x hard=%x%s  rows=%s" % (
                    s["idx"], a["len"], a["dir"], a["off"], lab, a["latch"], a["prev"], a["soft"], a["mask"],
                    a["hard"], (" idata=0x%x" % a["idata"]) if a["dir"] == "W" else "", ",".join(s["rows"][:3])))
    if any(r.startswith(("tl ", "time lb", "time sb", "time lh", "time sh")) for r in s["rows"]):
        print("S%02d TIME trace (rows %s):" % (s["idx"], ",".join(s["rows"])))
        for ln in lines:
            if ln[0] == "T" or (" rel=0x38 " in ln) or (" rel=0x7 " in ln):
                print("      " + ln)
print("static/measured access-list mismatches: %d of %d sessions" % (mism, len(S)))
print()
print("MEASURED REFUSED-ACCESS CELLS (label, len, dir, latch) -> sessions:")
for lab in ("REV", "CONTROL", "INTSTAT", "INTMASK", "DOG", "TIME"):
    for ln in (1, 2):
        for dr in ("R", "W"):
            for lt in ("CLEAR", "SET"):
                print("  %-8s %d%s %-5s %s" % (lab, ln, dr, lt, " ".join(cells.get((lab, ln, dr, lt), ["-- NONE --"]))))
