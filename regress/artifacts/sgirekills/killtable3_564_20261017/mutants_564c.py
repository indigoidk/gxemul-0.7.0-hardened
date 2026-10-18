#!/usr/bin/env python3
"""mutants_564c.py <fixed dev_sgi_re.c> <out dir> -- TABLE 3 of #564's kill table, for the pass-2 repair (F9, F10):
  * the 20 LATCH-CONDITIONED LABEL-SWAP variants the 2026-09-25 skipped-dispatch clause enumerates for S1 and S2,
    whose `return' bypasses `switch (dst_tlb)': each exempts ONE destination label in ONE latch state --
    {A, B, C, LIN_A, LIN_B} x {SET, CLEAR} x {S1, S2}.  (A plain label exemption exempts a superset of cells, so
    its detection follows from either conditioned variant's.)  Labels 3 (TEX), 6 (CLIP) and 7 reach `default:',
    which writes nothing, and are excluded as host-debug only;
  * one ALIAS per new latch bit onto a PRE-EXISTING bit no other session sets (F10): STIPPLE -> 10 (BADMODE) and
    COPY -> 11 (TEX_RD), the two the pass-2 seat named, plus SRC -> 6 (DE_LEN), DEPTH -> 12 (BADCOLOR) and
    BYTEMASK -> 8 (UNMAP_RD).  Every other (site, bit) pair is covered BY CONSTRUCTION via the `xbit primed' row;
  * the ACCEPT face at tiled B and C: S1 and S2 grown to refuse every transfer to B, or to C (`fill b ok', `fill c ok').
    The latch-conditioned accept-face variants are disclosed in the probe's contract, not measured.
Each line names its predicted catchers; the table is scored against the repaired instrument."""
import io, os, sys

G1 = 'if (mode & MTE_MODE_STIPPLE) {\n\t\tif (!(d->warned & SGIRE_W_MTE_STIPPLE))'
G2 = 'if (src > MTE_TLB_C) {\n'
DST = "((mode & MTE_MODE_DST_BUF_MASK) >> MTE_DST_TLB_SHIFT)"     # dst_tlb is not yet computed at S1
LAB = (("a", "MTE_TLB_A"), ("b", "MTE_TLB_B"), ("c", "MTE_TLB_C"), ("la", "MTE_TLB_LIN_A"), ("lb", "MTE_TLB_LIN_B"))
#  the rows that hold each (site, label, state) cell in the repaired instrument
CELL = {
    ("s1", "a", "clr"): "stip a",   ("s1", "a", "set"): "stip copy, latch paint (s1again)",
    ("s1", "b", "clr"): "stip b clr", ("s1", "b", "set"): "stip b",
    ("s1", "c", "clr"): "stip c clr", ("s1", "c", "set"): "stip c",
    ("s1", "la", "clr"): "stip la clr", ("s1", "la", "set"): "stip lin a",
    ("s1", "lb", "clr"): "stip lb clr", ("s1", "lb", "set"): "stip lin b",
    ("s2", "a", "clr"): "src 3, latch paint", ("s2", "a", "set"): "src 4, src 5, src 6, src 7, src 3 copy",
    ("s2", "b", "clr"): "src b clr",  ("s2", "b", "set"): "src 3 b",
    ("s2", "c", "clr"): "src c clr",  ("s2", "c", "set"): "src 3 c",
    ("s2", "la", "clr"): "src la clr", ("s2", "la", "set"): "src 3 lin",
    ("s2", "lb", "clr"): "src lb clr", ("s2", "lb", "set"): "src 3 lin b",
}
M = []
for site, guard in (("s1", G1), ("s2", G2)):
    for lab, sym in LAB:
        for st in ("set", "clr"):
            bit = "SGIRE_W_MTE_STIPPLE" if site == "s1" else "SGIRE_W_MTE_SRC"
            latch = "(d->warned & %s)" % bit if st == "set" else "!(d->warned & %s)" % bit
            if site == "s1":
                new = guard.replace("if (mode & MTE_MODE_STIPPLE) {",
                                    "if ((mode & MTE_MODE_STIPPLE) && !(%s == %s && %s)) {" % (DST, sym, latch))
            else:
                new = guard.replace("if (src > MTE_TLB_C) {",
                                    "if (src > MTE_TLB_C && !(dst_tlb == %s && %s)) {" % (sym, latch))
            M.append(("%s%s%s" % (site, lab, st), [(guard, new)], CELL[(site, lab, st)]))
ALIAS = (("xs1b10", "SGIRE_W_MTE_STIPPLE  = 1 << 13,", "1 << 10", "xbit texts"),
         ("xs2b6",  "SGIRE_W_MTE_SRC      = 1 << 14,", "1 << 6",  "xbit texts"),
         ("xs3b11", "SGIRE_W_MTE_COPY     = 1 << 15,", "1 << 11", "xbit texts"),
         ("xs4b12", "SGIRE_W_MTE_DEPTH    = 1 << 16,", "1 << 12", "xbit texts"),
         ("xs5b8",  "SGIRE_W_MTE_BYTEMASK = 1 << 17,", "1 << 8",  "xbit texts"))
for name, line, val, pred in ALIAS:
    M.append((name, [(line, line.rsplit("=", 1)[0] + "= " + val + ",")], pred))
#  the ACCEPT face at tiled B and C (Astra, F2 Q4): a guard grown to refuse every transfer to ONE label
for lab, sym in (("b", "MTE_TLB_B"), ("c", "MTE_TLB_C")):
    M.append(("s1g" + lab, [(G1, G1.replace("if (mode & MTE_MODE_STIPPLE) {",
                                             "if ((mode & MTE_MODE_STIPPLE) || %s == %s) {" % (DST, sym)))],
              "fill %s ok" % lab))
    M.append(("s2g" + lab, [(G2, G2.replace("if (src > MTE_TLB_C) {",
                                             "if (src > MTE_TLB_C || dst_tlb == %s) {" % sym))],
              "fill %s ok" % lab))

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
