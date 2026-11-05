#!/usr/bin/env python3
"""qhs_variants_6.py -- test-variant TABLE 6 for qhslowifetch (repair 6: 82 rows; no product change since repair 5), 2026-11-05.
Table 5's 42 (r5_20261105/qhs_variants_5.py, applied to this table's baseline) plus four for repair 6: R6_mask7 / R6_mask15 (the aligned
compare's mask widened to bit 2 / to bits 2-3) and R6_a_pceq / R6_a_align (arm (a)'s guard conjoined with `cpu->pc == addr` / with
`!(cpu->pc & 3)`).  Baseline: r6_20261105/cpu_ppc_instr.c.fix6 == GXEMUL-SEC (the qhs fix with repair 5, plus #575's two crandc/crorc
lines, which no qhs session executes).  qhs_variants_6.py list | apply <name> <in> <out> | pretable"""
import importlib.util
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
QD = os.path.dirname(HERE)
spec = importlib.util.spec_from_file_location("q5", os.path.join(QD, "r5_20261105", "qhs_variants_5.py"))
q5 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(q5)
T, NL = chr(9), chr(10)
BT = T * 3 + "if ((cpu->pc & ~(uint64_t)3) != addr) {" + NL
A = T * 3 + "if (cpu->translation_readahead)" + NL
NEWV = [
    ("R6_mask7", [(BT, BT.replace("~(uint64_t)3", "~(uint64_t)7"))], ["T_blr_nonex"], "the aligned compare's mask widened to bit 2"),
    ("R6_mask15", [(BT, BT.replace("~(uint64_t)3", "~(uint64_t)15"))],
     ["T_ra_nonex", "T_ra_me_nonex", "T_ra_odd_nonex", "T_blr_nonex"], "the mask widened to bits 2-3 (0xfec00008 has bit 3 set)"),
    ("R6_a_pceq", [(A, T * 3 + "if (cpu->translation_readahead && cpu->pc == addr)" + NL)], ["T_ra_odd_nonex"],
     "arm (a)'s guard conjoined with the unmasked compare"),
    ("R6_a_align", [(A, T * 3 + "if (cpu->translation_readahead && !(cpu->pc & 3))" + NL)], ["T_ra_odd_nonex"],
     "arm (a)'s guard conjoined with pc alignment"),
]
V = list(q5.V) + [(n, e) for n, e, _, _ in NEWV]


def pretable():
    m5 = {}
    for line in io.open(os.path.join(QD, "r5_20261105", "table5", "SCORES.txt"), encoding="utf-8"):
        p = line.split()
        if len(p) > 1 and "RED=" in line:
            red = line.rsplit("RED=", 1)[1].strip()
            m5[p[0]] = [] if red == "none" else red.split(",")
    head = m5["HEAD"] + ["T_ra_odd_session", "T_ra_odd_pc", "T_ra_odd_nonex"]
    out = [
        "PRETABLE_6 -- qhslowifetch, test-variant table 6 (repair 6: 82 rows).  Written BEFORE table 6 runs (this file's mtime precedes",
        "table6/'s).  Instrument: table6/probe82_frozen.py (the in-tree probe after apply_r6.py; 82/82 on build/, base82/).  Baseline: fix6.",
        "Table 5's 42 are predicted AT LEAST their table-5 red sets, except V12 (NOT PREDICTED) and D12 (BUILD-DEPENDENT: red, rows not",
        "predicted); the three `T ra odd' rows are informational for them.  Repair 6's four are predicted EXACTLY.  HEAD: table 5's HEAD",
        "set + T_ra_odd_session, T_ra_odd_pc, T_ra_odd_nonex (the pre-fix build exits at the read-ahead fetch) = %d red -> %d/82." % (
            len(head), 82 - len(head)),
        "Null media: CONTROL=FAIL.  CHANNELS: T_blr_nonex counts halt reports at r3 = 0x02040007 (addr 0x02040004): 1 when arm (c) parks,",
        "thousands when arm (b) re-runs the slot; T_ra_odd_nonex counts them for a read-ahead from 0xfec00005: 2 when arm (a) returns, 1",
        "when a conjoined guard sends the read-ahead failure to arm (c) (measured, p5_20261105/TRAODD_NOTE.md).",
        "", "VARIANTS:"]
    new = dict((a, (b, c)) for a, _, b, c in NEWV)
    for n, _ in V:
        if n in new:
            out.append("   %-14s exactly: %s   (%s)" % (n, ",".join(new[n][0]), new[n][1]))
        elif n == "V12_fail_ra":
            out.append("   %-14s NOT PREDICTED" % n)
        elif n == "D12_else_ra":
            out.append("   %-14s RED (build-dependent rows)" % n)
        else:
            out.append("   %-14s at least: %s" % (n, ",".join(m5.get(n, [])) or "none (green in table 5; predicted green)"))
    return NL.join(out) + NL


def main():
    a = sys.argv[1:]
    if a == ["list"]:
        print(" ".join(n for n, _ in V))
    elif a == ["pretable"]:
        sys.stdout.write(pretable())
    elif len(a) == 4 and a[0] == "apply":
        s = io.open(a[2], encoding="latin-1", newline="").read()
        f = dict(V)[a[1]]
        if callable(f):
            try:
                s = f(s)
            except (AssertionError, ValueError) as e:
                print("MUTANT-TEXT-NOT-FOUND", a[1], e)
                sys.exit(3)
        else:
            for old, new in f:
                if s.count(old) != 1:
                    print("MUTANT-TEXT-NOT-FOUND", a[1], repr(old[:60]), s.count(old))
                    sys.exit(3)
                s = s.replace(old, new)
        io.open(a[3], "w", encoding="latin-1", newline="").write(s)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
