#!/usr/bin/env python3
"""qhs_variants_4.py -- test-variant TABLE 4 for the qhslowifetch detector (repair 4: 69 rows), 2026-11-05, as ruled by the repair-pass-3
adjudication (p3_20261105/ADJ_MYTHOS.md): table 3's 32 variants (r3_20261105/qhs_variants_3.py) and the four of GPT-6 Astra's pass-3
findings (p3_20261105/p3_variants.py: B1a, B1b, B1c, B2), on ONE instrument at the final row count.  Baseline:
r3_20261105/cpu_ppc_instr.c.fix4 (== GXEMUL-SEC).  Instrument: table4/probe69_frozen.py.
  qhs_variants_4.py list | apply <name> <in> <out> | pretable"""
import importlib.util
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
QD = os.path.dirname(HERE)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


v3 = load("qv3", os.path.join(QD, "r3_20261105", "qhs_variants_3.py"))
p3 = load("qp3", os.path.join(QD, "p3_20261105", "p3_variants.py"))
NL = chr(10)
V = [(n, e) for n, e, _, _, _ in v3.V] + [(n, e) for n, e, _ in p3.V]
NEW_ROWS = ["T_cont_msr", "T_step_msr", "T_me_msr", "again_msr", "T_ra_msr", "T_ra_chkstop", "T_ra_me_msr"]
EXACT_NEW = {"B1a_c_meclr": ["T_me_msr", "T_ra_me_msr"], "B1b_a_meclr": ["T_ra_me_msr"],
             "B1c_c_meset": ["T_cont_msr", "T_step_msr", "again_msr", "T_ra_msr"], "B2_ra_chktext": ["T_ra_chkstop"]}


def measured3():
    out = {}
    for line in io.open(os.path.join(QD, "r3_20261105", "table3", "SCORES.txt"), encoding="utf-8"):
        p = line.split()
        if len(p) > 1 and "RED=" in line:
            red = line.rsplit("RED=", 1)[1].strip()
            out[p[0]] = [] if red == "none" else red.split(",")
    return out


def pretable():
    m3 = measured3()
    out = [
        "PRETABLE_4 -- qhslowifetch detector, test-variant table 4 (repair 4, 69 rows).  Written BEFORE table 4 runs (this file's mtime",
        "precedes table4/'s).  Instrument: table4/probe69_frozen.py, frozen from regress/ppc_ifetch_probe.py after apply_r4_rows.py (62 rows",
        "+ T cont msr, T step msr, T me msr, again msr, T ra msr, T ra chkstop, T ra me msr); base on the build tree 69/69",
        "(r4_20261105/base69_build.out).  Baseline r3_20261105/cpu_ppc_instr.c.fix4.  Legs first in the same clone: base, HEAD, null media.",
        "",
        "THE FOUR CHECKS for the seven rows (p3_20261105/ADJ_MYTHOS.md F1, F2):",
        "  SIBLING PARITY -- every -T session (T cont, T step, T me, again, T ra, T ra me) now pins the final MSR; T ra now pins the",
        "    checkstop channel its sibling T ra me pinned.",
        "  CLAIM -> ROW -- 'the park leaves MSR as it was' -> the six msr rows; 'no checkstop on the read-ahead route' -> T ra chkstop.",
        "  GUARD FIELD vs BODY FIELD -- MSR[ME] is read by arm (d) and is the one footprint field session() parsed and no row read; the",
        "    block's other footprint fields (pc, next_ic via the park, running via stopped/nonex, SRR0) were already rowed.",
        "  CHANNEL -- msr rows: B1a (ME cleared in arm (c)) moves T me / T ra me msr 0x1000 -> 0; B1b (cleared in arm (a)) moves T ra me;",
        "    B1c (set in arm (c)) moves the four ME-clear sessions 0 -> 0x1000; T ra chkstop: B2 prints the line on T ra.",
        "",
        "PREDICTIONS.  The four B variants: EXACTLY the rows named (p3's table_p3 measured their edits live and every old row green).",
        "Table 3's 32: AT LEAST their table-3 red sets (r3_20261105/table3/SCORES.txt), except V12, which is NOT PREDICTED (its outcome is",
        "decided by the stale stack word; p3 ruling F4).  The seven new rows on the 32 are informational: an exception-delivering variant",
        "may also move an msr row (ppc_exception's MSR update), and that would be a further catch, not a defect.",
        "HEAD leg: table 3's HEAD set + the six msr rows (every -T session exits before `reg`) = 32 red -> 37/69, SYMPTOM=PRESENT.",
        "Null media: CONTROL=FAIL each.",
        "",
        "VARIANTS (name, predicted red rows):",
    ]
    for n, _ in V:
        if n in EXACT_NEW:
            out.append("   %-14s exactly: %s -> %d/69" % (n, ",".join(EXACT_NEW[n]), 69 - len(EXACT_NEW[n])))
        elif n == "V12_fail_ra":
            out.append("   %-14s NOT PREDICTED (table 3: %s)" % (n, ",".join(m3.get(n, [])) or "none"))
        else:
            r = m3.get(n, [])
            out.append("   %-14s at least: %s" % (n, ",".join(r) if r else "none (green in table 3; predicted green)"))
    out.append("   HEAD leg       exactly: table 3's HEAD set + T_cont_msr,T_step_msr,T_me_msr,again_msr,T_ra_msr,T_ra_me_msr -> 37/69")
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
