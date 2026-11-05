#!/usr/bin/env python3
"""b9_variant.py <in.c> <out.c> <name> -- repair 9's variants (codex GPT-6 Astra, pass 8: p8_20261105/codex_codex_qhs_p8.txt, B1),
each ONE exact edit against the fix (GXEMUL-SEC's src/cpus/cpu_ppc_instr.c == r7_20261105/cpu_ppc_instr.c.fix7): a single conditional
statement inserted immediately inside the failed-read block, before arm (a).  EDITS is imported by qhs_variants_10.py.
  R9_tog_me1     if ((cpu->pc & 3) == 1) cpu->cd.ppc.msr ^= PPC_MSR_ME;      pass 8's B1: cancels on the two-entry read-ahead sessions
  R9_tog_me2     the same at low bits 10                                      B1's `== 2` form
  R9_tog_me0     the same at low bits 00                                      the family's aligned member
  R9_tog_me3     the same at low bits 11                                      the family's last member
  R9_tog_srr0_1  if ((cpu->pc & 3) == 1) cpu->cd.ppc.spr[SPR_SRR0] ^= 0x100;  "any other state the block could toggle": SRR0"""
import io
import sys

T, NL = chr(9), chr(10)
FAILT = T * 2 + "    sizeof(ib), MEM_READ, CACHE_INSTRUCTION)) {" + NL


def top(cond, stmt):
    return [(FAILT, FAILT + T * 3 + "if (" + cond + ")" + NL + T * 4 + stmt + NL)]


EDITS = {
    "R9_tog_me1": top("(cpu->pc & 3) == 1", "cpu->cd.ppc.msr ^= PPC_MSR_ME;"),
    "R9_tog_me2": top("(cpu->pc & 3) == 2", "cpu->cd.ppc.msr ^= PPC_MSR_ME;"),
    "R9_tog_me0": top("(cpu->pc & 3) == 0", "cpu->cd.ppc.msr ^= PPC_MSR_ME;"),
    "R9_tog_me3": top("(cpu->pc & 3) == 3", "cpu->cd.ppc.msr ^= PPC_MSR_ME;"),
    "R9_tog_srr0_1": top("(cpu->pc & 3) == 1", "cpu->cd.ppc.spr[SPR_SRR0] ^= 0x100;"),
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
