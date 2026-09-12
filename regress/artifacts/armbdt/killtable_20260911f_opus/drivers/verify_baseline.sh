#!/usr/bin/env bash
set -euo pipefail
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
REL=src/cpus/cpu_arm_instr.c
CLONE=/tmp/gxopus524c
git -C "$SEC" show 8d372aa:"$REL" > /tmp/opus524_baseline.c
echo "baseline bytes: $(wc -c < /tmp/opus524_baseline.c)"
printf 'clone currently == 8d372aa baseline? '
if cmp -s /tmp/opus524_baseline.c "$CLONE/$REL"; then echo YES; else echo NO; fi
printf 'unmasked-call count in baseline (want 2): '
grep -cF 'cpu->memory_rw(cpu, cpu->mem, addr, data,' /tmp/opus524_baseline.c || true
printf 'unmasked-call count in SEC working tree (want 0): '
grep -cF 'cpu->memory_rw(cpu, cpu->mem, addr, data,' "$SEC/$REL" || true
printf 'masked-call count in SEC working tree (want 2): '
grep -cF 'cpu->memory_rw(cpu, cpu->mem, addr & 0xfffffffc, data,' "$SEC/$REL" || true
