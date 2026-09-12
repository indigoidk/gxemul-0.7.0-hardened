#!/usr/bin/env bash
for i in $(seq 1 120); do
  if ! pgrep -f '[c]ontrol_run.sh' > /dev/null; then echo CONTROL_FINISHED; break; fi
  sleep 5
done
for f in /tmp/opus524_out/ldmdb_*.out; do echo "### $f"; cat "$f"; done
echo "--- sentinel:"; ls -la /tmp/gxopus524c/.MUTANT 2>&1 | head -1
echo "--- clone source == 8d372aa?"
git -C /mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC show 8d372aa:src/cpus/cpu_arm_instr.c | cmp -s - /tmp/gxopus524c/src/cpus/cpu_arm_instr.c && echo YES || echo NO
