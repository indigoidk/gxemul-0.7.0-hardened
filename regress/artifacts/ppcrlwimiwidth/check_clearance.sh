#!/bin/bash
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/cpus/cpu_ppc_instr.c

printf "%-22s %-25s %-25s\n" "Tree" "Part 1 (cmp -s vs SEC)" "Part 2 (binary -nt source)"
printf "%-22s %-25s %-25s\n" "----------------------" "-------------------------" "-------------------------"

# est/
if cmp -s "$SEC" /mnt/c/DocumentNoSnc/CC/GXEMUL/est/src/cpus/cpu_ppc_instr.c; then
    p1="CLEAN"
else
    p1="FAIL"
fi
p2="N/A"
printf "%-22s %-25s %-25s\n" "est/" "$p1" "$p2"

# build/
if cmp -s "$SEC" /mnt/c/DocumentNoSnc/CC/GXEMUL/build/src/cpus/cpu_ppc_instr.c; then
    p1="CLEAN"
else
    p1="FAIL"
fi
if [ /mnt/c/DocumentNoSnc/CC/GXEMUL/build/gxemul -nt /mnt/c/DocumentNoSnc/CC/GXEMUL/build/src/cpus/cpu_ppc_instr.c ]; then
    p2="FRESH"
else
    p2="STALE"
fi
printf "%-22s %-25s %-25s\n" "build/" "$p1" "$p2"

# build-asan/
if cmp -s "$SEC" /mnt/c/DocumentNoSnc/CC/GXEMUL/build-asan/src/cpus/cpu_ppc_instr.c; then
    p1="CLEAN"
else
    p1="FAIL"
fi
if [ /mnt/c/DocumentNoSnc/CC/GXEMUL/build-asan/gxemul -nt /mnt/c/DocumentNoSnc/CC/GXEMUL/build-asan/src/cpus/cpu_ppc_instr.c ]; then
    p2="FRESH"
else
    p2="STALE"
fi
printf "%-22s %-25s %-25s\n" "build-asan/" "$p1" "$p2"

# /tmp/gxsec-build
if cmp -s "$SEC" /tmp/gxsec-build/src/cpus/cpu_ppc_instr.c; then
    p1="CLEAN"
else
    p1="FAIL"
fi
if [ /tmp/gxsec-build/gxemul -nt /tmp/gxsec-build/src/cpus/cpu_ppc_instr.c ]; then
    p2="FRESH"
else
    p2="STALE"
fi
printf "%-22s %-25s %-25s\n" "/tmp/gxsec-build" "$p1" "$p2"
