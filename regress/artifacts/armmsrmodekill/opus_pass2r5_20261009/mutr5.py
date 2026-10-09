#!/usr/bin/env python3
"""mutr5.py <tree> <mutant>|LIST|<LANE> -- Opus pass-2R5 candidates for #562 repair 5.
Every find-text must occur EXACTLY ONCE (presence pin), else exit 3.  Edits are applied in order,
each against the file as left by the previous edit."""
import io
import sys

T, M = sys.argv[1], sys.argv[2]
C = "src/cpus/cpu_arm.c"
I = "src/cpus/cpu_arm_instr.c"
D = "src/cpus/cpu_arm_instr_dpi.c"
NL, TB = chr(10), chr(9)

MSR_LATCHSET = TB * 3 + "cpu->cd.arm.mode_warned |= ARM_MODEWARN_MSR;" + NL
POP_LATCHSET = TB * 4 + "cpu->cd.arm.mode_warned |= ARM_MODEWARN_POP;" + NL
DPI_LATCHSET = TB * 4 + "cpu->cd.arm.mode_warned |= ARM_MODEWARN_DPI;" + NL
POP_GUARD = TB * 2 + "if (!arm_mode_is_modelled(new_cpsr)) {" + NL
MSR_GUARD = TB + "if ((mask & ARM_FLAG_MODE) && !arm_mode_is_modelled(ic->arg[0])) {" + NL
MSR_NEWVAL = TB + "uint32_t new_value = ic->arg[0];" + NL + NL + TB + "cpu->cd.arm.cpsr &= 0x0fffffff;"
MSR_DEC = TB * 2 + "mask &= ~ARM_FLAG_MODE;" + NL
CUR = "(cpu->cd.arm.cpsr & ARM_FLAG_MODE)"

MUT = {
    # ---- L: the LATCH-CLEAR decline on the RESTORE paths, at the (SPSR bit 0) polarity, bits 31:8.
    #      The contract claims "forcing it to 0 or to 1, with the latch clear or set".
    "N_pop_forceN_first": [(I, POP_LATCHSET, POP_LATCHSET + TB * 4 + "new_cpsr |= 0x80000000;" + NL)],
    "N_dpi_forceN_first": [(D, DPI_LATCHSET, DPI_LATCHSET + TB * 4 + "new_cpsr |= 0x80000000;" + NL)],
    "N_pop_orold_first": [(I, POP_LATCHSET, POP_LATCHSET + TB * 4 +
                           "new_cpsr |= cpu->cd.arm.cpsr & 0xffffff00;" + NL)],
    "N_dpi_orold_first": [(D, DPI_LATCHSET, DPI_LATCHSET + TB * 4 +
                           "new_cpsr |= cpu->cd.arm.cpsr & 0xffffff00;" + NL)],
    # ---- the force-0 twins (coordinator's request): predicted KILLED -- the first decline's SPSR has N SET
    "N_pop_clrN_first": [(I, POP_LATCHSET, POP_LATCHSET + TB * 4 + "new_cpsr &= ~0x80000000;" + NL)],
    "N_dpi_clrN_first": [(D, DPI_LATCHSET, DPI_LATCHSET + TB * 4 + "new_cpsr &= ~0x80000000;" + NL)],
    # ---- codex's label x latch x mode-bit cell: the msr decline clears only M[3:0] (bit 4 WRITTEN from
    #      the operand) at IRQ, on the latch-clear decline only
    "M_msr_clr0f_irq_first": [(I, MSR_GUARD, TB + "int opus_irqfirst = 0;" + NL + MSR_GUARD),
                              (I, MSR_LATCHSET, MSR_LATCHSET + TB * 3 + "opus_irqfirst = (" + CUR +
                               " == ARM_MODE_IRQ32);" + NL),
                              (I, MSR_DEC, TB * 2 + "mask &= opus_irqfirst ? ~0x0f : ~ARM_FLAG_MODE;" + NL)],
    # ---- the LATCH-CLEAR ACCEPT (every restore/MSR while the site's latch is clear forces N)
    "E_pop_forceN_clracc": [(I, POP_GUARD, TB * 2 + "if (!(cpu->cd.arm.mode_warned & ARM_MODEWARN_POP))" + NL +
                             TB * 3 + "new_cpsr |= 0x80000000;" + NL + POP_GUARD)],
    "E_msr_forceN_clracc": [(I, MSR_NEWVAL, TB + "uint32_t new_value = ic->arg[0] | ((cpu->cd.arm.mode_warned &"
                             " ARM_MODEWARN_MSR) ? 0 : 0x80000000);" + NL + NL + TB + "cpu->cd.arm.cpsr &= 0x0fffffff;")],
    # ---- control: the SAME latch-clear force-1 on the MSR decline (msr wide drives operand 0 there)
    "M_msr_forceN_first": [(I, MSR_GUARD, TB + "int opus_first = 0;" + NL + MSR_GUARD),
                           (I, MSR_LATCHSET, MSR_LATCHSET + TB * 3 + "opus_first = 1;" + NL),
                           (I, MSR_NEWVAL, TB + "uint32_t new_value = ic->arg[0] | (opus_first ? 0x80000000 : 0);" +
                            NL + NL + TB + "cpu->cd.arm.cpsr &= 0x0fffffff;")],
    # ---- msr guard skipped at ONE label x latch-clear cell (IRQ, first decline only)
    "M_msr_skip_irq_first": [(I, MSR_GUARD, TB + "if ((mask & ARM_FLAG_MODE) && !arm_mode_is_modelled(ic->arg[0]) &&" + NL +
                              TB + "    !(" + CUR + " == ARM_MODE_IRQ32 && !(cpu->cd.arm.mode_warned & ARM_MODEWARN_MSR))) {" + NL)],
    # ---- the cached translation, IMMEDIATE form: the decline rewrites ic->arg[0] to the current mode
    "M_msr_arg0cur": [(I, MSR_DEC, TB * 2 + "ic->arg[0] = (ic->arg[0] & ~ARM_FLAG_MODE) | " + CUR + ";" + NL + MSR_DEC)],
    # ---- glm's C1 (wave 2): the pop decline assigns the RIGHT CPSR word and then skips the PC load
    "M_pop_retafter": [(I, TB + "int i, return_flag = 0;" + NL, TB + "int i, return_flag = 0, opus_dec = 0;" + NL),
                       (I, TB * 3 + "    (cpu->cd.arm.cpsr & ARM_FLAG_MODE);" + NL + TB * 2 + "}" + NL + NL +
                        TB * 2 + "switch_register_banks",
                        TB * 3 + "    (cpu->cd.arm.cpsr & ARM_FLAG_MODE);" + NL + TB * 3 + "opus_dec = 1;" + NL +
                        TB * 2 + "}" + NL + NL + TB * 2 + "switch_register_banks"),
                       (I, TB + "/*  NOTE: Special case: Loading the PC  */" + NL,
                        TB + "if (opus_dec)" + NL + TB * 2 + "return;" + NL + TB +
                        "/*  NOTE: Special case: Loading the PC  */" + NL)],
    # ---- the cached translation, REGISTER form (Opus pass-2R4; 47/47 in killtable5 kt1b)
    "M_msr_argmask": [(I, MSR_DEC, TB * 2 + "ic->arg[1] &= ~ARM_FLAG_MODE;" + NL + MSR_DEC)],
}
LANES = {
    "LANE1": ["N_pop_forceN_first", "N_pop_clrN_first", "N_dpi_orold_first"],
    "LANE2": ["N_dpi_forceN_first", "N_dpi_clrN_first", "N_pop_orold_first"],
    "LANE3": ["E_pop_forceN_clracc", "E_msr_forceN_clracc", "M_msr_forceN_first"],
    "LANE4": ["M_msr_clr0f_irq_first", "M_msr_skip_irq_first"],
    "LANE5": ["M_msr_argmask", "M_msr_arg0cur"],
}
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
