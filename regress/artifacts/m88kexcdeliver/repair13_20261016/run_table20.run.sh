#!/bin/bash
# TABLE 20: probe v24 (frozen copy beside this script) -- BASE plus 38 mutants: the whole delay-slot x is_trap class on ONE
# instrument, and the two disclosed user-trap escapes.  Scratch clone /tmp/gxm88kv20.  A mutant is VOID unless mut20.py
# reports MUT20_OK, the source differs from HEAD's, and the binary is newer than the source.
set -u
D=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/m88kexcdeliver/repair13_20261016
S=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad
C=/tmp/gxm88kv20
HEADC=$S/m88kv20/cpu_m88k.c.HEAD
cd $C || exit 9
[ -e $C/.MUTANT ] && { echo "SENTINEL PRESENT -- abort"; exit 9; }
cmp -s src/cpus/cpu_m88k.c $HEADC || { echo "clone source is not HEAD -- abort"; exit 9; }
cp $D/m88k_exc_probe_v24.FROZEN.py regress/m88k_exc_probe.py; md5sum regress/m88k_exc_probe.py | tee $D/probe_v24.md5
rm -f src/cpus/cpu_m88k.o; make -j8 > $D/build_t20_base.out 2>&1
[ gxemul -nt src/cpus/cpu_m88k.c ] || { echo "BASE REBUILD STALE"; exit 9; }
(cd regress && python3 -u m88k_exc_probe.py $C/gxemul) > $D/t20_BASE.out 2>&1
echo "== 20 BASE: $(grep -o 'M88KEXC_RESULT=[0-9/]*' $D/t20_BASE.out)"
mut() {
  echo "MUTANT $1" > $C/.MUTANT
  cp $HEADC src/cpus/cpu_m88k.c
  if ! python3 $D/mut20.py "$1"; then echo "== 20 $1: MUTATION FAILED -- VOID"; return; fi
  if cmp -s src/cpus/cpu_m88k.c $HEADC; then echo "== 20 $1: SOURCE UNCHANGED -- VOID"; return; fi
  rm -f src/cpus/cpu_m88k.o; make -j8 > $D/build_t20_$1.out 2>&1
  if [ ! gxemul -nt src/cpus/cpu_m88k.c ]; then echo "== 20 $1: STALE BINARY -- VOID"; return; fi
  (cd regress && python3 -u m88k_exc_probe.py $C/gxemul) > $D/t20_$1.out 2>&1
  echo "== 20 $1: $(grep -o 'M88KEXC_RESULT=[0-9/]*' $D/t20_$1.out)"
}
for L in MISALIGNED_ACCESS UNIMPLEMENTED_OPCODE PRIVILEGE_VIOLATION ILLEGAL_INTEGER_DIVIDE INTEGER_OVERFLOW; do
  mut M_RRDS_$L; mut M_ARMTSU_$L
done
for L in MISALIGNED_ACCESS UNIMPLEMENTED_OPCODE PRIVILEGE_VIOLATION BOUNDS_CHECK_VIOLATION ILLEGAL_INTEGER_DIVIDE INTEGER_OVERFLOW ERROR; do
  mut M_ARMTS_$L; mut M_DSNOT_$L; mut M_DSFRZ_$L
done
for m in M_DS865 M_RRTDS M_RRNTDS M_FBDS M_FBFRZDS M_RRUT M_DS840UT; do
  mut $m
done
cp $HEADC src/cpus/cpu_m88k.c
if cmp -s src/cpus/cpu_m88k.c $HEADC; then rm -f $C/.MUTANT; echo "clone source restored (cmp vs HEAD clean); sentinel cleared"; else echo "*** RESTORE FAILED -- sentinel kept"; fi
echo "TABLE20_DONE $(date '+%T')"
