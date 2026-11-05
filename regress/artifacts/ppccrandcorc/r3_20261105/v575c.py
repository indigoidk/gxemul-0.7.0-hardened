#!/usr/bin/env python3
"""v575c.py -- #575 ppccrandcorc ROUND 3 (2026-11-05): r2_20261105/v575b.py extended over the FULL single-constant space at the
sites round 2 had put in scope with a narrower vocabulary (pass 3, codex B1-B4), plus the 16 structural cells of its denominator.

The simulator copies the probe's session plans (regress/ppc_crlogic_probe.py: table(), the edge session, the two `hi' rows, the
four round-2 pin rows and the four round-3 whole-CR rows) and executes X(crandc)/X(crorc) (src/cpus/cpu_ppc_instr.c:2729-2737,
2756-2764) statement by statement under a SINGLE-EDIT VARIANT dict:

    mbt/mba/mbb = m     the field mask `& 31' at BT/BA/BB replaced by `& m', m in 0..30 (one site at a time)
    ba_src = BB|BT      the BA read `(cr >> (31-ba))' takes another field's index; bb_src = BA|BT likewise (at the BB read the
                        variable `ba' ALREADY holds the Boolean value, so bb_src=BA reads CR[a], a in {0,1})
    rma/rmb = m         the read mask `& 1' replaced by `& m' at the BA/BB read, ANY 32-bit m (round 2: 3 and 7 only; round 3:
                        1 + 2^k for k = 1..31, and 0, 2, 4, 6 -- the C conditions keep their semantics on the int values)
    clear = early|mid|none|xor   the clear moved before both reads | between the reads | deleted | replaced by a toggle
    clr_idx = ba|bb|rbt the clear's `(31-bt)' replaced by `(31-ba)', `(31-bb)' (ba, bb hold the READ VALUES there) or by `bt'
    set = none|xor      the set deleted | `|=' replaced by `^='
    set_idx = ba|bb|rbt the set's `(31-bt)' replaced likewise
    set_lit = C         the set's literal `1' replaced by the unsigned constant C: cr |= (C << (31-bt)), truncated to 32 bits
    clr_lit = C         (OUTSIDE the denominator, reported for information) the clear's literal `1' replaced likewise
    swap                the two read statements exchanged
    cond = f(a, b, bt)  a condition edit (table 1's b, d1-d6; the pass-1 ruling's four R5 bt-substitutions)
    identity            the whole body removed (table 1's c, per handler or both)
    decode = op'        the dispatch case (cpu_ppc_instr.c:4638/4641) bound to another CR-logical handler

Only the apparatus rows (ctl*, neg apparatus, *session, *mfcr, *disasm) are predicted green unconditionally.  The bit rows,
the `others' rows and the round-3 whole-CR rows are computed.  `check66' re-derives table 2's 27 predictions on the 66 rows
and checks them against r2_20261105/PRETABLE_2.out, which is what licenses the extension.

  v575c.py check66 | closure3 | pretable3 | write | names | codex"""
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
CTL_CR = 0x12345678          # the probe's control-session seed (PRETABLE_2 printed a placeholder 0 here: pass 3, R6)


# ------------------------------------------------------------------------------------------------ the simulator
def crbit(cr, n):
    return (cr >> (31 - n)) & 1


def bitof(n):
    return 1 << (31 - n)


def setbit(cr, n, v):
    return (cr | bitof(n)) if v else (cr & ~bitof(n) & 0xFFFFFFFF)


def NOT(x):          # C `!x' on an int
    return 0 if x else 1


# C-exact conditions on ints a, b (any non-negative int once a read mask is widened) and the masked BT field index.
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
    clr_lit = V.get("clr_lit", 1)

    def idx(which, a_val, b_val):   # the index a `(31-x)' names at the clear/set: bt, or the READ VALUE held in ba/bb
        return {"bt": fbt, "ba": a_val, "bb": b_val}[which]

    def do_clear(cr, a_val, b_val):
        w = V.get("clr_idx", "bt")
        if w == "rbt":                                   # `~(1 << bt)': bit position bt = CR index 31-bt
            return cr & ~((clr_lit << fbt) & 0xFFFFFFFF) & 0xFFFFFFFF
        n = idx(w, a_val, b_val)
        if clr == "xor":
            return cr ^ bitof(n)
        return cr & ~((clr_lit << (31 - n)) & 0xFFFFFFFF) & 0xFFFFFFFF

    if clr == "early":
        cr = do_clear(cr, fba, fbb)
    read_a = lambda cr, a_val: (cr >> (31 - {"BA": fba, "BB": fbb, "BT": fbt}[V.get("ba_src", "BA")])) & V.get("rma", 1)
    read_b = lambda cr, a_val: (cr >> (31 - {"BB": fbb, "BA": a_val, "BT": fbt}[V.get("bb_src", "BB")])) & V.get("rmb", 1)
    if V.get("swap"):
        b = read_b(cr, fba)          # swapped: at the BB read `ba' still holds the field index
        a = read_a(cr, b)
    else:
        a = read_a(cr, fba)
        if clr == "mid":
            cr = do_clear(cr, a, fbb)
        b = read_b(cr, a)
    if clr in ("and", "xor"):
        cr = do_clear(cr, a, b)
    if V.get("cond", COND[op])(a, b, fbt):
        st = V.get("set", "or")
        w = V.get("set_idx", "bt")
        lit = V.get("set_lit", 1)
        if w == "rbt":
            m = (lit << fbt) & 0xFFFFFFFF
        else:
            m = (lit << (31 - idx(w, a, b))) & 0xFFFFFFFF
        if st == "or":
            cr |= m
        elif st == "xor":
            cr ^= m
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

# Round-3 whole-CR rows (single instruction each; the row compares the WHOLE CR, read through the register dump and mfcr,
# against the architectural CR).  want = the whole CR after the instruction.
PINS3 = [
    # name, op, bt, ba, bb, seed, want_cr, preset
    ("64 crorc baread", "crorc", 17, 31, 5, setbit(0xFFFFFFFF, 31, 0), setbit(setbit(0xFFFFFFFF, 31, 0), 17, 0), "inverse (1)"),
    ("64 crorc bbread", "crorc", 30, 30, 31, 0xFFFFFFFC, 0xFFFFFFFE, "inverse (0) = the BA source"),
    ("64 crandc setbits", "crandc", 31, 30, 31, setbit(0, 30, 1), setbit(setbit(0, 30, 1), 31, 1), "inverse (0)"),
    ("64 crorc setbits", "crorc", 31, 0, 31, 0, setbit(0, 31, 1), "inverse (0) = the BB source"),
]


def sessions(stage=70):
    """Yields (session, seed, insns, rows) in the probe's order; rows = [(name, kind, bt-or-mask, want)], kind in
    bit|others|cr|app (app = apparatus row, always green; cr = the whole CR compared).  stage = 62 (table 1's probe),
    66 (after round 2) or 70 (after round 3)."""
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
    yield ("ctl", CTL_CR, [], [(n, "app", 0, 0) for n in APPARATUS])
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
    if stage >= 66:
        for name, op, bt, ba, bb, seed, want, _ in PINS:
            yield (name, seed, [(op, bt, ba, bb)], [(name, "bit", bt, want)])
    if stage >= 70:
        for name, op, bt, ba, bb, seed, want, _ in PINS3:
            yield (name, seed, [(op, bt, ba, bb)], [(name, "cr", 0, want)])
    yield table("32", ["crandc", "crorc"])


def names(stage=70):
    return [r[0] for _, _, _, rows in sessions(stage) for r in rows]


def predict(VV, stage=70):
    """Red row names (spaces -> underscores, as SCORES.txt writes them) for the variant VV = {op: V}."""
    red = []
    for _, seed, insns, rows in sessions(stage):
        cr = run(seed, insns, VV)
        for name, kind, arg, want in rows:
            if kind == "app":
                continue
            if kind == "bit":
                got = crbit(cr, arg)
            elif kind == "others":
                got = cr & ~arg & 0xFFFFFFFF
            else:
                got = cr
            if got != want:
                red.append(name.replace(" ", "_"))
    return red


def both(V):
    return {"crandc": dict(V), "crorc": dict(V)}


# ------------------------------------------------------------------------------------------------ the enumeration
def kmask(k):
    return 1 | (1 << k)


def cells():
    """Every cell of the round-3 denominator: (cls, label, VV).  cls in mask|read|rmask|rmask3|clear|set|setlit|struct|cond|decode.
    The first 239 are round 2's (same labels, same order); then the round-3 extension."""
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
    # ---- round 3: the read-mask sites over 1+2^k (k = 2..31; k = 1 is &3 above) and {0, 2, 4, 6}
    for op in EDITED:
        for src, key in (("BA", "rma"), ("BB", "rmb")):
            for k in range(2, 32):
                yield ("rmask3", "%s %s read mask &0x%x (1|1<<%d)" % (op, src, kmask(k), k), {op: {key: kmask(k)}})
            for m in (0, 2, 4, 6):
                yield ("rmask3", "%s %s read mask &%d" % (op, src, m), {op: {key: m}})
    # ---- round 3: the set literal 1 -> 1+2^k (k = 1..31), unsigned
    for op in EDITED:
        for k in range(1, 32):
            yield ("setlit", "%s set literal 0x%08xu (1+2^%d)" % (op, kmask(k), k), {op: {"set_lit": kmask(k)}})
    # ---- round 3: the 16 structural cells
    for op in EDITED:
        yield ("struct", op + " clear (31-bt) -> (31-ba)", {op: {"clr_idx": "ba"}})
        yield ("struct", op + " clear (31-bt) -> (31-bb)", {op: {"clr_idx": "bb"}})
        yield ("struct", op + " set (31-bt) -> (31-ba)", {op: {"set_idx": "ba"}})
        yield ("struct", op + " set (31-bt) -> (31-bb)", {op: {"set_idx": "bb"}})
        yield ("struct", op + " clear (31-bt) -> bt", {op: {"clr_idx": "rbt"}})
        yield ("struct", op + " set (31-bt) -> bt", {op: {"set_idx": "rbt"}})
        yield ("struct", op + " clear moved between the reads", {op: {"clear": "mid"}})
        yield ("struct", op + " read statements swapped", {op: {"swap": True}})


def info_cells():
    """OUTSIDE the denominator, reported for information: the clear literal 1 -> 1+2^k (an extra CLEAR; the disclosed class)."""
    for op in EDITED:
        for k in range(1, 32):
            yield ("clrlit", "%s clear literal 0x%08xu (1+2^%d)" % (op, kmask(k), k), {op: {"clr_lit": kmask(k)}})


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


def equiv_why(label):
    if label.startswith("crandc BA read mask &") and label != "crandc BA read mask &0":
        m = label.split("&")[1].split()[0]
        if int(m, 0) & 1:
            return "`ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition"
    return {
        "crandc set |= -> ^=": "the clear at :2734 has just zeroed the bit, so ^= and |= set it alike",
        "crorc set |= -> ^=": "the clear at :2761 has just zeroed the bit, so ^= and |= set it alike",
        "crandc read statements swapped": "the two reads are independent of each other and of the clear (which follows both)",
        "crorc read statements swapped": "the two reads are independent of each other and of the clear (which follows both)",
    }.get(label)


# ------------------------------------------------------------------------------------------------ codex's pass-3 claims
def codex_survivors():
    """(family, label) of the 54 cells codex says survive the 66 rows."""
    out = []
    for k in range(2, 31):
        out.append(("B1", "crorc BB read mask &0x%x (1|1<<%d)" % (kmask(k), k)))
    out.append(("B2", "crorc BA read mask &0x%x (1|1<<%d)" % (kmask(15), 15)))
    for k in [7, 9] + list(range(11, 31)):
        out.append(("B3", "crandc set literal 0x%08xu (1+2^%d)" % (kmask(k), k)))
    for k in (26, 27):
        out.append(("B4", "crorc set literal 0x%08xu (1+2^%d)" % (kmask(k), k)))
    return out


def codex_equivalents():
    out = ["crandc BA read mask &3", "crandc BA read mask &7", "crandc set |= -> ^=", "crorc set |= -> ^="]
    out += ["crandc BA read mask &0x%x (1|1<<%d)" % (kmask(k), k) for k in range(2, 31)]
    out += ["crandc read statements swapped", "crorc read statements swapped"]
    return out


def closure3():
    cl = list(cells())
    byl = dict((label, VV) for _, label, VV in cl)
    per = {}
    for cls, _, _ in cl:
        per[cls] = per.get(cls, 0) + 1
    n62, n66, n70 = len(names(62)), len(names(66)), len(names(70))
    L = ["# #575 ppccrandcorc -- CLASS CLOSURE BY SIMULATION, ROUND 3 (2026-11-05)", "",
         "Simulator: r3_20261105/v575c.py (r2_20261105/v575b.py extended; `v575c.py check66' re-derives table 2's 27 predictions on",
         "the 66 rows and matches r2_20261105/PRETABLE_2.out exactly, which licenses the extension).  Handlers simulated statement by",
         "statement: src/cpus/cpu_ppc_instr.c X(crandc) :2729-2737 and X(crorc) :2756-2764; dispatch :4638 and :4641.", "",
         "WHAT PASS 3 FOUND (p3_20261105/codex_codex_r575_p3.txt).  Round 2's enumeration had put the read-mask sites (:2732-2733,",
         ":2759-2760) and the set statements (:2736, :2763) in scope with a vocabulary narrower than the class: read masks {& 3, & 7} only,",
         "the set edited only to `deleted' and `^='.  This round enumerates the FULL single-constant family at those sites that codex",
         "named (1+2^k at every read site and every set literal, {0,2,4,6} at every read site), adds k = 31 at the same sites (in bound:",
         "the same constant sites, one more constant), the 16 structural cells of codex's denominator, and then PROVES the rest of the",
         "2^32-constant space at each site by argument (section PROOF below), so the contract can name the whole site.", "",
         "ENUMERATION (one edit per cell, per handler): round 2's 239 cells unchanged (field mask m in 0..30 at BT, BA, BB; each source",
         "read taking another field's index; the read mask & 3 / & 7; the clear moved before the reads, deleted or toggled; the set",
         "deleted or ^=; the condition edits; the dispatch re-bindings; c) PLUS: the read mask `& 1' -> `& (1|1<<k)' for k = 2..31 and",
         "-> & 0, & 2, & 4, & 6 at each of the four read sites (34 x 4 = 136); the set literal `1' -> the unsigned constant 1+2^k,",
         "k = 1..31, in each handler (31 x 2 = 62); and 16 structural cells: the clear's and the set's `(31-bt)' -> `(31-ba)' / `(31-bb)'",
         "(ba, bb hold the READ VALUES there, so the edit addresses CR[a] / CR[b]) and -> `bt' (bit position bt = CR index 31-bt), the",
         "clear moved between the two reads, and the two read statements swapped (8 x 2 = 16).", ""]
    L.append("DENOMINATOR: %d cells = %s." % (len(cl), " + ".join("%d %s" % (n, c) for c, n in sorted(per.items()))))
    L.append("codex's denominator was 447: the same cells without k = 31 at the four read sites (4 cells) and at the two set literals")
    L.append("(2 cells).  Its partition (357 detected, 35 equivalent, 54 breaches, 1 disclosed) is checked cell by cell below.")
    L.append("")
    # ---- codex's survivors, one by one
    L += ["## CODEX'S 54 SURVIVORS, ONE BY ONE (red on the 66 rows = none means the survivor is CONFIRMED; red on %d = the round-3 rows)" % n70, "",
          "| # | family | cell | red on 66 | verdict | red on %d |" % n70, "|---|---|---|---|---|---|"]
    conf = ref = 0
    for i, (fam, label) in enumerate(codex_survivors(), 1):
        VV = byl[label]
        r66, r70 = predict(VV, 66), predict(VV, 70)
        v = "CONFIRMED (survives 66)" if not r66 else "REFUTED (already red on 66)"
        conf += not r66
        ref += bool(r66)
        L.append("| %d | %s | %s | %s | %s | %s |" % (i, fam, label, ",".join(r66) or "none", v, ",".join(r70) or "**none**"))
    L += ["", "codex's survivors: %d CONFIRMED, %d REFUTED." % (conf, ref), ""]
    # ---- codex's equivalents
    L += ["## CODEX'S 35 EQUIVALENTS, ONE BY ONE (`rand-equiv' = 40000 random (cr,BT,BA,BB) found no difference from the fix; the proof is the WHY)", "",
          "| # | cell | red on 66 | red on %d | rand-equiv | verdict | why |" % n70, "|---|---|---|---|---|---|---|"]
    econf = eref = 0
    for i, label in enumerate(codex_equivalents(), 1):
        VV = byl[label]
        r66, r70, eq = predict(VV, 66), predict(VV, 70), equivalent(VV)
        why = equiv_why(label)
        v = "CONFIRMED" if (eq and why and not r70) else "REFUTED"
        econf += v == "CONFIRMED"
        eref += v == "REFUTED"
        L.append("| %d | %s | %s | %s | %s | %s | %s |" % (i, label, ",".join(r66) or "none", ",".join(r70) or "none", eq, v, why or "-"))
    L += ["", "codex's equivalents: %d CONFIRMED, %d REFUTED.  One more equivalent cell is in this denominator and not in codex's:" % (econf, eref),
          "crandc BA read mask &0x80000001 (1|1<<31), by the same proof.", ""]
    # ---- the full cell -> row map
    L += ["## CELL -> ROW MAP (every cell of the %d; 62/66/%d = red rows of the probe at that stage)" % (len(cl), n70), "",
          "| class | cell | status | red on 62 | red on 66 | red on %d |" % n70, "|---|---|---|---|---|---|"]
    undetected, equiv, excl, closed3, closed2 = [], [], [], [], []
    for cls, label, VV in cl:
        r62, r66, r70 = predict(VV, 62), predict(VV, 66), predict(VV, 70)
        if r62:
            status = "DETECTED(62)"
        elif r66:
            status = "CLOSED by round 2"
            closed2.append(label)
        elif r70:
            status = "CLOSED by round 3: " + ",".join(r70)
            closed3.append(label)
        elif equiv_why(label):
            status = "EQUIVALENT" + (" rand-equiv" if equivalent(VV) else " **RANDOM DIFFERENCE FOUND**")
            equiv.append(label)
        elif label in EXCLUDED:
            status = "EXCLUDED (disclosed)"
            excl.append(label)
        else:
            status = "**UNDETECTED**"
            undetected.append(label)
        L.append("| %s | %s | %s | %s | %s | %s |" % (cls, label, status, ",".join(r62) or "none", ",".join(r66) or "none",
                                                     ",".join(r70) or "none"))
    L += ["", "CLOSED BY THE 4 ROUND-3 ROWS (%d cells; missed by the 66 rows):" % len(closed3)]
    for m in closed3:
        L.append("  - " + m)
    L += ["", "EQUIVALENT (%d cells; proved, and 40000 random trials found no difference):" % len(equiv)]
    for m in equiv:
        L.append("  - %s: %s" % (m, equiv_why(m)))
    L += ["", "EXCLUDED / DISCLOSED (%d cell):" % len(excl)]
    for m in excl:
        L.append("  - %s: %s" % (m, EXCLUDED[m]))
    L += ["", "STILL UNDETECTED BY THE %d ROWS (%d cells):" % (n70, len(undetected))]
    for m in undetected:
        L.append("  - " + m)
    # ---- the new rows
    L += ["", "## THE 4 ROUND-3 ROWS (single-instruction sessions shaped like the `hi'/pin rows; each compares the WHOLE CR, from the",
          "register dump and from mfcr r10, with the architectural CR)", ""]
    for name, op, bt, ba, bb, seed, want, preset in PINS3:
        L.append("  %-17s %s BT=%d BA=%d BB=%d seed=0x%08x want CR=0x%08x  CR[BT] pre-set %s" % (name, op, bt, ba, bb, seed, want, preset))
    L += ["",
          "  64 crorc baread   crorc 17,31,5 over 0xfffffffe: a = CR[31] = 0, b = CR[5] = 1 -> 0.  The BA read shifts by 0, so a = CR & m: every",
          "                    mask m with ANY bit 1..31 set reads nonzero and gives 1 (codex B2's & 0x8001 reads CR[16] = 1 here; the",
          "                    round-2 `64 crorc bamask' row has CR[16] = 0, its destination).  Also: every BA field mask 0..30 (CR[m] = 1),",
          "                    mask 16 included, which repairs R1.",
          "  64 crorc bbread   crorc 30,30,31 over 0xfffffffc: a = CR[30] = 0, b = CR[31] = 0 -> 1 at CR[30] (its own pre-set inverse 0 IS",
          "                    the a = 0 source).  The BB read shifts by 0: every mask m with any bit 2..31 set reads nonzero, !bb = 0, 0",
          "                    (B1, k = 2..31); bit 1 = CR[30] = 0 here, and `& 3' / `& 7' are red on `64 crorc 00' (its BB = 2 read is 2).",
          "  64 crandc setbits crandc 31,30,31 over 0x00000002: a = CR[30] = 1, b = CR[31] = 0 -> 1 at CR[31]; the set shifts by 0, so a",
          "                    literal 1+2^k also sets CR[31-k]: zero in the seed for k = 2..31 (B3 and k = 31); k = 1 lands on CR[30] = 1,",
          "                    the source, and is red on `64 crandc 01' (crandc 10,1,0 sets CR[9] after `crandc 9' cleared it).",
          "  64 crorc setbits  crorc 31,0,31 over 0: a = b = 0 -> 1 at CR[31]; every extra bit CR[31-k], k = 1..31, lands on a zero (B4).",
          "",
          "WHY FOUR AND NO FEWER (single-instruction sessions).  The four open families need, respectively: (i) crorc with a = 0, b = 1,",
          "result 0 and CR[16] = 1 (B2); (ii) crorc with a = 0, b = 0 (result 1) and CR[0..29] all 1 so that a BB read shifted by 0 has",
          "bits 2..31 set (B1); (iii) crandc with result 1 and zeros at CR[BT-k] for k = 7, 9, 11..31 (B3); (iv) crorc with result 1 and",
          "zeros at CR[BT-26], CR[BT-27] (B4).  (i) and (ii)/(iv) differ in the result; (ii) needs ones where (iv) needs zeros (the",
          "extra set bits of (iv) at BT-26, BT-27 lie in 0..5 for any BT, inside (ii)'s ones at 0..29, and moving BT below 27 shifts",
          "(iv)'s bits out); (iii) is crandc.  So no single instruction serves two families, and 4 rows is the minimum; a multi-",
          "instruction session would cost more rows (session/others/mfcr/disasm), as the edge session shows.  (The round-2 rows are",
          "kept as measured: they were not the minimum, see r2_20261105/CLOSURE.errata.md.)",
          "",
          "## PROOF: the whole 2^32 constant space at the six sites (what the contract may claim beyond the enumerated cells)",
          "",
          "A read is a = (cr >> (31-x)) & m with x the field index; call q = cr >> (31-x), whose bit j is CR[x-j] (j <= x, zero above).",
          "  crandc BA (:2732):  the condition `ba & !bb' is bitwise with !bb in {0,1}, so only bit 0 of a counts.  m with bit 0 set:",
          "                      EQUIVALENT (32 of them enumerated here).  m with bit 0 clear: a & 1 = 0, the result is always 0, red on",
          "                      `64 crandc 10' (want 1).  Closed for every m.",
          "  crandc BB (:2733):  `!bb' sees only bb != 0.  `64 crandc bbmask' (BB = 31, q = 0xfffffffe, want 1 needs bb = 0): any m with a",
          "                      bit in 1..31 reads nonzero -> red.  m = 0: bb = 0 always, crandc becomes CR[BA], red on `64 crandc 11'.",
          "                      Closed for every m != 1.",
          "  crorc BA (:2759):   `ba | !bb' sees only a != 0.  `64 crorc baread' (BA = 31, q = 0xfffffffe, want 0 needs a = 0): any m with",
          "                      a bit in 1..31 -> red.  m = 0: a = 0 always, crorc becomes !CR[BB], red on `64 crorc 11'.  Closed.",
          "  crorc BB (:2760):   `64 crorc bbread' (BB = 31, q = 0xfffffffc, want 1 needs bb = 0): any m with a bit in 2..31 -> red; m",
          "                      with bit 1: `64 crorc 00' (q = 2, want 1) -> red; m = 0: bb = 0 always, result always 1, red on",
          "                      `64 crorc 01'.  Closed.",
          "  set literal C (:2736, :2763): cr |= (C << (31-BT)).  C without bit 0: CR[BT] is never set, red on every result-1 row.  C with",
          "                      bit 0 and some other bit j: on the `setbits' rows (BT = 31) the extra bit lands on CR[31-j], a zero for",
          "                      j = 2..31 (crandc) and j = 1..31 (crorc), seen by the whole-CR compare; j = 1 at crandc is red on",
          "                      `64 crandc 01'.  Closed for every C != 1 (and C = 0 is `set deleted').",
          "  The field masks `& 31' (:2730-2731, :2757-2758) are closed over 0..30 by enumeration; a mask with bits above 4 is the fix",
          "  (the field is 5 bits), so the mask sites are closed over every constant too.",
          "",
          "## WHAT STAYS UNDETECTED, AND WHY",
          "",
          "  - the %d EQUIVALENT cells above (proved; no row can see them);" % len(equiv),
          "  - crandc clear -> toggle (^=): DISCLOSED in the probe's clause (e)(5) (every crandc row with result 0 pre-sets the inverse,",
          "    and the round-3 `64 crandc setbits' row pre-sets 0 with result 1: a toggle of 0 then |= gives 1 too);",
          "  - OUTSIDE the denominator (disclosed, (e)(5)): an extra CLEAR (clear literal 1+2^k).  The round-3 whole-CR rows see some of",
          "    them incidentally (appendix); the rest need ones at non-source, non-destination bits, which the set-literal rows cannot",
          "    carry.  Not claimed.",
          "",
          "## PROBE CONTRACT TEXT (clause (e), round 3)",
          "",
          "  ROUND 3 (regress/artifacts/ppccrandcorc/r3_20261105/CLOSURE3.md): the four whole-CR rows after the round-2 pins close the",
          "  single-constant space at the four read-mask sites and the two set literals.  COVERED: every read mask `& m' other than the",
          "  fix's at crandc BB, crorc BA and crorc BB (all 2^32 m, by the proof; 1+2^k for k = 1..31 and 0, 2, 4, 6 enumerated and",
          "  simulated), every crandc BA read mask with bit 0 clear; every set literal C != 1 in both handlers (1+2^k, k = 1..31,",
          "  enumerated); the clear/set addressing cells (31-bt) -> (31-ba), (31-bb), bt and the clear moved between the reads.",
          "  DELIBERATELY UNCOVERED: crandc BA read masks with bit 0 set (EQUIVALENT: `ba & !bb' sees only bit 0 of ba); `|=' -> `^='",
          "  at either set (EQUIVALENT after the clear); the read statements swapped (EQUIVALENT); the crandc toggle of (5); an extra",
          "  CLEAR of a non-source, non-destination bit (5).",
          "",
          "OLD rows: %d (table 1), %d (round 2).  NEW rows: %d (N = %d)." % (n62, n66, n70 - n66, n70)]
    # ---- appendix: the clear-literal class
    L += ["", "## APPENDIX (outside the denominator): the clear literal 1 -> 1+2^k, what the %d rows happen to see" % n70, "",
          "| cell | red on 66 | red on %d |" % n70, "|---|---|---|"]
    for _, label, VV in info_cells():
        L.append("| %s | %s | %s |" % (label, ",".join(predict(VV, 66)) or "none", ",".join(predict(VV, 70)) or "none"))
    return NL.join(L) + NL, undetected, (conf, ref, econf, eref)


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
    # ---- round 3
    body = HD(op) + RA + RB + CLR + LINE[op] + SET
    if kind == "setlit":
        return one(s, body, body.replace(SET, SET.replace("(1 << (31-bt))", "(%s << (31-bt))" % arg)))
    if kind == "clridx":           # arg: "ba" | "bb" | "rbt"
        new = "~(1 << bt)" if arg == "rbt" else "~(1 << (31-%s))" % arg
        return one(s, body, body.replace(CLR, CLR.replace("~(1 << (31-bt))", new)))
    if kind == "setidx":
        new = "(1 << bt)" if arg == "rbt" else "(1 << (31-%s))" % arg
        return one(s, body, body.replace(SET, SET.replace("(1 << (31-bt))", new)))
    if kind == "midclear":
        return one(s, HD(op) + RA + RB + CLR, HD(op) + RA + CLR + RB)
    if kind == "swap":
        return one(s, HD(op) + RA + RB, HD(op) + RB + RA)
    raise ValueError(kind)


def cond(op, idx):
    return COND_EDITS[op][idx][1]


def hx(v):
    return "0x%08xu" % v


SPEC = {   # name: (VV, C edit)  -- table 2's 27 first (same names, same edits), then the round-3 representatives
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
    "s1_crandc_bb_from_bt": ({"crandc": {"bb_src": "BT"}}, ("crandc", "bbreadbt", None)),
    "s2_crorc_bb_from_bt": ({"crorc": {"bb_src": "BT"}}, ("crorc", "bbreadbt", None)),
    "o1_crandc_earlyclear": ({"crandc": {"clear": "early"}}, ("crandc", "earlyclear", None)),
    "o2_crorc_earlyclear": ({"crorc": {"clear": "early"}}, ("crorc", "earlyclear", None)),
    "m5_crandc_bbmask29": ({"crandc": {"mbb": 29}}, ("crandc", "bbmask", "29")),
    "m6_crandc_bbmask27": ({"crandc": {"mbb": 27}}, ("crandc", "bbmask", "27")),
    "m7_crandc_bbmask23": ({"crandc": {"mbb": 23}}, ("crandc", "bbmask", "23")),
    "m8_crorc_bamask29": ({"crorc": {"mba": 29}}, ("crorc", "bamask", "29")),
    "m9_crorc_bbmask29": ({"crorc": {"mbb": 29}}, ("crorc", "bbmask", "29")),
    "m10_crandc_bbmask17": ({"crandc": {"mbb": 17}}, ("crandc", "bbmask", "17")),
    "g1_crandc_bbread3": ({"crandc": {"rmb": 3}}, ("crandc", "bbread", "3")),
    "g2_crandc_baread3": ({"crandc": {"rma": 3}}, ("crandc", "baread", "3")),
    # ---- round 3: codex B1 (crorc BB read mask 1|1<<k) at k = 2, 15, 30 and the in-bound k = 31
    "r1_crorc_bbread_k2": ({"crorc": {"rmb": kmask(2)}}, ("crorc", "bbread", "0x5")),
    "r2_crorc_bbread_k15": ({"crorc": {"rmb": kmask(15)}}, ("crorc", "bbread", "0x8001")),
    "r3_crorc_bbread_k30": ({"crorc": {"rmb": kmask(30)}}, ("crorc", "bbread", "0x40000001")),
    "r4_crorc_bbread_k31": ({"crorc": {"rmb": kmask(31)}}, ("crorc", "bbread", "0x80000001u")),
    # ---- codex B2 (crorc BA read mask & 0x8001)
    "r5_crorc_baread_k15": ({"crorc": {"rma": kmask(15)}}, ("crorc", "baread", "0x8001")),
    # ---- codex B3 (crandc set literal 1+2^k): smallest 7, middle 19, largest 30; the in-bound k = 31
    "x1_crandc_setlit_k7": ({"crandc": {"set_lit": kmask(7)}}, ("crandc", "setlit", hx(kmask(7)))),
    "x2_crandc_setlit_k19": ({"crandc": {"set_lit": kmask(19)}}, ("crandc", "setlit", hx(kmask(19)))),
    "x3_crandc_setlit_k30": ({"crandc": {"set_lit": kmask(30)}}, ("crandc", "setlit", hx(kmask(30)))),
    "x4_crandc_setlit_k31": ({"crandc": {"set_lit": kmask(31)}}, ("crandc", "setlit", hx(kmask(31)))),
    # ---- codex B4 (crorc set literal) k = 26, 27
    "x5_crorc_setlit_k26": ({"crorc": {"set_lit": kmask(26)}}, ("crorc", "setlit", hx(kmask(26)))),
    "x6_crorc_setlit_k27": ({"crorc": {"set_lit": kmask(27)}}, ("crorc", "setlit", hx(kmask(27)))),
    # ---- the {0, 2, 4, 6} read masks, one each, spread over the four sites
    "z0_crorc_bbread0": ({"crorc": {"rmb": 0}}, ("crorc", "bbread", "0")),
    "z2_crandc_bbread2": ({"crandc": {"rmb": 2}}, ("crandc", "bbread", "2")),
    "z4_crorc_baread4": ({"crorc": {"rma": 4}}, ("crorc", "baread", "4")),
    "z6_crandc_baread6": ({"crandc": {"rma": 6}}, ("crandc", "baread", "6")),
    # ---- the structural cells, one representative per non-equivalent family (and the swap, predicted EQUIVALENT)
    "u1_crandc_clear_ba": ({"crandc": {"clr_idx": "ba"}}, ("crandc", "clridx", "ba")),
    "u2_crorc_clear_bb": ({"crorc": {"clr_idx": "bb"}}, ("crorc", "clridx", "bb")),
    "u3_crandc_set_bb": ({"crandc": {"set_idx": "bb"}}, ("crandc", "setidx", "bb")),
    "u4_crorc_set_ba": ({"crorc": {"set_idx": "ba"}}, ("crorc", "setidx", "ba")),
    "u5_crandc_clear_rbt": ({"crandc": {"clr_idx": "rbt"}}, ("crandc", "clridx", "rbt")),
    "u6_crorc_set_rbt": ({"crorc": {"set_idx": "rbt"}}, ("crorc", "setidx", "rbt")),
    "u7_crandc_midclear": ({"crandc": {"clear": "mid"}}, ("crandc", "midclear", None)),
    "u8_crorc_midclear": ({"crorc": {"clear": "mid"}}, ("crorc", "midclear", None)),
    "u9_crorc_swap": ({"crorc": {"swap": True}}, ("crorc", "swap", None)),
}
EQUIV_VARIANTS = ("g2_crandc_baread3", "u9_crorc_swap")
PREDICTED_ONLY = {   # the pass-1 ruling's R5 bt-substitutions: predicted, not built
    "r5a_crandc_bt_and_nbb": {"crandc": {"cond": cond("crandc", 4)}},
    "r5b_crandc_ba_and_nbt": {"crandc": {"cond": cond("crandc", 5)}},
    "r5c_crorc_bt_or_nbb": {"crorc": {"cond": cond("crorc", 4)}},
    "r5d_crorc_ba_or_nbt": {"crorc": {"cond": cond("crorc", 5)}},
}
TABLE2_NAMES = list(SPEC)[:29]


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


def check66():
    """Re-derive table 2's 27 predictions (and base/HEAD) on the 66 rows and compare with r2_20261105/PRETABLE_2.out."""
    want = {}
    for line in io.open(os.path.join(A, "r2_20261105", "PRETABLE_2.out"), encoding="latin-1"):
        parts = line.split()
        if len(parts) >= 3 and parts[0] in SPEC and parts[2] == "red:":
            want[parts[0]] = [] if parts[3] == "none" else parts[3].split(",")
    bad = 0
    for name in TABLE2_NAMES:
        got = predict(SPEC[name][0], 66)
        ok = got == want.get(name)
        bad += not ok
        print("%-22s %s %2d red" % (name, "OK  " if ok else "DIFF", len(got)))
    print("check66: %d of %d match PRETABLE_2.out; rows = %d (66), %d (70)" % (len(TABLE2_NAMES) - bad, len(TABLE2_NAMES),
                                                                               len(names(66)), len(names(70))))
    return bad == 0


def pretable3():
    N = len(names(70))
    L = ["PRETABLE_3 -- #575 ppccrandcorc, test-variant table 3 (%d rows).  Written BEFORE table 3 runs.  Instrument: the in-tree" % N,
         "probe regress/ppc_crlogic_probe.py after round 3 (r3_20261105/base%d/probe%d_run.py is its frozen copy).  Baseline: the fix" % (N, N),
         "(GXEMUL-SEC src/cpus/cpu_ppc_instr.c).  Every prediction below is EXACT and COMPUTED by r3_20261105/v575c.py (`pretable3'),",
         "whose 66-row re-derivation matches table 2's PRETABLE_2.out on all 29 legs (`check66').  Only the apparatus rows (ctl*, neg",
         "apparatus, *session, *mfcr, *disasm) are predicted green unconditionally; bit rows, `others' rows and the four round-3 whole-CR",
         "rows are computed.  Null media: /bin/true and /bin/false: CONTROL=FAIL; an absent binary: the probe raises before any row, no",
         "sentinel, CONTROL=none, DONE=0.  The control session's seed below is the probe's REAL CTL_CR (PRETABLE_2 printed 0: pass 3, R6).",
         "", "ROW MANIFEST (session: seed; instructions as op BT,BA,BB; rows):"]
    for sess, seed, insns, rows in sessions(70):
        L.append("  %-17s seed=0x%08x  %s" % (sess, seed, "  ".join("%s %d,%d,%d" % i for i in insns) or "(apparatus)"))
        L.append("                    rows: " + ", ".join(r[0] for r in rows))
    L.append("  %d rows: %s" % (N, " | ".join(names(70))))
    L += ["", "VARIANTS (exact red sets on the %d rows; table 2's 27 first, then the round-3 representatives):" % N]
    for name, (VV, edit) in SPEC.items():
        red = predict(VV, 70)
        tag = "  [EQUIVALENT: proved; a 0-red run is the prediction]" if name in EQUIV_VARIANTS else ""
        L.append("   %-22s %2d red: %s%s" % (name, len(red), ",".join(red) or "none", tag))
    L += ["", "PREDICTED ONLY (not built; the pass-1 ruling R5 bt-substitutions):"]
    for name, VV in PREDICTED_ONLY.items():
        red = predict(VV, 70)
        L.append("   %-22s %2d red: %s" % (name, len(red), ",".join(red) or "none"))
    return NL.join(L) + NL


if __name__ == "__main__":
    if sys.argv[1:] == ["check66"]:
        sys.exit(0 if check66() else 1)
    elif sys.argv[1:] == ["closure3"]:
        text, undetected, (c, r, ec, er) = closure3()
        io.open(os.path.join(HERE, "CLOSURE3.md"), "w", encoding="utf-8", newline="\n").write(text)
        print("CLOSURE3.md written: codex survivors %d confirmed / %d refuted; equivalents %d confirmed / %d refuted; "
              "UNDETECTED by 70: %d %s" % (c, r, ec, er, len(undetected), undetected))
    elif sys.argv[1:] == ["pretable3"]:
        sys.stdout.write(pretable3())
    elif sys.argv[1:] == ["write"]:
        write()
    elif sys.argv[1:] == ["names"]:
        print(" ".join('"%s"' % n for n in names(70)))
        print(len(names(70)))
    elif sys.argv[1:] == ["codex"]:
        for fam, label in codex_survivors():
            VV = dict((label2, VV2) for _, label2, VV2 in cells())[label]
            print("%s %-45s 66:%-4s 70:%s" % (fam, label, ",".join(predict(VV, 66)) or "none", ",".join(predict(VV, 70)) or "NONE"))
    else:
        sys.exit(__doc__)
