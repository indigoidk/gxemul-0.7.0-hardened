#!/usr/bin/env python3
"""mpu_variants2.py -- five variants the pass 2 named (2026-11-04 18:4xZ), measured as a supplement to table 1 (mpu_variants.py, frozen):
the three edits the probe's CLAUSE (e) lists as caught that table 1 did not run (Fable, Opus: "predicted, not measured"), and the two in-bound
cells Opus and Fable found absent from the table (both expected to go undetected and disclosed).  Same interface as mpu_variants.py
(list | apply <name> <in> <out> | pretable); exact-string edits, each asserted once."""
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mpu_variants as M  # noqa: E402

T, NL = M.T, M.NL
END_III = T * 2 + "} else {" + NL + T * 3 + "/*  #NNN: through MIPS II, LWC3 is a coprocessor-3 load.  No"
V = [
    ("D27_lwc3_ge1", [(M.C_LWC3III, M.C_LWC3III.replace("== 3", ">= 1"))],
     "32 lwc3 exc", "(contract) LWC3 ISA III arm `== 3` -> `>= 1` (RI at ISA I)"),
    ("D28_swc3_eq4", [(M.C_SWC3, M.C_SWC3.replace(">= 3", "== 4"))],
     "64/24k/5ke swc3 exc", "(contract) SWC3 gate `== 4`"),
    ("D29_lwc3_iii_drop", lambda s: M.blockrep(s, M.C_LWC3III, END_III, ""),
     "64 lwc3 exc", "(contract) the LWC3 ISA III RI arm dropped (back to CpU CE 3)"),
    ("D30_lwc3_ge2", [(M.C_LWC3III, M.C_LWC3III.replace("== 3", ">= 2"))],
     "NONE -- the ISA II cell (disclosed)", "(pass 2) LWC3 ISA III arm `== 3` -> `>= 2`"),
    ("D31_r5900_false", [(M.C_R5900, M.C_R5900.replace("rev == MIPS_R5900", "rev == MIPS_R5900 && 0"))],
     "NONE -- no R5900 session (disclosed)", "(pass 2) the MDMX arm's R5900 test made always false"),
]


def main():
    a = sys.argv[1:]
    if a == ["list"]:
        print(" ".join(n for n, _, _, _ in V))
    elif a == ["pretable"]:
        sys.stdout.write("PRETABLE2 -- supplement to table 1, written BEFORE these five ran (pass-2 findings, 2026-11-04)" + NL)
        for n, _, pred, what in V:
            sys.stdout.write("   %-18s %-58s red: %s%s" % (n, what[:58], pred, NL))
    elif len(a) == 4 and a[0] == "apply":
        name, src, dst = a[1:]
        s = io.open(src, encoding="latin-1", newline="").read()
        f = dict((n, e) for n, e, _, _ in V)[name]
        try:
            if callable(f):
                s = f(s)
            else:
                for old, new in f:
                    assert s.count(old) == 1, (old[:60], s.count(old))
                    s = s.replace(old, new)
        except (AssertionError, ValueError) as e:
            print("MUTANT-TEXT-NOT-FOUND", name, e)
            sys.exit(3)
        io.open(dst, "w", encoding="latin-1", newline="").write(s)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
