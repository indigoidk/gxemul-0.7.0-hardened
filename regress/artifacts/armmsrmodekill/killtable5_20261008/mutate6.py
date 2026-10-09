#!/usr/bin/env python3
"""mutate6.py <tree> <mutant>|LIST -- #562 repair 5: the pass-2r4 escapes, rebuilt from the
coordinator's and the panel's descriptions (Opus's own file was not yet published), plus codex's
two named cells.  Presence-pinned (count == 1)."""
import io
import sys
T, M = sys.argv[1], sys.argv[2]
C = "src/cpus/cpu_arm.c"
I = "src/cpus/cpu_arm_instr.c"
D = "src/cpus/cpu_arm_instr_dpi.c"
DPI_REP = "new_cpsr = (new_cpsr & ~ARM_FLAG_MODE) | cur_mode;"
POP_G = "\t\tif (!arm_mode_is_modelled(new_cpsr)) {\n"
MSR_MASK = "\t\tmask &= ~ARM_FLAG_MODE;\n"
CUR = "(cpu->cd.arm.cpsr & ARM_FLAG_MODE)"
MUT = {
    # grok / Opus: helper projection narrowed by bit 3 -- admits 0x18-0x1a
    "H_narrow_17": [(C, "\tswitch (mode & ARM_FLAG_MODE) {", "\tswitch (mode & 0x17) {")],
    # Opus: msr decline leaves bit 4 writable at IRQ/ABT/UND/SYS
    "M_msr_clr0f_iaus": [(I, MSR_MASK, "\t\tmask &= ~((%s == ARM_MODE_IRQ32 || %s == ARM_MODE_ABT32"
                          " || %s == ARM_MODE_UND32 || %s == ARM_MODE_SYS32) ? 0x0f : 0x1f);\n"
                          % (CUR, CUR, CUR, CUR))],
    # codex: the same, IRQ only
    "M_msr_clr0f_irq": [(I, MSR_MASK, "\t\tmask &= ~(%s == ARM_MODE_IRQ32 ? 0x0f : 0x1f);\n" % CUR)],
    # Opus: pop decline keeps the old T once latched
    "N_pop_Tlatch": [(I, POP_G, POP_G + "\t\t\tif (cpu->cd.arm.mode_warned & ARM_MODEWARN_POP)\n"
                      "\t\t\t\tnew_cpsr = (new_cpsr & ~ARM_FLAG_T) |\n"
                      "\t\t\t\t    (cpu->cd.arm.cpsr & ARM_FLAG_T);\n")],
    # Opus / codex: DPI decline forces N set
    "N_dpi_forceN": [(D, DPI_REP, DPI_REP + "\n\t\t\tnew_cpsr |= ARM_FLAG_N;")],
    # the mirror: pop decline forces N set
    "N_pop_forceN": [(I, "\t\t\t    (cpu->cd.arm.cpsr & ARM_FLAG_MODE);\n\t\t}\n\n\t\tswitch_register_banks",
                      "\t\t\t    (cpu->cd.arm.cpsr & ARM_FLAG_MODE);\n\t\t\tnew_cpsr |= ARM_FLAG_N;\n"
                      "\t\t}\n\n\t\tswitch_register_banks")],
    # codex: arm_pop's enclosing predicate widened into the {non-S, no PC} cell only
    "C_pop_nonS_nopc": [(I, "\tif (return_flag) {\n",
                         "\tif (return_flag || (!s_bit && !(iw & 0x8000))) {\n")],
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
