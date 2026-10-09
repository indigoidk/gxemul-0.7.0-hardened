#!/usr/bin/env python3
"""mutr.py <tree> <mutant>|LIST -- Opus pass-2R candidates for #562.  Find-text must occur
EXACTLY ONCE (presence pin), else exit 3."""
import io
import sys

T, M = sys.argv[1], sys.argv[2]
C = "src/cpus/cpu_arm.c"
I = "src/cpus/cpu_arm_instr.c"
D = "src/cpus/cpu_arm_instr_dpi.c"

DPI_REP = "new_cpsr = (new_cpsr & ~ARM_FLAG_MODE) | cur_mode;"
POP_REP = "new_cpsr = (new_cpsr & ~ARM_FLAG_MODE) |\n"
MUT = {
    # restore-side repair mask narrowed (the mirror of O_mask_nibble at msr_imm)
    "R_dpi_clr17": [(D, DPI_REP, "new_cpsr = (new_cpsr & ~0x17) | cur_mode;")],
    "R_dpi_clr1e": [(D, DPI_REP, "new_cpsr = (new_cpsr & ~0x1e) | cur_mode;")],
    "R_dpi_clr1d": [(D, DPI_REP, "new_cpsr = (new_cpsr & ~0x1d) | cur_mode;")],
    "R_pop_clr17": [(I, POP_REP, "new_cpsr = (new_cpsr & ~0x17) |\n")],
    "R_pop_clr14": [(I, POP_REP, "new_cpsr = (new_cpsr & ~0x14) |\n")],
    # helper projection WIDENED (the contract claims only DROPPED)
    "H_proj_ff": [(C, "switch (mode & ARM_FLAG_MODE) {", "switch (mode & 0xff) {")],
    # label x latch-state joint: repair skipped on a REPEAT visit at a non-SVC label
    "L_dpi_latchlabel": [(D, "if (spsr_copied && !arm_mode_is_modelled(new_cpsr)) {",
                          "if (spsr_copied && !arm_mode_is_modelled(new_cpsr) &&\n"
                          "\t\t    (cur_mode == ARM_MODE_SVC32 ||\n"
                          "\t\t    !(cpu->cd.arm.mode_warned & ARM_MODEWARN_DPI))) {")],
    "L_pop_latchlabel": [(I, "\t\tif (!arm_mode_is_modelled(new_cpsr)) {",
                          "\t\tif (!arm_mode_is_modelled(new_cpsr) &&\n"
                          "\t\t    ((cpu->cd.arm.cpsr & ARM_FLAG_MODE) == ARM_MODE_SVC32 ||\n"
                          "\t\t    !(cpu->cd.arm.mode_warned & ARM_MODEWARN_POP))) {")],
    # msr_imm label conjunct (clause (e) by my pass-2 ruling; built to measure, not to grade)
    "E_msr_notfiq": [(I, "if ((mask & ARM_FLAG_MODE) && !arm_mode_is_modelled(ic->arg[0])) {",
                      "if ((mask & ARM_FLAG_MODE) && !arm_mode_is_modelled(ic->arg[0]) &&\n"
                      "\t    (cpu->cd.arm.cpsr & ARM_FLAG_MODE) != ARM_MODE_FIQ32) {")],
    # NEGATIVE CONTROL: msr_imm mask narrowed at bit 0 -- predicted KILLED (kill 14: 0x14 bit0=0)
    "N_msr_clr1e": [(I, "\t\tmask &= ~ARM_FLAG_MODE;\n", "\t\tmask &= ~0x1e;\n")],
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
