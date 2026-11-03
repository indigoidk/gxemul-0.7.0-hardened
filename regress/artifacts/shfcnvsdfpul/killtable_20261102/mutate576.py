#!/usr/bin/env python3
"""mutate576.py <mutant> <path-to-cpu_sh_instr.c>  -- apply ONE #576 kill-table mutant to the FIXED handler (scratch clone only).
Every mutant is a small edit of X(fcnvsd_fpul_drn) as fixed; the find-text must occur exactly once or the script fails (a
MUTANT-TEXT-NOT-FOUND is a FAIL, so each find-text is also a presence pin)."""
import io, sys
m, p = sys.argv[1], sys.argv[2]
s = io.open(p, encoding="utf-8").read()
INTERP = "\tieee_interpret_float_value(cpu->cd.sh.fpul, &op1, IEEE_FMT_S);\n"
STORES = ("\treg(ic->arg[0]) = (uint32_t) (ieee >> 32);\n"
          "\treg(ic->arg[0] + sizeof(uint32_t)) = (uint32_t) ieee;\n")
LINE = "\tcpu->cd.sh.fpul = (int32_t) op1.f;\n"
assert s.count(INTERP) == 1 and s.count(STORES) == 1, (s.count(INTERP), s.count(STORES))
if m == "M_b":      # (b) verbatim reinstatement of the removed store
    s = s.replace(INTERP, INTERP + LINE)
elif m == "M_c":    # (c) identity body: decode and retire, write nothing
    a = s.index(INTERP); b = s.index(STORES) + len(STORES)
    s = s[:a] + "\t(void) op1; (void) ieee;\t/* M_c identity */\n" + s[b:]
elif m == "M_d":    # specials only
    s = s.replace(INTERP, INTERP + "\tif (op1.nan || isinf(op1.f)) cpu->cd.sh.fpul = 0x80000000;\n")
elif m == "M_f":    # only with DN clear (FPSCR bit 18)
    s = s.replace(INTERP, INTERP + "\tif (!(cpu->cd.sh.fpscr & 0x00040000)) cpu->cd.sh.fpul = (int32_t) op1.f;\n")
elif m == "M_g":    # only for a destination other than DR0
    s = s.replace(INTERP, INTERP + "\tif (ic->arg[0] != (size_t)&cpu->cd.sh.fr[0]) cpu->cd.sh.fpul = (int32_t) op1.f;\n")
elif m == "M_gm":   # the MIRROR of M_g: only for destination DR0 -- the cell the `0.1' DR0 row exists for
    s = s.replace(INTERP, INTERP + "\tif (ic->arg[0] == (size_t)&cpu->cd.sh.fr[0]) cpu->cd.sh.fpul = (int32_t) op1.f;\n")
elif m == "M_h":    # the low half of the result lands in FPUL after the store
    s = s.replace(STORES, STORES + "\tcpu->cd.sh.fpul = (uint32_t) ieee;\n")
elif m == "M_i":    # the two halves exchanged
    s = s.replace(STORES, "\treg(ic->arg[0]) = (uint32_t) ieee;\n\treg(ic->arg[0] + sizeof(uint32_t)) = (uint32_t) (ieee >> 32);\n")
elif m == "M_z":    # store zero on a zero operand
    s = s.replace(INTERP, INTERP + "\tif (op1.f == 0.0) cpu->cd.sh.fpul = 0;\n")
else:
    sys.exit("unknown mutant " + m)
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("applied", m)
