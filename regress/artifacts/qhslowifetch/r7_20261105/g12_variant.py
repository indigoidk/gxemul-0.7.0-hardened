#!/usr/bin/env python3
"""g12_variant.py <in.c> <out.c> <G1|G2> -- the two pass-6 findings of the Gemini 4 Argon seat
(_scratchpad/gweb/jobs_20261105_rounds/p6_qhs/gemini_web.out), each ONE exact edit against the fix (GXEMUL-SEC's
src/cpus/cpu_ppc_instr.c):
  G1  arm (b)'s aligned compare `(cpu->pc & ~(uint64_t)3) != addr` made `cpu->pc < addr`;
  G2  arm (d)'s test `cpu->cd.ppc.msr & PPC_MSR_ME` made `cpu->cd.ppc.msr`.
EDITS is imported by qhs_variants_7.py, so table 7 applies the same text.  Refuses unless the target text is found exactly once."""
import io
import sys

T, NL = chr(9), chr(10)
EDITS = {
    "G1": [(T * 3 + "if ((cpu->pc & ~(uint64_t)3) != addr) {" + NL, T * 3 + "if (cpu->pc < addr) {" + NL)],
    "G2": [(T * 3 + "if (cpu->cd.ppc.msr & PPC_MSR_ME) {" + NL, T * 3 + "if (cpu->cd.ppc.msr) {" + NL)],
}


def apply(s, edits):
    for old, new in edits:
        if s.count(old) != 1:
            raise ValueError("target found %d times: %r" % (s.count(old), old[:60]))
        s = s.replace(old, new)
    return s


if __name__ == "__main__":
    src = io.open(sys.argv[1], encoding="latin-1", newline="").read()
    try:
        out = apply(src, EDITS[sys.argv[3]])
    except ValueError as e:
        sys.exit("MUTANT-TEXT-NOT-FOUND %s %s" % (sys.argv[3], e))
    io.open(sys.argv[2], "w", encoding="latin-1", newline="").write(out)
