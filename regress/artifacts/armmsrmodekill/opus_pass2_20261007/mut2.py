import io, sys
T, M = sys.argv[1], sys.argv[2]
C = "src/cpus/cpu_arm.c"; I = "src/cpus/cpu_arm_instr.c"; D = "src/cpus/cpu_arm_instr_dpi.c"
TAB = chr(9); NL = chr(10)
MUT = {
    "O_msr_noconj": [(I, "if ((mask & ARM_FLAG_MODE) && !arm_mode_is_modelled(ic->arg[0])) {",
                      "if (!arm_mode_is_modelled(ic->arg[0])) {")],
    "O_latch_pop": [(I, TAB * 4 + "cpu->cd.arm.mode_warned |= ARM_MODEWARN_POP;" + NL, "")],
    "O_latch_dpi": [(D, TAB * 4 + "cpu->cd.arm.mode_warned |= ARM_MODEWARN_DPI;" + NL, "")],
    "O_latch_load": [(C, TAB * 3 + "cpu->cd.arm.mode_warned |= ARM_MODEWARN_LOAD;" + NL, "")],
}
if M == "LIST":
    print(" ".join(MUT)); sys.exit(0)
for f, a, b in MUT[M]:
    p = T + "/" + f; s = io.open(p, newline="").read(); n = s.count(a)
    if n != 1:
        print("MUTANT-TEXT-NOT-FOUND", M, f, n); sys.exit(3)
    io.open(p, "w", newline="").write(s.replace(a, b))
print("MUTANT-APPLIED", M)
