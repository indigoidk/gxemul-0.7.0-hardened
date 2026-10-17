#!/bin/bash
# TABLE 19b: Fable 5.1's two predicted v22 sweeps, MEASURED on v22 (m88k_exc_probe_v20final.FROZEN.py = probe v22; see
# NAMING.txt) -- seven M_DSFRZ_<L> and M_DS865.  Same scratch clone /tmp/gxm88kv20, strictly after table 19.
set -u
D=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/m88kexcdeliver/repair13_20261016
S=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad
C=/tmp/gxm88kv20
HEADC=$S/m88kv20/cpu_m88k.c.HEAD
cd $C || exit 9
[ -e $C/.MUTANT ] && { echo "SENTINEL PRESENT -- abort"; exit 9; }
cmp -s src/cpus/cpu_m88k.c $HEADC || { echo "clone source is not HEAD -- abort"; exit 9; }
cp $D/m88k_exc_probe_v20final.FROZEN.py regress/m88k_exc_probe.py; md5sum regress/m88k_exc_probe.py
rm -f src/cpus/cpu_m88k.o; make -j8 > $D/build_t19b_base.out 2>&1
[ gxemul -nt src/cpus/cpu_m88k.c ] || { echo "BASE REBUILD STALE"; exit 9; }
(cd regress && python3 -u m88k_exc_probe.py $C/gxemul) > $D/t19b_BASE.out 2>&1
echo "== 19b BASE: $(grep -o 'M88KEXC_RESULT=[0-9/]*' $D/t19b_BASE.out)"
mut() {
  echo "MUTANT $1" > $C/.MUTANT
  cp $HEADC src/cpus/cpu_m88k.c
  if ! python3 $D/mut19.py "$1"; then echo "== 19b $1: MUTATION FAILED -- VOID"; return; fi
  if cmp -s src/cpus/cpu_m88k.c $HEADC; then echo "== 19b $1: SOURCE UNCHANGED -- VOID"; return; fi
  rm -f src/cpus/cpu_m88k.o; make -j8 > $D/build_t19b_$1.out 2>&1
  if [ ! gxemul -nt src/cpus/cpu_m88k.c ]; then echo "== 19b $1: STALE BINARY -- VOID"; return; fi
  (cd regress && python3 -u m88k_exc_probe.py $C/gxemul) > $D/t19b_$1.out 2>&1
  echo "== 19b $1: $(grep -o 'M88KEXC_RESULT=[0-9/]*' $D/t19b_$1.out)"
}
for L in MISALIGNED_ACCESS UNIMPLEMENTED_OPCODE PRIVILEGE_VIOLATION BOUNDS_CHECK_VIOLATION ILLEGAL_INTEGER_DIVIDE INTEGER_OVERFLOW ERROR; do
  mut M_DSFRZ_$L
done
mut M_DS865
cp $HEADC src/cpus/cpu_m88k.c
if cmp -s src/cpus/cpu_m88k.c $HEADC; then rm -f $C/.MUTANT; echo "clone source restored (cmp vs HEAD clean); sentinel cleared"; else echo "*** RESTORE FAILED -- sentinel kept"; fi
echo "TABLE19B_DONE $(date '+%T')"
