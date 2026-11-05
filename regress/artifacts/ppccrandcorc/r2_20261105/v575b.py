#!/usr/bin/env python3
"""v575b.py -- #575 ppccrandcorc ROUND 2 (2026-11-05): table1_20261105/v575.py extended for CLASS CLOSURE BY SIMULATION.

The simulator copies the probe's session plans (regress/ppc_crlogic_probe.py: table(), the edge session, the two `hi' rows, and
the four round-2 pin rows) and executes X(crandc)/X(crorc) (src/cpus/cpu_ppc_instr.c:2729-2737, 2756-2764) statement by statement
under a SINGLE-EDIT VARIANT dict, so that every cell of the enumeration below can be expressed:

    mbt/mba/mbb = m     the field mask `& 31' at BT/BA/BB replaced by `& m', m in 0..30 (one site at a time)
    ba_src = BB|BT      the BA read `(cr >> (31-ba))' takes another field's index; bb_src = BA|BT likewise (at the BB read the
                        variable `ba' ALREADY holds the Boolean value, so bb_src=BA reads CR[a], a in {0,1})
    rma/rmb = 3|7       the read mask `& 1' widened at the BA/BB read (a, b then range over 0..7; the conditions keep C semantics)
    clear = early|none|xor   the clear moved before both reads | deleted | replaced by a toggle (the probe's disclosed escape)
    set = none|xor      the set deleted | `|=' replaced by `^='
    cond = f(a, b, bt)  a condition edit (table 1's b, d1-d6; the pass-1 ruling's four R5 bt-substitutions)
    identity            the whole body removed (table 1's c, per handler or both)
    decode = op'        the dispatch case (cpu_ppc_instr.c:4638/4641) bound to another CR-logical handler

Only the apparatus rows (ctl*, neg apparatus, *session, *mfcr, *disasm) are predicted green unconditionally: no cell touches the
debugger, mfcr or the disassembler.  The semantic rows (bit rows, `others' rows) are computed.  The old 62-row predictions are
re-derived and checked against table1_20261105/PRETABLE.out (`check62'), which is what licenses the rest.

  v575b.py check62 | closure | pretable2 | write | errata62"""
import io
import os
import random
import sys

T, NL = chr(9), chr(10)
HERE = os.path.dirname(os.path.abspath(__file__))
A = os.path.dirname(HERE)
FIXF = "C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/src/cpus/cpu_ppc_instr.c"
FIX = io.open(FIXF, encoding="latin-1", newline="").read()
OPS = ("crand", "crandc", "creqv", "cror", "crorc", "crnor", "crxor")
EDITED = ("crandc", "crorc")


# ------------------------------------------------------------------------------------------------ the simulator
def crbit(cr, n):
    return (cr >> (31 - n)) & 1


def bitof(n):
    return 1 << (31 - n)


def setbit(cr, n, v):
    return (cr | bitof(n)) if v else (cr & ~bitof(n) & 0xFFFFFFFF)


def NOT(x):          # C `!x' on an int
    return 0 if x else 1


# C-exact conditions on ints a, b (0..7 once a read mask is widened) and the masked BT field index.
COND = {"crand": lambda a, b, bt: (a & b) != 0,
        "crandc": lambda a, b, bt: (a & NOT(b)) != 0,          # the fix, :2735
        "creqv": lambda a, b, bt: (a ^ b) == 0,
        "cror": lambda a, b, bt: (a | b) != 0,
        "crorc": lambda a, b, bt: (a | NOT(b)) != 0,           # the fix, :2762
        "crnor": lambda a, b, bt: (a | b) == 0,
        "crxor": lambda a, b, bt: (a ^ b) != 0}
ARCH = dict((op, (lambda a, b, f=COND[op]: int(f(a, b, 0)))) for op in OPS)   # Book I wants on 0/1 operands

COND_EDITS = {
    "crandc": [("b1  !(ba & bb)  (NAND restored)", lambda a, b, bt: (a & b) == 0, "if (!(ba & bb))"),
               ("d1  !ba & bb", lambda a, b, bt: (NOT(a) & b) != 0, "if (!ba & bb)"),
               ("d3  ba & bb   (complement dropped)", lambda a, b, bt: (a & b) != 0, "if (ba & bb)"),
               ("d5  ba | !bb  (operator crossed)", lambda a, b, bt: (a | NOT(b)) != 0, "if (ba | !bb)"),
               ("r5a bt & !bb", lambda a, b, bt: (bt & NOT(b)) != 0, "if (bt & !bb)"),
               ("r5b ba & !bt", lambda a, b, bt: (a & NOT(bt)) != 0, "if (ba & !bt)")],
    "crorc": [("b2  !(ba | bb)  (NOR restored)", lambda a, b, bt: (a | b) == 0, "if (!(ba | bb))"),
              ("d2  !ba | bb", lambda a, b, bt: (NOT(a) | b) != 0, "if (!ba | bb)"),
              ("d4  ba | bb   (complement dropped)", lambda a, b, bt: (a | b) != 0, "if (ba | bb)"),
              ("d6  ba & !bb  (operator crossed)", lambda a, b, bt: (a & NOT(b)) != 0, "if (ba & !bb)"),
              ("r5c bt | !bb", lambda a, b, bt: (bt | NOT(b)) != 0, "if (bt | !bb)"),
              ("r5d ba | !bt", lambda a, b, bt: (a | NOT(bt)) != 0, "if (ba | !bt)")]}


def exec1(cr, op, bt, ba, bb, V):
    """One CR-logical handler (cpu_ppc_instr.c:2720-2782) on cr, under the single-edit variant V ({} = the fix)."""
    if V.get("identity"):
        return cr
    body = V.get("decode", op)
    if body != op:
        return exec1(cr, body, bt, ba, bb, {})
    bt, ba, bb = bt & V.get("mbt", 31), ba & V.get("mba", 31), bb & V.get("mbb", 31)
    fbt, fba, fbb = bt, ba, bb
    clr = V.get("clear", "and")
    if clr == "early":
        cr = cr & ~bitof(fbt) & 0xFFFFFFFF
    a = (cr >> (31 - {"BA": fba, "BB": fbb, "BT": fbt}[V.get("ba_src", "BA")])) & V.get("rma", 1)
    b = (cr >> (31 - {"BB": fbb, "BA": a, "BT": fbt}[V.get("bb_src", "BB")])) & V.get("rmb", 1)
    if clr == "and":
        cr = cr & ~bitof(fbt) & 0xFFFFFFFF
    elif clr == "xor":
        cr ^= bitof(fbt)
    if V.get("cond", COND[op])(a, b, fbt):
        st = V.get("set", "or")
        if st == "or":
            cr |= bitof(fbt)
        elif st == "xor":
            cr ^= bitof(fbt)
    return cr


def run(cr, insns, VV):
    for op, bt, ba, bb in insns:
        cr = exec1(cr, op, bt, ba, bb, VV.get(op, {}))
    return cr


# ------------------------------------------------------------------------------------------------ the probe's sessions
PICK = {(0, 0): (0, 2), (0, 1): (0, 1), (1, 0): (1, 0), (1, 1): (1, 3)}
APPARATUS = ["ctl session", "ctl live", "ctl seed holds", "ctl cr seed", "ctl mfcr", "neg apparatus"]

# Round-2 pin rows (single instruction each; seeds as the probe computes them).  `preset' records how CR[BT] is seeded.
PINS = [
    # name, op, bt, ba, bb, seed, want, preset
    ("64 crandc bbmask", "crandc", 16, 5, 31, setbit(0xFFFFFFFF, 31, 0), 1, "EQUAL to the result (1)"),
    ("64 crandc order", "crandc", 9, 5, 9, setbit(setbit(0, 5, 1), 9, 1), 0, "inverse (1)"),
    ("64 crorc bamask", "crorc", 16, 31, 5, setbit(setbit(0xFFFFFFFF, 31, 0), 16, 0), 0, "EQUAL to the result (0)"),
    ("64 crorc bbmask", "crorc", 31, 5, 31, setbit(0, 31, 1), 0, "inverse (1)"),
]


def sessions(new=True):
    """Yields (session, seed, insns, rows) in the probe's order; rows = [(name, kind, bt-or-mask, want)], kind in
    bit|others|app (app = apparatus row, always green)."""
    def table(prefix, ops):
        seed = setbit(setbit(0, 1, 1), 3, 1)
        plan, bt = [], 8
        for op in ops:
            for ab in ((0, 0), (0, 1), (1, 0), (1, 1)):
                want = ARCH[op](*ab)
                seed = setbit(seed, bt, 1 - want)
                plan.append((op, ab, bt, want))
                bt += 1
        insns = [(op, b, PICK[ab][0], PICK[ab][1]) for op, ab, b, _ in plan]
        rows = [(prefix + " session", "app", 0, 0)]
        rows += [("%s %s %d%d" % (prefix, op, ab[0], ab[1]), "bit", b, w) for op, ab, b, w in plan]
        mask = 0
        for _, _, b, _ in plan:
            mask |= bitof(b)
        rows.append((prefix + " others", "others", mask, seed & ~mask & 0xFFFFFFFF))
        rows += [(prefix + " mfcr", "app", 0, 0), (prefix + " disasm", "app", 0, 0)]
        return (prefix, seed, insns, rows)
    yield ("ctl", 0, [], [(n, "app", 0, 0) for n in APPARATUS])
    yield table("64", ["crandc", "crorc"])
    yield table("s64", ["crand", "cror", "crnor", "creqv", "crxor"])
    eseed = setbit(setbit(setbit(setbit(0, 4, 1), 5, 1), 0, 1), 31, 0)
    emask = bitof(0) | bitof(31)
    yield ("edge", eseed, [("crandc", 0, 2, 3), ("crorc", 31, 4, 5)],
           [("edge session", "app", 0, 0), ("edge crandc bt0", "bit", 0, 0), ("edge crorc bt31", "bit", 31, 1),
            ("edge others", "others", emask, eseed & ~emask & 0xFFFFFFFF), ("edge mfcr", "app", 0, 0),
            ("edge disasm", "app", 0, 0)])
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
    if new:
        for name, op, bt, ba, bb, seed, want, _ in PINS:
            yield (name, seed, [(op, bt, ba, bb)], [(name, "bit", bt, want)])
    yield table("32", ["crandc", "crorc"])


def names(new=True):
    return [r[0] for _, _, _, rows in sessions(new) for r in rows]


def predict(VV, new=True):
    """Red row names (spaces -> underscores, as SCORES.txt writes them) for the variant VV = {op: V}."""
    red = []
    for _, seed, insns, rows in sessions(new):
        cr = run(seed, insns, VV)
        for name, kind, arg, want in rows:
            if kind == "app":
                continue
            got = crbit(cr, arg) if kind == "bit" else (cr & ~arg & 0xFFFFFFFF)
            if got != want:
                red.append(name.replace(" ", "_"))
    return red


def both(V):
    return {"crandc": dict(V), "crorc": dict(V)}


# ------------------------------------------------------------------------------------------------ the enumeration
def cells():
    """Every cell: (cls, label, VV).  cls in mask|read|rmask|clear|set|cond|decode."""
    for op in EDITED:
        for site, key in (("BT", "mbt"), ("BA", "mba"), ("BB", "mbb")):
            for m in range(31):
                yield ("mask", "%s %s mask &%d" % (op, site, m), {op: {key: m}})
        for src, other in (("BA", "BB"), ("BA", "BT"), ("BB", "BA"), ("BB", "BT")):
            yield ("read", "%s %s read <- %s index" % (op, src, other), {op: {("ba_src" if src == "BA" else "bb_src"): other}})
        for src, key in (("BA", "rma"), ("BB", "rmb")):
            for m in (3, 7):
                yield ("rmask", "%s %s read mask &%d" % (op, src, m), {op: {key: m}})
        yield ("clear", op + " clear moved before the reads", {op: {"clear": "early"}})
        yield ("clear", op + " clear deleted", {op: {"clear": "none"}})
        yield ("clear", op + " clear -> toggle (^=)", {op: {"clear": "xor"}})
        yield ("set", op + " set deleted", {op: {"set": "none"}})
        yield ("set", op + " set |= -> ^=", {op: {"set": "xor"}})
        for label, fn, _ in COND_EDITS[op]:
            yield ("cond", op + " cond " + label, {op: {"cond": fn}})
        yield ("cond", op + " identity body", {op: {"identity": True}})
        for other in OPS:
            if other != op:
                yield ("decode", "%s dispatch -> instr(%s)" % (op, other), {op: {"decode": other}})
    yield ("cond", "c   both bodies identity", both({"identity": True}))


def equivalent(VV, trials=40000):
    """Random differential test of the variant against the fix over (cr, bt, ba, bb); True = no difference found."""
    rnd = random.Random(575)
    for _ in range(trials):
        cr = rnd.getrandbits(32)
        for op in VV:
            bt, ba, bb = rnd.randrange(32), rnd.randrange(32), rnd.randrange(32)
            if exec1(cr, op, bt, ba, bb, VV[op]) != exec1(cr, op, bt, ba, bb, {}):
                return False
    return True


EXCLUDED = {"crandc clear -> toggle (^=)": "disclosed in the probe's clause (e)(5): every crandc row with result 0 pre-sets the inverse"}
EQUIV_WHY = {
    "crandc BA read mask &3": "`ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can survive",
    "crandc BA read mask &7": "same: (ba & !bb) != 0  <=>  (ba & 1) && !bb",
    "crandc set |= -> ^=": "the clear at :2734 has just zeroed the bit, so ^= and |= set it alike",
    "crorc set |= -> ^=": "the clear at :2761 has just zeroed the bit, so ^= and |= set it alike",
}


def closure():
    old62, new66 = set(names(False)), set(names(True))
    L = ["# #575 ppccrandcorc -- CLASS CLOSURE BY SIMULATION (round 2, 2026-11-05)", "",
         "Simulator: r2_20261105/v575b.py (table1_20261105/v575.py extended; `v575b.py check62' re-derives table 1's 17 predictions",
         "on the old 62 rows and matches PRETABLE.out exactly).  Handlers simulated statement by statement:",
         "src/cpus/cpu_ppc_instr.c X(crandc) :2729-2737 and X(crorc) :2756-2764; dispatch :4638 and :4641.", "",
         "ENUMERATION (one edit per cell, per handler): field mask m in 0..30 at BT, BA, BB (3 x 31); each source read taking another",
         "field's index (BA<-BB, BA<-BT, BB<-BA, BB<-BT); the read mask `& 1' widened to `& 3' and `& 7' at BA and at BB; the clear moved",
         "before the reads, deleted, or replaced by a toggle; the set deleted or `|=' -> `^='; the condition edits table 1 had (b, d-moved,",
         "d-dropped, d-crossed) plus the pass-1 ruling's four R5 bt-substitutions and the identity body; the dispatch case bound to each",
         "of the six other CR-logical handlers; and table 1's c (both bodies identity).", ""]
    cl = list(cells())
    per = {}
    for cls, _, _ in cl:
        per[cls] = per.get(cls, 0) + 1
    L.append("DENOMINATOR: %d cells = %s." % (len(cl), " + ".join("%d %s" % (n, c) for c, n in sorted(per.items()))))
    L.append("")
    missed62, missed66, equiv, excl = [], [], [], []
    rowsmap = []
    for cls, label, VV in cl:
        r62 = predict(VV, new=False)
        r66 = predict(VV, new=True)
        newhit = [r for r in r66 if r.replace("_", " ") not in old62]
        status = "DETECTED(62)"
        if not r62:
            missed62.append(label)
            if r66:
                status = "MISSED by 62, CLOSED by " + ",".join(newhit)
            elif label in EQUIV_WHY:
                status = "EQUIVALENT"
                equiv.append(label)
            elif label in EXCLUDED:
                status = "EXCLUDED"
                excl.append(label)
            else:
                status = "**UNDETECTED**"
                missed66.append(label)
        eq = equivalent(VV) if not r66 else False
        rowsmap.append((cls, label, status, r62, r66, eq))
    L.append("CELL -> ROW MAP (62 = red rows of the old probe; 66 = red rows of the new one; `rand-equiv' = 40000 random (cr,BT,BA,BB)")
    L.append("found no difference from the fix):")
    L.append("")
    L.append("| class | cell | status | red on 62 | red on 66 |")
    L.append("|---|---|---|---|---|")
    for cls, label, status, r62, r66, eq in rowsmap:
        L.append("| %s | %s | %s%s | %s | %s |" % (cls, label, status, " rand-equiv" if eq else "",
                                                   ",".join(r62) or "none", ",".join(r66) or "none"))
    L += ["", "MISSED BY THE 62 ROWS (%d cells):" % len(missed62)]
    for m in missed62:
        L.append("  - " + m)
    L += ["", "EQUIVALENT (%d cells; proved, not merely unobserved):" % len(equiv)]
    for m in equiv:
        L.append("  - %s: %s" % (m, EQUIV_WHY[m]))
    L += ["", "EXCLUDED (%d cells):" % len(excl)]
    for m in excl:
        L.append("  - %s: %s" % (m, EXCLUDED[m]))
    L += ["", "STILL UNDETECTED BY THE 66 ROWS (%d cells):" % len(missed66)]
    for m in missed66:
        L.append("  - " + m)
    L += ["", "NEW ROWS (4; single-instruction sessions shaped like the `hi' rows):"]
    for name, op, bt, ba, bb, seed, want, preset in PINS:
        L.append("  %-17s %s BT=%d BA=%d BB=%d seed=0x%08x want=%d  CR[BT] pre-set %s" % (name, op, bt, ba, bb, seed, want, preset))
    L += ["",
          "WHY THESE FOUR AND NO FEWER.  A source-site row detects mask m iff CR[x & m] != CR[x] with the other operand decisive; with",
          "x = 31 every m in 0..30 is an alias, so one row per site with CR[0..30] uniformly opposite to CR[31] closes the whole site.",
          "crandc BB needs a = 1 and CR[0..30] = 1, CR[31] = 0 (want 1): pre-setting CR[BT] EQUAL to the result keeps the uniform seed",
          "and makes the same row read CR[BT] = 1 != CR[BB] = 0 for the BB<-BT cell (an inverse pre-set hides BB<-BT on every row, as",
          "codex B1-B2 show).  crandc clear-before-read needs BT == BB with b = 1 (want 0), a different seed: its own row (BT == BA is",
          "invisible for crandc: a is forced to 1-want, and the early clear changes a only when b = 1, where the result is 0 either",
          "way).  crorc BA needs b = 1, CR[0..30] = 1, CR[31] = 0 (want 0); pre-setting CR[BT] = 0 EQUAL to the result makes it read",
          "CR[BT] = 0 != CR[BB] = 1 for BB<-BT, and incidentally sees the crorc toggle (a 0 result pre-set 0).  Its one blind alias",
          "(m = 16 = BT) is red on `64 crorc 11' (BA 1 -> 0).  crorc BB needs a = 0, CR[0..30] = 0, CR[31] = 1 (want 0): with BT = BB = 31",
          "the inverse pre-set IS CR[31] = 1, and the same row is the crorc clear-before-read pin.  The two crandc needs (want 1 uniform",
          "ones; BT == BB with b = 1) and the two crorc needs (uniform ones; uniform zeros) are pairwise incompatible seeds, so four rows",
          "is the minimum for single-instruction sessions.",
          "",
          "OLD rows: %d.  NEW rows: %d (N = %d)." % (len(old62), len(new66) - len(old62), len(new66))]
    return NL.join(L) + NL, missed66


# ------------------------------------------------------------------------------------------------ variants (C sources)
LINE = {"crandc": T + "if (ba & !bb)" + T + "/*  #575: CR[BA] & ~CR[BB] (Book I); this was NAND  */" + NL,
        "crorc": T + "if (ba | !bb)" + T + "/*  #575: CR[BA] | ~CR[BB] (Book I); this was NOR  */" + NL}
HD = lambda op: ("X(" + op + ") {" + NL + T + "uint32_t iword = ic->arg[0]; int bt = (iword >> 21) & 31;" + NL +
                 T + "int ba = (iword >> 16) & 31, bb = (iword >> 11) & 31;" + NL)
RA = T + "ba = (cpu->cd.ppc.cr >> (31-ba)) & 1;" + NL
RB = T + "bb = (cpu->cd.ppc.cr >> (31-bb)) & 1;" + NL
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
        for o in EDITED:
            s = one(s, CLR + LINE[o] + SET, T + "(void) bt; (void) ba; (void) bb;" + NL)
        return s
    if kind == "abmask":
        return one(s, HD(op), HD(op).replace("(iword >> 16) & 31, bb = (iword >> 11) & 31;",
                                             "(iword >> 16) & %s, bb = (iword >> 11) & %s;" % (arg, arg)))
    if kind == "btmask":
        return one(s, HD(op), HD(op).replace("int bt = (iword >> 21) & 31;", "int bt = (iword >> 21) & %s;" % arg))
    if kind == "bamask":
        return one(s, HD(op), HD(op).replace("ba = (iword >> 16) & 31,", "ba = (iword >> 16) & %s," % arg))
    if kind == "bbmask":
        return one(s, HD(op), HD(op).replace("bb = (iword >> 11) & 31;", "bb = (iword >> 11) & %s;" % arg))
    if kind == "bbreadbt":
        return one(s, HD(op) + RA + RB, HD(op) + RA + RB.replace("(31-bb)", "(31-bt)"))
    if kind == "earlyclear":
        return one(s, HD(op) + RA + RB + CLR, HD(op) + CLR + RA + RB)
    if kind == "bbread":
        return one(s, HD(op) + RA + RB, HD(op) + RA + RB.replace("& 1;", "& %s;" % arg))
    if kind == "baread":
        return one(s, HD(op) + RA + RB, HD(op) + RA.replace("& 1;", "& %s;" % arg) + RB)
    raise ValueError(kind)


def cond(op, idx):
    return COND_EDITS[op][idx][1]


SPEC = {   # name: (VV, C edit)  -- table 1's 15 first (same names, same edits), then the round-2 closures
    "base": ({}, None),
    "HEAD": ({"crandc": {"cond": cond("crandc", 0)}, "crorc": {"cond": cond("crorc", 0)}}, None),
    "b1_crandc_nand": ({"crandc": {"cond": cond("crandc", 0)}}, ("crandc", "if", "if (!(ba & bb))")),
    "b2_crorc_nor": ({"crorc": {"cond": cond("crorc", 0)}}, ("crorc", "if", "if (!(ba | bb))")),
    "c_identity": (both({"identity": True}), ("both", "identity", None)),
    "d1_crandc_nba_and_b": ({"crandc": {"cond": cond("crandc", 1)}}, ("crandc", "if", "if (!ba & bb)")),
    "d2_crorc_nba_or_b": ({"crorc": {"cond": cond("crorc", 1)}}, ("crorc", "if", "if (!ba | bb)")),
    "d3_crandc_and": ({"crandc": {"cond": cond("crandc", 2)}}, ("crandc", "if", "if (ba & bb)")),
    "d4_crorc_or": ({"crorc": {"cond": cond("crorc", 2)}}, ("crorc", "if", "if (ba | bb)")),
    "d5_crandc_crossed": ({"crandc": {"cond": cond("crandc", 3)}}, ("crandc", "if", "if (ba | !bb)")),
    "d6_crorc_crossed": ({"crorc": {"cond": cond("crorc", 3)}}, ("crorc", "if", "if (ba & !bb)")),
    "m1_crandc_mask7": ({"crandc": {"mba": 7, "mbb": 7}}, ("crandc", "abmask", "7")),
    "m2_crorc_mask7": ({"crorc": {"mba": 7, "mbb": 7}}, ("crorc", "abmask", "7")),
    "m3_crandc_mask15": ({"crandc": {"mba": 15, "mbb": 15}}, ("crandc", "abmask", "15")),
    "m4_crorc_mask15": ({"crorc": {"mba": 15, "mbb": 15}}, ("crorc", "abmask", "15")),
    "t1_crandc_btmask7": ({"crandc": {"mbt": 7}}, ("crandc", "btmask", "7")),
    "t2_crorc_btmask7": ({"crorc": {"mbt": 7}}, ("crorc", "btmask", "7")),
    # ---- round 2: codex B1-B9 (p2_20261105/codex_codex_r575_p2.txt), glm's read-mask cells, one more crandc BB mask cell
    "s1_crandc_bb_from_bt": ({"crandc": {"bb_src": "BT"}}, ("crandc", "bbreadbt", None)),          # B1
    "s2_crorc_bb_from_bt": ({"crorc": {"bb_src": "BT"}}, ("crorc", "bbreadbt", None)),             # B2
    "o1_crandc_earlyclear": ({"crandc": {"clear": "early"}}, ("crandc", "earlyclear", None)),      # B3 (glm breach 1)
    "o2_crorc_earlyclear": ({"crorc": {"clear": "early"}}, ("crorc", "earlyclear", None)),         # B4 (glm breach 1)
    "m5_crandc_bbmask29": ({"crandc": {"mbb": 29}}, ("crandc", "bbmask", "29")),                   # B5
    "m6_crandc_bbmask27": ({"crandc": {"mbb": 27}}, ("crandc", "bbmask", "27")),                   # B6
    "m7_crandc_bbmask23": ({"crandc": {"mbb": 23}}, ("crandc", "bbmask", "23")),                   # B7
    "m8_crorc_bamask29": ({"crorc": {"mba": 29}}, ("crorc", "bamask", "29")),                      # B8
    "m9_crorc_bbmask29": ({"crorc": {"mbb": 29}}, ("crorc", "bbmask", "29")),                      # B9
    "m10_crandc_bbmask17": ({"crandc": {"mbb": 17}}, ("crandc", "bbmask", "17")),                  # a 62-miss codex's sweep lacked
    "g1_crandc_bbread3": ({"crandc": {"rmb": 3}}, ("crandc", "bbread", "3")),                      # glm breach 2, BB site (real)
    "g2_crandc_baread3": ({"crandc": {"rma": 3}}, ("crandc", "baread", "3")),                      # glm breach 2, BA site: EQUIVALENT
}
PREDICTED_ONLY = {   # the pass-1 ruling's R5 bt-substitutions: predicted, not built (PRETABLE.errata.md supplies the 62-row sets)
    "r5a_crandc_bt_and_nbb": {"crandc": {"cond": cond("crandc", 4)}},
    "r5b_crandc_ba_and_nbt": {"crandc": {"cond": cond("crandc", 5)}},
    "r5c_crorc_bt_or_nbb": {"crorc": {"cond": cond("crorc", 4)}},
    "r5d_crorc_ba_or_nbt": {"crorc": {"cond": cond("crorc", 5)}},
}


def write():
    out = os.path.join(HERE, "variants")
    os.makedirs(out, exist_ok=True)
    n = 0
    for name, (_, edit) in SPEC.items():
        if edit:
            t = source(edit)
            assert t != FIX
            io.open(os.path.join(out, name + ".c"), "w", encoding="latin-1", newline="").write(t)
            n += 1
    print("%d variants written to %s" % (n, out))


def check62():
    """Re-derive table 1's 17 predictions on the old 62 rows and compare with table1_20261105/PRETABLE.out."""
    want = {}
    for line in io.open(os.path.join(A, "table1_20261105", "PRETABLE.out"), encoding="latin-1"):
        parts = line.split()
        if len(parts) >= 3 and parts[0] in SPEC and parts[2] == "red:":
            want[parts[0]] = [] if parts[3] == "none" else parts[3].split(",")
    bad = 0
    for name in list(SPEC)[:17]:
        got = predict(SPEC[name][0], new=False)
        ok = got == want.get(name)
        bad += not ok
        print("%-22s %s %2d red" % (name, "OK  " if ok else "DIFF", len(got)))
    print("check62: %d of 17 match PRETABLE.out; old rows = %d" % (17 - bad, len(names(False))))
    return bad == 0


def pretable2():
    N = len(names(True))
    L = ["PRETABLE_2 -- #575 ppccrandcorc, test-variant table 2 (%d rows).  Written BEFORE table 2 runs.  Instrument: the in-tree" % N,
         "probe regress/ppc_crlogic_probe.py after round 2 (r2_20261105/base%d/probe%d_run.py is its frozen copy).  Baseline: the fix" % (N, N),
         "(GXEMUL-SEC src/cpus/cpu_ppc_instr.c).  Every prediction below is EXACT and COMPUTED by r2_20261105/v575b.py (`pretable2'),",
         "whose 62-row re-derivation matches table 1's PRETABLE.out on all 17 legs (`check62').  Only the apparatus rows (ctl*, neg",
         "apparatus, *session, *mfcr, *disasm) are predicted green unconditionally; bit rows and `others' rows are computed.  Null media:",
         "/bin/true and /bin/false: CONTROL=FAIL; an absent binary: the probe raises before any row, no sentinel, CONTROL=none, DONE=0.",
         "", "ROW MANIFEST (session: seed; instructions as op BT,BA,BB; rows):"]
    for sess, seed, insns, rows in sessions(True):
        L.append("  %-16s seed=0x%08x  %s" % (sess, seed, "  ".join("%s %d,%d,%d" % i for i in insns) or "(apparatus)"))
        L.append("                   rows: " + ", ".join(r[0] for r in rows))
    L.append("  %d rows: %s" % (N, " | ".join(names(True))))
    L += ["", "VARIANTS (exact red sets on the %d rows; table 1's 15 first, then the round-2 closures):" % N]
    for name, (VV, edit) in SPEC.items():
        red = predict(VV, True)
        tag = "  [EQUIVALENT: proved; a 0-red run is the prediction]" if name == "g2_crandc_baread3" else ""
        L.append("   %-22s %2d red: %s%s" % (name, len(red), ",".join(red) or "none", tag))
    L += ["", "PREDICTED ONLY (not built; the pass-1 ruling R5 bt-substitutions):"]
    for name, VV in PREDICTED_ONLY.items():
        red = predict(VV, True)
        L.append("   %-22s %2d red: %s" % (name, len(red), ",".join(red) or "none"))
    return NL.join(L) + NL


def errata62():
    """The four R5 bt-substitution predictions on the OLD 62 rows (for PRETABLE.errata.md)."""
    L = []
    for name, VV in PREDICTED_ONLY.items():
        red = predict(VV, False)
        L.append("   %-22s %2d red: %s" % (name, len(red), ",".join(red) or "none"))
    return NL.join(L) + NL


if __name__ == "__main__":
    if sys.argv[1:] == ["check62"]:
        sys.exit(0 if check62() else 1)
    elif sys.argv[1:] == ["closure"]:
        text, undetected = closure()
        io.open(os.path.join(HERE, "CLOSURE.md"), "w", encoding="utf-8", newline="\n").write(text)
        print(text)
        print("UNDETECTED by 66: %d" % len(undetected))
    elif sys.argv[1:] == ["pretable2"]:
        sys.stdout.write(pretable2())
    elif sys.argv[1:] == ["errata62"]:
        sys.stdout.write(errata62())
    elif sys.argv[1:] == ["write"]:
        write()
    elif sys.argv[1:] == ["names"]:
        print(" ".join('"%s"' % n for n in names(True)))
        print(len(names(True)))
    else:
        sys.exit(__doc__)
