#!/bin/bash
# TABLE 16b: the committed-form v20 probe (frozen copy beside this script) -- BASE on HEAD and one joint re-route mutant.
# Same scratch clone as table 16 (/tmp/gxm88kv20), run strictly AFTER it.  Sentinel + cmp-vs-HEAD restore as before.
set -u
D=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/m88kexcdeliver/repair13_20261016
S=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad
C=/tmp/gxm88kv20
HEADC=$S/m88kv20/cpu_m88k.c.HEAD
cd $C || { echo "NO CLONE"; exit 9; }
[ -e $C/.MUTANT ] && { echo "clone carries a sentinel from table 16 -- abort"; exit 9; }
cmp -s src/cpus/cpu_m88k.c $HEADC || { echo "clone source is not HEAD -- abort"; exit 9; }
cp $D/m88k_exc_probe_v20final.FROZEN.py regress/m88k_exc_probe.py; md5sum regress/m88k_exc_probe.py | tee $D/probe_v20final.md5
rm -f src/cpus/cpu_m88k.o; make -j8 > $D/build_16b_base.out 2>&1
[ gxemul -nt src/cpus/cpu_m88k.c ] || { echo "BASE REBUILD STALE"; exit 9; }
md5sum src/cpus/cpu_m88k.c gxemul | tee $D/base16b.md5
(cd regress && python3 -u m88k_exc_probe.py $C/gxemul) > $D/t16b_BASE.out 2>&1
echo "== 16b BASE: $(grep -o 'M88KEXC_RESULT=[0-9/]*' $D/t16b_BASE.out) $(tail -1 $D/t16b_BASE.out)"
echo "MUTANT M_RRTRAPJOINT" > $C/.MUTANT
cp $HEADC src/cpus/cpu_m88k.c
python3 - <<'PY'
import io
p = "src/cpus/cpu_m88k.c"
t = io.open(p, encoding="utf-8", newline="").read()
old = "\t\tif (!is_trap) {\n\t\t\tvector = M88K_EXCEPTION_ERROR;"
new = ("\t\tif (!is_trap || ((cpu->cd.m88k.cr[M88K_CR_PSR] & M88K_PSR_MODE) && "
       "!(cpu->cd.m88k.cr[M88K_CR_PSR] & M88K_PSR_SFD1))) {\n\t\t\tvector = M88K_EXCEPTION_ERROR;")
assert t.count(old) == 1, t.count(old)
io.open(p, "w", encoding="utf-8", newline="").write(t.replace(old, new))
print("mutated: the SFRZ re-route also takes a frozen TRAP when MODE is set and SFD1 is clear")
PY
rm -f src/cpus/cpu_m88k.o; make -j8 > $D/build_16b_joint.out 2>&1
if [ gxemul -nt src/cpus/cpu_m88k.c ]; then
  (cd regress && python3 -u m88k_exc_probe.py $C/gxemul) > $D/t16b_M_RRTRAPJOINT.out 2>&1
  echo "== 16b M_RRTRAPJOINT: $(grep -o 'M88KEXC_RESULT=[0-9/]*' $D/t16b_M_RRTRAPJOINT.out)"
else echo "== 16b M_RRTRAPJOINT: STALE BINARY -- VOID"; fi
cp $HEADC src/cpus/cpu_m88k.c
if cmp -s src/cpus/cpu_m88k.c $HEADC; then rm -f $C/.MUTANT; echo "clone source restored (cmp vs HEAD clean); sentinel cleared"; else echo "*** RESTORE FAILED -- sentinel kept"; fi
echo "TABLE16B_DONE $(date '+%T')"
