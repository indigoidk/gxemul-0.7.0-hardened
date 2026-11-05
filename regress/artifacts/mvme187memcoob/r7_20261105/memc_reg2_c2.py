#!/usr/bin/env python3
"""memc_reg2_c2.py -- MODEL-ONLY follow-up to memc_reg2_check.py, item C: for each NOCHANGE group whose representative table 6
MEASURED red, does every member of the repair path's own shape (memc_members_213.py's test) have the SAME observable trace as its
representative on the 213-row instrument?  That is table 5's EQUIV rule (memc_variants_5.py, Walk: "the same observable trace as
their representative on every probe access"), applied to the 213 rows.  Prints each such member and the verdict.
Usage: python3 -I memc_reg2_c2.py >> REG2_CHECK.txt
"""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
MD = os.path.dirname(HERE)
P213 = os.path.join(HERE, "table6", "probe213_frozen.py")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


mv5 = load("mv5", os.path.join(MD, "r5_20261105", "memc_variants_5.py"))
mem = load("mem213", os.path.join(HERE, "memc_members_213.py"))
rec = []
mv5.exec_probe(P213, {}, record=rec)


def trace213(cell):
    fake = mv5.Fake({"cell": cell})
    return tuple(fake.run_one(argv, inp) for argv, inp in rec)


def main():
    w = mv5.walk()
    noch = {}
    for (sk, devs), members in w.green_groups.items():
        rep = sorted(members, key=mv5.cell_rank)[0]
        if devs and not w.changed_of[rep.key()]:
            noch.setdefault(mv5.stmt_key(rep), []).extend(members)
    red6 = set()
    for line in open(os.path.join(HERE, "table6", "SCORES.txt"), encoding="utf-8"):
        p = line.split()
        if p[3] != "213/213":
            red6.add(p[0])
    out = ["", "C2. Own-shape members of the NOCHANGE groups whose representative table 6 MEASURED red -- same 213-row trace as the",
           "    representative (table 5's EQUIV rule)?  MODEL ONLY."]
    n = same = 0
    for sk, members in sorted(noch.items(), key=lambda kv: mv5.stmt_name(kv[0])):
        rep = sorted(members, key=mv5.cell_rank)[0]
        if rep.name() not in red6:
            continue
        tr = trace213(rep)
        for c in members:
            if c is rep or not mem.own_shape(c):
                continue
            n += 1
            eq = trace213(c) == tr
            same += eq
            out.append("    %-24s member %-24s %s" % (rep.name(), c.name(), "SAME trace" if eq else "DIFFERENT trace"))
    out.append("    own-shape members: %d; with the representative's trace: %d" % (n, same))
    out.append("REG2_CHECK_C2_DONE")
    print("\n".join(out))


if __name__ == "__main__":
    main()
