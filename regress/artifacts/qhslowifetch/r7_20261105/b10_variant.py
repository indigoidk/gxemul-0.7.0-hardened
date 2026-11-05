#!/usr/bin/env python3
"""b10_variant.py <in.c> <out.c> <name> -- repair 10's variants (codex GPT-6 Astra, pass 9: p9_20261105/codex_codex_qhs_p9.txt, B1 and
R2), each ONE conditional statement inserted immediately inside the failed-read block, before arm (a), against the fix (GXEMUL-SEC's
src/cpus/cpu_ppc_instr.c == r7_20261105/cpu_ppc_instr.c.fix7).  EDITS is imported by qhs_variants_11.py.
  R10_tog_srr0_meun  if ((msr & ME) && pc != addr) srr0 ^= 0x100;   pass 9's B1: cancels on the three unaligned ME-set read-ahead
                                                                     sessions; no one-entry failure was ME-set and unaligned
  R10_tog_srr0_me1   the same gated on (msr & ME) && (pc & 3) == 1  B1's isolated members, one per missing cell
  R10_tog_srr0_me2   ... == 2
  R10_tog_srr0_me3   ... == 3
  R10_tog_srr0_2     if ((pc & 3) == 2) srr0 ^= 0x100;              R2: the 10 toggle, `T blr o2 srr0`'s own named variant"""
import io
import sys

T, NL = chr(9), chr(10)
FAILT = T * 2 + "    sizeof(ib), MEM_READ, CACHE_INSTRUCTION)) {" + NL
ME = "(cpu->cd.ppc.msr & PPC_MSR_ME)"
TOG = "cpu->cd.ppc.spr[SPR_SRR0] ^= 0x100;"


def top(cond):
    return [(FAILT, FAILT + T * 3 + "if (" + cond + ")" + NL + T * 4 + TOG + NL)]


EDITS = {
    "R10_tog_srr0_meun": top(ME + " && cpu->pc != addr"),
    "R10_tog_srr0_me1": top(ME + " && (cpu->pc & 3) == 1"),
    "R10_tog_srr0_me2": top(ME + " && (cpu->pc & 3) == 2"),
    "R10_tog_srr0_me3": top(ME + " && (cpu->pc & 3) == 3"),
    "R10_tog_srr0_2": top("(cpu->pc & 3) == 2"),
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
