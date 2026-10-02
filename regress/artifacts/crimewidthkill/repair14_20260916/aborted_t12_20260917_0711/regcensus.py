#!/usr/bin/env python3
"""regcensus.py -- sibling census for the register-clobber defect found in crime_width_probe.py.

THE DEFECT: a row loads a value into register X and reads it back later, but a HELPER uses X as
scratch in between, so the row reads the helper's leftover.  Measured once: crime_width_probe.py
loaded into `a3` while st() uses `a3` for its address; six stores later, the row read an ADDRESS.

*** MY FIRST CENSUS WAS KEYED ON A CORRELATE AND REPORTED NO HAZARD ANYWHERE. ***  It grepped for the
first line matching '"<reg>=0x%x" % addr' -- which in crime_width_probe.py is ld()'s `at`, not st()'s
`a3`.  Keying on "the first helper that builds an address" is not keying on "the register st()
clobbers".  This version parses the FUNCTION DEFINITIONS with ast and reads each helper's own body.
"""
import ast, io, os, re, sys

REGS = set(["at", "v0", "v1", "a0", "a1", "a2", "a3", "ra"] +
           ["t%d" % i for i in range(10)] + ["s%d" % i for i in range(8)])

def helper_scratch(tree, src):
    """for each top-level def, the registers it ASSIGNS in a command string -- i.e. clobbers"""
    out = {}
    for node in tree.body:
        if not isinstance(node, ast.FunctionDef):
            continue
        seg = ast.get_source_segment(src, node) or ""
        regs = set(m for m in re.findall(r'"([a-z0-9]+)=0x', seg) if m in REGS)
        if regs:
            out[node.name] = regs
    return out

def ld_targets(src):
    """(register, line) for every ld(...) whose destination is a literal register name"""
    out = []
    for i, ln in enumerate(src.split(chr(10)), 1):
        for m in re.finditer(r'\bld\([^)]*?"([a-z0-9]+)"\s*[,)]', ln):
            if m.group(1) in REGS:
                out.append((m.group(1), i, ln.strip()[:70]))
    return out

print("%-34s %-28s %s" % ("probe", "helper scratch registers", "verdict"))
print("-" * 104)
hazards = 0
scanned = 0
for f in sorted(os.listdir(".")):
    if not f.endswith(".py"):
        continue
    src = io.open(f, encoding="utf-8", errors="replace").read()
    try:
        tree = ast.parse(src)
    except SyntaxError:
        continue
    scratch = helper_scratch(tree, src)
    if not scratch:
        continue
    scanned += 1
    #  everything any helper clobbers, EXCLUDING each ld's own declared destination parameter
    clob = set()
    for name, regs in scratch.items():
        clob |= regs
    tg = ld_targets(src)
    bad = [(r, i, t) for (r, i, t) in tg if r in clob]
    summary = " ".join(sorted(clob))
    if bad:
        hazards += 1
        print("%-34s %-28s *** %d ld() TARGET A CLOBBERED REG ***" % (f, summary[:28], len(bad)))
        for r, i, t in bad[:6]:
            print("        line %-5d -> %-4s   %s" % (i, r, t))
    else:
        print("%-34s %-28s clean" % (f, summary[:28]))

print("")
print("probes scanned: %d    with a hazard: %d" % (scanned, hazards))
print("REGCENSUS_%s" % ("CLEAN" if hazards == 0 else "HAZARD"))
