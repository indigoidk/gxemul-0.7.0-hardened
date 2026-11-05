#!/usr/bin/env python3
"""b8_variant.py <in.c> <out.c> <name> -- repair 8's variants (codex GPT-6 Astra, pass 7: p7_20261105/codex_codex_qhs_p7.txt, F1),
each ONE exact edit against the fix (GXEMUL-SEC's src/cpus/cpu_ppc_instr.c == r7_20261105/cpu_ppc_instr.c.fix7).  EDITS is imported
by qhs_variants_9.py, so table 9 applies the same text.  Refuses unless the target text is found exactly once.
  R8_c_meun_bad  arm (c) sends a halt with MSR[ME] set at pc != addr to bad: before its park   (pass 7's F1; V10_c_me_bad's shape,
                 specialised to the unaligned cell)
  R8_c_clun_bad  the same with MSR[ME] clear at pc != addr                                        (F1's ME-clear mirror)"""
import io
import sys

T, NL = chr(9), chr(10)
CHEAD = T * 3 + "if (!cpu->running) {" + NL + T * 4 + "cpu->cd.ppc.next_ic = &nothing_call;" + NL


def to_bad(cond):
    return [(CHEAD, T * 3 + "if (!cpu->running) {" + NL + T * 4 + "if (" + cond + " && cpu->pc != addr)" + NL + T * 5 + "goto bad;" + NL +
             T * 4 + "cpu->cd.ppc.next_ic = &nothing_call;" + NL)]


EDITS = {
    "R8_c_meun_bad": to_bad("(cpu->cd.ppc.msr & PPC_MSR_ME)"),
    "R8_c_clun_bad": to_bad("!(cpu->cd.ppc.msr & PPC_MSR_ME)"),
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
