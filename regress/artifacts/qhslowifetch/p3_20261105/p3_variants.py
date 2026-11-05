#!/usr/bin/env python3
"""p3_variants.py -- qhslowifetch REPAIR PASS 3: the four test variants of GPT-6 Astra's two floor findings (codex_qhs_p3.txt B1, B2),
MEASURED before the adjudication rules on them.  Baseline: r3_20261105/cpu_ppc_instr.c.fix4 (== GXEMUL-SEC).  Instrument: the
in-tree 62-row probe, frozen at table_p3/probe62_p3.py (AST-equal to table 3's probe62_frozen.py; only the docstring differs).
  B1a  inside arm (c), before the park: clear MSR[ME]                 (Astra's exact edit)
  B1b  inside arm (a), before its return: clear MSR[ME]               (Astra: "clearing ME inside arm (a)")
  B1c  inside arm (c), before the park: set MSR[ME]                   (Astra: "setting ME before arm (c)'s park")
  B2   before arm (a): on an ME-clear read-ahead failure, print the checkstop line; arm (a) still returns   (Astra's exact edit)
  p3_variants.py list | apply <name> <in> <out> | pretable
Exact-string edits, each asserted once; every backslash is chr(92)."""
import importlib.util
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("qv2", os.path.join(os.path.dirname(HERE), "det_20261104", "qhs_variants_2.py"))
qv2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qv2)
T, NL, BS = chr(9), chr(10), chr(92)
A, CHEAD = qv2.A, qv2.CHEAD
ME = "PPC_MSR_ME"
CHK = (T * 3 + "if (cpu->translation_readahead && !(cpu->cd.ppc.msr & " + ME + "))" + NL +
       T * 4 + 'fatal("[ ppc: instruction fetch from 0x%" PRIx64' + NL +
       T * 4 + '    " declined with MSR[ME]=0: checkstop ]' + BS + 'n", (uint64_t) addr);' + NL)
V = [
    ("B1a_c_meclr", [(CHEAD, T * 3 + "if (!cpu->running) {" + NL + T * 4 + "cpu->cd.ppc.msr &= ~" + ME + ";" + NL +
                      T * 4 + "cpu->cd.ppc.next_ic = &nothing_call;" + NL)],
     "none: 62/62 (no row reads the final MSR; T me and T ra me end with ME clear, every other row unchanged)"),
    ("B1b_a_meclr", [(A, T * 3 + "if (cpu->translation_readahead) {" + NL + T * 4 + "cpu->cd.ppc.msr &= ~" + ME + ";" + NL +
                      T * 4 + "return;" + NL + T * 3 + "}" + NL)],
     "none: 62/62 (T ra me's read-ahead clears ME; its real fetch parks in arm (c) as before: pc, two reports, no checkstop)"),
    ("B1c_c_meset", [(CHEAD, T * 3 + "if (!cpu->running) {" + NL + T * 4 + "cpu->cd.ppc.msr |= " + ME + ";" + NL +
                      T * 4 + "cpu->cd.ppc.next_ic = &nothing_call;" + NL)],
     "none: 62/62 (T step, T cont, again and T ra end with ME set; no row reads it)"),
    ("B2_ra_chktext", [(A, CHK + A)],
     "none: 62/62 (only T ra's read-ahead failure prints the checkstop line; T ra has no chkstop row; T ra me's ME is set)"),
]


def pretable():
    out = [
        "PRETABLE_P3 -- qhslowifetch, GPT-6 Astra's pass-3 floor findings B1 and B2 (p3_20261105/codex_qhs_p3.txt), written BEFORE the",
        "measurement (this file's mtime precedes table_p3/'s).  Instrument: table_p3/probe62_p3.py, the in-tree probe after the pass-3",
        "records fixes (AST-equal to table 3's probe62_frozen.py).  Baseline: r3_20261105/cpu_ppc_instr.c.fix4.  Base leg first.",
        "The prediction for each is Astra's derivation: ALL 62 GREEN.  A red row on any of them refutes the finding for that variant.", "",
    ]
    for n, _, pred in V:
        out.append("   %-14s predicted %s" % (n, pred))
    return NL.join(out) + NL


def main():
    a = sys.argv[1:]
    if a == ["list"]:
        print(" ".join(n for n, _, _ in V))
    elif a == ["pretable"]:
        sys.stdout.write(pretable())
    elif len(a) == 4 and a[0] == "apply":
        s = io.open(a[2], encoding="latin-1", newline="").read()
        for old, new in dict((n, e) for n, e, _ in V)[a[1]]:
            if s.count(old) != 1:
                print("MUTANT-TEXT-NOT-FOUND", a[1], repr(old[:60]), s.count(old))
                sys.exit(3)
            s = s.replace(old, new)
        io.open(a[3], "w", encoding="latin-1", newline="").write(s)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
