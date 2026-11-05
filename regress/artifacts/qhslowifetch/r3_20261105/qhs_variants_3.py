#!/usr/bin/env python3
"""qhs_variants_3.py -- test-variant TABLE 3 for the qhslowifetch detector, 2026-11-05, as ruled by the adjudication of repair pass 2
(p2r_20261105/ADJ_FABLE.md): table 2's 27 variants plus V8 (arm (a)'s guard conjoined with ME clear, GLM's floor gap, Q1), V9 (the
same with ME set) and V10 (the Q4 counter-edit: inside arm (c), `if (msr & ME) goto bad;`).  Baseline: r3_20261105/cpu_ppc_instr.c.fix4
(fix3 plus the ruled Q8 comment; no code change).  Instrument: the 60-row probe (table3/probe60_frozen.py).
  qhs_variants_3.py list                     the variant names, in table order
  qhs_variants_3.py apply <name> <in> <out>  write <in> with variant <name> applied (each edit asserted to occur ONCE; exit 3 if not)
  qhs_variants_3.py pretable                 the PRETABLE_3 predictions (written BEFORE table 3 runs), derived from table 2's MEASURED
                                             red sets plus the rules for the four new rows stated in the output
Exact-string edits; every backslash is chr(92)."""
import importlib.util
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DET = os.path.join(os.path.dirname(HERE), "det_20261104")
spec = importlib.util.spec_from_file_location("qv2", os.path.join(DET, "qhs_variants_2.py"))
qv2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qv2)
T, NL = chr(9), chr(10)
A, CHEAD = qv2.A, qv2.CHEAD
ME = "(cpu->cd.ppc.msr & PPC_MSR_ME)"
V = list(qv2.V) + [
    ("V8_a_meclear", [(A, A.replace("if (cpu->translation_readahead)", "if (cpu->translation_readahead && !" + ME + ")"))], 1,
     "T ra me nonex (with ME set the read-ahead failure passes arm (a); pc == addr skips (b); (c) parks: one report)",
     "arm (a)'s guard conjoined with ME clear (Q1, GLM)"),
    ("V9_a_meset", [(A, A.replace("if (cpu->translation_readahead)", "if (cpu->translation_readahead && " + ME + ")"))], 1,
     "T ra nonex (with ME clear the read-ahead failure passes arm (a) and (c) parks: one report)",
     "arm (a)'s guard conjoined with ME set (Q1's mirror)"),
    ("V10_c_me_bad", [(CHEAD, T * 3 + "if (!cpu->running) {" + NL + T * 4 + "if " + ME + NL + T * 5 + "goto bad;" + NL +
                       T * 4 + "cpu->cd.ppc.next_ic = &nothing_call;" + NL)], 1,
     "T me unimpl (bad: prints UNIMPLEMENTED; pc, SRR0, the count and the exit are base -- ADJ_FABLE.md Q4)",
     "inside arm (c): an ME-set halt sent to bad: (Q4's counter-edit)"),
    ("V11_c_me_chk", [(CHEAD, T * 3 + "if (!cpu->running) {" + NL + '\t\t\t\tif (cpu->cd.ppc.msr & PPC_MSR_ME) {\n\t\t\t\t\tfatal("[ ppc: instruction fetch from 0x%" PRIx64\n\t\t\t\t\t    " declined with MSR[ME]=0: checkstop ]\\n",\n\t\t\t\t\t    (uint64_t) addr);\n\t\t\t\t\tcpu->running = 0;\n\t\t\t\t\tcpu->cd.ppc.next_ic = &nothing_call;\n\t\t\t\t\treturn;\n\t\t\t\t}\n' +
                       T * 4 + "cpu->cd.ppc.next_ic = &nothing_call;" + NL)], 2,
     "T me chkstop, T ra me chkstop (the checkstop line is the only difference; GRID_OPUS/FABLE/MYTHOS G1)",
     "inside arm (c): an ME-set halt sent to the checkstop fallback (grid G1)"),
    ("V12_fail_ra", [(qv2.OPEN, qv2.OPEN.replace("CACHE_INSTRUCTION)) {", "CACHE_INSTRUCTION) && !cpu->translation_readahead) {"))], 2,
     "T ra nonex, T ra me nonex at least (BUILD-DEPENDENT: the read-ahead slot decodes the stale ib, as D12)",
     "the failure test conjoined with not-read-ahead (GRID_FABLE gap 2, conditional)"),
]
NEW_ROWS = ["T_me_unimpl", "T_ra_me_session", "T_ra_me_pc", "T_ra_me_nonex", "T_me_chkstop", "T_ra_me_chkstop"]
ME_DERIVED = {   # variants whose T ra me rows differ from T ra's because they consult MSR[ME] (derivations, stated in PRETABLE_3)
    "D1_c_inv": ["T_ra_me_pc"], "D2_c_del": ["T_ra_me_pc"], "D8_c_below_d": ["T_ra_me_pc"], "D13_c_me": ["T_ra_me_pc"],
    "D14_c_meset": [], "D15_dom_ok": ["T_ra_me_pc", "T_ra_me_nonex"], "V7_fail_inv": ["T_ra_me_pc", "T_ra_me_nonex"],
    "V8_a_meclear": ["T_ra_me_nonex"], "V9_a_meset": [], "V10_c_me_bad": ["T_me_unimpl"],
    "V11_c_me_chk": ["T_me_chkstop", "T_ra_me_chkstop"],
}


def measured2():
    out = {}
    for line in io.open(os.path.join(DET, "table2", "SCORES.txt"), encoding="utf-8"):
        p = line.split()
        if len(p) > 1 and "RED=" in line:
            red = line.rsplit("RED=", 1)[1].strip()
            out[p[0]] = [] if red == "none" else red.split(",")
    return out


def tme_unimpl2():
    out = {}
    for d in os.listdir(os.path.join(DET, "table2")):
        if d.startswith("sessions_"):
            f = os.path.join(DET, "table2", d, "T_me.txt")
            if os.path.exists(f):
                out[d[len("sessions_"):]] = "UNIMPLEMENTED" in io.open(f, encoding="latin-1").read()
    return out


def predict():
    m2, um = measured2(), tme_unimpl2()
    rows = {}
    for n, _, _, _, _ in V + [("HEAD", None, None, None, None)]:
        base = list(m2.get(n, []))
        if n in ME_DERIVED:
            new = list(ME_DERIVED[n])
        else:
            new = [r.replace("T_ra_", "T_ra_me_") for r in base if r in ("T_ra_session", "T_ra_pc", "T_ra_nonex")]
        if um.get(n):
            new.append("T_me_unimpl")
        extra = {"V9_a_meset": ["T_ra_nonex"], "V12_fail_ra": ["T_ra_nonex", "T_ra_me_nonex"]}.get(n, [])
        rows[n] = base + extra + new
    return rows


def pretable():
    p = predict()
    head = [
        "PRETABLE_3 -- qhslowifetch detector, test-variant table 3.  Written BEFORE table 3 runs (this file's mtime precedes table3/'s).",
        "Instrument: table3/probe62_frozen.py (62 rows; -E pmppc unmodified), frozen from regress/ppc_ifetch_probe.py (r3 + r3b edits).",
        "Baseline: r3_20261105/cpu_ppc_instr.c.fix4 = fix3 + the ruled Q8 comment (no code change) + cpu_ppc.h.fix.  Base run on the",
        "rebuilt build tree: 62/62 (r3_20261105/base62_build.out).  Legs first in the same clone: base, HEAD, three null media.",
        "THE SHAPE-GRID CHECK (before this table; GRID_OPUS.md, GRID_FABLE.md, GRID_MYTHOS.md): all three seats derived ONE firm gap,",
        "arm (c) composed with ME set -> the checkstop fallback (V11), caught only by the checkstop line on the ME-set sessions: the rows",
        "T me chkstop and T ra me chkstop were ADDED (table 2 had REMOVED T me chkstop as vacuous for single-edit shapes; this composition",
        "makes it live).  Fable named a conditional second gap (V12: the failure test conjoined with not-read-ahead), run as a variant.",
        "",
        "THE FOUR CHECKS for the four added rows (ADJ_FABLE.md Q1, Q4):",
        "  SIBLING PARITY -- arm (c) had an ME-set session (T me) and arm (a) did not; `T ra me` closes that asymmetry.  `T step` has an",
        "    unimpl row and `T me` did not; `T me unimpl` closes it (the exact parity argument the ruling made).",
        "  CLAIM -> ROW -- the docstring's 'arm (a)'s guard is seen with ME both clear and set' -> T ra / T ra me nonex; 'an arm (c)",
        "    that sends an ME-set halt to bad: [is caught] only by its UNIMPLEMENTED text' -> T me unimpl.",
        "  GUARD FIELD vs BODY FIELD -- the block reads running, translation_readahead, MSR[ME] and pc == addr; at every reachable entry",
        "    running == 0 (-T) and pc == addr (measured), so the live partitions are readahead {0,1} x ME {0,1}: (0,0) T step/T cont/again,",
        "    (0,1) T me, (1,0) T ra, (1,1) T ra me -- all four cells now have a session.",
        "  CHANNEL -- T ra me nonex: V8 (one report: arm (c) parks the read-ahead failure); T ra me pc: the ME-set exits that deliver a",
        "    machine check (D1, D2, D8, D13: pc 0x200) and D15/V7 (the successful fetch enters the block and takes arm (d)); T me unimpl:",
        "    W3 and V10 (bad: prints UNIMPLEMENTED).",
        "",
        "HOW THE PREDICTIONS ARE BUILT (stated so pass 3 can check them by reading): each table-2 variant's MEASURED red set",
        "(det_20261104/table2/SCORES.txt) is carried over; the new rows are added by rule -- T ra me X reds where T ra X red in table 2",
        "(X = session, pc, nonex) for every variant that does not consult MSR[ME]; for the ME-consulting variants the T ra me reds are",
        "derived (D1/D2/D8/D13: pc only, the machine check at 0x200 with both reports printed; D14: none, arm (c) still parks with ME",
        "set; D15/V7: pc 0x200 and nonex 0, the successful fetch of 0xfec00004 entering the block and taking arm (d), then the zero",
        "word at 0x200 on the fast path stops the CPU); T me unimpl reds where table 2's T_me transcript printed UNIMPLEMENTED (W3",
        "only).  W5, D7 and V7 ride on the uninitialised instruction word: BUILD-DEPENDENT, the claim is that SOME row reds.",
        "",
        "VARIANTS (name, what, predicted red rows -> predicted score):",
    ]
    out = NL.join(head) + NL
    for n, _, _, _, what in V:
        r = p[n]
        out += "   %-14s %-58s red: %s -> %d/62%s" % (n, what[:58], ",".join(r) if r else "none", 62 - len(r), NL)
    out += "   %-14s %-58s red: %s -> %d/62, SYMPTOM=PRESENT%s" % ("HEAD leg", "the pre-fix build", ",".join(p["HEAD"]), 62 - len(p["HEAD"]), NL)
    out += "   null media     /bin/true, an absent binary, /bin/false                    CONTROL=FAIL each" + NL
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
