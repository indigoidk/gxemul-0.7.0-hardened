#!/usr/bin/env python3
"""qhs_variants_7.py -- test-variant TABLE 7 for qhslowifetch (repair 7: 103 rows; no product change since repair 5), 2026-11-05.
Table 6's 46 (r6_20261105/qhs_variants_6.py, imported) plus thirteen for repair 7, each ONE exact edit against
r7_20261105/cpu_ppc_instr.c.fix7 (== GXEMUL-SEC == fix6):
  the arm (a) x pc-alignment x MSR[ME] closure (codex GPT-6 Astra, pass 6: p6_20261105/codex_codex_qhs_p6.txt; B123_NOTE.md) --
    R7_a_bit1    guard && !(cpu->pc & 2)                              codex B1 (b123_variant.py's text)
    R7_a_bit0    guard && !(cpu->pc & 1)                              B1's other low bit
    R7_a_meun    guard && (!(msr & ME) || cpu->pc == addr)            codex B2: refuses an unaligned read-ahead with ME set
    R7_a_clun    guard && ((msr & ME) || cpu->pc == addr)             B2's other polarity: refuses one with ME clear
    R7_a_msrset  arm (a) sets MSR[ME] when cpu->pc != addr            codex B3
    R7_a_msrclr  arm (a) clears MSR[ME] when cpu->pc != addr          B3's twin
    R7_x_alcl / R7_x_alme / R7_x_uncl / R7_x_unme  the guard conjoined with !(cell): each excludes exactly one of the four
                 (aligned, unaligned) x (ME clear, ME set) cells; x_uncl and x_unme are De Morgan forms of a_clun and a_meun
    R7_fail_unal the read's failure test disjoined with `|| cpu->pc != addr`   codex R3 (pass 5's FILED disclosure)
  and the Gemini 4 Argon seat's pass-6 findings (g12_variant.py's text; MEASURED 82/82, B123_NOTE.md) --
    R7_G1_b_lt   arm (b)'s aligned compare made `cpu->pc < addr`
    R7_G2_d_msr  arm (d)'s test made `if (cpu->cd.ppc.msr)`
  qhs_variants_7.py list | apply <name> <in> <out> | pretable"""
import importlib.util
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
QD = os.path.dirname(HERE)


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


q6 = _load("q6", os.path.join(QD, "r6_20261105", "qhs_variants_6.py"))
b123 = _load("b123", os.path.join(HERE, "b123_variant.py"))
g12 = _load("g12", os.path.join(HERE, "g12_variant.py"))
T, NL = chr(9), chr(10)
G = T * 3 + "if (cpu->translation_readahead)" + NL          # arm (a)'s guard line
A = G + T * 4 + "return;" + NL                               # arm (a): guard + bare return
FAILT = T * 2 + "    sizeof(ib), MEM_READ, CACHE_INSTRUCTION)) {" + NL
ME = "(cpu->cd.ppc.msr & PPC_MSR_ME)"


def guard(cond):
    return [(G, T * 3 + "if (cpu->translation_readahead && " + cond + ")" + NL)]


def nx(cells):
    return ["T_ra_%s_nonex" % c for c in cells]


# The six unaligned read-ahead sessions, by cell: odd = (01, clear); o1m = (01, set); o2/o2m = (10, clear/set); o3/o3m = (11, ...).
UNAL = ["odd", "o1m", "o2", "o2m", "o3", "o3m"]
NEWV = [
    ("R7_a_bit1", b123.EDITS["B1"], nx(["o2", "o2m", "o3", "o3m"]),
     "codex B1: refuses a read-ahead whose pc has bit 1 set (MEASURED on the cells, B123_NOTE.md)"),
    ("R7_a_bit0", guard("!(cpu->pc & 1)"), nx(["odd", "o1m", "o3", "o3m"]), "refuses a read-ahead whose pc has bit 0 set"),
    ("R7_a_meun", b123.EDITS["B2"], nx(["o1m", "o2m", "o3m"]),
     "codex B2: refuses an unaligned read-ahead with ME set (MEASURED on the cells)"),
    ("R7_a_clun", guard("(" + ME + " || cpu->pc == addr)"), nx(["odd", "o2", "o3"]),
     "refuses an unaligned read-ahead with ME clear"),
    ("R7_a_msrset", b123.EDITS["B3"], ["T_ra_odd_msr", "T_ra_o2_msr", "T_ra_o3_msr"],
     "codex B3: arm (a) sets ME at an unaligned pc (MEASURED on the cells)"),
    ("R7_a_msrclr", [(A, T * 3 + "if (cpu->translation_readahead) {" + NL + T * 4 +
                      "cpu->cd.ppc.msr &= ~(uint64_t)(cpu->pc != addr ? PPC_MSR_ME : 0);" + NL + T * 4 + "return;" + NL + T * 3 + "}" +
                      NL)], ["T_ra_o1m_msr", "T_ra_o2m_msr", "T_ra_o3m_msr"], "arm (a) clears ME at an unaligned pc"),
    ("R7_x_alcl", guard("!(cpu->pc == addr && !" + ME + ")"), ["T_ra_nonex"], "excludes the (aligned, ME clear) cell"),
    ("R7_x_alme", guard("!(cpu->pc == addr && " + ME + ")"), ["T_ra_me_nonex"], "excludes the (aligned, ME set) cell"),
    ("R7_x_uncl", guard("!(cpu->pc != addr && !" + ME + ")"), nx(["odd", "o2", "o3"]),
     "excludes the (unaligned, ME clear) cell; De Morgan form of R7_a_clun"),
    ("R7_x_unme", guard("!(cpu->pc != addr && " + ME + ")"), nx(["o1m", "o2m", "o3m"]),
     "excludes the (unaligned, ME set) cell; De Morgan form of R7_a_meun"),
    ("R7_fail_unal", [(FAILT, T * 2 + "    sizeof(ib), MEM_READ, CACHE_INSTRUCTION) || cpu->pc != addr) {" + NL)],
     [r for c in UNAL for r in ("T_ra_%s_pc" % c, "T_ra_%s_nonex" % c)],
     "codex R3: a successful unaligned fetch enters the block -- ME clear checkstops at the entry pc, ME set takes a machine "
     "check to 0x200; no halt report either way"),
    ("R7_G1_b_lt", g12.EDITS["G1"], [], "Gemini G1: GREEN, disclosed -- differs only on arm (b)'s taken side, which has no producer"),
    ("R7_G2_d_msr", g12.EDITS["G2"], [], "Gemini G2: GREEN, disclosed -- arm (d) is unreached on pmppc (V4, V5 green)"),
]
V = list(q6.V) + [(n, e) for n, e, _, _ in NEWV]
NEW_ROWS = ["T_ra_odd_msr"] + ["T_ra_%s_%s" % (c, k) for c in ("o1m", "o2", "o2m", "o3", "o3m") for k in ("session", "pc", "nonex", "msr")]
BUILD_DEP = ("W5_dec_tail", "D7_dom_run", "V7_fail_inv", "D12_else_ra")
GREEN6 = ("D6_d_inv", "D9_mc_vec", "D10_chk_run", "D11_b_noref", "V2_b_del", "V3_c_true", "V4_d_false", "V5_d_true",
          "V6_chk_nopark", "R5_cb", "R5_arun")


def scores6():
    m = {}
    for line in io.open(os.path.join(QD, "r6_20261105", "table6", "SCORES.txt"), encoding="utf-8"):
        p = line.split()
        if len(p) > 1 and "RED=" in line:
            red = line.rsplit("RED=", 1)[1].strip()
            m[p[0]] = [] if red == "none" else red.split(",")
    return m


def pretable():
    m6 = scores6()
    head = m6["HEAD"] + NEW_ROWS
    out = [
        "PRETABLE_7 -- qhslowifetch, test-variant table 7 (repair 7: 103 rows).  Written BEFORE table 7 runs (this file's mtime precedes",
        "table7/'s).  Instrument: table7/probe103_frozen.py (== base103/probe103_run.py, 103/103 on build/).  Baseline: fix7 (== fix6).",
        "Table 6's 46 are predicted AT LEAST their table-6 red sets, except the build-dependent W5_dec_tail, D7_dom_run, V7_fail_inv and",
        "D12_else_ra (RED, rows not predicted) and V12_fail_ra (NOT PREDICTED); the eleven green in table 6 are predicted GREEN.  The 21",
        "new rows are informational for the 46.  Repair 7's thirteen are predicted EXACTLY (row set equality; GREEN = no row red).",
        "base: 103/103 CONTROL=OK SYMPTOM=ABSENT.  HEAD: table 6's HEAD set + the 21 new rows (the pre-fix build exits at the read-ahead",
        "fetch, so every new session dies: exit1, no registers, one halt report) = %d red -> %d/103 (%d rows red), CONTROL=OK," % (
            len(head), 103 - len(head), len(head)),
        "SYMPTOM=PRESENT.  Null media, exactly: null_true 41/103 (table 6's 36 + the five new session rows, exit0), null_absent 24/103,",
        "null_false 25/103 -- CONTROL=FAIL, SYMPTOM=ABSENT on all three.",
        "CHANNELS for the new rows (derived from the code, measured on the cells in B123_NOTE.md): T_ra_<cell>_nonex counts halt reports",
        "for a read-ahead from 0xfec00004 | low bits -- 2 when arm (a) returns at that cell, 1 when a guard refusing it sends the",
        "read-ahead failure to arm (c), 0 when a successful fetch is sent into the block first (R7_fail_unal); T_ra_<cell>_pc is the",
        "park, 0xfec00008 | low bits -- the entry pc under R7_fail_unal with ME clear (checkstop), 0x200 with ME set (machine check);",
        "T_ra_<cell>_msr is MSR as entered -- an arm (a) MSR write at pc != addr flips it.",
        "", "VARIANTS:"]
    new = dict((a, (b, c)) for a, _, b, c in NEWV)
    for n, _ in V:
        if n in new:
            rows, why = new[n]
            out.append("   %-14s exactly: %s   (%s)" % (n, ",".join(rows) if rows else "none -- GREEN", why))
        elif n == "V12_fail_ra":
            out.append("   %-14s NOT PREDICTED" % n)
        elif n in BUILD_DEP:
            out.append("   %-14s RED (build-dependent rows; not predicted)" % n)
        elif n in GREEN6:
            assert m6.get(n) == [], (n, m6.get(n))
            out.append("   %-14s at least: none -- predicted GREEN (green in table 6)" % n)
        else:
            assert m6.get(n), n
            out.append("   %-14s at least: %s" % (n, ",".join(m6[n])))
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
