#!/usr/bin/env python3
"""latchcov.py <probe> -- OFFLINE, LATCH-AWARE re-derivation of the grid's G1 table.
grid_cov() asks: is there an observation whose WANT bit == pol while the wrong source differs?
This adds the axis the contract names ("with the latch clear or set"): an observation is
LATCH-CLEAR if no decline precedes it in its session (the site's latch is set by the first
decline; accepts never touch it).  Reports, per path, the uncovered (outcome, latch, bit, pol)
cells for bits 31:5 only (the contract bullet's bits), for the SHIPPED order and for a
zero-cost REORDER that moves one existing p2 accept and the p2 complement decline to the front
of each restore session."""
import io
import sys

src = io.open(sys.argv[1], newline="").read()
a = src.index("MODELLED = (0x10, 0x11, 0x12, 0x13, 0x17, 0x1B, 0x1F)")
b = src.index('GRID_SITE = {"msr": "msr_imm"')
keep, skip = [], False
for ln in src[a:b].split("\n"):
    if ln.startswith(("WORDS[", "GRID_CHECK", "GBAD", 'for k in ("ldm_r6_pc_s",)')):
        skip = True
    if skip and (ln.startswith("HI1") or ln.startswith("def ")):
        skip = False
    if not skip:
        keep.append(ln)
ns = {}
exec("\n".join(keep), ns)


def cells(obs):
    """{(outcome, latch, bit, pol)} covered, bits 5..31, wrong source = OLD (keep-old / OR-old) or
    a forced constant (force-1 needs WANT 0, force-0 needs WANT 1).  Reported separately:
    keep-old cells need OLD != pol; force cells need only WANT == pol."""
    keepold, forced = set(), set()
    latch = "clear"
    for kind, lab, old, new, want in obs:
        if kind in ("acc", "dec"):
            for bit in range(5, 32):
                pol = (want >> bit) & 1
                forced.add((kind, latch, bit, pol))
                if ((old >> bit) & 1) != pol:
                    keepold.add((kind, latch, bit, pol))
        if kind == "dec":
            latch = "set"
    return keepold, forced


def missing(obs, path):
    ko, fo = cells(obs)
    out = []
    for kind in ("acc", "dec"):
        for latch in ("clear", "set"):
            fm = [b for b in range(5, 32) for p in (0, 1) if (kind, latch, b, p) not in fo
                  and not (b == 5 and p == 0 and False)]
            #  force-1 cells are (pol 0); force-0 cells are (pol 1)
            f1 = sorted(b for b in range(5, 32) if (kind, latch, b, 0) not in fo)
            f0 = sorted(b for b in range(5, 32) if (kind, latch, b, 1) not in fo)
            out.append("  %s %-4s %-6s force-1 missing bits %s ; force-0 missing bits %s"
                       % (path, kind, latch, rng(f1), rng(f0)))
    return out


def rng(bits):
    if not bits:
        return "none"
    s, out = bits[0], []
    p = s
    for x in bits[1:] + [None]:
        if x is not None and x == p + 1:
            p = x
            continue
        out.append("%d" % s if s == p else "%d-%d" % (s, p))
        if x is not None:
            s = p = x
    return ",".join(out)


def reorder(obs):
    """Move the FIRST p2 accept (OLD = 0xffffffc0|lab) and the FIRST p2 decline to the front,
    accept first.  Multiset unchanged."""
    o = list(obs)
    ia = next(i for i, x in enumerate(o) if x[0] == "acc" and x[2] >> 6 == 0x3FFFFFF)
    acc = o.pop(ia)
    idd = next(i for i, x in enumerate(o) if x[0] == "dec" and x[2] >> 6 == 0x3FFFFFF)
    dec = o.pop(idd)
    return [acc, dec] + o


for path in ("msr", "dpi", "pop"):
    obs = ns["grid_obs"](path)
    print("SHIPPED order, path %s (%d obs; first = %s %s OLD %08x NEW %08x)"
          % (path, len(obs), obs[0][0], hex(obs[0][1]), obs[0][2], obs[0][3]))
    print("\n".join(missing(obs, path)))
for path in ("dpi", "pop"):
    obs = reorder(ns["grid_obs"](path))
    print("REORDERED (p2 accept, p2 decline first), path %s (%d obs; multiset %s)"
          % (path, len(obs), "unchanged" if sorted(obs) == sorted(ns["grid_obs"](path)) else "CHANGED"))
    print("\n".join(missing(obs, path)))
print("LATCHCOV_DONE")
