#!/bin/bash
# opus5 seat: (re)build /tmp/gxopusmmuv after the experiments/ dir was added; then check freshness + identity.
set -u
SRC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
DST=/tmp/gxopusmmuv
LOG=/tmp/gxopusmmuv_build2.log
cd "$DST" || exit 9
rm -f src/cpus/*.o gxemul
make -j8 > "$LOG" 2>&1
RC=$?
echo "MAKE_RC=$RC"
grep -n -iE " error|\*\*\*" "$LOG" | head -10
ls -la --time-style=full-iso gxemul 2>&1
for f in src/cpus/cpu_arm.c src/cpus/cpu_arm_instr.c src/cpus/cpu_arm_instr_dpi.c src/include/cpu_arm.h \
         src/cpus/memory_arm.c src/cpus/cpu_arm_coproc.c src/cpus/cpu_dyntrans.c src/debugger/debugger.c; do
  if [ gxemul -nt "$f" ]; then echo "FRESH  gxemul -nt $f"; else echo "STALE  gxemul NOT newer than $f"; fi
done
for f in src/cpus/cpu_arm.c src/cpus/cpu_arm_instr.c src/cpus/cpu_arm_instr_dpi.c src/include/cpu_arm.h \
         src/cpus/memory_arm.c src/cpus/cpu_arm_coproc.c src/cpus/cpu_dyntrans.c src/debugger/debugger.c \
         src/debugger/debugger_cmds.c src/core/memory.c src/cpus/memory_rw.c src/machines/machine_test.c; do
  if cmp -s "$f" "$SRC/$f"; then echo "CMP_OK $f"; else echo "CMP_DIFF $f"; fi
done
md5sum src/cpus/cpu_arm.c src/cpus/memory_arm.c gxemul
echo MAKE_DONE
