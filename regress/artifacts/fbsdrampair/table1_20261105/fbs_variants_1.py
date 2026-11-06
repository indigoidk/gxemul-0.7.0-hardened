#!/usr/bin/env python3
"""fbs_variants_1.py -- fbsdrampair test-variant TABLE 1 (2026-11-05).

Each variant is ONE exact-text replacement against dev_footbridge.c.fix1 (the named baseline: the GXEMUL-SEC
working copy at HEAD edb3213f plus the fbsdrampair fix, md5 ccaf09d4), refused unless its find-text occurs
EXACTLY ONCE in the input.  Two replace one contiguous span (d_exchanged, d_backing_*) -- still one
replacement.  Predictions are EXACT red-row sets for the 56-row probe (probe56_frozen.py); [] means GREEN.

  fbs_variants_1.py list                      the variant names, one per line, in table order
  fbs_variants_1.py apply <name> <in> <out>   write variant <name> of <in> to <out>
  fbs_variants_1.py check <dir>               apply every variant to fix1 into <dir>, report each
  fbs_variants_1.py pretable                  print PRETABLE_1.out (static sections + predictions)
  fbs_variants_1.py compare <SCORES.txt>      predictions against measurements, MATCH / MISS per line
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FIX1 = os.path.join(HERE, "dev_footbridge.c.fix1")
TAB, NL, BS = chr(9), chr(10), chr(92)

L1M = TAB * 3 + "if (!d->warned_sdram_mask_r) {" + NL
L2M = TAB * 4 + "d->warned_sdram_mask_r = 1;" + NL
L1O = TAB * 3 + "if (!d->warned_sdram_offset_r) {" + NL
L2O = TAB * 4 + "d->warned_sdram_offset_r = 1;" + NL
F2 = TAB * 4 + '    "declined, reads 0 (written values are "' + NL
F3 = TAB * 4 + '    "not kept) (once) ]' + BS + 'n");' + NL
MASK_FATAL = TAB * 4 + 'fatal("[ footbridge: read of sdram_ba_mask "' + NL + F2 + F3
OFF_FATAL = TAB * 4 + 'fatal("[ footbridge: read of sdram_ba_offset "' + NL + F2 + F3
CLOSE = TAB * 3 + "}" + NL
MASK_LATCH = L1M + L2M + MASK_FATAL + CLOSE
OFF_LATCH = L1O + L2O + OFF_FATAL + CLOSE
MASK_GUARD = TAB + "case SDRAM_BA_MASK:" + NL + TAB * 2 + "if (writeflag == MEM_READ) {" + NL
OFF_GUARD = TAB + "case SDRAM_BA_OFFSET:" + NL + TAB * 2 + "if (writeflag == MEM_READ) {" + NL
MASK_ELSE = TAB * 2 + "} else {" + NL + TAB * 3 + "switch (idata) {" + NL
OFF_ELSE = TAB * 2 + "} else {" + NL + TAB * 3 + "if (idata != 0)" + NL
OLD_MASK = (TAB * 3 + 'fatal("[ footbridge read from sdram_ba_mask ]' + BS + 'n");' + NL
            + TAB * 3 + "exit(1);" + NL)          # HEAD's two lines, verbatim
OLD_OFF = (TAB * 3 + 'fatal("[ footbridge read from sdram_ba_offset ]' + BS + 'n");' + NL
           + TAB * 3 + "exit(1);" + NL)
VALUE = TAB * 3 + "odata = SDRAM_MASK_16MB;" + NL         # the blank-ROM 0x00FC0000 the RESET rulings wanted


def one(s, old, new):
    n = s.count(old)
    if n != 1:
        raise SystemExit("REFUSED: find-text occurs %d times, want exactly 1: %r" % (n, old[:70]))
    return s.replace(old, new)


def guard(s, which, cond):
    g = MASK_GUARD if which == "mask" else OFF_GUARD
    return one(s, g, g.replace("writeflag == MEM_READ", cond))


def exchanged(s):
    a, b = s.index(L1M), s.index(L2O) + len(L2O)
    span = s[a:b]
    assert span.count("warned_sdram_mask_r") == 2 and span.count("warned_sdram_offset_r") == 2, "span"
    new = span.replace("warned_sdram_mask_r", "@M@").replace("warned_sdram_offset_r", "warned_sdram_mask_r")
    return one(s, span, new.replace("@M@", "warned_sdram_offset_r"))


#  (name, edit, what it is)
V = [
    ("b_exit_mask", lambda s: one(s, MASK_LATCH, OLD_MASK),
     "clause (b): HEAD's fatal()+exit(1) reinstated verbatim at +0x100"),
    ("b_exit_offset", lambda s: one(s, OFF_LATCH, OLD_OFF),
     "clause (b): HEAD's fatal()+exit(1) reinstated verbatim at +0x104"),
    ("b_exitkept_mask", lambda s: one(s, MASK_FATAL, MASK_FATAL + TAB * 4 + "exit(1);" + NL),
     "exit(1) kept after the NEW announce at +0x100"),
    ("d_latchnever_mask", lambda s: one(s, L2M, ""), "the mask latch never set"),
    ("d_latchnever_offset", lambda s: one(s, L2O, ""), "the offset latch never set"),
    ("d_latchpass_mask", lambda s: one(s, L1M, TAB * 3 + "if (1) {" + NL), "mask latch test always passes"),
    ("d_latchpass_offset", lambda s: one(s, L1O, TAB * 3 + "if (1) {" + NL), "offset latch test always passes"),
    ("d_latchinv_mask", lambda s: one(s, L1M, L1M.replace("(!d->", "(d->")), "mask latch test inverted"),
    ("d_latchinv_offset", lambda s: one(s, L1O, L1O.replace("(!d->", "(d->")), "offset latch test inverted"),
    ("d_shared_offusesmask", lambda s: one(s, L1O + L2O, L1M + L2M),
     "latch collision: the offset arm tests and sets the MASK latch"),
    ("d_shared_maskusesoff", lambda s: one(s, L1M + L2M, L1O + L2O),
     "latch collision: the mask arm tests and sets the OFFSET latch"),
    ("d_setswap_mask", lambda s: one(s, L2M, L2O), "the mask arm sets the OFFSET latch (tests its own)"),
    ("d_setswap_offset", lambda s: one(s, L2O, L2M), "the offset arm sets the MASK latch (tests its own)"),
    ("d_exchanged", exchanged, "both arms use the other's latch consistently (a renaming)"),
    ("d_value_mask", lambda s: one(s, L1M, VALUE + L1M), "declined value 0x00FC0000 at +0x100 (outside the latch)"),
    ("d_value_offset", lambda s: one(s, L1O, VALUE + L1O), "declined value 0x00FC0000 at +0x104 (outside the latch)"),
    ("d_value_inlatch_mask", lambda s: one(s, L2M, L2M + TAB + VALUE),
     "0x00FC0000 assigned INSIDE the mask latch (first read only)"),
    ("d_predinv_mask", lambda s: guard(s, "mask", "writeflag != MEM_READ"), "mask read predicate inverted"),
    ("d_predinv_offset", lambda s: guard(s, "offset", "writeflag != MEM_READ"), "offset read predicate inverted"),
    ("d_predalways_mask", lambda s: guard(s, "mask", "1"), "mask read predicate always true"),
    ("d_predalways_offset", lambda s: guard(s, "offset", "1"), "offset read predicate always true"),
    ("d_prednever_mask", lambda s: guard(s, "mask", "writeflag == MEM_READ && relative_addr != SDRAM_BA_MASK"),
     "mask read predicate never true (relative_addr conditioning)"),
    ("d_prednever_offset",
     lambda s: guard(s, "offset", "writeflag == MEM_READ && relative_addr != SDRAM_BA_OFFSET"),
     "offset read predicate never true (relative_addr conditioning)"),
    ("d_predlatch_mask", lambda s: guard(s, "mask", "writeflag == MEM_READ && !d->warned_sdram_mask_r"),
     "mask read predicate qualified by its latch"),
    ("d_predlatch_offset", lambda s: guard(s, "offset", "writeflag == MEM_READ && !d->warned_sdram_offset_r"),
     "offset read predicate qualified by its latch"),
    ("d_predorlatch_mask", lambda s: guard(s, "mask", "writeflag == MEM_READ || d->warned_sdram_mask_r"),
     "mask read predicate widened by its latch (a write after a read takes the read path)"),
    ("d_predorlatch_offset", lambda s: guard(s, "offset", "writeflag == MEM_READ || d->warned_sdram_offset_r"),
     "offset read predicate widened by its latch"),
    ("d_opswap_mask", lambda s: guard(s, "mask", "d->warned_sdram_mask_r == MEM_READ"),
     "clause (d) operand swap: writeflag -> the body-read mask latch"),
    ("d_opswap_offset", lambda s: guard(s, "offset", "d->warned_sdram_offset_r == MEM_READ"),
     "clause (d) operand swap: writeflag -> the body-read offset latch"),
    ("d_predlen_mask", lambda s: guard(s, "mask", "writeflag == MEM_READ && len == 4"),
     "a width conjunct on the mask read predicate"),
    ("d_announcedel_mask", lambda s: one(s, MASK_FATAL, ""), "the mask announce removed (latch kept)"),
    ("d_announcedel_offset", lambda s: one(s, OFF_FATAL, ""), "the offset announce removed (latch kept)"),
    ("d_oldtext_mask",
     lambda s: one(s, MASK_FATAL, TAB * 4 + 'fatal("[ footbridge read from sdram_ba_mask ]' + BS + 'n");' + NL),
     "HEAD's exit text kept at +0x100 WITHOUT the exit"),
    ("d_misname_mask", lambda s: one(s, 'fatal("[ footbridge: read of sdram_ba_mask "',
                                     'fatal("[ footbridge: read of sdram_ba_offset "'),
     "the mask arm prints the OFFSET's text"),
    ("d_earlyret_mask", lambda s: one(s, CLOSE + MASK_ELSE, CLOSE + TAB * 3 + "return 1;" + NL + MASK_ELSE),
     "the mask decline returns early (skips the common tail)"),
    ("d_earlyret_offset", lambda s: one(s, CLOSE + OFF_ELSE, CLOSE + TAB * 3 + "return 1;" + NL + OFF_ELSE),
     "the offset decline returns early"),
    ("d_wsetlatch_mask", lambda s: one(s, MASK_ELSE, TAB * 2 + "} else {" + NL + TAB * 3
                                       + "d->warned_sdram_mask_r = 1;" + NL + TAB * 3 + "switch (idata) {" + NL),
     "the mask WRITE path sets the read latch"),
    ("d_wsetlatch_offset", lambda s: one(s, OFF_ELSE, TAB * 2 + "} else {" + NL + TAB * 3
                                         + "d->warned_sdram_offset_r = 1;" + NL + TAB * 3 + "if (idata != 0)" + NL),
     "the offset WRITE path sets the read latch"),
    ("d_backing_mask", lambda s: one(s, MASK_LATCH + MASK_ELSE, TAB * 3 + "odata = d->fiq_status;" + NL + MASK_LATCH
                                     + TAB * 2 + "} else {" + NL + TAB * 3 + "d->fiq_status = idata;" + NL
                                     + TAB * 3 + "switch (idata) {" + NL),
     "a written mask value KEPT and returned (fiq_status as storage: no SDRAM arm reads FIQ)"),
    ("d_backing_offset", lambda s: one(s, OFF_LATCH + OFF_ELSE, TAB * 3 + "odata = d->fiq_status;" + NL + OFF_LATCH
                                       + TAB * 2 + "} else {" + NL + TAB * 3 + "d->fiq_status = idata;" + NL
                                       + TAB * 3 + "if (idata != 0)" + NL),
     "a written offset value KEPT and returned"),
]
NAMES = [n for n, _f, _d in V]
EDIT = dict((n, f) for n, f, _d in V)
DESC = dict((n, d) for n, _f, d in V)

ROWS = ("C1 C2 C3 C4 C5 A1 A2 A2b I1 H1 H2 SC1 SA1 S1 S2 S3 S4 S5 SF1 SF2 N1 N2 N3 N4 N5 N0 NO EC1 EA1 "
        "E0 E1 E2 E3 E6 E5 E4 MC M1 M2 M3 OC O1 O2 O3 XC X1 WC W1 W2 BC B1 B2 B3 UC U1 D1").split()
assert len(ROWS) == 56
ALL_BUT_D1 = [r for r in ROWS if r != "D1"]

P = {
    "b_exit_mask": "B1 B2 B3 M1 M2 M3 X1",
    "b_exit_offset": "B1 B2 B3 O1 O2 O3 X1",
    "b_exitkept_mask": "B1 B2 B3 M1 M2 X1",
    "d_latchnever_mask": "M3 X1",
    "d_latchnever_offset": "O3 X1",
    "d_latchpass_mask": "M3 X1",
    "d_latchpass_offset": "O3 X1",
    "d_latchinv_mask": "B1 M3 X1",
    "d_latchinv_offset": "B2 O3 X1",
    "d_shared_offusesmask": "B2 X1",
    "d_shared_maskusesoff": "B2 X1",
    "d_setswap_mask": "B2 M3 X1",
    "d_setswap_offset": "O3 X1",
    "d_exchanged": "",
    "d_value_mask": "B1 M2",
    "d_value_offset": "B2 O2",
    "d_value_inlatch_mask": "B1 M2",
    "d_predinv_mask": "B3 M3 W1 W2 X1",
    "d_predinv_offset": "B3 O3 W1 W2 X1",
    "d_predalways_mask": "B3 W1 W2",
    "d_predalways_offset": "B3 W1 W2",
    "d_prednever_mask": "B1 M3 X1",
    "d_prednever_offset": "B2 O3 X1",
    "d_predlatch_mask": "",
    "d_predlatch_offset": "",
    "d_predorlatch_mask": "B3",
    "d_predorlatch_offset": "B3",
    "d_opswap_mask": "W1",
    "d_opswap_offset": "W1",
    "d_predlen_mask": "",
    "d_announcedel_mask": "B1 M3 X1",
    "d_announcedel_offset": "B2 O3 X1",
    "d_oldtext_mask": "B1 M3 X1",
    "d_misname_mask": "B1 B2 M3 X1",
    "d_earlyret_mask": "",
    "d_earlyret_offset": "",
    "d_wsetlatch_mask": "B1",
    "d_wsetlatch_offset": "B2",
    "d_backing_mask": "B1",
    "d_backing_offset": "B2",
}
assert sorted(P) == sorted(NAMES), "a variant without a prediction, or the reverse"
PRED = dict((n, sorted(P[n].split())) for n in NAMES)
PRED.update({"base": [], "restored": [], "HEAD": sorted("B1 B2 B3 M1 M2 M3 O1 O2 O3 X1".split()),
             "null_absent": sorted(ALL_BUT_D1), "null_true": sorted(ALL_BUT_D1), "null_false": sorted(ALL_BUT_D1)})
CTRL = dict((n, "OK") for n in PRED)
CTRL.update({"null_absent": "FAIL", "null_true": "FAIL", "null_false": "FAIL"})
WHY = {
    "d_exchanged": "EQUIVALENT: each arm still tests and sets ONE latch of its own; the names are swapped",
    "d_predlatch_mask": "EQUIVALENT under a 0 decline: reads after the first take the write arm with idata 0, "
                        "which the mask whitelists (SDRAM_MASK_256KB == 0); odata stays 0",
    "d_predlatch_offset": "EQUIVALENT under a 0 decline: reads after the first take the write arm, where "
                          "`idata != 0` is false; odata stays 0",
    "d_predlen_mask": "ESCAPE, disclosed (clause e): every SDRAM row is a word access and the decline tests no width",
    "d_earlyret_mask": "EQUIVALENT: memory_rw.c (#95) zeroes the read buffer before the handler runs and the "
                       "declined value is 0, so skipping the tail still hands the guest 0",
    "d_earlyret_offset": "EQUIVALENT: as d_earlyret_mask",
}
OBS = {
    "MC": "arm M's pre-read `reg`: CP15 c1 bit 0, r5, r6 = 0x1011, r1, the r7-r9 sentinels",
    "OC": "arm O's pre-read `reg` (as MC)",
    "XC": "arm X's pre-read `reg` (as MC, plus sl)",
    "WC": "arm W's pre-write `reg`: the operands 0x01FC0000, 0, 0x40000, 0x12345678",
    "BC": "arm B's pre-write `reg`: the operands and the r7/r8 sentinels",
    "UC": "arm U's pre-read `reg`: CP15 c1 bit 0 SET, r6 present and != 0x1011, sentinels",
    "M1": "arm M's status and exit code (SURVIVED, 0)",
    "M2": "r7, r8, r9 after the three mask reads (each 0; each held 0x12345678 before)",
    "M3": "arm M's bracketed footbridge diagnostics as a list (exactly [mask announce])",
    "O1": "arm O's status and exit code",
    "O2": "r7, r8, r9 after the three offset reads",
    "O3": "arm O's diagnostics as a list (exactly [offset announce])",
    "X1": "arm X's diagnostics as a list (exactly [mask announce, offset announce])",
    "W1": "arm W alive, exit 0, and no read announce among its diagnostics",
    "W2": "arm W's write announces as a list (exactly [mask 0x12345678, offset 0x40000])",
    "B1": "r7 after B's mask read (0, not 0x03FC0000) and the mask announce count (1)",
    "B2": "r8 after B's offset read (0, not 0x40000) and the offset announce count (1)",
    "B3": "the counts of B's two after-the-read write announces (mask 0x12345678, offset 0x80000), 1 each",
    "U1": "arm U alive, exit 0, no footbridge diagnostic, r7 = r9 = 0 (zero fill)",
}
NEW_ROWS = "MC M1 M2 M3 OC O1 O2 O3 XC X1 WC W1 W2 BC B1 B2 B3 UC U1".split()

STATIC = """PRETABLE_1 -- fbsdrampair, test-variant TABLE 1.  Written BEFORE table 1 runs: this file's mtime precedes
table1_20261105/runs/, TABLE.log and SCORES.txt, which is the order discriminator.

INSTRUMENT  table1_20261105/probe56_frozen.py, md5 a52267ff1856bc4127c2052a4b30f8e0, cmp-identical at freeze time
            to regress/footbridge_sites_probe.py (56 rows; measured on the fix 56/56 and pre-fix 46/56 in
            impl_20261105/probe_legs.out, and through gate_arm.sh's own footbridge block, 29/29 on build/, in
            impl_20261105/fbblock_check.out).  The table runs ONLY this frozen copy.
BASELINE    named: the GXEMUL-SEC working copy of src/devices/dev_footbridge.c at HEAD edb3213f plus the uncommitted
            fbsdrampair fix, md5 ccaf09d4d30c5a29e6fe0422c0681314 = table1_20261105/dev_footbridge.c.fix1.  The table
            refuses to start unless fix1 cmp's against the working copy AND the clone's dev_footbridge.c cmp's
            against fix1 before mutant 1; it rebuilds the baseline in the clone and requires
            [ gxemul -nt dev_footbridge.c ] for that build and for every variant's.
CLONE       /tmp/gxfbs2, a cp -a of build/ (which holds the fix since propagation); a clone-local .MUTANT is written
            before anything is built; cleared ONLY after the restore (cp from GXEMUL-SEC) cmp's clean and the
            rebuilt binary is newer than its source; then the clone is removed.
VARIANTS    fbs_variants_1.py -- 40, each ONE exact-text replacement against fix1, refused unless the find-text
            occurs exactly once.  d_exchanged and d_backing_* replace one contiguous span.
SCORING     a row is RED when its line ends in FAIL.  SCORES.txt: <name> <green>/<total> CONTROL=<OK|FAIL>
            DONE=<1 if PROBE_WALL printed> NRED=<n> RED=<rows|none>; CONTROL=OK means FOOTBRIDGE_SITES_CONTROL=OK.

LEGS (exact):
  base          56/56  CONTROL=OK    RED=none
  HEAD          46/56  CONTROL=OK    RED=B1,B2,B3,M1,M2,M3,O1,O2,O3,X1   (impl_20261105/dev_footbridge.c.pre_fbs,
                       md5 0b3370b8, the pre-fix source, built IN THE CLONE: build/ holds the fix now)
  null_absent    1/56  CONTROL=FAIL  RED=every row but D1   (/nonexistent/gxemul: execvp fails, no prompt)
  null_true      1/56  CONTROL=FAIL  RED=every row but D1   (/bin/true: exits 0, no prompt)
  null_false     1/56  CONTROL=FAIL  RED=every row but D1   (/bin/false: exits 1, no prompt; H1's text clause fails)
                 D1 stays green on a dead run: it compares only words that were stepped, and none were.
  restored      56/56  CONTROL=OK    RED=none   (the clone rebuilt from GXEMUL-SEC before the sentinel goes)

FLOOR CLAUSES -> LEGS/VARIANTS: (a) HEAD; (b) b_exit_mask, b_exit_offset -- HEAD's two lines verbatim at each fixed
site; (c) the three null media (a runtime probe's null medium: an absent or non-emulator binary); (d) the null-repair
forms over the fix's DEPENDS-ON predicates -- the latch test (latchnever, latchpass, latchinv), the read guard
(predinv, predalways, prednever, predlatch, predorlatch, predlen, the opswap operand swaps drawn from the body-read
latch), and the repair's effect (announcedel, oldtext, misname, value_*, earlyret, wsetlatch, backing); the rulings'
latch-collision and announce variants are d_shared_*, d_setswap_*, d_exchanged, d_announcedel_*, d_oldtext_mask,
d_misname_mask; (e) the probe docstring's SDRAM CONTRACT and NOT COVERED.

SIBLING PARITY -- the two arms the fix edits, against each other and against #545's declined READ at 18Ch:
  channel                        SDRAM_BA_MASK (+0x100)     SDRAM_BA_OFFSET (+0x104)    18Ch (#545, arm S)
  survival                       M1 (X1, B1-B3)             O1 (X1, B1-B3)              N0-N5 require arm S alive
  declined value                 M2 (3 reads), B1           O2 (3 reads), B2            N3: r9 = r8 = 0
  announced once, its own text   M3, X1, B1                 O3, X1, B2                  N3 count 1
  one latch per register         X1, B2                     X1, B2                      N0: five distinct
  writes untouched               W1, W2, B3                 W1, W2, B3                  E5 (Clear still works)
  write with the read latch SET  B3                         B3                          n/a: 18Ch's write arm is
                                                                                        outside its read guard
  ASYMMETRY, and it is in the WRITE arms, not the fix: the mask write arm whitelists eleven Table 7-7 values (0
  among them) and announces the rest; the offset write arm announces any nonzero value.  So a READ diverted into
  the write path (idata 0) is silent at BOTH arms, and the predicate-inversion variants are caught by announce
  rows at both, never by a value or survival row.  Parity holds; no row owed.

CLAIM -> ROW -- each added comment sentence of the fix that asserts an observable:
  struct  "one warn-once latch per SDRAM register READ"          -> M3, O3 (once over 3 reads); X1 (per register)
          "that used to end the process"                         -> HEAD leg: M1, O1 red
          "(7.3.9, 7.3.10: both registers are R/W)"              -> provenance; no row
          "Zeroed by the same memset and calloc as the five above"-> M3/O3: the FIRST read announces (1, not 0)
  mask    "an R/W register ..., so this read is legal"            -> M1 (survival); provenance
          "-- it used to end the emulator with exit(1)"          -> HEAD leg; b_exit_mask
          "The write arms keep nothing"                          -> B1, B2 (0 read back after a write)
          "(hardware would read back W & 0x8ffc0000 here, W & 0x0ffc0000 at 104h; keeping writes is filed)"
                                                                 -> NO ROW: hardware behaviour the model does not
                                                                    implement; B1/B2 pin that it does not
          "so the read is declined: odata stays 0"               -> M2, O2, B1, B2; d_value_*
          "and the common tail below returns it -- keep the break"
                                                                 -> NO ROW POSSIBLE: an early return is EQUIVALENT
                                                                    (memory_rw.c #95 zeroes the read buffer, the
                                                                    decline is 0) -- d_earlyret_* predicted GREEN
          "0 is also both registers' normal reset value; 00FC0000h is only the mask's blank-ROM-programming default"
                                                                 -> provenance (dc21285.txt 7.3.9, 7.3.10,
                                                                    :3206-3228); the 0 itself is M2/O2
          "Announced once per register."                         -> M3, O3, X1, B1, B2
  offset  "declined with 0 and announced once, as for SDRAM_BA_MASK (7.3.10: R/W, reset value 0)"
                                                                 -> O2, O3, X1, B2

GUARD FIELD vs BODY FIELD -- per arm (mask shown; the offset arm is the same with its own latch):
  dominating predicates, walked to DEVICE_ACCESS(footbridge)'s boundary, never into callers or callees:
    switch (relative_addr) case SDRAM_BA_MASK   relative_addr: ONE value inside the arm (0x100); the timer fold
                                                 above the switch rewrites only 0x300..0x36c
    if (writeflag == MEM_READ)                   writeflag: {MEM_READ = 0, MEM_WRITE = 1}
    if (!d->warned_sdram_mask_r)   (added)       the latch: {0, set}
  body fields -- what the decline reads or writes: d->warned_sdram_mask_r (read and written); odata (NOT assigned:
    it keeps the function's initial 0); the common tail's len (memory_writemax64(cpu, data, len, odata)).
  partition the body induces on each: writeflag {READ, WRITE}; latch {0, set}; odata {0} -- no test; len: NONE --
    the decline tests no width, so a width conjunct is clause (e), DISCLOSED (d_predlen_mask predicted GREEN).
  guard field vs body field: the latch is both; who else writes it: `grep -c warned_sdram_mask_r` = 3 (declaration,
    test, set) -- only its own read arm.  No collision exists in the tree; the collisions are BUILT:
    d_shared_*, d_setswap_*, d_wsetlatch_*, d_exchanged.
  joint cells {READ, WRITE} x {latch 0, set}, per arm, and the rows holding each:
    (READ, 0)    the first read: M3/O3, X1, B1/B2       (READ, set)   reads 2-3: M3/O3 (count stays 1), M2/O2, X1
    (WRITE, 0)   W1, W2; B's first two writes           (WRITE, set)  B3: B's writes AFTER its reads
  operand swaps from body-read fields (clause d for a de-fatalisation): writeflag -> the latch (d_opswap_*).

CHANNEL CHECK -- the first mandated application, so it is CHECKED rather than obeyed: every row's predicted killers
and the observable that differs are written below before the table runs.  A variant that reds a row not listed for
it, or leaves a listed row green, is a MISS and is reported as one.
"""


def pretable():
    out = [STATIC, "CHANNEL -- per row: the observable that differs, and the variants predicted to red it:"]
    for r in NEW_ROWS:
        kill = [n for n in NAMES if r in PRED[n]]
        out.append("  %-3s %s" % (r, OBS[r]))
        out.append("      killed by: %s" % (", ".join(kill) if kill else "no product variant -- a CONTROL; "
                                                  "red only on the null media (no prompt, no `reg`)"))
    out.append("  The 37 older rows (arms L, T, E, S, Q, H) touch neither SDRAM register: predicted GREEN under every"
               " variant, red only on the null media (all but D1).")
    out.append("")
    out.append("VARIANTS -- %d, exact predicted RED sets (CONTROL=OK for every variant):" % len(NAMES))
    for n in NAMES:
        red = ",".join(PRED[n]) if PRED[n] else "none -- GREEN (%s)" % WHY[n]
        out.append("  %-22s %-58s RED=%s" % (n, DESC[n], red))
    eq = [n for n in NAMES if not PRED[n]]
    nequiv = sum(1 for n in eq if WHY[n].startswith("EQUIVALENT"))
    nesc = [n for n in eq if WHY[n].startswith("ESCAPE")]
    out.append("")
    out.append("PREDICTED GREEN: %d of %d (%s) -- %d EQUIVALENT, %d disclosed clause-(e) escape (%s).  Counts derived"
               " from WHY, not typed." % (len(eq), len(NAMES), ", ".join(eq), nequiv, len(nesc), ", ".join(nesc)))
    return NL.join(out) + NL


def parse_scores(path):
    got = {}
    for line in io.open(path, encoding="utf-8"):
        p = line.split()
        if not p:
            continue
        if len(p) == 2 and p[1].endswith("FAILED"):
            got[p[0]] = (p[1], None, None)
            continue
        f = dict(x.split("=", 1) for x in p[2:] if "=" in x)
        red = [] if f.get("RED", "none") == "none" else sorted(f["RED"].split(","))
        got[p[0]] = (p[1], f.get("CONTROL"), red)
    return got


def compare(path):
    got = parse_scores(path)
    order = ["base", "HEAD", "null_absent", "null_true", "null_false"] + NAMES + ["restored"]
    miss = 0
    for n in order:
        if n not in got:
            print("%-22s NOT RUN" % n)
            miss += 1
            continue
        score, ctrl, red = got[n]
        if red is None:
            print("%-22s %s" % (n, score))
            miss += 1
            continue
        want = PRED[n]
        ok = red == want and ctrl == CTRL[n]
        extra = sorted(set(red) - set(want))
        lost = sorted(set(want) - set(red))
        print("%-22s %-6s CONTROL=%-4s %-5s%s" % (n, score, ctrl, "MATCH" if ok else "MISS",
              "" if ok else "  extra-red=%s  predicted-but-green=%s  control-want=%s"
              % (",".join(extra) or "-", ",".join(lost) or "-", CTRL[n])))
        miss += 0 if ok else 1
    print("COMPARE: %d of %d lines match their prediction; %d miss" % (len(order) - miss, len(order), miss))


if __name__ == "__main__":
    a = sys.argv[1:]
    if a == ["list"]:
        print(NL.join(NAMES))
    elif len(a) == 4 and a[0] == "apply":
        src = io.open(a[2], encoding="latin-1", newline="").read()
        out = EDIT[a[1]](src)
        assert out != src
        io.open(a[3], "w", encoding="latin-1", newline="").write(out)
        print("%s: applied (%+d bytes)" % (a[1], len(out) - len(src)))
    elif len(a) == 2 and a[0] == "check":
        fix = io.open(FIX1, encoding="latin-1", newline="").read()
        os.makedirs(a[1], exist_ok=True)
        for n in NAMES:
            out = EDIT[n](fix)
            assert out != fix, n
            io.open(os.path.join(a[1], n + ".c"), "w", encoding="latin-1", newline="").write(out)
            print("%-22s applies once, %+5d bytes" % (n, len(out) - len(fix)))
        print("CHECK: %d variants apply" % len(NAMES))
    elif a == ["pretable"]:
        sys.stdout.write(pretable())
    elif len(a) == 2 and a[0] == "compare":
        compare(a[1])
    else:
        sys.exit(__doc__)
