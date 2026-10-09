#!/usr/bin/env python3
"""mutr4.py <tree> <mutant>|LIST|LANE1|LANE2|LANE3 -- Opus pass-2R4 candidates for #562 repair 4.
Find-text must occur EXACTLY ONCE (presence pin), else exit 3."""
import io
import sys

T, M = sys.argv[1], sys.argv[2]
C = "src/cpus/cpu_arm.c"
I = "src/cpus/cpu_arm_instr.c"
D = "src/cpus/cpu_arm_instr_dpi.c"

PROJ = "\tswitch (mode & ARM_FLAG_MODE) {"
MSR_DEC = "\t\tmask &= ~ARM_FLAG_MODE;\n"
MSR_LATCH = "\t\tif (!(cpu->cd.arm.mode_warned & ARM_MODEWARN_MSR)) {\n"
POP_LATCH = "\t\t\tif (!(cpu->cd.arm.mode_warned & ARM_MODEWARN_POP)) {\n"
DPI_LATCH = "\t\t\tif (!(cpu->cd.arm.mode_warned & ARM_MODEWARN_DPI)) {\n"
POP_GUARD = "\t\tif (!arm_mode_is_modelled(new_cpsr)) {"
CUR = "(cpu->cd.arm.cpsr & ARM_FLAG_MODE)"
NL, TB = chr(10), chr(9)
POP_TAIL = TB*3 + "    (cpu->cd.arm.cpsr & ARM_FLAG_MODE);" + NL + TB*2 + "}" + NL + NL + TB*2 + "switch_register_banks"

MUT = {
    # (A) helper projection NARROWED by bit 3 -- maps 0x18-0x1a onto 0x10-0x12; no driven value moves
    "H_narrow_17": [(C, PROJ, "\tswitch (mode & 0x17) {")],
    # control: narrowed by bit 2 -- 0x14 -> 0x10, predicted KILLED (kill 14)
    "H_narrow_1b": [(C, PROJ, "\tswitch (mode & 0x1b) {")],
    # (A') helper admits 0x18 (the 'admitting' class at an undriven value)
    "H_case_18": [(C, "\tcase ARM_MODE_UND32:\n\t\treturn 1;", "\tcase ARM_MODE_UND32:\n\tcase 0x18:\n\t\treturn 1;")],
    # (B) msr decline width x label: the contract says "fewer than all five mode bits, at any label"
    "M_msr_clr0f_iaus": [(I, MSR_DEC, "\t\tmask &= (" + CUR + " == ARM_MODE_SVC32 || " + CUR +
                          " == ARM_MODE_FIQ32) ? ~ARM_FLAG_MODE : ~0x0f;\n")],
    "M_msr_clr0f_irq": [(I, MSR_DEC, "\t\tmask &= (" + CUR + " == ARM_MODE_IRQ32) ? ~0x0f : ~ARM_FLAG_MODE;\n")],
    "M_msr_clr03_abt": [(I, MSR_DEC, "\t\tmask &= (" + CUR + " == ARM_MODE_ABT32) ? ~0x03 : ~ARM_FLAG_MODE;\n")],
    "M_msr_clr17_fiq": [(I, MSR_DEC, "\t\tmask &= (" + CUR + " == ARM_MODE_FIQ32) ? ~0x17 : ~ARM_FLAG_MODE;\n")],
    # (C) closure rule (2) at the LATCH-SET decline for bit 5 (T): T from the old CPSR once latched
    "N_pop_Tlatch": [(I, POP_LATCH, "\t\t\tif (cpu->cd.arm.mode_warned & ARM_MODEWARN_POP)\n"
                      "\t\t\t\tnew_cpsr = (new_cpsr & ~ARM_FLAG_T) | (cpu->cd.arm.cpsr & ARM_FLAG_T);\n" + POP_LATCH)],
    "N_dpi_Tlatch": [(D, DPI_LATCH, "\t\t\tif (cpu->cd.arm.mode_warned & ARM_MODEWARN_DPI)\n"
                      "\t\t\t\tnew_cpsr = (new_cpsr & ~ARM_FLAG_T) | (cpu->cd.arm.cpsr & ARM_FLAG_T);\n" + DPI_LATCH)],
    "N_msr_Tlatch": [(I, MSR_LATCH, "\t\tif (cpu->cd.arm.mode_warned & ARM_MODEWARN_MSR)\n"
                      "\t\t\tmask &= ~ARM_FLAG_T;\n" + MSR_LATCH)],
    # control: same shape on NZCV at the DPI latch-set decline -- predicted KILLED at R3
    "N_dpi_flagslatch": [(D, DPI_LATCH, "\t\t\tif (cpu->cd.arm.mode_warned & ARM_MODEWARN_DPI)\n"
                          "\t\t\t\tnew_cpsr = (new_cpsr & 0x0fffffff) | (cpu->cd.arm.cpsr & 0xf0000000);\n" + DPI_LATCH)],
    # (C') rule (1) at the latch-set ACCEPT for bit 5: a T-set valid SPSR declined once latched
    "E_pop_Tacc": [(I, POP_GUARD, "\t\tif (!arm_mode_is_modelled(new_cpsr) ||\n"
                    "\t\t    ((cpu->cd.arm.mode_warned & ARM_MODEWARN_POP) && (new_cpsr & ARM_FLAG_T))) {")],
    # (D) disclosed: the decline writes the cached translation's mask
    "M_msr_argmask": [(I, MSR_DEC, "\t\tic->arg[1] &= ~ARM_FLAG_MODE;\n" + MSR_DEC)],
    # (E) closure rule (2) polarity: a decline FORCING a bit 31:8 to 1 (contract: "or forcing it")
    "N_dpi_forceN": [(D, "new_cpsr = (new_cpsr & ~ARM_FLAG_MODE) | cur_mode;",
                      "new_cpsr = (new_cpsr & ~ARM_FLAG_MODE) | cur_mode | 0x80000000;")],
    "N_pop_forceN": [(I, POP_TAIL, POP_TAIL.replace("ARM_FLAG_MODE);", "ARM_FLAG_MODE) | 0x80000000;", 1))],
    # (E') the cell (SPSR bit 0, old bit 1): a decline that ORs in the old CPSR's bits 31:8
    "N_pop_orold": [(I, POP_TAIL, POP_TAIL.replace("ARM_FLAG_MODE);", "ARM_FLAG_MODE) | (cpu->cd.arm.cpsr & 0xffffff00);", 1))],
    "N_dpi_orold": [(D, "new_cpsr = (new_cpsr & ~ARM_FLAG_MODE) | cur_mode;",
                     "new_cpsr = (new_cpsr & ~ARM_FLAG_MODE) | cur_mode | (cpu->cd.arm.cpsr & 0xffffff00);")],
    # control: msr decline forcing N -- predicted KILLED (msr wide: operand N = 0)
    "M_msr_forceN": [(I, MSR_DEC, TB + TB + "mask &= ~(ARM_FLAG_MODE | 0x80000000);" + NL + TB + TB + "cpu->cd.arm.flags |= 8;" + NL)],
}
LANES = {
    "LANE1": ["H_narrow_17", "H_narrow_1b", "H_case_18", "M_argmask_placeholder"],
    "LANE2": ["M_msr_clr0f_iaus", "M_msr_clr0f_irq", "M_msr_clr03_abt", "M_msr_clr17_fiq"],
    "LANE4": ["N_dpi_forceN", "N_pop_forceN", "N_pop_orold", "N_dpi_orold", "M_msr_forceN"],
    "LANE3": ["N_pop_Tlatch", "N_dpi_Tlatch", "N_msr_Tlatch", "N_dpi_flagslatch", "E_pop_Tacc"],
}
LANES["LANE1"][-1] = "M_msr_argmask"
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
