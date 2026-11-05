#!/usr/bin/env python3
"""qhs_variants_11.py -- test-variant TABLE 11 for qhslowifetch (repair 10: 177 rows; no product change since repair 5), 2026-11-05.
Table 10's 74 (qhs_variants_10.py, imported) plus repair 10's five (b10_variant.py's text, MEASURED on the 153-row probe first,
B123_NOTE.md's repair-10 section), each ONE exact edit against r7_20261105/cpu_ppc_instr.c.fix7 (== GXEMUL-SEC):
  R10_tog_srr0_meun                     an SRR0 toggle gated on MSR[ME] and pc != addr (pass 9's B1)
  R10_tog_srr0_me1 / _me2 / _me3        the same gated on MSR[ME] and pc's low bits 01 / 10 / 11 (its isolated members)
  R10_tog_srr0_2                        an SRR0 toggle on low bits 10 (R2: `T blr o2 srr0`'s own named variant)
  qhs_variants_11.py list | apply <name> <in> <out> | pretable      (run it with python -B: it imports the earlier tables' modules)"""
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


q10 = _load("q10", os.path.join(HERE, "qhs_variants_10.py"))
b10 = _load("b10", os.path.join(HERE, "b10_variant.py"))
NL = chr(10)
SES_NEW = ["T_blr_m1", "T_blr_m2", "T_blr_m3"]
SESSIONS = q10.SESSIONS + SES_NEW
NEWV = [
    ("R10_tog_srr0_meun", ["T_blr_m1_srr0", "T_blr_m2_srr0", "T_blr_m3_srr0"],
     "pass 9's B1: cancels on `T ra o1m`/`o2m`/`o3m`, seen once by `T blr m1`/`m2`/`m3` (153/153 on the 153-row probe)"),
    ("R10_tog_srr0_me1", ["T_blr_m1_srr0"], "B1 at 01 only: `T blr m1` (153/153 before)"),
    ("R10_tog_srr0_me2", ["T_blr_m2_srr0"], "B1 at 10 only: `T blr m2` (153/153 before)"),
    ("R10_tog_srr0_me3", ["T_blr_m3_srr0"], "B1 at 11 only: `T blr m3` (153/153 before)"),
    ("R10_tog_srr0_2", ["T_blr_o2_srr0", "T_blr_m2_srr0"],
     "R2: the 10 toggle, any ME -- the two one-entry 10 sessions (152/153 before, T_blr_o2_srr0)"),
]
V = list(q10.V) + [(n, b10.EDITS[n]) for n, _, _ in NEWV]
NEW_ROWS = ["%s_%s" % (t, k) for t in SES_NEW for k in ("session", "pc", "nonex", "srr0", "msr", "chkstop", "unimpl", "lr")]
HEAD_NEW_RED = ["%s_%s" % (t, k) for t in SES_NEW for k in ("session", "pc", "srr0", "msr", "lr")]
GREEN10 = q10.GREEN9
# The failure-test narrowings' sessions, widened by the new ME-set, non-read-ahead, unaligned one-entry sessions where the conjunct
# refuses their fetch: && !ME refuses them, && translation_readahead refuses them; && ME and && pc != addr do not.
WITHIN = dict(q10.WITHIN)
WITHIN["R7b_f_meclr"] = WITHIN["R7b_f_meclr"] + SES_NEW
WITHIN["R7b_f_ra"] = WITHIN["R7b_f_ra"] + SES_NEW


def scores10():
    m = {}
    for line in io.open(os.path.join(HERE, "table10", "SCORES.txt"), encoding="utf-8"):
        p = line.split()
        if len(p) > 1 and "RED=" in line:
            red = line.rsplit("RED=", 1)[1].strip()
            m[p[0]] = [] if red == "none" else red.split(",")
    return m


def pretable():
    m10 = scores10()
    head = m10["HEAD"] + HEAD_NEW_RED
    out = [
        "PRETABLE_11 -- qhslowifetch, test-variant table 11 (repair 10: 177 rows).  Written BEFORE table 11 runs (this file's mtime",
        "precedes table11/'s outputs).  Instrument: table11/probe177_frozen.py (== base177/probe177_run.py, 177/177 on build/).  Baseline:",
        "fix7.  Table 10's 74 are predicted AT LEAST their table-10 red sets, except the build-dependent W5_dec_tail, D7_dom_run,",
        "V7_fail_inv and D12_else_ra (RED, rows not predicted), V12_fail_ra (NOT PREDICTED) and the four failure-test narrowings (RED",
        "WITHIN their sessions -- R7b_f_meclr's and R7b_f_ra's now include `T blr m1`, `m2` and `m3`, whose ME-set, non-read-ahead",
        "fetches they refuse); the fourteen green in table 10 are predicted GREEN.  The 24 new rows are informational for the 74.",
        "Repair 10's five are predicted EXACTLY.",
        "base: 177/177 CONTROL=OK SYMPTOM=ABSENT.  HEAD: table 10's HEAD set + `T blr m1` / `m2` / `m3`'s session, pc, srr0, msr and lr",
        "rows (the pre-fix build exits on their fetch after one halt report, as on `T blr`) = %d red -> %d/177 (%d rows red)," % (
            len(head), 177 - len(head), len(head)),
        "CONTROL=OK, SYMPTOM=PRESENT.  Null media, exactly: null_true 70/177 (table 10's 61 + each new session's session, chkstop and",
        "unimpl rows), null_absent 48/177 and null_false 49/177 (table 10's 42 and 43 + each new session's chkstop and unimpl rows) --",
        "CONTROL=FAIL, SYMPTOM=ABSENT on all three.",
        "CHANNELS for the new rows: as `T blr`'s, with msr = 0x1000, at pc 0x02040005 / 0x02040006 / 0x02040007: one entry into the block",
        "with ME set, so a toggle gated on ME and pc's low bits shows in srr0 / msr instead of cancelling.",
        "", "VARIANTS:"]
    new = dict((a, (r, w)) for a, r, w in NEWV)
    for n, _ in V:
        if n in new:
            rows, why = new[n]
            out.append("   %-14s exactly: %s   (%s)" % (n, ",".join(rows), why))
        elif n == "V12_fail_ra":
            out.append("   %-14s NOT PREDICTED" % n)
        elif n in q10.q9.q8.q7.BUILD_DEP:
            out.append("   %-14s RED (build-dependent rows; not predicted)" % n)
        elif n in WITHIN:
            out.append("   %-14s RED within: %s   (rows not predicted: stale-ib decode)" % (n, ",".join(WITHIN[n])))
        elif n in GREEN10:
            assert m10.get(n) == [], (n, m10.get(n))
            out.append("   %-14s at least: none -- predicted GREEN (green in table 10)" % n)
        else:
            assert m10.get(n), n
            out.append("   %-14s at least: %s" % (n, ",".join(m10[n])))
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
