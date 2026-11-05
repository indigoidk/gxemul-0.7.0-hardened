#!/usr/bin/env python3
"""b123_variant.py <in.c> <out.c> <B1|B2|B3> -- the three pass-6 breaches of arm (a) (codex GPT-6 Astra,
p6_20261105/codex_codex_qhs_p6.txt), each ONE exact edit against the fix (GXEMUL-SEC's src/cpus/cpu_ppc_instr.c):
  B1  the guard conjoined with `!(cpu->pc & 2)` (pc's second low bit);
  B2  the guard conjoined with `(!(cpu->cd.ppc.msr & PPC_MSR_ME) || cpu->pc == addr)` (refuses an unaligned read-ahead with ME set);
  B3  the bare return replaced by `{ cpu->cd.ppc.msr |= (cpu->pc != addr ? PPC_MSR_ME : 0); return; }`.
EDITS is imported by qhs_variants_7.py, so table 7 applies the same text.  Refuses unless the target text is found exactly once."""
import io
import sys

T, NL = chr(9), chr(10)
G = T * 3 + "if (cpu->translation_readahead)" + NL                 # arm (a)'s guard line
A = G + T * 4 + "return;" + NL                                      # arm (a): guard + bare return
EDITS = {
    "B1": [(G, T * 3 + "if (cpu->translation_readahead && !(cpu->pc & 2))" + NL)],
    "B2": [(G, T * 3 + "if (cpu->translation_readahead && (!(cpu->cd.ppc.msr & PPC_MSR_ME) || cpu->pc == addr))" + NL)],
    "B3": [(A, T * 3 + "if (cpu->translation_readahead) {" + NL + T * 4 + "cpu->cd.ppc.msr |= (cpu->pc != addr ? PPC_MSR_ME : 0);" +
            NL + T * 4 + "return;" + NL + T * 3 + "}" + NL)],
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
