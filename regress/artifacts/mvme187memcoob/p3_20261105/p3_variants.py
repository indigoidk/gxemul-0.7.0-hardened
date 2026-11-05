#!/usr/bin/env python3
"""p3_variants.py -- mvme187memcoob REPAIR PASS 3: the test variants of the pass-3 seats' floor findings, MEASURED before the
adjudication rules on them.  GPT-6 Astra (codex_memc_p3.txt) B1-B12, 27 cases; glm-5.3 (ollama_glm.txt) breaches 1-6 where they are
not already Astra's (breach 1's ternary member, breach 2, breach 3's idata gate, breach 5, conditional breach 6).  Each seat
DERIVED every one green on the 118-row probe; this table measures that.  Baseline: det_20261104/dev_mvme187.c.fix2 (== GXEMUL-SEC).
Instrument: table_p3/probe118_p3.py (the in-tree probe; AST-equal to r3_20261105/table3/probe118_frozen.py).
  p3_variants.py list | apply <name> <in> <out> | pretable
Exact-string edits, each asserted once; every backslash is chr(92)."""
import io
import sys

T, NL, BS = chr(9), chr(10), chr(92)
CHIPID = T * 2 + "odata = d->memcreg.memc_chipid;" + NL
CHIPREV = T * 2 + "odata = d->memcreg.memc_chiprev;" + NL
LATCH_M = T * 3 + "if (!d->warned_memconf) {" + NL
MNOTE = T * 4 + '    " (once) ]' + BS + 'n", (int)idata, controller);' + NL
LATCH_D = T * 2 + "if (!d->warned_default) {" + NL
SET_D = T * 3 + "d->warned_default = 1;" + NL
DGUARD = T * 3 + "if (writeflag == MEM_WRITE)" + NL + T * 4 + 'fatal(": 0x%x", (int)idata);' + NL
DDIR = T * 3 + '    " (controller %i)", writeflag == MEM_WRITE ?' + NL
RDMAX = T * 2 + "idata = memory_readmax64(cpu, data, len);" + NL
F3 = ("chipid", "chiprev", "memconf")


def before(anchor, line):
    return [(anchor, line + anchor)]


def after(anchor, line):
    return [(anchor, anchor + line)]


V = []
for f in F3:   # Astra B1: the FIRST default store (inside the latch block) written into a served field
    V.append(("A_B1_" + f, after(LATCH_D, T * 3 + "if (writeflag == MEM_WRITE) d->memcreg.memc_" + f + " = idata;" + NL), "Astra B1"))
for f in F3:   # Astra B2 (= glm breach 4): a controller-0 default store written into a served field
    V.append(("A_B2_" + f, before(LATCH_D, T * 2 + "if (writeflag == MEM_WRITE && !controller) d->memcreg.memc_" + f + " = idata;" + NL),
              "Astra B2 / glm 4"))
for f, a in (("chipid", CHIPID), ("chiprev", CHIPREV)):   # Astra B3: served stores kept by OR / XOR
    for op, nm in (("|=", "or"), ("^=", "xor")):
        V.append(("A_B3_%s_%s" % (f, nm), after(a, T * 2 + "if (writeflag == MEM_WRITE) d->memcreg.memc_%s %s idata;" % (f, op) + NL), "Astra B3"))
for f, a in (("chipid", CHIPID), ("chiprev", CHIPREV)):   # Astra B4 / glm 3: controller-1 served store kept; glm 3: idata-gated keep
    V.append(("A_B4_" + f, after(a, T * 2 + "if (writeflag == MEM_WRITE && controller) d->memcreg.memc_" + f + " = idata;" + NL),
              "Astra B4 / glm 3"))
    V.append(("G_3_idata_" + f, after(a, T * 2 + "if (writeflag == MEM_WRITE && idata) d->memcreg.memc_" + f + " = idata;" + NL), "glm 3"))
for f, a in (("chipid", CHIPID), ("chiprev", CHIPREV)):   # Astra B5: a served access sets the memconf latch; B6: a served store sets the default latch
    V.append(("A_B5_" + f, after(a, T * 2 + "d->warned_memconf = 1;" + NL), "Astra B5"))
    V.append(("A_B6_" + f, after(a, T * 2 + "if (writeflag == MEM_WRITE) d->warned_default = 1;" + NL), "Astra B6"))
V.append(("A_B7_valctl0", [(DGUARD, DGUARD.replace("if (writeflag == MEM_WRITE)", "if (writeflag == MEM_WRITE && !controller)"))],
          "Astra B7 / glm 1"))
V.append(("G_1_dirctl0", [(DDIR, DDIR.replace("writeflag == MEM_WRITE ?", "writeflag == MEM_WRITE && controller == 0 ?"))], "glm 1 (ternary)"))
V.append(("A_B8_validata", [(DGUARD, DGUARD.replace("if (writeflag == MEM_WRITE)", "if (idata)"))], "Astra B8"))
V.append(("A_B8_diridata", [(DDIR, DDIR.replace("writeflag == MEM_WRITE ?", "idata ?"))], "Astra B8"))
V.append(("A_B9_dsetidata", [(SET_D, T * 3 + "d->warned_default = writeflag == MEM_WRITE ? idata : 1;" + NL)], "Astra B9"))
V.append(("A_B10_u8", [(RDMAX, RDMAX.replace("idata = memory_readmax64", "idata = (uint8_t)memory_readmax64"))], "Astra B10"))
V.append(("A_B10_u16", [(RDMAX, RDMAX.replace("idata = memory_readmax64", "idata = (uint16_t)memory_readmax64"))], "Astra B10"))
for f in F3:   # Astra B11: a default store ORs in its bit 2
    V.append(("A_B11_" + f, before(LATCH_D, T * 2 + "if (writeflag == MEM_WRITE) d->memcreg.memc_" + f + " |= idata & 0x04;" + NL), "Astra B11"))
for f in ("chipid", "chiprev"):   # Astra B12: the first controller-1 memconf store written into another served field
    V.append(("A_B12_" + f, after(LATCH_M, T * 4 + "if (controller) d->memcreg.memc_" + f + " = idata;" + NL), "Astra B12"))
V.append(("G_2_dlen1", [(LATCH_D, T * 2 + "if (!d->warned_default && len == 1) {" + NL)], "glm 2"))
V.append(("G_5_mnote_ff", [(MNOTE, MNOTE.replace("(int)idata, controller);", "(int)(idata & 0xff), controller);"))], "glm 5"))
V.append(("G_5_dval_ff", [(DGUARD, DGUARD.replace('(int)idata);', '(int)(idata & 0xff));'))], "glm 5"))
V.append(("G_6_dbit3", [(LATCH_D, T * 2 + "if (!d->warned_default && (relative_addr & 0x08)) {" + NL)], "glm 6 (conditional)"))


def pretable():
    out = [
        "PRETABLE_P3 -- mvme187memcoob, the pass-3 seats' floor findings (p3_20261105/codex_memc_p3.txt, ollama_glm.txt), written BEFORE",
        "the measurement (this file's mtime precedes table_p3/'s).  Instrument: table_p3/probe118_p3.py (the in-tree 118-row probe).",
        "Baseline: det_20261104/dev_mvme187.c.fix2.  Base leg first.  The prediction for EVERY variant is its seat's derivation: ALL 118",
        "GREEN (glm marked G_6_dbit3 conditional on R8's latch-setting offset).  A red row on any variant refutes that seat's finding.", "",
    ]
    for n, _, who in V:
        out.append("   %-17s %-22s predicted 118/118" % (n, who))
    return NL.join(out) + NL


def main():
    a = sys.argv[1:]
    if a == ["list"]:
        print(" ".join(n for n, _, _ in V))
    elif a == ["pretable"]:
        sys.stdout.write(pretable())
    elif len(a) == 4 and a[0] == "apply":
        s = io.open(a[2], encoding="latin-1", newline="").read()
        for old, new in dict((n, e) for n, e, _ in V)[a[1]]:
            if s.count(old) != 1:
                print("MUTANT-TEXT-NOT-FOUND", a[1], repr(old[:60]), s.count(old))
                sys.exit(3)
            s = s.replace(old, new)
        io.open(a[3], "w", encoding="latin-1", newline="").write(s)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
