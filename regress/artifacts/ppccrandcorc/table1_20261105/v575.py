#!/usr/bin/env python3
"""v575.py -- #575 ppccrandcorc test-variant TABLE 1 (2026-11-05): the variant sources, and EXACT predictions computed by simulating the
probe's sessions (regress/ppc_crlogic_probe.py, 62 rows) under each variant's handler semantics.  The simulator copies the probe's
session plans (table(), the edge session, the two field-mask rows); rows that read the debugger, the disassembler or mfcr are predicted
green on every variant (no variant touches them).  Its base and HEAD predictions are checked against the measured runs, which is what
licenses the rest.  Variants: the pass-1 ruling's nine (b1 b2 c d1-d6, regress/artifacts/ppccrandcorc/adj_p1_20261105/MYTHOS_local.md
R5) plus the field-mask weakenings the owed hi rows exist for (m1-m4: BA/BB mask & 7 and & 15) and the BT mask (t1, t2: & 7).
  v575.py write | pretable"""
import io
import os
import sys

T, NL = chr(9), chr(10)
HERE = os.path.dirname(os.path.abspath(__file__))
FIXF = "C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/src/cpus/cpu_ppc_instr.c"
FIX = io.open(FIXF, encoding="latin-1", newline="").read()

# ------------------------------------------------------------------------------------------------ the simulator
def crbit(cr, n):
    return (cr >> (31 - n)) & 1


def setbit(cr, n, v):
    m = 1 << (31 - n)
    return (cr | m) if v else (cr & ~m & 0xFFFFFFFF)


ARCH = {"crand": lambda a, b: a & b, "crandc": lambda a, b: a & (1 - b), "creqv": lambda a, b: 1 - (a ^ b),
        "cror": lambda a, b: a | b, "crorc": lambda a, b: a | (1 - b), "crnor": lambda a, b: 1 - (a | b), "crxor": lambda a, b: a ^ b}


def run(cr, insns, fns, masks):
    for op, bt, ba, bb in insns:
        mbt, mab = masks.get(op, (31, 31))
        bt, ba, bb = bt & mbt, ba & mab, bb & mab
        if fns[op] is None:
            continue
        cr = setbit(cr, bt, fns[op](crbit(cr, ba), crbit(cr, bb)))
    return cr


def sessions():
    """Yields (session, seed, insns, [(row, kind, bt-or-mask, want)]) in the probe's row order (rows read off the final CR)."""
    pick = {(0, 0): (0, 2), (0, 1): (0, 1), (1, 0): (1, 0), (1, 1): (1, 3)}

    def table(prefix, ops):
        seed = setbit(setbit(0, 1, 1), 3, 1)
        plan, bt = [], 8
        for op in ops:
            for ab in ((0, 0), (0, 1), (1, 0), (1, 1)):
                want = ARCH[op](*ab)
                seed = setbit(seed, bt, 1 - want)
                plan.append((op, ab, bt, want))
                bt += 1
        insns = [(op, b, pick[ab][0], pick[ab][1]) for op, ab, b, _ in plan]
        rows = [("%s %s %d%d" % (prefix, op, ab[0], ab[1]), "bit", b, w) for op, ab, b, w in plan]
        mask = 0
        for _, _, b, _ in plan:
            mask |= 1 << (31 - b)
        rows.append((prefix + " others", "others", mask, seed & ~mask & 0xFFFFFFFF))
        return (prefix, seed, insns, rows)
    yield table("64", ["crandc", "crorc"])
    yield table("s64", ["crand", "cror", "crnor", "creqv", "crxor"])
    eseed = setbit(setbit(setbit(setbit(0, 4, 1), 5, 1), 0, 1), 31, 0)
    emask = (1 << 31) | 1
    yield ("edge", eseed, [("crandc", 0, 2, 3), ("crorc", 31, 4, 5)],
           [("edge crandc bt0", "bit", 0, 0), ("edge crorc bt31", "bit", 31, 1),
            ("edge others", "others", emask, eseed & ~emask & 0xFFFFFFFF)])
    for name, op, bt, ba, bb, ones, zeros, want in (
            ("64 crandc hi", "crandc", 20, 31, 30, [31, 14, 6, 2, 0], [30, 15, 7, 3, 1], 1),
            ("64 crorc hi", "crorc", 21, 29, 28, [28, 13, 5, 1], [29, 12, 4, 0], 0)):
        seed = 0
        for n in ones:
            seed = setbit(seed, n, 1)
        for n in zeros:
            seed = setbit(seed, n, 0)
        seed = setbit(seed, bt, 1 - want)
        yield (name, seed, [(op, bt, ba, bb)], [(name, "bit", bt, want)])
    yield table("32", ["crandc", "crorc"])


def predict(fns, masks):
    red = []
    for _, seed, insns, rows in sessions():
        cr = run(seed, insns, fns, masks)
        for name, kind, arg, want in rows:
            got = crbit(cr, arg) if kind == "bit" else (cr & ~arg & 0xFFFFFFFF)
            if got != want:
                red.append(name.replace(" ", "_"))
    return red


def F(**over):
    d = dict(ARCH)
    d.update(over)
    return d


NAND, NOR = (lambda a, b: 1 - (a & b)), (lambda a, b: 1 - (a | b))
SPEC = {   # name: (fns, masks, C edit)
    "base": (F(), {}, None),
    "HEAD": (F(crandc=NAND, crorc=NOR), {}, None),
    "b1_crandc_nand": (F(crandc=NAND), {}, ("crandc", "if", "if (!(ba & bb))")),
    "b2_crorc_nor": (F(crorc=NOR), {}, ("crorc", "if", "if (!(ba | bb))")),
    "c_identity": (F(crandc=None, crorc=None), {}, ("both", "identity", None)),
    "d1_crandc_nba_and_b": (F(crandc=lambda a, b: (1 - a) & b), {}, ("crandc", "if", "if (!ba & bb)")),
    "d2_crorc_nba_or_b": (F(crorc=lambda a, b: (1 - a) | b), {}, ("crorc", "if", "if (!ba | bb)")),
    "d3_crandc_and": (F(crandc=lambda a, b: a & b), {}, ("crandc", "if", "if (ba & bb)")),
    "d4_crorc_or": (F(crorc=lambda a, b: a | b), {}, ("crorc", "if", "if (ba | bb)")),
    "d5_crandc_crossed": (F(crandc=lambda a, b: a | (1 - b)), {}, ("crandc", "if", "if (ba | !bb)")),
    "d6_crorc_crossed": (F(crorc=lambda a, b: a & (1 - b)), {}, ("crorc", "if", "if (ba & !bb)")),
    "m1_crandc_mask7": (F(), {"crandc": (31, 7)}, ("crandc", "abmask", "7")),
    "m2_crorc_mask7": (F(), {"crorc": (31, 7)}, ("crorc", "abmask", "7")),
    "m3_crandc_mask15": (F(), {"crandc": (31, 15)}, ("crandc", "abmask", "15")),
    "m4_crorc_mask15": (F(), {"crorc": (31, 15)}, ("crorc", "abmask", "15")),
    "t1_crandc_btmask7": (F(), {"crandc": (7, 31)}, ("crandc", "btmask", "7")),
    "t2_crorc_btmask7": (F(), {"crorc": (7, 31)}, ("crorc", "btmask", "7")),
}

LINE = {"crandc": T + "if (ba & !bb)" + T + "/*  #575: CR[BA] & ~CR[BB] (Book I); this was NAND  */" + NL,
        "crorc": T + "if (ba | !bb)" + T + "/*  #575: CR[BA] | ~CR[BB] (Book I); this was NOR  */" + NL}
HD = lambda op: ("X(" + op + ") {" + NL + T + "uint32_t iword = ic->arg[0]; int bt = (iword >> 21) & 31;" + NL +
                 T + "int ba = (iword >> 16) & 31, bb = (iword >> 11) & 31;" + NL)
CLR = T + "cpu->cd.ppc.cr &= ~(1 << (31-bt));" + NL
SET = T + T + "cpu->cd.ppc.cr |= (1 << (31-bt));" + NL


def one(s, old, new):
    assert s.count(old) == 1, (old[:70], s.count(old))
    return s.replace(old, new)


def source(edit):
    op, kind, arg = edit
    s = FIX
    if kind == "if":
        return one(s, LINE[op], T + arg + NL)
    if kind == "identity":
        for o in ("crandc", "crorc"):
            s = one(s, CLR + LINE[o] + SET, T + "(void) bt; (void) ba; (void) bb;" + NL)
        return s
    if kind == "abmask":
        return one(s, HD(op), HD(op).replace("(iword >> 16) & 31, bb = (iword >> 11) & 31;",
                                             "(iword >> 16) & %s, bb = (iword >> 11) & %s;" % (arg, arg)))
    if kind == "btmask":
        return one(s, HD(op), HD(op).replace("int bt = (iword >> 21) & 31;", "int bt = (iword >> 21) & %s;" % arg))
    raise ValueError(kind)


def write():
    out = os.path.join(HERE, "variants")
    os.makedirs(out, exist_ok=True)
    n = 0
    for name, (_, _, edit) in SPEC.items():
        if edit:
            t = source(edit)
            assert t != FIX
            io.open(os.path.join(out, name + ".c"), "w", encoding="latin-1", newline="").write(t)
            n += 1
    print("%d variants written" % n)


def pretable():
    L = ["PRETABLE -- #575 ppccrandcorc, test-variant table 1 (62 rows).  Written BEFORE table 1 runs (its mtime precedes every file",
         "in table1/).  Instrument: table1/probe62_frozen.py (the in-tree probe after apply_r575.py).  Baseline: the fix (GXEMUL-SEC",
         "src/cpus/cpu_ppc_instr.c).  Every prediction below is EXACT and COMPUTED by v575.py's simulator of the probe's sessions;",
         "rows reading the debugger, the disassembler or mfcr are predicted green on every variant.  The base and HEAD legs check the",
         "simulator itself.  Null media (/bin/true, an absent binary, /bin/false): CONTROL=FAIL.  c_identity is the ruled null medium",
         "of the two handlers (identity bodies).",
         "", "ROW MANIFEST (session: seed; instructions as op BT,BA,BB; rows):"]
    for sess, seed, insns, rows in sessions():
        L.append("  %-12s seed=0x%08x  %s" % (sess, seed, "  ".join("%s %d,%d,%d" % i for i in insns)))
        L.append("               rows: " + ", ".join(r[0] for r in rows))
    L += ["", "VARIANTS (exact red sets):"]
    for name, (fns, masks, _) in SPEC.items():
        red = predict(fns, masks)
        L.append("   %-22s %2d red: %s" % (name, len(red), ",".join(red) or "none"))
    return NL.join(L) + NL


if __name__ == "__main__":
    if sys.argv[1:] == ["write"]:
        write()
    elif sys.argv[1:] == ["pretable"]:
        sys.stdout.write(pretable())
    else:
        sys.exit(__doc__)
