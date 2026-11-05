#!/usr/bin/env python3
"""b7b_variant.py <in.c> <out.c> <name> -- repair 7b's variants, each ONE exact edit against the fix (GXEMUL-SEC's
src/cpus/cpu_ppc_instr.c == r7_20261105/cpu_ppc_instr.c.fix7).  EDITS is imported by qhs_variants_8.py, so table 8 applies the same
text.  Refuses unless the target text is found exactly once.
  the channels the aligned read-ahead siblings pin and the six unaligned sessions did not (the coordinator's repair 7b) --
    R7b_a_srr0un   arm (a) writes SRR0 when pc != addr        R5_srr0_a's shape gated on alignment (the srr0 channel)
    R7b_a_chkun    the checkstop line printed on a read-ahead failure when pc != addr, arm (a) still returning
                                                              B2_ra_chktext's shape gated on alignment (the checkstop channel)
    R7b_a_pcalign  arm (a) aligns pc when pc != addr          the nearest single edit to the halt-address channel
    R7b_a_runun    arm (a) restores running when pc != addr   the nearest single edit to the stop channel (R5_arun's shape)
  the failure test -- the predicate dominating the whole block -- narrowed by a conjunct (LATE_REPLICATIONS_20261105.md rows 33, 41;
  never built in tables 1-7); a failure the conjunct refuses skips the block and decodes the uninitialised ib --
    R7b_f_me       && (msr & ME)      R7b_f_meclr   && !(msr & ME)
    R7b_f_ra       && translation_readahead               R7b_f_unal    && cpu->pc != addr"""
import io
import sys

T, NL, BS = chr(9), chr(10), chr(92)
G = T * 3 + "if (cpu->translation_readahead)" + NL                 # arm (a)'s guard line
A = G + T * 4 + "return;" + NL                                      # arm (a): guard + bare return
FAILT = T * 2 + "    sizeof(ib), MEM_READ, CACHE_INSTRUCTION)) {" + NL
ME = "(cpu->cd.ppc.msr & PPC_MSR_ME)"


def gated(stmt):
    """arm (a) with `stmt` run first when pc != addr; the bare return kept."""
    return [(A, T * 3 + "if (cpu->translation_readahead) {" + NL + T * 4 + "if (cpu->pc != addr)" + NL + T * 5 + stmt + NL +
             T * 4 + "return;" + NL + T * 3 + "}" + NL)]


def fail(conj):
    return [(FAILT, T * 2 + "    sizeof(ib), MEM_READ, CACHE_INSTRUCTION) && " + conj + ") {" + NL)]


CHKUN = (T * 3 + "if (cpu->translation_readahead && cpu->pc != addr)" + NL +
         T * 4 + 'fatal("[ ppc: instruction fetch from 0x%" PRIx64' + NL +
         T * 4 + '    " declined with MSR[ME]=0: checkstop ]' + BS + 'n", (uint64_t) addr);' + NL)
EDITS = {
    "R7b_a_srr0un": gated("cpu->cd.ppc.spr[SPR_SRR0] = addr;"),
    "R7b_a_chkun": [(A, CHKUN + A)],
    "R7b_a_pcalign": gated("cpu->pc = addr;"),
    "R7b_a_runun": gated("cpu->running = 1;"),
    "R7b_f_me": fail(ME),
    "R7b_f_meclr": fail("!" + ME),
    "R7b_f_ra": fail("cpu->translation_readahead"),
    "R7b_f_unal": fail("cpu->pc != addr"),
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
