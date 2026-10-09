import io, sys
T, M = sys.argv[1], sys.argv[2]
C="src/cpus/cpu_arm.c"; I="src/cpus/cpu_arm_instr.c"; D="src/cpus/cpu_arm_instr_dpi.c"
MUT = {
 "O_latch_msr": [(I, "\t\t\tcpu->cd.arm.mode_warned |= ARM_MODEWARN_MSR;\n", "")],
 "O_mask_nibble": [(I, "\t\tmask &= ~ARM_FLAG_MODE;\n", "\t\tmask &= ~0x0f;\n")],
 "O_dpi_svconly": [(D, "if (spsr_copied && !arm_mode_is_modelled(new_cpsr)) {",
                   "if (spsr_copied && cur_mode == ARM_MODE_SVC32 &&\n\t\t    !arm_mode_is_modelled(new_cpsr)) {")],
 "O_pop_svconly": [(I, "\t\tif (!arm_mode_is_modelled(new_cpsr)) {",
                   "\t\tif ((cpu->cd.arm.cpsr & ARM_FLAG_MODE) == ARM_MODE_SVC32 &&\n\t\t    !arm_mode_is_modelled(new_cpsr)) {")],
}
if M == "LIST": print(" ".join(MUT)); sys.exit(0)
for f,a,b in MUT[M]:
    p=T+"/"+f; s=io.open(p,newline="").read(); n=s.count(a)
    if n!=1: print("MUTANT-TEXT-NOT-FOUND",M,f,n); sys.exit(3)
    io.open(p,"w",newline="").write(s.replace(a,b))
print("MUTANT-APPLIED",M)
