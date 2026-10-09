#!/bin/bash
# opus5 seat, armmmuvehicle pass 1: build a PRIVATE scratch clone of GXEMUL-SEC's WORKING tree.
# READ-ONLY on every project tree: this only READS /mnt/c/.../GXEMUL-SEC and writes /tmp/gxopusmmuv.
set -u
SRC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
DST=/tmp/gxopusmmuv
LOG=/tmp/gxopusmmuv_build.log
rm -rf "$DST"
mkdir -p "$DST"
cd "$SRC" || exit 9
# copy sources only: top-level build files + src/ ; no .git, no regress artifacts, no objects
tar --exclude='*.o' -cf - configure Makefile.skel LICENSE README src \
  | tar -xf - -C "$DST"
cd "$DST" || exit 9
# objects and generator executables must not come across; rebuild everything
find . -name '*.o' -delete
for g in src/cpus/generate_*; do case "$g" in *.c) ;; *) rm -f "$g";; esac; done
rm -f src/include/make_ppc_spr_strings src/devices/fonts/Xconv_raw_to_c gxemul
echo "=== configure ===" > "$LOG"
./configure >> "$LOG" 2>&1 || { echo CONFIGURE_FAILED; tail -20 "$LOG"; exit 1; }
rm -f src/cpus/*.o
echo "=== make ===" >> "$LOG"
make -j8 >> "$LOG" 2>&1
RC=$?
echo "MAKE_RC=$RC"
ls -la --time-style=full-iso gxemul 2>&1
# freshness: binary newer than every source in the #562 set and memory_arm.c
for f in src/cpus/cpu_arm.c src/cpus/cpu_arm_instr.c src/cpus/cpu_arm_instr_dpi.c src/include/cpu_arm.h \
         src/cpus/memory_arm.c src/cpus/cpu_arm_coproc.c src/cpus/cpu_dyntrans.c src/debugger/debugger.c; do
  if [ gxemul -nt "$f" ]; then echo "FRESH  gxemul -nt $f"; else echo "STALE  gxemul NOT newer than $f"; fi
done
# source identity vs the working tree (cmp)
for f in src/cpus/cpu_arm.c src/cpus/cpu_arm_instr.c src/cpus/cpu_arm_instr_dpi.c src/include/cpu_arm.h \
         src/cpus/memory_arm.c src/cpus/cpu_arm_coproc.c src/cpus/cpu_dyntrans.c src/debugger/debugger.c \
         src/debugger/debugger_cmds.c src/core/memory.c src/cpus/memory_rw.c src/machines/machine_test.c; do
  if cmp -s "$f" "$SRC/$f"; then echo "CMP_OK $f"; else echo "CMP_DIFF $f"; fi
done
md5sum src/cpus/cpu_arm.c src/cpus/memory_arm.c gxemul
tail -3 "$LOG"
echo SETUP_DONE
