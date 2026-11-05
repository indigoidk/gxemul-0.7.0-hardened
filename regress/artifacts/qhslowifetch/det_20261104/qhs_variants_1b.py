#!/usr/bin/env python3
"""qhs_variants_1b.py -- test-variant table 1b for the qhslowifetch detector: the two variants pass 2 raised, measured against the
shipped 50-row probe (legs50/probe50_frozen.py) and against a candidate with two noT rows added (table1b/probe52c.py).
  qhs_variants_1b.py list | apply <name> <in> <out> | pretable
  D14_c_meset  arm (c) conditioned on MSR[ME] SET -- the mirror of table 1's D13.  Raised against the claim (grok, pass 2) that the
               chkstop rows are excess: with ME clear arm (c) is skipped and the checkstop arm runs; with ME set it parks, so T me
               cannot see it.
  D15_dom_ok   the read's failure test made true whatever the read returns (grok, pass 2: "weaken if (!cpu->memory_rw(...)) so the
               four-arm block runs after every slow-path read").  On the no-T route the read succeeds and running stays 1, so the
               block falls to the checkstop arm (MSR = 0) and parks at the same pc -- no shipped row reads the texts that differ.
Exact-string edits on cpu_ppc_instr.c.fix2; every backslash is chr(92)."""
import io
import sys

T = chr(9)
NL = chr(10)
CHEAD = T * 3 + "if (!cpu->running) {" + NL + T * 4 + "cpu->cd.ppc.next_ic = &nothing_call;" + NL
OPEN = T * 2 + "    sizeof(ib), MEM_READ, CACHE_INSTRUCTION)) {" + NL

V = [
    ("D14_c_meset", [(CHEAD, CHEAD.replace("if (!cpu->running)", "if (!cpu->running && (cpu->cd.ppc.msr & PPC_MSR_ME))"))],
     "50-row: T step/T cont/again chkstop only (T me green).  52-row: the same", "arm (c) conditioned on ME set"),
    ("D15_dom_ok", [(OPEN, T * 2 + "    sizeof(ib), MEM_READ, CACHE_INSTRUCTION) || 1) {" + NL)],
     "50-row: NONE (undetected, as grok predicts).  52-row: noT unimpl, noT chkstop", "the block entered whatever the read returns"),
]

PRETABLE = NL.join([
    "PRETABLE_1b -- qhslowifetch, table 1b.  Written BEFORE table1b runs (this file's mtime precedes table1b/'s).",
    "Instruments: legs50/probe50_frozen.py (the 50-row probe as sent to pass 2) and table1b/probe52c.py (the same plus `noT unimpl`, want",
    "present, and `noT chkstop`, want absent -- the shipped fix's noT transcript prints `cpu: UNIMPLEMENTED instruction at 0x2040000` and no",
    "checkstop text: legs50/sessions_base/noT.txt:33).  Baseline: cpu_ppc_instr.c.fix2 -- the post-fix source WITH the D8 comment",
    "rewording, comment-only different from table 1's .fix (the first 1b launch refused on that difference).  Each variant runs both",
    "probes from one build.",
    "",
    "VARIANTS (name, what, predicted red rows):",
    ""])


def main():
    a = sys.argv[1:]
    if a == ["list"]:
        print(" ".join(n for n, _, _, _ in V))
    elif a == ["pretable"]:
        out = PRETABLE
        for n, _, pred, what in V:
            out += "   %-12s %-48s red: %s%s" % (n, what, pred, NL)
        out += NL + "   base         the fix                                          red: none on either probe (52-row: 52 of 52)" + NL
        sys.stdout.write(out)
    elif len(a) == 4 and a[0] == "apply":
        name, src, dst = a[1:]
        s = io.open(src, encoding="latin-1", newline="").read()
        for old, new in dict((n, e) for n, e, _, _ in V)[name]:
            if s.count(old) != 1:
                print("MUTANT-TEXT-NOT-FOUND", name, repr(old[:60]), s.count(old))
                sys.exit(3)
            s = s.replace(old, new)
        io.open(dst, "w", encoding="latin-1", newline="").write(s)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
