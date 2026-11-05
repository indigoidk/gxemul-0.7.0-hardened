#!/usr/bin/env python3
"""b11_variant.py <in.c> <out.c> <name> -- repair 11's variants (codex GPT-6 Astra, pass 10: p10_20261105/codex_codex_qhs_p10.txt, B1),
each ONE conditional statement inserted immediately inside the failed-read block, before arm (a), against the fix (GXEMUL-SEC's
src/cpus/cpu_ppc_instr.c == r7_20261105/cpu_ppc_instr.c.fix7).  EDITS is imported by qhs_variants_12.py.
  R11_tog_full        if ((pc & ~0xb) != addr) srr0 ^= 0x100;     pass 10's B1: the masked read-ahead pcs (0xfec00008..b -> 0xfec00000)
                                                                  differ from addr on both visits, the masked one-entry pcs
                                                                  (0x02040000..7) equal it -- it cancels on every two-entry session
                                                                  and never fires on a one-entry one
  R11_tog_full_<k><e> the same also gated on (pc & 3) == k and ME clear (e = c) or set (e = m): one member per read-ahead cell"""
import io
import sys

T, NL = chr(9), chr(10)
FAILT = T * 2 + "    sizeof(ib), MEM_READ, CACHE_INSTRUCTION)) {" + NL
ME = "(cpu->cd.ppc.msr & PPC_MSR_ME)"
FULL = "(cpu->pc & ~(uint64_t)0xb) != addr"
TOG = "cpu->cd.ppc.spr[SPR_SRR0] ^= 0x100;"


def top(cond):
    return [(FAILT, FAILT + T * 3 + "if (" + cond + ")" + NL + T * 4 + TOG + NL)]


EDITS = {"R11_tog_full": top(FULL)}
for k in range(4):
    EDITS["R11_tog_full_%dc" % k] = top(FULL + " && (cpu->pc & 3) == %d && !%s" % (k, ME))
    EDITS["R11_tog_full_%dm" % k] = top(FULL + " && (cpu->pc & 3) == %d && %s" % (k, ME))
ORDER = ["R11_tog_full"] + ["R11_tog_full_%d%s" % (k, e) for k in range(4) for e in "cm"]


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
