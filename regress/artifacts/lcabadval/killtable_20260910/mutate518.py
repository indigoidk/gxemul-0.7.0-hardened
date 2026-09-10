#!/usr/bin/env python3
#
#  #518 lcabadval KILL-TABLE MUTATOR.
#
#  Restores the scratch clone's dev_lca.c from THE NAMED BASELINE (the SEC working tree, i.e.
#  the round's post-fix uncommitted source) and then applies exactly ONE named mutant by exact
#  find/replace.  MUTANT-TEXT-NOT-FOUND IS A HARD FAIL (exit 9), never a silent skip -- so every
#  mutant additionally PINS the presence of the text it edits.
#
#  Backslashes that must survive into the C file are built with chr(92): the carrier records
#  three incidents where one backslash level was eaten (or added) on the
#  Bash -> heredoc -> Python path, in both directions.
#
#  MULTI-EDIT IS LICENSED ONLY for the (b) verbatim reinstatements (floor clause (b) applied to
#  a source arm: it takes however many edits the historical arm took).  Every (d) mutant is ONE
#  find/replace string; where that string occurs at two textually identical sites the mutant
#  reports the site count rather than pretending it is one.
import sys, shutil

#  *** THE BASELINE IS A FROZEN COPY, NOT THE LIVE SEC WORKING TREE, AND THAT CHANGED
#  MID-TABLE ON 2026-09-10. ***  The first driver run restored from
#  GXEMUL-SEC/src/devices/dev_lca.c on every iteration.  At 00:19:23 the main loop shipped a
#  REPAIR of the fix (FIX518c: 20681 -> 21372 bytes, the diff growing 106 -> 116 insertions)
#  while the table was between mutants -- so BASE/M1/M2 were built over one fix and M3 over
#  another, and NOTHING in the run said so.  The `cmp against the named baseline' step passed
#  every time, because it compared against the moving thing.
#
#  A KILL TABLE OWES ONE BASELINE THE WAY A COMPARISON RUN OWES ONE INSTRUMENT.  The carrier's
#  frozen-copy rule is written for the PROBE; the baseline SOURCE needs it for exactly the same
#  reason, and in a live round it is the more likely of the two to move -- the round is FOR
#  editing that file.
SEC = ("/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/lcabadval/"
       "killtable_20260910/BASELINE_FIX518c.c")
LIVE_SEC = "/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/devices/dev_lca.c"
PRE = ("/mnt/c/Users/User00/AppData/Local/Temp/claude/"
       "C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/"
       "scratchpad/dev_lca.pre518.c")
CLONE = "/tmp/gxopus518/src/devices/dev_lca.c"

BS = chr(92)
NL = chr(10)
TAB = chr(9)


def unlatched(head_after_comma):
    """The announce helper's own fatal(), inlined WITHOUT the latch test -- the `latch removed'
    (d) form.  The %s/%" PRIx64 " argument order matches lca_ioc_announce's own body, so the
    printed text is byte-identical to the fixed build's; only the once-ness goes."""
    return 'fatal("[ lca_ioc: %s: 0x%" PRIx64 "  (once) ]' + BS + 'n", ' + head_after_comma


CASES = ["case LCA_IOC_BASE:", "case LCA_IOC_CONF:", "case LCA_IOC_TBIA:",
         "case LCA_IOC_TB_ENA:", "case LCA_IOC_W_BASE0:", "case LCA_IOC_W_MASK0:",
         "case LCA_IOC_W_T_BASE0:", "case LCA_IOC_W_BASE1:", "case LCA_IOC_W_MASK1:",
         "case LCA_IOC_W_T_BASE1:", "default:"]


def ioc_region(text):
    i = text.index("DEVICE_ACCESS(lca_ioc)")
    j = text.index("if (writeflag == MEM_READ)" + NL + TAB * 2 + "memory_writemax64", i)
    return i, j


def arm_block(text, case):
    """The verbatim source of one switch arm, from its `case' label up to the next label."""
    lo, hi = ioc_region(text)
    k = CASES.index(case)
    i = text.index(case, lo)
    if i >= hi:
        raise SystemExit("case %s not inside lca_ioc" % case)
    j = text.index(CASES[k + 1], i) if k + 1 < len(CASES) else hi
    return text[i:j]


BASEMASK = "idata & (IOC_W_BASE_W_BASE | IOC_W_BASE_SG | IOC_W_BASE_WEN)"

#  name -> ("__ARM__", case)          (b) verbatim reinstatement of that arm's pre-#518 source
#       -> ("__FILE__", path)         whole-file replacement (the null medium)
#       -> (find, replace, occ)       occ: 0 = every site, 1 = first site only, 2 = second only
M = {
    # ---- (b) VERBATIM REINSTATEMENT of the removed host kill, one arm each -------------------
    "M1_conf_kill":         ("__ARM__", "case LCA_IOC_CONF:"),
    "M2_tbena_kill":        ("__ARM__", "case LCA_IOC_TB_ENA:"),
    "M3_base0_kill":        ("__ARM__", "case LCA_IOC_W_BASE0:"),
    "M4_mask0_kill":        ("__ARM__", "case LCA_IOC_W_MASK0:"),
    "M5_base1_kill":        ("__ARM__", "case LCA_IOC_W_BASE1:"),
    "M6_mask1_kill":        ("__ARM__", "case LCA_IOC_W_MASK1:"),
    "M7_def_kill":          ("__ARM__", "default:"),

    # ---- (d) STORE MASK narrowed ------------------------------------------------------------
    "M8_conf_mask1":        ("d->ioc_conf = idata & 0x3ULL;",
                             "d->ioc_conf = idata & 0x1ULL;", 0),
    "M9_conf_raw":          ("d->ioc_conf = idata & 0x3ULL;",
                             "d->ioc_conf = idata;", 0),
    "M10_tbena_raw":        ("d->tlb_enable = idata & IOC_TB_ENA_TEN;",
                             "d->tlb_enable = idata;", 0),
    "M11_base_nowen":       ("d->window_base_1 = " + BASEMASK + ";",
                             "d->window_base_1 = idata & (IOC_W_BASE_W_BASE | IOC_W_BASE_SG);", 0),
    "M12_base_32":          ("d->window_base_0 = " + BASEMASK + ";",
                             "d->window_base_0 = idata & 0xffffffffULL;", 0),

    # ---- (d) the W_MASK FIELD RULE weakened / strengthened, and the store ORDER --------------
    "M13_rule_weak":        ("if ((f & (f + 1)) == 0)", "if (f != 0)", 1),
    "M14_rule_strong":      ("if ((f & (f + 1)) == 0)", "if (f == 1)", 2),
    "M15_store_first":      ("uint64_t v = idata & 0xfff00000ULL, f = v >> 20;",
                             "uint64_t v = idata & 0xfff00000ULL, f = v >> 20;"
                             " d->window_mask_0 = v;", 1),

    # ---- (d) LATCHES removed / collapsed ----------------------------------------------------
    "M16_nolatch_mask0":    ('lca_ioc_announce(d, LCA_W_IOC_WMASK0, "unsupported"',
                             unlatched('"unsupported"'), 0),
    "M17_shared_masklatch": ("lca_ioc_announce(d, LCA_W_IOC_WMASK1,",
                             "lca_ioc_announce(d, LCA_W_IOC_WMASK0,", 0),
    "M18_nolatch_conf":     ('lca_ioc_announce(d, LCA_W_IOC_CONF_CFG1, "IOC_CONF<1> set"',
                             unlatched('"IOC_CONF<1> set"'), 0),
    "M19_nolatch_wen":      ('lca_ioc_announce(d, LCA_W_IOC_WEN, "a DMA window was"',
                             unlatched('"a DMA window was"'), 0),

    # ---- (d) the DEFAULT arm ----------------------------------------------------------------
    "M20_def_echo":         ("int bit = writeflag == MEM_WRITE ?",
                             "odata = idata; int bit = writeflag == MEM_WRITE ?", 0),
    "M21_shared_deflatch":  ("LCA_W_IOC_DEF_W : LCA_W_IOC_DEF_R;",
                             "LCA_W_IOC_DEF_W : LCA_W_IOC_DEF_W;", 0),

    # ---- the NULL MEDIUM (floor clause (c)): the whole PRE-FIX file = all seven kills at once
    "M22_null":             ("__FILE__", PRE),

    # ---- the ACCEPT-ROW growth mutant (de-escalation failability) ----------------------------
    "M23_accept_narrow":    ("d->window_base_0 = " + BASEMASK + ";",
                             "if (idata != 0x300800000ULL) d->window_base_0 = "
                             + BASEMASK + ";", 0),

    # ========== THE MEASURING SEAT'S OWN MUTANTS (task 3), and the one CHANNEL row =============
    # ========== whose named mutant is absent from PRETABLE section 5 (M28).      =============
    #  The (d) cell space in section 5 is {mask kept, mask narrowed, mask DROPPED}; every
    #  planned mask mutant NARROWS.  M24/M25/M26/M27 are the WIDENED/DROPPED half of that same
    #  enumerated cell -- one edit each, the smallest that still reads like the same check.
    "M24_base_maskdrop":    (BASEMASK, "idata", 0),
    "M25_conf_mask_wide":   ("d->ioc_conf = idata & 0x3ULL;",
                             "d->ioc_conf = idata & 0x7ULL;", 0),
    "M26_mask_field_wide":  ("idata & 0xfff00000ULL", "idata & 0xffff00000ULL", 0),
    "M27_tbena_mask_wide":  ("d->tlb_enable = idata & IOC_TB_ENA_TEN;",
                             "d->tlb_enable = idata & ~1ULL;", 0),
    #  M28 is the CHANNEL table's own `M_base0_nonzero' for the `wbase0 zero' row.
    "M28_base0_nonzero":    ("d->window_base_0 = " + BASEMASK + ";",
                             "if (idata != 0ULL) d->window_base_0 = " + BASEMASK + ";", 0),
    #  M29 is the WORKING form of M20 (see TABLE1.out): a default read that answers nonzero.
    "M29_def_allones":      ("int bit = writeflag == MEM_WRITE ?",
                             "odata = ~0ULL; int bit = writeflag == MEM_WRITE ?", 0),
    #  M30: the accepted W_MASK value stored with its low bits mangled -- a store-side edit the
    #  field rule cannot see, testing whether any row pins the STORED value's low bits.
    "M30_wmask_lowbits":    ("d->window_mask_0 = v;", "d->window_mask_0 = v | 0xfULL;", 0),

    # ---- M31..M34: THE "SMALLEST EDIT THAT STILL PASSES" CANDIDATES (task 3) -----------------
    #  Each is ONE character or ONE token, and each was predicted to sweep BEFORE it was built,
    #  from the row set rather than from the code -- so a kill refutes the prediction and is
    #  just as informative as a sweep.
    #
    #  M31: an OFF-BY-ONE IN THE FIELD SHIFT.  Halving a contiguous-low-ones field leaves it
    #  contiguous-low-ones (0b111 -> 0b11) and halving 0b101 -> 0b10 stays non-conforming, so
    #  every one of the six W_MASK values any row drives is classified IDENTICALLY.  It is not
    #  an equivalent mutant: field 0b110 (0x600000) is ILLEGAL and `>> 21' ACCEPTS it.
    "M31_shift21":          ("f = v >> 20;", "f = v >> 21;", 0),
    #  M32/M33: the `&' -> `|' typo, the most plausible one-character mutation there is.  Both
    #  announce predicates become always-true, so the announce fires on values that do NOT have
    #  the announced property -- a WRONG RECORD in product code.  Predicted invisible because
    #  the latch fires on the FIRST (legitimate) write in every session, so a later spurious
    #  announce is suppressed and the count rows still read 1.
    "M32_wen_ann_or":       ("if (idata & IOC_W_BASE_WEN)", "if (idata | IOC_W_BASE_WEN)", 0),
    "M33_conf_ann_or":      ("if (idata & 0x2ULL)", "if (idata | 0x2ULL)", 0),
    #  M34: a CROSS-ARM LATCH COLLISION -- CONF's announce charged to the WEN bit.  PRETABLE
    #  section 3 asks for a state where the guard field and the body field DISAGREE and answers
    #  it with two WITHIN-family collisions (`wmask1 indep', `def r once').  No session in the
    #  40-row instrument writes two DIFFERENT arms' announcing values in one process, so a
    #  collision ACROSS families is unrowed by construction.
    "M34_crosslatch_conf":  ("lca_ioc_announce(d, LCA_W_IOC_CONF_CFG1,",
                             "lca_ioc_announce(d, LCA_W_IOC_WEN,", 0),
}


def apply_one(name):
    if name not in M:
        print("UNKNOWN-MUTANT: %s" % name)
        sys.exit(9)
    spec = M[name]
    shutil.copyfile(SEC, CLONE)              # restore from the NAMED BASELINE first, every time

    if spec[0] == "__FILE__":
        shutil.copyfile(spec[1], CLONE)
        print("MUTATE %s: whole-file replacement from %s" % (name, spec[1]))
        print("EDIT: <the entire PRE-FIX dev_lca.c: all seven host kills reinstated>")
        return

    txt = open(CLONE).read()

    if spec[0] == "__ARM__":
        case = spec[1]
        fixedblk = arm_block(txt, case)
        preblk = arm_block(open(PRE).read(), case)
        if txt.count(fixedblk) != 1:
            print("MUTANT-TEXT-NOT-FOUND: %s block count=%d" % (case, txt.count(fixedblk)))
            sys.exit(9)
        open(CLONE, "w").write(txt.replace(fixedblk, preblk))
        print("MUTATE %s: verbatim PRE-FIX reinstatement of %s (%d -> %d bytes)"
              % (name, case, len(fixedblk), len(preblk)))
        print("EDIT: the whole %s arm replaced by its pre-#518 source (%d lines)"
              % (case, preblk.count(NL)))
        return

    find, repl, occ = spec
    n = txt.count(find)
    if n == 0:
        print("MUTANT-TEXT-NOT-FOUND: %s   find=%r" % (name, find))
        sys.exit(9)
    if occ == 0:
        txt = txt.replace(find, repl)
        sites = n
    elif occ == 1:
        txt = txt.replace(find, repl, 1)
        sites = 1
    else:
        if n < occ:
            print("MUTANT-OCCURRENCE-NOT-FOUND: %s wanted occ %d, have %d" % (name, occ, n))
            sys.exit(9)
        parts = txt.split(find)
        txt = find.join(parts[:occ]) + repl + find.join(parts[occ:])
        sites = 1
    open(CLONE, "w").write(txt)
    print("MUTATE %s: %d site(s) edited of %d matching" % (name, sites, n))
    print("EDIT: %r" % (find,))
    print("  ->  %r   [occ=%d]" % (repl, occ))


if __name__ == "__main__":
    if sys.argv[1] == "--restore":
        shutil.copyfile(SEC, CLONE)
        print("RESTORED from SEC (the named baseline)")
    elif sys.argv[1] == "--list":
        for k in M:
            print(k)
    else:
        apply_one(sys.argv[1])
