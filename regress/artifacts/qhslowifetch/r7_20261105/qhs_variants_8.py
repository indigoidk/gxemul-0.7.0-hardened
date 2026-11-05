#!/usr/bin/env python3
"""qhs_variants_8.py -- test-variant TABLE 8 for qhslowifetch (repair 7b: 129 rows; no product change since repair 5), 2026-11-05.
Table 7's 59 (qhs_variants_7.py, imported) plus repair 7b's eight (b7b_variant.py's text, MEASURED on the 103-row probe first,
B123_NOTE.md's repair-7b section), each ONE exact edit against r7_20261105/cpu_ppc_instr.c.fix7 (== GXEMUL-SEC):
  R7b_a_srr0un / R7b_a_chkun / R7b_a_pcalign / R7b_a_runun -- arm (a) writing SRR0, printing the checkstop line, aligning pc or
      restoring running, each only when pc != addr;
  R7b_f_me / R7b_f_meclr / R7b_f_ra / R7b_f_unal -- the failure test conjoined with `(msr & ME)`, `!(msr & ME)`,
      `translation_readahead`, `cpu->pc != addr` (LATE_REPLICATIONS_20261105.md rows 33, 41).  A failure the conjunct refuses
      skips the block and decodes the uninitialised fetch buffer ib, so their rows are NOT predicted -- only their sessions are.
  qhs_variants_8.py list | apply <name> <in> <out> | pretable      (run it with python -B: it imports the earlier tables' modules)"""
import importlib.util
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
QD = os.path.dirname(HERE)


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


q7 = _load("q7", os.path.join(HERE, "qhs_variants_7.py"))
b7b = _load("b7b", os.path.join(HERE, "b7b_variant.py"))
NL = chr(10)
UNAL = ["odd", "o1m", "o2", "o2m", "o3", "o3m"]
SESSIONS = ["ctl", "neg", "isi", "isi1", "noT", "T_cont", "T_step", "T_me", "again", "T_ra", "T_ra_me", "T_ra_odd", "T_ra_o1m",
            "T_ra_o2", "T_ra_o2m", "T_ra_o3", "T_ra_o3m", "T_blr"]
NEWV = [
    ("R7b_a_srr0un", "exactly", ["T_ra_%s_srr0" % c for c in UNAL],
     "SRR0 written in arm (a) at pc != addr: the six unaligned srr0 rows (103/103 on the 103-row probe)"),
    ("R7b_a_chkun", "exactly", ["T_ra_%s_chkstop" % c for c in UNAL],
     "the checkstop line printed at pc != addr: the six unaligned chkstop rows (103/103 on the 103-row probe)"),
    ("R7b_a_pcalign", "exactly", ["T_ra_%s_pc" % c for c in UNAL],
     "pc aligned in arm (a): the six unaligned pc rows, the halt address unchanged (97/103 on the 103-row probe)"),
    ("R7b_a_runun", "exactly", [], "running restored at pc != addr: GREEN -- the real fetch's -T halt stops the machine anyway (R5_arun's class)"),
    ("R7b_f_me", "within", ["T_cont", "T_step", "again", "T_ra", "T_ra_odd", "T_ra_o2", "T_ra_o3", "T_blr"],
     "the ME-clear sessions whose fetch fails"),
    ("R7b_f_meclr", "within", ["T_me", "T_ra_me", "T_ra_o1m", "T_ra_o2m", "T_ra_o3m"], "the ME-set sessions whose fetch fails"),
    ("R7b_f_ra", "within", ["T_cont", "T_step", "T_me", "again", "T_blr"] + ["T_ra"] + ["T_ra_" + c for c in ["me"] + UNAL],
     "every session with a non-read-ahead failing fetch"),
    ("R7b_f_unal", "within", ["T_cont", "T_step", "T_me", "again", "T_ra", "T_ra_me"], "the aligned sessions whose fetch fails"),
]
V = list(q7.V) + [(n, b7b.EDITS[n]) for n, _, _, _ in NEWV]
NEW_ROWS = ["T_ra_me_addr", "T_ra_me_stopped"] + ["T_ra_%s_%s" % (c, k) for c in UNAL for k in ("addr", "stopped", "chkstop", "srr0")]
HEAD_NEW_RED = ["T_ra_me_stopped"] + ["T_ra_%s_%s" % (c, k) for c in UNAL for k in ("stopped", "srr0")]
GREEN7 = q7.GREEN6 + ("R7_G1_b_lt", "R7_G2_d_msr")


def scores7():
    m = {}
    for line in io.open(os.path.join(HERE, "table7", "SCORES.txt"), encoding="utf-8"):
        p = line.split()
        if len(p) > 1 and "RED=" in line:
            red = line.rsplit("RED=", 1)[1].strip()
            m[p[0]] = [] if red == "none" else red.split(",")
    return m


def pretable():
    m7 = scores7()
    head = m7["HEAD"] + HEAD_NEW_RED
    out = [
        "PRETABLE_8 -- qhslowifetch, test-variant table 8 (repair 7b: 129 rows).  Written BEFORE table 8 runs (this file's mtime precedes",
        "table8/'s outputs).  Instrument: table8/probe129_frozen.py (== base129/probe129_run.py, 129/129 on build/).  Baseline: fix7.",
        "Table 7's 59 are predicted AT LEAST their table-7 red sets, except the build-dependent W5_dec_tail, D7_dom_run, V7_fail_inv and",
        "D12_else_ra (RED, rows not predicted) and V12_fail_ra (NOT PREDICTED); the thirteen green in table 7 are predicted GREEN.  The 26",
        "new rows are informational for the 59.  Repair 7b's four arm (a) variants are predicted EXACTLY; its four failure-test",
        "narrowings are predicted RED WITHIN the listed sessions (every red row belongs to one of them, at least one row reds) -- which",
        "rows red is decided by the stale fetch buffer ib, as for W5 and D7.",
        "base: 129/129 CONTROL=OK SYMPTOM=ABSENT.  HEAD: table 7's HEAD set + the new stopped and srr0 rows (13; the pre-fix build exits",
        "at the read-ahead fetch with no stop line and no registers, while its one halt report names 0xfec00008 and no checkstop line",
        "prints, so the new addr and chkstop rows stay green) = %d red -> %d/129 (%d rows red), CONTROL=OK, SYMPTOM=PRESENT." % (
            len(head), 129 - len(head), len(head)),
        "Null media, exactly: null_true 47/129, null_absent 30/129, null_false 31/129 (table 7's 41, 24 and 25 + the six new",
        "chkstop rows, which read `absent` from an empty transcript) -- CONTROL=FAIL, SYMPTOM=ABSENT on all three.",
        "CHANNELS for the new rows: T_ra_<cell>_srr0 is SRR0 after the park (0x11111111 unless something writes it); T_ra_<cell>_chkstop",
        "is the checkstop text; T_ra_<cell>_addr the distinct halted addresses (0xfec00008); T_ra_<cell>_stopped the stop line.",
        "", "VARIANTS:"]
    new = dict((a, (k, r, w)) for a, k, r, w in NEWV)
    for n, _ in V:
        if n in new:
            kind, rows, why = new[n]
            if kind == "exactly":
                out.append("   %-14s exactly: %s   (%s)" % (n, ",".join(rows) if rows else "none -- GREEN", why))
            else:
                out.append("   %-14s RED within: %s   (%s; rows not predicted: stale-ib decode)" % (n, ",".join(rows), why))
        elif n == "V12_fail_ra":
            out.append("   %-14s NOT PREDICTED" % n)
        elif n in q7.BUILD_DEP:
            out.append("   %-14s RED (build-dependent rows; not predicted)" % n)
        elif n in GREEN7:
            assert m7.get(n) == [], (n, m7.get(n))
            out.append("   %-14s at least: none -- predicted GREEN (green in table 7)" % n)
        else:
            assert m7.get(n), n
            out.append("   %-14s at least: %s" % (n, ",".join(m7[n])))
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
