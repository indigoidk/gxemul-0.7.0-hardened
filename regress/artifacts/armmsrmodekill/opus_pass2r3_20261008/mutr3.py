#!/usr/bin/env python3
"""mutr3.py <tree> <mutant>|LIST|LANE1|LANE2 -- Opus pass-2R3 candidates for #562 repair 3.
Find-text must occur EXACTLY ONCE (presence pin), else exit 3."""
import io
import sys

T, M = sys.argv[1], sys.argv[2]
C = "src/cpus/cpu_arm.c"
I = "src/cpus/cpu_arm_instr.c"
D = "src/cpus/cpu_arm_instr_dpi.c"

DPI_REP = "new_cpsr = (new_cpsr & ~ARM_FLAG_MODE) | cur_mode;"
POP_REP = "new_cpsr = (new_cpsr & ~ARM_FLAG_MODE) |\n"
DPI_GUARD = "\t\tif (spsr_copied && !arm_mode_is_modelled(new_cpsr)) {\n"
POP_GUARD = "\t\tif (!arm_mode_is_modelled(new_cpsr)) {"
MSR_GUARD = "if ((mask & ARM_FLAG_MODE) && !arm_mode_is_modelled(ic->arg[0])) {"
PCCMP = "\tif (ic->arg[2] == (size_t)&cpu->cd.arm.r[ARM_PC]) {\n"
MUT = {
    # helper projection widened by bit 5 (T) only -- the 0xdX / 0xcf / 0xdf operands have bit 5 CLEAR
    "H_proj_3f": [(C, "switch (mode & ARM_FLAG_MODE) {", "switch (mode & 0x3f) {")],
    # decline keeps N Z C V from the OLD CPSR (the contract claims this is caught)
    "N_dpi_keepflags": [(D, DPI_REP, "new_cpsr = (new_cpsr & 0x0fffffe0) |"
                         " (cpu->cd.arm.flags << 28) | cur_mode;")],
    "N_pop_keepflags": [(I, POP_REP, "new_cpsr = (new_cpsr & 0x0fffffe0) |"
                         " (cpu->cd.arm.flags << 28) |\n")],
    # enclosing rd==PC compare unconditional in the S template instances only (cell S x Rd!=PC)
    "D_dpi_pccmpS": [(D, PCCMP, "#ifdef A__S\n\tif (1) {\n#else\n" + PCCMP + "#endif\n")],
    # enclosing return_flag widened to an S-bit LDM WITHOUT pc (user-bank LDM^)
    "C_pop_retflagS": [(I, "\tif (return_flag) {\n", "\tif (return_flag || s_bit) {\n")],
    # DPI repair compiled into the MOV instance only (SUBS pc,lr,#4 etc. unrepaired)
    "O_dpi_movonly": [(D, DPI_GUARD, "#ifdef A__MOV\n" + DPI_GUARD + "#else\n\t\tif (0) {\n#endif\n")],
    # msr_imm decline mask ~0x0f at every label but SVC (kill 03 is SVC-only)
    "M_msr_clr0f_nonsvc": [(I, "\t\tmask &= ~ARM_FLAG_MODE;\n",
                            "\t\tmask &= ((cpu->cd.arm.cpsr & ARM_FLAG_MODE) =="
                            " ARM_MODE_SVC32) ? ~ARM_FLAG_MODE : ~0x0fU;\n")],
    # restore keep-mode ~0x1b (bit 2) -- predicted KILLED (bit 2 clear at FIQ IRQ UND SVC)
    "R_dpi_clr1b": [(D, DPI_REP, "new_cpsr = (new_cpsr & ~0x1b) | cur_mode;")],
    "R_pop_clr1b": [(I, POP_REP, "new_cpsr = (new_cpsr & ~0x1b) |\n")],
    # value-form: pop repair only when I is clear -- predicted KILLED (0xcf has I set)
    "K_pop_ionly": [(I, POP_GUARD, "\t\tif (!arm_mode_is_modelled(new_cpsr) &&"
                     " !(new_cpsr & ARM_FLAG_I)) {")],
    # latch x label at msr_imm: guard skipped at SVC once latched -- predicted KILLED (latch rpt)
    "X_msr_latchsvc": [(I, MSR_GUARD, "if ((mask & ARM_FLAG_MODE) && !arm_mode_is_modelled(ic->arg[0])"
                        " &&\n\t    !((cpu->cd.arm.cpsr & ARM_FLAG_MODE) == ARM_MODE_SVC32 &&\n"
                        "\t    (cpu->cd.arm.mode_warned & ARM_MODEWARN_MSR))) {")],
}
LANES = {"LANE1": ["H_proj_3f", "N_dpi_keepflags", "D_dpi_pccmpS", "O_dpi_movonly",
                   "R_dpi_clr1b", "X_msr_latchsvc"],
         "LANE2": ["N_pop_keepflags", "C_pop_retflagS", "M_msr_clr0f_nonsvc", "R_pop_clr1b",
                   "K_pop_ionly"]}
if M == "LIST":
    print(" ".join(MUT))
    sys.exit(0)
if M in LANES:
    print(" ".join(LANES[M]))
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
