#!/usr/bin/env python3
"""#519 kill table 5 mutator.  usage: mutate519k5.py <SEC dev_sgi_re.c> <out path> <LEG>

Every leg is ONE replacement of the unique line `\t\t\tok = 0;`, text exactly as specified in
regress/artifacts/sgirandomcolour/codex_closurediff_20260912b.txt.  A find-text that does not
occur EXACTLY ONCE is a hard failure (exit 3): a leg that silently measured the unmutated tree
would read as a surviving mutant.  BASE copies the source unchanged."""
import io, sys

OLD = "\t\t\tok = 0;\n"
PRE = "\t\t\tmemset(buf, 0, sizeof(buf)); ok = "

def first(tm, depth):
    return PRE + "(tlb_mode == %d && bufdepth == %d && !(d->warned & SGIRE_W_BADCOLOR));\n" % (tm, depth)

LEGS = {
    "FIRST_A2_ZERO":  first(0, 2),
    "FIRST_A8_ZERO":  first(0, 8),
    "FIRST_B2_ZERO":  first(1, 2),
    "FIRST_B4_ZERO":  first(1, 4),
    "FIRST_B8_ZERO":  first(1, 8),
    "FIRST_C2_ZERO":  first(2, 2),
    "FIRST_C4_ZERO":  first(2, 4),
    "FIRST_C8_ZERO":  first(2, 8),
    "FIRST_L2_ZERO":  first(4, 2),
    "FIRST_L8_ZERO":  first(4, 8),
    "REPEAT_L1_ZERO": PRE + "(tlb_mode == 4 && bufdepth == 1 && (d->warned & SGIRE_W_BADCOLOR) != 0);\n",
    "NIB_OTHER_ZERO": PRE + "(color_mode != 0xf0 && color_mode != 0x50);\n",
    "TAIL8_ZERO":     "\t\t\tok = 0; if (bufdepth == 8) { memset(buf, 0, sizeof(buf)); cpu->memory_rw(cpu, "
                      "cpu->mem, tileptr + ofs + 4, buf, 4, MEM_WRITE, NO_EXCEPTIONS | PHYSICAL); }\n",
}

src, dst, leg = sys.argv[1:4]
t = io.open(src, encoding="utf-8").read()
if leg != "BASE":
    if leg not in LEGS:
        sys.exit("unknown leg %s" % leg)
    n = t.count(OLD)
    if n != 1:
        sys.stderr.write("FIND-TEXT occurs %d times, not 1 -- REFUSING\n" % n)
        sys.exit(3)
    t = t.replace(OLD, LEGS[leg])
io.open(dst, "w", encoding="utf-8", newline="\n").write(t)
print("MUTATED %s" % leg)
