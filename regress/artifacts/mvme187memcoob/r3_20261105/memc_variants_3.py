#!/usr/bin/env python3
"""memc_variants_3.py -- test-variant TABLE 3 for the mvme187memcoob detector (repair 3, the class closure), 2026-11-05, as ruled by
cloud Mythos 5.1 (p2r_20261105/ADJ_MYTHOS.md): table 2's 29 variants (memc_variants_2.py) plus the ruling's N1-N9, N19, N21 and the
cells it added -- the selector mask dropping each bit 0..7, the fold clear widened by each bit 0..6 (bit 7 is N4), the two hard-coded
access lengths, the idata-gated memconf latch and the default store mis-targeted into chipid.  Baseline: det_20261104/dev_mvme187.c.fix2
(== GXEMUL-SEC's dev_mvme187.c).  Instrument: the 118-row probe (table3/probe118_frozen.py).
  memc_variants_3.py list | apply <name> <in> <out> | pretable
Exact-string edits, each asserted once; every backslash is chr(92)."""
import importlib.util
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DET = os.path.join(os.path.dirname(HERE), "det_20261104")
spec = importlib.util.spec_from_file_location("mv2", os.path.join(DET, "memc_variants_2.py"))
mv2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mv2)
T, NL = chr(9), chr(10)
LATCH_M, SET_M, LATCH_D, SET_D, FOLD, SWITCH, CNF_W = mv2.LATCH_M, mv2.SET_M, mv2.LATCH_D, mv2.SET_D, mv2.FOLD, mv2.SWITCH, mv2.CNF_W
TEST = T + "if (relative_addr & 0x100) {" + NL
RDMAX = T * 2 + "idata = memory_readmax64(cpu, data, len);" + NL
WRMAX = T * 2 + "memory_writemax64(cpu, data, len, odata);" + NL
DEFKEEP = mv2.DEF_STORE


def ins_after(anchor, line):
    return [(anchor, anchor + line)]


NEW = [
    ("N1_mlatch_ctl0", [(LATCH_M, T * 3 + "if (!d->warned_memconf || controller == 0) {" + NL)],
     ["R3_lines", "R3_no_0x0"], "the memconf latch test bypassed on controller 0"),
    ("N2_mset_ctl0", [(SET_M, T * 4 + "if (controller == 0) d->warned_memconf = 1;" + NL)],
     ["R9_lines", "R9_no_0xff"], "the memconf latch set only on controller 0"),
    ("N3_dset_ctl0", [(SET_D, T * 3 + "if (controller == 0) d->warned_default = 1;" + NL)],
     ["R10_lines"], "the default latch set only on controller 0"),
    ("N4_fold_clr80", [(FOLD, FOLD.replace("~0x100", "~0x180"))], ["R11_180_r4"], "the fold clear widened by bit 7"),
    ("N5_fold_test80", [(TEST, TEST.replace("& 0x100", "& 0x180"))], ["R11_line_text"], "the fold test widened by bit 7"),
    ("N6_keep3", ins_after(CNF_W, T * 3 + "d->memcreg.memc_memconf = (d->memcreg.memc_memconf & ~3) | (idata & 3);" + NL),
     ["R3_108_r9", "R3_cnf0_r11"], "a memconf store keeps bits 0-1"),
    ("N6_keep1", ins_after(CNF_W, T * 3 + "d->memcreg.memc_memconf = (d->memcreg.memc_memconf & ~1) | (idata & 1);" + NL),
     ["R3_cnf0_r11"], "a memconf store keeps bit 0"),
    ("N6_keep2", ins_after(CNF_W, T * 3 + "d->memcreg.memc_memconf = (d->memcreg.memc_memconf & ~2) | (idata & 2);" + NL),
     ["R3_108_r9", "R3_cnf0_r11"], "a memconf store keeps bit 1"),
    ("N7_keep_ctl1", ins_after(CNF_W, T * 3 + "if (controller) d->memcreg.memc_memconf = idata;" + NL),
     ["R3_108_r9", "R3_cnf0_r11", "R9_108_r2", "R9_08_r4"], "a memconf store kept only through controller 1"),
    ("N8_defkeep_ctl1", [(LATCH_D, DEFKEEP.replace("if (relative_addr < sizeof(d->memcreg)) {",
                                                     "if (relative_addr < sizeof(d->memcreg) && controller) {") + LATCH_D)],
     ["R10_118_r6"], "a default store kept (and read back) only through controller 1"),
    ("N9a_cnf_chiprev", ins_after(CNF_W, T * 3 + "d->memcreg.memc_chiprev = idata;" + NL),
     ["R3_04_r13", "R12_04_r4"], "a memconf store mis-targeted into chiprev"),
    ("N9b_cnf_chipid", ins_after(CNF_W, T * 3 + "d->memcreg.memc_chipid = idata;" + NL),
     ["R3_00_r12", "R12_00_r2", "R12_w00_r6"], "a memconf store mis-targeted into chipid"),
    ("N9c_def_memconf", [(LATCH_D, T * 2 + "if (writeflag == MEM_WRITE) d->memcreg.memc_memconf = idata;" + NL + LATCH_D)],
     ["R10_08_r8"], "a default store mis-targeted into memconf"),
    ("N9d_def_chipid", [(LATCH_D, T * 2 + "if (writeflag == MEM_WRITE) d->memcreg.memc_chipid = idata;" + NL + LATCH_D)],
     ["R10_00_r9"], "a default store mis-targeted into chipid (change 3)"),
    ("N19_keep_latched", [(SET_M + T * 3 + "}" + NL, SET_M + T * 3 + "} else" + NL + T * 4 + "d->memcreg.memc_memconf = idata;" + NL)],
     ["R3_108_r9", "R3_cnf0_r11", "R9_108_r2", "R9_08_r4"], "a memconf store kept once the latch is set"),
    ("N21_sel_fc", [(SWITCH, SWITCH.replace("switch (relative_addr)", "switch (relative_addr & 0xfc)"))],
     ["R11_01_r5", "R11_0a_r6", "R11_101_r7", "R11_102_r8"], "the selector made word-granular (bits 0 and 1 dropped)"),
    ("WLEN1", [(WRMAX, WRMAX.replace("len, odata", "1, odata"))], ["R12_w00_r6", "R12_h08_r7"],
     "the read write-back length hard-coded to 1"),
    ("RLEN1", [(RDMAX, RDMAX.replace("data, len)", "data, 1)"))], ["R12_cnf_line"], "the store read length hard-coded to 1"),
    ("IDATA_GATE", [(LATCH_M, T * 3 + "if (!d->warned_memconf && idata) {" + NL)], ["R9_cnf_line", "R9_no_0xff"],
     "the memconf latch test gated on a nonzero value (change 5)"),
]
SEL_PRED = {0: ["R11_01_r5", "R11_101_r7"], 1: ["R11_0a_r6", "R11_102_r8"], 5: ["R11_20_r11", "R11_120_r9"],
            6: ["R11_40_r12", "R11_140_r10"], 7: ["R8_80_r8", "R8_84_r12", "R11_180_r4"]}
SEL_ATLEAST = {2: ["ctl_chiprev_r2", "R6_04"], 3: ["ctl_memconf_r2", "R6_08"], 4: ["R5_r2", "R10_18_r7"]}
for b in range(8):
    m = 0xff & ~(1 << b)
    pred = SEL_PRED.get(b, SEL_ATLEAST.get(b))
    NEW.append(("SEL_b%d" % b, [(SWITCH, SWITCH.replace("switch (relative_addr)", "switch (relative_addr & 0x%02x)" % m))],
                pred, "the selector drops bit %d%s" % (b, " (at least these rows)" if b in SEL_ATLEAST else "")))
FCL_PRED = {0: ["R11_101_r7"], 1: ["R11_102_r8"], 5: ["R11_120_r9"], 6: ["R11_140_r10"]}
FCL_ATLEAST = {2: ["R6_104", "R7_r2"], 3: ["R3_108_r9", "R6_108"], 4: ["R10_118_r6"]}
for b in range(7):
    pred = FCL_PRED.get(b, FCL_ATLEAST.get(b))
    NEW.append(("FCL_b%d" % b, [(FOLD, FOLD.replace("~0x100", "~0x%x" % (0x100 | (1 << b))))],
                pred, "the fold clear widened by bit %d%s" % (b, " (at least these rows)" if b in FCL_ATLEAST else "")))
ATLEAST = set(["SEL_b2", "SEL_b3", "SEL_b4", "FCL_b2", "FCL_b3", "FCL_b4"])
V = [(n, e, None, None, what) for n, e, _, _, what in mv2.V] + [(n, e, p, None, w) for n, e, p, w in NEW]


def measured2():
    out = {}
    for line in io.open(os.path.join(DET, "table2", "SCORES.txt"), encoding="utf-8"):
        p = line.split()
        if len(p) > 1 and "RED=" in line:
            red = line.rsplit("RED=", 1)[1].strip()
            out[p[0]] = [] if red == "none" else red.split(",")
    return out


def pretable():
    m2 = measured2()
    head = [
        "PRETABLE_3 -- mvme187memcoob detector, test-variant table 3.  Written BEFORE table 3 runs (this file's mtime precedes table3/'s).",
        "Instrument: table3/probe118_frozen.py (118 rows: 74 + R3's five, R7 pc, R9 7, R10 9, R11 13, R12 9), frozen from",
        "regress/mvme187_memc_probe.py with the repair-3 edits; base run on the fixed build tree: 118/118 (r3_20261105/base118_build.out).",
        "Baseline: det_20261104/dev_mvme187.c.fix2 (== GXEMUL-SEC).  Legs first in the same clone: base, HEAD, three null media.",
        "",
        "THE FOUR CHECKS for the added rows (ADJ_MYTHOS.md, the ruling of record):",
        "  SIBLING PARITY -- controller 0 and controller 1 now each carry a first-access session for both latches (R3/R9 memconf, R4/R10",
        "    default), and both store categories are followed by reads of every served field (R3 memconf store; R10 default store; R12 the",
        "    served-offset stores).",
        "  CLAIM -> ROW -- 'keeps no store' -> R3 108/cnf0, R9 108/08, R10 118/18, R12 00/04/08; 'announces each category once per device'",
        "    -> R3/R9/R10/R11/R12 lines and the 'no' fragments; the notice tails -> the fragments now run to ' (once) ]'; width -> R12 w00/h08",
        "    and R12 cnf line.",
        "  GUARD FIELD vs BODY FIELD -- the function reads relative_addr (before and after the fold), writeflag, len, idata and the two",
        "    latches; the partitions the body tests: the fold bit (0x100), the switch's case labels, writeflag, the latch bits, and (by the",
        "    ruling) len and idata == 0 for the memconf latch.  Every cell of {controller 0, 1} x {latch test, latch set, store kept} x {memconf,",
        "    default} has a first-access session; the fold-clear and selector masks are walked bit by bit (R11, R8, the served reads).",
        "  CHANNEL -- per new variant below: the row named is the one whose value or text differs under it.",
        "",
        "PREDICTIONS.  The ruling's new variants are predicted row by row (exact red sets; 'at least' where a bit moves many served reads).",
        "Table 2's 29 variants are predicted AT LEAST their measured 74-row red sets (det_20261104/table2/SCORES.txt); their reds on the 44",
        "new rows are informational (each was already detected on table 2; re-running them on the 118-row instrument is a regression check).",
        "",
        "VARIANTS (name, what, predicted red rows):",
    ]
    out = NL.join(head) + NL
    for n, _, pred, _, what in V:
        if pred is None:
            r = m2.get(n, [])
            out += "   %-17s %-56s at least: %s%s" % (n, what[:56], ",".join(r) if r else "none (table 2: green)", NL)
        else:
            tag = "at least: " if n in ATLEAST else "exactly: "
            out += "   %-17s %-56s %s%s -> %s/118%s" % (n, what[:56], tag, ",".join(pred), ("<=" if n in ATLEAST else "") + str(118 - len(pred)), NL)
    out += "   HEAD leg          the pre-fix build                                        at least: table 2's HEAD set; SYMPTOM=PRESENT" + NL
    out += "   null media        /bin/true, an absent binary, /bin/false                  CONTROL=FAIL each" + NL
    return out


def main():
    a = sys.argv[1:]
    if a == ["list"]:
        print(" ".join(n for n, _, _, _, _ in V))
    elif a == ["pretable"]:
        sys.stdout.write(pretable())
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
