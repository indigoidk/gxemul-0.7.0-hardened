#!/bin/bash
# build_fixed_clone.sh -- /tmp/gxfix576 = /tmp/gxdivw (HEAD 987cb596) + the #576 one-line fix, built in WSL.  Scratch clone only.
set -u
B=/tmp/gxdivw; F=/tmp/gxfix576
rm -rf "$F"; cp -a "$B" "$F"; cd "$F" || exit 1
echo "MUTANT: src/cpus/cpu_sh_instr.c #576 fix (scratch clone, intentional)" > .MUTANT
python3 - <<'PY'
import io
p="/tmp/gxfix576/src/cpus/cpu_sh_instr.c"
s=io.open(p,encoding="utf-8").read()
old="\tieee_interpret_float_value(cpu->cd.sh.fpul, &op1, IEEE_FMT_S);\n\tcpu->cd.sh.fpul = (int32_t) op1.f;\n"
new=("\tieee_interpret_float_value(cpu->cd.sh.fpul, &op1, IEEE_FMT_S);\n"
     "\t/*  #576: FCNVSD reads FPUL and writes DRn only (sh4_programming.txt\n"
     "\t    9.29, :10866-10871).  Upstream also stored (int32_t) op1.f into\n"
     "\t    fpul here -- the FTRC store, mis-copied -- so a guest reading FPUL\n"
     "\t    after an FCNVSD saw a truncated integer.  Removed; nothing else in\n"
     "\t    this handler changes.  */\n")
assert s.count(old)==1, s.count(old)
io.open(p,"w",encoding="utf-8",newline="\n").write(s.replace(old,new))
print("fix applied")
PY
rm -f src/cpus/cpu_sh*.o
make -j4 > make_fix.log 2>&1; rc=$?; echo "make rc=$rc"
if [ -x gxemul ] && [ gxemul -nt src/cpus/cpu_sh_instr.c ]; then echo "BINARY_FRESH $(ls -la --time-style=+%T gxemul | awk '{print $5, $6}')"; else echo "BINARY_STALE_OR_MISSING"; tail -5 make_fix.log; fi
diff "$B/src/cpus/cpu_sh_instr.c" "$F/src/cpus/cpu_sh_instr.c" | head -20
