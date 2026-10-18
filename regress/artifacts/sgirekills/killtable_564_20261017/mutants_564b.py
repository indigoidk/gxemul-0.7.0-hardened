#!/usr/bin/env python3
"""mutants_564b.py <fixed dev_sgi_re.c> <out dir> -- TABLE 2 of #564's kill table: the two ACCEPT-side growth mutants
table 1 lacked.  Found by deriving, from table 1's raw logs, the rows that NO mutant had turned red: three controls and
`lin fill a'.  The accept-row rule says an accept row is discharged by a MEASURED kill, never by existing; and of the
five de-fatalised predicates, S1 and S3 had no growth mutant at all (S2: s2down, S4: s4grow, S5: eccgrow).
Table 1 (mutants_564.py, KILLTABLE.txt) is left as it ran."""
import io, os, sys

G1 = 'if (mode & MTE_MODE_STIPPLE) {\n\t\tif (!(d->warned & SGIRE_W_MTE_STIPPLE))'
G3 = 'if (mode & MTE_MODE_COPY) {\n\t\t\tif (!(d->warned & SGIRE_W_MTE_COPY))'
M = [
    #  S1's guard grown by the adjacent modelled bit the PROM itself sets (DST_ECC, mode 0x11): the least-observable
    #  growth -- it still reads as "the stipple check".
    ("s1grow", [(G1, G1.replace("(mode & MTE_MODE_STIPPLE)", "(mode & (MTE_MODE_STIPPLE | MTE_MODE_DST_ECC))"))],
     "lin fill ecc"),
    #  S3's guard grown to refuse every LIN_A transfer -- the mirror of table 1's s4grow (LIN_B), and the growth only
    #  `lin fill a' (and `lin fill ecc', also LIN_A) can see.
    ("s3growa", [(G3, G3.replace("(mode & MTE_MODE_COPY)", "((mode & MTE_MODE_COPY) || dst_tlb == MTE_TLB_LIN_A)"))],
     "lin fill a, lin fill ecc"),
]

def main():
    src, out = sys.argv[1], sys.argv[2]
    t = io.open(src, encoding="utf-8", newline="").read()
    os.makedirs(out, exist_ok=True)
    for name, edits, pred in M:
        m = t
        for a, b in edits:
            n = m.count(a)
            if n != 1:
                print("MUTANT ANCHOR FAIL %s: %d occurrences" % (name, n)); sys.exit(9)
            m = m.replace(a, b)
        io.open(os.path.join(out, name + ".c"), "w", encoding="utf-8", newline="").write(m)
        print("%-9s predicted: %s" % (name, pred))
    print("mutants written: %d" % len(M))

if __name__ == "__main__":
    main()
