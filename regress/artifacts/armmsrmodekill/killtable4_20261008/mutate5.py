#!/usr/bin/env python3
"""mutate5.py <tree> <mutant>|LIST -- #562 repair 4 additions: two probes of closure rules (1)/(2)
at cells the closure claims but no earlier mutant targeted.  Presence-pinned (count == 1)."""
import io
import sys
T, M = sys.argv[1], sys.argv[2]
C = "src/cpus/cpu_arm.c"
I = "src/cpus/cpu_arm_instr.c"
MUT = {
    # rule (2) on the msr path: the field-only decline keeps NZCV from the old CPSR
    "W_msr_keepflags": [(I, "\t\tmask &= ~ARM_FLAG_MODE;\n", "\t\tmask &= ~(ARM_FLAG_MODE | 0xf0000000);\n")],
    # rule (1) at a bit no earlier mutant widened by: bit 8 (A)
    "H_proj_11f": [(C, "\tswitch (mode & ARM_FLAG_MODE) {", "\tswitch (mode & 0x11f) {")],
}
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
