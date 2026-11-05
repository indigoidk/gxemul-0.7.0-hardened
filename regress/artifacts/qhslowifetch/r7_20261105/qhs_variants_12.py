#!/usr/bin/env python3
"""qhs_variants_12.py -- test-variant TABLE 12 for qhslowifetch (repair 11: 249 rows; no product change since repair 5), 2026-11-05.
Table 11's 79 (qhs_variants_11.py, imported) plus repair 11's nine (b11_variant.py's text, MEASURED on the 177-row probe first,
B123_NOTE.md's repair-11 section), each ONE exact edit against r7_20261105/cpu_ppc_instr.c.fix7 (== GXEMUL-SEC):
  R11_tog_full          an SRR0 toggle gated on (pc & ~0xb) != addr (pass 10's B1)
  R11_tog_full_<k><e>   the same also gated on (pc & 3) == k and ME clear (c) or set (m): one per read-ahead cell
  qhs_variants_12.py list | apply <name> <in> <out> | pretable      (run it with python -B: it imports the earlier tables' modules)"""
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


q11 = _load("q11", os.path.join(HERE, "qhs_variants_11.py"))
b11 = _load("b11", os.path.join(HERE, "b11_variant.py"))
NL = chr(10)
CELLS = [("", 0, "c"), ("me", 0, "m"), ("odd", 1, "c"), ("o1m", 1, "m"), ("o2", 2, "c"), ("o2m", 2, "m"), ("o3", 3, "c"),
         ("o3m", 3, "m")]
PART = ["T_rp" + ("_" + t if t else "") for t, _, _ in CELLS]
SESSIONS = q11.SESSIONS + PART
NEWV = [("R11_tog_full", [p + "_srr0" for p in PART],
         "pass 10's B1: cancels on every read-ahead session, never fires on the 0x0204000x one-entry sessions, fires once on each "
         "partner (177/177 on the 177-row probe)")]
for (t, k, e), p in zip(CELLS, PART):
    NEWV.append(("R11_tog_full_%d%s" % (k, e), [p + "_srr0"], "B1 in the %s cell only: its partner (177/177 before)" % (
        ("T ra " + t).rstrip())))
V = list(q11.V) + [(n, b11.EDITS[n]) for n, _, _ in NEWV]
NEW_ROWS = ["%s_%s" % (p, k) for p in PART for k in ("session", "pc", "nonex", "addr", "stopped", "msr", "chkstop", "srr0", "unimpl")]
HEAD_NEW_RED = ["%s_%s" % (p, k) for p in PART for k in ("session", "pc", "stopped", "msr", "srr0")]
GREEN11 = q11.GREEN10
ME_CLEAR = [p for (t, k, e), p in zip(CELLS, PART) if e == "c"]
ME_SET = [p for (t, k, e), p in zip(CELLS, PART) if e == "m"]
ALIGNED = ["T_rp", "T_rp_me"]
# The failure-test narrowings' sessions, widened by the partners whose fetch each refuses: && ME refuses the ME-clear partners,
# && !ME the ME-set ones, && translation_readahead all eight (each partner's one fetch is not read-ahead), && pc != addr the aligned two.
WITHIN = dict(q11.WITHIN)
WITHIN["R7b_f_me"] = WITHIN["R7b_f_me"] + ME_CLEAR
WITHIN["R7b_f_meclr"] = WITHIN["R7b_f_meclr"] + ME_SET
WITHIN["R7b_f_ra"] = WITHIN["R7b_f_ra"] + PART
WITHIN["R7b_f_unal"] = WITHIN["R7b_f_unal"] + ALIGNED


def scores11():
    m = {}
    for line in io.open(os.path.join(HERE, "table11", "SCORES.txt"), encoding="utf-8"):
        p = line.split()
        if len(p) > 1 and "RED=" in line:
            red = line.rsplit("RED=", 1)[1].strip()
            m[p[0]] = [] if red == "none" else red.split(",")
    return m


def pretable():
    m11 = scores11()
    head = m11["HEAD"] + HEAD_NEW_RED
    out = [
        "PRETABLE_12 -- qhslowifetch, test-variant table 12 (repair 11: 249 rows).  Written BEFORE table 12 runs (this file's mtime",
        "precedes table12/'s outputs).  Instrument: table12/probe249_frozen.py (== base249/probe249_run.py, 249/249 on build/; its",
        "pairing check base249/PAIRS.out, PAIRS_OK=8/8).  Baseline: fix7.  Table 11's 79 are predicted AT LEAST their table-11 red sets,",
        "except the build-dependent W5_dec_tail, D7_dom_run, V7_fail_inv and D12_else_ra (RED, rows not predicted), V12_fail_ra (NOT",
        "PREDICTED) and the four failure-test narrowings (RED WITHIN their sessions, widened by the partners whose fetch each refuses);",
        "the fourteen green in table 11 are predicted GREEN.  The 72 new rows are informational for the 79.  Repair 11's nine are",
        "predicted EXACTLY.",
        "base: 249/249 CONTROL=OK SYMPTOM=ABSENT.  HEAD: table 11's HEAD set + each partner's session, pc, stopped, msr and srr0 rows",
        "(the pre-fix build prints the one halt report naming 0xfec00008 and exits, so nonex, addr, chkstop and unimpl stay green) = %d"
        % len(head),
        "red -> %d/249 (%d rows red), CONTROL=OK, SYMPTOM=PRESENT.  Null media, exactly: null_true 94/249 (table 11's 70 + each" % (
            249 - len(head), len(head)),
        "partner's session, chkstop and unimpl rows), null_absent 64/249 and null_false 65/249 (table 11's 48 and 49 + each partner's",
        "chkstop and unimpl rows) -- CONTROL=FAIL, SYMPTOM=ABSENT on all three.",
        "CHANNELS for the new rows: as the read-ahead cell's, for ONE entry at the same full pc and MSR: one halt report naming",
        "0xfec00008; a toggle that cancels over the two-entry session's visits shows once in the partner's srr0 / msr.",
        "", "VARIANTS:"]
    new = dict((a, (r, w)) for a, r, w in NEWV)
    for n, _ in V:
        if n in new:
            rows, why = new[n]
            out.append("   %-14s exactly: %s   (%s)" % (n, ",".join(rows), why))
        elif n == "V12_fail_ra":
            out.append("   %-14s NOT PREDICTED" % n)
        elif n in q11.q10.q9.q8.q7.BUILD_DEP:
            out.append("   %-14s RED (build-dependent rows; not predicted)" % n)
        elif n in WITHIN:
            out.append("   %-14s RED within: %s   (rows not predicted: stale-ib decode)" % (n, ",".join(WITHIN[n])))
        elif n in GREEN11:
            assert m11.get(n) == [], (n, m11.get(n))
            out.append("   %-14s at least: none -- predicted GREEN (green in table 11)" % n)
        else:
            assert m11.get(n), n
            out.append("   %-14s at least: %s" % (n, ",".join(m11[n])))
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
