#!/usr/bin/env python3
"""qhs_variants_5.py -- test-variant TABLE 5 for qhslowifetch (repair 5: the aligned compare in arm (b); 79 rows), 2026-11-05.  Table 4's 36
variants (r4_20261105/qhs_variants_4.py), each ADAPTED to fix5 by rewriting arm (b)'s old test text into the aligned one in its edit
strings (so a variant that edited the old test edits the new one the same way), plus six for repair 5 (the repair-pass-4 ruling,
p4_20261105/ADJ_MYTHOS.md, and the pass-4 review's arm (a) finding).  Baseline: r5_20261105/cpu_ppc_instr.c.fix5 (== GXEMUL-SEC).
  qhs_variants_5.py list | apply <name> <in> <out> | pretable"""
import importlib.util
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
QD = os.path.dirname(HERE)
spec = importlib.util.spec_from_file_location("q4", os.path.join(QD, "r4_20261105", "qhs_variants_4.py"))
q4 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(q4)
T, NL = chr(9), chr(10)
OLD_T, NEW_T = "if (cpu->pc != addr) {", "if ((cpu->pc & ~(uint64_t)3) != addr) {"
A = T * 3 + "if (cpu->translation_readahead)" + NL + T * 4 + "return;" + NL
BT = T * 3 + NEW_T + NL


def adapt(edits):
    if callable(edits):
        return lambda s: edits(s.replace(NEW_T, OLD_T)).replace(OLD_T, NEW_T)
    return [(o.replace(OLD_T, NEW_T), n.replace(OLD_T, NEW_T)) for o, n in edits]


NEWV = [
    ("R5_revert", [(BT, T * 3 + OLD_T + NL)], ["T_blr_nonex"], "arm (b)'s test back to pc != addr (the repair reverted)"),
    ("R5_mask1", [(BT, BT.replace("~(uint64_t)3", "~(uint64_t)1"))], ["T_blr_nonex"], "the aligned compare's mask narrowed to bit 0"),
    ("R5_mask2", [(BT, BT.replace("~(uint64_t)3", "~(uint64_t)2"))], ["T_blr_nonex"], "the aligned compare's mask narrowed to bit 1"),
    ("R5_srr0_a", [(A, T * 3 + "if (cpu->translation_readahead) {" + NL + T * 4 + "cpu->cd.ppc.spr[SPR_SRR0] = addr;" + NL +
                    T * 4 + "return;" + NL + T * 3 + "}" + NL)], ["T_ra_srr0", "T_ra_me_srr0"], "arm (a) writes SRR0 before its return"),
    ("R5_cb", [(BT, T * 3 + "if (!cpu->running) {" + NL + T * 4 + "cpu->cd.ppc.next_ic = &nothing_call;" + NL + T * 4 + "return;" + NL +
                T * 3 + "}" + NL + BT)], [], "the park tested before arm (b) too (CB): EQUIVALENT on every row (running is 0 at each -T entry)"),
    ("R5_arun", [(A, T * 3 + "if (cpu->translation_readahead) {" + NL + T * 4 + "cpu->running = 1;" + NL + T * 4 + "return;" + NL +
                  T * 3 + "}" + NL)], [], "arm (a) restores running before its return (pass-4 review): DISCLOSED, predicted green"),
]
V = [(n, adapt(e)) for n, e in q4.V] + [(n, e) for n, e, _, _ in NEWV]


def pretable():
    m4 = {}
    for line in io.open(os.path.join(QD, "r4_20261105", "table4", "SCORES.txt"), encoding="utf-8"):
        p = line.split()
        if len(p) > 1 and "RED=" in line:
            red = line.rsplit("RED=", 1)[1].strip()
            m4[p[0]] = [] if red == "none" else red.split(",")
    out = [
        "PRETABLE_5 -- qhslowifetch, test-variant table 5 (repair 5: the aligned compare; 79 rows).  Written BEFORE table 5 runs (this file's",
        "mtime precedes table5/'s).  Instrument: table5/probe79_frozen.py (the in-tree probe after apply_r5.py).  Baseline: fix5.",
        "Table 4's 36 are adapted to fix5 (arm (b)'s test text rewritten in their edits) and predicted AT LEAST their table-4 red sets, except",
        "V12 (NOT PREDICTED) and D12 (BUILD-DEPENDENT: red, rows not predicted).  Repair 5's six below are predicted EXACTLY.  The new rows",
        "(T blr *, T ra srr0, T ra me srr0) on the 36 are informational.  HEAD: table 4's HEAD set + T_blr_session, T_blr_pc, T_blr_srr0,",
        "T_blr_msr, T_blr_lr (the session exits on the fetch, so no registers) + T_ra_srr0, T_ra_me_srr0 = 39 red -> 40/79.  Null media:",
        "CONTROL=FAIL.  CHANNEL for the new rows: T_blr_nonex counts halt reports -- 1 when arm (c) parks, thousands when arm (b) re-runs the",
        "slot (8278 measured, p4_20261105/blr_table); r3 = 0x02040003 sets both low bits, so either one-bit mask leaves pc != addr.",
        "", "VARIANTS:"]
    for n, _ in V:
        new = dict((a, (b, c)) for a, _, b, c in NEWV)
        if n in new:
            out.append("   %-14s exactly: %s   (%s)" % (n, ",".join(new[n][0]) or "none -- GREEN", new[n][1]))
        elif n == "V12_fail_ra":
            out.append("   %-14s NOT PREDICTED" % n)
        elif n == "D12_else_ra":
            out.append("   %-14s RED (build-dependent rows)" % n)
        else:
            out.append("   %-14s at least: %s" % (n, ",".join(m4.get(n, [])) or "none (green in table 4; predicted green)"))
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
