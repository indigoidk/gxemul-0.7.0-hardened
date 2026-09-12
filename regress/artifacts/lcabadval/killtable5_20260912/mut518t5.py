#!/usr/bin/env python3
"""#518 table 5 mutator.  usage: mut518t5.py <SEC dev_lca.c> <out path> <LEG>

Baseline = the CURRENT SEC dev_lca.c (not a frozen older copy -- table 4's t2 mutator restored
from t2/BASELINE_t2.c, which predates later comment edits).  Every find-text is chosen to occur
EXACTLY ONCE, scoped by the arm's own store target where MASK0 and MASK1 share text; a count
other than 1 is a hard failure (exit 3), never an unmutated leg.

  M43_mask1_widen    MASK1 stored-field mask widened to bits 12-31      (t2 M43, L2 in table 4)
  M44_mask1_idata    MASK1 validation operand from RAW idata            (t2 M44, L2 in table 4)
  M47_base1_widen    BASE1 store mask widened to bit 34                 (t2 M47, L2 in table 4)
  M_RULE2            MASK1 rule weakened to (f & (f+1)) <= 2            (adjudicator's #499-trap)
  M_STORE01          MASK0 stored-field mask widened by bit 12          (adjudicator's #499-trap)
  M_CONF_B4          CONF store mask widened by bit 4    -- NEW: no 73-row input set bit 4
  M_TBENA_B8         TB_ENA store mask widened by bit 8  -- NEW: no 73-row input set bit 8
"""
import io, sys

T = "\t"
V0 = T*4 + "uint64_t v = idata & 0xfff00000ULL, f = v >> 20;\n" + T*4 + "if ((f & (f + 1)) == 0)\n" + T*5 + "d->window_mask_0 = v;\n"
V1 = T*4 + "uint64_t v = idata & 0xfff00000ULL, f = v >> 20;\n" + T*4 + "if ((f & (f + 1)) == 0)\n" + T*5 + "d->window_mask_1 = v;\n"
B1 = "d->window_base_1 = idata & (IOC_W_BASE_W_BASE | IOC_W_BASE_SG | IOC_W_BASE_WEN);"

LEGS = {
    "M43_mask1_widen": (V1, V1.replace("idata & 0xfff00000ULL", "idata & 0xfffff000ULL")),
    "M44_mask1_idata": (V1, V1.replace("f = v >> 20;", "f = idata >> 20;")),
    "M47_base1_widen": (B1, B1.replace("IOC_W_BASE_WEN);", "IOC_W_BASE_WEN | (1ULL << 34));")),
    "M_RULE2":         (V1, V1.replace("if ((f & (f + 1)) == 0)", "if ((f & (f + 1)) <= 2)")),
    "M_STORE01":       (V0, V0.replace("idata & 0xfff00000ULL", "idata & 0xfff01000ULL")),
    "M_CONF_B4":       ("d->ioc_conf = idata & 0x3ULL;", "d->ioc_conf = idata & 0x13ULL;"),
    "M_TBENA_B8":      ("d->tlb_enable = idata & IOC_TB_ENA_TEN;",
                        "d->tlb_enable = idata & (IOC_TB_ENA_TEN | 0x100ULL);"),
}

src, dst, leg = sys.argv[1:4]
t = io.open(src, encoding="utf-8").read()
if leg != "BASE":
    if leg not in LEGS:
        sys.exit("unknown leg %s" % leg)
    old, new = LEGS[leg]
    n = t.count(old)
    if n != 1 or old == new:
        sys.stderr.write("FIND-TEXT for %s occurs %d times (or is a no-op) -- REFUSING\n" % (leg, n))
        sys.exit(3)
    t = t.replace(old, new)
io.open(dst, "w", encoding="utf-8", newline="\n").write(t)
print("MUTATED %s" % leg)
