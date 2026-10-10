#!/bin/bash
# fable5 REGRESS seat for #562: build PARENT (04f3e7c0) and COMMIT (4f908ad5) from git-archive tarballs
# in a private WSL scratch dir.  Touches NO project tree.
set -u
S=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/c562/fable/work
D=/tmp/gxfable562
rm -rf "$D"; mkdir -p "$D"
for pair in "parent_04f3e7c0 parent" "commit_4f908ad5 commit"; do
  set -- $pair
  mkdir -p "$D/$2"
  echo "=== extract $1 -> $D/$2 $(date +%T)"
  tar -xf "$S/$1.tar" -C "$D/$2" --exclude='regress/artifacts' --exclude='regress/artifacts/*' ; echo "TAR_RC=$?"
  echo "=== configure $2 $(date +%T)"
  (cd "$D/$2" && ./configure > configure.log 2>&1; echo "CONFIGURE_RC=$?")
  echo "=== make $2 $(date +%T)"
  (cd "$D/$2" && make -j4 > make.log 2>&1; echo "MAKE_RC=$?")
  ls -la --time-style=full-iso "$D/$2/gxemul" "$D/$2/src/cpus/cpu_arm.c" 2>&1
  if [ "$D/$2/gxemul" -nt "$D/$2/src/cpus/cpu_arm.c" ]; then echo "$2: binary NEWER than cpu_arm.c  OK"; else echo "$2: binary NOT newer than cpu_arm.c  FAIL"; fi
  md5sum "$D/$2/src/cpus/cpu_arm.c" "$D/$2/src/cpus/cpu_arm_instr.c" "$D/$2/src/cpus/cpu_arm_instr_dpi.c" "$D/$2/src/include/cpu_arm.h" "$D/$2/regress/arm_msrmode_probe.py" 2>&1
done
echo "BUILD_DONE $(date +%T)"
