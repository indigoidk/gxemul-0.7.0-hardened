#!/usr/bin/env python3
"""qhs_variants_10.py -- test-variant TABLE 10 for qhslowifetch (repair 9: 153 rows; no product change since repair 5), 2026-11-05.
Table 9's 69 (qhs_variants_9.py, imported) plus repair 9's five (b9_variant.py's text, MEASURED on the 137-row probe first,
B123_NOTE.md's repair-9 section), each ONE exact edit against r7_20261105/cpu_ppc_instr.c.fix7 (== GXEMUL-SEC):
  R9_tog_me1 / R9_tog_me2 / R9_tog_me0 / R9_tog_me3 -- `if ((cpu->pc & 3) == k) cpu->cd.ppc.msr ^= PPC_MSR_ME;` at the top of the
      failed-read block, k = 1 (pass 8's B1), 2 (its `== 2` form), 0 and 3 (the family's other members);
  R9_tog_srr0_1 -- `if ((cpu->pc & 3) == 1) cpu->cd.ppc.spr[SPR_SRR0] ^= 0x100;` (the same cancellation on another state).
  qhs_variants_10.py list | apply <name> <in> <out> | pretable      (run it with python -B: it imports the earlier tables' modules)"""
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


q9 = _load("q9", os.path.join(HERE, "qhs_variants_9.py"))
b9 = _load("b9", os.path.join(HERE, "b9_variant.py"))
NL = chr(10)
SESSIONS = q9.SESSIONS + ["T_blr_o1", "T_blr_o2"]
NEWV = [
    ("R9_tog_me1", ["T_blr_o1_msr"], "pass 8's B1: cancels on `T ra odd`/`T ra o1m`, seen once by `T blr o1` (137/137 on the 137-row probe)"),
    ("R9_tog_me2", ["T_blr_o2_msr"], "B1's `== 2` form: cancels on `T ra o2`/`T ra o2m`, seen once by `T blr o2` (137/137 before)"),
    ("R9_tog_me0", ["T_cont_msr", "T_step_msr", "T_me_msr", "again_msr"],
     "the aligned member: the one-entry 0x02040000 sessions see it (133/137 before -- the 00 one-entry cell already existed)"),
    ("R9_tog_me3", ["T_blr_msr"], "the 11 member: `T blr` sees it (136/137 before)"),
    ("R9_tog_srr0_1", ["T_blr_o1_srr0"], "an SRR0 toggle at 01: cancels on the read-ahead sessions, seen once by `T blr o1` (137/137 before)"),
]
V = list(q9.V) + [(n, b9.EDITS[n]) for n, _, _ in NEWV]
SES_NEW = ["T_blr_o1", "T_blr_o2"]
NEW_ROWS = ["%s_%s" % (t, k) for t in SES_NEW for k in ("session", "pc", "nonex", "srr0", "msr", "chkstop", "unimpl", "lr")]
HEAD_NEW_RED = ["%s_%s" % (t, k) for t in SES_NEW for k in ("session", "pc", "srr0", "msr", "lr")]
GREEN9 = q9.GREEN8
# The failure-test narrowings' sessions, widened by the new one-entry sessions where the conjunct refuses their fetch (ME clear,
# not read-ahead, unaligned): && ME refuses them, && translation_readahead refuses them; && !ME and && pc != addr do not.
WITHIN = dict(q9.WITHIN)
WITHIN["R7b_f_me"] = WITHIN["R7b_f_me"] + SES_NEW
WITHIN["R7b_f_ra"] = WITHIN["R7b_f_ra"] + SES_NEW


def scores9():
    m = {}
    for line in io.open(os.path.join(HERE, "table9", "SCORES.txt"), encoding="utf-8"):
        p = line.split()
        if len(p) > 1 and "RED=" in line:
            red = line.rsplit("RED=", 1)[1].strip()
            m[p[0]] = [] if red == "none" else red.split(",")
    return m


def pretable():
    m9 = scores9()
    head = m9["HEAD"] + HEAD_NEW_RED
    out = [
        "PRETABLE_10 -- qhslowifetch, test-variant table 10 (repair 9: 153 rows).  Written BEFORE table 10 runs (this file's mtime",
        "precedes table10/'s outputs).  Instrument: table10/probe153_frozen.py (== base153/probe153_run.py, 153/153 on build/).  Baseline:",
        "fix7.  Table 9's 69 are predicted AT LEAST their table-9 red sets, except the build-dependent W5_dec_tail, D7_dom_run,",
        "V7_fail_inv and D12_else_ra (RED, rows not predicted), V12_fail_ra (NOT PREDICTED) and the four failure-test narrowings (RED",
        "WITHIN their sessions -- R7b_f_me's and R7b_f_ra's now include `T blr o1` and `T blr o2`, whose ME-clear, non-read-ahead",
        "fetches they refuse); the fourteen green in table 9 are predicted GREEN.  The 16 new rows are informational for the 69.  Repair",
        "9's five are predicted EXACTLY.",
        "base: 153/153 CONTROL=OK SYMPTOM=ABSENT.  HEAD: table 9's HEAD set + `T blr o1` / `T blr o2`'s session, pc, srr0, msr and lr rows",
        "(the pre-fix build exits on their fetch after one halt report, as on `T blr`: no registers, while nonex, chkstop and unimpl stay",
        "green) = %d red -> %d/153 (%d rows red), CONTROL=OK, SYMPTOM=PRESENT." % (len(head), 153 - len(head), len(head)),
        "Null media, exactly: null_true 61/153 (table 9's 55 + each new session's session, chkstop and unimpl rows), null_absent 42/153",
        "and null_false 43/153 (table 9's 38 and 39 + each new session's chkstop and unimpl rows) -- CONTROL=FAIL, SYMPTOM=ABSENT on all.",
        "CHANNELS for the new rows: as `T blr`'s, at pc 0x02040005 (01) and 0x02040006 (10): one entry into the block, so a toggle the",
        "block makes on pc's low bits shows in msr / srr0 instead of cancelling.",
        "", "VARIANTS:"]
    new = dict((a, (r, w)) for a, r, w in NEWV)
    for n, _ in V:
        if n in new:
            rows, why = new[n]
            out.append("   %-14s exactly: %s   (%s)" % (n, ",".join(rows), why))
        elif n == "V12_fail_ra":
            out.append("   %-14s NOT PREDICTED" % n)
        elif n in q9.q8.q7.BUILD_DEP:
            out.append("   %-14s RED (build-dependent rows; not predicted)" % n)
        elif n in WITHIN:
            out.append("   %-14s RED within: %s   (rows not predicted: stale-ib decode)" % (n, ",".join(WITHIN[n])))
        elif n in GREEN9:
            assert m9.get(n) == [], (n, m9.get(n))
            out.append("   %-14s at least: none -- predicted GREEN (green in table 9)" % n)
        else:
            assert m9.get(n), n
            out.append("   %-14s at least: %s" % (n, ",".join(m9[n])))
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
