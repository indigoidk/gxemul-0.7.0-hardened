#!/usr/bin/env python3
"""memc_members_213.py -- MODEL-ONLY analysis (no measurement): every cell table 5 left GREEN (PRETABLE_5's 4,299 green cells,
representatives and their EQUIV members), re-predicted on the 213-row probe (table6/probe213_frozen.py) with memc_variants_5.py's
device model, used read-only.  Table 6 measures the 665 representatives only; on the 206 rows a green representative stood for its
group because the group shared one deviation set (or, for NOCHANGE, one statement), and R18's new accesses can split a group.
Output: per PRETABLE_5 class, how many green cells the model turns red on 213 rows; and every cell still green whose shape is
the repair path's own (a latch written at a position of its own arm, gated by `any` or by direction and that arm's own latch
only; or a keep into an arm's own field under the same gates) -- the cells regress_20261105/REG_MYTHOS_local.md 2(d)'s test
would call floor.
Usage: python3 memc_members_213.py > MEMBERS_213.txt
"""
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MD = os.path.dirname(HERE)
P213 = os.path.join(HERE, "table6", "probe213_frozen.py")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


mv5 = load("mv5", os.path.join(MD, "r5_20261105", "memc_variants_5.py"))
ARM = {"MT": "M", "MW": "M", "MB": "M", "ME": "M", "DT": "D", "DB": "D", "DA": "D", "CI": "chipid", "CR": "chiprev"}
OWNFIELD = {"MT": "memconf", "MW": "memconf", "MB": "memconf", "ME": "memconf", "CI": "chipid", "CR": "chiprev"}


def own_gate(g, latch):
    if g[0] == "any":
        return True
    if g[0] != "c":
        return False
    ok = {"W", "nW"} | ({latch, "n" + latch} if latch in ("M", "D") else set())
    return all(l in ok for l in g[1])


def own_shape(c):
    if c.shape == "L" and c.P in ARM and ARM[c.P] == c.T:
        return own_gate(c.g, c.T)
    if c.shape == "K" and c.P in OWNFIELD and OWNFIELD[c.P] == c.T:
        return own_gate(c.g, ARM.get(c.P))
    return False


def main():
    w = mv5.walk()
    kind_of = {}
    for (sk, devs), members in w.green_groups.items():
        rep = sorted(members, key=mv5.cell_rank)[0]
        kind = "UNFIRED" if not devs else ("UNOBSERVED" if w.changed_of[rep.key()] else "NOCHANGE")
        for c in members:
            kind_of[c.key()] = kind
    cells = [c for ms in w.green_groups.values() for c in ms]
    print("MEMBERS_213 -- model only, no measurement.  Instrument: table6/probe213_frozen.py.  Green cells on the 206 rows: %d" % len(cells))
    tot = {}
    still_own = []
    for c in sorted(cells, key=mv5.cell_rank):
        red = mv5.predict({"cell": c}, P213)[0]
        k = kind_of[c.key()]
        t = tot.setdefault(k, [0, 0])
        t[0 if red else 1] += 1
        if not red and own_shape(c):
            still_own.append((c, k))
    for k in sorted(tot):
        print("  %-10s red on 213 rows: %4d   still green: %4d" % (k, tot[k][0], tot[k][1]))
    print("  total      red on 213 rows: %4d   still green: %4d" % (sum(v[0] for v in tot.values()), sum(v[1] for v in tot.values())))
    print("STILL GREEN AND OF THE REPAIR PATH'S OWN SHAPE (own-arm position, own target, gate `any` or direction/own latch only): %d"
          % len(still_own))
    for c, k in still_own:
        print("   %-34s %-10s %s" % (c.name(), k, c.what()))
    print("MEMBERS_213_DONE")


if __name__ == "__main__":
    main()
