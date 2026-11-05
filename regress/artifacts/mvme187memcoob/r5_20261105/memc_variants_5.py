#!/usr/bin/env python3
"""memc_variants_5.py -- test-variant TABLE 5 for the mvme187memcoob detector (repair 5: 206 rows), 2026-11-05, as ruled by the
repair-pass-4 consolidated ruling (p4_20261105/CONS_MYTHOS_local.md, section 3 "the closed enumeration", section 4 "order of work"):
table 4's 112 variants (r4_20261105/memc_variants_4.py, re-applied to the CURRENT fix, src/devices/dev_mvme187.c, which repair 5 did
not change) plus ONE variant per cell of the class L that is not already among them -- the "L-walking" script the ruling's D4 asks for.
Baseline: GXEMUL-SEC/src/devices/dev_mvme187.c (== det_20261104/dev_mvme187.c.fix2).  Instrument: table5/probe206_frozen.py.
  memc_variants_5.py list | apply <name> <in> <out> | pretable | predmap | check4 | stats | cells
Exact-string edits, each asserted once (MUTANT-TEXT-NOT-FOUND otherwise); every backslash is chr(92).

THE CLASS L (section 3).  One inserted statement `if (G) T op V;` at a position P, or one gate added to an existing latch set, latch
test or notice predicate:
  positions P: H (head: after the fold, before the switch), CI (chipid arm), CR (chiprev arm), MT (memconf arm top, after the field
    read), MW (memconf write block, before the latch test), MB (memconf latch body, after the set), ME (memconf arm end, after the
    write block -- the memconf twin of DA, added here; the ruling lists ten positions, this script walks eleven), DT (default arm
    before the test), DB (default latch body, after the set), DA (default arm after the test block), TL (tail, after the switch);
  latch targets T: M = warned_memconf, D = warned_default; ops: = 1 (set), = 0 (clr), = idata (idat), ^= 1 (xor1), ^= idata (xori);
  keep targets F: chipid, chiprev, memconf; ops: = (asg), |= (or), ^= (xor), &= (and) idata;
  gates G: every conjunction of literals over the four tests the function makes -- W/nW (direction), C/nC (controller), M/nM, D/nD
    -- 3^4 = 81 including `any` (always); single idata-bit tests ib<b>s / ib<b>c (bit b set / clear, b = 0..31; not at CI/CR where
    the ruling places none -- they are walked there too, as a superset); single offset-bit tests ob<m>s / ob<m>c (m = 0..7, at the
    default-arm positions, H and TL only: the served arms' offsets are constants).
  gated existing statements: GS_<T>_<G> (the latch SET at :116 / :135 gated: `if (G) d->warned_x = 1;` -- family A); TA_<T>_<G> /
    TO_<T>_<G> (the latch TEST at :112 / :127 made `!x && (G)` / `!x || (G)` -- the whole-notice gate and the re-announce form, the
    shapes of M_B1, G_6, D6, T2_mlatch_ctl1, N1, M_B5); NV_<G> / ND_<G> (the write notice's value guard at :132 and direction
    ternary at :129 made `writeflag == MEM_WRITE && (G)` -- A_B7, G_1, M_B1_v, M_B2).
Disjunctions over the four tests, two-bit masks, a bit jointly with another predicate, len, and multi-bit value gates are OUTSIDE
(disclosed by the ruling), not walked.

HOW EACH CELL IS PREDICTED.  The probe itself is executed (table5/probe206_frozen.py, falling back to the in-tree probe) with
subprocess.run replaced by a fake gxemul: the fake decodes the probe's m88k words (ld.bu, ld.hu, ld, st.b, st) and runs them against a
model of DEVICE_ACCESS(mvme187_memc) as written in the fix, with the cell's statement inserted at its position -- so the wants, row
names and row logic are the probe's own, and the prediction is the probe's verdict on the modelled device.  The same fake models the
HEAD leg (the pre-fix exits and indexed read), B1/B2 (the exits reinstated) and the three null media; `check4` replays table 4's
instrument (r4_20261105/table4/probe148_frozen.py) against the same model for every table-4 variant the model expresses and compares
with table 4's MEASURED red sets (table4/SCORES.txt) -- the model's calibration.

WHICH CELLS ARE BUILT.  Every cell is walked and classified:
  VACUOUS   -- semantically a no-op at its position (gate unsatisfiable there, e.g. `M` inside the memconf latch body before the
               set; or the statement cannot change the state, e.g. `M = 1` after the set, `F |= idata` under a read-only gate):
               not a mutant, not built, counted.
  EQUIV     -- same statement at the same position as a built cell and the same DEVIATION SET on the probe (the gate selects the
               same probe accesses): the compiled code would execute identically on every probe session, so the built representative
               measures it; listed under its representative.
  BUILT     -- one representative per (shape, position, target, op, deviation set): exact red set predicted.
  A built cell whose predicted red set is EMPTY is a predicted SURVIVOR; it is classified PROBE-EQUIVALENT when the statement fires on
  the probe but leaves every observable unchanged (the ruling's disclosed `^= idata` into a set latch), else UNFIRED/SURVIVOR.
"""
import importlib.util
import io
import itertools
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
MD = os.path.dirname(HERE)
REGRESS = os.path.dirname(os.path.dirname(MD))
T, NL, BS = chr(9), chr(10), chr(92)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


v4 = load("mv4", os.path.join(MD, "r4_20261105", "memc_variants_4.py"))
OLD = list(v4.V)                      # table 4's 112 (name, edits)
OLD_NAMES = [n for n, _ in OLD]
assert len(OLD) == 112, len(OLD)

PROBE206 = os.path.join(HERE, "table5", "probe206_frozen.py")
PROBE206_INTREE = os.path.join(REGRESS, "mvme187_memc_probe.py")
PROBE148 = os.path.join(MD, "r4_20261105", "table4", "probe148_frozen.py")
SCORES4 = os.path.join(MD, "r4_20261105", "table4", "SCORES.txt")
REWANTED = ["R5_lines", "R5_pc", "R7_pc", "R9_lines", "R9_pc", "R12_pc", "R13_lines", "R13_pc", "R15_lines", "R15_pc"]

# ----------------------------------------------------------------------------------------------------------------- anchors
# Exact text of the current fix (src/devices/dev_mvme187.c); each must occur exactly once.
SWITCH = T + "switch (relative_addr) {" + NL                                          # H: before
CHIPID = T * 2 + "odata = d->memcreg.memc_chipid;" + NL                               # CI: after
CHIPREV = T * 2 + "odata = d->memcreg.memc_chiprev;" + NL                             # CR: after
CNF_RD = T * 2 + "odata = d->memcreg.memc_memconf;" + NL                              # MT: after
CNF_W = T * 2 + "if (writeflag == MEM_WRITE) {" + NL                                  # MW: after
LATCH_M = T * 3 + "if (!d->warned_memconf) {" + NL                                    # TA/TO M
SET_M = T * 4 + "d->warned_memconf = 1;" + NL                                         # MB: after; GS M
CASE08_END = T * 3 + "}" + NL + T * 2 + "}" + NL + T * 2 + "break;" + NL + NL + T + "default:" + NL   # ME
LATCH_D = T * 2 + "if (!d->warned_default) {" + NL                                    # DT: before; TA/TO D
DDIR = T * 3 + '    " (controller %i)", writeflag == MEM_WRITE ?' + NL                # ND
DGUARD = T * 3 + "if (writeflag == MEM_WRITE)" + NL + T * 4 + 'fatal(": 0x%x", (int)idata);' + NL   # NV
SET_D = T * 3 + "d->warned_default = 1;" + NL                                         # DB: after; GS D
DEND = SET_D + T * 2 + "}" + NL + T * 2 + "break;" + NL                               # DA
TAILRD = T + "if (writeflag == MEM_READ)" + NL + T * 2 + "memory_writemax64(cpu, data, len, odata);" + NL   # TL: before

POSITIONS = ["H", "CI", "CR", "MT", "MW", "MB", "ME", "DT", "DB", "DA", "TL"]
INDENT = {"H": 1, "CI": 2, "CR": 2, "MT": 2, "MW": 3, "MB": 4, "ME": 2, "DT": 2, "DB": 3, "DA": 2, "TL": 1}
IB_POS = ["H", "CI", "CR", "MT", "MW", "MB", "ME", "DT", "DB", "DA", "TL"]           # idata-bit gates walked here
OB_POS = ["H", "DT", "DB", "DA", "TL"]                                                # offset-bit gates walked here


def insert_edit(P, stmt):
    """The exact-string edit placing `stmt` (one line, no indent) at position P."""
    line = T * INDENT[P] + stmt + NL
    if P == "H":
        return [(SWITCH, line + SWITCH)]
    if P == "CI":
        return [(CHIPID, CHIPID + line)]
    if P == "CR":
        return [(CHIPREV, CHIPREV + line)]
    if P == "MT":
        return [(CNF_RD, CNF_RD + line)]
    if P == "MW":
        return [(CNF_W, CNF_W + line)]
    if P == "MB":
        return [(SET_M, SET_M + line)]
    if P == "ME":
        return [(CASE08_END, T * 3 + "}" + NL + T * 2 + "}" + NL + line + T * 2 + "break;" + NL + NL + T + "default:" + NL)]
    if P == "DT":
        return [(LATCH_D, line + LATCH_D)]
    if P == "DB":
        return [(SET_D, SET_D + line)]
    if P == "DA":
        return [(DEND, SET_D + T * 2 + "}" + NL + line + T * 2 + "break;" + NL)]
    if P == "TL":
        return [(TAILRD, line + TAILRD)]
    raise ValueError(P)


# ------------------------------------------------------------------------------------------------------------------- gates
LITS = ["W", "nW", "C", "nC", "M", "nM", "D", "nD"]
LIT_C = {"W": "writeflag == MEM_WRITE", "nW": "writeflag != MEM_WRITE", "C": "controller", "nC": "!controller",
         "M": "d->warned_memconf", "nM": "!d->warned_memconf", "D": "d->warned_default", "nD": "!d->warned_default"}


def conj_gates():
    out = [("any",)]
    for choice in itertools.product((None, 0, 1), repeat=4):
        lits = []
        for var, c in zip("WCMD", choice):
            if c is None:
                continue
            lits.append(var if c else "n" + var)
        if lits:
            out.append(("c", tuple(lits)))
    return out


CONJ = conj_gates()
assert len(CONJ) == 81
IB = [("ib", b, pol) for b in range(32) for pol in (1, 0)]
OB = [("ob", m, pol) for m in range(8) for pol in (1, 0)]


def gate_name(g):
    if g[0] == "any":
        return "any"
    if g[0] == "c":
        return ".".join(g[1])
    if g[0] == "ib":
        return "ib%d%s" % (g[1], "s" if g[2] else "c")
    if g[0] == "ob":
        return "ob%d%s" % (g[1], "s" if g[2] else "c")
    if g[0] == "never":
        return "never"
    raise ValueError(g)


def gate_c(g):
    """C text of the gate, or None for `any`."""
    if g[0] == "any":
        return None
    if g[0] == "c":
        return " && ".join(LIT_C[l] for l in g[1])
    if g[0] == "ib":
        m = "(idata & 0x%xULL)" % (1 << g[1])
        return m if g[2] else "!" + m
    if g[0] == "ob":
        m = "(relative_addr & 0x%02x)" % (1 << g[1])
        return m if g[2] else "!" + m
    if g[0] == "never":
        return "0"
    raise ValueError(g)


def gate_eval(g, W, C, M, D, idata, rel):
    if g[0] == "any":
        return True
    if g[0] == "never":
        return False
    if g[0] == "c":
        for l in g[1]:
            v = {"W": W, "C": C, "M": bool(M), "D": bool(D)}[l[-1]]
            if l.startswith("n"):
                v = not v
            if not v:
                return False
        return True
    if g[0] == "ib":
        return bool((idata >> g[1]) & 1) == bool(g[2])
    if g[0] == "ob":
        return bool((rel >> g[1]) & 1) == bool(g[2])
    raise ValueError(g)


def gate_rank(g):
    """Representative preference: any, one literal, a bit, then longer conjunctions."""
    if g[0] == "any":
        return (0, "")
    if g[0] == "c":
        return (len(g[1]), gate_name(g))
    return (1, gate_name(g))


# ------------------------------------------------------------------------------------------------------------------- cells
LOPS = {"set": "= 1", "clr": "= 0", "idat": "= idata", "xor1": "^= 1", "xori": "^= idata"}
KOPS = {"asg": "=", "or": "|=", "xor": "^=", "and": "&="}
LATCH = {"M": "warned_memconf", "D": "warned_default"}
FIELDS = ["chipid", "chiprev", "memconf"]


class Cell(object):
    """shape L (latch statement), K (keep statement), GS (gated set), TA/TO (gated test), NV/ND (gated notice predicate)."""
    __slots__ = ("shape", "P", "T", "op", "g")

    def __init__(self, shape, P, T, op, g):
        self.shape, self.P, self.T, self.op, self.g = shape, P, T, op, g

    def key(self):
        return (self.shape, self.P, self.T, self.op, gate_name(self.g))

    def name(self):
        if self.shape in ("L", "K"):
            return "%s_%s_%s_%s_%s" % (self.shape, self.P, self.T, self.op, gate_name(self.g))
        if self.shape in ("GS", "TA", "TO"):
            return "%s_%s_%s" % (self.shape, self.T, gate_name(self.g))
        return "%s_%s" % (self.shape, gate_name(self.g))

    def stmt(self):
        if self.shape == "L":
            s = "d->%s %s;" % (LATCH[self.T], LOPS[self.op])
        else:
            s = "d->memcreg.memc_%s %s idata;" % (self.T, KOPS[self.op])
        gc = gate_c(self.g)
        return s if gc is None else "if (%s) %s" % (gc, s)

    def edits(self):
        gc = gate_c(self.g)
        if self.shape in ("L", "K"):
            return insert_edit(self.P, self.stmt())
        if self.shape == "GS":
            anchor = SET_M if self.T == "M" else SET_D
            ind = 4 if self.T == "M" else 3
            return [(anchor, T * ind + "if (%s) d->%s = 1;" % (gc, LATCH[self.T]) + NL)]
        if self.shape in ("TA", "TO"):
            anchor = LATCH_M if self.T == "M" else LATCH_D
            ind = 3 if self.T == "M" else 2
            return [(anchor, T * ind + "if (!d->%s %s (%s)) {" % (LATCH[self.T], "&&" if self.shape == "TA" else "||", gc) + NL)]
        if self.shape == "NV":
            return [(DGUARD, DGUARD.replace("if (writeflag == MEM_WRITE)", "if (writeflag == MEM_WRITE && (%s))" % gc))]
        if self.shape == "ND":
            return [(DDIR, DDIR.replace("writeflag == MEM_WRITE ?", "writeflag == MEM_WRITE && (%s) ?" % gc))]
        raise ValueError(self.shape)

    def what(self):
        if self.shape == "L":
            return "%s at %s: %s" % ({"M": "memconf latch", "D": "default latch"}[self.T], self.P, self.stmt())
        if self.shape == "K":
            return "keep into %s at %s: %s" % (self.T, self.P, self.stmt())
        if self.shape == "GS":
            return "the %s latch SET gated: if (%s)" % (self.T, gate_c(self.g))
        if self.shape == "TA":
            return "the %s latch TEST gated: !%s && (%s)" % (self.T, LATCH[self.T], gate_c(self.g))
        if self.shape == "TO":
            return "the %s notice re-announced: !%s || (%s)" % (self.T, LATCH[self.T], gate_c(self.g))
        if self.shape == "NV":
            return "the write notice's value guard gated: && (%s)" % gate_c(self.g)
        return "the notice's direction gated: writeflag == MEM_WRITE && (%s)" % gate_c(self.g)


def gate_from_name(s):
    if s == "any":
        return ("any",)
    if s == "never":
        return ("never",)
    if s[:2] in ("ib", "ob") and s[2:-1].isdigit() and s[-1] in "sc":
        return (s[:2], int(s[2:-1]), 1 if s[-1] == "s" else 0)
    lits = tuple(s.split("."))
    assert all(l in LITS for l in lits), s
    return ("c", lits)


def cell_from_name(name):
    """The inverse of Cell.name(): `apply` needs no walk."""
    p = name.split("_")
    if p[0] in ("L", "K"):
        assert len(p) == 5 and p[1] in POSITIONS, name
        if p[0] == "L":
            assert p[2] in LATCH and p[3] in LOPS, name
        else:
            assert p[2] in FIELDS and p[3] in KOPS, name
        return Cell(p[0], p[1], p[2], p[3], gate_from_name(p[4]))
    if p[0] in ("GS", "TA", "TO"):
        assert len(p) == 3 and p[1] in LATCH, name
        return Cell(p[0], None, p[1], None, gate_from_name(p[2]))
    if p[0] in ("NV", "ND"):
        assert len(p) == 2, name
        return Cell(p[0], None, None, None, gate_from_name(p[1]))
    raise KeyError(name)


def all_cells():
    cells = []
    for P in POSITIONS:
        gates = list(CONJ) + (IB if P in IB_POS else []) + (OB if P in OB_POS else [])
        for g in gates:
            for Tt in ("M", "D"):
                for op in LOPS:
                    cells.append(Cell("L", P, Tt, op, g))
            for F in FIELDS:
                for op in KOPS:
                    cells.append(Cell("K", P, F, op, g))
    for Tt in ("M", "D"):
        gates = [g for g in CONJ if g[0] != "any"] + IB + (OB if Tt == "D" else [])
        for g in gates:
            cells.append(Cell("GS", None, Tt, None, g))
            cells.append(Cell("TA", None, Tt, None, g))
            cells.append(Cell("TO", None, Tt, None, g))
    for shape in ("NV", "ND"):
        for g in [g for g in CONJ if g[0] != "any" and not any(l in ("W", "nW") for l in g[1])] + IB + OB:
            cells.append(Cell(shape, None, None, None, g))
    return cells


# --------------------------------------------------------------------------------------------------------- the device model
MASK = {1: 0xff, 2: 0xffff, 4: 0xffffffff}
HEADCNF = "mvme187_memc: Write to relative_addr %i (controller %i) not yet implemented!" + NL
MNOTE = "[ mvme187_memc: memconf write 0x%x (controller %i) ignored, not modelled (once) ]" + NL


class Exit(Exception):
    pass


class Device(object):
    """DEVICE_ACCESS(mvme187_memc) as written in the fix, with one variant applied.
    variant: dict(cell=Cell or None, exit_mw=bool (B1 / HEAD), exit_def=bool (B2 / HEAD), head=bool)."""

    def __init__(self, variant):
        self.v = variant
        self.cell = variant.get("cell")
        self.M = 0
        self.D = 0
        self.f = {"chipid": 0x80, "chiprev": 1, "memconf": 3}
        self.out = []          # transcript pieces (notices)
        self.devs = []         # deviation set: access indices where the variant's path differs from the fix's
        self.changed = False   # some deviation changed the state (latch truthiness, a field) or the notice text
        self.n = 0

    def _env(self, W, C, idata, rel):
        return (W, C, bool(self.M), bool(self.D), idata, rel)

    def _fire(self, env):
        return gate_eval(self.cell.g, *env)

    def hook(self, P, env):
        c = self.cell
        if c is None or c.shape not in ("L", "K") or c.P != P:
            return
        if not self._fire(env):
            return
        self.devs.append(self.n)
        idata = env[4]
        if c.shape == "L":
            cur = self.M if c.T == "M" else self.D
            was = bool(cur)
            if c.op == "set":
                cur = 1
            elif c.op == "clr":
                cur = 0
            elif c.op == "idat":
                cur = idata & 0xffffffff
            elif c.op == "xor1":
                cur = (cur ^ 1) & 0xffffffff
            else:
                cur = (cur ^ idata) & 0xffffffff
            if bool(cur) != was:
                self.changed = True
            if c.T == "M":
                self.M = cur
            else:
                self.D = cur
        else:
            b = idata & 0xff
            cur = self.f[c.T]
            was = cur
            if c.op == "asg":
                cur = b
            elif c.op == "or":
                cur |= b
            elif c.op == "xor":
                cur ^= b
            else:
                cur &= b
            self.f[c.T] = cur & 0xff
            if self.f[c.T] != was:
                self.changed = True

    def test(self, which, env):
        latch = self.M if which == "M" else self.D
        c = self.cell
        if c is not None and c.shape in ("TA", "TO") and c.T == which:
            g = self._fire(env)
            if c.shape == "TA":
                r = (not latch) and g
                if (not latch) and not g:
                    self.devs.append(self.n)
                    self.changed = True
            else:
                r = (not latch) or g
                if latch and g:
                    self.devs.append(self.n)
                    self.changed = True
            return r
        return not latch

    def setok(self, which, env):
        c = self.cell
        if c is not None and c.shape == "GS" and c.T == which:
            g = self._fire(env)
            if not g:
                self.devs.append(self.n)
                self.changed = True
            return g
        return True

    def pred(self, shape, env):
        """NV / ND: the write notice's predicate, with its gate."""
        c = self.cell
        if c is not None and c.shape == shape:
            g = self._fire(env)
            if not g:
                self.devs.append(self.n)
                self.changed = True
            return g
        return True

    def access(self, W, ln, off, value):
        self.n += 1
        idata = (value & MASK[ln]) if W else 0
        C = 1 if (off & 0x100) else 0
        rel = off & ~0x100
        i32 = idata & 0xffffffff
        odata = 0
        env = lambda: self._env(W, C, idata, rel)
        if self.v.get("head"):
            # the pre-fix code: image byte indexed before the switch, exits on a memconf store and on any other offset
            odata = {0: self.f["chipid"], 4: self.f["chiprev"], 8: self.f["memconf"]}.get(rel, 0)
            if rel in (0, 4):
                pass
            elif rel == 8:
                if W:
                    self.out.append(HEADCNF % (rel, C))
                    raise Exit()
            else:
                self.out.append("[ mvme187_memc: unimplemented %s offset 0x%x" % ("write to" if W else "read from", rel) +
                                (": 0x%x" % i32 if W else "") + " ]" + NL)
                raise Exit()
            return odata
        self.hook("H", env())
        if rel == 0x00:
            odata = self.f["chipid"]
            self.hook("CI", env())
        elif rel == 0x04:
            odata = self.f["chiprev"]
            self.hook("CR", env())
        elif rel == 0x08:
            odata = self.f["memconf"]
            self.hook("MT", env())
            if W:
                if self.v.get("exit_mw"):
                    self.out.append(HEADCNF % (rel, C))
                    raise Exit()
                self.hook("MW", env())
                if self.test("M", env()):
                    self.out.append(MNOTE % (i32, C))
                    if self.setok("M", env()):
                        self.M = 1
                    self.hook("MB", env())
            self.hook("ME", env())
        else:
            if self.v.get("exit_def"):
                self.out.append("[ mvme187_memc: unimplemented %s offset 0x%x" % ("write to" if W else "read from", rel) +
                                (": 0x%x" % i32 if W else "") + " ]" + NL)
                raise Exit()
            self.hook("DT", env())
            if self.test("D", env()):
                direction = "write to" if (W and self.pred("ND", env())) else "read from"
                s = "[ mvme187_memc: unimplemented %s offset 0x%x (controller %i)" % (direction, rel, C)
                if W and self.pred("NV", env()):
                    s += ": 0x%x" % i32
                self.out.append(s + " (once) ]" + NL)
                if self.setok("D", env()):
                    self.D = 1
                self.hook("DB", env())
            self.hook("DA", env())
        self.hook("TL", env())
        return odata


MEMC = 0xfff43000
OPS = {0x03: ("ld", 1), 0x02: ("ld", 2), 0x05: ("ld", 4), 0x0b: ("st", 1), 0x09: ("st", 4)}


class Completed(object):
    def __init__(self, rc, text):
        self.returncode = rc
        self.stdout = text.encode("latin-1")


class Fake(object):
    """subprocess.run replacement: a gxemul whose MEMC device is the model above (sessions recorded for the fast walk)."""

    def __init__(self, variant, record=None):
        self.v = variant
        self.record = record
        self.last = None       # the last Device (its deviation set)
        self.traces = []       # one (rc, text) per run

    def run(self, argv, input=b"", stdout=None, stderr=None, timeout=None):
        if self.record is not None:
            self.record.append((list(argv), input))
        rc, text = self.run_one(argv, input)
        return Completed(rc, text)

    def run_one(self, argv, inp):
        media = self.v.get("media")
        if media == "absent":
            raise FileNotFoundError(2, "No such file or directory", argv[0])
        if media == "true":
            return 0, ""
        if media == "false":
            return 1, ""
        if "nosuchmachine" in argv:
            return 1, "GXemul: unknown machine type" + NL
        dev = Device(self.v)
        self.last = dev
        regs = [0] * 32
        mem = {}
        pc = 0
        out = []
        rc = 0
        for line in inp.decode("latin-1").split(NL):
            line = line.strip()
            if not line or line == "quit":
                continue
            if line == "reg":
                out.append("GXemul> reg" + NL + "cpu0:  pc = 0x%08x" % pc + NL)
                for i in range(0, 32, 4):
                    out.append("  " + "  ".join("r%-2i = 0x%08x" % (j, regs[j]) for j in range(i, i + 4)) + NL)
                continue
            if line.startswith("put w "):
                a, w = line[6:].split(",")
                mem[int(a, 16)] = int(w, 16)
                continue
            if line == "step 1":
                w = mem.get(pc, 0)
                op = w >> 26
                rd = (w >> 21) & 31
                rs1 = (w >> 16) & 31
                imm = w & 0xffff
                addr = (regs[rs1] + imm) & 0xffffffff
                off = addr - MEMC
                if op in OPS and 0 <= off < 0x200:
                    kind, ln = OPS[op]
                    try:
                        if kind == "ld":
                            val = dev.access(False, ln, off, 0) & MASK[ln]
                            if rd:
                                regs[rd] = val
                        else:
                            dev.access(True, ln, off, regs[rd])
                    except Exit:
                        out.extend(dev.out)
                        return 1, "".join(out)
                    out.extend(dev.out)
                    dev.out = []
                pc = (pc + 4) & 0xffffffff
                continue
            if "=" in line:
                name, val = line.split("=", 1)
                val = int(val, 16)
                if name == "pc":
                    pc = val
                elif name.startswith("r"):
                    i = int(name[1:])
                    if i:
                        regs[i] = val
        return rc, "".join(out)


_PROBE_CODE = {}
_SHARED_TMP = None


def exec_probe(probe_path, variant, record=None):
    """Run the probe script against the fake gxemul; returns (rows [(name, ok)], controls, symptom_hits, got dict)."""
    global _SHARED_TMP
    if probe_path not in _PROBE_CODE:
        src = io.open(probe_path, encoding="utf-8").read()
        _PROBE_CODE[probe_path] = compile(src, probe_path, "exec")
    if _SHARED_TMP is None:
        _SHARED_TMP = tempfile.mkdtemp(prefix="memc_variants_5_")
    fake = Fake(variant, record)
    ns = {"__name__": "__probe__", "__file__": probe_path}
    real_run, real_mkdtemp = subprocess.run, tempfile.mkdtemp
    old_argv, old_stdout = sys.argv, sys.stdout
    subprocess.run = fake.run
    tempfile.mkdtemp = lambda prefix=None, **k: _SHARED_TMP
    sys.argv = ["probe", "fake-gxemul", "sim"]
    sys.stdout = io.StringIO()
    try:
        exec(_PROBE_CODE[probe_path], ns)
        text = sys.stdout.getvalue()
    finally:
        subprocess.run, tempfile.mkdtemp = real_run, real_mkdtemp
        sys.argv, sys.stdout = old_argv, old_stdout
    got = {}
    for line in text.split(NL):
        if len(line) > 60 and line[:18].strip() and line.endswith((" ok", " FAIL")):
            got[line[:18].strip()] = line[19:39].strip()
    return ns["rows"], ns["controls"], ns["symptom_hits"], got


def red_of(rows):
    return [n.replace(" ", "_") for n, ok in rows if not ok]


def probe_path():
    return PROBE206 if os.path.exists(PROBE206) else PROBE206_INTREE


# --------------------------------------------------------------------------------------------------- fast walk and classes
_RECORDED = None


def recorded_sessions():
    """The probe's sessions (argv, stdin) recorded once from a run of the fix."""
    global _RECORDED
    if _RECORDED is None:
        rec = []
        exec_probe(probe_path(), {}, record=rec)
        _RECORDED = rec
    return _RECORDED


def trace(variant):
    """(observable trace, deviation set, changed) of a variant over the recorded sessions."""
    fake = Fake(variant)
    obs = []
    devs = []
    changed = False
    for i, (argv, inp) in enumerate(recorded_sessions()):
        rc, text = fake.run_one(argv, inp)
        obs.append((rc, text))
        if fake.last is not None:
            devs.extend((i, n) for n in fake.last.devs)
            changed = changed or fake.last.changed
            fake.last = None
    return tuple(obs), tuple(devs), changed


# reachable (W, C, M, D) at each position, as the function is written (MB / DB after the set; GS before it)
def reach(P, shape=None):
    allv = [(W, C, M, D) for W in (0, 1) for C in (0, 1) for M in (0, 1) for D in (0, 1)]
    if shape == "GS":
        return [t for t in allv if (t[0] == 1 and t[2] == 0)] if P == "M" else [t for t in allv if t[3] == 0]
    if shape in ("TA", "TO"):
        return [t for t in allv if t[0] == 1] if P == "M" else allv
    if shape in ("NV", "ND"):
        return [t for t in allv if t[0] == 1 and t[3] == 0]
    if P in ("H", "CI", "CR", "MT", "DT"):
        return allv
    if P == "MW":
        return [t for t in allv if t[0] == 1]
    if P == "MB":
        return [t for t in allv if t[0] == 1 and t[2] == 1]
    if P == "ME":
        return [t for t in allv if t[0] == 0 or t[2] == 1]
    if P in ("DB", "DA"):
        return [t for t in allv if t[3] == 1]
    if P == "TL":
        return allv      # offset-dependent; handled with rels below
    raise ValueError(P)


IDATA_SAMPLES = [0, 0x05, 0x07, 0x5a, 0xff, 0xffffffff] + [1 << b for b in range(32)]
RELS = {"H": [0, 4, 8, 0x0c, 0xf3], "CI": [0], "CR": [4], "MT": [8], "MW": [8], "MB": [8], "ME": [8],
        "DT": [0x0c, 0xf3], "DB": [0x0c, 0xf3], "DA": [0x0c, 0xf3], "TL": [0, 4, 8, 0x0c, 0xf3]}


def semantic_vacuous(c):
    """True iff the cell cannot change any observable at its position for ANY access the function can see there."""
    if c.shape in ("L", "K"):
        for (W, C, M, D) in reach(c.P):
            for rel in RELS[c.P]:
                if c.P == "TL":        # consistency: a memconf store sets M; a default access sets D
                    if rel == 8 and W and not M:
                        continue
                    if rel not in (0, 4, 8) and not D:
                        continue
                for idata in (IDATA_SAMPLES if W else [0]):
                    if not gate_eval(c.g, W, C, M, D, idata, rel):
                        continue
                    if c.shape == "L":
                        cur = M if c.T == "M" else D
                        new = {"set": 1, "clr": 0, "idat": idata & 0xffffffff, "xor1": cur ^ 1,
                               "xori": (cur ^ idata) & 0xffffffff}[c.op]
                        if bool(new) != bool(cur):
                            return False
                    else:
                        b = idata & 0xff
                        cur = {"chipid": 0x80, "chiprev": 1, "memconf": 3}[c.T]
                        new = {"asg": b, "or": cur | b, "xor": cur ^ b, "and": cur & b}[c.op]
                        if new != cur:
                            return False
        return True
    if c.shape == "GS":
        for (W, C, M, D) in reach(c.T, "GS"):
            for idata in IDATA_SAMPLES if W else [0]:
                for rel in ([8] if c.T == "M" else [0x0c, 0xf3]):
                    if not gate_eval(c.g, W, C, M, D, idata, rel):
                        return False
        return True
    if c.shape in ("TA", "TO"):
        for (W, C, M, D) in reach(c.T, c.shape):
            latch = M if c.T == "M" else D
            if (c.shape == "TA" and latch) or (c.shape == "TO" and not latch):
                continue
            for idata in IDATA_SAMPLES if W else [0]:
                for rel in ([8] if c.T == "M" else [0x0c, 0xf3]):
                    g = gate_eval(c.g, W, C, M, D, idata, rel)
                    if (c.shape == "TA" and not g) or (c.shape == "TO" and g):
                        return False
        return True
    for (W, C, M, D) in reach(None, c.shape):
        for idata in IDATA_SAMPLES:
            for rel in (0x0c, 0xf3):
                if not gate_eval(c.g, W, C, M, D, idata, rel):
                    return False
    return True


SHAPES = ["L", "K", "GS", "TA", "TO", "NV", "ND"]


def cell_rank(c):
    return (SHAPES.index(c.shape), gate_rank(c.g), POSITIONS.index(c.P) if c.P else 0, c.T or "", c.op or "")


def stmt_key(c):
    return (c.shape, c.P, c.T, c.op)


def stmt_name(k):
    shape, P, Tt, op = k
    if shape in ("L", "K"):
        return "%s_%s_%s_%s" % (shape, P, Tt, op)
    if shape in ("GS", "TA", "TO"):
        return "%s_%s" % (shape, Tt)
    return shape


class Walk(object):
    """The L-walk: every cell classified; representatives chosen; exact predictions for the built ones.
    RED-predicted cells (trace differs from the fix's): one representative per distinct observable trace, plus promotions so
    that every statement and every gate form is compiled at least once.  GREEN-predicted cells (the fix's trace): one
    representative per (statement, deviation set), each labelled UNFIRED (no probe access selected), UNOBSERVED (fired and
    changed the state, never read back) or NOCHANGE (fired, state unchanged: probe-equivalent, the ruling's disclosed form)."""

    def __init__(self):
        self.cells = all_cells()
        self.vacuous = []
        self.fix_trace = trace({})[0]
        self.trace_of = {}
        self.devs_of = {}
        self.changed_of = {}
        self.by_trace = {}                 # observable trace -> [cells]  (non-vacuous)
        self.green_groups = {}             # (statement, deviation set) -> [cells]  (fix-trace cells)
        for c in self.cells:
            if semantic_vacuous(c):
                self.vacuous.append(c)
                continue
            obs, devs, changed = trace({"cell": c})
            k = c.key()
            self.trace_of[k], self.devs_of[k], self.changed_of[k] = obs, devs, changed
            self.by_trace.setdefault(obs, []).append(c)
            if obs == self.fix_trace:
                self.green_groups.setdefault((stmt_key(c), devs), []).append(c)
        self.nonvacuous = sum(len(v) for v in self.by_trace.values())
        reps = []
        self.rep_of_trace = {}
        for tr, members in self.by_trace.items():
            if tr == self.fix_trace:
                continue
            members.sort(key=cell_rank)
            reps.append(members[0])
            self.rep_of_trace[tr] = members[0]
        # promotions: every statement and every gate form compiled at least once (among RED-predicted cells)
        built_stmts = set(stmt_key(c) for c in reps)
        built_gates = set(gate_name(c.g) for c in reps)
        self.promoted = []
        red_cells = sorted((c for tr, ms in self.by_trace.items() if tr != self.fix_trace for c in ms), key=cell_rank)
        for c in red_cells:
            if stmt_key(c) not in built_stmts or gate_name(c.g) not in built_gates:
                reps.append(c)
                self.promoted.append(c)
                built_stmts.add(stmt_key(c))
                built_gates.add(gate_name(c.g))
        self.green_reps = []
        self.green_kind = {}
        self.green_members = {}            # rep key -> the GREEN cells it measures
        nochange = {}                      # NOCHANGE cells are probe-equivalent by construction: one build per statement
        for (sk, devs), members in self.green_groups.items():
            members.sort(key=cell_rank)
            rep = members[0]
            kind = "UNFIRED" if not devs else ("UNOBSERVED" if self.changed_of[rep.key()] else "NOCHANGE")
            if kind == "NOCHANGE":
                nochange.setdefault(sk, []).extend(members)
                continue
            self.green_reps.append(rep)
            self.green_kind[rep.key()] = kind
            self.green_members[rep.key()] = members[1:]
        for sk, members in nochange.items():
            members.sort(key=cell_rank)
            rep = members[0]
            self.green_reps.append(rep)
            self.green_kind[rep.key()] = "NOCHANGE"
            self.green_members[rep.key()] = members[1:]
        self.green_reps.sort(key=cell_rank)
        reps.sort(key=cell_rank)
        self.red_reps = reps
        self.reps = reps + self.green_reps
        names = [c.name() for c in self.reps]
        assert len(set(names)) == len(names)
        assert not set(names) & set(OLD_NAMES)

    def equivalents(self, rep):
        """Cells the representative measures: same observable trace (RED) or same (statement, deviation set) (GREEN)."""
        k = rep.key()
        if k in self.green_members:
            return self.green_members[k]
        return [c for c in self.by_trace[self.trace_of[k]] if c is not rep and c not in self.promoted]

    def green_summary(self):
        """UNFIRED / UNOBSERVED groups by (position, gate): the access kinds the probe lacks."""
        out = {}
        for rep in self.green_reps:
            kind = self.green_kind[rep.key()]
            if kind == "NOCHANGE":
                continue
            members = self.green_groups[(stmt_key(rep), self.devs_of[rep.key()])]
            for c in members:
                out.setdefault((kind, c.P or c.shape, gate_name(c.g)), []).append(stmt_name(stmt_key(c)))
        return out


_WALK = None


def walk():
    global _WALK
    if _WALK is None:
        _WALK = Walk()
    return _WALK


# ------------------------------------------------------------------------------- table 4's variants the model expresses
def C(shape, P, Tt, op, g):
    return Cell(shape, P, Tt, op, g)


def cg(*lits):
    return ("c", tuple(lits))


OLD2CELL = {
    "D2_mlatch_noset": C("L", "MB", "M", "clr", ("any",)), "D5_dlatch_noset": C("L", "DB", "D", "clr", ("any",)),
    "N2_mset_ctl0": C("GS", None, "M", None, cg("nC")), "N3_dset_ctl0": C("GS", None, "D", None, cg("nC")),
    "A_B5_chipid": C("L", "CI", "M", "set", ("any",)), "A_B5_chiprev": C("L", "CR", "M", "set", ("any",)),
    "A_B6_chipid": C("L", "CI", "D", "set", cg("W")), "A_B6_chiprev": C("L", "CR", "D", "set", cg("W")),
    "T2_dlatch_rd00": C("L", "CI", "D", "set", ("any",)), "T2_dlatch_rd04": C("L", "CR", "D", "set", ("any",)),
    "T2_dlatch_rd08": C("L", "MT", "D", "set", cg("nW")), "T2_mlatch_hoist": C("L", "ME", "M", "set", ("any",)),
    "A_B3_chipid_or": C("K", "CI", "chipid", "or", cg("W")), "A_B3_chipid_xor": C("K", "CI", "chipid", "xor", cg("W")),
    "A_B3_chiprev_or": C("K", "CR", "chiprev", "or", cg("W")), "A_B3_chiprev_xor": C("K", "CR", "chiprev", "xor", cg("W")),
    "M_B3_chipid": C("K", "CI", "chipid", "and", cg("W")), "M_B3_chiprev": C("K", "CR", "chiprev", "and", cg("W")),
    "A_B4_chipid": C("K", "CI", "chipid", "asg", cg("W", "C")), "A_B4_chiprev": C("K", "CR", "chiprev", "asg", cg("W", "C")),
    "A_B12_chipid": C("K", "MB", "chipid", "asg", cg("C")), "A_B12_chiprev": C("K", "MB", "chiprev", "asg", cg("C")),
    "A_B9_dsetidata": C("L", "DB", "D", "idat", cg("W")),
    "N9a_cnf_chiprev": C("K", "MW", "chiprev", "asg", ("any",)), "N9b_cnf_chipid": C("K", "MW", "chipid", "asg", ("any",)),
    "N9c_def_memconf": C("K", "DT", "memconf", "asg", cg("W")), "N9d_def_chipid": C("K", "DT", "chipid", "asg", cg("W")),
    "N7_keep_ctl1": C("K", "MW", "memconf", "asg", cg("C")), "N19_keep_latched": C("K", "MW", "memconf", "asg", cg("M")),
    "A_cnf_accept": C("K", "MW", "memconf", "asg", ("any",)),
    "A_B7_valctl0": C("NV", None, None, None, cg("nC")), "G_1_dirctl0": C("ND", None, None, None, cg("nC")),
    "M_B1_v": C("NV", None, None, None, ("ib", 8, 0)), "M_B2_v": C("NV", None, None, None, ("ob", 4, 1)),
    "M_B2_d": C("ND", None, None, None, ("ob", 4, 1)), "D13_def_noval": C("NV", None, None, None, ("never",)),
    "M_B1_m": C("TA", None, "M", None, ("ib", 8, 0)), "M_B1_d": C("TA", None, "D", None, ("ib", 8, 0)),
    "G_6_dbit3": C("TA", None, "D", None, ("ob", 3, 1)), "D6_dlatch_ctrl": C("TO", None, "D", None, cg("C")),
    "T2_mlatch_ctl1": C("TO", None, "M", None, cg("C")), "N1_mlatch_ctl0": C("TO", None, "M", None, cg("nC")),
    "M_B5_m": C("TO", None, "M", None, ("ib", 8, 1)), "M_B5_d": C("TO", None, "D", None, ("ib", 0, 1)),
}
for f in FIELDS:
    OLD2CELL["A_B1_" + f] = C("K", "DB", f, "asg", cg("W"))
    OLD2CELL["A_B2_" + f] = C("K", "DT", f, "asg", cg("W", "nC"))
    OLD2CELL["M_B4_" + f] = C("K", "DB", f, "and", cg("W"))
OLD2VAR = {n: {"cell": c} for n, c in OLD2CELL.items()}
OLD2VAR["B1_cnf_exit"] = {"exit_mw": True}
OLD2VAR["B2_def_exit"] = {"exit_def": True}
LEGS = [("base", {}), ("HEAD", {"head": True}), ("null_true", {"media": "true"}), ("null_absent", {"media": "absent"}),
        ("null_false", {"media": "false"})]
assert all(n in OLD_NAMES for n in OLD2VAR), set(OLD2VAR) - set(OLD_NAMES)


def measured4():
    out = {}
    for line in io.open(SCORES4, encoding="utf-8"):
        p = line.split()
        if len(p) > 1 and "RED=" in line:
            red = line.rsplit("RED=", 1)[1].strip()
            out[p[0]] = [] if red == "none" else red.split(",")
    return out


def predict(variant, probe=None):
    rows, controls, sym, got = exec_probe(probe or probe_path(), variant)
    return red_of(rows), all(ok for _, ok in controls), sym > 0, len(rows), got


# --------------------------------------------------------------------------------------------------------------- outputs
def V_all():
    return OLD + [(c.name(), c.edits()) for c in walk().reps]


def predmap_lines():
    """name<TAB>EXACT|ATLEAST<TAB>comma-joined red rows (the driver's comparison input)."""
    m4 = measured4()
    out = []
    for n, v in LEGS:
        red = predict(v)[0]
        out.append("%s\tEXACT\t%s" % (n, ",".join(red) or "none"))
    for n, _ in OLD:
        if n in OLD2VAR:
            red = predict(OLD2VAR[n])[0]
            out.append("%s\tEXACT\t%s" % (n, ",".join(red) or "none"))
        else:
            red = [r for r in m4.get(n, []) if r not in REWANTED]
            out.append("%s\tATLEAST\t%s" % (n, ",".join(red) or "none"))
    for c in walk().reps:
        red = predict({"cell": c})[0]
        out.append("%s\tEXACT\t%s" % (c.name(), ",".join(red) or "none"))
    return out


def pretable():
    w = walk()
    m4 = measured4()
    nrows = predict({})[3]
    out = []
    a = out.append
    a("PRETABLE_5 -- mvme187memcoob detector, test-variant table 5 (repair 5, %d rows).  Written BEFORE table 5 runs (this file's" % nrows)
    a("mtime precedes table5/SCORES.txt).  Instrument: table5/probe206_frozen.py (copied from regress/mvme187_memc_probe.py after the")
    a("repair-5 edits; base on the build tree 206/206, r5_20261105/base206/probe_base206.out).  Baseline: GXEMUL-SEC/src/devices/")
    a("dev_mvme187.c (== det_20261104/dev_mvme187.c.fix2: repair 5 changed the probe and the gate, not the device).  Legs first, in the")
    a("same clone: base, HEAD (det_20261104/dev_mvme187.c.HEAD), three null media.  Rows: %d." % nrows)
    a("")
    a("METHOD.  Every prediction marked `exact` is the probe's own verdict on a modelled device: the frozen probe is executed with its")
    a("gxemul replaced by a fake that decodes its m88k words and runs them against DEVICE_ACCESS(mvme187_memc) as written in the fix")
    a("with the variant's statement inserted at its position (memc_variants_5.py, class Device).  Calibration: `memc_variants_5.py")
    a("check4` replays table 4's frozen 148-row instrument through the same model for the HEAD leg, the null media, B1/B2 and every")
    a("table-4 variant the model expresses (%d of 112) and compares with table 4's measured red sets (T5_PREP.md records the result)." % len(OLD2VAR))
    a("Predictions marked `at least` are table 4's MEASURED red sets for the variants the model does not express (exits, faults, the")
    a("indexed read, masks, casts, swaps, widths: their mechanisms are not statements of L), minus the ten rows repair 5 re-wanted")
    a("(%s): those rows are not carried." % ", ".join(REWANTED))
    a("")
    a("THE DENOMINATOR (CONS_MYTHOS_local.md section 3, walked cell by cell -- see the module docstring for the alphabet):")
    nL = sum(1 for c in w.cells if c.shape == "L")
    nK = sum(1 for c in w.cells if c.shape == "K")
    nG = sum(1 for c in w.cells if c.shape in ("GS", "TA", "TO"))
    nN = sum(1 for c in w.cells if c.shape in ("NV", "ND"))
    a("  cells walked: %d = latch statements %d + keep statements %d + gated latch sets/tests %d + gated notice predicates %d" %
      (len(w.cells), nL, nK, nG, nN))
    a("  positions 11 (the ruling's ten plus ME, the memconf arm's after-block twin of DA); gates per position: 81 conjunctions over")
    a("  {W, C, M, D} (incl. always) + 64 idata-bit tests (all positions) + 16 offset-bit tests (H, DT, DB, DA, TL).")
    a("  VACUOUS (semantically no-op at the position; not mutants, not built): %d" % len(w.vacuous))
    ngreen = sum(len(m) for m in w.green_groups.values())
    nred = w.nonvacuous - ngreen
    a("  non-vacuous cells: %d.  Predicted RED: %d cells in %d distinct observable traces -> %d BUILT (one per trace, plus %d" %
      (w.nonvacuous, nred, len(w.rep_of_trace), len(w.red_reps), len(w.promoted)))
    a("  promoted so that every statement and every gate form is compiled at least once); the other %d RED cells are EQUIV:" %
      (nred - len(w.red_reps)))
    a("  the same observable trace as their representative on every probe access (listed under it).")
    a("  Predicted GREEN (the fix's trace): %d cells in %d (statement, deviation-set) groups -> %d BUILT: one per group for" %
      (ngreen, len(w.green_groups), len(w.green_reps)))
    kinds = {}
    for r in w.green_reps:
        kinds[w.green_kind[r.key()]] = kinds.get(w.green_kind[r.key()], 0) + 1
    a("  UNFIRED and UNOBSERVED, one per statement for NOCHANGE: %s." % ", ".join("%s %d" % kv for kv in sorted(kinds.items())))
    a("  UNFIRED = no probe access satisfies the gate at that position; UNOBSERVED = the statement fired and changed the state but")
    a("  no later access read it back; NOCHANGE = fired, state unchanged (probe-equivalent: the ruling's disclosed `^= idata` into")
    a("  a set latch and kin).  UNFIRED and UNOBSERVED are predicted SURVIVORS of the 206 rows inside the denominator.")
    a("")
    a("LEGS (exact):")
    for n, v in LEGS:
        red, ctl, sym, _, _ = predict(v)
        a("   %-18s %3d/%d  CONTROL=%s SYMPTOM=%s  red: %s" % (n, nrows - len(red), nrows, "OK" if ctl else "FAIL",
                                                           "PRESENT" if sym else "ABSENT", ",".join(red) or "none"))
    a("")
    a("TABLE 4's 112 (name, prediction):")
    for n, _ in OLD:
        if n in OLD2VAR:
            red = predict(OLD2VAR[n])[0]
            tag = "exact: %s" % (",".join(red) or "none (GREEN)")
            carried = [r for r in m4.get(n, []) if r not in REWANTED]
            a("   %-18s %-70s [table 4 measured: %s]" % (n, tag, ",".join(carried) or "none"))
        else:
            red = [r for r in m4.get(n, []) if r not in REWANTED]
            a("   %-18s at least: %s" % (n, ",".join(red) or "none (table 4: green)"))
    a("")
    a("NEW CELLS OF L, PREDICTED RED (%d built; name, exact red set on the %d rows, the statement, then the EQUIV cells it measures" %
      (len(w.red_reps), nrows))
    a("grouped by statement with their gates):")
    for c in w.red_reps:
        red = predict({"cell": c})[0]
        assert red, c.name()
        a("   %-34s exact: %s" % (c.name(), ",".join(red)))
        a("   %-34s   %s%s" % ("", c.what(), "   [promoted: statement or gate form not otherwise compiled]" if c in w.promoted else ""))
        eq = w.equivalents(c)
        if eq:
            by = {}
            for e in eq:
                by.setdefault(stmt_name(stmt_key(e)), []).append(gate_name(e.g))
            a("   %-34s   equiv (%d): %s" % ("", len(eq), "; ".join("%s: %s" % (k, " ".join(v)) for k, v in sorted(by.items()))))
    a("")
    a("NEW CELLS OF L, PREDICTED GREEN (%d built, one per (statement, deviation set); each a predicted SURVIVOR unless NOCHANGE):" %
      len(w.green_reps))
    for c in w.green_reps:
        red = predict({"cell": c})[0]
        assert not red, (c.name(), red)
        kind = w.green_kind[c.key()]
        eq = w.equivalents(c)
        a("   %-34s exact: none -- %s" % (c.name(), kind))
        a("   %-34s   %s" % ("", c.what()))
        if eq:
            a("   %-34s   equiv (%d): %s" % ("", len(eq), " ".join(gate_name(e.g) for e in eq)))
    a("")
    a("SURVIVOR SUMMARY -- the access kinds the 206 rows lack (kind, position, gate -> the statements that survive there):")
    for (kind, P, g), stmts in sorted(w.green_summary().items()):
        a("   %-10s %-4s %-12s %d statements: %s" % (kind, P, g, len(stmts), " ".join(sorted(set(stmts)))))
    a("")
    a("HEAD leg: SYMPTOM=PRESENT (exact set above).  Null media: CONTROL=FAIL each (exact sets above).  Base: %d/%d." % (nrows, nrows))
    return NL.join(out) + NL


def check4():
    """Replay table 4's instrument through the model: HEAD, the null media, and every table-4 variant the model expresses."""
    m4 = measured4()
    out = []
    bad = 0
    for n, v in [("base", {})] + [(n, v) for n, v in LEGS if n != "base"] + [(n, OLD2VAR[n]) for n, _ in OLD if n in OLD2VAR]:
        red = predict(v, PROBE148)[0]
        meas = m4.get(n, [])
        ok = sorted(red) == sorted(meas)
        bad += 0 if ok else 1
        out.append("%-18s %s  model: %s%s" % (n, "MATCH" if ok else "MISMATCH", ",".join(red) or "none",
                                              "" if ok else "   measured: " + (",".join(meas) or "none")))
    out.append("check4: %d compared, %d mismatches" % (len(out), bad))
    return NL.join(out) + NL


def main():
    a = sys.argv[1:]
    if a == ["list"]:
        print(" ".join(n for n, _ in V_all()))
    elif a == ["pretable"]:
        sys.stdout.write(pretable())
    elif a == ["predmap"]:
        sys.stdout.write(NL.join(predmap_lines()) + NL)
    elif a == ["check4"]:
        sys.stdout.write(check4())
    elif a == ["stats"]:
        w = walk()
        ngreen = sum(len(m) for m in w.green_groups.values())
        print("cells %d vacuous %d nonvacuous %d red-cells %d red-traces %d red-reps %d (promoted %d) green-cells %d green-groups %d" %
              (len(w.cells), len(w.vacuous), w.nonvacuous, w.nonvacuous - ngreen, len(w.rep_of_trace), len(w.red_reps),
               len(w.promoted), ngreen, len(w.green_reps)))
        by = {}
        for c in w.reps:
            by[c.shape] = by.get(c.shape, 0) + 1
        print("reps by shape", sorted(by.items()))
        kinds = {}
        for r in w.green_reps:
            kinds[w.green_kind[r.key()]] = kinds.get(w.green_kind[r.key()], 0) + 1
        print("green reps by kind", sorted(kinds.items()))
        for (kind, P, g), stmts in sorted(w.green_summary().items()):
            print("  %-10s %-4s %-12s %d: %s" % (kind, P, g, len(stmts), " ".join(sorted(set(stmts)))))
    elif a == ["cells"]:
        w = walk()
        built = set(c.key() for c in w.reps)
        for c in w.cells:
            k = "VACUOUS" if c in w.vacuous else ("BUILT" if c.key() in built else "EQUIV")
            print("%-9s %s" % (k, c.name()))
    elif len(a) == 4 and a[0] == "apply":
        s = io.open(a[2], encoding="latin-1", newline="").read()
        if a[1] in OLD_NAMES:
            f = dict(OLD)[a[1]]
        else:
            c = cell_from_name(a[1])
            assert c.name() == a[1], (c.name(), a[1])
            f = c.edits()
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
