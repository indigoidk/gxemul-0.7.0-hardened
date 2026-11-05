#!/bin/bash
# table1_575.sh -- #575 ppccrandcorc TEST-VARIANT TABLE 1 (62 rows).  PRETABLE.out must exist first (its mtime precedes table1/'s files).
# Mutates ONLY the WSL scratch clone /tmp/gx575t (a cp -a of build/) under a clone-local .MUTANT sentinel.  Legs: base (the fix), HEAD
# (impl_20261105/cpu_ppc_instr.c.pre575: the tree without the #575 edit), three null media; then the 15 variants of v575.py.  The probe
# prints no RED line, so each red set is read off its FAIL rows.  Restore = the fix, cmp-checked against GXEMUL-SEC and rebuilt fresh
# before the sentinel is cleared.
set -u
G=/mnt/c/DocumentNoSnc/cc/GXEMUL
SEC=$G/GXEMUL-SEC
A=$SEC/regress/artifacts/ppccrandcorc
OUT=$A/table1_20261105/table1
P=$OUT/probe62_frozen.py
FIX=$SEC/src/cpus/cpu_ppc_instr.c
PRE=$A/impl_20261105/cpu_ppc_instr.c.pre575
C=/tmp/gx575t
S1=src/cpus/cpu_ppc_instr.c
mkdir -p $OUT
log(){ echo "$(date +%H:%M:%S) $*" | tee -a $OUT/TABLE.log; }
[ -f $A/table1_20261105/PRETABLE.out ] || { log "ABORT: no PRETABLE.out"; exit 2; }
[ -f $P ] || { log "ABORT: no frozen probe"; exit 2; }
rm -rf $C && cp -a $G/build $C || { log "ABORT: clone failed"; exit 3; }
cd $C || exit 3
echo "$S1: #575 table 1; baseline GXEMUL-SEC" > .MUTANT
cp $FIX $OUT/cpu_ppc_instr.c.fix575
cmp -s $S1 $FIX || { log "ABORT: clone baseline is not the fix (propagate first)"; exit 4; }
md5sum $P $FIX $PRE $A/table1_20261105/variants/*.c $A/table1_20261105/PRETABLE.out > $OUT/MD5.txt; : > $OUT/SCORES.txt
build(){ rm -f src/cpus/cpu_ppc*.o; make -j4 > $OUT/build_$1.log 2>&1; local rc=$?
         [ $rc = 0 ] && [ src/cpus/cpu_ppc.o -nt $S1 ] && [ gxemul -nt src/cpus/cpu_ppc.o ] && return 0
         log "build $1 rc=$rc NOT FRESH"; return 1; }
run(){ python3 -u $P "$2" "$1" > $OUT/probe_$1.out 2>&1
       local r=$(grep -h "^PPC_CRLOGIC_RESULT=" $OUT/probe_$1.out | cut -d= -f2) c=$(grep -h "^PPC_CRLOGIC_CONTROL=" $OUT/probe_$1.out | cut -d= -f2)
       local d=$(grep -c "^PPC_CRLOGIC_PROBE_DONE" $OUT/probe_$1.out)
       local red=$(grep -E ' FAIL$' $OUT/probe_$1.out | cut -c1-19 | sed 's/ *$//; s/ /_/g' | paste -sd, -)
       echo "$1 [62 rows] ${r:-none} CONTROL=${c:-none} DONE=$d RED=${red:-none}" >> $OUT/SCORES.txt; log "$1 ${r:-none} RED=${red:-none}"; }
build base && run base $C/gxemul
cp $PRE $S1; build HEAD && run HEAD $C/gxemul
run null_true /bin/true; run null_absent /nonexistent/gxemul; run null_false /bin/false
for v in $A/table1_20261105/variants/*.c; do n=$(basename $v .c)
  cp $v $S1
  if build $n; then run $n $C/gxemul; else echo "$n [62 rows] BUILD-FAILED" >> $OUT/SCORES.txt; fi
done
cp $FIX $S1; build restored && run restored $C/gxemul
if cmp -s $S1 $FIX && [ gxemul -nt $S1 ]; then rm -f .MUTANT; log "restored: cmp clean vs SEC, binary fresh, sentinel cleared"
else log "RESTORE NOT VERIFIED -- sentinel kept"; fi
log TABLE1_575_DONE
