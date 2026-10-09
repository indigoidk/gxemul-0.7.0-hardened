#!/bin/bash
# opus5 seat: post-table clearance of the BASE scratch clone (never mutated: mutants were built in copies)
SRC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
B=/tmp/gxopusmmuv
for f in src/cpus/memory_arm.c src/cpus/cpu_arm.c src/cpus/cpu_arm_coproc.c src/cpus/cpu_dyntrans.c; do
  if cmp -s "$B/$f" "$SRC/$f"; then echo "CMP_OK $f"; else echo "CMP_DIFF $f"; fi
  if [ "$B/gxemul" -nt "$B/$f" ]; then echo "FRESH $f"; else echo "STALE $f"; fi
done
[ -e "$B/.MUTANT" ] && echo "BASE HAS .MUTANT (unexpected)" || echo "BASE no .MUTANT sentinel"
md5sum "$B/gxemul" /tmp/gxopusmmuv_bins/BASE | cut -c1-12,34-
ls -d /tmp/gxopusmmuv_M_* | while read d; do echo "$d: $(cat "$d/.MUTANT" 2>/dev/null)"; done
echo FINAL_CHECK_DONE
