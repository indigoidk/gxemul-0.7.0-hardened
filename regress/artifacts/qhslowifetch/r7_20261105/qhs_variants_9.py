#!/usr/bin/env python3
"""qhs_variants_9.py -- test-variant TABLE 9 for qhslowifetch (repair 8: 137 rows; no product change since repair 5), 2026-11-05.
Table 8's 67 (qhs_variants_8.py, imported) plus repair 8's two (b8_variant.py's text, MEASURED on the 129-row probe first,
B123_NOTE.md's repair-8 section), each ONE exact edit against r7_20261105/cpu_ppc_instr.c.fix7 (== GXEMUL-SEC):
  R8_c_meun_bad  arm (c) sends a halt with MSR[ME] set at pc != addr to bad: (pass 7's F1)
  R8_c_clun_bad  the same with MSR[ME] clear (F1's mirror)
  qhs_variants_9.py list | apply <name> <in> <out> | pretable      (run it with python -B: it imports the earlier tables' modules)"""
import importlib.util
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


q8 = _load("q8", os.path.join(HERE, "qhs_variants_8.py"))
b8 = _load("b8", os.path.join(HERE, "b8_variant.py"))
NL = chr(10)
SESSIONS = q8.SESSIONS
NEWV = [
    ("R8_c_meun_bad", ["T_ra_o1m_unimpl", "T_ra_o2m_unimpl", "T_ra_o3m_unimpl"],
     "pass 7's F1: the three unaligned ME-set real fetches go to bad: and print UNIMPLEMENTED (129/129 on the 129-row probe)"),
    ("R8_c_clun_bad", ["T_ra_odd_unimpl", "T_ra_o2_unimpl", "T_ra_o3_unimpl", "T_blr_unimpl"],
     "its mirror: the three unaligned ME-clear real fetches and T blr's fetch (128/129 on the 129-row probe, T_blr_unimpl)"),
]
V = list(q8.V) + [(n, b8.EDITS[n]) for n, _, _ in NEWV]
NEW_ROWS = ["T_ra_unimpl", "T_ra_me_unimpl"] + ["T_ra_%s_unimpl" % c for c in q8.UNAL]
HEAD_NEW_RED = []
GREEN8 = q8.GREEN7 + ("R7b_a_runun",)
WITHIN = dict((n, r) for n, k, r, _ in q8.NEWV if k == "within")


def scores8():
    m = {}
    for line in io.open(os.path.join(HERE, "table8", "SCORES.txt"), encoding="utf-8"):
        p = line.split()
        if len(p) > 1 and "RED=" in line:
            red = line.rsplit("RED=", 1)[1].strip()
            m[p[0]] = [] if red == "none" else red.split(",")
    return m


def pretable():
    m8 = scores8()
    head = m8["HEAD"] + HEAD_NEW_RED
    out = [
        "PRETABLE_9 -- qhslowifetch, test-variant table 9 (repair 8: 137 rows).  Written BEFORE table 9 runs (this file's mtime precedes",
        "table9/'s outputs).  Instrument: table9/probe137_frozen.py (== base137/probe137_run.py, 137/137 on build/).  Baseline: fix7.",
        "Table 8's 67 are predicted AT LEAST their table-8 red sets, except the build-dependent W5_dec_tail, D7_dom_run, V7_fail_inv and",
        "D12_else_ra (RED, rows not predicted), V12_fail_ra (NOT PREDICTED) and the four failure-test narrowings (RED WITHIN their",
        "table-8 sessions, rows stack-decided); the fourteen green in table 8 are predicted GREEN.  The 8 new unimpl rows are",
        "informational for the 67.  Repair 8's two are predicted EXACTLY.",
        "base: 137/137 CONTROL=OK SYMPTOM=ABSENT.  HEAD: table 8's HEAD set unchanged (the pre-fix build exits at the read-ahead fetch",
        "with `read failed: TODO`, not UNIMPLEMENTED, so the eight new unimpl rows stay green) = %d red -> %d/137 (%d rows red)," % (
            len(head), 137 - len(head), len(head)),
        "CONTROL=OK, SYMPTOM=PRESENT.  Null media, exactly: null_true 55/137, null_absent 38/137, null_false 39/137 (table 8's 47, 30",
        "and 31 + the eight unimpl rows, which read `absent` from an empty transcript) -- CONTROL=FAIL, SYMPTOM=ABSENT on all three.",
        "CHANNEL for the new rows: T_ra_<cell>_unimpl is the UNIMPLEMENTED text, which only bad: prints on these sessions (on the fix",
        "it appears in isi, isi1 and noT only -- b8_table/).",
        "", "VARIANTS:"]
    new = dict((a, (r, w)) for a, r, w in NEWV)
    for n, _ in V:
        if n in new:
            rows, why = new[n]
            out.append("   %-14s exactly: %s   (%s)" % (n, ",".join(rows), why))
        elif n == "V12_fail_ra":
            out.append("   %-14s NOT PREDICTED" % n)
        elif n in q8.q7.BUILD_DEP:
            out.append("   %-14s RED (build-dependent rows; not predicted)" % n)
        elif n in WITHIN:
            out.append("   %-14s RED within: %s   (rows not predicted: stale-ib decode)" % (n, ",".join(WITHIN[n])))
        elif n in GREEN8:
            assert m8.get(n) == [], (n, m8.get(n))
            out.append("   %-14s at least: none -- predicted GREEN (green in table 8)" % n)
        else:
            assert m8.get(n), n
            out.append("   %-14s at least: %s" % (n, ",".join(m8[n])))
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
