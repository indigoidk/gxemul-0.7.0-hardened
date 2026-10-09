#!/usr/bin/env python3
"""mutate3.py <tree> <mutant> -- #562 table 3 (Opus pass-2 additions).  Find-text must occur
EXACTLY ONCE (presence pin), else exit 3."""
import io
import sys

T, M = sys.argv[1], sys.argv[2]
C = "src/cpus/cpu_arm.c"
I = "src/cpus/cpu_arm_instr.c"
D = "src/cpus/cpu_arm_instr_dpi.c"

MUT = {
    "O_mask_nibble": [(I, "\t\tmask &= ~ARM_FLAG_MODE;\n", "\t\tmask &= ~0x0f;\n")],
}
for site, f in (("MSR", I), ("POP", I), ("DPI", D), ("SAVE", C), ("LOAD", C)):
    MUT["D_del_" + site.lower()] = [(f, "cpu->cd.arm.mode_warned |= ARM_MODEWARN_%s;" % site,
                                     "/* #562 mutant: latch set deleted */")]

if M == "LIST":
    print(" ".join(MUT))
    sys.exit(0)
for f, a, b in MUT[M]:
    p = T + "/" + f
    s = io.open(p, newline="").read()
    n = s.count(a)
    if n != 1:
        print("MUTANT-TEXT-NOT-FOUND %s %s count=%d" % (M, f, n))
        sys.exit(3)
    io.open(p, "w", newline="").write(s.replace(a, b))
print("MUTANT-APPLIED %s" % M)
