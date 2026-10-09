#!/usr/bin/env python3
"""mutr2.py <tree> <mutant>|LIST -- coordinator-requested panel predictions (grok/codex/deepseek)
for #562 pass-2R.  Find-text must occur EXACTLY ONCE (presence pin), else exit 3."""
import io
import sys

T, M = sys.argv[1], sys.argv[2]
C = "src/cpus/cpu_arm.c"
I = "src/cpus/cpu_arm_instr.c"
D = "src/cpus/cpu_arm_instr_dpi.c"

POP_REP = "new_cpsr = (new_cpsr & ~ARM_FLAG_MODE) |\n"
POP_GUARD = "\t\tif (!arm_mode_is_modelled(new_cpsr)) {"
DPI_GUARD = "if (spsr_copied && !arm_mode_is_modelled(new_cpsr)) {"
DPI_REP = "new_cpsr = (new_cpsr & ~ARM_FLAG_MODE) | cur_mode;"
POP_TAIL = "    (cpu->cd.arm.cpsr & ARM_FLAG_MODE);\n\t\t}\n\n\t\tswitch_register_banks"
MUT = {
    # (a) grok: pop mode-keep mask narrowed (dpi 17/1e/1d and pop 17/14 are in mutr.py)
    "R_pop_clr1e": [(I, POP_REP, "new_cpsr = (new_cpsr & ~0x1e) |\n")],
    "R_pop_clr1d": [(I, POP_REP, "new_cpsr = (new_cpsr & ~0x1d) |\n")],
    # (b) grok: pop guard declines only 0x14
    "B_pop_only14": [(I, POP_GUARD, "\t\tif (!arm_mode_is_modelled(new_cpsr) &&"
                      " (new_cpsr & 0x1f) == 0x14) {")],
    # (c) codex: arm_pop restore block entered for every LDM
    "C_pop_retflag1": [(I, "\tif (return_flag) {\n", "\tif (1) {\n")],
    # (d) codex: DPI destination-PC comparison unconditional; S restore without S
    "D_dpi_pccmp1": [(D, "if (ic->arg[2] == (size_t)&cpu->cd.arm.r[ARM_PC]) {", "if (1) {")],
    "D_dpi_snots": [(D, "#ifdef A__S\n\t\t/*  Copy the right SPSR into CPSR:  */",
                     "#if 1\n\t\t/*  Copy the right SPSR into CPSR:  */")],
    # (e) codex: label x latch, ONE non-SVC label (IRQ)
    "E_dpi_irqlatch": [(D, DPI_GUARD, "if (spsr_copied && !arm_mode_is_modelled(new_cpsr) &&\n"
                        "\t\t    (cur_mode != ARM_MODE_IRQ32 ||\n"
                        "\t\t    !(cpu->cd.arm.mode_warned & ARM_MODEWARN_DPI))) {")],
    "E_pop_irqlatch": [(I, POP_GUARD, "\t\tif (!arm_mode_is_modelled(new_cpsr) &&\n"
                        "\t\t    ((cpu->cd.arm.cpsr & ARM_FLAG_MODE) != ARM_MODE_IRQ32 ||\n"
                        "\t\t    !(cpu->cd.arm.mode_warned & ARM_MODEWARN_POP))) {")],
    # (e') codex accepted/clear cells: a VALID SPSR wrongly declined at IRQ before any warning
    "E_dpi_irqacc": [(D, DPI_GUARD, "if (spsr_copied && (!arm_mode_is_modelled(new_cpsr) ||\n"
                      "\t\t    (cur_mode == ARM_MODE_IRQ32 &&\n"
                      "\t\t    !(cpu->cd.arm.mode_warned & ARM_MODEWARN_DPI)))) {")],
    "E_pop_irqacc": [(I, POP_GUARD, "\t\tif (!arm_mode_is_modelled(new_cpsr) ||\n"
                      "\t\t    ((cpu->cd.arm.cpsr & ARM_FLAG_MODE) == ARM_MODE_IRQ32 &&\n"
                      "\t\t    !(cpu->cd.arm.mode_warned & ARM_MODEWARN_POP))) {")],
    # (f) codex: I forced to 0 in a decline
    "F_dpi_iclr": [(D, DPI_REP, DPI_REP + "\n\t\t\tnew_cpsr &= ~ARM_FLAG_I;")],
    "F_pop_iclr": [(I, POP_TAIL, "    (cpu->cd.arm.cpsr & ARM_FLAG_MODE);\n"
                    "\t\t\tnew_cpsr &= ~ARM_FLAG_I;\n\t\t}\n\n\t\tswitch_register_banks")],
    # (g) deepseek: spsr_copied gate deleted
    "G_dpi_nocopied": [(D, DPI_GUARD, "if (!arm_mode_is_modelled(new_cpsr)) {")],
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
