#!/usr/bin/env python3
"""mutate.py <tree> <mutant> -- apply one #562 kill-table mutant to <tree>/src.  Every find-text
must occur EXACTLY ONCE (a presence pin); otherwise exit 3 (MUTANT-TEXT-NOT-FOUND = FAIL)."""
import io
import sys

T, M = sys.argv[1], sys.argv[2]
C = "src/cpus/cpu_arm.c"
I = "src/cpus/cpu_arm_instr.c"
D = "src/cpus/cpu_arm_instr_dpi.c"
H = "src/include/cpu_arm.h"

LOAD_LATCH = """		if (!(cpu->cd.arm.mode_warned & ARM_MODEWARN_LOAD)) {
			cpu->cd.arm.mode_warned |= ARM_MODEWARN_LOAD;
			fatal("arm_load_register_bank: unimplemented mode %i;"
			    " registers not loaded (once)\\n",
			    cpu->cd.arm.cpsr & ARM_FLAG_MODE);
		}
		return;"""
SAVE_LATCH = LOAD_LATCH.replace("LOAD", "SAVE").replace("load", "save").replace(
    "not saveed", "not saved")
SAVE_LATCH = """		if (!(cpu->cd.arm.mode_warned & ARM_MODEWARN_SAVE)) {
			cpu->cd.arm.mode_warned |= ARM_MODEWARN_SAVE;
			fatal("arm_save_register_bank: unimplemented mode %i;"
			    " registers not saved (once)\\n",
			    cpu->cd.arm.cpsr & ARM_FLAG_MODE);
		}
		return;"""
HEAD_LOAD = """		fatal("arm_load_register_bank: unimplemented mode %i\\n",
		    cpu->cd.arm.cpsr & ARM_FLAG_MODE);
		exit(1);"""
HEAD_SAVE = HEAD_LOAD.replace("load", "save")

MUT = {
    # clause (b): VERBATIM reinstatement of HEAD's arm body, one fixed site each
    "M_load_exit": [(C, LOAD_LATCH, HEAD_LOAD)],
    "M_save_exit": [(C, SAVE_LATCH, HEAD_SAVE)],
    # latch kept, exit(1) in place of return
    "M_load_exit_latched": [(C, LOAD_LATCH, LOAD_LATCH.replace("return;", "exit(1);"))],
    "M_save_exit_latched": [(C, SAVE_LATCH, SAVE_LATCH.replace("return;", "exit(1);"))],
    # helper
    "M_helper_always1": [(C, "\tdefault:return 0;\n\t}\n}", "\tdefault:return 1;\n\t}\n}")],
    "M_helper_range": [(C, "\tswitch (mode & ARM_FLAG_MODE) {\n\tcase ARM_MODE_USR32:\n\tcase ARM_MODE_SYS32:\n\tcase ARM_MODE_FIQ32:",
                        "\tmode &= ARM_FLAG_MODE;\n\tif ((mode >= 0x10 && mode <= 0x13) || mode == 0x17 || mode >= 0x1b)\n\t\treturn 1;\n\tswitch (mode & ARM_FLAG_MODE) {\n\tcase ARM_MODE_USR32:\n\tcase ARM_MODE_SYS32:\n\tcase ARM_MODE_FIQ32:")],
    # guards dropped
    "M_drop_msr": [(I, "if ((mask & ARM_FLAG_MODE) && !arm_mode_is_modelled(ic->arg[0])) {",
                    "if (0 && (mask & ARM_FLAG_MODE) && !arm_mode_is_modelled(ic->arg[0])) {")],
    "M_drop_pop": [(I, "\t\tif (!arm_mode_is_modelled(new_cpsr)) {", "\t\tif (0) {")],
    "M_drop_dpi": [(D, "if (spsr_copied && !arm_mode_is_modelled(new_cpsr)) {", "if (0) {")],
    # restore guard unconditional (always keep the current mode)
    "M_uncond_both": [(I, "\t\tif (!arm_mode_is_modelled(new_cpsr)) {", "\t\tif (1) {"),
                      (D, "if (spsr_copied && !arm_mode_is_modelled(new_cpsr)) {", "if (spsr_copied) {")],
    "M_uncond_pop": [(I, "\t\tif (!arm_mode_is_modelled(new_cpsr)) {", "\t\tif (1) {")],
    "M_uncond_dpi": [(D, "if (spsr_copied && !arm_mode_is_modelled(new_cpsr)) {", "if (spsr_copied) {")],
    # whole-operation decline in msr_imm
    "M_wholeop_msr": [(I, "\t\tmask &= ~ARM_FLAG_MODE;\n\t}\n\n\tint switch_register_banks",
                       "\t\treturn;\n\t}\n\n\tint switch_register_banks")],
    # latch sharing
    "M_shared_latch": [(H, "#define\tARM_MODEWARN_POP\t0x02", "#define\tARM_MODEWARN_POP\t0x01"),
                       (H, "#define\tARM_MODEWARN_DPI\t0x04", "#define\tARM_MODEWARN_DPI\t0x01"),
                       (H, "#define\tARM_MODEWARN_SAVE\t0x08", "#define\tARM_MODEWARN_SAVE\t0x01"),
                       (H, "#define\tARM_MODEWARN_LOAD\t0x10", "#define\tARM_MODEWARN_LOAD\t0x01")],
    "M_shared_saveload": [(H, "#define\tARM_MODEWARN_LOAD\t0x10", "#define\tARM_MODEWARN_LOAD\t0x08")],
    "M_shared_msrpop": [(H, "#define\tARM_MODEWARN_POP\t0x02", "#define\tARM_MODEWARN_POP\t0x01")],
    "M_shared_msrdpi": [(H, "#define\tARM_MODEWARN_DPI\t0x04", "#define\tARM_MODEWARN_DPI\t0x01")],
    "M_shared_popdpi": [(H, "#define\tARM_MODEWARN_DPI\t0x04", "#define\tARM_MODEWARN_DPI\t0x02")],
    # DPI helper called even when no SPSR was copied
    "M_dpi_uncond_call": [(D, "if (spsr_copied && !arm_mode_is_modelled(new_cpsr)) {",
                           "if (!arm_mode_is_modelled(new_cpsr)) {")],
    # arm_pop: copy the neighbouring default: arm's `return' (skips the PC load)
    "M_pop_return": [(I, "\t\t\tnew_cpsr = (new_cpsr & ~ARM_FLAG_MODE) |\n\t\t\t    (cpu->cd.arm.cpsr & ARM_FLAG_MODE);\n\t\t}",
                      "\t\t\tnew_cpsr = (new_cpsr & ~ARM_FLAG_MODE) |\n\t\t\t    (cpu->cd.arm.cpsr & ARM_FLAG_MODE);\n\t\t\treturn;\n\t\t}")],
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
