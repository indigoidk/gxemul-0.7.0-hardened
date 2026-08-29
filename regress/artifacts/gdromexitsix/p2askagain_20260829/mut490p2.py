#!/usr/bin/env python3
#  #490 pass 2 ask-again mutator.  Exact-substring, UNIQUE-anchor, refuse on miss or
#  ambiguity -- MUTANT-TEXT-NOT-FOUND is a hard failure, never a silent no-op.
import sys

MUTANTS = {
    #  E1: alias Site A's latch onto a DIFFERENT pre-existing bit than the one `crossbit`
    #  exercises.  The product comment names OVERREAD as the realistic collision partner.
    "E1_aliasover": ("<< GDROM_W_FMT_B)", "<< GDROM_W_OVERREAD_B)"),
    #  E2: one character -- `|=` becomes `=`.  Site A's latch set CLEARS every other bit.
    "E2_assignA": ("d->warned |= GDROM_W_FMT;", "d->warned = GDROM_W_FMT;"),
    #  E3: Site A's guard widened to test BOTH bits.  Order-asymmetric: FMT-then-CMD is
    #  unaffected, CMD-then-FMT goes silent.  `both sites` fixes one order.
    "E3_widenA": ("if (!(d->warned & GDROM_W_FMT)) {",
                  "if (!(d->warned & (GDROM_W_FMT | GDROM_W_CMD))) {"),
}

if len(sys.argv) != 4:
    sys.stderr.write("usage: mut490p2.py <name> <infile> <outfile>\n")
    sys.exit(2)

name, src, dst = sys.argv[1], sys.argv[2], sys.argv[3]
if name not in MUTANTS:
    sys.stderr.write("MUT_FAIL unknown mutant %s\n" % name)
    sys.exit(3)

find, repl = MUTANTS[name]
text = open(src, "r", encoding="latin-1").read()
n = text.count(find)
if n != 1:
    sys.stderr.write("MUT_FAIL anchor count %d (want 1) for %s: %r\n" % (n, name, find))
    sys.exit(4)

out = text.replace(find, repl)
if out == text:
    sys.stderr.write("MUT_FAIL replacement was a no-op for %s\n" % name)
    sys.exit(5)
open(dst, "w", encoding="latin-1").write(out)
print("MUT_OK %s  anchor=1  bytes %d -> %d" % (name, len(text), len(out)))
