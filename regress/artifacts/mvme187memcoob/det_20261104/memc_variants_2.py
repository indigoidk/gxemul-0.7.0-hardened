#!/usr/bin/env python3
"""memc_variants_2.py -- test-variant TABLE 2 for the mvme187memcoob detector, 2026-11-05, as ruled by the pass-2 adjudication
(adj_20261104/ADJ_MYTHOS.md, the adjudicator; ADJ_OPUS.md, grok and glm-5.3 confirming).  Table 1's nineteen (M20: rerun on the
74-row instrument so every score line names 74) and the ten the adjudication added, each prefixed T2_ so its name cannot collide
with the reconciliation's D-numbers (M8): the chipid mirror of D9 (M8), the value-print guard dropped (M1), the memconf latch made
per-controller (M2) and grok's controller-qualified form (M23), the memconf notice's controller replaced by 0 (M5), the memconf
latch set on reads (M25), a served read setting the default latch in case 0x00, case 0x04 and the memconf read path (M26, X1),
and a memconf store that keeps the bits above the size code (M27).  Baseline: dev_mvme187.c.fix2, the final candidate (the ruled
M4/M6b/M21 comments in; comment-only different from table 1's .fix).
  memc_variants_2.py list | apply <name> <in> <out> | pretable <rows>
Exact-string edits, each asserted once; every backslash is chr(92)."""
import io
import sys

T = chr(9)
NL = chr(10)
BS = chr(92)

FOLD = T * 2 + "relative_addr &= ~0x100;" + NL
CTRL = T * 2 + "controller = 1;" + NL
SWITCH = T + "switch (relative_addr) {" + NL
CHIPID = T * 2 + "odata = d->memcreg.memc_chipid;" + NL
CHIPREV = T * 2 + "odata = d->memcreg.memc_chiprev;" + NL
CNF_RD = T * 2 + "odata = d->memcreg.memc_memconf;" + NL
CNF_W = T * 2 + "if (writeflag == MEM_WRITE) {" + NL
STRUCT_M = T + "int" + T * 3 + "warned_memconf;" + NL
LATCH_M = T * 3 + "if (!d->warned_memconf) {" + NL
SET_M = T * 4 + "d->warned_memconf = 1;" + NL
MNOTE = T * 4 + '    " (once) ]' + BS + 'n", (int)idata, controller);' + NL
CASE08_END = T * 3 + "}" + NL + T * 2 + "}" + NL + T * 2 + "break;" + NL + NL + T + "default:" + NL
LATCH_D = T * 2 + "if (!d->warned_default) {" + NL
SET_D = T * 3 + "d->warned_default = 1;" + NL
DVAL = T * 3 + "if (writeflag == MEM_WRITE)" + NL + T * 4 + 'fatal(": 0x%x", (int)idata);' + NL
RW = '"write to" : "read from"'
HEAD_CNF = (T * 3 + 'fatal("mvme187_memc: Write to relative_addr %i (controller %i) not yet"' + NL +
            T * 3 + '    " implemented!' + BS + 'n", (int)relative_addr, controller);' + NL + T * 3 + "exit(1);" + NL)
HEAD_DEF = (T * 2 + 'fatal("[ mvme187_memc: unimplemented %s offset 0x%x",' + NL +
            T * 2 + '    writeflag == MEM_WRITE? "write to" : "read from",' + NL +
            T * 2 + '    (int) relative_addr);' + NL + T * 2 + "if (writeflag == MEM_WRITE)" + NL +
            T * 3 + 'fatal(": 0x%x", (int)idata);' + NL + T * 2 + 'fatal(" ]' + BS + 'n");' + NL + T * 2 + "exit(1);" + NL)
HEAD_IDX = T + "odata = ((uint8_t*)&d->memcreg)[relative_addr];" + NL + NL
DEF_STORE = (T * 2 + "if (relative_addr < sizeof(d->memcreg)) {" + NL +
             T * 3 + "if (writeflag == MEM_WRITE)" + NL + T * 4 + "((uint8_t*)&d->memcreg)[relative_addr] = idata;" + NL +
             T * 3 + "odata = ((uint8_t*)&d->memcreg)[relative_addr];" + NL + T * 2 + "}" + NL)

R8ALL = "R8 session, the twelve byte rows, R8 pc, R8 lines"
V = [
    ("B1_cnf_exit", [(LATCH_M, HEAD_CNF + LATCH_M)], 28,
     "wr cnf session prompt; R3 session cnf r2 7c r4 pc lines cnf line 7c line; R7 session r2 108 r4 cnf line (R7 lines stays 2: "
     "the exit text carries the tag); " + R8ALL + " (R8's first access exits)", "(b) the memconf store's fatal()+exit(1), verbatim"),
    ("B2_def_exit", [(LATCH_D, HEAD_DEF + LATCH_D)], 44,
     "rd 0x0c/0x7c/0xff session+prompt; R3 session cnf r2 7c r4 pc 7c line; R4 session 00 r7 04 r8 0c 7c ff 10c pc line text; "
     "R5 session r2 pc line text; R7 session r2 108 r4 lines line text cnf line; R8 session, twelve bytes, pc (R8 lines stays 2)",
     "(b) the default arm's fatal()+exit(1), verbatim"),
    ("B3_idx_read", [(SWITCH, HEAD_IDX + SWITCH)], 3,
     "R3 7c r4, R8 7c r4, R8 80 r8 (x86_64, little-endian: each latch's low byte reads 1; big-endian would red R8 7f r7 and 83 r11 "
     "instead); R4 ff and R8 84..87 read past the 132-byte allocation and are INDETERMINATE (F2)",
     "(b) the indexed read before the switch, verbatim"),
    ("A_cnf_accept", [(CNF_W, CNF_W + T * 3 + "d->memcreg.memc_memconf = idata;" + NL)], 1,
     "R3 cnf r2 (0xff, not 0x3)", "ACCEPT: the memconf store is kept"),
    ("F_def_fault", [(LATCH_D, T * 2 + "return 0;" + NL + LATCH_D)], 34,
     "R3 7c r4 pc lines 7c line; R4 0c 7c ff 10c pc lines line text; R5 r2 pc lines line text; R7 r2 108 r4 lines line text cnf "
     "line; R8 twelve bytes, pc, lines (the faulting access and everything after it in each session)", "FAULT: the default arm fails the access"),
    ("D1_mlatch_inv", [(LATCH_M, LATCH_M.replace("!d->warned_memconf", "d->warned_memconf"))], 5,
     "R3 lines, R3 cnf line, R7 lines, R7 cnf line, R8 lines", "(d) the memconf latch test inverted"),
    ("D2_mlatch_noset", [(SET_M, "")], 2, "R3 lines (3), R3 no 0x5", "(d) the memconf latch never set"),
    ("D3_shared_latch", [(LATCH_M, LATCH_M.replace("warned_memconf", "warned_default")), (SET_M, SET_M.replace("warned_memconf", "warned_default"))],
     5, "R3 lines, R3 7c line, R7 lines, R7 cnf line, R8 lines", "(d) one shared latch for both categories"),
    ("D4_dlatch_inv", [(LATCH_D, LATCH_D.replace("!d->warned_default", "d->warned_default"))], 9,
     "R3 lines, R3 7c line, R4 lines, R4 line text, R5 lines, R5 line text, R7 lines, R7 line text, R8 lines",
     "(d) the default latch test inverted"),
    ("D5_dlatch_noset", [(SET_D, "")], 3, "R4 lines (4), R5 lines (3), R8 lines (14)", "(d) the default latch never set"),
    ("D6_dlatch_ctrl", [(LATCH_D, T * 2 + "if (!d->warned_default || controller) {" + NL)], 2,
     "R4 lines (2), R5 lines (2)", "(d) the default latch made per-controller"),
    ("D7_fold", [(FOLD, FOLD.replace("~0x100", "~0x80"))], 9,
     "ctl ctl1id r2, R6 100 104 108, R6 lines, R7 line text, R7 108 r4, R7 lines, R7 cnf line", "(d) the fold mask narrowed"),
    ("D8_ctrl_drop", [(CTRL, "")], 2, "R7 line text, R7 cnf line (both name controller 0)", "(d) the controller number never set"),
    ("D9_chiprev_swap", [(CHIPREV, CHIPREV.replace("memc_chiprev", "memc_chipid"))], 4,
     "ctl chiprev r2, R6 04, R6 104, R4 04 r8", "mis-split field read: chiprev returns chipid"),
    ("D10_cnf_noread", [(CNF_RD, "")], 5,
     "ctl memconf r2, R3 cnf r2, R6 08, R6 108, R7 108 r4", "memconf's read arm loses its field read"),
    ("D11_cnf_on_read", [(CNF_W, CNF_W.replace("MEM_WRITE", "MEM_READ"))], 4,
     "R3 cnf line, R6 lines, R7 cnf line, R8 lines", "(d) the memconf announce keyed on reads, not writes"),
    ("D12_def_store", [(LATCH_D, DEF_STORE + LATCH_D)], 1, "R5 r2 (0x5a)", "a default-arm store kept and read back"),
    ("D13_def_noval", [(DVAL, "")], 1, "R5 line text", "the write notice drops its value"),
    ("D14_rw_swap", [(RW, '"read from" : "write to"')], 4,
     "R3 7c line, R4 line text, R5 line text, R7 line text", "(d) the notice's direction swapped"),
    ("T2_D9b_chipid_swap", [(CHIPID, CHIPID.replace("memc_chipid", "memc_chiprev"))], 5,
     "ctl chipid r2, ctl ctl1id r2, R6 00, R6 100, R4 00 r7", "M8: chipid returns chiprev (D9's mirror)"),
    ("T2_valprint", [(DVAL, T * 3 + 'fatal(": 0x%x", (int)idata);' + NL)], 3,
     "R3 7c line, R4 line text, R7 line text (a read notice gains ': 0x0' before ' (once) ]')", "M1: the value print unguarded"),
    ("T2_mlatch_perctl", [(STRUCT_M, T + "int" + T * 3 + "warned_memconf[2];" + NL),
                          (LATCH_M, T * 3 + "if (!d->warned_memconf[controller]) {" + NL),
                          (SET_M, T * 4 + "d->warned_memconf[controller] = 1;" + NL)], 2,
     "R3 no 0x5, R3 lines (3)", "M2: the memconf latch made per-controller (D6's mirror)"),
    ("T2_mlatch_ctl1", [(LATCH_M, T * 3 + "if (!d->warned_memconf || controller != 0) {" + NL)], 2,
     "R3 no 0x5, R3 lines (3)", "M23: the memconf latch test qualified by controller"),
    ("T2_mnotice_ctl0", [(MNOTE, MNOTE.replace("(int)idata, controller);", "(int)idata, 0);"))], 1,
     "R7 cnf line (names controller 0)", "M5: the memconf notice's controller argument replaced by 0"),
    ("T2_mlatch_hoist", [(SET_M, ""), (CASE08_END, T * 3 + "}" + NL + T * 2 + "}" + NL + T * 2 + "d->warned_memconf = 1;" + NL +
                                                   T * 2 + "break;" + NL + NL + T + "default:" + NL)], 2,
     "R7 lines (1), R7 cnf line (its memconf load sets the latch first)", "M25: the memconf latch set on every access, reads too"),
    ("T2_dlatch_rd00", [(CHIPID, CHIPID + T * 2 + "d->warned_default = 1;" + NL)], 2,
     "R4 lines (0), R4 line text", "M26: a served chipid access sets the default latch"),
    ("T2_dlatch_rd04", [(CHIPREV, CHIPREV + T * 2 + "d->warned_default = 1;" + NL)], 2,
     "R4 lines (0), R4 line text", "M26: a served chiprev access sets the default latch"),
    ("T2_dlatch_rd08", [(CNF_RD, CNF_RD + T * 2 + "if (writeflag == MEM_READ)" + NL + T * 3 + "d->warned_default = 1;" + NL)], 2,
     "R3 lines (1), R3 7c line (X1: R3's memconf load precedes its +0x7c load)", "X1: a memconf read sets the default latch"),
    ("T2_keepstore", [(CNF_W, CNF_W + T * 3 + "d->memcreg.memc_memconf = (d->memcreg.memc_memconf & 7) | (idata & ~7);" + NL)], 1,
     "R3 cnf r2 (0xfb: 0xff's bits above the size code kept)", "M27: a memconf store keeps the bits above the size code"),
]


def pretable(rows):
    head = [
        "PRETABLE_2 -- mvme187memcoob detector, test-variant table 2.  Written BEFORE table 2 runs (this file's mtime precedes table2/'s).",
        "Instrument: table2/probe%d_frozen.py (%d rows; -E mvme88k -e mvme187 -M 64 unmodified), frozen from regress/mvme187_memc_probe.py" % (rows, rows),
        "after its first run on the fixed build (fixed_first74.out: 74/74, CONTROL=OK, SYMPTOM=ABSENT, ASAN=0).  Baseline: the final",
        "candidate, dev_mvme187.c.fix2 (comment-only different from table 1's .fix: ADJ_MYTHOS M4/M6b/M21).  The legs -- base, the HEAD leg",
        "(dev_mvme187.c.HEAD) and three null media -- run first, in the same clone.",
        "",
        "THE FOUR CHECKS: PRETABLE.out (table 1) still holds for the arms; what changed is the rows (adj_20261104/ADJ_MYTHOS.md):",
        "  ADDED -- R4 00 r7 and R4 04 r8 (two served loads first: no served read may set the default latch, M26/X1); R7 108 r4 and R7 cnf",
        "  line (R7 is now a controller-1 default load, memconf load and memconf store: M5, M25); R8's fifteen (both latches set, then the",
        "  twelve bytes past memcreg: B3 on either byte order, M3/X5).  CHANGED -- R3's first store writes 0xff (M27) and its fourth goes",
        "  through controller 1 (M2/M23); the read notices' fragments run to ' (once) ]' (M1); R4 pc wants CODE + 24.  DROPPED -- `asan",
        "  reports` (M9: it cannot fail on the gate's plain build; MVME187_MEMC_ASAN is now informational).  RECLASSIFIED -- the four ctl",
        "  r2 rows are detector rows, not controls (M12): the nine CONTROL rows are neg apparatus and the ctl sess/pc rows.",
        "  CHANNEL for the new rows: R4 00 r7 / 04 r8 -- D9b, D9 (a wrong field read); R7 108 r4 -- D7, D10; R7 cnf line -- T2_mnotice_ctl0,",
        "  T2_mlatch_hoist, D1, D3, D7, D8, D11 (the memconf notice's presence and controller); R8 bytes -- B3 (the latches forwarded);",
        "  R8 lines -- D1, D3, D4, D5, D11 (one announce per category over fourteen accesses).",
        "",
        "SCOPE (ADJ_MYTHOS.md M20, X7): table 1's nineteen rerun on this instrument, and the ten added; every SCORES line names its row",
        "count.  Predicted scores are %d minus the red count listed.  B3's rows at +0x84..+0x87 and R4 ff read past the allocation under" % rows,
        "B3 and are INDETERMINATE there (F2): the prediction counts only the three latch rows.",
        "",
        "VARIANTS (name, what, predicted red rows -> predicted score):",
    ]
    out = NL.join(head) + NL
    for n, _, k, pred, what in V:
        out += "   %-18s %-56s red: %s -> %d/%d%s" % (n, what[:56], pred, rows - k, rows, NL)
    out += "   HEAD leg           the pre-fix build                                        red: 49 -> %d/%d, SYMPTOM=PRESENT%s" % (
        rows - 49, rows, NL)
    out += "   null media         /bin/true, an absent binary, /bin/false                  CONTROL=FAIL each" + NL
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
        for old, new in dict((n, e) for n, e, _, _, _ in V)[name]:
            if s.count(old) != 1:
                print("MUTANT-TEXT-NOT-FOUND", name, repr(old[:60]), s.count(old))
                sys.exit(3)
            s = s.replace(old, new)
        io.open(dst, "w", encoding="latin-1", newline="").write(s)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
