#!/bin/bash
# TABLE 17: three delay-slot mutants at the two non-arm sites (the SFRZ re-route and the fallback), on the committed-form
# v20 probe.  Same scratch clone /tmp/gxm88kv20, run strictly AFTER gate 11 finished with it.  Sentinel + cmp restore.
# A mutant is VOID unless mut17.py reports MUT17_OK AND the mutated source differs from HEAD's (cmp) AND the binary is
# newer than the source -- the first draft had none of the first two and would have scored BASE as an escape.
set -u
D=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/m88kexcdeliver/repair13_20261016
S=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad
C=/tmp/gxm88kv20
HEADC=$S/m88kv20/cpu_m88k.c.HEAD
cd $C || exit 9
[ -e $C/.MUTANT ] && { echo "SENTINEL PRESENT -- abort"; exit 9; }
cmp -s src/cpus/cpu_m88k.c $HEADC || { echo "clone source is not HEAD -- abort"; exit 9; }
cp $D/m88k_exc_probe_v20final.FROZEN.py regress/m88k_exc_probe.py; md5sum regress/m88k_exc_probe.py
rm -f src/cpus/cpu_m88k.o; make -j8 > $D/build_t17_base.out 2>&1
[ gxemul -nt src/cpus/cpu_m88k.c ] || { echo "BASE REBUILD STALE"; exit 9; }
(cd regress && python3 -u m88k_exc_probe.py $C/gxemul) > $D/t17_BASE.out 2>&1
echo "== 17 BASE: $(grep -o 'M88KEXC_RESULT=[0-9/]*' $D/t17_BASE.out)"
mut() {   # $1 tag
  echo "MUTANT $1" > $C/.MUTANT
  cp $HEADC src/cpus/cpu_m88k.c
  if ! python3 $D/mut17.py "$1"; then echo "== 17 $1: MUTATION FAILED -- VOID"; return; fi
  if cmp -s src/cpus/cpu_m88k.c $HEADC; then echo "== 17 $1: SOURCE UNCHANGED -- VOID"; return; fi
  rm -f src/cpus/cpu_m88k.o; make -j8 > $D/build_t17_$1.out 2>&1
  if [ ! gxemul -nt src/cpus/cpu_m88k.c ]; then echo "== 17 $1: STALE BINARY -- VOID"; return; fi
  (cd regress && python3 -u m88k_exc_probe.py $C/gxemul) > $D/t17_$1.out 2>&1
  echo "== 17 $1: $(grep -o 'M88KEXC_RESULT=[0-9/]*' $D/t17_$1.out)"
}
mut M_RRNTDS
mut M_RRTDS
mut M_FBDS
cp $HEADC src/cpus/cpu_m88k.c
if cmp -s src/cpus/cpu_m88k.c $HEADC; then rm -f $C/.MUTANT; echo "clone source restored (cmp vs HEAD clean); sentinel cleared"; else echo "*** RESTORE FAILED -- sentinel kept"; fi
echo "TABLE17_DONE $(date '+%T')"
