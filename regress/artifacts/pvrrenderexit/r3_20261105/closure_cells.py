#!/usr/bin/env python3
"""closure_cells.py -- the DERIVER of CLOSURE3.md's input-cell denominator and its disposition tally (pvrrenderexit repair 3,
2026-11-05).  One line per INPUT CELL (codex's unit: a region of a predicate's inputs that a row can place a span or a header in).
Edit forms are a different unit and are not counted here (CLOSURE3.md section 4 tabulates them by family; table 3 builds 114).
Dispositions: OLD = an existing row reads it; NEW = a repair-3 row; EQUIV / DOM = equivalent / dominated (CLOSURE3.md gives the
derivation); UB = only an edit with undefined behaviour reaches it; NN = a decode pattern no single edit separates.
usage: closure_cells.py   (prints every cell, then the tally)"""
import collections

C = []


def cell(group, name, disp, row):
    C.append((group, name, disp, row))


for r, tex in (("s", ""), ("t", "tex")):
    g = "codex84/" + r
    cell(g, "P1 row -1", "UB", "Y2 admits it: vram_z[x - 640]")
    cell(g, "P1 row 0", "OLD", tex + "yedges t in")
    cell(g, "P1 row 479", "OLD", tex + "yedges b in")
    cell(g, "P1 row 480", "OLD", tex + "yedges b out (the admitting edit Y4 is UB)")
    cell(g, "P2 (no,no)", "OLD", "every inner row")
    cell(g, "P2 (yes,no)", "OLD", tex + "edges l in")
    cell(g, "P2 (no,yes)", "NEW", tex + "edges2 l rev")
    cell(g, "P2 (yes,yes)", "EQUIV", "the inner x > 0 draws nothing of it")
    cell(g, "P3 (no,no)", "OLD", "every inner row")
    cell(g, "P3 (no,yes)", "OLD", tex + "edges r in, rspan")
    cell(g, "P3 (yes,no)", "NEW", tex + "edges2 r rev")
    cell(g, "P3 (yes,yes)", "EQUIV", "the inner x < 640 draws nothing of it")
    cell(g, "P4 forward", "OLD", "every forward row")
    cell(g, "P4 equal ends, equal attributes", "EQUIV", "an exchange of equal values")
    cell(g, "P4 equal ends, unequal attributes", "NEW", tex + "swap vert")
    cell(g, "P4 reversed by 1", "NEW", tex + "swap s tip")
    cell(g, "P4 reversed by > 1", "OLD", tex + "yedges swap")
    cell(g, "P5 before", "NEW", tex + "swap s before")
    cell(g, "P5 at", "OLD", tex + "edges rspan")
    cell(g, "P5 after", "DOM", "dropped only with P5 at")
    cell(g, "P6 before", "OLD", "every inner row")
    cell(g, "P6 at", "OLD", tex + "yedges s end")
    cell(g, "P6 after", "OLD", tex + "yedges s past")
    for c, rw in ((0, "l out"), (1, "l in"), (639, "r in"), (640, "r out")):
        cell(g, "P7 column %d" % c, "OLD", tex + "edges " + rw)
    cell(g, "P8 (<,on)", "OLD", "ovon t1 only" if r == "s" else "texbeh t1 only")
    cell(g, "P8 (<,off)", "OLD", "ovoff t1 only" if r == "s" else "texoff t1 only")
    cell(g, "P8 (==,on)", "OLD", tex + "equal overlap")
    cell(g, "P8 (==,off)", "NEW", tex + "zeq overlap")
    cell(g, "P8 (>,on)", "OLD", "ovon overlap" if r == "s" else "texon overlap")
    cell(g, "P8 (>,off)", "OLD", "behind overlap" if r == "s" else "texbeh overlap")
cell("codex84/s", "fractional end floor(x2)", "DOM", "every narrowing that drops it drops yedges s end")
cell("codex84/s", "fractional end ceil(x2)", "NEW", "swap frac past")
for pat, disp, rw in ((0x00, "OLD", "ovon (every Z-on header)"), (0x02, "OLD", "mask25 overlap"), (0x04, "OLD", "ovoff overlap"),
                      (0x08, "OLD", "mask overlap"), (0x0c, "NEW", "maskoff overlap"), (0x10, "NEW", "maskhi overlap (0xf0000000)")):
    cell("codex84/decode", "word 1 bits 25-28 = 0x%02x000000" % pat, disp, rw)
for pat in (0x06, 0x0a, 0x0e, 0x12, 0x14, 0x16, 0x18, 0x1a, 0x1c, 0x1e):
    cell("codex84/decode", "word 1 bits 25-28 = 0x%02x000000" % pat, "NN", "no single edit separates it (CLOSURE3.md, P9)")
for a in ("z", "r", "g", "b"):
    cell("A1 swap body", "simpleline: a reversed span whose ends differ in %s" % a, "NEW", "ramp l end")
for a in ("z", "u", "v"):
    cell("A1 swap body", "texturedline: a reversed span whose ends differ in %s" % a, "NEW", "texramp l end")
for r, tex in (("s", ""), ("t", "tex")):
    cell("A2 right edges", r + ": forward span from [639, 640) to >= 640", "OLD", tex + "edges rspan")
    cell("A2 right edges", r + ": reversed span from >= 640 to [639, 640)", "NEW", tex + "edges2 r rev")
    cell("A3 left edges", r + ": reversed span from [1, 2) to < 0", "NEW", tex + "edges2 l tip")
    cell("A3 left edges", r + ": forward span from < 0 to [1, 2)", "NEW", tex + "edges2 x2 tip")
for b in (29, 30, 31):
    cell("A7 decode", "a Z-on header with word 1 bit %d set" % b, "NEW", "maskhi overlap (0xf0000000)")

#  THE Z-OFF TWINS (the coordinator's ruling on the 09-04 floor): every P1-P7 cell above (codex84's per-rasterizer geometry cells, the
#  fractional pair, A1, A2, A3) crossed with Z-write OFF.  The rows above draw Z-on polygons; each twin is rowed by the same pixel of
#  the matching z* / zt* session (zleft / texzleft for the x2 edge), so a rowed cell's twin is NEW, and an EQUIV, DOM or UB cell's twin
#  keeps that disposition for the same reason (Z-write changes only the depth store, never which pixels are drawn).
_TWINROW = {"yedges": "zyedges", "texyedges": "ztyedges", "edges": "zedges", "texedges": "ztedges", "swap": "zswap", "texswap": "ztswap",
            "edges2": "zedges2", "texedges2": "ztedges2", "ramp": "zramp", "texramp": "ztramp"}


def _twin_row(rw):
    w = rw.split(" ", 1)
    if rw.startswith(("edges2 x2 tip", "texedges2 x2 tip")):
        return ("tex" if rw.startswith("tex") else "") + "zleft tip"
    if w[0] in _TWINROW:
        return _TWINROW[w[0]] + " " + w[1]
    return "the Z-off twin of: " + rw


for g, n, d, rw in list(C):
    geo = (g.startswith("codex84/s") or g.startswith("codex84/t")) and not n.startswith("P8") or g.startswith(("A1", "A2", "A3"))
    if geo:
        cell("Z-off twins/" + g, n + " -- Z-OFF", "NEW" if d in ("OLD", "NEW") else d, _twin_row(rw) if d in ("OLD", "NEW") else rw)

if __name__ == "__main__":
    for g, n, d, rw in C:
        print("%-18s %-52s %-6s %s" % (g, n, d, rw))
    t = collections.Counter(d for _, _, d, _ in C)
    print("CELLS %d: %s" % (len(C), "  ".join("%s %d" % (k, t[k]) for k in ("OLD", "NEW", "EQUIV", "DOM", "UB", "NN"))))
    print("codex84 %d, added %d (of them Z-off twins %d)" % (sum(1 for g, *_ in C if g.startswith("codex84")),
                                                             sum(1 for g, *_ in C if not g.startswith("codex84")),
                                                             sum(1 for g, *_ in C if g.startswith("Z-off twins"))))
