#!/usr/bin/env python3
"""memc_variants_4.py -- test-variant TABLE 4 for the mvme187memcoob detector (repair 4: 148 rows), 2026-11-05, as ruled by the
repair-pass-3 adjudication (p3_20261105/ADJ_MYTHOS.md): table 3's 63 variants (r3_20261105/memc_variants_3.py), the pass-3 seats' 34
measured escapes (p3_20261105/p3_variants.py), and the ruling's own six new families B1-B6 (15 cases), on ONE instrument at the final
row count.  Baseline: det_20261104/dev_mvme187.c.fix2 (== GXEMUL-SEC).  Instrument: table4/probe148_frozen.py.
  memc_variants_4.py list | apply <name> <in> <out> | pretable
Exact-string edits, each asserted once; every backslash is chr(92)."""
import importlib.util
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MD = os.path.dirname(HERE)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


v3 = load("mv3", os.path.join(MD, "r3_20261105", "memc_variants_3.py"))
p3 = load("mp3", os.path.join(MD, "p3_20261105", "p3_variants.py"))
T, NL, BS = chr(9), chr(10), chr(92)
LATCH_M, LATCH_D, DGUARD, DDIR = p3.LATCH_M, p3.LATCH_D, p3.DGUARD, p3.DDIR
CHIPID, CHIPREV = p3.CHIPID, p3.CHIPREV
DEND = T * 3 + "d->warned_default = 1;" + NL + T * 2 + "}" + NL + T * 2 + "break;" + NL
F3 = ("chipid", "chiprev", "memconf")
NEW = [
    ("M_B1_m", [(LATCH_M, LATCH_M.replace("if (!d->warned_memconf)", "if (!d->warned_memconf && !(idata & 0x100))"))],
     ["R12_cnf_line"], "the memconf latch test gated on idata bit 8 clear"),
    ("M_B1_d", [(LATCH_D, LATCH_D.replace("if (!d->warned_default)", "if (!d->warned_default && !(idata & 0x100))"))],
     ["R13_line_text"], "the default latch test gated on idata bit 8 clear"),
    ("M_B1_v", [(DGUARD, DGUARD.replace("if (writeflag == MEM_WRITE)", "if (writeflag == MEM_WRITE && !(idata & 0x100))"))],
     ["R13_line_text"], "the value guard gated on idata bit 8 clear"),
    ("M_B2_v", [(DGUARD, DGUARD.replace("if (writeflag == MEM_WRITE)", "if (writeflag == MEM_WRITE && (relative_addr & 0x10))"))],
     ["R14_line_text"], "the value guard gated on offset bit 4"),
    ("M_B2_d", [(DDIR, DDIR.replace("writeflag == MEM_WRITE ?", "writeflag == MEM_WRITE && (relative_addr & 0x10) ?"))],
     ["R14_line_text"], "the direction gated on offset bit 4"),
    ("M_B3_chipid", [(CHIPID, CHIPID + T * 2 + "if (writeflag == MEM_WRITE) d->memcreg.memc_chipid &= idata;" + NL)],
     ["R12_00_r2"], "a chipid store kept by AND"),
    ("M_B3_chiprev", [(CHIPREV, CHIPREV + T * 2 + "if (writeflag == MEM_WRITE) d->memcreg.memc_chiprev &= idata;" + NL)],
     ["R12_04_r4"], "a chiprev store kept by AND"),
]
for f, row in zip(F3, ("R14_00_r2", "R14_04_r4", "R14_08_r5")):
    NEW.append(("M_B4_" + f, [(LATCH_D, LATCH_D + T * 3 + "if (writeflag == MEM_WRITE) d->memcreg.memc_" + f + " &= idata;" + NL)],
                [row], "the first default store ANDed into " + f))
NEW.append(("M_B5_m", [(LATCH_M, LATCH_M.replace("if (!d->warned_memconf)", "if (!d->warned_memconf || (idata & 0x100))"))],
            ["R9_lines", "R9_no_wide"], "the memconf notice re-announced on idata bit 8"))
NEW.append(("M_B5_d", [(LATCH_D, LATCH_D.replace("if (!d->warned_default)", "if (!d->warned_default || (idata & 0x01))"))],
            ["R5_lines"], "the default notice re-announced on idata bit 0"))
for f, row in zip(F3, ("R5_00_r7", "R5_04_r8", "R5_08_r9")):
    NEW.append(("M_B6_" + f, [(DEND, T * 3 + "d->warned_default = 1;" + NL + T * 2 + "} else if (writeflag == MEM_WRITE)" + NL +
                               T * 3 + "d->memcreg.memc_" + f + " |= idata & 0x04;" + NL + T * 2 + "break;" + NL)],
                [row], "a non-first default store ORs bit 2 into " + f))
P3_CATCH = {   # the row repair 4 added for each pass-3 family (the ruling's D3 and changes), predicted AT LEAST
    "A_B1_chipid": ["R5_00_r7"], "A_B1_chiprev": ["R5_04_r8"], "A_B1_memconf": ["R5_08_r9"],
    "A_B2_chipid": ["R5_00_r7"], "A_B2_chiprev": ["R5_04_r8"], "A_B2_memconf": ["R5_08_r9"],
    "A_B3_chipid_or": ["R12_00_r2"], "A_B3_chipid_xor": ["R12_00_r2"], "A_B3_chiprev_or": ["R12_04_r4"], "A_B3_chiprev_xor": ["R12_04_r4"],
    "A_B4_chipid": ["R12_100_r10"], "A_B4_chiprev": ["R12_104_r11"], "G_3_idata_chipid": ["R12_00_r2"], "G_3_idata_chiprev": ["R12_04_r4"],
    "A_B5_chipid": ["R15_cnf_line"], "A_B5_chiprev": ["R15_cnf_line"], "A_B6_chipid": ["R12_0c_line"], "A_B6_chiprev": ["R12_0c_line"],
    "A_B7_valctl0": ["R13_line_text"], "G_1_dirctl0": ["R13_line_text"], "A_B8_validata": ["R14_line_text"],
    "A_B8_diridata": ["R14_line_text"], "A_B9_dsetidata": ["R14_lines"], "A_B10_u8": ["R12_cnf_line"], "A_B10_u16": ["R12_cnf_line"],
    "A_B11_chipid": ["R5_00_r7"], "A_B11_chiprev": ["R5_04_r8"], "A_B11_memconf": ["R5_08_r9"],
    "A_B12_chipid": ["R9_00_r6"], "A_B12_chiprev": ["R9_04_r7"], "G_5_mnote_ff": ["R12_cnf_line"], "G_5_dval_ff": ["R13_line_text"],
    "G_6_dbit3": ["R14_line_text"],
}
V = ([(n, e) for n, e, _, _, _ in v3.V] + [(n, e) for n, e, _ in p3.V] + [(n, e) for n, e, _, _ in NEW])


def pretable():
    out = [
        "PRETABLE_4 -- mvme187memcoob detector, test-variant table 4 (repair 4, 148 rows).  Written BEFORE table 4 runs (this file's mtime",
        "precedes table4/'s).  Instrument: table4/probe148_frozen.py (the in-tree probe after apply_r4_edits.py; base on the build tree",
        "148/148, r4_20261105/base148_build.out).  Baseline det_20261104/dev_mvme187.c.fix2.  Legs first: base, HEAD, three null media.",
        "",
        "THE FOUR CHECKS for the repair-4 rows (p3_20261105/ADJ_MYTHOS.md, D3 and changes 1-7):",
        "  SIBLING PARITY -- each store category {memconf, default, chipid, chiprev} x controller {0, 1} now has a session whose first",
        "    access of that category is a store, followed by served readbacks (R3/R12 memconf ctl0, R9 ctl1; R5 default ctl0, R13 ctl1;",
        "    R12 chipid/chiprev ctl0 and ctl1); each notice category has a zero first store (R9, R14) and a wide first store (R12, R13).",
        "  CLAIM -> ROW -- 'no store reaches a served field' -> the readbacks in R5, R9, R12, R13, R14; 'a served store is dropped' ->",
        "    R12's four 0xff-then-0x00 readbacks; 'the notice prints the whole value' -> R12 cnf line, R13 line text (0xffffffff).",
        "  GUARD FIELD vs BODY FIELD -- the default body reads warned_default, writeflag, relative_addr, controller, idata; the memconf",
        "    body reads idata, controller, warned_memconf, memc_memconf; each is varied: idata {0x00, 0xff, 0xffffffff} at first and",
        "    non-first stores, offset bits by the complement pair 0x18 / 0xe7 among first default stores, controller {0, 1} per category.",
        "    len is read by neither guarded body (G_2 ruled OUT): no row claims it.",
        "  CHANNEL -- per variant below: the named row's value or notice differs under it (derived from the function as written).",
        "",
        "PREDICTIONS.  Table 3's 63: RED (each was red on the 118-row instrument; several of their rows changed meaning in repair 4, so the",
        "row sets are not carried, only the verdict).  The pass-3 34: AT LEAST the repair-4 row named (G_2_dlen1 was ruled OUT and no row",
        "was added for it: predicted GREEN).  The ruling's B1-B6: AT LEAST the row named.  HEAD: SYMPTOM=PRESENT.  Null media: CONTROL=FAIL.",
        "The ruling asks the freshness proof that served &= stays red after change 3: M_B3_chipid / M_B3_chiprev, predicted red on",
        "R12 00 r2 / R12 04 r4 (0x80 & 0xff & 0x00 = 0; 0x1 & 0xff & 0x00 = 0).",
        "",
        "VARIANTS (name, predicted):",
    ]
    for n, _, _, _, what in v3.V:
        out.append("   %-17s RED (table 3)" % n)
    for n, _, who in p3.V:
        out.append("   %-17s %s" % (n, "GREEN (ruled OUT; no row)" if n == "G_2_dlen1" else "at least: " + ",".join(P3_CATCH[n]) + "   (" + who + ")"))
    for n, _, pred, what in NEW:
        out.append("   %-17s at least: %s   (%s)" % (n, ",".join(pred), what))
    return NL.join(out) + NL


def main():
    a = sys.argv[1:]
    if a == ["list"]:
        print(" ".join(n for n, _ in V))
    elif a == ["pretable"]:
        sys.stdout.write(pretable())
    elif len(a) == 4 and a[0] == "apply":
        s = io.open(a[2], encoding="latin-1", newline="").read()
        f = dict(V)[a[1]]
        if callable(f):
            try:
                s = f(s)
            except (AssertionError, ValueError) as e:
                print("MUTANT-TEXT-NOT-FOUND", a[1], e)
                sys.exit(3)
        else:
            for old, new in f:
                if s.count(old) != 1:
                    print("MUTANT-TEXT-NOT-FOUND", a[1], repr(old[:60]), s.count(old))
                    sys.exit(3)
                s = s.replace(old, new)
        io.open(a[3], "w", encoding="latin-1", newline="").write(s)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
