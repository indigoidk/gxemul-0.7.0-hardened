#!/usr/bin/env python3
#
#  #518 lcabadval KILL TABLE 2 MUTATOR  (the REPAIRED 58-row instrument).
#
#  Written by the table-2 measuring seat.  It is a SEPARATE FILE from the table-1 seat's
#  `mutate518.py' by directive; the (b)-arm machinery and several (d) edit strings are reused
#  from it deliberately, so that a mutant name common to both tables means the SAME EDIT and the
#  two tables can be read against each other.  Where this file's mutant numbering differs from
#  that one's, PRETABLE.out sections 5/6/7 are the authority -- table 1's M24..M34 are ITS OWN
#  seat's additions and are NOT PRETABLE's M24..M41.
#
#  THE NAMED BASELINE is a FROZEN COPY, `t2/BASELINE_t2.c', taken from the SEC working tree at
#  table start and verified `cmp'-clean against it (and against build/ and the clone) before
#  mutant 1.  It is frozen for the reason table 1 learned the hard way: the main loop shipped a
#  REPAIR of the fix at 00:19:23 while that table was between mutants, so BASE/M1/M2 were built
#  over one fix and M3 over another, and the `cmp against the baseline' step passed every time
#  because it compared against the moving thing.  A KILL TABLE OWES ONE BASELINE THE WAY A
#  COMPARISON RUN OWES ONE INSTRUMENT.  The frozen copy is re-`cmp'd against live SEC at the END
#  of the table, and any divergence is REPORTED rather than absorbed.
#
#  Backslashes that must survive into the C file are built with chr(92): the carrier records
#  three incidents where one backslash level was eaten (or added) in either direction on the
#  Bash -> heredoc -> Python path.
#
#  MUTANT-TEXT-NOT-FOUND IS A HARD FAIL (exit 9), never a silent skip, so every mutant
#  additionally PINS the presence of the text it edits.
#
#  MULTI-EDIT IS LICENSED ONLY for the (b) verbatim reinstatements (floor clause (b) applied to
#  a source arm takes however many edits the historical arm took) and for the null medium.
#  Every (d) mutant is ONE find/replace string.  Where that string occurs at two textually
#  identical sites the mutant edits both and REPORTS THE SITE COUNT rather than pretending it is
#  one edit.
import sys, shutil

HERE = ("/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/lcabadval/"
        "killtable_20260910/t2/")
BASE = HERE + "BASELINE_t2.c"          # the FROZEN named baseline
LIVE_SEC = "/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/devices/dev_lca.c"
PRE = ("/mnt/c/Users/User00/AppData/Local/Temp/claude/"
       "C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/"
       "scratchpad/dev_lca.pre518.c")
CLONE = "/tmp/gxopus518b/src/devices/dev_lca.c"

BS = chr(92)
NL = chr(10)
TAB = chr(9)


def unlatched(first_literal):
    """lca_ioc_announce()'s own fatal(), inlined WITHOUT the latch test -- the `latch REMOVED'
    (d) form.  The argument order matches the helper's body exactly, so the printed text is
    byte-identical to the fixed build's and only the once-ness goes.  The rest of the call (its
    continuation string literals and `, idata);') is left untouched by the replacement."""
    return 'fatal("[ lca_ioc: %s: 0x%" PRIx64 "  (once) ]' + BS + 'n", ' + first_literal


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


BMASK = "idata & (IOC_W_BASE_W_BASE | IOC_W_BASE_SG | IOC_W_BASE_WEN)"
ST_B0 = "d->window_base_0 = " + BMASK + ";"
ST_B1 = "d->window_base_1 = " + BMASK + ";"
ST_CONF = "d->ioc_conf = idata & 0x3ULL;"
ST_TB = "d->tlb_enable = idata & IOC_TB_ENA_TEN;"
WENIF = "if (idata & IOC_W_BASE_WEN)"
VDECL = "uint64_t v = idata & 0xfff00000ULL, f = v >> 20;"
RULE = "if ((f & (f + 1)) == 0)"
DEFIF = "if (!(d->warned & (1u << bit))) {"

#  name -> ("__ARM__", case)          (b) verbatim reinstatement of that arm's pre-#518 source
#       -> ("__FILE__", path)         whole-file replacement (the null medium, clause (c))
#       -> (find, replace, occ)       occ: 0 = every site, N = the Nth site only
M = {
    # ================= PRETABLE section 5 : M1..M23 ==========================================
    # ---- (b) VERBATIM REINSTATEMENT of the removed host kill, one arm each -------------------
    "M1_conf_kill":         ("__ARM__", "case LCA_IOC_CONF:"),
    "M2_tbena_kill":        ("__ARM__", "case LCA_IOC_TB_ENA:"),
    "M3_base0_kill":        ("__ARM__", "case LCA_IOC_W_BASE0:"),
    "M4_mask0_kill":        ("__ARM__", "case LCA_IOC_W_MASK0:"),
    "M5_base1_kill":        ("__ARM__", "case LCA_IOC_W_BASE1:"),
    "M6_mask1_kill":        ("__ARM__", "case LCA_IOC_W_MASK1:"),
    "M7_def_kill":          ("__ARM__", "default:"),

    # ---- (d) STORE MASK narrowed / dropped ---------------------------------------------------
    "M8_conf_mask1":        (ST_CONF, "d->ioc_conf = idata & 0x1ULL;", 0),
    "M9_conf_raw":          (ST_CONF, "d->ioc_conf = idata;", 0),
    "M10_tbena_raw":        (ST_TB, "d->tlb_enable = idata;", 0),
    "M11_base_nowen":       (ST_B1, "d->window_base_1 = idata & (IOC_W_BASE_W_BASE"
                                    " | IOC_W_BASE_SG);", 0),
    "M12_base_32":          (ST_B0, "d->window_base_0 = idata & 0xffffffffULL;", 0),

    # ---- (d) the W_MASK FIELD RULE weakened / strengthened, and the store ORDER ---------------
    "M13_rule_weak":        (RULE, "if (f != 0)", 1),
    "M14_rule_strong":      (RULE, "if (f == 1)", 2),
    "M15_store_first":      (VDECL, VDECL + " d->window_mask_0 = v;", 1),

    # ---- (d) LATCHES removed / collapsed -----------------------------------------------------
    "M16_nolatch_mask0":    ('lca_ioc_announce(d, LCA_W_IOC_WMASK0, "unsupported"',
                             unlatched('"unsupported"'), 0),
    "M17_shared_masklatch": ("lca_ioc_announce(d, LCA_W_IOC_WMASK1,",
                             "lca_ioc_announce(d, LCA_W_IOC_WMASK0,", 0),
    "M18_nolatch_conf":     ('lca_ioc_announce(d, LCA_W_IOC_CONF_CFG1, "IOC_CONF<1> set"',
                             unlatched('"IOC_CONF<1> set"'), 0),
    "M19_nolatch_wen":      ('lca_ioc_announce(d, LCA_W_IOC_WEN, "a DMA window was"',
                             unlatched('"a DMA window was"'), 0),

    # ---- (d) the DEFAULT arm -----------------------------------------------------------------
    "M20_def_echo":         ("int bit = writeflag == MEM_WRITE ?",
                             "odata = idata; int bit = writeflag == MEM_WRITE ?", 0),
    "M21_shared_deflatch":  ("LCA_W_IOC_DEF_W : LCA_W_IOC_DEF_R;",
                             "LCA_W_IOC_DEF_W : LCA_W_IOC_DEF_W;", 0),

    # ---- the NULL MEDIUM (floor clause (c)) --------------------------------------------------
    "M22_null":             ("__FILE__", PRE),

    # ---- the ACCEPT-ROW growth mutant (de-escalation failability) -----------------------------
    "M23_accept_narrow":    (ST_B0, "if (idata != 0x300800000ULL) " + ST_B0, 0),

    # ================= PRETABLE section 6 : M24..M33 ==========================================
    "M24_base_nosg":        (ST_B0, "d->window_base_0 = idata & (IOC_W_BASE_W_BASE"
                                    " | IOC_W_BASE_WEN);", 0),
    "M25_conf_widen":       (ST_CONF, "d->ioc_conf = idata & 0x7ULL;", 0),
    "M26_base_widen":       (ST_B0, "d->window_base_0 = idata & (IOC_W_BASE_W_BASE"
                                    " | IOC_W_BASE_SG | IOC_W_BASE_WEN | (1ULL << 34));", 0),
    "M27_mask_widen":       ("idata & 0xfff00000ULL", "idata & 0xfffff000ULL", 0),
    "M28_field_idata":      ("f = v >> 20;", "f = idata >> 20;", 0),
    #  A CONDITIONAL no-store, which is what section 6 means: an unconditional one also reds
    #  `tbena stored' (the first, accepted, write would not land either), and kimi's point is
    #  precisely that `tbena stored' CANNOT see a skipped store because 0x80 normalizes to 0x80.
    #  Storing only when TEN is set leaves `tbena stored' green and reds `tbena clear' alone.
    "M29_tbena_nostore":    (ST_TB, "if (idata & IOC_TB_ENA_TEN) " + ST_TB, 0),
    "M30_nolatch_mask1":    ('lca_ioc_announce(d, LCA_W_IOC_WMASK1, "unsupported"',
                             unlatched('"unsupported"'), 0),
    "M31_nolatch_defr":     (DEFIF, "if (!(d->warned & (1u << bit)) || writeflag == MEM_READ) {",
                             0),
    "M32_shared_conf_wen":  ("lca_ioc_announce(d, LCA_W_IOC_CONF_CFG1,",
                             "lca_ioc_announce(d, LCA_W_IOC_WEN,", 0),
    "M33_shared_m0_defw":   ("lca_ioc_announce(d, LCA_W_IOC_WMASK0,",
                             "lca_ioc_announce(d, LCA_W_IOC_DEF_W,", 0),

    # ================= PRETABLE section 7 : M34..M41 ==========================================
    "M34_conf_dropbit0":    (ST_CONF, "d->ioc_conf = idata & 0x2ULL;", 0),
    "M35_tbena_dropten":    (ST_TB, "d->tlb_enable = idata & 0;", 0),
    "M36_nolatch_defw":     (DEFIF, "if (!(d->warned & (1u << bit)) || writeflag == MEM_WRITE) {",
                             0),
    "M37_base0_nonzero":    (ST_B0, "if (idata != 0ULL) " + ST_B0, 0),
    #  "the announce call deleted", expressed as a single-line always-false guard: observably
    #  identical to deleting the call and it does not need a multi-line find.
    "M38_wen_base1_off":    (WENIF, "if (0 && (idata & IOC_W_BASE_WEN))", 2),
    "M39_wen_base0_off":    (WENIF, "if (0 && (idata & IOC_W_BASE_WEN))", 1),
    "M40_conf_ann_bit0":    ("if (idata & 0x2ULL)", "if (idata & 0x1ULL)", 0),
    "M41_mask_raw_store":   (" = v;", " = idata;", 0),

    # ============ THE MEASURING SEAT'S OWN MUTANTS (task 4) ===================================
    #  M42 is a CONTROL, not a candidate: it verifies that the pass-2 repair of `def read0'
    #  (index 0 -> index 1) actually works, by answering a default READ with a nonzero value.
    #  M20's own `odata = idata' cannot do this -- `idata' is 0 on a read (see the handler's
    #  own `if (writeflag == MEM_WRITE) idata = memory_readmax64(...)').
    "M42_def_allones":      ("int bit = writeflag == MEM_WRITE ?",
                             "odata = ~0ULL; int bit = writeflag == MEM_WRITE ?", 0),
    #  M43..M47: THE SIBLING-CELL HALF.  Every mask/field/announce mutant PRETABLE enumerates is
    #  rowed at the arm whose row names it -- MASK0, BASE0 -- and the twin arm's identical cell
    #  is driven by no row with the bits that would show it.  These are the `#499' shape: repair
    #  at the address the mutant used, symmetric cell left open.  Each is ONE token or ONE hex
    #  digit and each was predicted BEFORE it was built, from the row set, so a KILL refutes the
    #  prediction and is as informative as a sweep.
    "M43_mask1_widen":      ("idata & 0xfff00000ULL", "idata & 0xfffff000ULL", 2),
    "M44_mask1_field_idata": ("f = v >> 20;", "f = idata >> 20;", 2),
    "M45_base1_nosg":       (ST_B1, "d->window_base_1 = idata & (IOC_W_BASE_W_BASE"
                                    " | IOC_W_BASE_WEN);", 0),
    "M46_conf_ann_wide":    ("if (idata & 0x2ULL)", "if (idata & 0x3ULL)", 0),
    "M47_base1_widen":      (ST_B1, "d->window_base_1 = idata & (IOC_W_BASE_W_BASE"
                                    " | IOC_W_BASE_SG | IOC_W_BASE_WEN | (1ULL << 34));", 0),
}

ORDER = ["M%d" % i for i in range(1, 48)]


def sorted_names():
    def key(n):
        return int(n.split("_")[0][1:])
    return sorted(M, key=key)


def apply_one(name):
    if name not in M:
        print("UNKNOWN-MUTANT: %s" % name)
        sys.exit(9)
    spec = M[name]
    shutil.copyfile(BASE, CLONE)          # restore from the FROZEN NAMED BASELINE, every time

    if spec[0] == "__FILE__":
        shutil.copyfile(spec[1], CLONE)
        print("MUTATE %s: whole-file replacement from %s" % (name, spec[1]))
        print("EDIT: <the entire PRE-FIX dev_lca.c: all seven host kills reinstated at once>")
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
    print("  ->  %r   [occ=%s]" % (repl, "ALL" if occ == 0 else occ))


if __name__ == "__main__":
    a = sys.argv[1]
    if a == "--restore":
        shutil.copyfile(BASE, CLONE)
        print("RESTORED the clone from the FROZEN named baseline t2/BASELINE_t2.c")
    elif a == "--restore-sec":
        shutil.copyfile(LIVE_SEC, CLONE)
        print("RESTORED the clone from the LIVE SEC working tree")
    elif a == "--list":
        for k in sorted_names():
            print(k)
    elif a == "--checkbase":
        import filecmp
        same = filecmp.cmp(BASE, LIVE_SEC, shallow=False)
        print("BASELINE_vs_LIVE_SEC=%s" % ("IDENTICAL" if same else "*** DIVERGED ***"))
        sys.exit(0 if same else 7)
    else:
        apply_one(a)
