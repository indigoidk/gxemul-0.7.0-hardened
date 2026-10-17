#!/bin/bash
# delay-slot variants of m88k_exception()'s four delivered arms, measured against the shipped 59-row probe.
# Scratch clone /tmp/gxm88kds (never a project build tree).  Logs land beside this script (durable).
set -u
D=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/m88kexcdeliver/delayslot_20261016
C=/tmp/gxm88kds
rm -rf $C; mkdir -p $C; cd $C && tar xf /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/m88kds/head_7b23b785.tar || { echo "UNTAR FAILED"; exit 9; }
echo "== configure $(date '+%T')"; ./configure > $D/configure.out 2>&1 || { echo "CONFIGURE FAILED"; exit 9; }
echo "== build $(date '+%T')"; make -j8 > $D/build_base.out 2>&1; [ -x gxemul ] || { echo "BUILD FAILED"; tail -20 $D/build_base.out; exit 9; }
md5sum src/cpus/cpu_m88k.c gxemul | tee $D/base.md5
cp src/cpus/cpu_m88k.c $C/cpu_m88k.c.ORIG
echo "== baseline probe $(date '+%T')"; (cd regress && python3 -u m88k_exc_probe.py $C/gxemul) > $D/probe_BASE.out 2>&1; tail -3 $D/probe_BASE.out
for arm in MISALIGNED_ACCESS UNIMPLEMENTED_OPCODE PRIVILEGE_VIOLATION INTEGER_OVERFLOW; do
  for form in notds ds; do
    cp $C/cpu_m88k.c.ORIG src/cpus/cpu_m88k.c
    python3 - "$arm" "$form" <<'PY'
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
    make -j8 > $D/build_${arm}_${form}.out 2>&1
    if [ ! gxemul -nt src/cpus/cpu_m88k.c ]; then echo "STALE BINARY for $arm $form -- VOID"; continue; fi
    (cd regress && python3 -u m88k_exc_probe.py $C/gxemul) > $D/probe_${arm}_${form}.out 2>&1
    echo "== $arm $form: $(tail -1 $D/probe_${arm}_${form}.out)"
  done
done
cp $C/cpu_m88k.c.ORIG src/cpus/cpu_m88k.c; cmp -s src/cpus/cpu_m88k.c $C/cpu_m88k.c.ORIG && echo "clone restored (scratch only)"
echo "DELAYSLOT_DONE $(date '+%T')"
