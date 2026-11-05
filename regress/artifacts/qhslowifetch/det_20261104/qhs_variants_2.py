#!/usr/bin/env python3
"""qhs_variants_2.py -- test-variant TABLE 2 for the qhslowifetch detector, 2026-11-05, as ruled by the adjudication (adj_20261104/
ADJ_FABLE.md P9/P15, FINAL_FABLE.md F6/F8, TIE_FABLE.md T1): table 1's eighteen (D8 re-anchored: the ruled ME comment now sits inside
arm (d)'s block), table 1b's D14 and D15, and the seven the rulings added -- arm (a)'s guard deleted (the reconciliation's W7), arm (b)
deleted, arm (c)'s guard forced true, arm (d)'s guard forced false and forced true, the checkstop fallback's park dropped, and the read's
failure test inverted.  Baseline: cpu_ppc_instr.c.fix3, the final candidate (T1: no MSR edit in arm (d)).
  qhs_variants_2.py list                     the variant names, in table order
  qhs_variants_2.py apply <name> <in> <out>  write <in> with variant <name> applied (each edit asserted to occur ONCE; exit 3 if not)
  qhs_variants_2.py pretable <rows>          the PRETABLE_2 record for a <rows>-row instrument (written BEFORE table 2 runs)
Exact-string edits; every backslash is chr(92)."""
import io
import sys

T = chr(9)
NL = chr(10)
BS = chr(92)

OPEN = T * 2 + "    sizeof(ib), MEM_READ, CACHE_INSTRUCTION)) {" + NL
FAILT = T * 2 + "if (!cpu->memory_rw(cpu, cpu->mem, addr, ib," + NL
A = T * 3 + "if (cpu->translation_readahead)" + NL + T * 4 + "return;" + NL
B = T * 3 + "if (cpu->pc != addr) {" + NL
BREF = B + T * 4 + "quick_pc_to_pointers(cpu);" + NL
BFULL = BREF + T * 4 + "return;" + NL + T * 3 + "}" + NL
C = (T * 3 + "if (!cpu->running) {" + NL + T * 4 + "cpu->cd.ppc.next_ic = &nothing_call;" + NL + T * 4 + "return;" + NL +
     T * 3 + "}" + NL)
CHEAD = T * 3 + "if (!cpu->running) {" + NL + T * 4 + "cpu->cd.ppc.next_ic = &nothing_call;" + NL
DHEAD = T * 3 + "if (cpu->cd.ppc.msr & PPC_MSR_ME) {" + NL
DD = (DHEAD + T * 4 + "/*  ppc_exception() leaves MSR[ME] set," + NL + T * 4 + "    where the architecture clears it on a" + NL +
      T * 4 + "    machine check, so a further failing" + NL + T * 4 + "    fetch here takes a second machine check" + NL +
      T * 4 + "    instead of checkstopping (#QQQ).  */" + NL + T * 4 + "ppc_exception(cpu, PPC_EXCEPTION_MC);" + NL + T * 4 + "return;" +
      NL + T * 3 + "}" + NL)
CHK = (T * 3 + "cpu->running = 0;" + NL + T * 3 + "cpu->cd.ppc.next_ic = &nothing_call;" + NL + T * 3 + "return;" + NL + T * 2 + "}" + NL)
ELSE = T + "} else {" + NL + T * 2 + '/*  fatal("TRANSLATION MISS!' + BS + 'n");  */' + NL
HEAD_EXIT = (T * 3 + 'fatal("PPC to_be_translated(): "' + NL + T * 3 + '    "read failed: TODO' + BS + 'n");' + NL + T * 3 + "exit(1);" + NL +
             T * 3 + "/*  goto bad;  */" + NL)


def w5(s):
    assert s.count(A) == 1 and s.count(CHK) == 1
    a = s.index(A)
    b = s.index(CHK, a) + len(CHK) - len(T * 2 + "}" + NL)
    return s[:a] + T * 3 + ";" + NL + s[b:]


def d8(s):
    assert s.count(C) == 1 and s.count(DD) == 1
    return s.replace(C, "", 1).replace(DD, DD + C, 1)


S_TS = "T step: session text prompt pc srr0"
S_TC = "T cont: session text prompt pc srr0"
S_AG = "again: session text prompt pc srr0"
S_ME = "T me: session text pc srr0"
TRA = "T ra session pc nonex stopped (the exit fires inside the read-ahead)"
W5RED = "T cont unimpl; T step pc srr0 exc; T me pc srr0 exc; again pc srr0 exc (W5's set, BUILD-DEPENDENT: the uninitialised word, P25)"
V = [
    ("B1_exit_head", [(OPEN, OPEN + HEAD_EXIT)], 23,
     "%s; %s; %s; %s; again session; %s (= the HEAD leg)" % (S_TS, S_TC, S_AG, S_ME, TRA), "(b) HEAD's fatal()+exit(1) reinstated at the arm head"),
    ("W2_bare_ret", [(OPEN, OPEN + T * 3 + "return;" + NL)], 8,
     "T step pc, T cont pc nonex, T me pc, again pc; T ra pc nonex addr (the real fetch returns unparked, the run walks on)", "W2: a bare return at the arm head, no park"),
    ("W3_goto_bad", [(OPEN, OPEN + T * 3 + "goto bad;" + NL)], 3,
     "T step unimpl, T cont unimpl, again unimpl", "W3: goto bad"),
    ("W4_isi_inv", [(C, T * 3 + "if (!cpu->running) {" + NL + T * 4 + "ppc_exception(cpu, PPC_EXCEPTION_ISI);" + NL + T * 4 + "return;" + NL +
                     T * 3 + "}" + NL)], 14,
     "pc srr0 exc in T step, T cont, T me, again; T cont unimpl; T ra pc (0x400)", "W4: arm (c) invents an ISI instead of parking"),
    ("W5_dec_tail", w5, 11, W5RED + "; T ra nonex (the read-ahead slot is translated from garbage, so no real fetch) and maybe pc", "W5: the arm emptied, the uninitialised ib decoded"),
    ("D1_c_inv", [(CHEAD, CHEAD.replace("if (!cpu->running)", "if (cpu->running)"))], 6,
     "T step/T cont/again chkstop; T me pc srr0 exc", "(d) arm (c)'s test inverted"),
    ("D2_c_del", [(C, "")], 6, "as D1", "(d) arm (c) deleted"),
    ("D3_c_nopark", [(C, T * 3 + "if (!cpu->running) {" + NL + T * 4 + "return;" + NL + T * 3 + "}" + NL)], 8,
     "T step pc, T cont pc nonex, T me pc, again pc; T ra pc nonex addr (no park: the run walks past the window)", "(d) arm (c) keeps its test, drops the park"),
    ("D4_b_inv", [(B, T * 3 + "if (cpu->pc == addr) {" + NL)], 2,
     "T cont nonex (measured in table 1; again nonex stays 2 -- PRETABLE.errata.md item 2); T ra nonex (the refreshed slot re-fetches)", "(d) arm (b)'s test inverted"),
    ("D5_a_inv", [(A, T * 3 + "if (!cpu->translation_readahead)" + NL + T * 4 + "return;" + NL)], 6,
     "as W2 on the four -T sessions; T ra nonex (the read-ahead failure falls to (c)'s park: one report) and maybe pc", "(d) arm (a)'s test inverted: a bare return on every non-readahead fetch"),
    ("D6_d_inv", [(DHEAD, T * 3 + "if (!(cpu->cd.ppc.msr & PPC_MSR_ME)) {" + NL)], 0,
     "NONE (arm (c) returns first on every -T session; arm (d) is ROW 5's, FILED pending X11)", "(d) arm (d)'s test inverted"),
    ("D7_dom_run", [(OPEN, T * 2 + "    sizeof(ib), MEM_READ, CACHE_INSTRUCTION) && cpu->running) {" + NL)], 11,
     "as W5, T ra included (memory_rw cleared running before returning, so the arm is skipped; BUILD-DEPENDENT)",
     "(d) the read's failure test conditioned on running"),
    ("D8_c_below_d", d8, 3, "T me pc srr0 exc", "(d) arm (c) moved below arm (d) (re-anchored on the commented arm (d))"),
    ("D9_mc_vec", [("ppc_exception(cpu, PPC_EXCEPTION_MC);", "ppc_exception(cpu, PPC_EXCEPTION_DSI);")], 0,
     "NONE (disclosed: arm (d) unreachable here)", "(d) arm (d) delivers the wrong exception"),
    ("D10_chk_run", [(CHK, T * 3 + "cpu->cd.ppc.next_ic = &nothing_call;" + NL + T * 3 + "return;" + NL + T * 2 + "}" + NL)], 0,
     "NONE (disclosed: the checkstop fallback is unreachable here)", "(d) the checkstop fallback leaves running set"),
    ("D11_b_noref", [(BREF, B)], 0, "NONE (disclosed: arm (b) is reached on no measured session)", "(d) arm (b) drops its next_ic refresh"),
    ("D12_else_ra", [(ELSE, T + "} else if (!cpu->translation_readahead) {" + NL + T * 2 + '/*  fatal("TRANSLATION MISS!' + BS + 'n");  */' + NL)],
     3, "T ra nonex addr stopped (read-ahead skips the read: the slot is translated from garbage, no halt at all; BUILD-DEPENDENT, "
        "the session may run on to its timeout)",
     "(d) the slow path's else conditioned on not read-ahead"),
    ("D13_c_me", [(CHEAD, CHEAD.replace("if (!cpu->running)", "if (!cpu->running && !(cpu->cd.ppc.msr & PPC_MSR_ME))"))], 3,
     "T me pc srr0 exc", "(d) arm (c) conditioned on ME clear"),
    ("D14_c_meset", [(CHEAD, CHEAD.replace("if (!cpu->running)", "if (!cpu->running && (cpu->cd.ppc.msr & PPC_MSR_ME))"))], 3,
     "T step/T cont/again chkstop (table 1b)", "arm (c) conditioned on ME set (the mirror of D13)"),
    ("D15_dom_ok", [(OPEN, T * 2 + "    sizeof(ib), MEM_READ, CACHE_INSTRUCTION) || 1) {" + NL)], 5,
     "noT unimpl, noT chkstop (table 1b; table1b/D15_EDIT.md); T ra pc nonex addr (the successful fetch of 0xfec00004 itself enters "
     "the block and checkstops there: no subfic, no read-ahead)", "the block entered whatever the slow-path read returns"),
    ("W7_a_del", [(A, "")], 1,
     "T ra nonex (the read-ahead failure falls to (c)'s park, whose batch end survives the read-ahead return: one report; F4) and "
     "maybe pc",
     "the reconciliation's W7: arm (a)'s read-ahead guard deleted"),
    ("V2_b_del", [(BFULL, "")], 0, "NONE (arm (b) is reached on no measured session)", "arm (b) deleted"),
    ("V3_c_true", [(CHEAD, CHEAD.replace("if (!cpu->running)", "if (1)"))], 0,
     "NONE (on pmppc every failing fetch that reaches (c) has running 0 already)", "arm (c)'s guard forced true"),
    ("V4_d_false", [(DHEAD, T * 3 + "if (0) {" + NL)], 0, "NONE (arm (d) unreachable here)", "arm (d)'s guard forced false"),
    ("V5_d_true", [(DHEAD, T * 3 + "if (1) {" + NL)], 0, "NONE (arm (d) unreachable here)", "arm (d)'s guard forced true"),
    ("V6_chk_nopark", [(CHK, T * 3 + "cpu->running = 0;" + NL + T * 3 + "return;" + NL + T * 2 + "}" + NL)], 0,
     "NONE (the checkstop fallback is unreachable here)", "the checkstop fallback's park dropped (Mythos (iv))"),
    ("V7_fail_inv", [(FAILT, FAILT.replace("if (!cpu->memory_rw", "if (cpu->memory_rw"))], 15,
     "noT unimpl, noT chkstop (the zero-fill succeeds: the block's checkstop fallback runs, MSR 0) + " + W5RED.split(" (")[0] +
     " (the failing -T reads skip the block, F6; BUILD-DEPENDENT) + T ra pc nonex addr (as D15)", "the read's failure test inverted (F6)"),
]


def pretable(rows):
    head = [
        "PRETABLE_2 -- qhslowifetch detector, test-variant table 2.  Written BEFORE table 2 runs (this file's mtime precedes table2/'s).",
        "Instrument: table2/probe%d_frozen.py (%d rows; -E pmppc unmodified), frozen from regress/ppc_ifetch_probe.py.  Baseline: the" % (rows, rows),
        "final candidate, cpu_ppc_instr.c.fix3 + cpu_ppc.h.fix (TIE_FABLE.md T1: no MSR edit in arm (d); the ruled comments in).  The legs",
        "-- base, the HEAD leg (cpu_ppc_instr.c.HEAD + cpu_ppc.h.HEAD) and three null media -- run first, in the same clone.",
        "",
        "THE FOUR CHECKS: PRETABLE.out (table 1) with PRETABLE.errata.md, which corrects three of its sentences, still holds for the arm.",
        "What changed since, row by row: noT unimpl (want present) and noT chkstop (want absent) were ADDED (P9: D15 was a floor gap,",
        "undetected on the 50-row probe); T me chkstop was REMOVED (vacuous: ME set never reaches the checkstop text); five ISI rows, the",
        "two step-count rows and again nonex became CONTROLS (premise pins, not repair rows; P11).  The five `T ra` rows were ADDED",
        "after the window sweep (window_sweep.out) reached arm (a) on cpc700_pci: FINAL_FABLE.md F4 owed a read-ahead row with four",
        "pins -- the halt line's address, running 0 (the stop), pc after the batch, the halt count -- plus the session's survival.",
        "CHANNEL for the added rows: noT unimpl -- D15 and V7 (the zero word is never decoded: the block's checkstop fallback parks first);",
        "noT chkstop -- the same two (the fallback's text).  No other variant touches the no-T route: it never enters the failure arm.",
        "CHANNEL for T ra: session -- B1 (the exit fires inside the read-ahead); pc -- B1 (none), W2/D3 (walks on), W4 (0x400),",
        "D15/V7 (0xfec00004: the successful fetch checkstops); nonex -- W7/D5 (one: parked during read-ahead), W5/D7/D12 (garbage-",
        "translated slot), D4 (re-fetch loop), W2/D3 (walk); addr -- W2/D3 (later words), D12/D15/V7 (no halt); stopped -- B1, D12.",
        "",
        "SCOPE (FINAL_FABLE.md F8): table 1's eighteen, table 1b's two, and P15/F6's seven, all on ONE instrument; every SCORES line names",
        "its row count.  Predicted scores are %d minus the red count listed.  W5, D7 and V7 ride on the uninitialised instruction word (P25):" % rows,
        "their exact red rows are BUILD-DEPENDENT, and the claim is that SOME row reds, not which.",
        "",
        "VARIANTS (name, what, predicted red rows -> predicted score):",
    ]
    out = NL.join(head) + NL
    for n, _, k, pred, what in V:
        out += "   %-14s %-60s red: %s -> %d/%d%s" % (n, what[:60], pred, rows - k, rows, NL)
    out += "   HEAD leg       the pre-fix build                                            red: as B1 -> %d/%d, SYMPTOM=PRESENT%s" % (
        rows - dict((n, k) for n, _, k, _, _ in V)["B1_exit_head"], rows, NL)
    out += "   null media     /bin/true, an absent binary, /bin/false                      CONTROL=FAIL each" + NL
    return out


def main():
    a = sys.argv[1:]
    if a == ["list"]:
        print(" ".join(n for n, _, _, _, _ in V))
    elif len(a) == 2 and a[0] == "pretable":
        sys.stdout.write(pretable(int(a[1])))
    elif len(a) == 4 and a[0] == "apply":
        name, src, dst = a[1:]
        s = io.open(src, encoding="latin-1", newline="").read()
        f = dict((n, e) for n, e, _, _, _ in V)[name]
        if callable(f):
            try:
                s = f(s)
            except (AssertionError, ValueError) as e:
                print("MUTANT-TEXT-NOT-FOUND", name, e)
                sys.exit(3)
        else:
            for old, new in f:
                if s.count(old) != 1:
                    print("MUTANT-TEXT-NOT-FOUND", name, repr(old[:60]), s.count(old))
                    sys.exit(3)
                s = s.replace(old, new)
        io.open(dst, "w", encoding="latin-1", newline="").write(s)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
