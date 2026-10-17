#!/bin/bash
# m88kexcdeliver repair 13, TABLE 16: the v20 probe (frozen copy beside this script) against HEAD 7b23b785 and eleven
# mutants of m88k_exception()'s switch-1 arms.  Scratch clone /tmp/gxm88kv20 -- never a project build tree.  Clone-local
# sentinel; restore verified by cmp against HEAD's cpu_m88k.c (exported from git, not the script's own backup).
set -u
D=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/m88kexcdeliver/repair13_20261016
S=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad
C=/tmp/gxm88kv20
HEADC=$S/m88kv20/cpu_m88k.c.HEAD
rm -rf $C; mkdir -p $C; cd $C && tar xf $S/m88kds/head_7b23b785.tar || { echo "UNTAR FAILED"; exit 9; }
cmp -s src/cpus/cpu_m88k.c $HEADC || { echo "BASELINE IS NOT HEAD -- abort"; exit 9; }
cp $D/m88k_exc_probe_v20.FROZEN.py regress/m88k_exc_probe.py
md5sum regress/m88k_exc_probe.py | tee $D/probe_v20.md5
echo "== configure $(date '+%T')"; ./configure > $D/configure.out 2>&1 || { echo "CONFIGURE FAILED"; exit 9; }
echo "== build $(date '+%T')"; make -j8 > $D/build_base.out 2>&1
[ -x gxemul ] && [ gxemul -nt src/cpus/cpu_m88k.c ] || { echo "BASE BUILD FAILED OR STALE"; tail -20 $D/build_base.out; exit 9; }
md5sum src/cpus/cpu_m88k.c gxemul | tee $D/base.md5
echo "== BASE probe $(date '+%T')"; (cd regress && python3 -u m88k_exc_probe.py $C/gxemul) > $D/t16_BASE.out 2>&1
echo "== BASE: $(grep -o 'M88KEXC_RESULT=[0-9/]*' $D/t16_BASE.out) $(tail -1 $D/t16_BASE.out)"
run_mut() {   # $1 = arm (M88K_EXCEPTION_<arm>), $2 = notds|ds, $3 = tag
  echo "MUTANT $3" > $C/.MUTANT
  cp $HEADC src/cpus/cpu_m88k.c
  python3 - "$1" "$2" <<'PY'
import sys, io
arm, form = sys.argv[1], sys.argv[2]
p = "src/cpus/cpu_m88k.c"
t = io.open(p, encoding="utf-8", newline="").read().split("\n")
i = next(k for k, l in enumerate(t) if l.strip() == "case M88K_EXCEPTION_%s:" % arm)
j = next(k for k in range(i, i + 6) if "implemented = true;" in t[k])
new = "!cpu->delay_slot" if form == "notds" else "cpu->delay_slot ? true : false"
t[j] = t[j].replace("implemented = true;", "implemented = %s;" % new)
io.open(p, "w", encoding="utf-8", newline="").write("\n".join(t))
print("mutated line %d: %s" % (j + 1, t[j].strip()))
PY
  rm -f src/cpus/cpu_m88k.o
  make -j8 > $D/build_$3.out 2>&1
  if [ ! gxemul -nt src/cpus/cpu_m88k.c ]; then echo "== $3: STALE BINARY -- VOID"; return; fi
  (cd regress && python3 -u m88k_exc_probe.py $C/gxemul) > $D/t16_$3.out 2>&1
  echo "== $3: $(grep -o 'M88KEXC_RESULT=[0-9/]*' $D/t16_$3.out)  red: $(grep -E '^M88KEXC_ROW=' $D/t16_$3.out | grep -v -E 'RESULT=(DELIVER|DONE)' | awk '{print $1"/"$2}' | sed 's/M88KEXC_ROW=//; s/RESULT=//' | tr '\n' ' ')"
}
for arm in MISALIGNED_ACCESS UNIMPLEMENTED_OPCODE PRIVILEGE_VIOLATION INTEGER_OVERFLOW ILLEGAL_INTEGER_DIVIDE BOUNDS_CHECK_VIOLATION ERROR; do
  run_mut $arm notds M_DSNOT_$arm
done
for arm in MISALIGNED_ACCESS UNIMPLEMENTED_OPCODE PRIVILEGE_VIOLATION INTEGER_OVERFLOW; do
  run_mut $arm ds M_DS_$arm
done
cp $HEADC src/cpus/cpu_m88k.c
if cmp -s src/cpus/cpu_m88k.c $HEADC; then rm -f $C/.MUTANT; echo "clone source restored (cmp vs HEAD clean); sentinel cleared (scratch clone only)"; else echo "*** RESTORE FAILED -- sentinel kept"; fi
echo "TABLE16_DONE $(date '+%T')"
