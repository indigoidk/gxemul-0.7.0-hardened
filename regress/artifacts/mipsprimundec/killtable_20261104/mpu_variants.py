#!/usr/bin/env python3
"""mpu_variants.py -- the test-variant set for the mipsprimundec fix's detector (regress/mips_primundec_probe.py, 121 rows), 2026-11-04.
  mpu_variants.py list                     the variant names, in table order
  mpu_variants.py apply <name> <in> <out>  write <in> with variant <name> applied (each edit asserted to occur ONCE; exit 3 if not)
  mpu_variants.py pretable                 the PRETABLE record (written BEFORE table 1 runs; its mtime proves the order)
The set is clause (b) -- each removed defect reinstated VERBATIM at its fixed site (B1-B6; B5/B6 copy HEAD's own block from
cpu_mips_instr.c.HEAD beside this file) -- and clause (d) -- each predicate the edited lines depend on, weakened to the least-restrictive
form that still reads like the same check, within the enclosing function (D*), with the bound-edge moves of rule D2 for every relational
compare, plus the contract's own claims (the PC-sync handlers, the x64 MODE32 tail, single dropped labels).  Exact-string edits only."""
import io
import os
import sys

T = chr(9)
NL = chr(10)
BS = chr(92)
HERE = os.path.dirname(os.path.abspath(__file__))


def blockrep(s, start, end, new):
    a = s.index(start)
    b = s.index(end, a + len(start))
    assert s.count(start) == 1, ("block start", start)
    return s[:a] + new + s[b:]


def head_block(start, end):
    h = io.open(os.path.join(HERE, "cpu_mips_instr.c.HEAD"), encoding="latin-1", newline="").read()
    a = h.index(start)
    return h[a:h.index(end, a + len(start))]


C_LWC2 = "privilege level.  */" + NL + T * 2 + "ic->f = instr(cpu);" + NL + T * 2 + "ic->arg[0] = 2;" + NL + T * 2 + "break;"
C_LDC2 = ("already are (above).  */" + NL + T * 2 + "if (cpu->cd.mips.cpu_type.isa_level < 2) {" + NL + T * 3 + "ic->f = instr(reserved);" + NL +
          T * 2 + "} else {" + NL + T * 3 + "ic->f = instr(cpu);" + NL + T * 3 + "ic->arg[0] = 2;" + NL + T * 2 + "}")
C_SWC3 = "    CPU.  */" + NL + T * 2 + "if (cpu->cd.mips.cpu_type.isa_level >= 3) {"
C_SWC3ARG = T * 3 + "ic->arg[0] = 3;" + NL + T * 2 + "}" + NL + T * 2 + "break;" + NL + NL + T + "case 0x1d:"
C_JALX = "not a stopped CPU.  */" + NL + T * 2 + "ic->f = instr(reserved);"
C_PREF = "/*  PREF (prefetch) on ISA IV and MIPS32/64:  */" + NL + T * 2 + "if (cpu->cd.mips.cpu_type.isa_level >= 4) {"
C_LWC3III = T * 2 + "} else if (cpu->cd.mips.cpu_type.isa_level == 3) {"
C_LWC3ARG = T * 3 + "ic->arg[0] = 3;" + NL + T * 2 + "}" + NL + T * 2 + "break;" + NL + NL + T + "case HI6_LQ_MDMX:"
C_R5900 = T + "case HI6_LQ_MDMX:" + NL + T * 2 + "if (cpu->cd.mips.cpu_type.rev == MIPS_R5900) {"
NOSYNC_RI = "X(reserved_nosync)" + NL + "{" + NL + T + "mips_cpu_exception(cpu, EXCEPTION_RI, 0, 0, 0, 0, 0, 0);" + NL + "}" + NL + NL + NL
NOSYNC_CPU = "X(cpu_nosync)" + NL + "{" + NL + T + "mips_cpu_exception(cpu, EXCEPTION_CPU, 0, 0, ic->arg[0], 0, 0, 0);" + NL + "}" + NL + NL + NL

# name -> (list of (old, new) or a callable, predicted red rows, what it is)
V = [
    ("B1_lwc2swc2_del", lambda s: blockrep(s, T + "case HI6_LWC2:", T + "case HI6_LDC2:", ""),
     "64/32/24k lwc2+swc2 stop|exc|epc|pc, 64 dsc *", "(b) the LWC2/SWC2 case removed: both fall to default: goto bad (HEAD)"),
    ("B2_ldc2sdc2_del", lambda s: blockrep(s, T + "case HI6_LDC2:", T + "case HI6_SWC3:", ""),
     "64/32/24k ldc2+sdc2 *", "(b) the LDC2/SDC2 case removed (HEAD)"),
    ("B3_swc3_del", lambda s: blockrep(s, T + "case HI6_SWC3:", T + "case 0x1d:", ""),
     "64/32/r5k/24k/5ke swc3 *", "(b) the SWC3 case removed (HEAD)"),
    ("B4_jalx_del", lambda s: blockrep(s, T + "case 0x1d:", T + "case HI6_LWC3:", ""),
     "64/32 jalx *, 64 ds *", "(b) the 0x1d case removed (HEAD)"),
    ("B5_lwc3_head", lambda s: blockrep(s, T + "case HI6_LWC3:", T + "case HI6_LQ_MDMX:", head_block(T + "case HI6_LWC3:", T + "case HI6_LQ_MDMX:")),
     "64/32 lwc3 *", "(b) HEAD's LWC3 block verbatim (fatal TODO + goto bad below ISA IV)"),
    ("B6_mdmx_head", lambda s: blockrep(s, T + "case HI6_LQ_MDMX:", T + "case HI6_SQ_SPECIAL3:", head_block(T + "case HI6_LQ_MDMX:", T + "case HI6_SQ_SPECIAL3:")),
     "64/32 mdmx *", "(b) HEAD's LQ_MDMX block verbatim (fatal TODO: MDMX + goto bad)"),
    ("D01_ldc2_le2", [(C_LDC2, C_LDC2.replace("isa_level < 2", "isa_level <= 2"))],
     "NONE -- the ISA II cell (no ISA II CPU constructs on testmips; disclosed)", "(d) LDC2/SDC2 gate `< 2` -> `<= 2` (edge B+1 = 2)"),
    ("D03_ldc2_lt4", [(C_LDC2, C_LDC2.replace("isa_level < 2", "isa_level < 4"))],
     "64 ldc2+sdc2 exc", "(d) LDC2/SDC2 gate widened `< 4` (R4400 RI, not CpU)"),
    ("D04_ldc2_ge2", [(C_LDC2, C_LDC2.replace("isa_level < 2", "isa_level >= 2"))],
     "64/32/24k ldc2+sdc2 exc", "(d) LDC2/SDC2 gate inverted"),
    ("D05_ldc2_nogate", [(C_LDC2, "already are (above).  */" + NL + T * 2 + "ic->f = instr(cpu);" + NL + T * 2 + "ic->arg[0] = 2;")],
     "32 ldc2+sdc2 exc", "(d) LDC2/SDC2 gate dropped (CpU at ISA I)"),
    ("D06_ldc2_ce3", [(C_LDC2, C_LDC2.replace("ic->arg[0] = 2;", "ic->arg[0] = 3;"))],
     "64/24k ldc2+sdc2 exc", "(d) arg[0] 2 -> 3 on the LDC2/SDC2 CpU arm"),
    ("D07_lwc2_ce3", [(C_LWC2, C_LWC2.replace("ic->arg[0] = 2;", "ic->arg[0] = 3;"))],
     "64/32/24k lwc2+swc2 exc, 64 dsc exc", "(d) arg[0] 2 -> 3 on the LWC2/SWC2 arm"),
    ("D08_swc3_ge4", [(C_SWC3, C_SWC3.replace(">= 3", ">= 4"))],
     "64 swc3 exc", "(d) SWC3 gate `>= 3` -> `>= 4` (edge: ISA III)"),
    ("D09_swc3_gt4", [(C_SWC3, C_SWC3.replace(">= 3", "> 4"))],
     "64 swc3 exc, r5k swc3 exc", "(d) SWC3 gate `> 4`"),
    ("D10_swc3_eq3", [(C_SWC3, C_SWC3.replace(">= 3", "== 3"))],
     "r5k/24k/5ke swc3 exc", "(d) SWC3 gate `== 3`"),
    ("D11_swc3_ge2", [(C_SWC3, C_SWC3.replace(">= 3", ">= 2"))],
     "NONE -- the ISA II cell (disclosed)", "(d) SWC3 gate `>= 2` (edge B-1 = 2)"),
    ("D12_swc3_ge1", [(C_SWC3, C_SWC3.replace(">= 3", ">= 1"))],
     "32 swc3 exc", "(d) SWC3 gate `>= 1` (RI at ISA I)"),
    ("D13_swc3_ce2", [(C_SWC3ARG, C_SWC3ARG.replace("ic->arg[0] = 3;", "ic->arg[0] = 2;"))],
     "32 swc3 exc", "(d) arg[0] 3 -> 2 on the SWC3 CpU arm"),
    ("D14_lwc3_le3", [(C_LWC3III, C_LWC3III.replace("== 3", "<= 3"))],
     "32 lwc3 exc", "(d) LWC3 ISA III arm `== 3` -> `<= 3` (RI at ISA I)"),
    ("D15_pref_ge3", [(C_PREF, C_PREF.replace(">= 4", ">= 3"))],
     "64 lwc3 exc|epc|pc", "(d) PREF gate `>= 4` -> `>= 3` (eats ISA III; edge B-1 = 3)"),
    ("D16_pref_ge5", [(C_PREF, C_PREF.replace(">= 4", ">= 5"))],
     "r5k lwc3 exc|epc|pc", "(d) PREF gate `>= 4` -> `>= 5` (edge B+1: ISA IV to CpU CE 3)"),
    ("D18_lwc3_ce2", [(C_LWC3ARG, C_LWC3ARG.replace("ic->arg[0] = 3;", "ic->arg[0] = 2;"))],
     "32 lwc3 exc", "(d) arg[0] 3 -> 2 on the LWC3 CpU arm"),
    ("D19_r5900_inv", [(C_R5900, C_R5900.replace("== MIPS_R5900", "!= MIPS_R5900"))],
     "64/32 mdmx *", "(d) the MDMX arm's R5900 test inverted"),
    ("D22a_jalx_nosync", [(C_JALX, C_JALX.replace("instr(reserved)", "instr(reserved_nosync)")),
                          ("X(reserved)" + NL + "{", NOSYNC_RI + "X(reserved)" + NL + "{")],
     "64 ds epc and/or bd (the contract's claim; MEASURE)", "(contract) jalx through an RI handler with no PC sync"),
    ("D22b_lwc2_nosync", [(C_LWC2, C_LWC2.replace("instr(cpu)", "instr(cpu_nosync)")),
                          ("X(cpu)" + NL + "{", NOSYNC_CPU + "X(cpu)" + NL + "{")],
     "64 dsc epc and/or bd (the contract's claim; MEASURE)", "(contract) LWC2/SWC2 through a CpU handler with no PC sync"),
    ("D23_ldc2_x64", [(C_LDC2, C_LDC2.replace("ic->arg[0] = 2;" + NL + T * 2 + "}", "ic->arg[0] = 2;" + NL + T * 3 + "x64 = 1;" + NL + T * 2 + "}"))],
     "24k ldc2+sdc2 exc", "(contract) x64 set on the LDC2/SDC2 CpU arm: the MODE32 tail rewrites it to RI"),
    ("D24_lwc2_x64", [(C_LWC2, C_LWC2.replace("ic->arg[0] = 2;", "ic->arg[0] = 2;" + NL + T * 2 + "x64 = 1;"))],
     "32/24k lwc2+swc2 exc", "(contract) x64 set on the LWC2/SWC2 arm (MODE32 rows only)"),
    ("D25_swc2_label", [(T + "case HI6_LWC2:" + NL + T + "case HI6_SWC2:" + NL, T + "case HI6_LWC2:" + NL)],
     "64/32/24k swc2 *", "(d) the SWC2 label alone dropped"),
    ("D26_sdc2_label", [(T + "case HI6_LDC2:" + NL + T + "case HI6_SDC2:" + NL, T + "case HI6_LDC2:" + NL)],
     "64/32/24k sdc2 *", "(d) the SDC2 label alone dropped"),
]

PRETABLE = """PRETABLE -- mipsprimundec detector (regress/mips_primundec_probe.py, 121 rows), written BEFORE table 1 (2026-11-04, the main loop)
Baseline: the round's post-fix working set, GXEMUL-SEC/src/cpus/cpu_mips_instr.c (v3 + v3b + C2), copied beside this file as
cpu_mips_instr.c.base and cmp'd against the clone before variant 1.  Fixed build 121/121; HEAD (pre-fix) 28/121 (detector121_*.out).

1. SIBLING PARITY (the six edited arms; channels: stop, exc, epc, pc; plus Cause.BD in a delay slot; per translator)
   LWC2/SWC2  64-bit R4400 | MODE32 R3000, 24KEc | delay slot: 64 dsc        -- all channels rowed
   LDC2/SDC2  64-bit R4400 | MODE32 R3000 (RI), 24KEc (CpU)                  -- no delay-slot row: the CpU raise is X(cpu), the same
                                                                                handler 64 dsc reaches; owed nothing new
   SWC3       64-bit R4400, R5000, 5KE | MODE32 R3000 (CpU), 24KEc (RI)      -- rowed both translators, both dispositions
   0x1d       64-bit R4400 | MODE32 R3000 | delay slot: 64 ds                -- rowed
   LWC3       64-bit R4400 (RI), R5000/5KE (PREF) | MODE32 R3000 (CpU), 24KEc (PREF)
              ASYMMETRY: the ISA III RI arm has no MODE32 row -- N/A: no ISA III CPU is built with the MODE32 translator.
   LQ_MDMX    64-bit R4400 | MODE32 R3000                                    -- the R5900 branch is untouched and disclosed
   ISA II: no row on any arm -- no ISA II CPU constructs on testmips (disclosed in the probe's contract).

2. CLAIM -> ROW (each added comment sentence asserting an observable consequence)
   LWC2/SWC2 "the architectural result is Coprocessor Unusable (Cause.CE = 2)"     -> 64/32/24k lwc2,swc2 exc
             "Before this they fell to default: goto bad, which stopped ... from any privilege level" -> HEAD history; the witness
             (detector121_head.out, 93 red) is its row in kernel mode; user mode is disclosed, not claimed
   LDC2/SDC2 "below that the encoding is reserved"                                -> 32 ldc2,sdc2 exc (10/0)
   SWC3      "raises Coprocessor Unusable with CE = 3 whatever Status.CU3 holds"   -> 32 swc3 exc; CU3 = 1 is the contract's explicit
             no-row sentence ("Status.CU2 = 1 and CU3 = 1 ... not claimed")
             "from ISA III on it is a Reserved Instruction"                         -> 64, r5k, 24k, 5ke swc3 exc
             "Neither stops the CPU"                                                -> 64/32 swc3 stop
   0x1d      "it is a Reserved Instruction here ..., not a stopped CPU"             -> 64/32 jalx exc, stop; 64 ds
   LWC3      "the encoding is a Reserved Instruction there" (ISA III)              -> 64 lwc3 exc
             "raises Coprocessor Unusable with Cause.CE = 3 ... instead of stopping the CPU" (ISA <= II) -> 32 lwc3 exc, stop
   LQ_MDMX   "decodes as a Reserved Instruction ... instead of stopping the CPU"    -> 64/32 mdmx exc, stop

3. GUARD FIELD vs BODY FIELD, and the partition the body induces on each lvalue
   guards read: cpu_type.isa_level (LDC2/SDC2 `< 2`; SWC3 `>= 3`; LWC3 `>= 4`, `== 3`), cpu_type.rev (LQ_MDMX `== MIPS_R5900`),
   x64 (the MODE32 tail, after the switch).  bodies write ic->f and ic->arg[0]; X(cpu) reads arg[0] (Cause.CE); X(reserved) none.
   isa_level partition: {1, 2, 3, 4, 32, 64}; rowed 1 (R3000), 3 (R4400), 4 (R5000), 32 (24KEc), 64 (5KE) -- SAMPLED, the ISA II
   slice unrowed and disclosed.  Rule-D2 edges: `< 2` pinned at 1, its edge 2 unrowed (D01 predicted to pass: disclosed); `>= 3`
   pinned at 3 (D08), edge 2 unrowed (D11, disclosed); `>= 4` pinned at both edges 3 (D15) and 4 (D16); `== 3` at 3 and 4.
   rev: {R5900, other} -- R5900 unrowed (every R5900 behaviour disclosed).  arg[0]: {2, 3} -- read by every CpU exc row (D06, D07,
   D13, D18).  x64: {0, 1} on MODE32 -- the 24KEc and R3000 rows hold 0; D23/D24 set it.
   Guard field and body field differ (isa_level/rev vs arg[0]/ic->f) but are written at the SAME site (one decode), so no
   disagreeing-state row is owed.

4. CHANNEL (each variant, the rows predicted red, the observable that differs) -- below; measured next to it in SCORES.txt.
   exc rows read ExcCode/CE from `reg ,0`; stop rows read the debugger's "UNIMPLEMENTED instruction" text; epc/pc rows read
   EPC and PC; bd rows read Cause.BD.  A stopped CPU leaves EPC/Cause untouched, so a (b) variant reds all four of its rows.
"""


def main():
    a = sys.argv[1:]
    if a == ["list"]:
        print(" ".join(n for n, _, _, _ in V))
    elif a == ["pretable"]:
        out = PRETABLE
        for n, _, pred, what in V:
            out += "   %-18s %-58s red: %s%s" % (n, what[:58], pred, NL)
        sys.stdout.write(out)
    elif len(a) == 4 and a[0] == "apply":
        name, src, dst = a[1:]
        s = io.open(src, encoding="latin-1", newline="").read()
        f = dict((n, e) for n, e, _, _ in V)[name]
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
