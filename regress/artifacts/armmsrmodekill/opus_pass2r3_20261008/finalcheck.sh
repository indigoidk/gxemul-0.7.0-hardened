ls /tmp/gxopus562r3/*/tree/.MUTANT 2>&1
for l in 1 2 3 4 5; do for f in src/cpus/cpu_arm.c src/cpus/cpu_arm_instr.c src/cpus/cpu_arm_instr_dpi.c src/include/cpu_arm.h; do
 cmp -s /tmp/gxopus562r3/LANE$l/tree/$f /mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/$f || echo DIRTY $l $f; done; done; echo cmpdone
