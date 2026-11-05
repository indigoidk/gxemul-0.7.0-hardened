#!/bin/bash
# table3_575.sh -- #575 ppccrandcorc TEST-VARIANT TABLE 3 (70 rows; repair 3).  PRETABLE_3.out must exist first (its mtime precedes table3/'s files).
# Mutates ONLY the WSL scratch clone /tmp/gx575t3 (a cp -a of build/) under a clone-local .MUTANT sentinel.  Legs: base (the fix), HEAD
# (impl_20261105/cpu_ppc_instr.c.pre575: the tree without the #575 edit), three null media; then the variants of v575c.py (table 2's 27
# re-created, then the round-3 representatives).  The probe prints no RED line, so each red set is read off its FAIL rows.  Restore = the
# fix, cmp-checked against GXEMUL-SEC and rebuilt fresh (binary newer than the source) before the sentinel is cleared.
set -u
G=/mnt/c/DocumentNoSnc/cc/GXEMUL
SEC=$G/GXEMUL-SEC
A=$SEC/regress/artifacts/ppccrandcorc
OUT=$A/r3_20261105/table3
P=$OUT/probe70_frozen.py
FIX=$SEC/src/cpus/cpu_ppc_instr.c
PRE=$A/impl_20261105/cpu_ppc_instr.c.pre575
C=/tmp/gx575t3
S1=src/cpus/cpu_ppc_instr.c
mkdir -p $OUT
log(){ echo "$(date +%H:%M:%S) $*" | tee -a $OUT/TABLE.log; }
[ -f $A/r3_20261105/PRETABLE_3.out ] || { log "ABORT: no PRETABLE_3.out"; exit 2; }
[ -f $P ] || { log "ABORT: no frozen probe ($P: copy base70/probe70_run.py there, cmp-identical to the in-tree probe)"; exit 2; }
cmp -s $P $SEC/regress/ppc_crlogic_probe.py || { log "ABORT: frozen probe differs from the in-tree probe"; exit 2; }
rm -rf $C && cp -a $G/build $C || { log "ABORT: clone failed"; exit 3; }
cd $C || exit 3
echo "$S1: #575 table 3; baseline GXEMUL-SEC" > .MUTANT
cp $FIX $OUT/cpu_ppc_instr.c.fix575
cmp -s $S1 $FIX || { log "ABORT: clone baseline is not the fix (propagate first)"; exit 4; }
md5sum $P $FIX $PRE $A/r3_20261105/variants/*.c $A/r3_20261105/PRETABLE_3.out > $OUT/MD5.txt; : > $OUT/SCORES.txt
build(){ rm -f src/cpus/cpu_ppc*.o; make -j4 > $OUT/build_$1.log 2>&1; local rc=$?
         [ $rc = 0 ] && [ src/cpus/cpu_ppc.o -nt $S1 ] && [ gxemul -nt src/cpus/cpu_ppc.o ] && return 0
         log "build $1 rc=$rc NOT FRESH"; return 1; }
run(){ python3 -u $P "$2" "$1" > $OUT/probe_$1.out 2>&1
       local r=$(grep -h "^PPC_CRLOGIC_RESULT=" $OUT/probe_$1.out | cut -d= -f2) c=$(grep -h "^PPC_CRLOGIC_CONTROL=" $OUT/probe_$1.out | cut -d= -f2)
       local d=$(grep -c "^PPC_CRLOGIC_PROBE_DONE" $OUT/probe_$1.out)
       local red=$(grep -E ' FAIL$' $OUT/probe_$1.out | cut -c1-19 | sed 's/ *$//; s/ /_/g' | paste -sd, -)
       echo "$1 [70 rows] ${r:-none} CONTROL=${c:-none} DONE=$d RED=${red:-none}" >> $OUT/SCORES.txt; log "$1 ${r:-none} RED=${red:-none}"; }
build base && run base $C/gxemul
cp $PRE $S1; build HEAD && run HEAD $C/gxemul
run null_true /bin/true; run null_absent /nonexistent/gxemul; run null_false /bin/false
for v in $A/r3_20261105/variants/*.c; do n=$(basename $v .c)
  cp $v $S1
  if build $n; then run $n $C/gxemul; else echo "$n [70 rows] BUILD-FAILED" >> $OUT/SCORES.txt; fi
done
cp $FIX $S1; build restored && run restored $C/gxemul
if cmp -s $S1 $FIX && [ gxemul -nt $S1 ]; then rm -f .MUTANT; log "restored: cmp clean vs SEC, binary fresh, sentinel cleared"
else log "RESTORE NOT VERIFIED -- sentinel kept"; fi
log TABLE3_575_DONE
